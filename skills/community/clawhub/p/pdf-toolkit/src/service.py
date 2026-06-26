# pyright: reportMissingImports=false
from constants import (
    CMD_CONVERT,
    CMD_CREATE_PDF,
    CMD_DOCTOR,
    CMD_EXTRACT_IMAGES,
    CMD_EXTRACT_TABLES,
    CMD_EXTRACT_TEXT,
    CMD_INFO,
    CMD_MERGE,
    CMD_OCR,
    CMD_READ_DOCX,
    CMD_ROTATE,
    CMD_SPLIT,
    CMD_TTS,
    CMD_WRITE_DOCX,
    TABLE_CELL_SEP,
    TABLE_ROW_SEP,
    TTS_DEFAULT_VOICE,
    OCR_DEFAULT_LANG,
)
from utils import get_flag, get_positional_args, has_flag, resolve_path


# ---------------------------------------------------------------------------
# Dispatch
# ---------------------------------------------------------------------------


def dispatch(command: str, args: list[str]) -> dict:
    """Route a command string + remaining args to the appropriate handler."""
    try:
        if command == CMD_DOCTOR:
            return _cmd_doctor(args)
        elif command == CMD_INFO:
            return _cmd_info(args)
        elif command == CMD_EXTRACT_TEXT:
            return _cmd_extract_text(args)
        elif command == CMD_EXTRACT_TABLES:
            return _cmd_extract_tables(args)
        elif command == CMD_EXTRACT_IMAGES:
            return _cmd_extract_images(args)
        elif command == CMD_MERGE:
            return _cmd_merge(args)
        elif command == CMD_SPLIT:
            return _cmd_split(args)
        elif command == CMD_ROTATE:
            return _cmd_rotate(args)
        elif command == CMD_CREATE_PDF:
            return _cmd_create_pdf(args)
        elif command == CMD_READ_DOCX:
            return _cmd_read_docx(args)
        elif command == CMD_WRITE_DOCX:
            return _cmd_write_docx(args)
        elif command == CMD_OCR:
            return _cmd_ocr(args)
        elif command == CMD_TTS:
            return _cmd_tts(args)
        elif command == CMD_CONVERT:
            return _cmd_convert(args)
        else:
            return {
                "error": f"Unknown command: '{command}'. Run without arguments to see available commands."
            }
    except Exception as exc:
        return {"error": f"Unexpected error in '{command}': {exc}"}


# ---------------------------------------------------------------------------
# Command implementations
# ---------------------------------------------------------------------------


def _cmd_doctor(_args: list[str]) -> dict:
    from doctor import run_doctor

    return run_doctor()


def _cmd_info(args: list[str]) -> dict:
    positional = get_positional_args(args)
    if not positional:
        return {"error": "Usage: info <pdf_path>"}
    from pdf_info import get_pdf_info

    return get_pdf_info(positional[0])


def _cmd_extract_text(args: list[str]) -> dict:
    positional = get_positional_args(args)
    if not positional:
        return {"error": "Usage: extract-text <pdf_path> [--pages 1,3,5-8]"}
    pages = get_flag(args, "--pages")
    from extract_text import extract_text

    return extract_text(positional[0], pages)


def _cmd_extract_tables(args: list[str]) -> dict:
    positional = get_positional_args(args)
    if not positional:
        return {"error": "Usage: extract-tables <pdf_path> [--pages 2-4]"}
    pages = get_flag(args, "--pages")
    from extract_text import extract_tables

    return extract_tables(positional[0], pages)


def _cmd_extract_images(args: list[str]) -> dict:
    positional = get_positional_args(args)
    if not positional:
        return {"error": "Usage: extract-images <pdf_path> [--output-dir /path]"}
    output_dir = get_flag(args, "--output-dir")
    from extract_text import extract_images

    return extract_images(positional[0], output_dir)


def _cmd_merge(args: list[str]) -> dict:
    positional = get_positional_args(args)
    output = get_flag(args, "--output")
    if len(positional) < 2 or not output:
        return {"error": "Usage: merge <pdf1> <pdf2> [<pdf3> ...] --output merged.pdf"}
    from merge_pdfs import merge_pdfs

    return merge_pdfs(positional, output)


