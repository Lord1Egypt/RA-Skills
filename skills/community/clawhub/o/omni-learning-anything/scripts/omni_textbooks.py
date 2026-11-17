"""Bound textbook scopes, precise source retrieval and original figure crops."""
import hashlib
import io
import re
import unicodedata
from pathlib import Path

import omni_core as core
import omni_materials as materials
from omni_textbook_fetch import source_pdf


def require(condition, message):
    if not condition:
        raise ValueError(message)


def compact(text):
    value = unicodedata.normalize('NFKC', text).casefold()
    return re.sub(r'\s+', '', value).translate(str.maketrans({'−': '-', '–': '-', '·': '×'}))


def locate(root, material_id, version, query):
    """Find actual phrase/formula occurrences. The agent checks candidates visually."""
    require(isinstance(query, str) and 0 < len(query.strip()) <= 160, 'Provide a short chapter, concept or formula.')
    needle = compact(query)
    item = materials.load(root, material_id, version)
    units = item['units']
    if (Path(root) / 'config.json').is_file():
        allowed = {unit for selection in materials.scoped(root)
                   if selection['id'] == material_id and selection['version'] == version
                   for unit in selection['units']}
        require(bool(allowed), 'This textbook is outside the approved scope.')
        units = [unit for unit in units if unit['id'] in allowed]
    hits = {}
    for unit in units:
        page = unit['page']
        if page and needle in compact(unit['text']) and page not in hits:
            snippet = unit['text']
            offset = snippet.casefold().find(query.casefold())
            start = max(0, offset - 90)
            hits[page] = {'page': page, 'locator': unit['locator'], 'unit': unit['id'],
                          'excerpt': snippet[start:start + 240]}
    return {'query': query, 'matches': list(hits.values())[:12], 'match_count': len(hits),
            'missing_pages': item['missing_pages']}


def validate_settings(config):
    info = config.get('textbook')
    require(isinstance(info, dict) and set(info) == {'book_id', 'version', 'focus', 'title', 'stage', 'grade'},
            'Use the textbook binding created by textbooks bind.')
    require(all(isinstance(info.get(k), str) and info[k].strip() for k in ('book_id', 'focus', 'title', 'stage')),
            'Textbook scope and identity must be explicit.')
    require(info['grade'] is None or isinstance(info['grade'], str), 'Invalid textbook grade.')
    require(isinstance(info['version'], str) and re.fullmatch('[0-9a-f]{64}', info['version']),
            'Textbook binding needs the original PDF checksum.')
    settings = config.get('materials', {})
    materials.validate_config(settings)
    require(settings['policy'] == 'strict' and not config.get('course_pathway'),
            'Textbook mode requires a strict material selection.')
    selections = settings['selections']
    require(len(selections) == 1 and selections[0].get('version') == info['version'],
            'Textbook scope must bind one selected textbook version.')


def bind(root, book, material_id, version, pages, focus):
    require(isinstance(focus, str) and 0 < len(focus.strip()) <= 200, 'Name the intended learning scope.')
    source_pdf(root, book['book_id'], version)
    selection = materials.select(root, material_id, version, pages=pages)
    config = {
        'textbook': {'book_id': book['book_id'], 'version': version, 'title': book['title'],
                     'stage': book['stage'], 'grade': book.get('grade'), 'focus': focus.strip()},
        'materials': {'policy': 'strict', 'selections': [selection]},
    }
    validate_settings(config)
    return config


def crop_bytes(pdf, page_number, box):
    import pypdfium2 as pdfium

    require(type(page_number) is int and page_number > 0, 'Use a positive 1-based PDF page number.')
    require(isinstance(box, (tuple, list)) and len(box) == 4
            and all(type(value) in (int, float) and 0 <= value <= 1 for value in box),
            'Use normalized x0 y0 x1 y1 crop coordinates between 0 and 1.')
    x0, y0, x1, y1 = box
    require(x1 - x0 >= 0.02 and y1 - y0 >= 0.02, 'Choose a visible original figure rectangle.')
    with pdfium.PdfDocument(pdf) as source:
        require(page_number <= len(source), 'PDF page is outside the source book.')
        page = source[page_number - 1]
        try:
            width, height = page.get_size()
            require(0 < width <= 3000 and 0 < height <= 3000, 'Source page dimensions exceed the preview budget.')
            scale = min(2.5, 2200 / max(width, height))
            bitmap = page.render(scale=scale, crop=(x0 * width, (1-y1) * height, (1-x1) * width, y0 * height),
                                 draw_annots=False, may_draw_forms=False, limit_image_cache=True)
            try:
                image = bitmap.to_pil().convert('RGB')
                buffer = io.BytesIO()
                image.save(buffer, 'PNG')
                return buffer.getvalue()
            finally:
                bitmap.close()
        finally:
            page.close()


def extract_figure(root, book, version, page, box, caption):
    root = Path(root).resolve()
    require(isinstance(caption, str) and bool(caption.strip()), 'Describe the figure in a caption.')
    pdf = source_pdf(root, book['book_id'], version)
    raw = crop_bytes(pdf, page, box)
    sha = hashlib.sha256(raw).hexdigest()
    ref = {'book_id': book['book_id'], 'version': version, 'page': page, 'box': list(box), 'sha256': sha}
    path = materials.path(root, 'textbook-figures', sha + '.png')
    with core.lock(root):
        path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        temporary = path.with_suffix('.tmp')
        try:
            require(not temporary.is_symlink(), 'Figure staging file cannot use symlinks.')
            temporary.write_bytes(raw)
            temporary.replace(path)
        finally:
            temporary.unlink(missing_ok=True)
    return {'path': path.relative_to(root).as_posix(), 'caption': caption,
            'credit': f'教材原图 / Original textbook figure · {book["title"]} · PDF p. {page}', 'textbook_ref': ref}


def validate_figure(root, config, figure, sources):
    validate_settings(config)
    book = config['textbook']
    ref = figure.get('textbook_ref')
    require(isinstance(ref, dict) and set(ref) == {'book_id', 'version', 'page', 'box', 'sha256'},
            'Use an original textbook figure generated by textbooks figure.')
    require(ref['book_id'] == book['book_id'] and ref['version'] == book['version'],
            'Figure comes from a different textbook edition.')
    selection = config['materials']['selections'][0]
    item = materials.verify_selection(root, selection)
    page = ref['page']
    require(type(page) is int and page > 0, 'Invalid textbook figure page.')
    page_units = {unit['id'] for unit in item['units'] if unit['page'] == page}
    require(bool(page_units.intersection(selection['units'])), 'Figure page is outside the selected textbook scope.')
    require(any(source.get('material_ref', {}).get('unit') in page_units
                and source.get('material_ref', {}).get('version') == book['version'] for source in sources),
            'Cite evidence from the same page as the original textbook figure.')
    sha = ref['sha256']
    require(isinstance(sha, str) and re.fullmatch('[0-9a-f]{64}', sha), 'Invalid textbook figure checksum.')
    path = materials.path(root, 'textbook-figures', sha + '.png')
    require(Path(root).resolve() / figure['path'] == path and core.digest(path) == sha,
            'Original textbook figure changed or is not in its provenance location.')
    original = source_pdf(root, book['book_id'], book['version'])
    require(hashlib.sha256(crop_bytes(original, page, ref['box'])).hexdigest() == sha,
            'Original textbook figure changed or does not match its recorded crop.')
    require(figure['credit'] == f'教材原图 / Original textbook figure · {book["title"]} · PDF p. {page}',
            'Keep the original textbook figure attribution and PDF page.')
