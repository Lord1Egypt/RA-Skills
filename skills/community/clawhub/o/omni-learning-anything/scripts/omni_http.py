"""Bounded HTTP calls without secret-bearing errors, redirects or write retries."""
import re
from urllib.parse import urlsplit


class HTTP:
    def __init__(self):
        import requests
        self.session = requests.Session()

    def json(self, method, url, **kwargs):
        try:
            response = self.session.request(method, url, timeout=(10, 45), allow_redirects=False, **kwargs)
            if not 200 <= response.status_code < 300:
                raise RuntimeError('Provider HTTP status ' + str(response.status_code))
            result = response.json()
            if not isinstance(result, dict):
                raise RuntimeError('Provider returned a non-object response.')
            return result
        except Exception:
            raise RuntimeError('Provider HTTP request failed; check permissions/network and reconcile uncertain writes.') from None

    def download(self, url, allowed_hosts=('docs.qq.com', 'myqcloud.com', 'qcloud.com', 'gtimg.com'), max_bytes=100 * 1024 * 1024):
        parsed = urlsplit(url); host = parsed.hostname or ''
        if parsed.scheme != 'https' or parsed.username or parsed.password or not any(host == h or host.endswith('.' + h) for h in allowed_hosts):
            raise ValueError('Untrusted provider download URL.')
        try:
            # No account headers are sent to temporary storage URLs.
            with self.session.get(url, timeout=(10, 45), allow_redirects=False, stream=True) as response:
                if response.status_code != 200:
                    raise RuntimeError('Provider download failed.')
                chunks = []; size = 0
                for chunk in response.iter_content(65536):
                    size += len(chunk)
                    if size > max_bytes:
                        raise ValueError('Provider download exceeds size limit.')
                    chunks.append(chunk)
                return b''.join(chunks)
        except Exception:
            raise RuntimeError('Provider document download failed.') from None


def business(response, field):
    if response.get(field) != 0:
        # Provider messages may echo supplied credentials; report only numeric codes.
        code = response.get(field)
        safe = str(code) if isinstance(code, int) else 'missing'
        raise RuntimeError('Provider business error: ' + safe)
    return response.get('data', {})


def segment(value):
    from urllib.parse import quote
    if not isinstance(value, str) or not value or len(value)>512 or any(ch.isspace() for ch in value) or any(ch in value for ch in ('/', '\\', '?', '#')):
        raise ValueError('Use a document/folder ID rather than a URL in API configuration.')
    return quote(value, safe='')


def normalize(text):
    return re.sub(r'[\s\u200e\u200f\u202a-\u202e\u2066-\u2069]+', '', text.replace('<br>', '\n'))


def check_text(text, data, include_title=True):
    normalized = normalize(text)
    required = ([data['title']] if include_title else []) + [s['title'] for s in data['sections']]
    required += [s['body'] for s in data['sections']] + [data['figure']['caption'], data['figure']['credit']]
    required += [value for source in data.get('sources',[]) if source.get('material_ref') for value in (source['title'],source['note'])]
    if any(normalize(value) not in normalized for value in required):
        raise ValueError('Remote document readback is incomplete; keep the current lesson pending.')


def check_links(text, data):
    if any(source['url'] not in text for source in data['sources'] if source.get('url')):
        raise ValueError('Remote document is missing source links.')


def document_data(root, manifest):
    import omni_core as c
    key = manifest['key']
    path = root / manifest.get('input', 'plan.json' if key == 'plan' else f'data/{key}.json')
    if not path.resolve().is_relative_to(root.resolve()):
        raise ValueError('Document input escapes project.')
    return c.read(path)


def verified(remote_id=None, url=None, note='Read back sections, figure and all source links'):
    result = {'status': 'verified', 'evidence': {'content_checked': True, 'image_checked': True,
                                               'links_checked': True, 'note': note}}
    if remote_id: result['remote_id'] = remote_id
    if url: result['url'] = url
    return result
