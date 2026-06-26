"""
Image Generator - Generate poster/slides images via Gemini native image generation API.
Uses the Runway/Nano Banana proxy to access Gemini's image generation capabilities.
"""
import io
import os
import json
import base64
import logging
import time
from pathlib import Path
from typing import List, Dict, Optional, Tuple

import requests

from .models import (
    ContentPlan, Section, GeneratedImage, FigureInfo,
)
from .prompts import (
    FORMAT_POSTER, FORMAT_SLIDE, FORMAT_SLIDE_VERTICAL,
    POSTER_STYLE_HINTS, SLIDE_STYLE_HINTS,
    SLIDE_LAYOUTS, VERTICAL_SLIDE_LAYOUTS,
    VISUALIZATION_HINTS,
    CONSISTENCY_HINT, FIGURE_HINT,
)

logger = logging.getLogger(__name__)


class GeminiImageGenerator:
    """Generate poster/slides images using Gemini native image generation API."""

    def __init__(
        self,
        api_key: str = None,
        timeout: int = 180,
        max_retries: int = 3,
    ):
        self.api_key = api_key or os.getenv("IMAGE_GEN_API_KEY")
        if not self.api_key:
            raise ValueError(
                "IMAGE_GEN_API_KEY is required. Set it in .env or pass api_key parameter."
            )
        self.timeout = timeout
        self.max_retries = max_retries

    @property
    def endpoint(self) -> str:
        """Get image generation endpoint from environment variable."""
        endpoint = os.getenv("IMAGE_GEN_ENDPOINT")
        if not endpoint:
            raise ValueError(
                "IMAGE_GEN_ENDPOINT is required. Set it in .env (e.g., https://runway.devops.rednote.life/openai/google/v1:generateContent)"
            )
        return endpoint

    def generate(
        self,
        plan: ContentPlan,
        style: str = "academic",
        figure_base_path: str = "",
        language: str = "auto",
        orientation: str = "landscape",
    ) -> List[GeneratedImage]:
        """Generate images from a ContentPlan.

        Args:
            orientation: 'landscape' (16:9) or 'portrait' (9:16)
        """
        figure_images = self._load_figure_images(plan, figure_base_path)
        all_sections_md = self._format_sections_markdown(plan)

        if plan.output_type == "poster":
            return self._generate_poster(style, all_sections_md, plan, figure_images, language)
        return self._generate_slides(
            plan, style, all_sections_md, figure_images, language, orientation
        )

    def _generate_poster(
        self,
        style: str,
        sections_md: str,
        plan: ContentPlan,
        figure_images: List[Dict],
        language: str = "auto",
    ) -> List[GeneratedImage]:
        """Generate a single poster image."""
        prompt = self._build_poster_prompt(style, sections_md, language)

        used_images = self._filter_images(plan.sections, figure_images)
        image_data, mime_type = self._call_gemini(prompt, used_images)
        return [GeneratedImage(
            section_id="poster",
            image_data=image_data,
            mime_type=mime_type,
        )]

    def _generate_slides(
        self,
        plan: ContentPlan,
        style: str,
        all_sections_md: str,
        figure_images: List[Dict],
        language: str = "auto",
        orientation: str = "landscape",
    ) -> List[GeneratedImage]:
        """Generate N slide images.

        Args:
            orientation: 'landscape' (16:9) or 'portrait' (9:16)
        """
        is_vertical = orientation == "portrait"
        aspect_ratio = "9:16" if is_vertical else "16:9"
        results = []
        style_ref_image = None

        for i, section in enumerate(plan.sections):
            section_md = self._format_single_section_markdown(section, plan)
            slide_info = f"Slide {i + 1} of {len(plan.sections)}"
            prompt = self._build_slide_prompt(
                style, section_md, all_sections_md, slide_info,
                section.section_type, language, is_vertical,
            )

            section_images = self._filter_images([section], figure_images)
            reference_images = []
            if style_ref_image:
                reference_images.append(style_ref_image)
            reference_images.extend(section_images)

            image_data, mime_type = self._call_gemini(
                prompt, reference_images, section.id, aspect_ratio=aspect_ratio,
            )

            if i == 1 and image_data:
                style_ref_image = {
                    "figure_id": "Reference Slide",
                    "caption": "Maintain consistent style",
                    "base64": base64.b64encode(image_data).decode("utf-8"),
                    "mime_type": mime_type,
                }

            results.append(GeneratedImage(
                section_id=section.id,
                image_data=image_data,
                mime_type=mime_type,
            ))
            logger.info("Generated slide %d/%d: %s", i + 1, len(plan.sections), section.id)

        return results

    # ------------------------------------------------------------------
    # Prompt builders
    # ------------------------------------------------------------------

    def _build_poster_prompt(self, style: str, sections_md: str, language: str = "auto") -> str:
        style_hint = POSTER_STYLE_HINTS.get(style, POSTER_STYLE_HINTS.get("academic", ""))
        
        # 根据语言设置添加语言指令
        language_hint = self._get_language_hint(language, sections_md)
        
        parts = [
            FORMAT_POSTER,
            style_hint,
            language_hint,
            VISUALIZATION_HINTS,
            FIGURE_HINT,
            "---",
            "Content:",
            sections_md,
        ]
        return "\n\n".join(parts)
    
    def _get_language_hint(self, language: str, content: str) -> str:
        """根据语言设置返回相应的语言提示."""
        if language == "zh":
            return "LANGUAGE: ALL text MUST be in Chinese (中文)."
        elif language == "en":
            return "LANGUAGE: ALL text MUST be in English."
        elif language == "auto":
            # 检测内容中的中文字符比例
            chinese_chars = len([c for c in content if '\u4e00' <= c <= '\u9fff'])
            total_chars = len(content.replace(' ', '').replace('\n', ''))
            if total_chars > 0 and chinese_chars / total_chars > 0.1:
                return "LANGUAGE: Use Chinese (中文) to match the content."
            else:
                return "LANGUAGE: Use English to match the content."
        return ""

    def _build_slide_prompt(
        self,
        style: str,
        section_md: str,
        context_md: str,
        slide_info: str,
        section_type: str,
        language: str = "auto",
        vertical: bool = False,
    ) -> str:
        style_hint = SLIDE_STYLE_HINTS.get(style, SLIDE_STYLE_HINTS.get("academic", ""))

        if vertical:
            format_hint = FORMAT_SLIDE_VERTICAL
            layout_map = VERTICAL_SLIDE_LAYOUTS.get(style, VERTICAL_SLIDE_LAYOUTS.get("academic", {}))
        else:
            format_hint = FORMAT_SLIDE
            layout_map = SLIDE_LAYOUTS.get(style, SLIDE_LAYOUTS.get("academic", {}))
        layout = layout_map.get(section_type, layout_map.get("content", ""))

        language_hint = self._get_language_hint(language, section_md)

        parts = [
            format_hint,
            style_hint,
            language_hint,
            layout,
            VISUALIZATION_HINTS,
            FIGURE_HINT,
            CONSISTENCY_HINT,
            slide_info,
            "---",
            "Full context:",
            context_md,
            "---",
            "This slide:",
            section_md,
        ]
        return "\n\n".join(parts)

    # ------------------------------------------------------------------
    # Gemini API call
    # ------------------------------------------------------------------

    def _call_gemini(
        self,
        prompt: str,
        reference_images: Optional[List[Dict]] = None,
        section_id: str = "",
        aspect_ratio: str = "16:9",
    ) -> Tuple[bytes, str]:
        """Call Gemini native API for image generation with retry."""
        parts = self._build_gemini_parts(prompt, reference_images)

        logger.info("=" * 60)
        logger.info("[GEMINI PROMPT] Section: %s | Aspect: %s", section_id or "unknown", aspect_ratio)
        logger.info("[GEMINI PROMPT] Content:\n%s", prompt)
        logger.info("[GEMINI PROMPT] Reference images count: %d", len(reference_images or []))
        logger.info("=" * 60)

        payload = {
            "contents": [{"role": "user", "parts": parts}],
            "generationConfig": {
                "responseModalities": ["TEXT", "IMAGE"],
                "temperature": 0.6,
                "imageConfig": {
                    "aspectRatio": aspect_ratio,
                    "imageOutputOptions": {"mimeType": "image/png"},
                },
            },
        }

        headers = {
            "Content-Type": "application/json",
            "api-key": self.api_key,
        }

        for attempt in range(1, self.max_retries + 1):
            try:
                logger.info(
                    "Gemini image gen request (attempt %d/%d) to %s",
                    attempt, self.max_retries, self.endpoint,
                )
                resp = requests.post(
                    self.endpoint,
                    headers=headers,
                    json=payload,
                    timeout=self.timeout,
                )

                if resp.status_code >= 400:
                    error_msg = resp.text[:500]
                    logger.warning(
                        "Gemini API returned %d: %s", resp.status_code, error_msg
                    )
                    if attempt < self.max_retries:
                        time.sleep(2 ** attempt)
                        continue
                    raise RuntimeError(
                        f"Gemini API error after {self.max_retries} retries: "
                        f"HTTP {resp.status_code}: {error_msg}"
                    )

                return self._parse_gemini_image_response(resp.json())

            except requests.exceptions.Timeout:
                logger.warning("Gemini API timeout (attempt %d/%d)", attempt, self.max_retries)
                if attempt < self.max_retries:
                    time.sleep(2 ** attempt)
                    continue
                raise
            except RuntimeError:
                raise
            except Exception as e:
                logger.error("Gemini API call failed: %s", e)
                if attempt < self.max_retries:
                    time.sleep(2 ** attempt)
                    continue
                raise

        raise RuntimeError("Gemini image generation failed after all retries")

    def _build_gemini_parts(
        self, prompt: str, reference_images: Optional[List[Dict]]
    ) -> List[Dict]:
        """Build Gemini API parts array with text and optional images."""
        parts = []

        if reference_images:
            for img in reference_images:
                if img.get("caption"):
                    parts.append({"text": f"Reference - {img['figure_id']}: {img['caption']}"})
                parts.append({
                    "inlineData": {
                        "mimeType": img["mime_type"],
                        "data": img["base64"],
                    }
                })

        parts.append({"text": prompt})
        return parts

    def _parse_gemini_image_response(self, resp_json: Dict) -> Tuple[bytes, str]:
        """Extract image data from Gemini response."""
        if "error" in resp_json:
            raise RuntimeError(f"Gemini API error: {resp_json['error']}")

        candidates = resp_json.get("candidates", [])
        if not candidates:
            raise RuntimeError(f"No candidates in Gemini response: {json.dumps(resp_json)[:500]}")

        parts = candidates[0].get("content", {}).get("parts", [])

        for part in parts:
            inline_data = part.get("inlineData")
            if inline_data and inline_data.get("data"):
                mime_type = inline_data.get("mimeType", "image/png")
                image_bytes = base64.b64decode(inline_data["data"])
                logger.info(
                    "Received image: %s, %d bytes", mime_type, len(image_bytes)
                )
                return image_bytes, mime_type

        text_parts = [p.get("text", "") for p in parts if "text" in p]
        raise RuntimeError(
            f"No image in Gemini response. Text parts: {' '.join(text_parts)[:500]}"
        )

    # ------------------------------------------------------------------
    # Section formatting helpers
    # ------------------------------------------------------------------

    def _format_sections_markdown(self, plan: ContentPlan) -> str:
        return "\n\n---\n\n".join(
            self._format_single_section_markdown(s, plan) for s in plan.sections
        )

    def _format_single_section_markdown(self, section: Section, plan: ContentPlan) -> str:
        lines = [f"## {section.title}", "", section.content]

        for ref in section.tables:
            table = plan.tables_index.get(ref.table_id)
            if table:
                lines.extend(["", f"**{ref.table_id}**:", ref.extract or table.html_content])

        for ref in section.figures:
            fig = plan.figures_index.get(ref.figure_id)
            if fig:
                lines.extend(["", f"**{ref.figure_id}**: {fig.caption or ''}", "[Image attached]"])

        return "\n".join(lines)

    def _load_figure_images(self, plan: ContentPlan, base_path: str) -> List[Dict]:
        images = []
        mime_map = {
            ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
            ".png": "image/png", ".webp": "image/webp",
        }
        for fig_id, fig in plan.figures_index.items():
            img_path = Path(base_path) / fig.image_path if base_path else Path(fig.image_path)
            if not img_path.exists():
                continue
            try:
                img_data = base64.b64encode(img_path.read_bytes()).decode("utf-8")
                images.append({
                    "figure_id": fig_id,
                    "caption": fig.caption,
                    "base64": img_data,
                    "mime_type": mime_map.get(img_path.suffix.lower(), "image/jpeg"),
                })
            except Exception:
                continue
        return images

    def _filter_images(self, sections: List[Section], figure_images: List[Dict]) -> List[Dict]:
        used_ids = {ref.figure_id for section in sections for ref in section.figures}
        return [img for img in figure_images if img.get("figure_id") in used_ids]


def save_images_as_pdf(images: List[GeneratedImage], output_path: str):
    """Save generated images as a single PDF file."""
    from PIL import Image

    pdf_images = []
    for img in images:
        pil_img = Image.open(io.BytesIO(img.image_data))
        if pil_img.mode != "RGB":
            pil_img = pil_img.convert("RGB")
        pdf_images.append(pil_img)

    if pdf_images:
        pdf_images[0].save(
            output_path,
            save_all=True,
            append_images=pdf_images[1:] if len(pdf_images) > 1 else [],
            resolution=100.0,
        )
