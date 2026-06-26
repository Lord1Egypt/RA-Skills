from __future__ import annotations

import json
import tempfile
from pathlib import Path
from typing import Optional

import typer

from .core.agent import parse_agent_text
from .core.deps import check_bins
from .core.llm import LLMError, generate_plan
from .core.output import emit_result
from .core.usage import Usage, UsageMeter
from .tools.compress import compress_pdf
from .tools.compare import compare_pdfs
from .tools.crop import crop_pdf
from .tools.edit import add_image, add_text
from .tools.html_to_pdf import html_to_pdf
from .tools.images import images_to_pdf, pdf_to_jpg
from .tools.merge import merge_pdfs
from .tools.office import office_to_pdf
from .tools.ocr import ocr_pdf
from .tools.organize import extract_pages, insert_pdf, remove_pages, reorder_pages
from .tools.page_numbers import add_page_numbers
from .tools.pdf_to_docx import pdf_to_docx
from .tools.pdf_to_pptx import pdf_to_pptx
from .tools.pdf_to_xlsx import pdf_to_xlsx
from .tools.pdfa import pdf_to_pdfa
from .tools.repair import repair_pdf
from .tools.rotate import rotate_pdf
from .tools.scan import scan_to_pdf
from .tools.security import protect_pdf, unlock_pdf
from .tools.sign import sign_digital, sign_visible
from .tools.split import split_every, split_ranges
from .tools.translate import translate_pdf
from .tools.watermark import add_watermark
from .tools.redact import RedactionBox, redact_pdf

app = typer.Typer(add_completion=False, help="Self-hosted PDF CLI with agent-style commands")


TOOLS = [
    "merge",
    "split",
    "compress",
    "jpg_to_pdf",
    "word_to_pdf",
    "powerpoint_to_pdf",
    "excel_to_pdf",
    "html_to_pdf",
    "pdf_to_jpg",
    "pdf_to_word",
    "pdf_to_powerpoint",
    "pdf_to_excel",
    "pdf_to_pdfa",
    "remove_pages",
    "extract_pages",
    "organize",
    "scan_to_pdf",
    "repair",
    "ocr",
    "rotate",
    "add_page_numbers",
    "watermark",
    "crop",
    "edit",
    "unlock",
    "protect",
    "sign",
    "redact",
    "compare",
    "translate",
    "workflow",
]


def _append_usage(path: Optional[Path], payload: dict) -> None:
    if not path:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload))
        f.write("\n")


def _parse_passwords(spec: Optional[str]) -> dict[str, str] | None:
    if not spec:
        return None
    result: dict[str, str] = {}
    for part in spec.split(","):
        if "=" not in part:
            raise ValueError("--passwords expects file=pass pairs")
        name, pwd = part.split("=", 1)
        result[name.strip()] = pwd.strip()
    return result


def _normalize_passwords(value) -> dict[str, str] | None:
    if value is None:
        return None
    if isinstance(value, dict):
        return {str(k): str(v) for k, v in value.items()}
    if isinstance(value, str):
        return _parse_passwords(value)
    raise ValueError("passwords must be a dict or file=pass string")


def _sum_usage(usages: list[Usage]) -> Usage:
    if not usages:
        raise ValueError("No usage to sum")
    base = usages[0]
    total = Usage(
        tool="agent",
        started_at=base.started_at,
        ended_at=usages[-1].ended_at,
        duration_ms=sum(u.duration_ms for u in usages),
        cpu_ms=sum(u.cpu_ms for u in usages),
        bytes_in=sum(u.bytes_in for u in usages),
        bytes_out=sum(u.bytes_out for u in usages),
        pages_in=_sum_opt(u.pages_in for u in usages),
        pages_out=_sum_opt(u.pages_out for u in usages),
        inputs=base.inputs,
        outputs=usages[-1].outputs,
        success=all(u.success for u in usages),
        error=None,
    )
    return total


def _sum_opt(values):
    total = 0
    for v in values:
        if v is None:
            return None
        total += v
    return total


@app.command()
def doctor(json_output: bool = typer.Option(False, "--json", help="Emit JSON output")):
    bins = check_bins(
        [
            "gs",
            "qpdf",
            "pdftoppm",
            "soffice",
            "ocrmypdf",
            "wkhtmltopdf",
            "google-chrome",
            "chromium",
            "ollama",
        ]
    )
    if json_output:
        print(json.dumps({"binaries": bins}, indent=2))
        return

    print("Dependency check:")
    for name, ok in bins.items():
        print(f"- {name}: {'OK' if ok else 'missing'}")


@app.command()
def merge(
    inputs: list[Path] = typer.Argument(..., exists=True, readable=True, help="Input PDF files"),
    out: Path = typer.Option(..., "--out", help="Output PDF path"),
    password: Optional[str] = typer.Option(None, "--password", help="Password for encrypted PDFs"),
    passwords: Optional[str] = typer.Option(None, "--passwords", help="Per-file passwords: file=pass,file2=pass2"),
    json_output: bool = typer.Option(False, "--json", help="Emit JSON output"),
    usage_file: Optional[Path] = typer.Option(None, "--usage-file", help="Append JSON usage to file"),
):
    meter = UsageMeter("merge", inputs)
    try:
        pw_map = _parse_passwords(passwords)
        merge_pdfs(inputs, out, password=password, passwords=pw_map)
        usage = meter.finish([out], success=True)
    except Exception as exc:
        usage = meter.finish([out], success=False, error=str(exc))
        emit_result(tool="merge", outputs=[out], usage=usage, json_output=json_output)
        _append_usage(usage_file, usage.to_dict())
        raise typer.Exit(code=1)

    emit_result(tool="merge", outputs=[out], usage=usage, json_output=json_output)
    _append_usage(usage_file, usage.to_dict())


@app.command()
def split(
    input_pdf: Path = typer.Argument(..., exists=True, readable=True, help="Input PDF"),
    out_dir: Path = typer.Option(..., "--out-dir", help="Output directory"),
    every: Optional[int] = typer.Option(None, "--every", help="Split every N pages"),
    page_range: Optional[str] = typer.Option(None, "--range", help="Page ranges, e.g. 1-3,5,7-9"),
    json_output: bool = typer.Option(False, "--json", help="Emit JSON output"),
    usage_file: Optional[Path] = typer.Option(None, "--usage-file", help="Append JSON usage to file"),
):
    if (every is None and page_range is None) or (every is not None and page_range is not None):
        typer.echo("Provide exactly one of --every or --range", err=True)
        raise typer.Exit(code=2)

    meter = UsageMeter("split", [input_pdf])
    try:
        if every is not None:
            outputs = split_every(input_pdf, out_dir, every)
        else:
            outputs = split_ranges(input_pdf, out_dir, page_range or "")
        usage = meter.finish(outputs, success=True, metrics={"outputs": len(outputs)})
    except Exception as exc:
        usage = meter.finish([out_dir], success=False, error=str(exc))
        emit_result(tool="split", outputs=[out_dir], usage=usage, json_output=json_output)
        _append_usage(usage_file, usage.to_dict())
        raise typer.Exit(code=1)

    emit_result(tool="split", outputs=outputs, usage=usage, json_output=json_output)
    _append_usage(usage_file, usage.to_dict())


