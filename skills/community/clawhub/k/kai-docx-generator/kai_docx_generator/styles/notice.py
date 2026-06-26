"""Style preset: Notice (通知)"""

from docx.shared import Pt, RGBColor
from docx.oxml.ns import qn

from kai_docx_generator.styles.standard import _configure_paragraph_style


NOTICE_CONFIG = {
    "Normal": {
        "font": "FangSong",
        "eastAsia": "FangSong",
        "size": Pt(16),
        "color": "333333",
        "bold": False,
        "italic": False,
        "space_after": Pt(0),
        "line_spacing": Pt(28),
    },
    "Heading 1": {
        "font": "SimHei",
        "eastAsia": "SimHei",
        "size": Pt(22),
        "color": "333333",
        "bold": True,
        "space_before": Pt(12),
        "space_after": Pt(6),
        "outline_level": 0,
    },
    "Heading 2": {
        "font": "KaiTi",
        "eastAsia": "KaiTi",
        "size": Pt(16),
        "color": "333333",
        "bold": True,
        "space_before": Pt(10),
        "space_after": Pt(4),
        "outline_level": 1,
    },
    "Heading 3": {
        "font": "FangSong",
        "eastAsia": "FangSong",
        "size": Pt(16),
        "color": "333333",
        "bold": True,
        "space_before": Pt(6),
        "space_after": Pt(3),
        "outline_level": 2,
    },
}


def apply_notice_style(document, style_config: dict | None = None):
    """
    在 Document 上应用 Notice (通知) Style 预设。
    """
    if style_config:
        config = {**NOTICE_CONFIG, **style_config}
        for key in config:
            if key in NOTICE_CONFIG and key in style_config:
                config[key] = {**NOTICE_CONFIG[key], **style_config[key]}
    else:
        config = NOTICE_CONFIG
    _apply_style(document, config)


def _apply_style(document, config: dict):
    """Apply config to document styles"""
    for style_name in ("Normal", "Heading 1", "Heading 2", "Heading 3"):
        if style_name in config:
            style = document.styles[style_name]
            _configure_paragraph_style(style, config[style_name])
