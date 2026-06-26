from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Iterable, List, Optional, Sequence, Tuple

from pypdf import PdfReader, PdfWriter, Transformation
from pypdf._page import PageObject


DEFAULT_INPUT_DIR = Path("data/input")
DEFAULT_OUTPUT_FILE = Path("data/output/booklet_print.pdf")
DEFAULT_MERGED_FILE = Path("data/output/merged_source.pdf")


def natural_sort_key(path: Path) -> List[object]:
    parts = re.split(r"(\d+)", path.name)
    return [int(part) if part.isdigit() else part.lower() for part in parts]


def collect_pdf_files(input_dir: Path) -> List[Path]:
    if not input_dir.exists():
        raise FileNotFoundError(f"Input directory not found: {input_dir}")

    pdf_files = sorted(
        [path for path in input_dir.iterdir() if path.is_file() and path.suffix.lower() == ".pdf"],
        key=natural_sort_key,
    )
    if not pdf_files:
        raise ValueError(f"No PDF files found in: {input_dir}")
    return pdf_files


def load_pages(pdf_files: Sequence[Path]) -> List[PageObject]:
    pages: List[PageObject] = []
    for pdf_file in pdf_files:
        reader = PdfReader(str(pdf_file))
        pages.extend(reader.pages)

    if not pages:
        raise ValueError("The selected PDF files do not contain any pages.")
    return pages


def page_size(pages: Sequence[PageObject]) -> Tuple[float, float]:
    max_width = max(float(page.mediabox.width) for page in pages)
    max_height = max(float(page.mediabox.height) for page in pages)
    return max_width, max_height


def pad_to_booklet_multiple(pages: Sequence[PageObject]) -> List[Optional[PageObject]]:
    padded: List[Optional[PageObject]] = list(pages)
    while len(padded) % 4 != 0:
        padded.append(None)
    return padded


def booklet_pairs(pages: Sequence[Optional[PageObject]]) -> Iterable[Tuple[Optional[PageObject], Optional[PageObject]]]:
    total = len(pages)
    for sheet_index in range(total // 4):
        front_left = pages[total - 1 - (sheet_index * 2)]
        front_right = pages[sheet_index * 2]
        back_left = pages[(sheet_index * 2) + 1]
        back_right = pages[total - 2 - (sheet_index * 2)]

        yield front_left, front_right
        yield back_left, back_right


def place_page(
    sheet: PageObject,
    source_page: PageObject,
    slot_x: float,
    slot_y: float,
    slot_width: float,
    slot_height: float,
) -> None:
    source_width = float(source_page.mediabox.width)
    source_height = float(source_page.mediabox.height)
    scale = min(slot_width / source_width, slot_height / source_height)

    scaled_width = source_width * scale
    scaled_height = source_height * scale
    translate_x = slot_x + (slot_width - scaled_width) / 2
    translate_y = slot_y + (slot_height - scaled_height) / 2

    transformation = Transformation().scale(scale).translate(translate_x, translate_y)
    sheet.merge_transformed_page(source_page, transformation)


def create_booklet_writer(pages: Sequence[PageObject], title: str) -> PdfWriter:
    padded_pages = pad_to_booklet_multiple(pages)
    source_width, source_height = page_size(pages)
    sheet_width = source_width * 2
    sheet_height = source_height

    outer_margin = 18
    inner_gap = 12
    slot_width = (sheet_width - (outer_margin * 2) - inner_gap) / 2
    slot_height = sheet_height - (outer_margin * 2)

    writer = PdfWriter()
    for left_page, right_page in booklet_pairs(padded_pages):
        sheet = PageObject.create_blank_page(width=sheet_width, height=sheet_height)

        if left_page is not None:
            place_page(
                sheet,
                left_page,
                slot_x=outer_margin,
                slot_y=outer_margin,
                slot_width=slot_width,
                slot_height=slot_height,
            )

        if right_page is not None:
            place_page(
                sheet,
                right_page,
                slot_x=outer_margin + slot_width + inner_gap,
                slot_y=outer_margin,
                slot_width=slot_width,
                slot_height=slot_height,
            )

        writer.add_page(sheet)

    writer.add_metadata({"/Title": title})
    return writer


def create_merged_writer(pages: Sequence[PageObject], title: str) -> PdfWriter:
    writer = PdfWriter()
    for page in pages:
        writer.add_page(page)
    writer.add_metadata({"/Title": title})
    return writer


def write_pdf(writer: PdfWriter, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("wb") as file_obj:
        writer.write(file_obj)


def build_booklet_pdf(input_dir: Path, output_file: Path, merged_output_file: Optional[Path]) -> Tuple[int, int]:
    pdf_files = collect_pdf_files(input_dir)
    pages = load_pages(pdf_files)

    booklet_writer = create_booklet_writer(pages, title="Booklet Print Version")
    write_pdf(booklet_writer, output_file)

    if merged_output_file is not None:
        merged_writer = create_merged_writer(pages, title="Merged Source PDF")
        write_pdf(merged_writer, merged_output_file)

    return len(pdf_files), len(pages)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Merge PDFs and generate a 2-up booklet file for duplex printing.",
    )
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=DEFAULT_INPUT_DIR,
        help="Directory containing the source PDF files. Default: data/input",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_FILE,
        help="Path of the generated booklet PDF. Default: data/output/booklet_print.pdf",
    )
    parser.add_argument(
        "--merged-output",
        type=Path,
        default=DEFAULT_MERGED_FILE,
        help="Path of the sequentially merged PDF. Use --no-merged-output to skip it.",
    )
    parser.add_argument(
        "--no-merged-output",
        action="store_true",
        help="Skip writing the sequential merged PDF.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    merged_output = None if args.no_merged_output else args.merged_output

    try:
        file_count, page_count = build_booklet_pdf(
            input_dir=args.input_dir,
            output_file=args.output,
            merged_output_file=merged_output,
        )
    except (FileNotFoundError, ValueError) as exc:
        print(exc)
        return 1

    print(f"Merged {file_count} PDF files with {page_count} pages.")
    print(f"Booklet output: {args.output}")
    if merged_output is not None:
        print(f"Merged source output: {merged_output}")
    print("Print with landscape mode, duplex, and flip on short edge.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())