@app.command("compress")
def compress_cmd(
    input_pdf: Path = typer.Argument(..., exists=True, readable=True),
    out: Path = typer.Option(..., "--out"),
    preset: str = typer.Option("screen", "--preset", help="screen|ebook|printer|prepress"),
    remove_metadata: bool = typer.Option(False, "--remove-metadata"),
    json_output: bool = typer.Option(False, "--json"),
    usage_file: Optional[Path] = typer.Option(None, "--usage-file"),
):
    meter = UsageMeter("compress", [input_pdf])
    try:
        compress_pdf(input_pdf, out, preset=preset, remove_metadata=remove_metadata)
        before = input_pdf.stat().st_size
        after = out.stat().st_size
        ratio = round((1 - (after / before)) * 100, 2) if before else 0
        usage = meter.finish([out], success=True, metrics={"compression_pct": ratio})
    except Exception as exc:
        usage = meter.finish([out], success=False, error=str(exc))
        emit_result(tool="compress", outputs=[out], usage=usage, json_output=json_output)
        _append_usage(usage_file, usage.to_dict())
        raise typer.Exit(code=1)

    emit_result(tool="compress", outputs=[out], usage=usage, json_output=json_output)
    _append_usage(usage_file, usage.to_dict())


@app.command("jpg-to-pdf")
def jpg_to_pdf_cmd(
    inputs: list[Path] = typer.Argument(..., exists=True, readable=True),
    out: Path = typer.Option(..., "--out"),
    page_size: Optional[str] = typer.Option(None, "--page-size", help="A4 or LETTER"),
    margin: int = typer.Option(0, "--margin", help="Margin in points"),
    json_output: bool = typer.Option(False, "--json"),
    usage_file: Optional[Path] = typer.Option(None, "--usage-file"),
):
    meter = UsageMeter("jpg_to_pdf", inputs)
    try:
        images_to_pdf(inputs, out, page_size=page_size, margin=margin)
        usage = meter.finish([out], success=True)
    except Exception as exc:
        usage = meter.finish([out], success=False, error=str(exc))
        emit_result(tool="jpg_to_pdf", outputs=[out], usage=usage, json_output=json_output)
        _append_usage(usage_file, usage.to_dict())
        raise typer.Exit(code=1)

    emit_result(tool="jpg_to_pdf", outputs=[out], usage=usage, json_output=json_output)
    _append_usage(usage_file, usage.to_dict())


@app.command("word-to-pdf")
def word_to_pdf_cmd(
    input_doc: Path = typer.Argument(..., exists=True, readable=True),
    out_dir: Path = typer.Option(..., "--out-dir"),
    json_output: bool = typer.Option(False, "--json"),
    usage_file: Optional[Path] = typer.Option(None, "--usage-file"),
):
    meter = UsageMeter("word_to_pdf", [input_doc])
    try:
        out_path = office_to_pdf(input_doc, out_dir)
        usage = meter.finish([out_path], success=True)
    except Exception as exc:
        usage = meter.finish([out_dir], success=False, error=str(exc))
        emit_result(tool="word_to_pdf", outputs=[out_dir], usage=usage, json_output=json_output)
        _append_usage(usage_file, usage.to_dict())
        raise typer.Exit(code=1)

    emit_result(tool="word_to_pdf", outputs=[out_path], usage=usage, json_output=json_output)
    _append_usage(usage_file, usage.to_dict())


@app.command("powerpoint-to-pdf")
def powerpoint_to_pdf_cmd(
    input_ppt: Path = typer.Argument(..., exists=True, readable=True),
    out_dir: Path = typer.Option(..., "--out-dir"),
    json_output: bool = typer.Option(False, "--json"),
    usage_file: Optional[Path] = typer.Option(None, "--usage-file"),
):
    meter = UsageMeter("powerpoint_to_pdf", [input_ppt])
    try:
        out_path = office_to_pdf(input_ppt, out_dir)
        usage = meter.finish([out_path], success=True)
    except Exception as exc:
        usage = meter.finish([out_dir], success=False, error=str(exc))
        emit_result(tool="powerpoint_to_pdf", outputs=[out_dir], usage=usage, json_output=json_output)
        _append_usage(usage_file, usage.to_dict())
        raise typer.Exit(code=1)

    emit_result(tool="powerpoint_to_pdf", outputs=[out_path], usage=usage, json_output=json_output)
    _append_usage(usage_file, usage.to_dict())


@app.command("excel-to-pdf")
def excel_to_pdf_cmd(
    input_xls: Path = typer.Argument(..., exists=True, readable=True),
    out_dir: Path = typer.Option(..., "--out-dir"),
    json_output: bool = typer.Option(False, "--json"),
    usage_file: Optional[Path] = typer.Option(None, "--usage-file"),
):
    meter = UsageMeter("excel_to_pdf", [input_xls])
    try:
        out_path = office_to_pdf(input_xls, out_dir)
        usage = meter.finish([out_path], success=True)
    except Exception as exc:
        usage = meter.finish([out_dir], success=False, error=str(exc))
        emit_result(tool="excel_to_pdf", outputs=[out_dir], usage=usage, json_output=json_output)
        _append_usage(usage_file, usage.to_dict())
        raise typer.Exit(code=1)

    emit_result(tool="excel_to_pdf", outputs=[out_path], usage=usage, json_output=json_output)
    _append_usage(usage_file, usage.to_dict())


@app.command("html-to-pdf")
def html_to_pdf_cmd(
    source: str = typer.Argument(..., help="URL or HTML file path"),
    out: Path = typer.Option(..., "--out"),
    json_output: bool = typer.Option(False, "--json"),
    usage_file: Optional[Path] = typer.Option(None, "--usage-file"),
):
    meter = UsageMeter("html_to_pdf", [Path(source)] if Path(source).exists() else [])
    try:
        html_to_pdf(source, out)
        usage = meter.finish([out], success=True)
    except Exception as exc:
        usage = meter.finish([out], success=False, error=str(exc))
        emit_result(tool="html_to_pdf", outputs=[out], usage=usage, json_output=json_output)
        _append_usage(usage_file, usage.to_dict())
        raise typer.Exit(code=1)

    emit_result(tool="html_to_pdf", outputs=[out], usage=usage, json_output=json_output)
    _append_usage(usage_file, usage.to_dict())


@app.command("pdf-to-jpg")
def pdf_to_jpg_cmd(
    input_pdf: Path = typer.Argument(..., exists=True, readable=True),
    out_dir: Path = typer.Option(..., "--out-dir"),
    dpi: int = typer.Option(150, "--dpi"),
    first_page: Optional[int] = typer.Option(None, "--from"),
    last_page: Optional[int] = typer.Option(None, "--to"),
    json_output: bool = typer.Option(False, "--json"),
    usage_file: Optional[Path] = typer.Option(None, "--usage-file"),
):
    meter = UsageMeter("pdf_to_jpg", [input_pdf])
    try:
        outputs = pdf_to_jpg(input_pdf, out_dir, dpi=dpi, first_page=first_page, last_page=last_page)
        usage = meter.finish(outputs, success=True, metrics={"outputs": len(outputs)})
    except Exception as exc:
        usage = meter.finish([out_dir], success=False, error=str(exc))
        emit_result(tool="pdf_to_jpg", outputs=[out_dir], usage=usage, json_output=json_output)
        _append_usage(usage_file, usage.to_dict())
        raise typer.Exit(code=1)

    emit_result(tool="pdf_to_jpg", outputs=outputs, usage=usage, json_output=json_output)
    _append_usage(usage_file, usage.to_dict())


