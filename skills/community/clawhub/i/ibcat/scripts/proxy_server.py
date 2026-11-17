#!/usr/bin/env python3
"""
OpenAI-compatible translation proxy server for BabelDOC.
Two-phase operation:
  - extract mode: Collects all text segments from BabelDOC into segments.json
  - translate mode: Returns translations from translations.json for each segment

Usage:
  PROXY_MODE=extract python3 proxy_server.py   # Phase 1: collect segments
  PROXY_MODE=translate python3 proxy_server.py  # Phase 3: serve translations

Environment variables:
  PROXY_MODE     - 'extract' or 'translate' (default: extract)
  PROXY_PORT     - Port number (default: 8899)
  WORK_DIR       - Working directory for JSON files (default: /data/user/work)
"""

import json
import os
import re
import sys
import threading
import time
import uuid
from http.server import HTTPServer, BaseHTTPRequestHandler

# Configuration from environment
MODE = os.environ.get('PROXY_MODE', 'extract')
PORT = int(os.environ.get('PROXY_PORT', '8899'))
WORK_DIR = os.environ.get('WORK_DIR', '/data/user/work')

SEGMENTS_FILE = os.path.join(WORK_DIR, 'segments.json')
TRANSLATIONS_FILE = os.path.join(WORK_DIR, 'translations.json')
UNKNOWN_FILE = os.path.join(WORK_DIR, 'unknown_segments.json')

_segments = {}
_translations = {}
_unknown = {}
_lock = threading.Lock()


def load_files():
    """Load JSON data files."""
    global _segments, _translations, _unknown
    if os.path.exists(SEGMENTS_FILE):
        with open(SEGMENTS_FILE, 'r') as f:
            _segments = json.load(f)
    if os.path.exists(TRANSLATIONS_FILE):
        with open(TRANSLATIONS_FILE, 'r') as f:
            _translations = json.load(f)
    if os.path.exists(UNKNOWN_FILE):
        with open(UNKNOWN_FILE, 'r') as f:
            _unknown = json.load(f)
    print(f"Loaded {len(_segments)} segments, {len(_translations)} translations, {len(_unknown)} unknown")


