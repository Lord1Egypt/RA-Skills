"""Optional bounded local recognition of selected original textbook pages."""
import hashlib
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import omni_materials as materials
from omni_material_readers import ReaderError
from omni_textbook_fetch import MAX_TEXTBOOK_BYTES, source_pdf
from omni_textbooks import crop_bytes

VISION = r'''
import Foundation
import Vision
let request = VNRecognizeTextRequest()
request.recognitionLevel = .accurate
request.recognitionLanguages = ["zh-Hans", "en-US"]
let handler = VNImageRequestHandler(url: URL(fileURLWithPath: CommandLine.arguments[1]))
try handler.perform([request])
for result in request.results ?? [] {
    if let line = result.topCandidates(1).first { print(line.string) }
}
'''


def ocr(root, book_id, material_id, version, ranges):
    if (Path(root) / 'config.json').exists():
        raise ValueError('Create a new textbook archive before changing its text extraction.')
    original = source_pdf(root, book_id, version)
    item = materials.load(root, material_id, version)
    total = item.get('total_pages')
    if not total:
        raise ValueError('The PDF reader could not establish the source pages.')
    pages = set()
    for group in ranges.split(','):
        match = re.fullmatch(r'(\d+)(?:-(\d+))?', group.strip())
        if not match:
            raise ValueError('Use PDF page numbers such as 2-4,7.')
        start, end = int(match[1]), int(match[2] or match[1])
        if not 1 <= start <= end <= total or end-start >= 8:
            raise ValueError('Select up to eight actual PDF pages per OCR import.')
        pages.update(range(start, end+1))
    if len(pages) > 8:
        raise ValueError('Select up to eight actual PDF pages per OCR import.')
    prior = dict.fromkeys(set(item.get('ocr_pages', [])) - pages, '')
    for unit in item['units']:
        if unit['page'] in prior:
            prior[unit['page']] += unit['text']

    def retained_text(_pdf, page):
        return prior[page]

    tool = shutil.which('tesseract')
    if sys.platform == 'darwin' and shutil.which('swift'):
        engine = 'apple-vision'
    elif tool:
        engine = 'tesseract'
    else:
        raise ValueError('Selected pages need local OCR. Use macOS Swift/Vision or Tesseract with chi_sim and eng.')
    with tempfile.TemporaryDirectory(prefix='omni-ocr-') as scratch:
        folder = Path(scratch)
        script = folder / 'recognize.swift'
        script.write_text(VISION, encoding='utf-8')

        def recognize(pdf, page):
            png = folder / f'page-{page}.png'
            png.write_bytes(crop_bytes(pdf, page, (0, 0, 1, 1)))
            args = ['swift', str(script), str(png)] if engine == 'apple-vision' else [
                tool, str(png), 'stdout', '-l', 'chi_sim+eng']
            try:
                result = subprocess.run(args, text=True, capture_output=True, timeout=45)
            except subprocess.TimeoutExpired as error:
                raise ReaderError(f'OCR timed out on PDF page {page}.') from error
            if result.returncode:
                raise ReaderError(f'Local OCR failed on PDF page {page}; check the OCR tool and Chinese language support.')
            return result.stdout

        key = f'{material_id}:{version}:{engine}:{sorted(pages)}'
        identity = 'm_' + hashlib.sha256(key.encode()).hexdigest()[:16]
        extractors = dict.fromkeys(prior, retained_text) | dict.fromkeys(pages, recognize)
        return materials.import_file(root, original, material_id=identity, url=item.get('url'), retry=True,
                                     max_file=MAX_TEXTBOOK_BYTES, pdf_ocr=extractors,
                                     title=item['title'], publisher=item.get('publisher'))
