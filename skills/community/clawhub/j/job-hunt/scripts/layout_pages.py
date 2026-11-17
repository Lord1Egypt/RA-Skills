#!/usr/bin/env python3
"""Prepare PDF page previews and reuse only verified, previously reviewed pages.

The normal layout gate still checks the current document and requirements.
This helper never turns a changed page into a passed human review.
"""
from __future__ import annotations

import argparse
import copy
import datetime
import hashlib
import json
import pathlib
import re
import shutil

import journal
import yaml

DPI = 144


def _digest(value):
    return hashlib.sha256(value).hexdigest()


def _paths(report):
    prefix = 'report-' if report else ''
    return prefix + 'layout-review.yaml', prefix + 'layout-requirements.yaml', ('report.pdf' if report else 'cv.pdf')


def _local(ws, raw):
    path = (ws / raw).resolve()
    if not path.is_relative_to(ws.resolve()):
        raise ValueError('layout cache input must stay inside the workspace')
    return path


def _canonical(value):
    if isinstance(value, dict):
        return {key: _canonical(item) for key, item in value.items() if key not in ('xref', 'id')}
    if isinstance(value, (list, tuple)) or type(value).__name__ in ('Rect', 'Point'):
        return [_canonical(item) for item in value]
    return value


def _page(page):
    import pymupdf
    pix = page.get_pixmap(dpi=DPI, colorspace=pymupdf.csRGB, alpha=False)
    fonts = sorted([font[1], font[2], re.sub(r'^[A-Z]{6}\+', '', font[3]), font[5]]
                   for font in page.get_fonts())
    details = {'pixels': _digest(pix.samples), 'size': list(page.rect),
               'rotation': page.rotation, 'text': page.get_text(), 'fonts': fonts,
               'links': sorted((_canonical(link) for link in page.get_links()),
                               key=lambda link: json.dumps(link, sort_keys=True))}
    # Form/annotation state needs its usual inspection; do not guess equivalence.
    reusable = page.first_annot is None and page.first_widget is None
    return pix, _digest(json.dumps(details, sort_keys=True, ensure_ascii=False).encode()), reusable


def _preview(previews, number, what):
    """The one preview recorded for a page; a missing or doubled page is a ValueError.

    A bare generator lookup raised StopIteration, which no caller catches:
    check_layout wrote its pass receipt and then died with a traceback.
    """
    found = [item for item in previews if isinstance(item, dict) and item.get('page') == number]
    if len(found) != 1:
        raise ValueError(f'{what} records {len(found)} previews for page {number}, expected exactly one')
    return found[0]


def _same_pixels(image, pix):
    import pymupdf
    old = pymupdf.Pixmap(image)
    return (old.width, old.height, old.n, old.samples) == (pix.width, pix.height, pix.n, pix.samples)


def _context(ws, review, report):
    _, requirements, _ = _paths(report)
    reference = review.get('reference')
    if reference is not None:
        if not isinstance(reference, dict) or not isinstance(reference.get('path'), str):
            raise ValueError('reference is not a bound template')
        path = pathlib.Path(reference['path'])
        path = path if path.is_absolute() else ws / path
        if journal.sha256_file(path) != reference.get('sha256'):
            raise ValueError('reference changed')
    return {'requirements': journal.sha256_file(ws / requirements),
            'reference': reference, 'user_overrides': review.get('user_overrides')}


def remember(ws, report, receipt):
    """Archive a real passed gate and its exact reviewed previews, when supported."""
    import pymupdf
    ws = pathlib.Path(ws).resolve()
    review_name, _, pdf_name = _paths(report)
    review = journal.load_yaml(ws / review_name, dict)
    if not journal.receipt_intact(receipt) or receipt.get('verdict') != 'pass':
        raise ValueError('a passed intact layout receipt is required')
    for raw, expected in receipt['input_hashes'].items():
        if journal.sha256_file(ws / raw) != expected:
            raise ValueError('layout inputs changed during archival')
    directory = ws / 'raw/layout-history' / receipt['receipt_hash']
    artifacts = review.get('artifacts', {})
    stored, copies = {}, []
    with pymupdf.open(ws / pdf_name) as doc:
        for name in ((pdf_name,) if report else ('cv.pdf', 'cv.docx')):
            if name not in artifacts:
                continue
            previews = artifacts[name]['previews']
            if not isinstance(previews, list) or len(previews) != len(doc):
                raise ValueError(f'{name} review covers {len(previews) if isinstance(previews, list) else 0} '
                                 f'pages but {pdf_name} has {len(doc)}')
            pages = []
            for number, page in enumerate(doc, 1):
                pix, signature, supported = _page(page)
                preview = _preview(previews, number, name)
                source = _local(ws, preview['path'])
                if not _same_pixels(source, pix):
                    raise ValueError('reviewed previews are not the canonical 144-dpi RGB PDF render; use layout_pages.py before the next visual review')
                target = directory / f'{name}-page-{number}.png'
                copies.append((source, target))
                pages.append({'page': number, 'signature': signature, 'supported': supported,
                              'preview': target.name, 'sha256': journal.sha256_file(source),
                              'original_path': source.relative_to(ws).as_posix()})
            stored[name] = pages
    directory.mkdir(parents=True, exist_ok=True)
    for source, target in copies:
        shutil.copy2(source, target)
    shutil.copy2(ws / pdf_name, directory / 'document.pdf')
    shutil.copy2(ws / review_name, directory / 'review.yaml')
    proof = {'version': 1, 'report': report, 'dpi': DPI, 'receipt': receipt,
             'context': _context(ws, review, report), 'pdf_name': pdf_name,
             'review_name': review_name, 'artifacts': stored}
    path = directory / 'proof.json'
    path.write_text(json.dumps(proof, ensure_ascii=False, indent=2) + '\n')
    index = ws / (('report-' if report else '') + 'layout-cache.json')
    index.write_text(json.dumps({'path': path.relative_to(ws).as_posix(),
                                 'sha256': journal.sha256_file(path)}) + '\n')