def _cmd_split(args: list[str]) -> dict:
    positional = get_positional_args(args)
    if not positional:
        return {
            "error": "Usage: split <pdf_path> [--pages 2-5 --output extracted.pdf] [--output-dir /path]"
        }
    pages = get_flag(args, "--pages")
    output = get_flag(args, "--output")
    output_dir = get_flag(args, "--output-dir")
    from merge_pdfs import split_pdf

    return split_pdf(positional[0], output_dir, pages, output)


def _cmd_rotate(args: list[str]) -> dict:
    positional = get_positional_args(args)
    degrees_str = get_flag(args, "--degrees")
    output = get_flag(args, "--output")
    if not positional or not degrees_str or not output:
        return {
            "error": "Usage: rotate <pdf_path> --degrees 90 --output rotated.pdf [--pages 1,3]"
        }
    try:
        degrees = int(degrees_str)
    except ValueError:
        return {
            "error": f"--degrees must be an integer (90, 180, 270), got: {degrees_str}"
        }
    pages = get_flag(args, "--pages")
    from merge_pdfs import rotate_pdf

    return rotate_pdf(positional[0], degrees, output, pages)


def _cmd_create_pdf(args: list[str]) -> dict:
    text = get_flag(args, "--text")
    file_str = get_flag(args, "--file")
    output = get_flag(args, "--output")
    if not output:
        return {
            "error": "Usage: create-pdf (--text 'content' | --file input.txt) --output doc.pdf"
        }
    if not text and not file_str:
        return {"error": "Provide --text 'content' or --file path to input file"}

    if file_str:
        path = resolve_path(file_str)
        if not path.exists():
            return {"error": f"File not found: {path}"}
        try:
            text = path.read_text(errors="replace")
        except Exception as exc:
            return {"error": f"Could not read file: {exc}"}

    from create_pdf import create_pdf_from_text

    return create_pdf_from_text(text, output)


def _cmd_read_docx(args: list[str]) -> dict:
    positional = get_positional_args(args)
    if not positional:
        return {"error": "Usage: read-docx <docx_path>"}
    from read_docx import read_docx

    return read_docx(positional[0])


def _cmd_write_docx(args: list[str]) -> dict:
    text = get_flag(args, "--text")
    file_str = get_flag(args, "--file")
    output = get_flag(args, "--output")
    if not output:
        return {
            "error": "Usage: write-docx (--text 'content' | --file input.txt) --output document.docx"
        }
    if not text and not file_str:
        return {"error": "Provide --text 'content' or --file path to input file"}

    if file_str:
        path = resolve_path(file_str)
        if not path.exists():
            return {"error": f"File not found: {path}"}
        try:
            text = path.read_text(errors="replace")
        except Exception as exc:
            return {"error": f"Could not read file: {exc}"}

    from read_docx import write_docx

    return write_docx(text, output)


def _cmd_ocr(args: list[str]) -> dict:
    positional = get_positional_args(args)
    if not positional:
        return {"error": "Usage: ocr <pdf_path> [--pages 1-3] [--lang eng]"}
    pages = get_flag(args, "--pages")
    lang = get_flag(args, "--lang") or OCR_DEFAULT_LANG
    from ocr_pdf import ocr_pdf

    return ocr_pdf(positional[0], pages, lang)


def _cmd_tts(args: list[str]) -> dict:
    text = get_flag(args, "--text")
    file_str = get_flag(args, "--file")
    output = get_flag(args, "--output")
    voice = get_flag(args, "--voice") or TTS_DEFAULT_VOICE
    rate = get_flag(args, "--rate") or "+0%"
    volume = get_flag(args, "--volume") or "+0%"
    if not output:
        return {
            "error": "Usage: tts (--text 'content' | --file path) --output speech.mp3 [--voice en-US-AriaNeural]"
        }
    from tts_audio import tts_to_mp3

    return tts_to_mp3(text, file_str, output, voice, rate, volume)


def _cmd_convert(args: list[str]) -> dict:
    positional = get_positional_args(args)
    output = get_flag(args, "--output")
    if not positional or not output:
        return {"error": "Usage: convert <input_path> --output <output_path>"}
    from convert_document import convert_document

    return convert_document(positional[0], output)