@app.command("pdf-to-word")
def pdf_to_word_cmd(
    input_pdf: Path = typer.Argument(..., exists=True, readable=True),
    out: Path = typer.Option(..., "--out"),
    start: Optional[int] = typer.Option(None, "--start"),
    end: Optional[int] = typer.Option(None, "--end"),
    json_output: bool = typer.Option(False, "--json"),
    usage_file: Optional[Path] = typer.Option(None, "--usage-file"),
):
    meter = UsageMeter("pdf_to_word", [input_pdf])
    try:
        pdf_to_docx(input_pdf, out, start=start, end=end)
        usage = meter.finish([out], success=True)
    except Exception as exc:
        usage = meter.finish([out], success=False, error=str(exc))
        emit_result(tool="pdf_to_word", outputs=[out], usage=usage, json_output=json_output)
        _append_usage(usage_file, usage.to_dict())
        raise typer.Exit(code=1)

    emit_result(tool="pdf_to_word", outputs=[out], usage=usage, json_output=json_output)
    _append_usage(usage_file, usage.to_dict())


@app.command("pdf-to-powerpoint")
def pdf_to_powerpoint_cmd(
    input_pdf: Path = typer.Argument(..., exists=True, readable=True),
    out: Path = typer.Option(..., "--out"),
    dpi: int = typer.Option(150, "--dpi"),
    json_output: bool = typer.Option(False, "--json"),
    usage_file: Optional[Path] = typer.Option(None, "--usage-file"),
):
    meter = UsageMeter("pdf_to_powerpoint", [input_pdf])
    try:
        pdf_to_pptx(input_pdf, out, dpi=dpi)
        usage = meter.finish([out], success=True)
    except Exception as exc:
        usage = meter.finish([out], success=False, error=str(exc))
        emit_result(tool="pdf_to_powerpoint", outputs=[out], usage=usage, json_output=json_output)
        _append_usage(usage_file, usage.to_dict())
        raise typer.Exit(code=1)

    emit_result(tool="pdf_to_powerpoint", outputs=[out], usage=usage, json_output=json_output)
    _append_usage(usage_file, usage.to_dict())


@app.command("pdf-to-excel")
def pdf_to_excel_cmd(
    input_pdf: Path = typer.Argument(..., exists=True, readable=True),
    out: Path = typer.Option(..., "--out"),
    pages: str = typer.Option("1", "--pages", help="Camelot pages spec"),
    flavor: str = typer.Option("stream", "--flavor", help="stream or lattice"),
    json_output: bool = typer.Option(False, "--json"),
    usage_file: Optional[Path] = typer.Option(None, "--usage-file"),
):
    meter = UsageMeter("pdf_to_excel", [input_pdf])
    try:
        pdf_to_xlsx(input_pdf, out, pages=pages, flavor=flavor)
        usage = meter.finish([out], success=True)
    except Exception as exc:
        usage = meter.finish([out], success=False, error=str(exc))
        emit_result(tool="pdf_to_excel", outputs=[out], usage=usage, json_output=json_output)
        _append_usage(usage_file, usage.to_dict())
        raise typer.Exit(code=1)

    emit_result(tool="pdf_to_excel", outputs=[out], usage=usage, json_output=json_output)
    _append_usage(usage_file, usage.to_dict())


@app.command("pdf-to-pdfa")
def pdf_to_pdfa_cmd(
    input_pdf: Path = typer.Argument(..., exists=True, readable=True),
    out: Path = typer.Option(..., "--out"),
    level: int = typer.Option(2, "--level"),
    icc: Path = typer.Option(..., "--icc", exists=True, readable=True),
    json_output: bool = typer.Option(False, "--json"),
    usage_file: Optional[Path] = typer.Option(None, "--usage-file"),
):
    meter = UsageMeter("pdf_to_pdfa", [input_pdf])
    try:
        pdf_to_pdfa(input_pdf, out, level=level, icc_profile=icc)
        usage = meter.finish([out], success=True)
    except Exception as exc:
        usage = meter.finish([out], success=False, error=str(exc))
        emit_result(tool="pdf_to_pdfa", outputs=[out], usage=usage, json_output=json_output)
        _append_usage(usage_file, usage.to_dict())
        raise typer.Exit(code=1)

    emit_result(tool="pdf_to_pdfa", outputs=[out], usage=usage, json_output=json_output)
    _append_usage(usage_file, usage.to_dict())


@app.command("remove-pages")
def remove_pages_cmd(
    input_pdf: Path = typer.Argument(..., exists=True, readable=True),
    out: Path = typer.Option(..., "--out"),
    pages: str = typer.Option(..., "--pages", help="Pages to remove (e.g. 1-3,5 or odd/even)"),
    json_output: bool = typer.Option(False, "--json"),
    usage_file: Optional[Path] = typer.Option(None, "--usage-file"),
):
    meter = UsageMeter("remove_pages", [input_pdf])
    try:
        remove_pages(input_pdf, out, pages)
        usage = meter.finish([out], success=True)
    except Exception as exc:
        usage = meter.finish([out], success=False, error=str(exc))
        emit_result(tool="remove_pages", outputs=[out], usage=usage, json_output=json_output)
        _append_usage(usage_file, usage.to_dict())
        raise typer.Exit(code=1)

    emit_result(tool="remove_pages", outputs=[out], usage=usage, json_output=json_output)
    _append_usage(usage_file, usage.to_dict())


@app.command("extract-pages")
def extract_pages_cmd(
    input_pdf: Path = typer.Argument(..., exists=True, readable=True),
    pages: str = typer.Option(..., "--pages"),
    out: Optional[Path] = typer.Option(None, "--out", help="Output PDF (single-file)"),
    out_dir: Optional[Path] = typer.Option(None, "--out-dir", help="Output directory (multi-file)"),
    multi: bool = typer.Option(False, "--multi", help="Create one file per page"),
    json_output: bool = typer.Option(False, "--json"),
    usage_file: Optional[Path] = typer.Option(None, "--usage-file"),
):
    meter = UsageMeter("extract_pages", [input_pdf])
    try:
        outputs = extract_pages(input_pdf, out, out_dir, pages, single_file=not multi)
        usage = meter.finish(outputs, success=True, metrics={"outputs": len(outputs)})
    except Exception as exc:
        usage = meter.finish([out_dir or out or input_pdf], success=False, error=str(exc))
        emit_result(tool="extract_pages", outputs=[out_dir or out or input_pdf], usage=usage, json_output=json_output)
        _append_usage(usage_file, usage.to_dict())
        raise typer.Exit(code=1)

    emit_result(tool="extract_pages", outputs=outputs, usage=usage, json_output=json_output)
    _append_usage(usage_file, usage.to_dict())