def _baseline(ws, raw, report, hashes):
    import pymupdf
    path = _local(ws, raw)
    proof = json.loads(path.read_text())
    if not isinstance(proof, dict) or (proof.get('review_name'), proof.get('pdf_name')) != (_paths(report)[0], _paths(report)[2]):
        raise ValueError('cache artifact names changed')
    receipt = proof['receipt']
    if not isinstance(receipt, dict):
        raise ValueError('cache receipt is not a record')
    gate = 'check_report_layout' if report else 'check_layout'
    if (proof.get('version') != 1 or proof.get('dpi') != DPI or proof.get('report') != report
            or receipt.get('gate') != gate or receipt.get('verdict') != 'pass'
            or not journal.receipt_intact(receipt)
            or receipt not in journal.read_receipts(ws, gate)):
        raise ValueError('no matching original passed layout gate')
    directory = path.parent
    review_path, pdf_path = directory / 'review.yaml', directory / 'document.pdf'
    review = journal.load_yaml(review_path, dict)
    if (journal.sha256_file(review_path) != receipt['input_hashes'].get(proof['review_name'])
            or journal.sha256_file(pdf_path) != receipt['input_hashes'].get(proof['pdf_name'])):
        raise ValueError('archived document/review differs from its original gate')
    for file in (path, review_path, pdf_path):
        hashes[file.relative_to(ws).as_posix()] = journal.sha256_file(file)
    with pymupdf.open(pdf_path) as doc:
        for name, records in proof['artifacts'].items():
            if len(records) != len(doc):
                raise ValueError('archived page coverage changed')
            for number, item in enumerate(records, 1):
                source = _local(ws, (directory / item['preview']).relative_to(ws))
                actual = journal.sha256_file(source)
                old = _preview(review['artifacts'][name]['previews'], number, 'archived review')
                pix, signature, supported = _page(doc[number - 1])
                if (item['page'] != number or old['page'] != number
                        or actual != item['sha256'] or actual != old['sha256']
                        or actual != receipt['input_hashes'].get(item['original_path'])
                        or item['signature'] != signature or item['supported'] != supported
                        or not _same_pixels(source, pix)):
                    raise ValueError('archived page is not its actually reviewed PDF render')
                hashes[source.relative_to(ws).as_posix()] = actual
    if proof['context'] != _context(ws, review, report):
        raise ValueError('review requirements or reference changed')
    return proof, review


def validate_reuse(ws, review, name, preview, report, hashes, cache=None):
    """Called by the normal gate; stale or edited reuse claims fail closed."""
    import pymupdf
    try:
        reuse = preview['reused_from']
        cache = {} if cache is None else cache
        key = (reuse['path'], report)
        if key not in cache:
            baseline_hashes = {}
            proof, _ = _baseline(ws, reuse['path'], report, baseline_hashes)
            cache[key] = proof, baseline_hashes
        proof, baseline_hashes = cache[key]
        hashes.update(baseline_hashes)
        if proof['context'] != _context(ws, review, report):
            raise ValueError('current review conditions differ')
        number = preview['page']
        if type(number) is not int or number < 1 or type(reuse['page']) is not int or reuse['page'] != number:
            raise ValueError('page position changed')
        if name == 'cv.docx':
            export = review.get('word_export', {})
            if (export.get('docx_sha256') != journal.sha256_file(ws / 'cv.docx')
                    or export.get('sha256') != journal.sha256_file(ws / 'cv.pdf')
                    or journal.sha256_file(_local(ws, export['path'])) != export['sha256']):
                raise ValueError('current Word export is not bound to the DOCX/PDF')
        with pymupdf.open(ws / proof['pdf_name']) as doc:
            if len(doc) != len(proof['artifacts'][name]):
                raise ValueError('page count changed; inspect the new pagination')
            pix, signature, supported = _page(doc[number - 1])
        prior = proof['artifacts'][name][number - 1]
        if not supported or not prior['supported'] or signature != prior['signature']:
            raise ValueError('page pixels, text, fonts, links or geometry changed')
        if not _same_pixels(_local(ws, preview['path']), pix):
            raise ValueError('current preview is not the current PDF page')
    except (OSError, ValueError, KeyError, IndexError, TypeError, RuntimeError, journal.YamlUnreadable) as exc:
        return f'LAYOUT_REUSE_INVALID: {name} page {preview.get("page")}: {exc}'
    return ''


