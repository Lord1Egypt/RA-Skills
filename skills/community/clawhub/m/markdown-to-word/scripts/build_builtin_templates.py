#!/usr/bin/env python3
from __future__ import annotations

import shutil
import subprocess
import tempfile
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "assets" / "templates"

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
A_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"

ET.register_namespace("w", W_NS)
ET.register_namespace("a", A_NS)


def w(tag: str) -> str:
    return f"{{{W_NS}}}{tag}"


def a(tag: str) -> str:
    return f"{{{A_NS}}}{tag}"


THEMES = {
    "modern-blue": {
        "accent1": "1D5B8F",
        "accent2": "5DA9E9",
        "hyperlink": "1D4ED8",
        "major_latin": "Aptos Display",
        "minor_latin": "Aptos",
        "major_hans": "PingFang SC",
        "minor_hans": "PingFang SC",
        "body_size": 22,
        "body_after": 160,
        "title_size": 58,
        "title_color": "17324D",
        "title_align": "center",
        "heading1_size": 34,
        "heading2_size": 28,
        "heading3_size": 24,
        "heading_color": "1D5B8F",
        "code_font": "Menlo",
        "toc_color": "1D5B8F",
        "code_bg": "F4F8FC",
        "code_border": "C9DAEA",
        "code_text": "17324D",
        "code_keyword": "1D4ED8",
        "code_string": "047857",
        "code_key": "7C3AED",
        "code_number": "B45309",
        "code_comment": "64748B",
        "code_operator": "0F766E",
    },
    "executive-serif": {
        "accent1": "274C77",
        "accent2": "6096BA",
        "hyperlink": "274C77",
        "major_latin": "Baskerville",
        "minor_latin": "Georgia",
        "major_hans": "Songti SC",
        "minor_hans": "PingFang SC",
        "body_size": 23,
        "body_after": 170,
        "title_size": 60,
        "title_color": "1B263B",
        "title_align": "left",
        "heading1_size": 32,
        "heading2_size": 27,
        "heading3_size": 24,
        "heading_color": "274C77",
        "code_font": "Menlo",
        "toc_color": "274C77",
        "code_bg": "F7F4F1",
        "code_border": "D9CDC0",
        "code_text": "3B322C",
        "code_keyword": "274C77",
        "code_string": "0F766E",
        "code_key": "7C2D12",
        "code_number": "9A3412",
        "code_comment": "78716C",
        "code_operator": "57534E",
    },
    "warm-notebook": {
        "accent1": "9A3412",
        "accent2": "D97706",
        "hyperlink": "B45309",
        "major_latin": "Avenir Next",
        "minor_latin": "Avenir Next",
        "major_hans": "PingFang SC",
        "minor_hans": "PingFang SC",
        "body_size": 22,
        "body_after": 180,
        "title_size": 56,
        "title_color": "7C2D12",
        "title_align": "left",
        "heading1_size": 34,
        "heading2_size": 28,
        "heading3_size": 24,
        "heading_color": "9A3412",
        "code_font": "Menlo",
        "toc_color": "9A3412",
        "code_bg": "FFF6ED",
        "code_border": "F3D2B3",
        "code_text": "7C2D12",
        "code_keyword": "C2410C",
        "code_string": "15803D",
        "code_key": "9A3412",
        "code_number": "B45309",
        "code_comment": "78716C",
        "code_operator": "9A3412",
    },
    "minimal-gray": {
        "accent1": "374151",
        "accent2": "6B7280",
        "hyperlink": "4B5563",
        "major_latin": "Helvetica Neue",
        "minor_latin": "Helvetica Neue",
        "major_hans": "PingFang SC",
        "minor_hans": "PingFang SC",
        "body_size": 21,
        "body_after": 140,
        "title_size": 54,
        "title_color": "111827",
        "title_align": "left",
        "heading1_size": 32,
        "heading2_size": 26,
        "heading3_size": 23,
        "heading_color": "374151",
        "code_font": "Menlo",
        "toc_color": "374151",
        "code_bg": "F5F6F7",
        "code_border": "D1D5DB",
        "code_text": "1F2937",
        "code_keyword": "374151",
        "code_string": "047857",
        "code_key": "4B5563",
        "code_number": "B45309",
        "code_comment": "6B7280",
        "code_operator": "4B5563",
    },
}