def save_json(filepath, data):
    """Save JSON data atomically."""
    tmp = filepath + '.tmp'
    with open(tmp, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(tmp, filepath)


def normalize_text(text):
    """Normalize whitespace for matching."""
    return re.sub(r'\s+', ' ', text.strip())


def extract_text_from_content(content):
    """
    Extract actual text(s) to translate from BabelDOC's message content.
    BabelDOC sends text in various formats; this function normalizes them.
    Returns a list of (format_type, text) tuples.
    """
    results = []

    # Format 1: JSON batch format - array of {"input": "text", ...}
    try:
        json_starts = [m.start() for m in re.finditer(r'\[\s*\{', content)]
        for start in json_starts:
            depth = 0
            end = start
            for i in range(start, len(content)):
                if content[i] == '[':
                    depth += 1
                elif content[i] == ']':
                    depth -= 1
                    if depth == 0:
                        end = i + 1
                        break
            try:
                items = json.loads(content[start:end])
                if isinstance(items, list):
                    for item in items:
                        if isinstance(item, dict) and 'input' in item:
                            results.append(('json', item['input']))
            except json.JSONDecodeError:
                pass
    except Exception:
        pass

    # Format 2: "Now translate the following text:\n\n<text>"
    simple_match = re.search(r'Now translate the following text:\s*\n+(.+)$', content, re.DOTALL)
    if simple_match:
        text = simple_match.group(1).strip()
        if text:
            results.append(('simple', text))

    # Format 3: "Input:\n\n<text>" (do_translate format)
    dt_match = re.search(r'Input:\s*\n+(.+)$', content, re.DOTALL)
    if dt_match:
        text = dt_match.group(1).strip()
        if text and (';; Treat' in content or 'translate' in content[:200].lower()):
            results.append(('do_translate', text))

    # Format 4: Direct text (do_llm_translate - content is just the text)
    if not results:
        if not content.startswith('You are a professional') and not content.startswith(';;'):
            results.append(('direct', content.strip()))

    return results


def lookup_translation(text):
    """Look up translation for a given text."""
    normalized = normalize_text(text)

    # Exact match
    if normalized in _translations:
        return _translations[normalized]
    if text in _translations:
        return _translations[text]

    # Case-insensitive match
    for key, val in _translations.items():
        if normalize_text(key).lower() == normalized.lower():
            return val

    return None


def handle_translation(content):
    """Process a translation request and return response content."""
    if not content or not content.strip():
        return content

    texts = extract_text_from_content(content)
    if not texts:
        return content

    if MODE == 'translate':
        if len(texts) == 1:
            fmt, text = texts[0]
            result = lookup_translation(text)
            if result is not None:
                return result
            # Log unknown segment
            with _lock:
                if text not in _unknown:
                    _unknown[text] = True
                    save_json(UNKNOWN_FILE, _unknown)
            return text  # Return original if no translation found
        else:
            for fmt, text in texts:
                with _lock:
                    if text not in _unknown:
                        _unknown[text] = True
                        save_json(UNKNOWN_FILE, _unknown)
            return content
    else:  # extract mode
        for fmt, text in texts:
            with _lock:
                if text not in _segments:
                    _segments[text] = {'format': fmt}
                    save_json(SEGMENTS_FILE, _segments)

        if len(texts) == 1:
            return texts[0][1]
        else:
            return content


class ProxyHandler(BaseHTTPRequestHandler):
    """HTTP handler mimicking OpenAI API."""

    def do_POST(self):
        if self.path == '/v1/chat/completions':
            self.handle_chat()
        else:
            self.send_error(404)

    def do_GET(self):
        if self.path == '/v1/models':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                "object": "list",
                "data": [{"id": "gpt-4o-mini", "object": "model", "created": int(time.time())}]
            }).encode())
        else:
            self.send_error(404)

    def handle_chat(self):
        text = ""
        try:
            body = self.rfile.read(int(self.headers.get('Content-Length', 0)))
            data = json.loads(body)

            messages = data.get('messages', [])
            model = data.get('model', 'gpt-4o-mini')

            for msg in reversed(messages):
                if msg.get('role') == 'user':
                    text = msg.get('content', '')
                    break

            translated = handle_translation(text)

            response = {
                "id": f"chatcmpl-{uuid.uuid4().hex[:8]}",
                "object": "chat.completion",
                "created": int(time.time()),
                "model": model,
                "choices": [{
                    "index": 0,
                    "message": {"role": "assistant", "content": translated},
                    "finish_reason": "stop",
                }],
                "usage": {
                    "prompt_tokens": max(1, len(text) // 4),
                    "completion_tokens": max(1, len(translated) // 4),
                    "total_tokens": max(1, (len(text) + len(translated)) // 4),
                },
            }

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            # Return valid response even on error (don't break BabelDOC)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {
                "id": f"chatcmpl-{uuid.uuid4().hex[:8]}",
                "object": "chat.completion",
                "created": int(time.time()),
                "model": "gpt-4o-mini",
                "choices": [{
                    "index": 0,
                    "message": {"role": "assistant", "content": text if text else ""},
                    "finish_reason": "stop",
                }],
                "usage": {"prompt_tokens": 1, "completion_tokens": 1, "total_tokens": 2},
            }
            self.wfile.write(json.dumps(response).encode())

    def log_message(self, *args):
        pass


if __name__ == '__main__':
    load_files()
    print(f"Proxy server running in '{MODE}' mode on port {PORT}")
    print(f"  Work dir: {WORK_DIR}")
    print(f"  Segments: {SEGMENTS_FILE}")
    print(f"  Translations: {TRANSLATIONS_FILE}")
    server = HTTPServer(('127.0.0.1', PORT), ProxyHandler)
    server.serve_forever()
