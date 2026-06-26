#!/usr/bin/env python3
import argparse
from typing import List, Any
from pathlib import Path

from PIL import Image as PILImage, ImageFile
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Image as ReportLabImage, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors as reportlab_colors

ImageFile.LOAD_TRUNCATED_IMAGES = True


def slice_and_generate_pdf(
    source_image_path: str,
    output_dir: str,
    output_pdf_name: str,
    slice_height: int,
    overlap: int,
    images_per_row: int,
    images_per_col: int,
    layout: str,
    cleanup: bool
):
    source_path = Path(source_image_path).expanduser().resolve()
    output_path = Path(output_dir).expanduser().resolve()

    if not source_path.is_file():
        print(f"Error: Source image not found -> {source_path}")
        return

    output_path.mkdir(parents=True, exist_ok=True)
    sliced_image_paths: List[str] = []

    # ================= 1. Slicing Image =================
    print(f"Opening image: {source_path.name}")
    try:
        img = PILImage.open(source_path)
        img_width, img_height = img.size
        img_format = img.format or 'PNG'

        if slice_height <= overlap:
            print("Error: slice_height must be greater than overlap.")
            return

        start_y = 0
        slice_index = 0
        effective_step = max(1, slice_height - overlap)

        print(f"Image dimensions: {img_width}x{img_height}. Slicing...")
        while start_y < img_height:
            end_y = min(start_y + slice_height, img_height)

            # Skip very small trailing slices if they are mostly overlap
            current_slice_actual_height = end_y - start_y
            if start_y > 0 and current_slice_actual_height < (overlap * 0.5):
                print(f"  Skipping small trailing slice {slice_index + 1}")
                break

            box = (0, start_y, img_width, end_y)
            slice_img = img.crop(box)

            output_suffix = source_path.suffix.lower() if source_path.suffix else '.png'
            save_format = 'PNG' if output_suffix not in [
                '.jpg', '.jpeg', '.png', '.webp'] else img_format
            save_suffix = '.png' if save_format == 'PNG' else output_suffix

            slice_filename = f"slice_{slice_index:04d}{save_suffix}"
            slice_output_path_obj = output_path / slice_filename

            slice_img.save(slice_output_path_obj, format=save_format)
            slice_img.close()

            sliced_image_paths.append(str(slice_output_path_obj))
            slice_index += 1
            start_y += effective_step

        img.close()
        print(f"Successfully generated {len(sliced_image_paths)} slices.")
    except Exception as e:
        print(f"Error during slicing: {e}")
        return

    if not sliced_image_paths:
        print("Error: No slices were generated.")
        return

    # ================= 2. Generating PDF =================
    pdf_path = output_path / output_pdf_name
    print(f"Generating PDF: {pdf_path}")
    try:
        doc = SimpleDocTemplate(str(pdf_path), pagesize=A4,
                                topMargin=10*mm, bottomMargin=10*mm,
                                leftMargin=10*mm, rightMargin=10*mm)
        story: List[Any] = []

        content_width, content_height = doc.width, doc.height
        safety_factor = 0.98
        adjusted_content_height = content_height * safety_factor
        cell_padding = 1.0 * mm

        cell_total_height = adjusted_content_height / images_per_col
        cell_total_width = content_width / images_per_row

        img_container_width = max(1*mm, cell_total_width - 2 * cell_padding)
        img_container_height = max(1*mm, cell_total_height - 2 * cell_padding)

        images_per_page = images_per_row * images_per_col
        total_images = len(sliced_image_paths)
        num_pages = (total_images + images_per_page - 1) // images_per_page

        img_style = TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.25, reportlab_colors.lightgrey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('LEFTPADDING', (0, 0), (-1, -1), cell_padding),
            ('RIGHTPADDING', (0, 0), (-1, -1), cell_padding),
            ('TOPPADDING', (0, 0), (-1, -1), cell_padding),
            ('BOTTOMPADDING', (0, 0), (-1, -1), cell_padding)
        ])

        col_widths = [cell_total_width] * images_per_row
        row_heights = [cell_total_height] * images_per_col

        def create_rl_image(img_path: str) -> Any:
            try:
                with PILImage.open(img_path) as pil_img:
                    original_w, original_h = pil_img.size
                    ratio = min(img_container_width / original_w,
                                img_container_height / original_h)
                    display_w = original_w * ratio
                    display_h = original_h * ratio
                return ReportLabImage(img_path, width=display_w, height=display_h)
            except Exception as e:
                print(f"Failed to create image object for {img_path}: {e}")
                return None

        for page_num in range(num_pages):
            start_idx = page_num * images_per_page
            end_idx = min(start_idx + images_per_page, total_images)
            page_image_paths = sliced_image_paths[start_idx:end_idx]

            page_table_data: List[List[Any]] = [
                [Spacer(1, 1) for _ in range(images_per_row)] for _ in range(images_per_col)]
            img_idx = 0

            if layout == 'column':
                for c in range(images_per_row):
                    for r in range(images_per_col):
                        if img_idx < len(page_image_paths):
                            rl_img = create_rl_image(page_image_paths[img_idx])
                            if rl_img:
                                page_table_data[r][c] = rl_img
                            img_idx += 1
            else:
                for r in range(images_per_col):
                    for c in range(images_per_row):
                        if img_idx < len(page_image_paths):
                            rl_img = create_rl_image(page_image_paths[img_idx])
                            if rl_img:
                                page_table_data[r][c] = rl_img
                            img_idx += 1

            table = Table(page_table_data, colWidths=col_widths,
                          rowHeights=row_heights)
            table.setStyle(img_style)
            story.append(table)

            if page_num < num_pages - 1:
                story.append(PageBreak())

        doc.build(story)  

        deleted_count = 0
        if cleanup:
            for img_p in sliced_image_paths:
                try:
                    Path(img_p).unlink(missing_ok=True)
                    deleted_count += 1
                except Exception as e:
                    print(
                        f"Warning: Failed to delete intermediate file {img_p}: {e}")

        print("\n--- TASK COMPLETION SUMMARY ---")
        print("STATUS: Success")
        print(f"TOTAL_SLICES: {total_images}")
        print(
            f"CLEANUP_PERFORMED: {'Yes (' + str(deleted_count) + ' files deleted)' if cleanup else 'No'}")
        print(f"FINAL_PDF_PATH: {pdf_path.resolve()}")
        print("-------------------------------")

    except Exception as e:
        print("\n--- TASK FAILED ---")
        print(f"ERROR: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Slice a long image and convert to PDF.")
    parser.add_argument("--source", type=str, required=True,
                        help="Path to the source long image.")
    parser.add_argument("--out-dir", type=str, required=True,
                        help="Directory to save slices and PDF.")
    parser.add_argument("--pdf-name", type=str,
                        default="output.pdf", help="Name of the output PDF file.")
    parser.add_argument("--slice-height", type=int,
                        default=2000, help="Height of each slice in pixels.")
    parser.add_argument("--overlap", type=int, default=200,
                        help="Overlap height in pixels.")

    parser.add_argument("--cols", type=int, default=2,
                        help="Images per row (columns) in PDF.")
    parser.add_argument("--rows", type=int, default=2,
                        help="Images per column (rows) in PDF.")
    parser.add_argument(
        "--layout", type=str, choices=['grid', 'column'], default='grid', help="Layout mode.")
    parser.add_argument("--cleanup", action="store_true",
                        help="Delete intermediate slice images after PDF is generated.")

    args = parser.parse_args()

    slice_and_generate_pdf(
        source_image_path=args.source,
        output_dir=args.out_dir,
        output_pdf_name=args.pdf_name,
        slice_height=args.slice_height,
        overlap=args.overlap,
        images_per_row=args.cols,
        images_per_col=args.rows,
        layout=args.layout,
        cleanup=args.cleanup
    )
