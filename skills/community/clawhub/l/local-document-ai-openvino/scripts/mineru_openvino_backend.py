#!/usr/bin/env python3
"""
Runtime helpers for MinerU 2.5 on OpenVINO GenAI.

This module is adapted from the official OpenVINO MinerU notebook helper and
kept focused on runtime inference. The local-document-ai-openvino skill uses
preconverted OpenVINO model bundles and does not require local export.
"""

from __future__ import annotations

import io
import logging
from pathlib import Path
from typing import Iterable, List, Optional, Sequence, Tuple, Union

import numpy as np
import openvino as ov
import openvino_genai as ov_genai
from PIL import Image

from mineru_vl_utils.mineru_client import (
    DEFAULT_PROMPTS,
    DEFAULT_SAMPLING_PARAMS,
    MinerUClientHelper,
)
from mineru_vl_utils.post_process import json2md
from mineru_vl_utils.post_process.table_image_processor import (
    TABLE_IMAGE_TOKEN_MAP_KEY,
    replace_table_image_tokens,
)
from mineru_vl_utils.structs import ExtractResult
from mineru_vl_utils.vlm_client.base_client import SamplingParams


logger = logging.getLogger(__name__)

ImageInput = Union[Image.Image, str, Path, bytes]


def _pil_to_ov_tensor(image: Image.Image) -> ov.Tensor:
    image = image.convert("RGB")
    array = np.array(image, dtype=np.uint8)
    array = array[None, ...]
    return ov.Tensor(array)


def _load_image(src: ImageInput) -> Image.Image:
    if isinstance(src, Image.Image):
        return src
    if isinstance(src, (bytes, bytearray)):
        return Image.open(io.BytesIO(src))
    return Image.open(str(src))


def pdf_to_images(pdf: Union[str, Path, bytes], dpi: int = 200) -> List[Image.Image]:
    import pypdfium2 as pdfium

    if isinstance(pdf, (str, Path)):
        doc = pdfium.PdfDocument(str(pdf))
    else:
        doc = pdfium.PdfDocument(pdf)

    scale = dpi / 72.0
    pages: List[Image.Image] = []
    for index in range(len(doc)):
        page = doc[index]
        rendered = page.render(scale=scale).to_pil().convert("RGB")
        pages.append(rendered)
        page.close()
    doc.close()
    return pages