# ---------------------------------------------------------------------------
# Output formatting
# ---------------------------------------------------------------------------


def format_output(data: dict) -> str:
    """Render a result dict as plain-text output."""
    if "error" in data:
        return f"Error: {data['error']}"

    # Doctor
    if "python" in data and "system" in data:
        return _fmt_doctor(data)

    # PDF info
    if "pages" in data and "file" in data and "encrypted" in data:
        return _fmt_info(data)

    # Extract text
    if "extracted_pages" in data:
        return _fmt_extracted_text(data)

    # Extract tables
    if "tables" in data:
        return _fmt_tables(data)

    # Extract images
    if "images_extracted" in data:
        return _fmt_images(data)

    # Merge
    if "inputs" in data and "total_pages" in data:
        return _fmt_merge(data)

    # Split (individual pages)
    if "files" in data and "output_dir" in data:
        return _fmt_split_dir(data)

    # Split (range)
    if "pages_extracted" in data:
        return _fmt_split_range(data)

    # Rotate
    if "pages_rotated" in data:
        return _fmt_rotate(data)

    # Create PDF
    if "pages" in data and "chars" in data and "output" in data:
        return _fmt_create(data)

    # Read DOCX
    if "paragraphs" in data and "text" in data:
        return _fmt_read_docx(data)

    # Write DOCX / convert / tts (simple success messages)
    if "output" in data and "paragraphs" in data:
        return _fmt_write_docx(data)

    # OCR
    if "ocr_pages" in data:
        return _fmt_ocr(data)

    # TTS
    if "voice" in data and "output" in data:
        return _fmt_tts(data)

    # Convert
    if "converter" in data:
        return _fmt_convert(data)

    # Fallback — dump key: value
    return "\n".join(f"{k}: {v}" for k, v in data.items())


# ---------------------------------------------------------------------------
# Formatters
# ---------------------------------------------------------------------------


def _fmt_doctor(data: dict) -> str:
    lines = ["PDF Toolkit — System Check", ""]
    lines.append("Python packages (managed by uv):")
    for pkg in data["python"]:
        status = (
            "ok" if pkg["available"] else "not available (uv will install on first run)"
        )
        lines.append(f"  {pkg['package']:<20} {status}")

    lines.append("")
    lines.append("System tools (optional):")
    col_w = max(len(t["label"]) for t in data["system"]) + 2
    for tool in data["system"]:
        status = "available" if tool["available"] else "NOT FOUND"
        path_str = f"  ({tool['path']})" if tool["available"] else ""
        lines.append(f"  {tool['label']:<{col_w}} {status}{path_str}")
        if not tool["available"]:
            lines.append(f"    Purpose:  {tool['purpose']}")
            lines.append(f"    Install:  {tool['install']}")

    return "\n".join(lines)


def _fmt_info(data: dict) -> str:
    lines = [
        f"File:        {data['file']}",
        f"Pages:       {data['pages']}",
        f"Size:        {data['file_size_kb']} KB",
        f"Encrypted:   {'Yes' if data['encrypted'] else 'No'}",
    ]
    for key, label in [
        ("title", "Title"),
        ("author", "Author"),
        ("subject", "Subject"),
        ("creator", "Creator"),
        ("producer", "Producer"),
        ("creation_date", "Created"),
        ("mod_date", "Modified"),
    ]:
        if data.get(key):
            lines.append(f"{label + ':':<13}{data[key]}")
    return "\n".join(lines)


def _fmt_extracted_text(data: dict) -> str:
    parts = [f"File: {data['file']}  ({data['total_pages']} pages total)", ""]
    for page_num, text in data["extracted_pages"]:
        parts.append(f"--- Page {page_num} ---")
        parts.append(text.strip() if text.strip() else "[no text on this page]")
        parts.append("")
    return "\n".join(parts).rstrip()


