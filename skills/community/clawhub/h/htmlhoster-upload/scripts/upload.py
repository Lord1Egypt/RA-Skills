#!/usr/bin/env python3
"""htmlhoster-upload - publish local files to htmlhoster.com via its Agent upload API.

Pure standard-library implementation (no third-party deps), so any agent
(WorkBuddy / Claude Code / Codex / ...) can run it directly.

htmlhoster is a PUBLIC site: every uploaded file is reachable by anyone who has
the URL, with no authentication. To reduce accidental leaks, the script scans
the content for likely secrets / credentials BEFORE every upload and aborts if
it finds any. Pass --no-check to skip the scan, but only with content you are
certain is safe to publish.

Usage:
  # HTML / images / PDF / ZIP(unzip) hosting
  python upload.py --mode html --file index.html --file logo.png --unzip

  # Markdown - zip package mode (contains .md + assets)
  python upload.py --mode markdown --package doc.zip

  # Markdown - single file + assets mode
  python upload.py --mode markdown --file doc.md --asset img1.png --asset img2.png

  # Delete a page you uploaded (needs the deleteToken from the upload response)
  python upload.py --mode delete --id A1B2C3D4 --token <deleteToken>

Environment:
  HTMLHOSTER_API_BASE            API base URL, default https://api.htmlhoster.com
  HTMLHOSTER_UPLOAD_EXTRA_HEADERS  optional extra headers, "k1:v1;k2:v2"

Output: the API JSON. A successful upload includes both `entryUrl` (the public
link) and `deleteToken` — keep the token if the page may need removing later,
it is the only way to delete that page and it cannot be recovered.
Exit 0 on success, non-zero on failure.
"""
import argparse
import datetime
import json
import os
import re
import sys
import urllib.error
import urllib.request
import zipfile

API_BASE_DEFAULT = "https://api.htmlhoster.com"
BOUNDARY = "----htmlhosterUploadBoundary%s" % datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")


# ---------------------------------------------------------------------------
# Sensitive-information scan
#
# htmlhoster is a public site; anyone with the URL can read uploaded files.
# Before uploading we scan text-like files (and the entries of a markdown zip
# package) for likely secrets / credentials. Matched values are never printed —
# only the file, the kind of match, and a line number — so the scan itself does
# not re-leak what it found.
# ---------------------------------------------------------------------------
# Only scan these text-like extensions; binaries / images / pdf are skipped.
_SCAN_TEXT_EXTS = {
    ".html", ".htm", ".md", ".markdown", ".txt", ".text",
    ".json", ".js", ".mjs", ".ts", ".jsx", ".tsx", ".css", ".scss", ".less",
    ".xml", ".yaml", ".yml", ".toml", ".ini", ".cfg", ".conf", ".env",
    ".csv", ".log", ".sh", ".bash", ".zsh", ".py", ".rb", ".go", ".java",
    ".c", ".cpp", ".h", ".hpp", ".php", ".sql", ".rst", ".tex", ".gradle",
}
# Filenames that are sensitive regardless of content.
_SENSITIVE_NAME_TOKENS = (
    "id_rsa", "id_dsa", "id_ecdsa", "id_ed25519",
    ".env", "credentials", "secrets", ".npmrc", ".netrc",
    "authorized_keys", "known_hosts",
)
_SENSITIVE_NAME_EXTS = (".pem", ".key", ".p12", ".pfx", ".keystore", ".jks", ".kdbx")
# (compiled regex, human label, is_assignment).
# For assignment patterns the captured value is checked against placeholders;
# for the rest the whole match is structurally specific enough to trust.
_SECRET_PATTERNS = [
    (re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA |PGP |ENCRYPTED )?PRIVATE KEY-----"),
     "private key block", False),
    (re.compile(r"AKIA[0-9A-Z]{16}"), "AWS access key id", False),
    (re.compile(r"(?:AKID|LTAI)[0-9A-Za-z]{8,}"), "Alibaba cloud access key", False),
    (re.compile(r"AIza[0-9A-Za-z_\-]{35}"), "Google API key", False),
    (re.compile(r"(?:ghp|gho|ghu|ghs|ghr)_[0-9A-Za-z]{36}"), "GitHub token", False),
    (re.compile(r"github_pat_[0-9A-Za-z_]{22,}"), "GitHub fine-grained PAT", False),
    (re.compile(r"glpat-[0-9A-Za-z_\-]{20,}"), "GitLab PAT", False),
    (re.compile(r"xox[baprs]-[0-9A-Za-z\-]{10,}"), "Slack token", False),
    (re.compile(r"sk-[A-Za-z0-9]{20,}"), "LLM API key (sk-)", False),
    (re.compile(r"cfat_[0-9A-Za-z]{16,}"), "Cloudflare API token", False),
    (re.compile(r"ya29\.[0-9A-Za-z_\-]+"), "Google OAuth token", False),
    (re.compile(r"strip[e]?_[a-z]{2,}_[0-9A-Za-z]{10,}"), "Stripe key", False),
    (re.compile(
        r"(?:password|passwd|pwd|secret|api[_-]?key|access[_-]?token|"
        r"auth[_-]?token|client[_-]?secret|private[_-]?key)\s*[:=]\s*['\"]?([^\s'\"]{12,})"),
     "credential assignment", True),
    (re.compile(r"(?:mongodb|postgres|postgresql|mysql|redis|amqp)://[^\s:/]+:[^\s@]{4,}@"),
     "DB / connection string with credentials", False),
]
# If a credential assignment's value (lowercased) contains any of these, treat
# it as an obvious placeholder and skip — e.g. `password = "your_password"`.
_PLACEHOLDER_VALUES = {
    "your", "example", "exampled", "changeme", "changeit", "test", "demo",
    "sample", "placeholder", "todo", "fixme", "none", "null", "undefined",
    "redacted", "dummy", "fake", "mock", "xxxx", "xxxxx", "xxxxxx", "xxxxxxx",
    "secret", "password",
}
_SCAN_SIZE_CAP = 5 * 1024 * 1024  # skip files larger than 5 MB


