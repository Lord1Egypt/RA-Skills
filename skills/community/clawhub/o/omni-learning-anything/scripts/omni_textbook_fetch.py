"""Acquire one pinned textbook into a private course archive on demand."""
import hashlib
import os
import re
import stat
import tempfile
from pathlib import Path
from time import monotonic
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import HTTPRedirectHandler, Request, build_opener

import omni_materials as materials


REPOSITORY = 'TapXWorld/ChinaTextbook'
MAX_TEXTBOOK_BYTES = 256 * 1024 * 1024
MAX_FETCH_SECONDS = 180
MAX_IO_SECONDS = 12
MAX_PARTS = 16
CHUNK = 1024 * 1024
BOOK_ID = re.compile(r'[a-z0-9][a-z0-9_-]{0,79}')


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if fp is not None:
            fp.close()
        raise ValueError('Pinned textbook download refused an HTTP redirect; provide an authorized local copy.')


OPENER = build_opener(NoRedirect())


def _hex(value, length):
    return isinstance(value, str) and bool(re.fullmatch(f'[0-9a-f]{{{length}}}', value))


def _book_id(value):
    if not isinstance(value, str) or not BOOK_ID.fullmatch(value):
        raise ValueError('Invalid textbook ID.')
    return value


def _sources(book):
    if book.get('repository') != REPOSITORY or not _hex(book.get('commit'), 40):
        raise ValueError('Textbook origin must be the catalog repository at a pinned commit.')
    sources = book.get('sources')
    if not isinstance(sources, list) or not 1 <= len(sources) <= MAX_PARTS:
        raise ValueError('Textbook index must contain a bounded ordered list of source files.')
    split = len(sources) > 1
    first_path = None
    for i, source in enumerate(sources, 1):
        if not isinstance(source, dict):
            raise ValueError('Invalid textbook source record.')
        path = source.get('path')
        size = source.get('size')
        part = source.get('part')
        suffix = f'.pdf.{i}' if split else '.pdf'
        if (not isinstance(path, str) or not path.lower().endswith(suffix)
                or any(p in ('', '.', '..') for p in path.split('/'))
                or '\\' in path or any(ord(ch) < 32 or ord(ch) == 127 for ch in path)):
            raise ValueError('Invalid textbook source path.')
        if (split and (type(part) is not int or part != i)) or (not split and part is not None):
            raise ValueError('Textbook split sources must have consecutive ordered part numbers.')
        if split:
            stem = path.rsplit('.', 1)[0]
            if first_path is None:
                first_path = stem
            if first_path != stem:
                raise ValueError('Textbook split sources must share a single base path.')
        if type(size) is not int or size <= 0 or not _hex(source.get('sha'), 40):
            raise ValueError('Textbook source needs a Git blob checksum and positive byte size.')
    return sources


def _raw_url(commit, source):
    return f'https://raw.githubusercontent.com/{REPOSITORY}/{commit}/{quote(source["path"], safe="/")}'


def _open_pdf(path):
    if path.is_symlink():
        raise ValueError('Textbook PDF cannot be a symlink.')
    try:
        fd = os.open(path, os.O_RDONLY | os.O_NONBLOCK | os.O_NOFOLLOW)
    except OSError as error:
        raise ValueError('Textbook PDF is unavailable or became a symlink.') from error
    try:
        info = os.fstat(fd)
        if not stat.S_ISREG(info.st_mode) or not 0 < info.st_size <= MAX_TEXTBOOK_BYTES:
            raise ValueError('Textbook PDF must be a regular file within 256 MiB.')
        return os.fdopen(fd, 'rb')
    except BaseException:
        os.close(fd)
        raise


def _file_sha(path):
    digest = hashlib.sha256()
    with _open_pdf(path) as stream:
        size = 0
        for data in iter(lambda: stream.read(CHUNK), b''):
            size += len(data)
            if size > MAX_TEXTBOOK_BYTES:
                raise ValueError('Textbook PDF grew beyond 256 MiB.')
            digest.update(data)
    return digest.hexdigest()


def _copy_part(read, source, whole, *, out=None):
    size = source['size']
    git = hashlib.sha1(f'blob {size}\0'.encode())
    while size:
        data = read(min(CHUNK, size))
        if not data or len(data) > size:
            return False
        size -= len(data)
        git.update(data)
        whole.update(data)
        if out is not None:
            out.write(data)
    return git.hexdigest() == source['sha']


def _verify_pinned(path, sources):
    with _open_pdf(path) as stream:
        if os.fstat(stream.fileno()).st_size != sum(s['size'] for s in sources):
            return None
        digest = hashlib.sha256()
        for source in sources:
            if not _copy_part(stream.read, source, digest):
                return None
        return None if stream.read(1) else digest.hexdigest()


def _remaining(deadline):
    left = deadline - monotonic()
    if left <= 0:
        raise ValueError('Pinned textbook download timed out; retry or provide an authorized local copy.')
    return left