@app.command("organize")
def organize_cmd(
    input_pdf: Path = typer.Argument(..., exists=True, readable=True),
    out: Path = typer.Option(..., "--out"),
    order: Optional[str] = typer.Option(None, "--order", help="New order e.g. 3,1,2"),
    insert: Optional[str] = typer.Option(None, "--insert", help="Insert file@position"),
    json_output: bool = typer.Option(False, "--json"),
    usage_file: Optional[Path] = typer.Option(None, "--usage-file"),
):
    meter = UsageMeter("organize", [input_pdf])
    try:
        if order:
            reorder_pages(input_pdf, out, order)
        elif insert:
            if "@" not in insert:
                raise ValueError("--insert expects file@position")
            path_s, pos_s = insert.split("@", 1)
            insert_pdf(input_pdf, Path(path_s), out, int(pos_s))
        else:
            raise ValueError("Provide --order or --insert")
        usage = meter.finish([out], success=True)
    except Exception as exc:
        usage = meter.finish([out], success=False, error=str(exc))
        emit_result(tool="organize", outputs=[out], usage=usage, json_output=json_output)
        _append_usage(usage_file, usage.to_dict())
        raise typer.Exit(code=1)

    emit_result(tool="organize", outputs=[out], usage=usage, json_output=json_output)
    _append_usage(usage_file, usage.to_dict())


@app.command("scan-to-pdf")
def scan_to_pdf_cmd(
    inputs: list[Path] = typer.Argument(..., exists=True, readable=True),
    out: Path = typer.Option(..., "--out"),
    enhance: bool = typer.Option(False, "--enhance"),
    grayscale: bool = typer.Option(False, "--grayscale"),
    ocr: bool = typer.Option(False, "--ocr"),
    ocr_lang: str = typer.Option("eng", "--ocr-lang"),
    json_output: bool = typer.Option(False, "--json"),
    usage_file: Optional[Path] = typer.Option(None, "--usage-file"),
):
    meter = UsageMeter("scan_to_pdf", inputs)
    try:
        scan_to_pdf(inputs, out, enhance=enhance, grayscale=grayscale, ocr=ocr, ocr_lang=ocr_lang)
        usage = meter.finish([out], success=True)
    except Exception as exc:
        usage = meter.finish([out], success=False, error=str(exc))
        emit_result(tool="scan_to_pdf", outputs=[out], usage=usage, json_output=json_output)
        _append_usage(usage_file, usage.to_dict())
        raise typer.Exit(code=1)

    emit_result(tool="scan_to_pdf", outputs=[out], usage=usage, json_output=json_output)
    _append_usage(usage_file, usage.to_dict())


@app.command("repair")
def repair_cmd(
    input_pdf: Path = typer.Argument(..., exists=True, readable=True),
    out: Path = typer.Option(..., "--out"),
    json_output: bool = typer.Option(False, "--json"),
    usage_file: Optional[Path] = typer.Option(None, "--usage-file"),
):
    meter = UsageMeter("repair", [input_pdf])
    try:
        repair_pdf(input_pdf, out)
        usage = meter.finish([out], success=True)
    except Exception as exc:
        usage = meter.finish([out], success=False, error=str(exc))
        emit_result(tool="repair", outputs=[out], usage=usage, json_output=json_output)
        _append_usage(usage_file, usage.to_dict())
        raise typer.Exit(code=1)

    emit_result(tool="repair", outputs=[out], usage=usage, json_output=json_output)
    _append_usage(usage_file, usage.to_dict())


@app.command("ocr")
def ocr_cmd(
    input_pdf: Path = typer.Argument(..., exists=True, readable=True),
    out: Path = typer.Option(..., "--out"),
    languages: str = typer.Option("eng", "--lang"),
    deskew: bool = typer.Option(False, "--deskew"),
    force: bool = typer.Option(False, "--force"),
    json_output: bool = typer.Option(False, "--json"),
    usage_file: Optional[Path] = typer.Option(None, "--usage-file"),
):
    meter = UsageMeter("ocr", [input_pdf])
    try:
        ocr_pdf(input_pdf, out, languages=languages, deskew=deskew, force=force)
        usage = meter.finish([out], success=True)
    except Exception as exc:
        usage = meter.finish([out], success=False, error=str(exc))
        emit_result(tool="ocr", outputs=[out], usage=usage, json_output=json_output)
        _append_usage(usage_file, usage.to_dict())
        raise typer.Exit(code=1)

    emit_result(tool="ocr", outputs=[out], usage=usage, json_output=json_output)
    _append_usage(usage_file, usage.to_dict())


@app.command("rotate")
def rotate_cmd(
    input_pdf: Path = typer.Argument(..., exists=True, readable=True, help="Input PDF"),
    out: Path = typer.Option(..., "--out", help="Output PDF path"),
    degrees: int = typer.Option(..., "--degrees", help="Rotation degrees (multiple of 90)"),
    pages: Optional[str] = typer.Option(None, "--pages", help="Pages to rotate, e.g. 1-3,5"),
    json_output: bool = typer.Option(False, "--json", help="Emit JSON output"),
    usage_file: Optional[Path] = typer.Option(None, "--usage-file", help="Append JSON usage to file"),
):
    meter = UsageMeter("rotate", [input_pdf])
    try:
        rotate_pdf(input_pdf, out, degrees=degrees, pages=pages)
        usage = meter.finish([out], success=True)
    except Exception as exc:
        usage = meter.finish([out], success=False, error=str(exc))
        emit_result(tool="rotate", outputs=[out], usage=usage, json_output=json_output)
        _append_usage(usage_file, usage.to_dict())
        raise typer.Exit(code=1)

    emit_result(tool="rotate", outputs=[out], usage=usage, json_output=json_output)
    _append_usage(usage_file, usage.to_dict())


@app.command("add-page-numbers")
def add_page_numbers_cmd(
    input_pdf: Path = typer.Argument(..., exists=True, readable=True),
    out: Path = typer.Option(..., "--out"),
    start: int = typer.Option(1, "--start"),
    position: str = typer.Option("bottom-center", "--position"),
    pages: Optional[str] = typer.Option(None, "--pages"),
    json_output: bool = typer.Option(False, "--json"),
    usage_file: Optional[Path] = typer.Option(None, "--usage-file"),
):
    meter = UsageMeter("add_page_numbers", [input_pdf])
    try:
        add_page_numbers(input_pdf, out, start=start, position=position, pages=pages)
        usage = meter.finish([out], success=True)
    except Exception as exc:
        usage = meter.finish([out], success=False, error=str(exc))
        emit_result(tool="add_page_numbers", outputs=[out], usage=usage, json_output=json_output)
        _append_usage(usage_file, usage.to_dict())
        raise typer.Exit(code=1)

    emit_result(tool="add_page_numbers", outputs=[out], usage=usage, json_output=json_output)
    _append_usage(usage_file, usage.to_dict())