CODE_TOKEN_COLORS = {
    "KeywordTok": "code_keyword",
    "DataTypeTok": "code_key",
    "DecValTok": "code_number",
    "BaseNTok": "code_number",
    "FloatTok": "code_number",
    "ConstantTok": "code_number",
    "CharTok": "code_string",
    "SpecialCharTok": "code_operator",
    "StringTok": "code_string",
    "VerbatimStringTok": "code_string",
    "SpecialStringTok": "code_string",
    "ImportTok": "code_text",
    "CommentTok": "code_comment",
    "DocumentationTok": "code_comment",
    "AnnotationTok": "code_comment",
    "CommentVarTok": "code_comment",
    "OtherTok": "code_operator",
    "FunctionTok": "code_operator",
    "VariableTok": "code_text",
    "ControlFlowTok": "code_keyword",
    "OperatorTok": "code_operator",
    "BuiltInTok": "code_text",
    "ExtensionTok": "code_text",
    "PreprocessorTok": "code_comment",
    "AttributeTok": "code_key",
    "RegionMarkerTok": "code_text",
    "InformationTok": "code_comment",
    "WarningTok": "code_comment",
    "AlertTok": "code_keyword",
    "ErrorTok": "code_keyword",
    "NormalTok": "code_text",
}

CODE_TOKEN_BOLD = {
    "KeywordTok",
    "ControlFlowTok",
    "FunctionTok",
    "AttributeTok",
    "DataTypeTok",
}

CODE_TOKEN_ITALIC = {
    "CommentTok",
    "DocumentationTok",
    "AnnotationTok",
    "CommentVarTok",
    "PreprocessorTok",
}


def ensure_pandoc() -> str:
    pandoc = shutil.which("pandoc")
    if not pandoc:
        raise SystemExit("pandoc is required but was not found on PATH.")
    return pandoc


def update_theme(theme_xml: bytes, cfg: dict[str, object]) -> bytes:
    root = ET.fromstring(theme_xml)
    color_map = {
        "accent1": cfg["accent1"],
        "accent2": cfg["accent2"],
        "hlink": cfg["hyperlink"],
    }
    for name, value in color_map.items():
        node = root.find(f".//{a(name)}/{a('srgbClr')}")
        if node is not None:
            node.set("val", str(value))

    for section, latin_font, hans_font in [
        ("majorFont", cfg["major_latin"], cfg["major_hans"]),
        ("minorFont", cfg["minor_latin"], cfg["minor_hans"]),
    ]:
        section_node = root.find(f".//{a(section)}")
        if section_node is None:
            continue
        latin = section_node.find(a("latin"))
        if latin is not None:
            latin.set("typeface", str(latin_font))
        east_asia = section_node.find(a("ea"))
        if east_asia is not None:
            east_asia.set("typeface", str(hans_font))
        for font in section_node.findall(a("font")):
            if font.get("script") == "Hans":
                font.set("typeface", str(hans_font))
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def ensure_child(parent: ET.Element, tag: str) -> ET.Element:
    node = parent.find(tag)
    if node is None:
        node = ET.SubElement(parent, tag)
    return node


def style_by_id(root: ET.Element, style_id: str) -> ET.Element | None:
    for style in root.findall(w("style")):
        if style.get(w("styleId")) == style_id:
            return style
    return None


def set_font_on_rpr(rpr: ET.Element, *, ascii_font: str | None = None, east_asia_font: str | None = None) -> None:
    fonts = ensure_child(rpr, w("rFonts"))
    if ascii_font:
        fonts.set(w("ascii"), ascii_font)
        fonts.set(w("hAnsi"), ascii_font)
    if east_asia_font:
        fonts.set(w("eastAsia"), east_asia_font)


def set_size_on_rpr(rpr: ET.Element, value: int) -> None:
    sz = ensure_child(rpr, w("sz"))
    sz.set(w("val"), str(value))
    sz_cs = ensure_child(rpr, w("szCs"))
    sz_cs.set(w("val"), str(value))


def set_color_on_rpr(rpr: ET.Element, value: str) -> None:
    color = ensure_child(rpr, w("color"))
    color.attrib.clear()
    color.set(w("val"), value)


def set_spacing_on_ppr(ppr: ET.Element, *, before: int | None = None, after: int | None = None) -> None:
    spacing = ensure_child(ppr, w("spacing"))
    if before is not None:
        spacing.set(w("before"), str(before))
    if after is not None:
        spacing.set(w("after"), str(after))