def _is_sensitive_filename(path):
    base = os.path.basename(path).lower()
    if base in _SENSITIVE_NAME_TOKENS:
        return True
    for tok in _SENSITIVE_NAME_TOKENS:
        if tok in base:  # e.g. prod.env, my-credentials.json
            return True
    for ext in _SENSITIVE_NAME_EXTS:
        if base.endswith(ext):
            return True
    return False


def _scan_text(name, text):
    """Return [(label, lineno), ...] for the given text content."""
    findings = []
    for lineno, line in enumerate(text.splitlines(), 1):
        for rx, label, is_assign in _SECRET_PATTERNS:
            m = rx.search(line)
            if not m:
                continue
            if is_assign:
                val = m.group(1).lower()
                if any(p in val for p in _PLACEHOLDER_VALUES):
                    break  # placeholder, not a real secret
            findings.append((label, lineno))
            break
    return findings


def _scan_bytes(name, data):
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        try:
            text = data.decode("latin-1")
        except Exception:
            return []
    return _scan_text(name, text)


def _scan_files(specs):
    """specs: list of (path, data_bytes). Returns [(path, label, lineno), ...]."""
    findings = []
    for path, data in specs:
        if _is_sensitive_filename(path):
            findings.append((path, "sensitive filename (key / credential file)", 0))
            continue
        ext = os.path.splitext(path)[1].lower()
        if ext not in _SCAN_TEXT_EXTS or len(data) > _SCAN_SIZE_CAP:
            continue
        for label, lineno in _scan_bytes(path, data):
            findings.append((path, label, lineno))
    return findings


def _scan_zip(path):
    """Scan the text-like entries of a markdown zip package."""
    findings = []
    try:
        with zipfile.ZipFile(path) as zf:
            for info in zf.infolist():
                if info.is_dir() or info.file_size > _SCAN_SIZE_CAP:
                    continue
                if _is_sensitive_filename(info.filename):
                    findings.append((info.filename, "sensitive filename (key / credential file)", 0))
                    continue
                ext = os.path.splitext(info.filename)[1].lower()
                if ext not in _SCAN_TEXT_EXTS:
                    continue
                try:
                    data = zf.read(info)
                except Exception:
                    continue
                for label, lineno in _scan_bytes(info.filename, data):
                    findings.append((info.filename, label, lineno))
    except zipfile.BadZipFile:
        pass
    return findings


def _maybe_abort_on_findings(findings):
    if not findings:
        return
    sys.stderr.write("\n[!] SENSITIVE-INFORMATION SCAN\n")
    sys.stderr.write("    htmlhoster is a PUBLIC site - anyone with the URL can read\n")
    sys.stderr.write("    uploaded files. The following potential secrets / credentials\n")
    sys.stderr.write("    were found. Review them before publishing:\n\n")
    for path, label, lineno in findings:
        loc = " (line %d)" % lineno if lineno else ""
        sys.stderr.write("    - %s  [%s]%s\n" % (path, label, loc))
    sys.stderr.write("\n    If you are CERTAIN the content is safe to publish, re-run with\n")
    sys.stderr.write("    --no-check. Otherwise remove the sensitive data first.\n\n")
    sys.exit(3)


def _encode_multipart(fields):
    """fields: list of (name, value, filename_or_None, content_type_or_None)."""
    parts = []
    for name, value, filename, ctype in fields:
        disp = 'form-data; name="%s"' % name
        if filename:
            disp += '; filename="%s"' % filename
        header = "Content-Disposition: %s\r\n" % disp
        if ctype:
            header += "Content-Type: %s\r\n" % ctype
        body = value if isinstance(value, bytes) else value.encode("utf-8")
        parts.append(("--%s\r\n%s\r\n" % (BOUNDARY, header)).encode("utf-8") + body + b"\r\n")
    body = b"".join(parts) + ("--%s--\r\n" % BOUNDARY).encode("utf-8")
    return body


def _guess_content_type(path):
    ext = os.path.splitext(path)[1].lower()
    table = {
        ".html": "text/html", ".htm": "text/html",
        ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
        ".gif": "image/gif", ".webp": "image/webp", ".svg": "image/svg+xml",
        ".pdf": "application/pdf",
        ".md": "text/markdown", ".markdown": "text/markdown",
        ".zip": "application/zip",
        ".css": "text/css", ".js": "application/javascript",
        ".json": "application/json", ".txt": "text/plain",
    }
    return table.get(ext, "application/octet-stream")