@app.command("watermark")
def watermark_cmd(
    input_pdf: Path = typer.Argument(..., exists=True, readable=True),
    out: Path = typer.Option(..., "--out"),
    text: Optional[str] = typer.Option(None, "--text"),
    image: Optional[Path] = typer.Option(None, "--image", exists=True, readable=True),
    opacity: float = typer.Option(0.3, "--opacity"),
    rotation: int = typer.Option(45, "--rotation"),
    position: str = typer.Option("center", "--position"),
    pages: Optional[str] = typer.Option(None, "--pages"),
    json_output: bool = typer.Option(False, "--json"),
    usage_file: Optional[Path] = typer.Option(None, "--usage-file"),
):
    meter = UsageMeter("watermark", [input_pdf])
    try:
        add_watermark(
            input_pdf,
            out,
            text=text,
            image=image,
            opacity=opacity,
            rotation=rotation,
            position=position,
            pages=pages,
        )
        usage = meter.finish([out], success=True)
    except Exception as exc:
        usage = meter.finish([out], success=False, error=str(exc))
        emit_result(tool="watermark", outputs=[out], usage=usage, json_output=json_output)
        _append_usage(usage_file, usage.to_dict())
        raise typer.Exit(code=1)

    emit_result(tool="watermark", outputs=[out], usage=usage, json_output=json_output)
    _append_usage(usage_file, usage.to_dict())


@app.command("crop")
def crop_cmd(
    input_pdf: Path = typer.Argument(..., exists=True, readable=True),
    out: Path = typer.Option(..., "--out"),
    left: float = typer.Option(0, "--left"),
    top: float = typer.Option(0, "--top"),
    right: float = typer.Option(0, "--right"),
    bottom: float = typer.Option(0, "--bottom"),
    pages: Optional[str] = typer.Option(None, "--pages"),
    apply_media: bool = typer.Option(False, "--apply-media"),
    json_output: bool = typer.Option(False, "--json"),
    usage_file: Optional[Path] = typer.Option(None, "--usage-file"),
):
    meter = UsageMeter("crop", [input_pdf])
    try:
        crop_pdf(
            input_pdf,
            out,
            left=left,
            top=top,
            right=right,
            bottom=bottom,
            pages=pages,
            apply_media=apply_media,
        )
        usage = meter.finish([out], success=True)
    except Exception as exc:
        usage = meter.finish([out], success=False, error=str(exc))
        emit_result(tool="crop", outputs=[out], usage=usage, json_output=json_output)
        _append_usage(usage_file, usage.to_dict())
        raise typer.Exit(code=1)

    emit_result(tool="crop", outputs=[out], usage=usage, json_output=json_output)
    _append_usage(usage_file, usage.to_dict())


@app.command("edit")
def edit_cmd(
    input_pdf: Path = typer.Argument(..., exists=True, readable=True),
    out: Path = typer.Option(..., "--out"),
    text: Optional[str] = typer.Option(None, "--text"),
    image: Optional[Path] = typer.Option(None, "--image", exists=True, readable=True),
    x: float = typer.Option(50, "--x"),
    y: float = typer.Option(50, "--y"),
    width: Optional[float] = typer.Option(None, "--width"),
    height: Optional[float] = typer.Option(None, "--height"),
    pages: Optional[str] = typer.Option(None, "--pages"),
    json_output: bool = typer.Option(False, "--json"),
    usage_file: Optional[Path] = typer.Option(None, "--usage-file"),
):
    meter = UsageMeter("edit", [input_pdf])
    try:
        if text:
            add_text(input_pdf, out, text=text, x=x, y=y, pages=pages)
        elif image:
            add_image(input_pdf, out, image=image, x=x, y=y, width=width, height=height, pages=pages)
        else:
            raise ValueError("Provide --text or --image")
        usage = meter.finish([out], success=True)
    except Exception as exc:
        usage = meter.finish([out], success=False, error=str(exc))
        emit_result(tool="edit", outputs=[out], usage=usage, json_output=json_output)
        _append_usage(usage_file, usage.to_dict())
        raise typer.Exit(code=1)

    emit_result(tool="edit", outputs=[out], usage=usage, json_output=json_output)
    _append_usage(usage_file, usage.to_dict())


@app.command("unlock")
def unlock_cmd(
    input_pdf: Path = typer.Argument(..., exists=True, readable=True),
    out: Path = typer.Option(..., "--out"),
    password: str = typer.Option(..., "--password"),
    json_output: bool = typer.Option(False, "--json"),
    usage_file: Optional[Path] = typer.Option(None, "--usage-file"),
):
    meter = UsageMeter("unlock", [input_pdf])
    try:
        unlock_pdf(input_pdf, out, password=password)
        usage = meter.finish([out], success=True)
    except Exception as exc:
        usage = meter.finish([out], success=False, error=str(exc))
        emit_result(tool="unlock", outputs=[out], usage=usage, json_output=json_output)
        _append_usage(usage_file, usage.to_dict())
        raise typer.Exit(code=1)

    emit_result(tool="unlock", outputs=[out], usage=usage, json_output=json_output)
    _append_usage(usage_file, usage.to_dict())


@app.command("protect")
def protect_cmd(
    input_pdf: Path = typer.Argument(..., exists=True, readable=True),
    out: Path = typer.Option(..., "--out"),
    password: str = typer.Option(..., "--password"),
    owner_password: Optional[str] = typer.Option(None, "--owner-password"),
    allow_print: bool = typer.Option(False, "--allow-print"),
    allow_copy: bool = typer.Option(False, "--allow-copy"),
    allow_modify: bool = typer.Option(False, "--allow-modify"),
    json_output: bool = typer.Option(False, "--json"),
    usage_file: Optional[Path] = typer.Option(None, "--usage-file"),
):
    meter = UsageMeter("protect", [input_pdf])
    try:
        protect_pdf(
            input_pdf,
            out,
            user_password=password,
            owner_password=owner_password,
            allow_print=allow_print,
            allow_copy=allow_copy,
            allow_modify=allow_modify,
        )
        usage = meter.finish([out], success=True)
    except Exception as exc:
        usage = meter.finish([out], success=False, error=str(exc))
        emit_result(tool="protect", outputs=[out], usage=usage, json_output=json_output)
        _append_usage(usage_file, usage.to_dict())
        raise typer.Exit(code=1)

    emit_result(tool="protect", outputs=[out], usage=usage, json_output=json_output)
    _append_usage(usage_file, usage.to_dict())


@app.command("sign")
def sign_cmd(
    input_pdf: Path = typer.Argument(..., exists=True, readable=True),
    out: Path = typer.Option(..., "--out"),
    text: Optional[str] = typer.Option(None, "--text"),
    image: Optional[Path] = typer.Option(None, "--image", exists=True, readable=True),
    x: float = typer.Option(50, "--x"),
    y: float = typer.Option(50, "--y"),
    width: float = typer.Option(200, "--width"),
    height: float = typer.Option(80, "--height"),
    digital_cert: Optional[Path] = typer.Option(None, "--cert", exists=True, readable=True),
    digital_key: Optional[Path] = typer.Option(None, "--key", exists=True, readable=True),
    key_password: Optional[str] = typer.Option(None, "--key-password"),
    pages: Optional[str] = typer.Option(None, "--pages"),
    json_output: bool = typer.Option(False, "--json"),
    usage_file: Optional[Path] = typer.Option(None, "--usage-file"),
):
    meter = UsageMeter("sign", [input_pdf])
    try:
        if digital_cert and digital_key:
            sign_digital(input_pdf, out, cert_path=digital_cert, key_path=digital_key, key_password=key_password)
        else:
            sign_visible(input_pdf, out, text=text, image=image, x=x, y=y, width=width, height=height, pages=pages)
        usage = meter.finish([out], success=True)
    except Exception as exc:
        usage = meter.finish([out], success=False, error=str(exc))
        emit_result(tool="sign", outputs=[out], usage=usage, json_output=json_output)
        _append_usage(usage_file, usage.to_dict())
        raise typer.Exit(code=1)

    emit_result(tool="sign", outputs=[out], usage=usage, json_output=json_output)
    _append_usage(usage_file, usage.to_dict())