def set_line_spacing_on_ppr(ppr: ET.Element, line: int, rule: str = "auto") -> None:
    spacing = ensure_child(ppr, w("spacing"))
    spacing.set(w("line"), str(line))
    spacing.set(w("lineRule"), rule)


def set_shading(target: ET.Element, fill: str) -> None:
    shd = ensure_child(target, w("shd"))
    shd.set(w("val"), "clear")
    shd.set(w("fill"), fill)


def set_indentation(ppr: ET.Element, *, left: int | None = None, right: int | None = None) -> None:
    ind = ensure_child(ppr, w("ind"))
    if left is not None:
        ind.set(w("left"), str(left))
    if right is not None:
        ind.set(w("right"), str(right))


def set_borders(ppr: ET.Element, color: str, size: int = 8, space: int = 4) -> None:
    p_bdr = ensure_child(ppr, w("pBdr"))
    for edge in ("top", "left", "bottom", "right"):
        border = ensure_child(p_bdr, w(edge))
        border.set(w("val"), "single")
        border.set(w("sz"), str(size))
        border.set(w("space"), str(space))
        border.set(w("color"), color)


def append_style(root: ET.Element, style_type: str, style_id: str, name: str) -> ET.Element:
    style = ET.SubElement(root, w("style"))
    style.set(w("type"), style_type)
    style.set(w("customStyle"), "1")
    style.set(w("styleId"), style_id)
    name_node = ET.SubElement(style, w("name"))
    name_node.set(w("val"), name)
    return style


def upsert_code_styles(root: ET.Element, cfg: dict[str, object]) -> None:
    source_code = style_by_id(root, "SourceCode")
    if source_code is None:
        source_code = append_style(root, "paragraph", "SourceCode", "Source Code")
        based_on = ET.SubElement(source_code, w("basedOn"))
        based_on.set(w("val"), "Normal")
        link = ET.SubElement(source_code, w("link"))
        link.set(w("val"), "VerbatimChar")
    ppr = ensure_child(source_code, w("pPr"))
    set_spacing_on_ppr(ppr, before=120, after=120)
    set_line_spacing_on_ppr(ppr, 240)
    set_indentation(ppr, left=240, right=120)
    set_shading(ppr, str(cfg["code_bg"]))
    set_borders(ppr, str(cfg["code_border"]))

    verbatim = style_by_id(root, "VerbatimChar")
    if verbatim is None:
        verbatim = append_style(root, "character", "VerbatimChar", "Verbatim Char")
        based_on = ET.SubElement(verbatim, w("basedOn"))
        based_on.set(w("val"), "BodyTextChar")
    rpr = ensure_child(verbatim, w("rPr"))
    set_font_on_rpr(
        rpr,
        ascii_font=str(cfg["code_font"]),
        east_asia_font=str(cfg["minor_hans"]),
    )
    set_size_on_rpr(rpr, max(18, int(cfg["body_size"]) - 2))
    set_color_on_rpr(rpr, str(cfg["code_text"]))

    for token_style_id, color_key in CODE_TOKEN_COLORS.items():
        token_style = style_by_id(root, token_style_id)
        if token_style is None:
            token_style = append_style(root, "character", token_style_id, token_style_id)
            based_on = ET.SubElement(token_style, w("basedOn"))
            based_on.set(w("val"), "VerbatimChar")
        token_rpr = ensure_child(token_style, w("rPr"))
        set_color_on_rpr(token_rpr, str(cfg[color_key]))
        if token_style_id in CODE_TOKEN_BOLD:
            ensure_child(token_rpr, w("b"))
        if token_style_id in CODE_TOKEN_ITALIC:
            ensure_child(token_rpr, w("i"))


