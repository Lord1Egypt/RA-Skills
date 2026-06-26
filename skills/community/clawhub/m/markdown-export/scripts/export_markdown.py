#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DOCX_TEMPLATE_DIR = ROOT / "assets" / "docx" / "templates"
HTML_TEMPLATE_DIR = ROOT / "assets" / "html" / "templates"
HTML_STYLE_DIR = ROOT / "assets" / "html" / "styles"
W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"

ET.register_namespace("w", W_NS)

DOCX_TEMPLATES = {
    "modern-blue": {
        "file": DOCX_TEMPLATE_DIR / "modern-blue.docx",
        "description": "Clean report style with strong blue headings.",
    },
    "executive-serif": {
        "file": DOCX_TEMPLATE_DIR / "executive-serif.docx",
        "description": "Formal memo style with serif typography.",
    },
    "warm-notebook": {
        "file": DOCX_TEMPLATE_DIR / "warm-notebook.docx",
        "description": "Warm editorial style with softer accent colors.",
    },
    "minimal-gray": {
        "file": DOCX_TEMPLATE_DIR / "minimal-gray.docx",
        "description": "Low-contrast documentation style.",
    },
}

DOCX_CODE_THEMES = {
    "modern-blue": {
        "code_font": "Menlo",
        "minor_hans": "PingFang SC",
        "body_size": 22,
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
        "code_font": "Menlo",
        "minor_hans": "PingFang SC",
        "body_size": 23,
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
        "code_font": "Menlo",
        "minor_hans": "PingFang SC",
        "body_size": 22,
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
        "code_font": "Menlo",
        "minor_hans": "PingFang SC",
        "body_size": 21,
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
    "neutral": {
        "code_font": "Menlo",
        "minor_hans": "PingFang SC",
        "body_size": 22,
        "code_bg": "F6F8FA",
        "code_border": "D0D7DE",
        "code_text": "24292F",
        "code_keyword": "0550AE",
        "code_string": "0A7F42",
        "code_key": "8250DF",
        "code_number": "9A6700",
        "code_comment": "6E7781",
        "code_operator": "0A3069",
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

CODE_TOKEN_BOLD = {"KeywordTok", "ControlFlowTok", "FunctionTok", "AttributeTok", "DataTypeTok"}
CODE_TOKEN_ITALIC = {"CommentTok", "DocumentationTok", "AnnotationTok", "CommentVarTok", "PreprocessorTok"}

HTML_TEMPLATES = {
    "docs-slate": {
        "template": HTML_TEMPLATE_DIR / "docs-slate.html",
        "css": [HTML_STYLE_DIR / "docs-slate.css"],
        "description": "Technical documentation layout with clean spacing and slate tones.",
    },
    "magazine-amber": {
        "template": HTML_TEMPLATE_DIR / "magazine-amber.html",
        "css": [HTML_STYLE_DIR / "magazine-amber.css"],
        "description": "Editorial layout with warm highlights and magazine rhythm.",
    },
    "product-midnight": {
        "template": HTML_TEMPLATE_DIR / "product-midnight.html",
        "css": [HTML_STYLE_DIR / "product-midnight.css"],
        "description": "Dark narrative layout for launch notes and product storytelling.",
    },
    "serif-paper": {
        "template": HTML_TEMPLATE_DIR / "serif-paper.html",
        "css": [HTML_STYLE_DIR / "serif-paper.css"],
        "description": "Print-inspired article page with serif typography.",
    },
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Export Markdown files or Markdown strings into DOCX or HTML."
    )
    parser.add_argument("--format", choices=["docx", "html"], help="Target output format.")
    parser.add_argument("--input-file", type=Path, help="Absolute or relative path to a Markdown file.")
    parser.add_argument("--markdown", help="Raw Markdown string to convert.")
    parser.add_argument("--output", type=Path, help="Output path. Defaults from --input-file when possible.")
    parser.add_argument(
        "--template",
        type=Path,
        help="Custom template. DOCX expects reference.docx, HTML expects a Pandoc HTML template.",
    )
    parser.add_argument("--builtin-template", help="Built-in template name for the selected --format.")
    parser.add_argument(
        "--css",
        action="append",
        type=Path,
        default=[],
        help="Additional CSS file for HTML output. May be passed more than once.",
    )
    parser.add_argument("--metadata-file", type=Path, help="Pandoc metadata file, usually YAML.")
    parser.add_argument("--resource-path", help="Extra pandoc resource path for linked assets.")
    parser.add_argument("--title")
    parser.add_argument("--author")
    parser.add_argument("--date")
    parser.add_argument("--toc", action="store_true", help="Insert a table of contents.")
    parser.add_argument("--number-sections", action="store_true", help="Number document headings.")
    parser.add_argument(
        "--no-body-background",
        action="store_true",
        help="Remove the background, border, and shadow behind the rendered HTML article body.",
    )
    parser.add_argument(
        "--embed-assets",
        action="store_true",
        help="Embed CSS, images, and other resources into HTML when possible.",
    )
    parser.add_argument(
        "--self-contained",
        action="store_true",
        help="Compatibility alias for --embed-assets.",
    )
    parser.add_argument(
        "--highlight-style",
        default="tango",
        help="Pandoc syntax highlighting style. Default: tango.",
    )
    parser.add_argument("--list-templates", action="store_true", help="Print built-in templates and exit.")
    parser.add_argument("--print-command", action="store_true", help="Print the pandoc command before running.")
    return parser


def ensure_pandoc() -> str:
    pandoc = shutil.which("pandoc")
    if not pandoc:
        raise SystemExit("pandoc is required but was not found on PATH.")
    return pandoc


def w(tag: str) -> str:
    return f"{{{W_NS}}}{tag}"


def style_by_id(root: ET.Element, style_id: str) -> ET.Element | None:
    for style in root.findall(w("style")):
        if style.get(w("styleId")) == style_id or style.get("styleId") == style_id:
            return style
    return None


def ensure_child(parent: ET.Element, tag: str) -> ET.Element:
    node = parent.find(tag)
    if node is None:
        node = ET.SubElement(parent, tag)
    return node


def append_style(root: ET.Element, style_type: str, style_id: str, name: str) -> ET.Element:
    style = ET.SubElement(root, w("style"))
    style.set(w("type"), style_type)
    style.set(w("customStyle"), "1")
    style.set(w("styleId"), style_id)
    name_node = ET.SubElement(style, w("name"))
    name_node.set(w("val"), name)
    return style


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


def set_spacing_on_ppr(ppr: ET.Element, *, before: int, after: int, line: int) -> None:
    spacing = ensure_child(ppr, w("spacing"))
    spacing.set(w("before"), str(before))
    spacing.set(w("after"), str(after))
    spacing.set(w("line"), str(line))
    spacing.set(w("lineRule"), "auto")


def set_indentation(ppr: ET.Element, *, left: int, right: int) -> None:
    ind = ensure_child(ppr, w("ind"))
    ind.set(w("left"), str(left))
    ind.set(w("right"), str(right))


def set_shading(target: ET.Element, fill: str) -> None:
    shd = ensure_child(target, w("shd"))
    shd.set(w("val"), "clear")
    shd.set(w("fill"), fill)


def set_borders(ppr: ET.Element, color: str, size: int = 8, space: int = 4) -> None:
    p_bdr = ensure_child(ppr, w("pBdr"))
    for edge in ("top", "left", "bottom", "right"):
        border = ensure_child(p_bdr, w(edge))
        border.set(w("val"), "single")
        border.set(w("sz"), str(size))
        border.set(w("space"), str(space))
        border.set(w("color"), color)


def update_docx_code_styles(styles_xml: bytes, cfg: dict[str, str | int]) -> bytes:
    root = ET.fromstring(styles_xml)

    source_code = style_by_id(root, "SourceCode")
    if source_code is None:
        source_code = append_style(root, "paragraph", "SourceCode", "Source Code")
        based_on = ET.SubElement(source_code, w("basedOn"))
        based_on.set(w("val"), "Normal")
        link = ET.SubElement(source_code, w("link"))
        link.set(w("val"), "VerbatimChar")
    ppr = ensure_child(source_code, w("pPr"))
    word_wrap = ppr.find(w("wordWrap"))
    if word_wrap is not None:
        ppr.remove(word_wrap)
    set_spacing_on_ppr(ppr, before=120, after=120, line=240)
    set_indentation(ppr, left=240, right=120)
    set_shading(ppr, str(cfg["code_bg"]))
    set_borders(ppr, str(cfg["code_border"]))

    verbatim = style_by_id(root, "VerbatimChar")
    if verbatim is None:
        verbatim = append_style(root, "character", "VerbatimChar", "Verbatim Char")
        based_on = ET.SubElement(verbatim, w("basedOn"))
        based_on.set(w("val"), "BodyTextChar")
    verbatim_rpr = ensure_child(verbatim, w("rPr"))
    set_font_on_rpr(
        verbatim_rpr,
        ascii_font=str(cfg["code_font"]),
        east_asia_font=str(cfg["minor_hans"]),
    )
    set_size_on_rpr(verbatim_rpr, max(18, int(cfg["body_size"]) - 2))
    set_color_on_rpr(verbatim_rpr, str(cfg["code_text"]))

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

    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def patch_docx_output_styles(docx_path: Path, builtin_template: str | None) -> None:
    cfg = DOCX_CODE_THEMES.get(builtin_template or "", DOCX_CODE_THEMES["neutral"])
    with tempfile.TemporaryDirectory(prefix="markdown-export-docx-") as tmpdir:
        tmpdir_path = Path(tmpdir)
        unpack_dir = tmpdir_path / "docx"
        unpack_dir.mkdir()
        with zipfile.ZipFile(docx_path) as src_zip:
            src_zip.extractall(unpack_dir)

        styles_path = unpack_dir / "word" / "styles.xml"
        styles_path.write_bytes(update_docx_code_styles(styles_path.read_bytes(), cfg))

        rewritten = tmpdir_path / "rewritten.docx"
        with zipfile.ZipFile(rewritten, "w", compression=zipfile.ZIP_DEFLATED) as out_zip:
            for path in sorted(unpack_dir.rglob("*")):
                if path.is_file():
                    out_zip.write(path, path.relative_to(unpack_dir).as_posix())
        shutil.move(str(rewritten), str(docx_path))


def list_templates(output_format: str | None) -> None:
    payload: dict[str, object] = {}
    if output_format in (None, "docx"):
        payload["docx"] = [
            {
                "name": name,
                "path": str(config["file"]),
                "description": config["description"],
                "exists": config["file"].exists(),
            }
            for name, config in DOCX_TEMPLATES.items()
        ]
    if output_format in (None, "html"):
        payload["html"] = [
            {
                "name": name,
                "template": str(config["template"]),
                "css": [str(path) for path in config["css"]],
                "description": config["description"],
                "exists": config["template"].exists() and all(path.exists() for path in config["css"]),
            }
            for name, config in HTML_TEMPLATES.items()
        ]
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def validate_args(args: argparse.Namespace) -> None:
    if args.list_templates and not args.format:
        return
    if not args.format:
        raise SystemExit("--format is required unless you only use --list-templates.")
    if args.list_templates:
        return
    if bool(args.input_file) == bool(args.markdown):
        raise SystemExit("Provide exactly one of --input-file or --markdown.")
    if args.input_file and not args.input_file.exists():
        raise SystemExit(f"Input Markdown file not found: {args.input_file}")
    if args.template and not args.template.exists():
        raise SystemExit(f"Template file not found: {args.template}")
    if args.metadata_file and not args.metadata_file.exists():
        raise SystemExit(f"Metadata file not found: {args.metadata_file}")
    for css_path in args.css:
        if not css_path.exists():
            raise SystemExit(f"CSS file not found: {css_path}")
    if args.format == "docx" and args.css:
        raise SystemExit("--css is only valid with --format html.")


def resolve_output(args: argparse.Namespace) -> Path:
    if args.output:
        return args.output.expanduser().resolve()
    if args.input_file:
        suffix = ".docx" if args.format == "docx" else ".html"
        return args.input_file.expanduser().resolve().with_suffix(suffix)
    raise SystemExit("--output is required when using --markdown.")


def resolve_docx_template(args: argparse.Namespace) -> Path:
    if args.template:
        return args.template.expanduser().resolve()
    name = args.builtin_template or "modern-blue"
    if name not in DOCX_TEMPLATES:
        valid = ", ".join(sorted(DOCX_TEMPLATES))
        raise SystemExit(f"Unknown DOCX built-in template '{name}'. Valid values: {valid}")
    path = DOCX_TEMPLATES[name]["file"]
    if not path.exists():
        raise SystemExit(f"Built-in DOCX template is missing: {path}")
    return path


def resolve_html_template(args: argparse.Namespace) -> tuple[Path, list[Path], str | None]:
    if args.template:
        return args.template.expanduser().resolve(), [path.expanduser().resolve() for path in args.css], None
    name = args.builtin_template or "docs-slate"
    if name not in HTML_TEMPLATES:
        valid = ", ".join(sorted(HTML_TEMPLATES))
        raise SystemExit(f"Unknown HTML built-in template '{name}'. Valid values: {valid}")
    config = HTML_TEMPLATES[name]
    template_path = config["template"]
    if not template_path.exists():
        raise SystemExit(f"Built-in HTML template is missing: {template_path}")
    css_paths = [path.resolve() for path in config["css"]] + [path.expanduser().resolve() for path in args.css]
    return template_path, css_paths, name


def base_resource_path(args: argparse.Namespace) -> str | None:
    if args.resource_path:
        return args.resource_path
    if args.input_file:
        return str(args.input_file.expanduser().resolve().parent)
    return None


def pandoc_markdown_input() -> str:
    return (
        "markdown+yaml_metadata_block+emoji+footnotes+pipe_tables+grid_tables+task_lists+"
        "fenced_divs+fenced_code_attributes+raw_attribute+tex_math_dollars"
    )


def build_docx_command(
    pandoc: str,
    source_path: Path,
    output_path: Path,
    template_path: Path,
    args: argparse.Namespace,
) -> list[str]:
    command = [
        pandoc,
        str(source_path),
        "--from",
        pandoc_markdown_input(),
        "--to",
        "docx",
        "--standalone",
        "--reference-doc",
        str(template_path),
        "--syntax-highlighting",
        args.highlight_style,
        "--output",
        str(output_path),
    ]
    extend_common_command(command, args)
    return command


def build_html_command(
    pandoc: str,
    source_path: Path,
    output_path: Path,
    template_path: Path,
    css_paths: list[Path],
    args: argparse.Namespace,
) -> list[str]:
    command = [
        pandoc,
        str(source_path),
        "--from",
        pandoc_markdown_input(),
        "--to",
        "html5",
        "--standalone",
        "--template",
        str(template_path),
        "--syntax-highlighting",
        args.highlight_style,
        "--output",
        str(output_path),
    ]
    extend_common_command(command, args)
    if args.embed_assets or args.self_contained:
        command.append("--embed-resources")
    for css_path in css_paths:
        command.extend(["--css", str(css_path)])
    return command


def extend_common_command(command: list[str], args: argparse.Namespace) -> None:
    if args.metadata_file:
        command.extend(["--metadata-file", str(args.metadata_file.expanduser().resolve())])
    if args.title:
        command.extend(["--metadata", f"title={args.title}"])
    if args.author:
        command.extend(["--metadata", f"author={args.author}"])
    if args.date:
        command.extend(["--metadata", f"date={args.date}"])
    if args.no_body_background:
        command.extend(["--metadata", "plain_content=true"])
    resource_path = base_resource_path(args)
    if resource_path:
        command.extend(["--resource-path", resource_path])
    if args.toc:
        command.append("--toc")
    if args.number_sections:
        command.append("--number-sections")


def prepare_source(args: argparse.Namespace) -> tuple[Path, tempfile.NamedTemporaryFile[str] | None]:
    if args.input_file:
        return args.input_file.expanduser().resolve(), None
    # 使用上下文管理器确保临时文件总是被清理
    temp_source = tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".md",
        prefix="markdown-export-",
        encoding="utf-8",
        delete=False,
    )
    with temp_source:
        temp_source.write(args.markdown)
        temp_source.flush()
    return Path(temp_source.name), temp_source


def run_conversion(args: argparse.Namespace) -> int:
    pandoc = ensure_pandoc()
    output_path = resolve_output(args)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    source_path, temp_source = prepare_source(args)
    try:
        if args.format == "docx":
            template_path = resolve_docx_template(args)
            command = build_docx_command(pandoc, source_path, output_path, template_path, args)
            css_paths: list[Path] = []
            builtin_name = None if args.template else (args.builtin_template or "modern-blue")
        else:
            template_path, css_paths, builtin_name = resolve_html_template(args)
            command = build_html_command(pandoc, source_path, output_path, template_path, css_paths, args)

        if args.print_command:
            print(" ".join(command), file=sys.stderr)
        completed = subprocess.run(command, check=False)
        if completed.returncode != 0:
            return completed.returncode
        if args.format == "docx":
            patch_docx_output_styles(output_path, builtin_name)

        print(
            json.dumps(
                {
                    "format": args.format,
                    "output": str(output_path),
                    "template": str(template_path),
                    "css": [str(path) for path in css_paths],
                    "builtin_template": builtin_name,
                    "source": str(source_path),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0
    finally:
        if temp_source is not None:
            try:
                Path(temp_source.name).unlink(missing_ok=True)
            except OSError:
                pass


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    validate_args(args)
    if args.list_templates:
        list_templates(args.format)
        return 0
    return run_conversion(args)


if __name__ == "__main__":
    raise SystemExit(main())