USER_AGENT = "htmlhoster-upload-skill/1.0 (+https://htmlhoster.com/agent/)"


def _send(req, extra_headers):
    req.add_header("User-Agent", USER_AGENT)
    for k, v in (extra_headers or {}).items():
        req.add_header(k, v)
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            return resp.status, resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")
    except Exception as e:  # noqa: BLE001 - surface any network error to caller
        return 0, str(e)


def _post(api_base, endpoint, fields, extra_headers):
    url = api_base.rstrip("/") + endpoint
    data = _encode_multipart(fields)
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "multipart/form-data; boundary=%s" % BOUNDARY)
    return _send(req, extra_headers)


def _delete(api_base, upload_id, token, extra_headers):
    url = "%s/api/uploads/%s" % (api_base.rstrip("/"), upload_id)
    req = urllib.request.Request(url, method="DELETE")
    req.add_header("X-Delete-Token", token)
    return _send(req, extra_headers)


def main():
    p = argparse.ArgumentParser(description="Upload files to htmlhoster via Agent endpoint")
    p.add_argument("--mode", choices=["html", "markdown", "delete"], default="html")
    p.add_argument("--id", help="(delete) uploadId of the page to remove")
    p.add_argument("--token", help="(delete) deleteToken returned by the upload response")
    p.add_argument("--file", action="append", default=[], help="file path (html: multiple; markdown: first is .md)")
    p.add_argument("--path", action="append", default=[], help="(html) relative path per --file, optional")
    p.add_argument("--unzip", action="store_true", help="(html) unzip zip and host contents")
    p.add_argument("--package", help="(markdown) zip package path (contains .md + assets)")
    p.add_argument("--asset", action="append", default=[], help="(markdown) asset file path")
    p.add_argument("--asset-path", action="append", default=[], help="(markdown) asset relative path, optional")
    p.add_argument("--api-base", default=os.environ.get("HTMLHOSTER_API_BASE", API_BASE_DEFAULT))
    p.add_argument("--no-check", action="store_true",
                   help="skip the pre-upload sensitive-information scan (use only with trusted content)")
    args = p.parse_args()

    extra = {}
    eh = os.environ.get("HTMLHOSTER_UPLOAD_EXTRA_HEADERS")
    if eh:
        for item in eh.split(";"):
            if ":" in item:
                k, v = item.split(":", 1)
                extra[k.strip()] = v.strip()

    if args.mode == "delete":
        if not args.id or not args.token:
            sys.stderr.write("error: --id and --token are required for delete mode\n")
            sys.exit(2)
        status, raw = _delete(args.api_base, args.id, args.token, extra)
    elif args.mode == "html":
        if not args.file:
            sys.stderr.write("error: --file required for html mode\n")
            sys.exit(2)
        specs = []
        fields = []
        for i, f in enumerate(args.file):
            with open(f, "rb") as fh:
                data = fh.read()
            specs.append((f, data))
            fields.append(("files", data, os.path.basename(f), _guess_content_type(f)))
            if i < len(args.path) and args.path[i]:
                fields.append(("paths", args.path[i], None, None))
        if args.unzip:
            fields.append(("unzip", "true", None, None))
        _maybe_abort_on_findings(_scan_files(specs) if not args.no_check else [])
        status, raw = _post(args.api_base, "/agent/upload", fields, extra)
    else:  # markdown
        fields = []
        if args.package:
            findings = _scan_zip(args.package) if not args.no_check else []
            with open(args.package, "rb") as fh:
                data = fh.read()
            fields.append(("package", data, os.path.basename(args.package), "application/zip"))
        else:
            if not args.file:
                sys.stderr.write("error: --file (doc.md) or --package required for markdown mode\n")
                sys.exit(2)
            specs = []
            with open(args.file[0], "rb") as fh:
                data = fh.read()
            specs.append((args.file[0], data))
            fields.append(("markdown", data, os.path.basename(args.file[0]), "text/markdown"))
            for i, a in enumerate(args.asset):
                with open(a, "rb") as fh:
                    adata = fh.read()
                specs.append((a, adata))
                fields.append(("assets", adata, os.path.basename(a), _guess_content_type(a)))
                if i < len(args.asset_path) and args.asset_path[i]:
                    fields.append(("asset_paths", args.asset_path[i], None, None))
            findings = _scan_files(specs) if not args.no_check else []
        _maybe_abort_on_findings(findings)
        status, raw = _post(args.api_base, "/agent/markdown", fields, extra)

    try:
        payload = json.loads(raw) if raw else {}
    except json.JSONDecodeError:
        payload = {"raw": raw}
    action = "delete" if args.mode == "delete" else "upload"
    if status and 200 <= status < 300:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        sys.exit(0)
    sys.stderr.write("%s failed (HTTP %s):\n%s\n" % (action, status, raw))
    sys.exit(1)


if __name__ == "__main__":
    main()
