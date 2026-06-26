"""
Data models for content planning and image generation.
Ported from Paper2Slides project.
"""
import json
import re
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class TableRef:
    """Table reference for a section."""
    table_id: str
    extract: str = ""
    focus: str = ""


@dataclass
class FigureRef:
    """Figure reference for a section."""
    figure_id: str
    focus: str = ""


@dataclass
class Section:
    """A single section/slide in the output."""
    id: str
    title: str
    section_type: str
    content: str
    tables: List[TableRef] = field(default_factory=list)
    figures: List[FigureRef] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        result = {
            "id": self.id,
            "title": self.title,
            "type": self.section_type,
            "content": self.content,
        }
        result["tables"] = []
        for t in self.tables:
            t_dict = {"table_id": t.table_id}
            if t.extract:
                t_dict["extract"] = t.extract
            if t.focus:
                t_dict["focus"] = t.focus
            result["tables"].append(t_dict)

        result["figures"] = []
        for f in self.figures:
            f_dict = {"figure_id": f.figure_id}
            if f.focus:
                f_dict["focus"] = f.focus
            result["figures"].append(f_dict)

        return result


@dataclass
class TableInfo:
    """Information about an extracted table."""
    table_id: str
    caption: str = ""
    html_content: str = ""

    def to_markdown(self) -> str:
        return f"**{self.table_id}**: {self.caption}\n\n{self.html_content}"


@dataclass
class FigureInfo:
    """Information about an extracted figure."""
    figure_id: str
    caption: Optional[str] = None
    image_path: str = ""


@dataclass
class ContentPlan:
    """Planned content structure for generation."""
    output_type: str
    sections: List[Section] = field(default_factory=list)
    tables_index: Dict[str, TableInfo] = field(default_factory=dict)
    figures_index: Dict[str, FigureInfo] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def get_section_tables(self, section: Section) -> List[tuple]:
        result = []
        for ref in section.tables:
            if ref.table_id in self.tables_index:
                result.append((self.tables_index[ref.table_id], ref.extract))
        return result

    def get_section_figures(self, section: Section) -> List[tuple]:
        result = []
        for ref in section.figures:
            if ref.figure_id in self.figures_index:
                result.append((self.figures_index[ref.figure_id], ref.focus))
        return result

    def to_dict(self) -> Dict[str, Any]:
        return {
            "output_type": self.output_type,
            "sections": [s.to_dict() for s in self.sections],
            "metadata": self.metadata,
        }


@dataclass
class GeneratedImage:
    """A single generated image from the image generation backend."""
    section_id: str
    image_data: bytes
    mime_type: str
