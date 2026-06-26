"""
Content Planner - Plans content structure for poster/slides image generation.
Uses multimodal LLM (VLM) to analyze markdown content and plan sections.
Ported and adapted from Paper2Slides project.
"""
import json
import base64
import re
import os
import logging
from pathlib import Path
from typing import List, Dict, Optional
from openai import OpenAI

from .models import (
    TableRef, FigureRef, Section, ContentPlan,
    TableInfo, FigureInfo,
)
from .prompts import (
    SLIDES_PLANNING_PROMPT,
    POSTER_PLANNING_PROMPT,
    POSTER_DENSITY_GUIDELINES,
    SLIDES_PAGE_RANGES,
)

logger = logging.getLogger(__name__)


class ContentPlanner:
    """Plans content structure using multimodal LLM."""

    def __init__(self, model: str = None, api_key: str = None, base_url: str = None):
        self.model = model or os.getenv("TEXT_MODEL", "qwen3-vl-235b-a22b-instruct")
        self.client = OpenAI(
            api_key=api_key or os.getenv("OPENAI_API_KEY"),
            base_url=base_url or os.getenv("OPENAI_BASE_URL"),
        )

    def plan(
        self,
        markdown_text: str,
        output_type: str = "poster",
        tables: Optional[List[TableInfo]] = None,
        figures: Optional[List[FigureInfo]] = None,
        figure_base_path: str = "",
        density: str = "medium",
        slides_length: str = "medium",
        language: str = "auto",
    ) -> ContentPlan:
        """Create a content plan from markdown text and extracted assets."""
        tables = tables or []
        figures = figures or []

        tables_index = {t.table_id: t for t in tables}
        figures_index = {f.figure_id: f for f in figures}

        tables_md = self._format_tables_markdown(tables)
        figure_images = self._load_figure_images(figures, figure_base_path)

        if output_type == "poster":
            sections = self._plan_poster(markdown_text, tables_md, figure_images, density, language)
        else:
            sections = self._plan_slides(markdown_text, tables_md, figure_images, slides_length, language)

        return ContentPlan(
            output_type=output_type,
            sections=sections,
            tables_index=tables_index,
            figures_index=figures_index,
            metadata={
                "density": density if output_type == "poster" else None,
                "page_range": SLIDES_PAGE_RANGES.get(slides_length, (8, 12))
                    if output_type == "slides" else None,
            },
        )

    def plan_from_parser_results(
        self,
        parser_results: Dict,
        output_type: str = "poster",
        density: str = "medium",
        slides_length: str = "medium",
        language: str = "auto",
    ) -> ContentPlan:
        """Create a content plan directly from PosterGenParserUnit output."""
        md_path = parser_results["raw_text_path"]
        figures_path = parser_results.get("figures_path", "")
        tables_path = parser_results.get("tables_path", "")

        markdown_text = Path(md_path).read_text(encoding="utf-8")

        tables = self._load_tables_from_json(tables_path)
        figures = self._load_figures_from_json(figures_path)
        figure_base_path = str(Path(figures_path).parent) if figures_path else ""

        return self.plan(
            markdown_text=markdown_text,
            output_type=output_type,
            tables=tables,
            figures=figures,
            figure_base_path=figure_base_path,
            density=density,
            slides_length=slides_length,
            language=language,
        )

    def _plan_slides(
        self,
        summary: str,
        tables_md: str,
        figure_images: List[Dict],
        slides_length: str,
        language: str = "auto",
    ) -> List[Section]:
        min_pages, max_pages = SLIDES_PAGE_RANGES.get(slides_length, (8, 12))
        assets_section = self._build_assets_section(tables_md, bool(figure_images))
        
        # 构建语言指令
        language_instruction = self._get_language_instruction(language, summary)

        prompt = SLIDES_PLANNING_PROMPT.format(
            min_pages=min_pages,
            max_pages=max_pages,
            summary=self._truncate(summary, 10000),
            assets_section=assets_section,
        )
        
        # 在 prompt 后添加语言指令
        if language_instruction:
            prompt = f"{prompt}\n\n## Language Requirement\n{language_instruction}"

        result = self._call_multimodal_llm(prompt, figure_images)
        return self._parse_sections(result, is_slides=True)

    def _plan_poster(
        self,
        summary: str,
        tables_md: str,
        figure_images: List[Dict],
        density: str,
        language: str = "auto",
    ) -> List[Section]:
        density_guidelines = POSTER_DENSITY_GUIDELINES.get(
            density, POSTER_DENSITY_GUIDELINES["medium"]
        )
        assets_section = self._build_assets_section(tables_md, bool(figure_images))
        
        # 构建语言指令
        language_instruction = self._get_language_instruction(language, summary)

        prompt = POSTER_PLANNING_PROMPT.format(
            density_guidelines=density_guidelines,
            summary=self._truncate(summary, 10000),
            assets_section=assets_section,
        )
        
        # 在 prompt 后添加语言指令
        if language_instruction:
            prompt = f"{prompt}\n\n## Language Requirement\n{language_instruction}"

        result = self._call_multimodal_llm(prompt, figure_images)
        return self._parse_sections(result, is_slides=False)
    
    def _get_language_instruction(self, language: str, content: str) -> str:
        """根据语言设置返回相应的语言指令."""
        if language == "zh":
            return "ALL content MUST be in Chinese (中文). Do not use English."
        elif language == "en":
            return "ALL content MUST be in English. Do not use Chinese or other languages."
        elif language == "auto":
            # 自动检测内容语言
            # 简单启发式：如果内容中中文字符比例较高，则使用中文
            chinese_chars = len([c for c in content if '\u4e00' <= c <= '\u9fff'])
            total_chars = len(content.replace(' ', '').replace('\n', ''))
            if total_chars > 0 and chinese_chars / total_chars > 0.1:
                return "MATCH THE LANGUAGE of the input content (which appears to be Chinese). Use Chinese (中文) for all output."
            else:
                return "MATCH THE LANGUAGE of the input content (which appears to be English). Use English for all output."
        return ""

    def _build_assets_section(self, tables_md: str, has_figures: bool) -> str:
        has_tables = bool(tables_md)
        if not has_tables and not has_figures:
            return ""

        parts = ["\n## Original Tables and Figures"]
        if has_tables and has_figures:
            parts.append("Below are the original tables and figures. Use them to supplement the content.")
        elif has_tables:
            parts.append("Below are the original tables. Use them to supplement the content.")
        else:
            parts.append("Below are the original figures. Use them to supplement the content.")

        if has_tables:
            parts.append(f"\n{tables_md}")
        if has_figures:
            parts.append("\n[FIGURE_IMAGES]")
        parts.append("")
        return "\n".join(parts)

    def _call_multimodal_llm(self, text_prompt: str, figure_images: List[Dict]) -> str:
        MARKER = "[FIGURE_IMAGES]"
        content = []

        if MARKER in text_prompt and figure_images:
            before, after = text_prompt.split(MARKER, 1)
            if before.strip():
                content.append({"type": "text", "text": before})

            for fig in figure_images:
                caption_text = f"**{fig['figure_id']}**: {fig['caption']}" if fig.get("caption") else f"**{fig['figure_id']}**"
                content.append({"type": "text", "text": caption_text})
                content.append({
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:{fig['mime_type']};base64,{fig['base64']}",
                    }
                })

            if after.strip():
                content.append({"type": "text", "text": after})
            logger.info("Calling LLM with %d images", len(figure_images))
        else:
            content.append({"type": "text", "text": text_prompt})
            logger.info("Calling LLM with text only (no images)")

        try:
            logger.info("Calling %s with max_tokens=16000", self.model)
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": content}],
                max_tokens=16000,
            )
            result = response.choices[0].message.content or ""
            logger.info("LLM returned %d characters", len(result))
            return result
        except Exception as e:
            logger.error("LLM API call failed: %s", e)
            raise

    def _parse_sections(self, llm_response: str, is_slides: bool = True) -> List[Section]:
        json_match = re.search(r'```json\s*(.*?)\s*```', llm_response, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
        else:
            json_match = re.search(r'\{.*\}', llm_response, re.DOTALL)
            json_str = json_match.group(0) if json_match else "{}"

        json_str = self._fix_invalid_escapes(json_str)
        data = json.loads(json_str)
        items = data.get("slides") or data.get("sections") or []

        sections = []
        total = len(items)
        for idx, item in enumerate(items):
            tables = [
                TableRef(
                    table_id=t.get("table_id", ""),
                    extract=t.get("extract", ""),
                    focus=t.get("focus", ""),
                ) for t in item.get("tables", [])
            ]
            figures = [
                FigureRef(
                    figure_id=f.get("figure_id", ""),
                    focus=f.get("focus", ""),
                ) for f in item.get("figures", [])
            ]

            if is_slides:
                if idx == 0:
                    section_type = "opening"
                elif idx == total - 1:
                    section_type = "ending"
                else:
                    section_type = "content"
            else:
                section_type = "content"

            sections.append(Section(
                id=item.get("id", f"section_{idx + 1}"),
                title=item.get("title", ""),
                section_type=section_type,
                content=item.get("content", ""),
                tables=tables,
                figures=figures,
            ))
        return sections

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _load_tables_from_json(self, tables_path: str) -> List[TableInfo]:
        if not tables_path or not Path(tables_path).exists():
            return []
        try:
            data = json.loads(Path(tables_path).read_text(encoding="utf-8"))
            return [
                TableInfo(
                    table_id=t.get("id", t.get("table_id", f"Table {i+1}")),
                    caption=t.get("caption", ""),
                    html_content=t.get("html", t.get("html_content", "")),
                ) for i, t in enumerate(data)
            ]
        except Exception:
            return []

    def _load_figures_from_json(self, figures_path: str) -> List[FigureInfo]:
        if not figures_path or not Path(figures_path).exists():
            return []
        try:
            data = json.loads(Path(figures_path).read_text(encoding="utf-8"))
            return [
                FigureInfo(
                    figure_id=f.get("id", f.get("figure_id", f"Figure {i+1}")),
                    caption=f.get("caption"),
                    image_path=f.get("path", f.get("image_path", "")),
                ) for i, f in enumerate(data)
            ]
        except Exception:
            return []

    def _format_tables_markdown(self, tables: List[TableInfo]) -> str:
        if not tables:
            return ""
        parts = [t.to_markdown() for t in tables]
        return "\n\n---\n\n".join(parts)

    def _load_figure_images(self, figures: List[FigureInfo], base_path: str) -> List[Dict]:
        images = []
        mime_map = {
            ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
            ".png": "image/png", ".webp": "image/webp", ".gif": "image/gif",
        }
        for fig in figures:
            img_path = Path(base_path) / fig.image_path if base_path else Path(fig.image_path)
            if not img_path.exists():
                continue
            suffix = img_path.suffix.lower()
            mime_type = mime_map.get(suffix, "image/jpeg")
            try:
                img_data = base64.b64encode(img_path.read_bytes()).decode("utf-8")
                images.append({
                    "figure_id": fig.figure_id,
                    "caption": fig.caption,
                    "base64": img_data,
                    "mime_type": mime_type,
                })
            except Exception:
                continue
        return images

    @staticmethod
    def _fix_invalid_escapes(s: str) -> str:
        result = []
        i = 0
        while i < len(s):
            if s[i] == '\\' and i + 1 < len(s):
                next_char = s[i + 1]
                if next_char in ('"', '\\', '/', 'b', 'f', 'n', 'r', 't', 'u'):
                    result.append(s[i:i + 2])
                    i += 2
                else:
                    result.append('\\\\')
                    result.append(next_char)
                    i += 2
            else:
                result.append(s[i])
                i += 1
        return ''.join(result)

    @staticmethod
    def _truncate(text: str, max_len: int) -> str:
        if len(text) <= max_len:
            return text
        return text[:max_len] + "\n\n[Content truncated...]"