@app.command("redact")
def redact_cmd(
    input_pdf: Path = typer.Argument(..., exists=True, readable=True),
    out: Path = typer.Option(..., "--out"),
    box: list[str] = typer.Option([], "--box", help="page,x,y,width,height"),
    search: Optional[str] = typer.Option(None, "--search"),
    pages: Optional[str] = typer.Option(None, "--pages"),
    mode: str = typer.Option("overlay", "--mode", help="overlay or rasterize"),
    json_output: bool = typer.Option(False, "--json"),
    usage_file: Optional[Path] = typer.Option(None, "--usage-file"),
):
    meter = UsageMeter("redact", [input_pdf])
    try:
        boxes: list[RedactionBox] = []
        for spec in box:
            parts = [p.strip() for p in spec.split(",")]
            if len(parts) != 5:
                raise ValueError("--box expects page,x,y,width,height")
            page, x, y, w, h = parts
            boxes.append(RedactionBox(page=int(page), x=float(x), y=float(y), width=float(w), height=float(h)))
        redact_pdf(input_pdf, out, boxes=boxes, search=search, pages=pages, mode=mode)
        usage = meter.finish([out], success=True)
    except Exception as exc:
        usage = meter.finish([out], success=False, error=str(exc))
        emit_result(tool="redact", outputs=[out], usage=usage, json_output=json_output)
        _append_usage(usage_file, usage.to_dict())
        raise typer.Exit(code=1)

    emit_result(tool="redact", outputs=[out], usage=usage, json_output=json_output)
    _append_usage(usage_file, usage.to_dict())


@app.command("compare")
def compare_cmd(
    left: Path = typer.Argument(..., exists=True, readable=True),
    right: Path = typer.Argument(..., exists=True, readable=True),
    out_dir: Path = typer.Option(..., "--out-dir"),
    report_pdf: bool = typer.Option(True, "--report-pdf/--no-report-pdf"),
    json_output: bool = typer.Option(False, "--json"),
    usage_file: Optional[Path] = typer.Option(None, "--usage-file"),
):
    meter = UsageMeter("compare", [left, right])
    try:
        result = compare_pdfs(left, right, out_dir, report_pdf=report_pdf)
        outputs = [result.summary_path] + ([result.report_pdf] if result.report_pdf else [])
        usage = meter.finish(outputs, success=True, metrics={"outputs": len(outputs)})
    except Exception as exc:
        usage = meter.finish([out_dir], success=False, error=str(exc))
        emit_result(tool="compare", outputs=[out_dir], usage=usage, json_output=json_output)
        _append_usage(usage_file, usage.to_dict())
        raise typer.Exit(code=1)

    emit_result(tool="compare", outputs=outputs, usage=usage, json_output=json_output)
    _append_usage(usage_file, usage.to_dict())


@app.command("translate")
def translate_cmd(
    input_pdf: Path = typer.Argument(..., exists=True, readable=True),
    out: Path = typer.Option(..., "--out"),
    target: str = typer.Option(..., "--to"),
    source: Optional[str] = typer.Option(None, "--from"),
    provider: str = typer.Option("command", "--provider", help="none|command|ollama"),
    llm_cmd: Optional[str] = typer.Option(None, "--llm-cmd"),
    model: Optional[str] = typer.Option(None, "--model"),
    text_out: Optional[Path] = typer.Option(None, "--text-out"),
    json_output: bool = typer.Option(False, "--json"),
    usage_file: Optional[Path] = typer.Option(None, "--usage-file"),
):
    meter = UsageMeter("translate", [input_pdf])
    try:
        translate_pdf(
            input_pdf,
            out,
            source_lang=source,
            target_lang=target,
            provider=provider,
            llm_cmd=llm_cmd,
            model=model,
            text_out=text_out,
        )
        outputs = [out] + ([text_out] if text_out else [])
        usage = meter.finish(outputs, success=True)
    except Exception as exc:
        usage = meter.finish([out], success=False, error=str(exc))
        emit_result(tool="translate", outputs=[out], usage=usage, json_output=json_output)
        _append_usage(usage_file, usage.to_dict())
        raise typer.Exit(code=1)

    emit_result(tool="translate", outputs=outputs, usage=usage, json_output=json_output)
    _append_usage(usage_file, usage.to_dict())


@app.command("workflow")
def workflow_cmd(
    file: Path = typer.Argument(..., exists=True, readable=True, help="Workflow JSON file"),
    json_output: bool = typer.Option(False, "--json"),
    usage_file: Optional[Path] = typer.Option(None, "--usage-file"),
):
    data = json.loads(file.read_text(encoding="utf-8"))
    steps = data.get("steps", [])
    if not isinstance(steps, list) or not steps:
        raise typer.Exit("Workflow must include steps")

    current_inputs = [Path(p) for p in data.get("inputs", [])]
    if not current_inputs:
        raise typer.Exit("Workflow requires inputs")

    step_usages: list[Usage] = []
    final_outputs: list[Path] = []
    work_dir = Path(tempfile.mkdtemp(prefix="pdfagent_workflow_"))

    for idx, step in enumerate(steps):
        tool = step.get("tool")
        params = step.get("params", {})
        outputs, usage = _run_tool_step(tool, current_inputs, params, work_dir)
        step_usages.append(usage)
        current_inputs = outputs
        final_outputs = outputs

    total = _sum_usage(step_usages)
    if json_output:
        payload = {
            "tool": "workflow",
            "outputs": [str(p) for p in final_outputs],
            "usage": total.to_dict(),
            "steps": [
                {"tool": u.tool, "outputs": u.outputs, "usage": u.to_dict()} for u in step_usages
            ],
        }
        print(json.dumps(payload, indent=2))
    else:
        print("Tool: workflow")
        print("Outputs:")
        for out in final_outputs:
            print(f"- {out}")
        print("Usage:")
        print(f"  Duration (ms): {total.duration_ms}")

    _append_usage(usage_file, total.to_dict())


