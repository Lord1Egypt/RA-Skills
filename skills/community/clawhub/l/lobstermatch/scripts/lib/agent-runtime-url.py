#!/usr/bin/env python3
"""Normalize a LobsterMatch URL before an agent token is attached.

Percent-decode the path until it is stable, reject traversal and encoding
tricks, then allowlist the normalized path. Callers must request the returned
url and must not attach a token unless sendAgentHeaders is true.
"""
import json
import re
import sys
from urllib.parse import unquote, urlsplit, urlunsplit

AGENT_RUNTIME_PREFIXES = (
    '/api/sessions',
    '/api/dialogs',
    '/api/agents',
    '/api/help-requests',
    '/api/help-invitations',
)
BLOCKED_PREFIXES = ('/api/growth', '/admin')
BLOCKED_EXACT = {'/api/growth', '/admin/growth'}
FORBIDDEN_ENCODINGS = ('%2e', '%2f', '%5c', '%3f', '%23', '%00')
SEGMENT_RE = re.compile(r'^[A-Za-z0-9._~-]+$')
QUERY_RE = re.compile(r'^[A-Za-z0-9._~!$&\'()*+,;=:@:/-]*$')


def emit(payload, ok):
    print(json.dumps(payload))
    return 0 if ok else 1


def reject(error, message, path=''):
    return emit({
        'ok': False,
        'error': error,
        'message': message,
        'path': path,
        'sendAgentHeaders': False,
    }, False)


def bad_chars(value):
    return any(ord(char) < 0x21 or ord(char) == 0x7f or ord(char) > 0x7e for char in value)


def forbidden_encoding(value):
    lowered = value.lower()
    return any(token in lowered for token in FORBIDDEN_ENCODINGS)


def decode_until_stable(value):
    current = value
    for _ in range(8):
        if forbidden_encoding(current) or '\\' in current or '//' in current or bad_chars(current):
            return None
        if '?' in current or '#' in current:
            return None
        decoded = unquote(current)
        if decoded == current:
            return current
        current = decoded
    return None


def allowlisted(path):
    if path in BLOCKED_EXACT or any(path == prefix or path.startswith(prefix + '/') for prefix in BLOCKED_PREFIXES):
        return 'blocked'
    if any(path == prefix or path.startswith(prefix + '/') for prefix in AGENT_RUNTIME_PREFIXES):
        return 'allowed'
    return 'rejected'


def normalize_query(query):
    if not query:
        return ''
    if not QUERY_RE.fullmatch(query) or '..' in query or '//' in query or '\\' in query or '%' in query:
        return None
    decoded = decode_until_stable(query)
    if decoded != query:
        return None
    return query


def canonical_path(raw_path):
    if not raw_path.startswith('/') or raw_path.startswith('//'):
        return None
    if '\\' in raw_path or '//' in raw_path or '?' in raw_path or '#' in raw_path or '%' in raw_path:
        return None
    if forbidden_encoding(raw_path) or bad_chars(raw_path):
        return None
    decoded = decode_until_stable(raw_path)
    if not decoded or '%' in decoded or '\\' in decoded or '//' in decoded or '?' in decoded or '#' in decoded:
        return None
    if bad_chars(decoded) or not decoded.startswith('/') or decoded.startswith('//'):
        return None
    segments = decoded.split('/')
    if segments[0] != '':
        return None
    normalized = []
    for segment in segments[1:]:
        if segment in {'', '.', '..'} or not SEGMENT_RE.fullmatch(segment):
            return None
        normalized.append(segment)
    if not normalized:
        return None
    return '/' + '/'.join(normalized)


def evaluate(base_url, target):
    base_text = str(base_url or '').strip()
    target_text = str(target or '').strip()
    if bad_chars(base_text) or '\\' in base_text or not target_text or bad_chars(target_text) or '\\' in target_text:
        return reject('unsafe-agent-runtime-path', 'The request path contains a backslash, space, control character, or non-ASCII character.')
    base = urlsplit(base_text)
    if base.scheme not in {'http', 'https'} or not base.hostname or base.username or base.password or base.query or base.fragment:
        return reject('non-lobstermatch-target-blocked', 'Agent runtime auth is only sent to the configured LobsterMatch baseUrl.')
    if base.path not in {'', '/'}:
        return reject('non-lobstermatch-target-blocked', 'Agent runtime auth is only sent to the configured LobsterMatch baseUrl.')
    absolute = target_text.startswith('http://') or target_text.startswith('https://')
    if absolute:
        parsed = urlsplit(target_text)
        if parsed.scheme != base.scheme or parsed.netloc != base.netloc or parsed.username or parsed.password:
            return reject('non-lobstermatch-target-blocked', 'Agent runtime auth is only sent to the configured LobsterMatch baseUrl.')
    else:
        if target_text.startswith('//'):
            return reject('unsafe-agent-runtime-path', 'The request path contains an empty segment.')
        raw = target_text if target_text.startswith('/') else '/' + target_text
        parsed = urlsplit(raw)
        if parsed.scheme or parsed.netloc:
            return reject('unsafe-agent-runtime-path', 'The request path is not a LobsterMatch agent-runtime path.')
    if parsed.fragment:
        return reject('unsafe-agent-runtime-path', 'The request path contains a query or fragment trick.', parsed.path or '')
    path = canonical_path(parsed.path or '')
    if not path:
        return reject('unsafe-agent-runtime-path', 'The request path is not a canonical agent-runtime path.', parsed.path or '')
    query = normalize_query(parsed.query)
    if query is None:
        return reject('unsafe-agent-runtime-path', 'The request path contains a query or fragment trick.', path)
    decision = allowlisted(path)
    if decision == 'blocked':
        return reject('admin-route-blocked', 'Agent session headers must not be sent to Growth/admin/diagnostic routes.', path)
    if decision != 'allowed':
        return reject('non-agent-runtime-route', 'This helper only sends agent auth to known agent-runtime APIs.', path)
    url = urlunsplit((base.scheme, base.netloc, path, query, ''))
    checked = urlsplit(url)
    if checked.path != path or checked.query != query or checked.fragment or checked.netloc != base.netloc:
        return reject('unsafe-agent-runtime-path', 'The request path is not a canonical agent-runtime path.', path)
    return emit({
        'ok': True,
        'url': url,
        'path': path,
        'sendAgentHeaders': True,
    }, True)


def main(argv):
    args = list(argv)
    print_url = False
    if args and args[0] == '--print-url':
        print_url = True
        args = args[1:]
    if len(args) != 2:
        return reject('unsafe-agent-runtime-path', 'A base URL and request path are required.')
    if print_url:
        # Re-run through evaluate, but publish only the URL when the token may be attached.
        import io
        from contextlib import redirect_stdout
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            status = evaluate(args[0], args[1])
        payload = json.loads(buffer.getvalue() or '{}')
        if status == 0 and payload.get('sendAgentHeaders') is True and payload.get('url'):
            print(payload['url'])
            return 0
        print(payload.get('message') or 'Refusing to attach a token to this path.', file=sys.stderr)
        return 1
    return evaluate(args[0], args[1])


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
