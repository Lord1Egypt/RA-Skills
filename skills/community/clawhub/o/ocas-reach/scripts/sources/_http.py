"""Shared HTTP helper for custom source modules — stdlib only."""
import json
import urllib.parse
import urllib.request
import urllib.error


def get(url, headers=None, timeout=30):
    req = urllib.request.Request(url, headers=headers or {})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        raw = r.read()
        ct = r.headers.get("Content-Type", "")
        if "json" in ct or raw.startswith(b"{") or raw.startswith(b"["):
            return json.loads(raw.decode("utf-8", "replace"))
        return raw.decode("utf-8", "replace")


def post(url, body, headers=None, timeout=30):
    headers = dict(headers or {})
    if isinstance(body, dict):
        headers.setdefault("Content-Type", "application/json")
        data = json.dumps(body).encode()
    elif isinstance(body, str):
        data = body.encode()
    else:
        data = body
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        raw = r.read()
        ct = r.headers.get("Content-Type", "")
        if "json" in ct or raw.startswith(b"{"):
            return json.loads(raw.decode("utf-8", "replace"))
        return raw.decode("utf-8", "replace")


def qs(params):
    return urllib.parse.urlencode({k: v for k, v in params.items() if v is not None}, doseq=True)