@app.command("agent")
def agent_cmd(
    text: str = typer.Argument(..., help="Natural-language instruction"),
    inputs: list[Path] = typer.Option(None, "--input", "-i", help="Input files", exists=True, readable=True),
    out: Optional[Path] = typer.Option(None, "--out", help="Final output path"),
    out_dir: Optional[Path] = typer.Option(None, "--out-dir", help="Final output directory"),
    plan: bool = typer.Option(False, "--plan", help="Show planned steps without running"),
    provider: str = typer.Option("none", "--provider", help="none|command|ollama"),
    llm_cmd: Optional[str] = typer.Option(None, "--llm-cmd", help="Command to run LLM"),
    model: Optional[str] = typer.Option(None, "--model", help="LLM model name (ollama)"),
    password: Optional[str] = typer.Option(None, "--password", help="Default password for encrypted PDFs"),
    passwords: Optional[str] = typer.Option(None, "--passwords", help="Per-file passwords: file=pass,file2=pass2"),
    json_output: bool = typer.Option(False, "--json", help="Emit JSON output"),
    usage_file: Optional[Path] = typer.Option(None, "--usage-file", help="Append JSON usage to file"),
):
    if provider != "none":
        prompt = _agent_prompt(text)
        try:
            plan_obj = generate_plan(provider=provider, prompt=prompt, cmd=llm_cmd, model=model)
            steps = plan_obj.get("steps", [])
        except LLMError as exc:
            typer.echo(str(exc), err=True)
            raise typer.Exit(code=2)
    else:
        steps = [s.__dict__ for s in parse_agent_text(text)]

    if not steps:
        raise typer.Exit("No steps generated")

    if plan:
        typer.echo("Planned steps:")
        for step in steps:
            typer.echo(f"- {step.get('tool')} {step.get('params', {})}")
        raise typer.Exit()

    if not inputs:
        typer.echo("--input is required for agent runs", err=True)
        raise typer.Exit(code=2)

    work_dir = Path(tempfile.mkdtemp(prefix="pdfagent_"))
    current_inputs = inputs
    step_usages: list[Usage] = []
    final_outputs: list[Path] = []

    default_passwords = _parse_passwords(passwords)
    for idx, step in enumerate(steps):
        tool = step.get("tool")
        params = step.get("params", {})
        if idx == len(steps) - 1:
            params = {**params}
            if out:
                params.setdefault("out", str(out))
            if out_dir:
                params.setdefault("out_dir", str(out_dir))
        if tool in {"merge"}:
            if password:
                params.setdefault("password", password)
            if default_passwords:
                params.setdefault("passwords", default_passwords)
        outputs, usage = _run_tool_step(tool, current_inputs, params, work_dir)
        step_usages.append(usage)
        current_inputs = outputs
        final_outputs = outputs

    total = _sum_usage(step_usages)
    if json_output:
        payload = {
            "tool": "agent",
            "outputs": [str(p) for p in final_outputs],
            "usage": total.to_dict(),
            "steps": [
                {"tool": u.tool, "outputs": u.outputs, "usage": u.to_dict()} for u in step_usages
            ],
        }
        print(json.dumps(payload, indent=2))
    else:
        print("Tool: agent")
        print("Steps:")
        for u in step_usages:
            print(f"- {u.tool}: {u.outputs}")
        print("Usage:")
        print(f"  Duration (ms): {total.duration_ms}")
        print(f"  CPU (ms): {total.cpu_ms}")
        print(f"  Bytes in: {total.bytes_in}")
        print(f"  Bytes out: {total.bytes_out}")
        if total.pages_in is not None:
            print(f"  Pages in: {total.pages_in}")
        if total.pages_out is not None:
            print(f"  Pages out: {total.pages_out}")

    _append_usage(usage_file, total.to_dict())
    for u in step_usages:
        _append_usage(usage_file, u.to_dict())


def _agent_prompt(text: str) -> str:
    tool_list = ", ".join(TOOLS)
    return (
        "You are a planner for a PDF CLI. Convert the user request into JSON with steps. "
        "Return only JSON: {\"steps\":[{\"tool\":...,\"params\":{...}}]}. "
        f"Tools: {tool_list}. "
        "Use tool names exactly as provided. Avoid natural language. "
        f"User request: {text}"
    )


