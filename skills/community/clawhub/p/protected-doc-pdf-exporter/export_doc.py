#!/usr/bin/env python3
"""
Universal Protected Online Document & Presentation PDF Exporter
Exports protected/restricted documents from WeChat Work Cloud Drive (微盘),
Tencent Docs (腾讯文档), Weboffice, Feishu, and web slide readers into clean PDFs.
"""

import os
import sys
import time
import shutil
import asyncio
import argparse
import websockets

from browser_manager import BrowserSession
from pdf_builder import parse_page_range, compile_images_to_pdf
from extractors import (
    WeComWebofficeExtractor,
    TencentDocsExtractor,
    FeishuExtractor,
    DOMStepperExtractor
)

EXTRACTORS = [
    WeComWebofficeExtractor,
    TencentDocsExtractor,
    FeishuExtractor,
    DOMStepperExtractor
]

def select_extractor(url: str):
    for ext_cls in EXTRACTORS:
        if ext_cls.can_handle(url):
            return ext_cls
    return DOMStepperExtractor

async def run_pipeline(args):
    url = args.url
    output_path = os.path.abspath(args.output)
    temp_images_dir = os.path.abspath(args.images_dir)
    os.makedirs(temp_images_dir, exist_ok=True)

    extractor_cls = select_extractor(url)
    print(f"[*] Target URL: {url}")
    print(f"[*] Selected Extractor Engine: {extractor_cls.__name__}")

    session = BrowserSession(
        url=url,
        user_data_dir=args.user_data_dir,
        browser_type=args.browser,
        headless=not args.no_headless,
        window_size=(1920, 1080)
    )

    try:
        ws_url = await session.start()
        print("[*] Connecting DevTools WebSocket...")

        async with websockets.connect(ws_url, max_size=35 * 1024 * 1024) as ws:
            extractor = extractor_cls(ws, ws_url)
            print("[*] Initializing document viewer & querying pages...")
            total_pages = await extractor.prepare()
            print(f"[✓] Document detected with {total_pages} total page(s).")

            page_indices = parse_page_range(args.pages, total_pages)
            print(f"[*] Exporting {len(page_indices)} selected page(s): {[p + 1 for p in page_indices]}")

            image_paths = []
            for idx in page_indices:
                print(f"    [+] Capturing page {idx + 1:02d}/{total_pages:02d}...", end='', flush=True)
                start_p = time.time()
                try:
                    img_p = await extractor.extract_page(idx, temp_images_dir)
                    if img_p and os.path.exists(img_p):
                        image_paths.append(img_p)
                        size_kb = os.path.getsize(img_p) // 1024
                        elapsed = time.time() - start_p
                        print(f" OK ({size_kb} KB, {elapsed:.1f}s)")
                    else:
                        print(" FAILED (empty)")
                except Exception as e:
                    print(f" ERROR ({e})")

            if not image_paths:
                raise RuntimeError("No pages were successfully extracted.")

            print(f"[✓] Successfully captured {len(image_paths)} pages.")

            # Formats
            fmt = args.format.lower()
            if fmt in ['pdf', 'both']:
                # Ensure output has .pdf extension if it's a file
                pdf_target = output_path
                if not pdf_target.lower().endswith('.pdf'):
                    pdf_target = os.path.join(output_path, "exported_document.pdf")

                print(f"[*] Compiling PDF: {pdf_target}...")
                compile_images_to_pdf(image_paths, pdf_target, quality=args.quality)
                pdf_kb = os.path.getsize(pdf_target) // 1024
                print(f"[✓] PDF generated successfully: {pdf_target} ({pdf_kb} KB, {len(image_paths)} pages)")

            if fmt in ['images', 'both']:
                out_img_dir = output_path if not output_path.lower().endswith('.pdf') else os.path.splitext(output_path)[0] + "_images"
                os.makedirs(out_img_dir, exist_ok=True)
                for p in image_paths:
                    shutil.copy2(p, os.path.join(out_img_dir, os.path.basename(p)))
                print(f"[✓] Image cutouts saved to: {out_img_dir}")

    finally:
        print("[*] Cleaning up browser process & temporary sessions...")
        await session.close()
        if not args.keep_images and args.format != 'images':
            try:
                shutil.rmtree(temp_images_dir)
            except Exception:
                pass

def main():
    parser = argparse.ArgumentParser(
        description="Universal Protected Online Document & Presentation PDF Exporter",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Export WeCom Drive presentation to PDF:
  python3 export_doc.py --url "https://drive.weixin.qq.com/s?k=..." -o ~/Downloads/doc.pdf

  # Export pages 1-10 with visible browser window:
  python3 export_doc.py --url "https://docs.qq.com/..." -o ~/Desktop/report.pdf --pages 1-10 --no-headless

  # Export both PDF and individual high-res PNG images:
  python3 export_doc.py --url "https://..." -o ~/Downloads/presentation.pdf --format both
        """
    )
    parser.add_argument('--url', required=True, help="URL of the protected document, presentation, or reader page.")
    parser.add_argument('--output', '-o', required=True, help="Destination PDF file path or output directory.")
    parser.add_argument('--pages', default='all', help="Page range to export, e.g. 'all', '1-5', '1,3,5-10' (default: all).")
    parser.add_argument('--format', choices=['pdf', 'images', 'both'], default='pdf', help="Export format (default: pdf).")
    parser.add_argument('--browser', choices=['chrome', 'edge', 'chromium', 'brave'], default='chrome', help="Browser to emulate profile from (default: chrome).")
    parser.add_argument('--user-data-dir', help="Custom browser profile directory.")
    parser.add_argument('--quality', type=int, default=95, help="Image quality for PDF assembly (default: 95).")
    parser.add_argument('--no-headless', action='store_true', help="Run in visible (headful) window mode for manual login or inspection.")
    parser.add_argument('--keep-images', action='store_true', help="Keep temporary image cutouts.")
    parser.add_argument('--images-dir', default='/tmp/universal_doc_slides', help="Directory for temporary image cutouts.")

    args = parser.parse_args()
    asyncio.run(run_pipeline(args))

if __name__ == '__main__':
    main()
