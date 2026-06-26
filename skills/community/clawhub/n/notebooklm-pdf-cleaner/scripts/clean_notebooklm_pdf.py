#!/usr/bin/env python3
import argparse
import io
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject
from reportlab.lib.colors import white
from reportlab.pdfgen import canvas

DEFAULT_BASE_W = 1376.0
DEFAULT_BASE_H = 768.0
DEFAULT_MASK = {
    'x': 1208.0,
    'y': 0.0,
    'w': 168.0,
    'h': 32.0,
}


def make_overlay(page_w: float, page_h: float, x: float, y: float, w: float, h: float):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=(page_w, page_h))
    c.setFillColor(white)
    c.setStrokeColor(white)
    c.rect(x, y, w, h, fill=1, stroke=0)
    c.showPage()
    c.save()
    buf.seek(0)
    return PdfReader(buf).pages[0]


def strip_annots(page):
    if NameObject('/Annots') in page:
        del page[NameObject('/Annots')]


def inspect_pdf(reader: PdfReader):
    print(f'pages={len(reader.pages)}')
    try:
        print(f'outline_len={len(reader.outline)}')
    except Exception as e:
        print(f'outline_err={e}')
    print(f'metadata={reader.metadata}')
    total_annots = 0
    for page in reader.pages:
        annots = page.get('/Annots')
        if annots:
            total_annots += len(annots)
    print(f'total_annots={total_annots}')


def clean_pdf(
    input_path: Path,
    output_path: Path,
    mask_x: float,
    mask_y: float,
    mask_w: float,
    mask_h: float,
    strip_metadata: bool = False,
    strip_annots_flag: bool = False,
    inspect: bool = False,
):
    reader = PdfReader(str(input_path))

    if inspect:
        inspect_pdf(reader)
        return

    writer = PdfWriter()

    for page in reader.pages:
        page_w = float(page.mediabox.width)
        page_h = float(page.mediabox.height)

        sx = page_w / DEFAULT_BASE_W
        sy = page_h / DEFAULT_BASE_H
        x = mask_x * sx
        y = mask_y * sy
        w = mask_w * sx
        h = mask_h * sy

        overlay = make_overlay(page_w, page_h, x, y, w, h)
        page.merge_page(overlay)
        if strip_annots_flag:
            strip_annots(page)
        writer.add_page(page)

    if strip_metadata:
        writer.add_metadata({})

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'wb') as f:
        writer.write(f)
    print(output_path)


def main():
    ap = argparse.ArgumentParser(description='Create a cleaner NotebookLM slide-deck PDF by masking the small bottom-right footer badge')
    ap.add_argument('input_pdf')
    ap.add_argument('--out', dest='out')
    ap.add_argument('--mask-x', type=float, default=DEFAULT_MASK['x'])
    ap.add_argument('--mask-y', type=float, default=DEFAULT_MASK['y'])
    ap.add_argument('--mask-w', type=float, default=DEFAULT_MASK['w'])
    ap.add_argument('--mask-h', type=float, default=DEFAULT_MASK['h'])
    ap.add_argument('--strip-metadata', action='store_true', help='Also clear document metadata')
    ap.add_argument('--strip-annots', action='store_true', help='Also remove page annotations if present')
    ap.add_argument('--force', action='store_true', help='Allow overwriting an existing output file')
    ap.add_argument('--inspect', action='store_true')
    args = ap.parse_args()

    input_path = Path(args.input_pdf).expanduser().resolve()
    if not input_path.exists():
        raise SystemExit(f'File not found: {input_path}')
    if input_path.suffix.lower() != '.pdf':
        raise SystemExit('Only .pdf input is supported')

    output_path = Path(args.out).expanduser().resolve() if args.out else input_path.with_name(f'{input_path.stem}-clean{input_path.suffix}')

    if output_path == input_path:
        raise SystemExit('Refusing to overwrite the source PDF; choose a different output path')
    if output_path.exists() and not args.force:
        raise SystemExit(f'Output already exists: {output_path} (use --force to overwrite)')

    clean_pdf(
        input_path,
        output_path,
        args.mask_x,
        args.mask_y,
        args.mask_w,
        args.mask_h,
        strip_metadata=args.strip_metadata,
        strip_annots_flag=args.strip_annots,
        inspect=args.inspect,
    )


if __name__ == '__main__':
    main()