def _fmt_tables(data: dict) -> str:
    if not data["tables"]:
        return f"File: {data['file']}\n\nNo tables found."
    parts = [f"File: {data['file']}  ({data['total_pages']} pages total)", ""]
    for i, tbl in enumerate(data["tables"], 1):
        parts.append(f"--- Table {i} (page {tbl['page']}) ---")
        rows = tbl["rows"] or []
        for row in rows:
            cells = [str(c or "").replace("\n", " ") for c in row]
            parts.append(TABLE_CELL_SEP.join(cells))
        parts.append("")
    return "\n".join(parts).rstrip()


def _fmt_images(data: dict) -> str:
    lines = [
        f"File:              {data['file']}",
        f"Images extracted:  {data['images_extracted']}",
        f"Output directory:  {data['output_dir']}",
    ]
    if data["files"]:
        lines.append("")
        lines.append("Files:")
        for f in data["files"]:
            lines.append(f"  {f}")
    return "\n".join(lines)


def _fmt_merge(data: dict) -> str:
    lines = [
        "Merged successfully.",
        f"Output:       {data['output']}",
        f"Total pages:  {data['total_pages']}",
        "",
        "Input files:",
    ]
    for f in data["inputs"]:
        lines.append(f"  {f}")
    return "\n".join(lines)


def _fmt_split_dir(data: dict) -> str:
    lines = [
        f"Split successfully.",
        f"Source:       {data['file']}",
        f"Total pages:  {data.get('total_pages', len(data['files']))}",
        f"Output dir:   {data['output_dir']}",
        f"Files:        {len(data['files'])}",
    ]
    return "\n".join(lines)


def _fmt_split_range(data: dict) -> str:
    pages = ", ".join(str(p) for p in data["pages_extracted"])
    return (
        f"Extracted successfully.\n"
        f"Source:   {data['file']}\n"
        f"Pages:    {pages}\n"
        f"Output:   {data['output']}"
    )


def _fmt_rotate(data: dict) -> str:
    pages = ", ".join(str(p) for p in data["pages_rotated"])
    return (
        f"Rotated successfully.\n"
        f"Source:        {data['file']}\n"
        f"Degrees:       {data['degrees']}\n"
        f"Pages rotated: {pages}\n"
        f"Output:        {data['output']}"
    )


def _fmt_create(data: dict) -> str:
    return (
        f"PDF created successfully.\n"
        f"Output:  {data['output']}\n"
        f"Pages:   {data['pages']}\n"
        f"Chars:   {data['chars']:,}"
    )


def _fmt_read_docx(data: dict) -> str:
    meta_lines = [f"File: {data['file']}"]
    for key, label in [
        ("title", "Title"),
        ("author", "Author"),
        ("created", "Created"),
        ("modified", "Modified"),
    ]:
        if data.get(key):
            meta_lines.append(f"{label + ':':<10}{data[key]}")
    meta_lines.append(f"{'Paragraphs:':<10}{data['paragraphs']}")
    meta_lines.append("")
    meta_lines.append(data["text"])
    return "\n".join(meta_lines)


def _fmt_write_docx(data: dict) -> str:
    return (
        f"DOCX written successfully.\n"
        f"Output:     {data['output']}\n"
        f"Paragraphs: {data['paragraphs']}\n"
        f"Chars:      {data['chars']:,}"
    )


def _fmt_ocr(data: dict) -> str:
    parts = [
        f"File: {data['file']}",
        f"Language: {data['lang']}  |  Pages OCR'd: {len(data['ocr_pages'])} of {data['total_pages']}",
        "",
    ]
    for page_num, text in data["ocr_pages"]:
        parts.append(f"--- Page {page_num} ---")
        parts.append(text.strip() if text.strip() else "[no text detected]")
        parts.append("")
    return "\n".join(parts).rstrip()


def _fmt_tts(data: dict) -> str:
    return (
        f"Audio created successfully.\n"
        f"Output:    {data['output']}\n"
        f"Voice:     {data['voice']}\n"
        f"Chars:     {data['chars']:,}\n"
        f"File size: {data['file_size_kb']} KB"
    )


def _fmt_convert(data: dict) -> str:
    return (
        f"Converted successfully.\n"
        f"Input:     {data['input']}\n"
        f"Output:    {data['output']}\n"
        f"Converter: {data['converter']}"
    )