def _run_tool_step(tool: str, inputs: list[Path], params: dict, work_dir: Path) -> tuple[list[Path], Usage]:
    tool = tool.replace("-", "_")

    if tool == "merge":
        out = Path(params.get("out") or work_dir / "merge.pdf")
        meter = UsageMeter("merge", inputs)
        merge_pdfs(
            inputs,
            out,
            password=params.get("password"),
            passwords=_normalize_passwords(params.get("passwords")),
        )
        return [out], meter.finish([out], success=True)

    if tool == "split":
        out_dir = Path(params.get("out_dir") or work_dir / "split")
        meter = UsageMeter("split", inputs)
        if len(inputs) != 1:
            raise ValueError("split expects one input")
        if "every" in params:
            outputs = split_every(inputs[0], out_dir, int(params["every"]))
        else:
            range_spec = params.get("range") or params.get("ranges") or ""
            outputs = split_ranges(inputs[0], out_dir, range_spec)
        return outputs, meter.finish(outputs, success=True, metrics={"outputs": len(outputs)})

    if tool == "jpg_to_pdf":
        out = Path(params.get("out") or work_dir / "images.pdf")
        meter = UsageMeter("jpg_to_pdf", inputs)
        images_to_pdf(inputs, out, page_size=params.get("page_size"), margin=int(params.get("margin", 0)))
        return [out], meter.finish([out], success=True)

    if tool == "compress":
        out = Path(params.get("out") or work_dir / "compress.pdf")
        meter = UsageMeter("compress", inputs)
        compress_pdf(inputs[0], out, preset=params.get("preset", "screen"))
        return [out], meter.finish([out], success=True)

    if tool == "pdf_to_jpg":
        out_dir = Path(params.get("out_dir") or work_dir / "pdf_to_jpg")
        meter = UsageMeter("pdf_to_jpg", inputs)
        outputs = pdf_to_jpg(inputs[0], out_dir, dpi=int(params.get("dpi", 150)))
        return outputs, meter.finish(outputs, success=True, metrics={"outputs": len(outputs)})

    if tool == "word_to_pdf":
        out_dir = Path(params.get("out_dir") or work_dir)
        meter = UsageMeter("word_to_pdf", inputs)
        out = office_to_pdf(inputs[0], out_dir)
        return [out], meter.finish([out], success=True)

    if tool == "powerpoint_to_pdf":
        out_dir = Path(params.get("out_dir") or work_dir)
        meter = UsageMeter("powerpoint_to_pdf", inputs)
        out = office_to_pdf(inputs[0], out_dir)
        return [out], meter.finish([out], success=True)

    if tool == "excel_to_pdf":
        out_dir = Path(params.get("out_dir") or work_dir)
        meter = UsageMeter("excel_to_pdf", inputs)
        out = office_to_pdf(inputs[0], out_dir)
        return [out], meter.finish([out], success=True)

    if tool == "html_to_pdf":
        out = Path(params.get("out") or work_dir / "page.pdf")
        meter = UsageMeter("html_to_pdf", inputs)
        html_to_pdf(params.get("source", str(inputs[0]) if inputs else ""), out)
        return [out], meter.finish([out], success=True)

    if tool == "pdf_to_word":
        out = Path(params.get("out") or work_dir / "output.docx")
        meter = UsageMeter("pdf_to_word", inputs)
        pdf_to_docx(inputs[0], out)
        return [out], meter.finish([out], success=True)

    if tool == "pdf_to_powerpoint":
        out = Path(params.get("out") or work_dir / "output.pptx")
        meter = UsageMeter("pdf_to_powerpoint", inputs)
        pdf_to_pptx(inputs[0], out)
        return [out], meter.finish([out], success=True)

    if tool == "pdf_to_excel":
        out = Path(params.get("out") or work_dir / "output.xlsx")
        meter = UsageMeter("pdf_to_excel", inputs)
        pdf_to_xlsx(inputs[0], out)
        return [out], meter.finish([out], success=True)

    if tool == "pdf_to_pdfa":
        out = Path(params.get("out") or work_dir / "output_pdfa.pdf")
        meter = UsageMeter("pdf_to_pdfa", inputs)
        pdf_to_pdfa(inputs[0], out, level=int(params.get("level", 2)), icc_profile=Path(params["icc"]))
        return [out], meter.finish([out], success=True)

    if tool == "remove_pages":
        out = Path(params.get("out") or work_dir / "remove_pages.pdf")
        meter = UsageMeter("remove_pages", inputs)
        remove_pages(inputs[0], out, params.get("pages", ""))
        return [out], meter.finish([out], success=True)

    if tool == "extract_pages":
        out_dir = Path(params.get("out_dir") or work_dir / "extract")
        meter = UsageMeter("extract_pages", inputs)
        outputs = extract_pages(inputs[0], None, out_dir, params.get("pages", ""), single_file=False)
        return outputs, meter.finish(outputs, success=True, metrics={"outputs": len(outputs)})

    if tool == "organize":
        out = Path(params.get("out") or work_dir / "organize.pdf")
        meter = UsageMeter("organize", inputs)
        if "order" in params:
            reorder_pages(inputs[0], out, params["order"])
        elif "insert" in params:
            path_s, pos_s = params["insert"].split("@", 1)
            insert_pdf(inputs[0], Path(path_s), out, int(pos_s))
        else:
            raise ValueError("organize requires order or insert")
        return [out], meter.finish([out], success=True)

    if tool == "scan_to_pdf":
        out = Path(params.get("out") or work_dir / "scan.pdf")
        meter = UsageMeter("scan_to_pdf", inputs)
        scan_to_pdf(inputs, out, enhance=bool(params.get("enhance", False)), grayscale=bool(params.get("grayscale", False)))
        return [out], meter.finish([out], success=True)

    if tool == "repair":
        out = Path(params.get("out") or work_dir / "repair.pdf")
        meter = UsageMeter("repair", inputs)
        repair_pdf(inputs[0], out)
        return [out], meter.finish([out], success=True)

    if tool == "ocr":
        out = Path(params.get("out") or work_dir / "ocr.pdf")
        meter = UsageMeter("ocr", inputs)
        ocr_pdf(inputs[0], out, languages=params.get("lang", "eng"))
        return [out], meter.finish([out], success=True)

    if tool == "rotate":
        out = Path(params.get("out") or work_dir / "rotate.pdf")
        meter = UsageMeter("rotate", inputs)
        rotate_pdf(inputs[0], out, degrees=int(params.get("degrees", 90)), pages=params.get("pages"))
        return [out], meter.finish([out], success=True)

    if tool == "edit":
        out = Path(params.get("out") or work_dir / "edit.pdf")
        meter = UsageMeter("edit", inputs)
        if "text" in params:
            add_text(inputs[0], out, text=params["text"], x=float(params.get("x", 50)), y=float(params.get("y", 50)))
        elif "image" in params:
            add_image(inputs[0], out, image=Path(params["image"]), x=float(params.get("x", 50)), y=float(params.get("y", 50)))
        else:
            raise ValueError("edit requires text or image")
        return [out], meter.finish([out], success=True)

    if tool == "protect":
        out = Path(params.get("out") or work_dir / "protect.pdf")
        meter = UsageMeter("protect", inputs)
        protect_pdf(inputs[0], out, user_password=params["password"], owner_password=params.get("owner_password"))
        return [out], meter.finish([out], success=True)

    if tool == "unlock":
        out = Path(params.get("out") or work_dir / "unlock.pdf")
        meter = UsageMeter("unlock", inputs)
        unlock_pdf(inputs[0], out, password=params["password"])
        return [out], meter.finish([out], success=True)

    if tool == "watermark":
        out = Path(params.get("out") or work_dir / "watermark.pdf")
        meter = UsageMeter("watermark", inputs)
        add_watermark(inputs[0], out, text=params.get("text"), pages=params.get("pages"))
        return [out], meter.finish([out], success=True)

    if tool == "add_page_numbers":
        out = Path(params.get("out") or work_dir / "page_numbers.pdf")
        meter = UsageMeter("add_page_numbers", inputs)
        add_page_numbers(inputs[0], out, start=int(params.get("start", 1)), pages=params.get("pages"))
        return [out], meter.finish([out], success=True)

    if tool == "crop":
        out = Path(params.get("out") or work_dir / "crop.pdf")
        meter = UsageMeter("crop", inputs)
        crop_pdf(
            inputs[0],
            out,
            left=float(params.get("left", 0)),
            top=float(params.get("top", 0)),
            right=float(params.get("right", 0)),
            bottom=float(params.get("bottom", 0)),
            pages=params.get("pages"),
        )
        return [out], meter.finish([out], success=True)

    if tool == "sign":
        out = Path(params.get("out") or work_dir / "sign.pdf")
        meter = UsageMeter("sign", inputs)
        if "cert" in params and "key" in params:
            sign_digital(inputs[0], out, cert_path=Path(params["cert"]), key_path=Path(params["key"]))
        else:
            sign_visible(
                inputs[0],
                out,
                text=params.get("text"),
                image=Path(params["image"]) if params.get("image") else None,
            )
        return [out], meter.finish([out], success=True)

    if tool == "redact":
        out = Path(params.get("out") or work_dir / "redact.pdf")
        meter = UsageMeter("redact", inputs)
        boxes = []
        for spec in params.get("box", []):
            parts = [p.strip() for p in spec.split(",")]
            if len(parts) != 5:
                continue
            page, x, y, w, h = parts
            boxes.append(RedactionBox(page=int(page), x=float(x), y=float(y), width=float(w), height=float(h)))
        redact_pdf(inputs[0], out, boxes=boxes, search=params.get("search"), mode=params.get("mode", "overlay"))
        return [out], meter.finish([out], success=True)

    if tool == "compare":
        out_dir = Path(params.get("out_dir") or work_dir / "compare")
        meter = UsageMeter("compare", inputs)
        result = compare_pdfs(inputs[0], inputs[1], out_dir, report_pdf=True)
        outputs = [result.summary_path] + ([result.report_pdf] if result.report_pdf else [])
        return outputs, meter.finish(outputs, success=True, metrics={"outputs": len(outputs)})

    if tool == "translate":
        out = Path(params.get("out") or work_dir / "translate.pdf")
        meter = UsageMeter("translate", inputs)
        translate_pdf(
            inputs[0],
            out,
            source_lang=params.get("from"),
            target_lang=params.get("to", "en"),
            provider=params.get("provider", "command"),
            llm_cmd=params.get("llm_cmd"),
            model=params.get("model"),
        )
        return [out], meter.finish([out], success=True)

    raise ValueError(f"Unsupported tool in agent/workflow: {tool}")


if __name__ == "__main__":
    app()