def _download(urls, sources, target):
    deadline = monotonic() + MAX_FETCH_SECONDS
    digest = hashlib.sha256()
    with target.open('xb') as out:
        for url, source in zip(urls, sources):
            request = Request(url, headers={'Accept-Encoding': 'identity', 'User-Agent': 'Omni-Learning-Textbooks'})
            try:
                with OPENER.open(request, timeout=min(MAX_IO_SECONDS, _remaining(deadline))) as response:
                    if response.status != 200:
                        raise ValueError('Pinned textbook source did not return a complete file.')
                    if response.headers.get('Content-Type', '').lower().startswith(('text/html', 'application/xhtml')):
                        raise ValueError('Pinned textbook source returned HTML in place of the file.')
                    length = response.headers.get('Content-Length')
                    if length is not None and (not length.isdigit() or int(length) != source['size']):
                        raise ValueError('Pinned textbook file size differs from the index.')

                    def read(limit):
                        _remaining(deadline)
                        chunk = response.read1(limit)
                        _remaining(deadline)
                        return chunk

                    if not _copy_part(read, source, digest, out=out) or read(1):
                        raise ValueError('Pinned textbook file size or Git blob checksum differs from the index.')
            except HTTPError as error:
                error.close()
                raise ValueError(f'Pinned textbook source returned HTTP {error.code}; provide an authorized local copy.') from None
            except (URLError, OSError) as error:
                raise ValueError('Pinned textbook download failed; retry or provide an authorized local copy.') from error
    return digest.hexdigest()


def _copy_local(path, target):
    digest = hashlib.sha256()
    with _open_pdf(path) as stream, target.open('xb') as out:
        size = 0
        for data in iter(lambda: stream.read(CHUNK), b''):
            size += len(data)
            if size > MAX_TEXTBOOK_BYTES:
                raise ValueError('Textbook PDF grew beyond 256 MiB.')
            digest.update(data)
            out.write(data)
    return digest.hexdigest()


def _check_pdf(path):
    with _open_pdf(path) as stream:
        header = stream.read(16)
        size = os.fstat(stream.fileno()).st_size
        stream.seek(max(0, size - 8192))
        trailer = stream.read(8192)
        if not re.match(rb'%PDF-\d\.\d[\r\n]', header) or not re.search(rb'startxref\s+\d+\s+%%EOF\s*\Z', trailer):
            raise ValueError('Acquired bytes are not a complete PDF.')
        try:
            from pypdf import PdfReader
        except ModuleNotFoundError:
            return
        try:
            stream.seek(0)
            reader = PdfReader(stream)
            if not reader.is_encrypted and not len(reader.pages):
                raise ValueError('PDF has no pages.')
        except Exception as error:
            raise ValueError('Acquired PDF could not be opened; provide a readable authorized copy.') from error


def _storage(root, book_id, sha256):
    _book_id(book_id)
    if not _hex(sha256, 64):
        raise ValueError('Invalid textbook SHA-256.')
    return materials.path(root, 'textbooks', book_id, sha256, book_id + '.pdf')


def source_pdf(root, book_id, sha256):
    """Return the verified physical-page original for an exact acquisition."""
    path = _storage(root, book_id, sha256)
    if _file_sha(path) != sha256:
        raise ValueError('Archived textbook PDF checksum changed; preserve its exact verified original.')
    return path


def _cached(root, book_dir, book_id, sources):
    for candidate in sorted(book_dir.iterdir()):
        if not _hex(candidate.name, 64):
            continue
        path = _storage(root, book_id, candidate.name)
        if path.exists() and _verify_pinned(path, sources) == candidate.name:
            return path, candidate.name
    return None


def acquire(root, book, *, local_pdf=None, confirm_local_edition=False, retry=False):
    """Capture the selected edition only and import it with physical PDF page numbers."""
    root = Path(root).resolve()
    if root.is_relative_to(Path(__file__).resolve().parents[1]):
        raise ValueError('Use a course archive outside the installed skill.')
    book_id = _book_id(book.get('book_id'))
    sources = _sources(book)
    if local_pdf is None and sum(s['size'] for s in sources) > MAX_TEXTBOOK_BYTES:
        raise ValueError('Pinned textbook exceeds the 256 MiB acquisition budget; provide a smaller authorized PDF.')
    urls = [_raw_url(book['commit'], source) for source in sources]
    origin_url = urls[0]
    origin = 'pinned_repository'

    book_dir = materials.path(root, 'textbooks', book_id)
    book_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
    cached = _cached(root, book_dir, book_id, sources) if local_pdf is None else None
    if cached:
        path, digest = cached
    else:
        with tempfile.TemporaryDirectory(prefix='.stage-', dir=book_dir) as stage:
            staged = Path(stage) / (book_id + '.pdf')
            if local_pdf is None:
                digest = _download(urls, sources, staged)
            else:
                local_pdf = Path(local_pdf).absolute()
                digest = _copy_local(local_pdf, staged)
                _check_pdf(staged)
                if _verify_pinned(staged, sources) != digest:
                    if confirm_local_edition is not True:
                        raise ValueError('Local PDF bytes differ from the pinned edition. Confirm this authorized copy matches the selected edition.')
                    origin = 'user_confirmed_edition'
                    origin_url = None
            if local_pdf is None:
                _check_pdf(staged)
            path = _storage(root, book_id, digest)
            path.parent.mkdir(mode=0o700, exist_ok=True)
            try:
                os.link(staged, path)
            except FileExistsError:
                source_pdf(root, book_id, digest)

    material_key = f'{book_id}\0{origin_url or origin}'
    material_id = 'm_' + hashlib.sha256(material_key.encode()).hexdigest()[:16]
    material = materials.import_file(root, path, material_id=material_id, url=origin_url,
                                     retry=retry, max_file=MAX_TEXTBOOK_BYTES,
                                     title=book['title'], publisher=book.get('publisher') or book.get('edition'))
    if material['version'] != digest:
        raise ValueError('Archived textbook PDF changed during material import.')
    return {'book_id': book_id, 'pdf_path': str(path.relative_to(root)), 'sha256': digest,
            'origin': origin, 'origin_url': origin_url, 'material': material}