def prepare(ws, report=False, adopt=False):
    import pymupdf
    import check_layout
    ws = pathlib.Path(ws).resolve()
    review_name, requirements_name, pdf_name = _paths(report)
    requirements = journal.load_yaml(ws / requirements_name, dict)
    current = journal.load_yaml(ws / review_name, dict) if (ws / review_name).is_file() else {}
    old, proof, baseline_path = {}, None, ''
    index = ws / (('report-' if report else '') + 'layout-cache.json')
    try:
        entry = json.loads(index.read_text())
        baseline_path = entry['path']
        if journal.sha256_file(_local(ws, baseline_path)) != entry['sha256']:
            raise ValueError('cache index changed')
        proof, old = _baseline(ws, baseline_path, report, {})
        if (proof['context'] != _context(ws, current, report)
                or current.get('unresolved_differences') != []
                or any(journal.as_mapping(item).get('status') != 'pass'
                       for item in journal.as_mapping(current.get('checks')).values())):
            proof = None
    except (OSError, ValueError, KeyError, TypeError, RuntimeError, journal.YamlUnreadable):
        proof = None
    draft = copy.deepcopy(old if proof else current)
    draft.update(requirements_sha256=journal.sha256_file(ws / requirements_name),
                 reference=requirements.get('reference'), user_overrides=current.get('user_overrides', []))
    if 'word_export' in current:
        draft['word_export'] = copy.deepcopy(current['word_export'])
    if report:
        draft['source_sha256'] = journal.sha256_file(ws / 'report.md')
    draft.setdefault('reviewer', 'pending visual review')
    draft.setdefault('reviewed_at', datetime.datetime.now(datetime.timezone.utc).isoformat())
    draft['review_method'] = 'unchanged pages reuse prior visual observations; changed pages require inspection'
    names = (pdf_name,) if report else tuple(name for name in ('cv.docx', 'cv.pdf') if (ws / name).is_file())
    draft['artifacts'] = {}
    needed = set()
    reuse_cache = {}
    directory = ws / 'raw/layout-pages' / journal.sha256_file(ws / pdf_name)
    directory.mkdir(parents=True, exist_ok=True)
    with pymupdf.open(ws / pdf_name) as doc:
        page_count = len(doc)
        if not page_count:
            raise ValueError('PDF has no pages')
        for name in names:
            previews = []
            for number, page in enumerate(doc, 1):
                pix, signature, supported = _page(page)
                image = directory / f'page-{number}.png'
                pix.save(image)
                item = {'page': number, 'path': image.relative_to(ws).as_posix(),
                        'sha256': journal.sha256_file(image), 'review_status': 'pending'}
                if (proof and supported and len(doc) == len(proof['artifacts'].get(name, []))
                        and proof['artifacts'][name][number - 1]['supported']
                        and signature == proof['artifacts'][name][number - 1]['signature']):
                    item.update(review_status='reused', reused_from={'path': baseline_path, 'page': number})
                    # Word reuse also requires the existing, current export proof.
                    if name == 'cv.docx' and validate_reuse(ws, draft, name, item, report, {}, reuse_cache):
                        item.pop('reused_from')
                        item['review_status'] = 'pending'
                if item['review_status'] == 'pending':
                    needed.add(number)
                previews.append(item)
            draft['artifacts'][name] = {'sha256': journal.sha256_file(ws / name),
                                        'pages': len(doc), 'previews': previews}
    if needed:
        draft['checks'] = {key: {'status': 'pending', 'detail': 'Inspect the changed pages against current requirements.'}
                           for key in check_layout.CHECKS}
        draft['unresolved_differences'] = ['Visual review needed for pages: ' + ', '.join(map(str, sorted(needed)))]
    target = ws / (review_name if adopt and not needed else review_name.replace('.yaml', '.next.yaml'))
    target.write_text(yaml.safe_dump(draft, allow_unicode=True, sort_keys=False), encoding='utf-8')
    return {'draft': str(target), 'review_required': sorted(needed),
            'reused_pages': sorted(set(range(1, page_count + 1)) - needed),
            'adopted': bool(adopt and not needed)}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace', required=True, type=pathlib.Path)
    parser.add_argument('--report', action='store_true')
    parser.add_argument('--adopt', action='store_true', help='Use the prepared review only when every page is verified unchanged')
    args = parser.parse_args(argv)
    try:
        print(json.dumps(prepare(args.workspace, args.report, args.adopt), ensure_ascii=False))
        return 0
    except (OSError, ValueError, KeyError, TypeError, RuntimeError, journal.YamlUnreadable) as exc:
        print(f'LAYOUT_PAGES_UNAVAILABLE: {exc}')
        return 2


if __name__ == '__main__':
    from cli_io import configure_output
    configure_output()
    raise SystemExit(main())