def update_styles(styles_xml: bytes, cfg: dict[str, object]) -> bytes:
    root = ET.fromstring(styles_xml)

    doc_defaults = root.find(w("docDefaults"))
    if doc_defaults is not None:
        rpr_default = doc_defaults.find(f"{w('rPrDefault')}/{w('rPr')}")
        if rpr_default is not None:
            set_font_on_rpr(
                rpr_default,
                ascii_font=str(cfg["minor_latin"]),
                east_asia_font=str(cfg["minor_hans"]),
            )
            set_size_on_rpr(rpr_default, int(cfg["body_size"]))
        ppr_default = doc_defaults.find(f"{w('pPrDefault')}/{w('pPr')}")
        if ppr_default is not None:
            set_spacing_on_ppr(ppr_default, after=int(cfg["body_after"]))

    body = style_by_id(root, "BodyText")
    if body is not None:
        ppr = ensure_child(body, w("pPr"))
        set_spacing_on_ppr(ppr, before=80, after=int(cfg["body_after"]))

    title = style_by_id(root, "Title")
    if title is not None:
        ppr = ensure_child(title, w("pPr"))
        align = ensure_child(ppr, w("jc"))
        align.set(w("val"), str(cfg["title_align"]))
        set_spacing_on_ppr(ppr, after=120)
        rpr = ensure_child(title, w("rPr"))
        set_color_on_rpr(rpr, str(cfg["title_color"]))
        set_size_on_rpr(rpr, int(cfg["title_size"]))

    subtitle = style_by_id(root, "Subtitle")
    if subtitle is not None:
        rpr = ensure_child(subtitle, w("rPr"))
        set_color_on_rpr(rpr, str(cfg["accent2"]))

    for style_id, size in [
        ("Heading1", int(cfg["heading1_size"])),
        ("Heading2", int(cfg["heading2_size"])),
        ("Heading3", int(cfg["heading3_size"])),
        ("Heading4", int(cfg["heading3_size"])),
    ]:
        style = style_by_id(root, style_id)
        if style is None:
            continue
        rpr = ensure_child(style, w("rPr"))
        set_color_on_rpr(rpr, str(cfg["heading_color"]))
        if style_id != "Heading4":
            set_size_on_rpr(rpr, size)

    verbatim = style_by_id(root, "VerbatimChar")
    if verbatim is not None:
        rpr = ensure_child(verbatim, w("rPr"))
        set_font_on_rpr(rpr, ascii_font=str(cfg["code_font"]), east_asia_font=str(cfg["minor_hans"]))
        set_size_on_rpr(rpr, max(18, int(cfg["body_size"]) - 2))
        set_color_on_rpr(rpr, str(cfg["code_text"]))

    hyperlink = style_by_id(root, "Hyperlink")
    if hyperlink is not None:
        rpr = ensure_child(hyperlink, w("rPr"))
        set_color_on_rpr(rpr, str(cfg["hyperlink"]))

    toc = style_by_id(root, "TOCHeading")
    if toc is not None:
        rpr = ensure_child(toc, w("rPr"))
        set_color_on_rpr(rpr, str(cfg["toc_color"]))

    upsert_code_styles(root, cfg)

    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def build_default_reference(pandoc: str, destination: Path) -> None:
    reference_bytes = subprocess.check_output(
        [pandoc, "--print-default-data-file", "reference.docx"]
    )
    destination.write_bytes(reference_bytes)


def write_theme(base_docx: Path, target_docx: Path, cfg: dict[str, object]) -> None:
    with tempfile.TemporaryDirectory(prefix="markdown-to-word-") as tmpdir:
        tmpdir_path = Path(tmpdir)
        unpack_dir = tmpdir_path / "unpacked"
        unpack_dir.mkdir()
        with zipfile.ZipFile(base_docx) as src_zip:
            src_zip.extractall(unpack_dir)

        theme_path = unpack_dir / "word" / "theme" / "theme1.xml"
        styles_path = unpack_dir / "word" / "styles.xml"
        theme_path.write_bytes(update_theme(theme_path.read_bytes(), cfg))
        styles_path.write_bytes(update_styles(styles_path.read_bytes(), cfg))

        with zipfile.ZipFile(target_docx, "w", compression=zipfile.ZIP_DEFLATED) as out_zip:
            for path in sorted(unpack_dir.rglob("*")):
                if path.is_file():
                    out_zip.write(path, path.relative_to(unpack_dir).as_posix())


def main() -> int:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    pandoc = ensure_pandoc()
    with tempfile.TemporaryDirectory(prefix="markdown-to-word-reference-") as tmpdir:
        base_docx = Path(tmpdir) / "reference.docx"
        build_default_reference(pandoc, base_docx)
        for name, cfg in THEMES.items():
            write_theme(base_docx, OUTPUT_DIR / f"{name}.docx", cfg)
            print(f"built {OUTPUT_DIR / f'{name}.docx'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
