"""标准 Style 预设"""

from docx.shared import Pt, RGBColor
from docx.oxml.ns import qn


def apply_standard_style(document, style_config: dict | None = None):
    """
    在 Document 上应用标准 Style 预设。

    Args:
        document: python-docx Document 对象
        style_config: 可选的自定义配置字典，会与默认配置合并（浅合并）
    """
    if style_config:
        config = {**STANDARD_CONFIG, **style_config}
        for key in config:
            if key in STANDARD_CONFIG and key in style_config:
                config[key] = {**STANDARD_CONFIG[key], **style_config[key]}
    else:
        config = STANDARD_CONFIG
    _apply_style(document, config)


STANDARD_CONFIG = {
    "Normal": {
        "font": "Microsoft YaHei",
        "eastAsia": "Microsoft YaHei",
        "size": Pt(11),
        "color": None,
        "bold": False,
        "italic": False,
        "space_after": Pt(6),
        "line_spacing": 1.5,
    },
    "Heading 1": {
        "font": "Microsoft YaHei",
        "eastAsia": "Microsoft YaHei",
        "size": Pt(16),
        "color": "1A1A2E",
        "bold": True,
        "space_before": Pt(18),
        "space_after": Pt(10),
        "outline_level": 0,
    },
    "Heading 2": {
        "font": "Microsoft YaHei",
        "eastAsia": "Microsoft YaHei",
        "size": Pt(14),
        "color": "2563EB",
        "bold": True,
        "space_before": Pt(12),
        "space_after": Pt(6),
        "outline_level": 1,
    },
    "Heading 3": {
        "font": "Microsoft YaHei",
        "eastAsia": "Microsoft YaHei",
        "size": Pt(12),
        "color": "333333",
        "bold": True,
        "space_before": Pt(10),
        "space_after": Pt(4),
        "outline_level": 2,
    },
}


def _apply_style(document, config: dict):
    """应用配置到 Document 的样式"""
    # Normal 样式
    if "Normal" in config:
        normal = document.styles["Normal"]
        _configure_paragraph_style(normal, config["Normal"])

    # Heading 样式
    for style_name in ("Heading 1", "Heading 2", "Heading 3"):
        if style_name in config:
            style = document.styles[style_name]
            _configure_paragraph_style(style, config[style_name])


def _configure_paragraph_style(style, cfg: dict):
    """配置段落样式"""
    font = style.font
    font.name = cfg["font"]

    if cfg.get("size"):
        font.size = cfg["size"]
    if cfg.get("color"):
        font.color.rgb = RGBColor.from_string(cfg["color"])
    if cfg.get("bold") is not None:
        font.bold = cfg["bold"]
    if cfg.get("italic") is not None:
        font.italic = cfg["italic"]

    # 东亚字体设置
    rPr = style.element.get_or_add_rPr()
    rFonts = rPr.get_or_add_rFonts()
    rFonts.set(qn("w:eastAsia"), cfg["eastAsia"])

    # 段落格式
    pf = style.paragraph_format
    if cfg.get("space_before"):
        pf.space_before = cfg["space_before"]
    if cfg.get("space_after"):
        pf.space_after = cfg["space_after"]
    if cfg.get("line_spacing"):
        pf.line_spacing = cfg["line_spacing"]
    if cfg.get("outline_level") is not None:
        pf.outline_level = cfg["outline_level"]


def set_run_cjk_font(run, font_name: str = "Microsoft YaHei"):
    """在单个 run 上设置 CJK 字体"""
    run.font.name = font_name
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.get_or_add_rFonts()
    rFonts.set(qn("w:eastAsia"), font_name)
