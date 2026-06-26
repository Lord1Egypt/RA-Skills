"""Style preset: Meeting Minutes (会议纪要)"""

from docx.shared import Pt, RGBColor
from docx.oxml.ns import qn

from kai_docx_generator.styles.standard import _configure_paragraph_style


MEETING_CONFIG = {
    "Normal": {
        "font": "Microsoft YaHei",
        "eastAsia": "Microsoft YaHei",
        "size": Pt(12),
        "color": "333333",
        "bold": False,
        "italic": False,
        "space_after": Pt(4),
        "line_spacing": 1.5,
    },
    "Heading 1": {
        "font": "Microsoft YaHei",
        "eastAsia": "Microsoft YaHei",
        "size": Pt(16),
        "color": "1A1A2E",
        "bold": True,
        "space_before": Pt(12),
        "space_after": Pt(8),
        "outline_level": 0,
    },
    "Heading 2": {
        "font": "Microsoft YaHei",
        "eastAsia": "Microsoft YaHei",
        "size": Pt(14),
        "color": "2563EB",
        "bold": True,
        "space_before": Pt(10),
        "space_after": Pt(4),
        "outline_level": 1,
    },
    "Heading 3": {
        "font": "Microsoft YaHei",
        "eastAsia": "Microsoft YaHei",
        "size": Pt(12),
        "color": "333333",
        "bold": True,
        "space_before": Pt(6),
        "space_after": Pt(3),
        "outline_level": 2,
    },
}


def apply_meeting_style(document, style_config: dict | None = None):
    """
    在 Document 上应用 Meeting Minutes (会议纪要) Style 预设。
    """
    if style_config:
        config = {**MEETING_CONFIG, **style_config}
        for key in config:
            if key in MEETING_CONFIG and key in style_config:
                config[key] = {**MEETING_CONFIG[key], **style_config[key]}
    else:
        config = MEETING_CONFIG
    _apply_style(document, config)


def _apply_style(document, config: dict):
    """Apply config to document styles"""
    for style_name in ("Normal", "Heading 1", "Heading 2", "Heading 3"):
        if style_name in config:
            style = document.styles[style_name]
            _configure_paragraph_style(style, config[style_name])