class OVMinerUClient:
    """OpenVINO inference client for MinerU 2.5 document parsing."""

    def __init__(
        self,
        model_dir: Union[str, Path],
        device: str = "AUTO",
        prompts: Optional[dict] = None,
        sampling_params: Optional[dict] = None,
        layout_image_size: Tuple[int, int] = (1036, 1036),
        min_image_edge: int = 28,
        max_image_edge_ratio: float = 50.0,
        image_analysis: bool = False,
        debug: bool = False,
        ov_config: Optional[dict] = None,
    ) -> None:
        self.model_dir = Path(model_dir)
        self.device = device
        self.pipe = ov_genai.VLMPipeline(
            str(self.model_dir),
            device=device,
            **(ov_config or {}),
        )
        self.helper = MinerUClientHelper(
            backend="openvino",
            prompts=prompts or DEFAULT_PROMPTS,
            sampling_params=sampling_params or DEFAULT_SAMPLING_PARAMS,
            layout_image_size=layout_image_size,
            min_image_edge=min_image_edge,
            max_image_edge_ratio=max_image_edge_ratio,
            simple_post_process=False,
            handle_equation_block=True,
            abandon_list=False,
            abandon_paratext=False,
            image_analysis=image_analysis,
            debug=debug,
        )

    def _build_generation_config(self, sp: Optional[SamplingParams]) -> ov_genai.GenerationConfig:
        cfg = ov_genai.GenerationConfig()
        cfg.max_new_tokens = sp.max_new_tokens if sp and sp.max_new_tokens else 4096

        if sp is not None:
            do_sample = (sp.temperature or 0.0) > 0.0 and (sp.top_k or 1) > 1
            cfg.do_sample = do_sample
            if do_sample:
                if sp.temperature is not None:
                    cfg.temperature = float(sp.temperature)
                if sp.top_p is not None:
                    cfg.top_p = float(sp.top_p)
                if sp.top_k is not None:
                    cfg.top_k = int(sp.top_k)
            if sp.repetition_penalty is not None:
                cfg.repetition_penalty = float(sp.repetition_penalty)
            if sp.presence_penalty is not None:
                try:
                    cfg.presence_penalty = float(sp.presence_penalty)
                except AttributeError:
                    pass
            if sp.frequency_penalty is not None:
                try:
                    cfg.frequency_penalty = float(sp.frequency_penalty)
                except AttributeError:
                    pass
            if sp.no_repeat_ngram_size is not None:
                try:
                    cfg.no_repeat_ngram_size = int(sp.no_repeat_ngram_size)
                except AttributeError:
                    pass
        else:
            cfg.do_sample = False
        return cfg

    def _predict(self, image: Image.Image, prompt: str, sp: Optional[SamplingParams]) -> str:
        cfg = self._build_generation_config(sp)
        tensor = _pil_to_ov_tensor(image)
        result = self.pipe.generate(prompt, image=tensor, generation_config=cfg)
        return str(result)

    def two_step_extract(
        self,
        image: ImageInput,
        not_extract_list: Optional[Sequence[str]] = None,
        image_analysis: Optional[bool] = None,
    ) -> ExtractResult:
        page = _load_image(image).convert("RGB")

        layout_image = self.helper.prepare_for_layout(page)
        layout_prompt = self.helper.prompts["[layout]"]
        layout_sp = self.helper.sampling_params.get("[layout]")
        layout_text = self._predict(layout_image, layout_prompt, layout_sp)
        blocks = self.helper.parse_layout_output(layout_text)

        block_images, prompts, sps, indices = self.helper.prepare_for_extract(
            page,
            blocks,
            not_extract_list=list(not_extract_list) if not_extract_list else None,
            image_analysis=image_analysis,
        )
        for block_image, prompt, sp, idx in zip(block_images, prompts, sps, indices):
            content = self._predict(block_image, prompt, sp)
            block = blocks[idx]
            if TABLE_IMAGE_TOKEN_MAP_KEY in block:
                token_map = block.get(TABLE_IMAGE_TOKEN_MAP_KEY) or {}
                if token_map:
                    content = replace_table_image_tokens(content, token_map)
            block["content"] = content

        blocks = self.helper.post_process(blocks)
        return ExtractResult(blocks)

    def image_to_markdown(self, image: ImageInput, **kwargs) -> Tuple[str, ExtractResult]:
        blocks = self.two_step_extract(image, **kwargs)
        return json2md(list(blocks)), blocks

    def pdf_to_markdown(
        self,
        pdf: Union[str, Path, bytes],
        dpi: int = 200,
        progress_callback=None,
        **kwargs,
    ) -> Tuple[str, List[ExtractResult]]:
        pages = pdf_to_images(pdf, dpi=dpi)
        md_pages: List[str] = []
        block_pages: List[ExtractResult] = []
        for index, page in enumerate(pages):
            if progress_callback is not None:
                progress_callback(index, len(pages))
            markdown, blocks = self.image_to_markdown(page, **kwargs)
            md_pages.append(markdown)
            block_pages.append(blocks)
        if progress_callback is not None:
            progress_callback(len(pages), len(pages))
        joined = "\n\n---\n\n".join(md_pages)
        return joined, block_pages


def render_blocks_overlay(image: Image.Image, blocks: Iterable[dict]) -> Image.Image:
    from PIL import ImageDraw, ImageFont

    canvas = image.convert("RGB").copy()
    draw = ImageDraw.Draw(canvas)
    width, height = canvas.size
    try:
        font = ImageFont.truetype("arial.ttf", max(12, height // 80))
    except OSError:
        font = ImageFont.load_default()

    palette = {
        "text": "#1f77b4",
        "title": "#d62728",
        "table": "#2ca02c",
        "equation": "#9467bd",
        "image": "#ff7f0e",
        "chart": "#8c564b",
    }
    for block in blocks:
        btype = block.get("type", "text")
        bbox = block.get("bbox") or [0, 0, 0, 0]
        if len(bbox) != 4:
            continue
        x1, y1, x2, y2 = bbox
        color = palette.get(btype, "#7f7f7f")
        draw.rectangle((x1 * width, y1 * height, x2 * width, y2 * height), outline=color, width=2)
        draw.text((x1 * width + 2, y1 * height + 2), btype, fill=color, font=font)
    return canvas
