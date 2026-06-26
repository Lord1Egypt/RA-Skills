"""视觉大模型兜底：扫描页 / lines+text 都失败的页或低置信表格。

错误处理见 SKILL.md "异常处理决策树 E003"。
配置来源：环境变量 ARK_API_KEY / ARK_BASE_URL（或 OPENAI_API_KEY）。
"""
from __future__ import annotations

import base64
import io
import json
import os
import re
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


@dataclass
class VLMConfig:
    provider: str = "ark"                                              # ark / openai / ollama
    model: str = "doubao-1.5-vision-pro"
    base_url: str = ""
    api_key: str = ""
    max_retries: int = 3
    retry_backoff_seconds: tuple[int, ...] = (1, 2, 4)
    timeout_seconds: int = 60
    dpi: int = 200


def vlm_config_from_env() -> VLMConfig | None:
    """从环境变量构造 VLMConfig；密钥缺失返回 None。"""
    api_key = os.environ.get("ARK_API_KEY") or os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        return None
    base_url = os.environ.get("ARK_BASE_URL") or os.environ.get("OPENAI_BASE_URL", "")
    if not base_url and os.environ.get("ARK_API_KEY"):
        base_url = "https://ark.cn-beijing.volces.com/api/v3"           # ARK 默认
    return VLMConfig(
        provider="ark" if os.environ.get("ARK_API_KEY") else "openai",
        model=os.environ.get("VLM_MODEL", "doubao-1.5-vision-pro"),
        base_url=base_url,
        api_key=api_key,
    )


class VLMError(RuntimeError):
    pass


# ─────────────────────────── 渲染 PDF → PNG ───────────────────────────


def render_page_to_image(pdf_path: str, page_index_1based: int,
                         dpi: int = 200) -> bytes:
    """单页 → PNG bytes。用 PyMuPDF 避免再装 pdf2image。"""
    import fitz                                                          # PyMuPDF
    doc = fitz.open(pdf_path)
    try:
        page = doc[page_index_1based - 1]
        zoom = dpi / 72                                                  # PDF 默认 72 dpi
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat, alpha=False)
        return pix.tobytes("png")
    finally:
        doc.close()


# ─────────────────────────── 调 VLM ───────────────────────────


_DEFAULT_PROMPT = """你是金融报表表格识别助手。图片是一份财务报告的一页。
请把页面上的所有表格抽取为 JSON，格式严格如下：
{"tables": [{"rows": [["单元格1","单元格2", ...], ...]}, ...]}

约束：
1. 数字保留原文千分位和小数点（如 "1,234,567.89"），不要做单位换算
2. 空白单元格用空字符串
3. 合并单元格的非锚位置用空字符串，文本只放在锚位置
4. 不要输出任何 Markdown 代码块或解释文字，只输出原始 JSON
5. 页面没有表格时输出 {"tables": []}
"""


def _strip_code_fence(s: str) -> str:
    """模型常会在 JSON 外包 ```json ... ``` 围栏，剥掉。"""
    s = s.strip()
    m = re.match(r"```(?:json)?\s*(.*?)```\s*$", s, re.DOTALL)
    return m.group(1).strip() if m else s


def call_vlm(image_bytes: bytes, prompt: str = _DEFAULT_PROMPT,
             cfg: VLMConfig | None = None) -> dict:
    """调 VLM 返回结构化结果 {"tables": [...]}。

    使用 OpenAI 兼容 client，可对接 ARK / OpenAI / Ollama。
    指数退避重试，失败抛 VLMError。
    """
    if cfg is None:
        cfg = vlm_config_from_env()
    if cfg is None or not cfg.api_key:
        raise VLMError("VLM not configured (ARK_API_KEY / OPENAI_API_KEY missing)")

    try:
        from openai import OpenAI
    except ImportError as e:                                             # pragma: no cover
        raise VLMError(f"openai SDK not installed: {e}")

    client = OpenAI(
        api_key=cfg.api_key,
        base_url=cfg.base_url or None,
        timeout=cfg.timeout_seconds,
    )
    b64 = base64.b64encode(image_bytes).decode("ascii")
    image_url = f"data:image/png;base64,{b64}"

    last_err: Exception | None = None
    for attempt in range(cfg.max_retries):
        try:
            resp = client.chat.completions.create(
                model=cfg.model,
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": image_url}},
                    ],
                }],
            )
            content = resp.choices[0].message.content or ""
            content = _strip_code_fence(content)
            try:
                return json.loads(content)
            except json.JSONDecodeError as e:
                raise VLMError(f"VLM 返回非 JSON: {e}; head={content[:200]!r}")
        except VLMError:
            raise                                                        # 解析错不重试
        except Exception as e:                                           # API 错误重试
            last_err = e
            if attempt < cfg.max_retries - 1:
                delay = cfg.retry_backoff_seconds[
                    min(attempt, len(cfg.retry_backoff_seconds) - 1)]
                time.sleep(delay)
    raise VLMError(f"VLM 调用失败（{cfg.max_retries} 次重试）: {last_err}")


# ─────────────────────────── 整页 → list[Table] ───────────────────────────


def extract_tables_via_vlm(pdf_path: str, page_index_1based: int,
                           cfg: VLMConfig | None = None) -> list:
    """渲染该页 → 调 VLM → 解析 JSON → 返回 Table dataclass 列表。

    Returns: list[table_extractor.Table]
    """
    # 延迟 import 避免循环
    from table_extractor import (
        Table, TableCell, _PageTable, _rows_to_table,
        _clean_table_rows_with_indices, self_assess,
    )

    if cfg is None:
        cfg = vlm_config_from_env()
    if cfg is None:
        raise VLMError("VLM not configured")

    import fitz
    doc = fitz.open(pdf_path)
    page_height = doc[page_index_1based - 1].rect.height
    page_width = doc[page_index_1based - 1].rect.width
    doc.close()

    img_bytes = render_page_to_image(pdf_path, page_index_1based, cfg.dpi)
    data = call_vlm(img_bytes, cfg=cfg)

    tables_out: list = []
    for raw in data.get("tables", []):
        rows_raw = raw.get("rows", [])
        if not rows_raw:
            continue
        cleaned, _ = _clean_table_rows_with_indices(rows_raw)
        if not cleaned:
            continue
        pt = _PageTable(
            page=page_index_1based,
            page_height=page_height,
            bbox=(0.0, 0.0, page_width, page_height),                    # VLM 不给精确 bbox
            rows=cleaned,
            engine="vlm",
            spans={},                                                    # VLM 不给 spans
        )
        t = _rows_to_table(pt)
        t.confidence = self_assess(t)
        tables_out.append(t)
    return tables_out
