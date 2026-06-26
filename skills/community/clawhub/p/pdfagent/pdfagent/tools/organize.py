from __future__ import annotations

from pathlib import Path

from pypdf import PdfReader, PdfWriter

from ..core.ranges import parse_page_ranges


def remove_pages(input_path: Path, output_path: Path, remove_spec: str) -> None:
    reader = PdfReader(str(input_path))
    total = len(reader.pages)
    remove_indices = set(parse_page_ranges(remove_spec, total))

    writer = PdfWriter()
    for idx, page in enumerate(reader.pages):
        if idx not in remove_indices:
            writer.add_page(page)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("wb") as f:
        writer.write(f)


def extract_pages(
    input_path: Path,
    output_path: Path | None,
    output_dir: Path | None,
    extract_spec: str,
    single_file: bool,
) -> list[Path]:
    reader = PdfReader(str(input_path))
    total = len(reader.pages)
    indices = parse_page_ranges(extract_spec, total)

    if single_file:
        if output_path is None:
            raise ValueError("output_path is required for single_file output")
        writer = PdfWriter()
        for idx in indices:
            writer.add_page(reader.pages[idx])
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("wb") as f:
            writer.write(f)
        return [output_path]

    if output_dir is None:
        raise ValueError("output_dir is required for multi-file output")
    output_dir.mkdir(parents=True, exist_ok=True)

    outputs: list[Path] = []
    for idx in indices:
        writer = PdfWriter()
        writer.add_page(reader.pages[idx])
        out = output_dir / f"{input_path.stem}_page_{idx + 1}.pdf"
        with out.open("wb") as f:
            writer.write(f)
        outputs.append(out)
    return outputs


def reorder_pages(input_path: Path, output_path: Path, order_spec: str) -> None:
    reader = PdfReader(str(input_path))
    total = len(reader.pages)

    order = [int(p.strip()) for p in order_spec.split(",") if p.strip()]
    if len(order) != total:
        raise ValueError("Order list must include every page exactly once")
    if set(order) != set(range(1, total + 1)):
        raise ValueError("Order list must be a permutation of all pages")

    writer = PdfWriter()
    for page_num in order:
        writer.add_page(reader.pages[page_num - 1])

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("wb") as f:
        writer.write(f)


def insert_pdf(input_path: Path, insert_path: Path, output_path: Path, position: int) -> None:
    reader = PdfReader(str(input_path))
    insert_reader = PdfReader(str(insert_path))
    total = len(reader.pages)

    if position < 1 or position > total + 1:
        raise ValueError("Insert position out of bounds")

    writer = PdfWriter()
    for idx in range(total + 1):
        if idx == position - 1:
            for page in insert_reader.pages:
                writer.add_page(page)
        if idx < total:
            writer.add_page(reader.pages[idx])

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("wb") as f:
        writer.write(f)
