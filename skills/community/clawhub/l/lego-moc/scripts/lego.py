#!/usr/bin/env python3
"""Client for the LEGO parts recognition server (the "lego-moc" agent skill).

Stage 1: uploads 1-30 photos of loose LEGO parts, waits for the asynchronous
result and stores it in a local directory shared by all agents (~/.lego-parts/,
or $LEGO_PARTS_HOME).  Stage 2: downloads the MOC design guide and connector
sheets, submits an LDraw model designed from that inventory and fetches the
verifier's report.  Python 3.8+, standard library only.  See ../SKILL.md.

  lego.py scan [--no-wait] [--wait SECONDS] [--images] PHOTO...
  lego.py status [--wait SECONDS] [--images] [TASK_ID...]
  lego.py parts [--images]
  lego.py whoami
  lego.py moc guide [--parts-file PATH | --parts 3001,3020,...]
  lego.py moc find WORD...       look up supported part numbers by name (for a free build)
  lego.py moc submit [--title NAME] [--brief TEXT] [--design design.json] [--moc MOC_ID] [--mode inventory|free]
                     [--parts-file PATH] [--no-wait] [--wait SECONDS] MODEL.ldr
  lego.py moc status [--wait SECONDS] [MOC_ID]
  lego.py mcp                    local MCP server (stdio) for agent hosts: see coord/api-skill.md 3.5
  lego.py mcp-config [--remote]  print the JSON to paste into an agent host's MCP settings

Exit codes: 0 all tasks finished / MOC passed, 4 MOC failed the check, 3 still
running, 1 error (including a server-side MOC error), 2 usage error.
The last line printed is always "RESULT " followed by a one-line JSON object,
except for mcp (stdout carries only MCP messages) and mcp-config (stdout is only
the JSON); both write their notes to stderr.
"""

import argparse
import errno
import glob
import hashlib
import http.client
import io
import json
import mimetypes
import os
import re
import ssl
import sys
import tempfile
import threading
import time
import traceback
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
import uuid
import zipfile
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

# Replaced with the server's public address when this file is downloaded from
# {server}/skill/install/lego.py.  The placeholder must appear on this line only.
DEFAULT_SERVER = "https://lego.groundrl.com"
PLACEHOLDER = "__LEGO_" + "SERVER__"  # split in two so the installer's replacement leaves it alone

VERSION = "2.1"
# Addresses older installs saved in user.json (HTTP and HTTPS on the server's IP). When the built-in address is
# configured, a user.json that still names one of these follows the built-in one instead (coord/api-skill.md 3.7).
LEGACY_SERVER_HOSTS = ("136.117.205.131",)
IMAGE_THREADS = 8
API_PREFIX = "/skill/v1"
MAX_PHOTOS = 30
MAX_PHOTO_BYTES = 25 * 1024 * 1024
CHUNK_FILES = 4
CHUNK_BYTES = 80 * 1024 * 1024
SCAN_WAIT_S = 480
TIMEOUT_S = 30
UPLOAD_TIMEOUT_S = 300
GET_RETRIES = 3
POLL_DEFAULT_S, POLL_MIN_S, POLL_MAX_S = 5.0, 1.0, 60.0
IDS_PER_QUERY = 100
ROWS_SHOWN = 10
TERMINAL = ("done", "failed")
ID_RE = re.compile(r"^[A-Za-z0-9_-]{1,64}$")
IMAGE_SUFFIXES = (".jpg", ".jpeg", ".png", ".webp", ".heic", ".heif")
MIME_TYPES = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png",
              ".webp": "image/webp", ".heic": "image/heic", ".heif": "image/heif"}
EXIT_OK, EXIT_ERROR, EXIT_USAGE, EXIT_PENDING, EXIT_MOC_FAILED = 0, 1, 2, 3, 4
# A failed upload request with one of these codes loses only that request's
# files; any other failure (quota, full queue, network, server error) stops the upload.
SKIP_CHUNK_CODES = ("bad_request", "bad_image", "no_photos", "photo_too_large", "too_many_photos",
                    "duplicate_photo")
HINTS = {
    "quota_user_daily": "the daily photo limit for this user ID is used up; it resets at 00:00 UTC",
    "quota_ip_ids": "this network has created too many new user IDs today; try again tomorrow",
    "queue_full": "the server's queue is full; try again later",
    "photo_too_large": "each photo must be at most 25 MB",
    "too_many_photos": "at most 30 photos per scan",
    "no_photos": "none of the files was a usable JPEG/PNG/WEBP/HEIC photo",
    "network": "check the network or proxy, and that the server address is right",
    "quota_moc_daily": "the daily MOC submission limit for this user ID is used up; it resets at 00:00 UTC",
    "moc_queue_full": "the server's MOC check queue is full; try again in a few minutes",
    "bad_model": "the model must be an LDraw text file of at most 1 MB with only 0 and 1 lines, no sub-models",
    "bad_parts": "the parts file must be an inventory in the parts.json format written by lego.py parts",
    "not_ready": "the server is still generating connector sheets; run moc guide again in a few minutes",
}

# Stage 2 (MOC check), coord/api-skill.md section 3.
MOC_WAIT_S = 300
MAX_MODEL_BYTES = 1024 * 1024
MAX_PARTS_BYTES = 2 * 1024 * 1024
MAX_TITLE_CHARS = 80
MAX_BRIEF_CHARS = 500
UNUSED_SHOWN = 8
CONNECTOR_BATCH = 400
NOT_READY_RETRY_S = 10.0  # on not_ready (503): retry every 10 s ...
NOT_READY_MAX_S = 180.0   # ... for at most 3 minutes over the whole command
ISSUE_PARTS_SHOWN = 12
MOC_TERMINAL = ("passed", "failed", "error")
PART_LINE_RE = re.compile(r"^[ \t]*1[ \t]")
UNSUPPORTED_RE = re.compile(r"^(\S+): not a supported part[ \t]*$", re.M)


class Fatal(Exception):
    """Ends the command with exit code 1; the message is shown to the user."""


class UsageError(Exception):
    """Ends the command with exit code 2."""


class ApiError(Exception):
    """A request failed: an HTTP error (status set) or a network failure (status None)."""

    def __init__(self, status, code, message, refused=False, body=b""):
        Exception.__init__(self, message)
        self.status = status
        self.code = code
        self.message = message
        self.refused = refused  # connection refused: nothing was sent, any method may be retried
        self.body = body        # the reply's body for an HTTP error (it may carry more detail than code/message)


def describe(err):
    text = "[{}] {}".format(err.code, err.message)
    hint = HINTS.get(err.code)
    return text + " (" + hint + ")" if hint else text


# ---------------------------------------------------------------- output

def say(*parts):
    print(*parts, flush=True)


def setup_stdout():
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(errors="replace")  # never die on a console that cannot show a character
        except (AttributeError, ValueError):
            pass


def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def elapsed(ctx):
    s = int(time.monotonic() - ctx["start"])
    return "{:02d}:{:02d}".format(s // 60, s % 60)


def add_unique(target, items):
    for item in items:
        if item not in target:
            target.append(item)


def valid_id(value):
    return isinstance(value, str) and bool(ID_RE.match(value))


def safe_name(value):
    return re.sub(r"[^A-Za-z0-9._-]", "_", str(value)).strip(".") or "_"


def python_cmd():
    return "python" if os.name == "nt" else "python3"


def script_cmd(args):
    return '{} "{}" {}'.format(python_cmd(), os.path.abspath(__file__), args)


# ---------------------------------------------------------------- local files

def home_dir():
    raw = os.environ.get("LEGO_PARTS_HOME", "").strip() or os.path.join("~", ".lego-parts")
    return Path(os.path.abspath(os.path.expanduser(raw)))


def parts_path(ctx):
    return ctx["home"] / "parts.json"


def tasks_dir(ctx):
    return ctx["home"] / "tasks"


def write_atomic(path, data):
    """Write bytes, or an object as pretty JSON, to path via a temp file and os.replace."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not isinstance(data, bytes):
        data = (json.dumps(data, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix="." + path.name + ".", suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        for attempt in range(5):
            try:
                os.replace(tmp, str(path))
                break
            except PermissionError:  # Windows: the target is briefly open in another process
                if attempt == 4:
                    raise
                time.sleep(0.2)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def read_json(path):
    """Parsed JSON at path, or None when the file does not exist. Raises ValueError/OSError."""
    try:
        with open(str(path), "r", encoding="utf-8-sig") as f:  # -sig: tolerate a BOM from Notepad
            return json.loads(f.read())
    except FileNotFoundError:
        return None


@contextmanager
def file_lock(path, timeout=15.0, stale=300.0):
    """Cross-platform exclusive lock: a <path>.lock file created with O_EXCL."""
    lock = str(path) + ".lock"
    Path(lock).parent.mkdir(parents=True, exist_ok=True)
    deadline = time.monotonic() + timeout
    while True:
        try:
            os.close(os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY))
            break
        except (FileExistsError, PermissionError):
            try:
                if time.time() - os.path.getmtime(lock) > stale:
                    os.unlink(lock)  # left behind by a killed process
                    continue
            except OSError:
                continue
            if time.monotonic() > deadline:
                raise Fatal("{} is held by another lego.py run; if none is running, delete that file".format(lock))
            time.sleep(0.05)
    try:
        yield
    finally:
        try:
            os.unlink(lock)
        except OSError:
            pass


def load_ids(path, key):
    """(IDs listed under key in the JSON file at path, file was readable). Missing or empty file = no IDs."""
    try:
        with open(str(path), "r", encoding="utf-8-sig") as f:
            text = f.read()
    except FileNotFoundError:
        return [], True
    except OSError:
        return [], False
    if not text.strip():
        return [], True
    try:
        data = json.loads(text)
    except ValueError:
        return [], False
    ids = data.get(key) if isinstance(data, dict) else data
    if not isinstance(ids, list):
        return [], False
    return list(dict.fromkeys(i for i in ids if valid_id(i))), True


def read_ids(ctx, path, key):
    ids, ok = load_ids(path, key)
    warned = ctx.setdefault("ids_warned", set())
    if not ok and str(path) not in warned:
        warned.add(str(path))
        say("WARNING: {} is unreadable; treating it as empty (the old file is kept as "
            "{}.corrupt when {} is next rewritten)".format(path, path.name, path.name))
    return ids


def update_ids(path, key, add=(), remove=()):
    """Add/remove IDs in a JSON ID list under a lock, so concurrent agents don't lose IDs."""
    with file_lock(path):
        ids, ok = load_ids(path, key)
        if not ok:
            try:
                write_atomic(path.with_name(path.name + ".corrupt"), path.read_bytes())
            except OSError:
                pass
        drop = set(remove)
        new = [i for i in ids if i not in drop]
        add_unique(new, [i for i in add if i not in drop])
        if new != ids or not ok or not path.exists():
            write_atomic(path, {key: new})


def load_pending(ctx):
    """(task IDs in pending.json, file was readable)."""
    return load_ids(ctx["home"] / "pending.json", "task_ids")


def read_pending(ctx):
    return read_ids(ctx, ctx["home"] / "pending.json", "task_ids")


def update_pending(ctx, add=(), remove=()):
    update_ids(ctx["home"] / "pending.json", "task_ids", add, remove)


def moc_dir(ctx):
    return ctx["home"] / "moc"


def moc_pending_path(ctx):
    return moc_dir(ctx) / "pending.json"


def read_moc_pending(ctx):
    return read_ids(ctx, moc_pending_path(ctx), "moc_ids")


def update_moc_pending(ctx, add=(), remove=()):
    update_ids(moc_pending_path(ctx), "moc_ids", add, remove)


def load_user(ctx):
    path = ctx["home"] / "user.json"
    try:
        data = read_json(path)
    except (OSError, ValueError) as e:
        raise Fatal("{} is unreadable ({}). It holds your user ID: repair it by hand, or move it away "
                    "to start a new, empty inventory.".format(path, e))
    if data is None:
        return None
    if not isinstance(data, dict) or not valid_id(data.get("user_id")):
        raise Fatal("{} has no valid user_id. Repair it by hand, or move it away to start a new, "
                    "empty inventory.".format(path))
    return data


def load_inventory(ctx, path=None):
    """(rows, total quantity, problem text or None) from the local parts.json (or path)."""
    path = Path(path) if path is not None else parts_path(ctx)
    try:
        data = read_json(path)
    except (OSError, ValueError) as e:
        return [], 0, "{} is not valid JSON ({})".format(path.name, e)
    if data is None:
        return [], 0, "no {} yet".format(path.name)
    items = data.get("items") if isinstance(data, dict) else None
    if not isinstance(items, list):
        return [], 0, "{} has no items list".format(path.name)
    rows = [r for r in items if isinstance(r, dict)]
    total = sum(r["quantity"] for r in rows
                if isinstance(r.get("quantity"), int) and not isinstance(r.get("quantity"), bool))
    return rows, total, None


# ---------------------------------------------------------------- server address and HTTP

def normalize_server(value):
    value = (value or "").strip().rstrip("/")
    if value.endswith(API_PREFIX):
        value = value[:-len(API_PREFIX)].rstrip("/")
    if value and "://" not in value and PLACEHOLDER not in value:
        value = "http://" + value
    return value


def is_legacy_server(url):
    """True for an address older installs saved: http:// or https:// on a LEGACY_SERVER_HOSTS IP, nothing else."""
    try:
        parts = urllib.parse.urlsplit(url)
        port = parts.port
    except ValueError:
        return False
    return (parts.scheme in ("http", "https") and (parts.hostname or "") in LEGACY_SERVER_HOSTS
            and port in (None, 80, 443) and parts.path in ("", "/") and not parts.query)


def resolve_server(user):
    """(server address, where it came from). LEGO_PARTS_SERVER always wins. A user.json address is kept, except
    that it follows a configured built-in address when it is an old one: the same host over http:// when the
    built-in one is https://, or a legacy IP address (http or https). It never moves from https:// to http://."""
    env = os.environ.get("LEGO_PARTS_SERVER", "").strip()
    if env:
        return normalize_server(env), "LEGO_PARTS_SERVER"
    if user and isinstance(user.get("server"), str) and user["server"].strip():
        stored, built_in = normalize_server(user["server"]), normalize_server(DEFAULT_SERVER)
        if server_configured(built_in) and stored != built_in:
            if (built_in.startswith("https://") and stored.startswith("http://")
                    and stored[len("http://"):] == built_in[len("https://"):]):
                return built_in, "built-in default (HTTPS; user.json still has the old http:// address)"
            downgrade = stored.startswith("https://") and built_in.startswith("http://")
            if is_legacy_server(stored) and not downgrade:
                return built_in, "built-in default (user.json still has the old address {})".format(stored)
        return stored, "user.json"
    return normalize_server(DEFAULT_SERVER), "built-in default"


def server_configured(server):
    return bool(server) and PLACEHOLDER not in server


def no_server_message():
    return ("No recognition server address is configured. Set the environment variable "
            "LEGO_PARTS_SERVER to the server's address, for example LEGO_PARTS_SERVER=http://203.0.113.7 "
            "(without /skill/v1), or download the client from <server>/skill/install/lego.py, which has "
            "the address built in.")


def bad_user_message(ctx):
    return ("The server {} does not recognise user ID {} (from {}). The results stored in {} belong to "
            "that ID, so no new ID was created. Check that the server address is right "
            "(LEGO_PARTS_SERVER, or \"server\" in user.json). To start over with a new, empty inventory, "
            "move {} somewhere else and run scan again.").format(
                ctx["server"], ctx["user_id"], ctx["home"] / "user.json", ctx["home"], ctx["home"])


def is_refused(reason):
    return isinstance(reason, ConnectionRefusedError) or getattr(reason, "errno", None) == errno.ECONNREFUSED


def error_from_response(status, raw, host=""):
    code = message = None
    try:
        err = json.loads(raw.decode("utf-8"))["error"]
        code, message = err.get("code"), err.get("message")
    except (ValueError, KeyError, TypeError, AttributeError):
        pass
    if code or message:
        return ApiError(status, code or "http_{}".format(status), message or "HTTP {} from the server".format(status))
    if status in (403, 407, 451):
        # The LEGO server always answers errors with its JSON envelope and never with these codes.
        return ApiError(status, "blocked", (
            "HTTP {0} for {1}, and the reply is not from the LEGO server: a sandbox, proxy or firewall on the way "
            "answered instead. Allow network access to {1} (or run this command outside the sandbox, or bypass "
            "the proxy for this host), then run the same command again. Do not call the server by hand to work "
            "around it: every extra new-ID request counts against a small daily limit.").format(status, host))
    return ApiError(status, "http_{}".format(status), "HTTP {} from the server".format(status))


def http_request(method, url, body=None, headers=None, timeout=TIMEOUT_S):
    """One HTTP request -> (status, body bytes). Raises ApiError for HTTP errors and network failures."""
    req = urllib.request.Request(url, data=body, method=method)
    req.add_header("User-Agent", "lego-moc-skill/" + VERSION)
    for key, value in (headers or {}).items():
        req.add_header(key, value)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as e:
        try:
            raw = e.read()
        except (OSError, http.client.HTTPException):
            raw = b""
        err = error_from_response(e.code, raw, urllib.parse.urlparse(url).netloc)
        err.body = raw
        raise err
    except (urllib.error.URLError, OSError, http.client.HTTPException) as e:
        reason = getattr(e, "reason", e)
        host = urllib.parse.urlparse(url).netloc
        if isinstance(reason, ssl.SSLCertVerificationError) or "CERTIFICATE_VERIFY_FAILED" in str(reason):
            raise ApiError(None, "tls", (
                "cannot verify the HTTPS certificate of {0}: {1}. Usually this Python has no root certificates "
                "(on macOS with a python.org install, run \"Install Certificates.command\" from its "
                "Applications folder), or a proxy on this computer intercepts HTTPS. Fix that and run the same "
                "command again. Only if the user accepts sending the photos unencrypted, set "
                "LEGO_PARTS_SERVER=http://{0}").format(host, reason))
        raise ApiError(None, "network", "cannot reach {}: {}".format(host, reason), refused=is_refused(reason))


def request_with_retry(method, url, body=None, headers=None, timeout=TIMEOUT_S, retry="get"):
    """retry="get": retry network errors and 5xx (idempotent requests only);
    retry="refused": retry only when the connection was refused, i.e. nothing was sent.
    A 503 not_ready is never retried here: the caller has its own, slower policy for it."""
    for attempt in range(GET_RETRIES + 1):
        try:
            return http_request(method, url, body, headers, timeout)
        except ApiError as e:
            if retry == "get":
                retryable = (e.status is None or e.status >= 500) and e.code != "not_ready"
            else:
                retryable = e.refused
            if not retryable or attempt == GET_RETRIES:
                raise
            time.sleep(2 ** attempt)  # 1, 2, 4 s


def api_raw(ctx, method, path, body=None, content_type=None, timeout=TIMEOUT_S, retry="get", auth=True,
            accept="application/json"):
    """Call {server}/skill/v1{path} -> (status, body bytes). A 401 becomes Fatal (never re-mint)."""
    headers = {"Accept": accept}
    if content_type:
        headers["Content-Type"] = content_type
    if auth:
        headers["X-Lego-User"] = ctx["user_id"]
    try:
        return request_with_retry(method, ctx["server"] + API_PREFIX + path, body, headers, timeout, retry)
    except ApiError as e:
        if auth and (e.status == 401 or e.code == "bad_user"):
            raise Fatal(bad_user_message(ctx))
        raise


def api(ctx, method, path, body=None, content_type=None, timeout=TIMEOUT_S, retry="get", auth=True):
    """Call {server}/skill/v1{path} and return the JSON object. A 401 becomes Fatal (never re-mint)."""
    status, raw = api_raw(ctx, method, path, body, content_type, timeout, retry, auth)
    try:
        data = json.loads(raw.decode("utf-8"))
    except ValueError:
        data = None
    if not isinstance(data, dict):
        raise ApiError(status, "bad_response", "the server sent an unexpected reply to {} {}".format(
            method, path.split("?")[0]))
    return data


# ---------------------------------------------------------------- user ID

def setup(ctx, need_server=True):
    ctx["user"] = load_user(ctx)
    ctx["user_id"] = ctx["user"]["user_id"] if ctx["user"] else None
    ctx["server"], ctx["server_source"] = resolve_server(ctx["user"])
    if need_server and not server_configured(ctx["server"]):
        raise Fatal(no_server_message())


def ensure_user(ctx):
    """Use the local user ID; create one on the server only when none exists locally.
    Returns True when this call created (and saved) a new ID."""
    if ctx["user_id"]:
        return False
    path = ctx["home"] / "user.json"
    created = False
    with file_lock(path, timeout=180.0):
        user = load_user(ctx)  # another agent may have created it meanwhile
        if user is None:
            say("No user ID on this computer yet; requesting one from", ctx["server"])
            resp = api(ctx, "POST", "/users", body=b"", retry="refused", auth=False)
            if not valid_id(resp.get("user_id")):
                raise Fatal("the server did not return a valid user ID")
            user = {"user_id": resp["user_id"], "server": ctx["server"],
                    "created_at": resp.get("created_at") or now_iso()}
            write_atomic(path, user)
            created = True
            say("New user ID {} saved to {}".format(user["user_id"], path))
    ctx["user"], ctx["user_id"] = user, user["user_id"]
    return created


# ---------------------------------------------------------------- scan: photos and upload

def expand_photos(args):
    """PHOTO arguments (files, folders, glob patterns) -> unique list of files. Raises UsageError."""
    found = []
    for arg in args:
        raw = os.path.expanduser(arg)
        path = Path(raw)
        if path.is_dir():
            found += sorted(p for p in path.iterdir()
                            if p.is_file() and not p.name.startswith(".") and p.suffix.lower() in IMAGE_SUFFIXES)
        elif path.is_file():
            found.append(path)
        elif any(ch in arg for ch in "*?["):  # Windows shells do not expand globs
            matches = sorted(Path(m) for m in glob.glob(raw) if os.path.isfile(m))
            if not matches:
                raise UsageError("no files match " + arg)
            found += matches
        else:
            raise UsageError("file not found: " + arg)
    unique, seen = [], set()
    for path in found:
        key = os.path.normcase(os.path.abspath(str(path)))
        if key not in seen:
            seen.add(key)
            unique.append(path)
    if not unique:
        raise UsageError("no photos found in: " + " ".join(args))
    if len(unique) > MAX_PHOTOS:
        raise UsageError("{} photos given; one scan takes at most {}. Split them over several scan "
                         "commands.".format(len(unique), MAX_PHOTOS))
    return unique


def make_chunks(sized):
    """Group (path, size) into upload requests of at most CHUNK_FILES files / CHUNK_BYTES bytes."""
    chunks, current, current_bytes = [], [], 0
    for path, size in sized:
        if current and (len(current) >= CHUNK_FILES or current_bytes + size > CHUNK_BYTES):
            chunks.append(current)
            current, current_bytes = [], 0
        current.append(path)
        current_bytes += size
    if current:
        chunks.append(current)
    return chunks


def mime_type(name):
    ext = os.path.splitext(name)[1].lower()
    return MIME_TYPES.get(ext) or mimetypes.guess_type(name)[0] or "application/octet-stream"


def multipart_form(fields):
    """multipart/form-data body from (field name, filename or None, content type or None, bytes)
    -> (body, content type). A field with a filename is sent as a file part."""
    boundary = "lego-moc-" + uuid.uuid4().hex
    while any(boundary.encode("ascii") in data for _, _, _, data in fields):
        boundary = "lego-moc-" + uuid.uuid4().hex
    sep = b"--" + boundary.encode("ascii")
    out = []
    for name, filename, content_type, data in fields:
        disposition = 'Content-Disposition: form-data; name="' + name + '"'
        if filename is not None:
            quoted = (unicodedata.normalize("NFC", filename)
                      .replace('"', "%22").replace("\r", "%0D").replace("\n", "%0A"))
            disposition += '; filename="' + quoted + '"'
        out += [sep, b"\r\n", (disposition + "\r\n").encode("utf-8")]
        if content_type:
            out.append(("Content-Type: " + content_type + "\r\n").encode("ascii"))
        out += [b"\r\n", data, b"\r\n"]
    out += [sep, b"--\r\n"]
    return b"".join(out), "multipart/form-data; boundary=" + boundary


def multipart_body(files):
    """multipart/form-data body with one "photos" field per (filename, bytes) -> (body, content type)."""
    return multipart_form([("photos", name, mime_type(name), data) for name, data in files])


def read_files(rep, paths):
    files = []
    for path in paths:
        try:
            files.append((path.name, path.read_bytes()))
        except OSError as e:
            rep["rejected"].append({"filename": path.name, "code": "unreadable", "message": str(e)})
    return files


def upload(ctx, rep, photos):
    sized = []
    for path in photos:
        try:
            size = path.stat().st_size
        except OSError as e:
            rep["rejected"].append({"filename": path.name, "code": "unreadable", "message": str(e)})
            continue
        if size > MAX_PHOTO_BYTES:
            rep["rejected"].append({"filename": path.name, "code": "photo_too_large",
                                    "message": "larger than 25 MB; not uploaded"})
        else:
            sized.append((path, size))
    chunks = make_chunks(sized)
    if chunks:
        say("Uploading {} photo(s) in {} request(s) to {} ...".format(len(sized), len(chunks), ctx["server"]))
    for n, chunk in enumerate(chunks, 1):
        label = "request {}/{}".format(n, len(chunks))
        files = read_files(rep, chunk)
        if not files:
            continue
        body, content_type = multipart_body(files)
        try:
            resp = api(ctx, "POST", "/scans", body, content_type, timeout=UPLOAD_TIMEOUT_S, retry="refused")
        except ApiError as e:
            names = [name for name, _ in files]
            if e.status in (400, 413) and e.code in SKIP_CHUNK_CODES:
                rep["rejected"] += chunk_rejections(e, names)
                say("  {}: all {} file(s) rejected: {}".format(label, len(names), describe(e)))
                continue
            upload_stopped(rep, label, e, names + [p.name for c in chunks[n:] for p in c])
            return
        record_scan(ctx, rep, resp, label)


def rejection(r):
    """One entry of a scan's rejected list, as reported. duplicate_photo keeps the first upload's task_id and
    its result summary (previous; null when the duplicate was in the same request)."""
    out = {"filename": r.get("filename"), "code": r.get("code"), "message": r.get("message")}
    if r.get("code") == "duplicate_photo":
        out["task_id"] = r.get("task_id") if valid_id(r.get("task_id")) else None
        out["previous"] = r.get("previous") if isinstance(r.get("previous"), dict) else None
    return out


def chunk_rejections(err, names):
    """Rejections for a request the server refused as a whole: the per-file reasons from the reply's rejected
    list when it has one (a server answers so since v2.0), the request's error for every other file."""
    try:
        listed = json.loads(err.body.decode("utf-8")).get("rejected")
    except (ValueError, AttributeError, UnicodeDecodeError):
        listed = None
    out, left = [], list(names)
    for r in listed if isinstance(listed, list) else []:
        if isinstance(r, dict) and r.get("filename") in left:
            left.remove(r["filename"])
            out.append(rejection(r))
    return out + [{"filename": name, "code": err.code, "message": err.message} for name in left]


def upload_stopped(rep, label, err, not_sent):
    rep["not_uploaded"] += not_sent
    msg = "upload stopped at {}: {}. {} photo(s) were not uploaded: {}.".format(
        label, describe(err), len(not_sent), ", ".join(not_sent))
    if rep["submitted"]:
        msg += " The {} photo(s) accepted before that are being processed.".format(len(rep["submitted"]))
    if (err.status is None and not err.refused) or (err.status or 0) >= 500 or err.code == "bad_response":
        msg += (" The server may still have received {}; if so, its parts will show up in parts.json later, "
                "and uploading those photos again would count them twice.".format(label))
    rep["errors"].append(msg)
    say("ERROR:", msg)


def record_scan(ctx, rep, resp, label):
    tasks = [t for t in resp.get("tasks") or [] if isinstance(t, dict) and valid_id(t.get("task_id"))]
    ids = [t["task_id"] for t in tasks]
    if ids:
        update_pending(ctx, add=ids)  # first: the IDs must survive anything that happens next
    for task in tasks:
        rep["tasks"][task["task_id"]] = task
    add_unique(rep["submitted"], ids)
    add_unique(rep["scope"], ids)
    rejected = [r for r in resp.get("rejected") or [] if isinstance(r, dict)]
    rep["rejected"] += [rejection(r) for r in rejected]
    if isinstance(resp.get("gpu"), dict):
        rep["gpu"] = resp["gpu"]
    if isinstance(resp.get("eta_s"), (int, float)) and not isinstance(resp.get("eta_s"), bool):
        rep["eta_s"] = max(rep.get("eta_s") or 0, resp["eta_s"])  # later requests queue behind earlier ones
    line = "  {}: {} accepted".format(label, len(ids))
    if rejected:
        line += ", {} rejected".format(len(rejected))
    if resp.get("queue_ahead") is not None:
        line += ", {} photo(s) ahead in the queue".format(resp["queue_ahead"])
    if resp.get("eta_s") is not None:
        line += ", estimate ~{} s".format(resp["eta_s"])
    say(line)


# ---------------------------------------------------------------- polling and collecting

def poll_seconds(value, default):
    try:
        seconds = float(value)
    except (TypeError, ValueError):
        return default
    return min(max(seconds, POLL_MIN_S), POLL_MAX_S)


def query_tasks(ctx, ids):
    """GET /tasks in batches -> (tasks by id, missing ids, gpu, seconds until next poll)."""
    tasks, missing, gpu, poll_s = {}, [], None, POLL_DEFAULT_S
    for i in range(0, len(ids), IDS_PER_QUERY):
        batch = ids[i:i + IDS_PER_QUERY]
        resp = api(ctx, "GET", "/tasks?ids=" + ",".join(batch))
        for task in resp.get("tasks") or []:
            if isinstance(task, dict) and task.get("task_id") in batch:
                tasks[task["task_id"]] = task
        missing += [m for m in resp.get("missing") or [] if m in batch]
        if isinstance(resp.get("gpu"), dict):
            gpu = resp["gpu"]
        poll_s = poll_seconds(resp.get("poll_after_s"), POLL_DEFAULT_S)
    return tasks, missing, gpu, poll_s


def forget_task(ctx, rep, tid):
    if tid in rep["missing"]:
        return
    update_pending(ctx, remove=[tid])
    rep["missing"].append(tid)
    msg = "task {} is unknown to the server for this user ID; removed it from pending.json".format(tid)
    rep["errors"].append(msg)
    say("ERROR:", msg)


def collect(ctx, rep, tid):
    """Fetch a finished task's full result into tasks/<id>.json and drop it from pending.json."""
    try:
        detail = api(ctx, "GET", "/tasks/" + tid)
    except ApiError as e:
        if e.status == 404:
            forget_task(ctx, rep, tid)
        else:
            say("WARNING: could not fetch the result of task {}: {}; will retry".format(tid, describe(e)))
        return
    if detail.get("status") not in TERMINAL:
        return
    write_atomic(tasks_dir(ctx) / (tid + ".json"), detail)
    update_pending(ctx, remove=[tid])
    rep["tasks"][tid] = detail
    add_unique(rep["collected"], [tid])
    add_unique(rep["scope"], [tid])


def poll_round(ctx, rep, open_ids, untracked):
    """One status query over open_ids plus pending.json; collects what finished. Returns poll interval."""
    ids = list(dict.fromkeys(open_ids + read_pending(ctx)))
    try:
        tasks, missing, gpu, poll_s = query_tasks(ctx, ids)
    except ApiError as e:
        if rep["poll_error"] != describe(e):
            say("WARNING: could not check task status:", describe(e))
        rep["poll_error"] = describe(e)
        return POLL_DEFAULT_S
    rep["poll_error"] = None
    if gpu:
        rep["gpu"] = gpu
    for tid in missing:
        forget_task(ctx, rep, tid)
    for tid, task in tasks.items():
        if tid not in rep["collected"]:
            rep["tasks"][tid] = task
        if task.get("status") in TERMINAL:
            collect(ctx, rep, tid)
        elif tid in untracked:  # named on the command line but not in pending.json: track it from now on
            update_pending(ctx, add=[tid])
            untracked.discard(tid)
    return poll_s


def still_open(rep, ids):
    return [t for t in ids if t not in rep["collected"] and t not in rep["missing"]]


def track(ctx, rep, watch, wait_s):
    """Poll until every task in watch is collected or wait_s seconds have passed."""
    add_unique(rep["scope"], watch)
    untracked = set(watch) - set(read_pending(ctx))
    deadline = time.monotonic() + wait_s
    shown = {}
    while still_open(rep, watch):
        poll_s = poll_round(ctx, rep, still_open(rep, watch), untracked)
        if wait_s > 0:
            show_progress(ctx, rep, watch, shown)
        left = deadline - time.monotonic()
        if not still_open(rep, watch) or left <= 0:
            break
        time.sleep(min(poll_s, left))


def show_progress(ctx, rep, watch, shown):
    """Print one line, only when a status, queue position or the GPU state changed."""
    tasks = [rep["tasks"].get(t, {"task_id": t}) for t in watch if t not in rep["missing"]]
    gpu = rep.get("gpu") or {}
    signature = (tuple((t.get("task_id"), t.get("status"), t.get("queue_ahead")) for t in tasks), gpu.get("state"))
    if signature == shown.get("signature"):
        return
    shown["signature"] = signature
    finished = [t for t in tasks if t.get("status") in TERMINAL]
    failed = [t for t in finished if t.get("status") == "failed"]
    bits = ["[{}] {}/{} done".format(elapsed(ctx), len(finished), len(tasks))
            + (" ({} failed)".format(len(failed)) if failed else "")]
    active = [t for t in tasks if t.get("status") not in TERMINAL + ("queued", None)]
    for task in active[:2]:
        text = "{} {}".format(task.get("filename") or task.get("task_id"), task.get("status"))
        progress = task.get("progress")
        if isinstance(progress, dict) and progress.get("total"):
            text += " {}/{}".format(progress.get("done"), progress.get("total"))
        bits.append(text)
    if len(active) > 2:
        bits.append("+{} more in progress".format(len(active) - 2))
    queued = [t for t in tasks if t.get("status") == "queued"]
    if queued:
        ahead = [t.get("queue_ahead") for t in queued if isinstance(t.get("queue_ahead"), int)]
        bits.append("{} queued".format(len(queued)) + (" ({} ahead)".format(min(ahead)) if ahead else ""))
    if gpu.get("state"):
        bits.append("GPU {}".format(gpu["state"]) + (" ~{}s".format(gpu["eta_s"]) if gpu.get("eta_s") else ""))
    say(" · ".join(bits))


# ---------------------------------------------------------------- parts.json and images

def refresh_parts(ctx, rep, images):
    data = api(ctx, "GET", "/parts")
    if not isinstance(data.get("items"), list):
        raise ApiError(200, "bad_response", "GET /parts returned no items list")
    data["fetched_at"] = now_iso()
    data["local_pending_tasks"] = len(read_pending(ctx))
    if images:
        download_images(ctx, rep, data["items"])
    path = parts_path(ctx)
    try:
        old = path.read_bytes()
    except FileNotFoundError:
        old = None
    if old is not None and parts_differ(old, data):
        write_atomic(path.with_name("parts.json.bak"), old)
        say("Previous parts.json kept as", path.with_name("parts.json.bak"))
    write_atomic(path, data)
    rep["parts_refreshed"] = True
    if isinstance(data.get("inventory_url"), str):
        say("Inventory page with pictures (give this link to the user):", data["inventory_url"])
    sheet = path.with_name("inventory.png")
    try:                                   # one overview picture of the inventory, for chats that can show a local image
        _status, raw = api_raw(ctx, "GET", "/parts/sheet.png", timeout=UPLOAD_TIMEOUT_S, accept="image/png")
        if raw[:8] == b"\x89PNG\r\n\x1a\n":
            write_atomic(sheet, raw)
            say("Inventory overview picture (show this image to the user):", sheet)
    except (ApiError, OSError):
        pass                               # an older server or a failed download: the page link still works
    rep["server_pending"] = data.get("pending_tasks")


def parts_differ(old_bytes, new):
    try:
        old = json.loads(old_bytes.decode("utf-8-sig"))
    except ValueError:
        return True
    if not isinstance(old, dict):
        return True
    return ({k: v for k, v in old.items() if k != "fetched_at"}
            != {k: v for k, v in new.items() if k != "fetched_at"})


def ldraw_image_name(row, url):
    part, color = row.get("ldraw_part"), row.get("ldraw_color")
    if part is None or color is None:
        match = re.search(r"/ldraw/([^/]+)/([^/]+?)\.png$", urllib.parse.urlparse(url).path)
        if not match:
            return hashlib.sha1(url.encode("utf-8")).hexdigest()[:16] + ".png"
        part, color = urllib.parse.unquote(match.group(1)), match.group(2)
    return "{}_{}.png".format(safe_name(part), safe_name(color))


def crop_image_name(row, url):
    match = re.search(r"/tasks/([^/]+)/crops/([^/]+?)\.[A-Za-z0-9]+$", urllib.parse.urlparse(url).path)
    if match:
        return "{}_{}.jpg".format(safe_name(match.group(1)), safe_name(match.group(2)))
    return hashlib.sha1(url.encode("utf-8")).hexdigest()[:16] + ".jpg"


def fetch_image(ctx, rep, url, folder, name_for):
    """Download url into folder (skipped when present) -> absolute path, or None on any failure."""
    if not isinstance(url, str) or not url:
        return None
    url = urllib.parse.urljoin(ctx["server"] + "/", url)
    if urllib.parse.urlparse(url).scheme not in ("http", "https"):
        return None
    dest = folder / name_for(url)
    if dest.is_file() and dest.stat().st_size > 0:
        if str(dest) not in ctx.get("_bundled", ()):   # those were counted as downloaded already
            rep["images"]["present"] += 1
        return str(dest)
    try:
        status, body = request_with_retry("GET", url)  # media needs no user header
        if not body:
            raise ApiError(status, "empty", "empty file")
        write_atomic(dest, body)
    except (ApiError, OSError) as e:
        rep["images"]["failed"].append("{} ({})".format(url, describe(e) if isinstance(e, ApiError) else e))
        return None
    rep["images"]["downloaded"] += 1
    return str(dest)


def fetch_bundle(ctx, rep, jobs):
    """Get all missing pictures in one request (images.zip); whatever it lacks is then fetched one by one.
    Only entries whose names this client computed itself are written, so the archive cannot place files elsewhere."""
    wanted = {}
    for row, _field, url, folder, namer in jobs:
        if isinstance(url, str) and url:
            dest = folder / namer(row, urllib.parse.urljoin(ctx["server"] + "/", url))
            if not (dest.is_file() and dest.stat().st_size > 0):
                wanted["{}/{}".format(folder.name, dest.name)] = dest
    if len(wanted) < 8:
        return
    try:
        _status, raw = api_raw(ctx, "GET", "/parts/images.zip", timeout=UPLOAD_TIMEOUT_S, accept="application/zip")
        with zipfile.ZipFile(io.BytesIO(raw)) as z:
            for name in z.namelist():
                dest = wanted.get(name)
                if dest is not None and 0 < z.getinfo(name).file_size <= 20 * 1024 * 1024:
                    write_atomic(dest, z.read(name))
                    rep["images"]["downloaded"] += 1
                    ctx.setdefault("_bundled", set()).add(str(dest))
    except (ApiError, Fatal, OSError, zipfile.BadZipFile, ValueError):
        pass  # an older server, or a broken download: fall back to one request per picture


def download_images(ctx, rep, items):
    """Download both pictures of every row, IMAGE_THREADS at a time (an inventory can have over a thousand)."""
    root = ctx["home"] / "images"
    jobs = []
    for row in items:
        if isinstance(row, dict):
            jobs.append((row, "local_ldraw_image", row.get("ldraw_image_url"), root / "ldraw", ldraw_image_name))
            jobs.append((row, "local_crop", row.get("crop_url"), root / "crops", crop_image_name))
    fetch_bundle(ctx, rep, jobs)
    lock, position = threading.Lock(), [0]

    def work():
        while True:
            with lock:
                if position[0] >= len(jobs):
                    return
                row, field, url, folder, namer = jobs[position[0]]
                position[0] += 1
            local = {"images": {"downloaded": 0, "present": 0, "failed": []}}
            path = fetch_image(ctx, local, url, folder, lambda u, r=row, f=namer: f(r, u))
            with lock:
                row[field] = path
                for key in ("downloaded", "present"):
                    rep["images"][key] += local["images"][key]
                rep["images"]["failed"].extend(local["images"]["failed"])

    threads = [threading.Thread(target=work, daemon=True) for _ in range(min(IMAGE_THREADS, len(jobs)))]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    info = rep["images"]
    say("Images: {} downloaded, {} already present, {} failed (in {})".format(
        info["downloaded"], info["present"], len(info["failed"]), root))
    for failure in info["failed"][:3]:
        say("WARNING: image not downloaded:", failure)
    if len(info["failed"]) > 3:
        say("WARNING: ... and {} more images not downloaded".format(len(info["failed"]) - 3))


# ---------------------------------------------------------------- summary and RESULT

def new_report(command):
    return {"command": command, "scope": [], "tasks": {}, "collected": [], "missing": [], "submitted": [],
            "rejected": [], "not_uploaded": [], "errors": [], "poll_error": None, "gpu": None, "eta_s": None,
            "parts_refreshed": False, "server_pending": None,
            "images": {"downloaded": 0, "present": 0, "failed": []},
            "moc": {"targets": [], "guide_file": None, "connectors_file": None, "connector_parts": None,
                    "connector_requests": 0, "unsupported_parts": []}}


def classify(rep):
    done = [t for t in rep["collected"] if rep["tasks"][t].get("status") == "done"]
    failed = [t for t in rep["collected"] if rep["tasks"][t].get("status") == "failed"]
    return done, failed, still_open(rep, rep["scope"])


def task_messages(rep, field, status):
    out = []
    for tid in rep["collected"]:
        task = rep["tasks"][tid]
        info = task.get(field)
        if task.get("status") == status and isinstance(info, dict):
            out.append({"task_id": tid, "filename": task.get("filename"),
                        "code": info.get("code"), "message": info.get("message")})
    return out


def task_line(rep, tid):
    task = rep["tasks"].get(tid, {})
    status = task.get("status") or "not checked"
    detail = ""
    if tid in rep["collected"] and status == "done":
        detail = "{} pieces found, {} accepted".format(task.get("pieces_found"), task.get("pieces_accepted"))
    elif tid not in rep["collected"]:
        progress = task.get("progress")
        if isinstance(progress, dict) and progress.get("total"):
            detail = "{}/{}".format(progress.get("done"), progress.get("total"))
        elif status == "queued" and task.get("queue_ahead") is not None:
            detail = "{} ahead in queue".format(task["queue_ahead"])
        if status in TERMINAL:
            status += " (result not fetched yet)"
    lines = ["  " + "  ".join(s for s in ("{:<13}".format(status), task.get("filename") or "?", detail,
                                         "[{}]".format(tid)) if s)]
    for field, label in (("notice", "NOTICE"), ("error", "ERROR")):
        info = task.get(field)
        if tid in rep["collected"] and isinstance(info, dict):
            lines.append("      {} [{}] {}".format(label, info.get("code"), info.get("message")))
    return lines


def previous_text(prev):
    """The summary of a duplicate photo's first upload (rejected[].previous) as one phrase."""
    text = "task {}, {}".format(prev.get("task_id") or "?", prev.get("status") or "status unknown")
    if prev.get("pieces_found") is not None:
        text += ", {} pieces found, {} accepted".format(prev.get("pieces_found"), prev.get("pieces_accepted"))
    notice = prev.get("notice")
    if isinstance(notice, dict) and notice.get("message"):
        text += "; notice [{}] {}".format(notice.get("code"), notice["message"])
    return text


def row_line(row):
    flags = ""
    if row.get("low_confidence"):
        flags += " [low confidence]"
    if row.get("designable") is False:
        flags += " [not designable]"
    return "  {:>4} x {:<18} {} ({}){}".format(row.get("quantity"), str(row.get("key")), row.get("name") or "?",
                                               row.get("color_name") or "colour ?", flags)


def print_summary(ctx, rep):
    done, failed, pending = classify(rep)
    say("")
    say("== Summary ==")
    if rep["scope"]:
        say("Tasks: {} done, {} failed, {} still running".format(len(done), len(failed), len(pending)))
        for tid in rep["scope"]:
            if tid not in rep["missing"]:
                for line in task_line(rep, tid):
                    say(line)
    for r in rep["rejected"]:
        say("  REJECTED {}: [{}] {}".format(r.get("filename"), r.get("code"), r.get("message")))
        if r.get("previous"):
            say("      first upload: " + previous_text(r["previous"]))
    if rep["not_uploaded"]:
        say("  NOT UPLOADED:", ", ".join(rep["not_uploaded"]))
    rows, total, problem = load_inventory(ctx)
    if problem:
        say("Inventory:", problem)
    else:
        say("Inventory ({}): {} pieces in {} rows; {} low-confidence, {} not designable".format(
            "refreshed from server" if rep["parts_refreshed"] else "local file, not refreshed", total, len(rows),
            sum(1 for r in rows if r.get("low_confidence")), sum(1 for r in rows if r.get("designable") is False)))
        for row in rows[:ROWS_SHOWN]:
            say(row_line(row))
        if len(rows) > ROWS_SHOWN:
            say("  ... {} more rows in parts.json".format(len(rows) - ROWS_SHOWN))
    if isinstance(rep["server_pending"], int) and rep["server_pending"] > len(pending):
        say("Note: the server reports {} unfinished task(s) for this user ID.".format(rep["server_pending"]))
    say("Files:")
    say("  parts.json:", parts_path(ctx))
    say("  tasks dir: ", tasks_dir(ctx))
    if rep["errors"]:
        say("FINISHED WITH ERRORS: see the ERROR lines above.")
    if pending:
        say("STILL RUNNING: {} of {} task(s) not finished; parts.json is incomplete. Run: {}".format(
            len(pending), len(rep["scope"]), script_cmd("status --wait 300")))
    elif rep["scope"] and not rep["errors"]:
        say("All tasks finished.")


def exit_code(rep):
    if rep["errors"]:
        return EXIT_ERROR
    return EXIT_PENDING if classify(rep)[2] else EXIT_OK


def emit_result(ctx, rep, code):
    try:
        if (rep.get("command") or "").startswith("moc"):
            obj = moc_result(ctx, rep, code)
        else:
            obj = scan_result(ctx, rep, code)
    except Exception as e:  # the RESULT line must always be printed
        obj = {"exit_code": code, "errors": rep.get("errors", []) + ["could not build RESULT: {}".format(e)]}
    print("RESULT " + json.dumps(obj, ensure_ascii=True, separators=(",", ":")), flush=True)


def inventory_url(ctx):
    try:
        url = json.loads(parts_path(ctx).read_text(encoding="utf-8-sig")).get("inventory_url")
    except (OSError, ValueError, AttributeError):
        return None
    return url if isinstance(url, str) else None


def scan_result(ctx, rep, code):
    done, failed, pending = classify(rep)
    rows, total, _ = load_inventory(ctx)
    return {
        "exit_code": code, "command": rep["command"],
        "user_id": ctx.get("user_id"), "server": ctx.get("server"),
        "done": len(done), "failed": len(failed), "pending": len(pending),
        "pending_task_ids": pending, "task_ids": rep["scope"], "missing_task_ids": rep["missing"],
        "local_pending_tasks": len(load_pending(ctx)[0]), "server_pending_tasks": rep["server_pending"],
        "rejected": rep["rejected"], "not_uploaded": rep["not_uploaded"],
        "notices": task_messages(rep, "notice", "done"), "task_errors": task_messages(rep, "error", "failed"),
        "errors": rep["errors"],
        "parts_file": str(parts_path(ctx)), "parts_refreshed": rep["parts_refreshed"],
        "tasks_dir": str(tasks_dir(ctx)), "home": str(ctx["home"]),
        "total_quantity": total, "distinct_parts": len(rows), "inventory_url": inventory_url(ctx),
        "inventory_image": str(parts_path(ctx).with_name("inventory.png")) if parts_path(ctx).with_name("inventory.png").is_file() else None,
    }


# ---------------------------------------------------------------- moc: local input files

def arg_path(text):
    return Path(os.path.abspath(os.path.expanduser(text)))


def positive_int(value):
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


def num(value):
    """A coordinate as short text: 40.0 -> "40", -12.5 -> "-12.5"."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return "?"
    if float(value).is_integer():
        return str(int(value))
    return ("%.3f" % value).rstrip("0").rstrip(".")


def read_model(arg):
    """Check the model file named on the command line -> (path, bytes to send, number of part lines).
    Problems are usage errors: the file is the command's argument."""
    path = arg_path(arg)
    if not path.is_file():
        raise UsageError("model file not found: " + arg)
    size = path.stat().st_size
    if size > MAX_MODEL_BYTES:
        raise UsageError("{} is {} bytes; a model file may be at most 1 MB ({} bytes)".format(
            arg, size, MAX_MODEL_BYTES))
    try:
        data = path.read_bytes()
    except OSError as e:
        raise UsageError("cannot read {}: {}".format(arg, e))
    if data.startswith(b"\xef\xbb\xbf"):
        data = data[3:]  # a BOM would hide a "1" at the start of the first line
    try:
        if b"\x00" in data:
            raise ValueError("NUL byte")
        text = data.decode("utf-8")
    except ValueError:
        raise UsageError("{} is not a text file; an LDraw model is plain UTF-8 text".format(arg))
    count = sum(1 for line in text.splitlines() if PART_LINE_RE.match(line))
    if not count:
        raise UsageError("{} has no part lines. Each part is one line: "
                         "1 <colour> x y z a b c d e f g h i <part>.dat".format(arg))
    return path, data, count


def read_design(arg):
    path = arg_path(arg)
    if not path.is_file():
        raise UsageError("design file not found: " + arg)
    try:
        data = read_json(path)
    except (OSError, ValueError) as e:
        raise UsageError("{} is not valid JSON ({})".format(arg, e))
    if not isinstance(data, dict):
        raise UsageError('{} must be a JSON object, e.g. {{"title": "...", "motions": [...]}}'.format(arg))
    return json.dumps(data, ensure_ascii=False).encode("utf-8")


def read_parts_upload(ctx, arg):
    """The inventory sent with a model -> JSON bytes, without the local-only local_* fields.
    A file named with --parts-file is an argument (usage error); the default parts.json is local state (error)."""
    explicit = arg is not None
    path = arg_path(arg) if explicit else parts_path(ctx)
    problem = UsageError if explicit else Fatal
    if not path.is_file():
        if explicit:
            raise UsageError("parts file not found: " + arg)
        raise Fatal("no inventory at {}. A model is checked against the parts you own: scan them first ({}), "
                    "or pass --parts-file.".format(path, script_cmd("scan PHOTO...")))
    try:
        data = read_json(path)
    except (OSError, ValueError) as e:
        raise problem("{} is not valid JSON ({})".format(path, e))
    items = data.get("items") if isinstance(data, dict) else None
    if not isinstance(items, list):
        raise problem("{} has no items list, so it is not an inventory".format(path))
    data = dict(data, items=[{k: v for k, v in row.items() if not str(k).startswith("local_")}
                             if isinstance(row, dict) else row for row in items])
    body = json.dumps(data, ensure_ascii=False).encode("utf-8")
    if len(body) > MAX_PARTS_BYTES:
        raise problem("{} is larger than 2 MB, the server's limit for an inventory".format(path))
    return body


# ---------------------------------------------------------------- moc: guide and connector sheets

def not_ready_retry(ctx, call):
    """call() -> its result. While the server answers 503 not_ready, retry every NOT_READY_RETRY_S
    seconds, for at most NOT_READY_MAX_S seconds counted over the whole command."""
    while True:
        try:
            return call()
        except ApiError as e:
            if e.code != "not_ready":
                raise
            now = time.monotonic()
            since = ctx.setdefault("not_ready_since", now)
            if now - since >= NOT_READY_MAX_S:
                raise ApiError(e.status, e.code, "{} (still not ready after {} s of retrying)".format(
                    e.message, int(NOT_READY_MAX_S)))
            say("[{}] the server is not ready yet ({}); retrying in {} s, for up to {} s".format(
                elapsed(ctx), e.message, num(NOT_READY_RETRY_S), int(NOT_READY_MAX_S)))
            time.sleep(NOT_READY_RETRY_S)


def connector_part_ids(rows):
    """Distinct LDraw part numbers of the inventory rows, in inventory order; rows without one are skipped."""
    ids = []
    for row in rows:
        part = row.get("ldraw_part")
        if isinstance(part, int) and not isinstance(part, bool):
            part = str(part)
        if isinstance(part, str) and part.strip():
            ids.append(part.strip())
    return list(dict.fromkeys(ids))


def cmd_moc_guide(ctx, rep, args):
    m = rep["moc"]
    inventory = arg_path(args.parts_file) if args.parts_file is not None else parts_path(ctx)
    named = [p.strip().lower() for p in (args.parts or "").replace(";", ",").split(",") if p.strip()]
    if named and args.parts_file is not None:
        raise UsageError("use --parts or --parts-file, not both")
    if len(named) > 400:
        raise UsageError("--parts names {} parts; at most 400".format(len(named)))
    if args.parts_file is not None and not inventory.is_file():
        raise UsageError("parts file not found: " + args.parts_file)
    setup(ctx)
    folder = moc_dir(ctx)
    _, guide = not_ready_retry(ctx, lambda: api_raw(ctx, "GET", "/moc/guide", auth=False,
                                                    accept="text/markdown, text/plain, */*"))
    if not guide.strip():
        raise ApiError(200, "bad_response", "the server sent an empty design guide")
    write_atomic(folder / "DESIGN_GUIDE.md", guide)
    m["guide_file"] = str(folder / "DESIGN_GUIDE.md")
    say("Design guide saved to", m["guide_file"])
    if named:   # free build: sheets of the parts named on the command line, no inventory needed
        rows, problem = [{"ldraw_part": p[:-4] if p.endswith(".dat") else p} for p in named], None
    else:
        rows, _, problem = load_inventory(ctx, inventory)
    ids = connector_part_ids(rows)
    if not problem and not ids:
        problem = "{} has no rows with an LDraw part number".format(inventory.name)
    if problem:
        msg = ("connectors.txt was not fetched: connector sheets are fetched for the parts in an inventory, and "
               "{} ({}). Scan your parts first ({}), or pass --parts-file. For a free build (not limited to the "
               "inventory) name the parts: {}.".format(
                   problem, inventory, script_cmd("scan PHOTO..."), script_cmd("moc guide --parts 3001,3020")))
        rep["errors"].append(msg)
        say("ERROR:", msg)
        return EXIT_ERROR
    batches = [ids[i:i + CONNECTOR_BATCH] for i in range(0, len(ids), CONNECTOR_BATCH)]
    say("Fetching connector sheets for {} distinct part(s) in {} request(s) ...".format(len(ids), len(batches)))
    texts = []
    for n, batch in enumerate(batches, 1):
        body = json.dumps({"parts": batch}).encode("utf-8")
        try:
            _, raw = not_ready_retry(ctx, lambda b=body: api_raw(
                ctx, "POST", "/moc/connectors", b, "application/json", auth=False, accept="text/plain, */*"))
        except ApiError as e:
            raise Fatal("could not fetch connector sheets (request {}/{}): {}. connectors.txt was not "
                        "updated.".format(n, len(batches), describe(e)))
        m["connector_requests"] += 1
        texts.append(raw.decode("utf-8", "replace").strip("\r\n"))
    text = "\n\n".join(t for t in texts if t) + "\n"
    path = folder / "connectors.txt"
    write_atomic(path, text.encode("utf-8"))
    unsupported = list(dict.fromkeys(UNSUPPORTED_RE.findall(text)))
    m.update(connectors_file=str(path), connector_parts=len(ids), unsupported_parts=unsupported)
    say("Connector sheets for {} part(s) saved to {}".format(len(ids) - len(unsupported), path))
    if unsupported:
        say("WARNING: {} part(s) are not supported for design (no connector sheet; don't build "
            "with them): {}{}".format(len(unsupported), ", ".join(unsupported[:20]),
                                      " ..." if len(unsupported) > 20 else ""))
    if named:
        say("Next: read both files, write an LDraw model (free build: any supported part, any colour), then run: "
            + script_cmd("moc submit model.ldr --mode free"))
        return EXIT_OK
    say("Next: read both files, write an LDraw model using only designable rows of {} (at most `quantity` of "
        "each), then run: {}".format(inventory, script_cmd("moc submit model.ldr" + (
            ' --parts-file "{}"'.format(inventory) if args.parts_file is not None else ""))))
    return EXIT_OK


def cmd_moc_find(ctx, rep, args):
    """Supported parts whose LDraw name has every word (or whose number starts with it): for a free build."""
    query = " ".join(args.words).strip()
    if not query or len(query) > 80:
        raise UsageError("give 1-80 characters: words from the part name (e.g. slope 45 2 x 2) or a part number")
    setup(ctx)
    path = "/moc/parts?" + urllib.parse.urlencode({"q": query, "offset": args.offset, "limit": 100})
    data = not_ready_retry(ctx, lambda: api(ctx, "GET", path, auth=False))
    parts = [p for p in (data.get("parts") or []) if isinstance(p, dict)]
    say("{} supported part(s) match '{}'{}".format(data.get("total", len(parts)), query,
                                                  "; showing {}-{}".format(args.offset + 1, args.offset + len(parts))
                                                  if parts else ""))
    for p in parts:
        say("{} | {}".format(p.get("ldraw_part"), p.get("name") or ""))
    if parts and args.offset + len(parts) < (data.get("total") or 0):
        say("More: add --offset {}, or add a word to narrow it.".format(args.offset + len(parts)))
    if parts:
        say("Next: fetch the connector sheets of the parts you choose: " + script_cmd("moc guide --parts 3001,3020"))
    rep["moc"]["found_parts"] = [p.get("ldraw_part") for p in parts]
    return EXIT_OK


# ---------------------------------------------------------------- moc: submit and track

def new_target(moc_id, version=None, data=None, pinned=False, poll_s=POLL_DEFAULT_S):
    """One MOC being checked. pinned: poll exactly this version (submit) rather than the latest (status)."""
    return {"moc_id": moc_id, "version": version, "pinned": pinned, "data": data, "done": False,
            "missing": False, "untracked": False, "poll_error": None, "poll_s": poll_s,
            "report_file": None, "model_file": None}


def submit_failed(err, moc_id):
    if err.status == 404 and moc_id:
        return ("MOC {} is not one of this user ID's MOCs ({}). Check the ID, or leave out --moc to start "
                "a new MOC.".format(moc_id, describe(err)))
    if (err.status is None and not err.refused) or (err.status or 0) >= 500 or err.code == "bad_response":
        msg = "submitting failed: {}. The server may still have received the model".format(describe(err))
        return msg + ("; check with {} before submitting again".format(script_cmd("moc status " + moc_id))
                      if moc_id else "; submitting it again may create a second MOC")
    return "the model was not accepted: " + describe(err)


def cmd_moc_submit(ctx, rep, args):
    if args.moc is not None and not valid_id(args.moc):
        raise UsageError("not a MOC ID: " + args.moc)
    title = args.title.strip() if args.title is not None else None
    if title and len(title) > MAX_TITLE_CHARS:
        raise UsageError("--title has {} characters; at most {}".format(len(title), MAX_TITLE_CHARS))
    brief = args.brief.strip() if args.brief is not None else None
    if brief and len(brief) > MAX_BRIEF_CHARS:
        raise UsageError("--brief has {} characters; at most {}".format(len(brief), MAX_BRIEF_CHARS))
    model, model_bytes, part_lines = read_model(args.model)
    design = read_design(args.design) if args.design is not None else None
    free = args.mode == "free"
    if free and args.parts_file is not None:
        raise UsageError("--mode free is not checked against an inventory: leave out --parts-file")
    # no mode and no local inventory: the server decides (its own inventory of this ID; free when that is empty)
    send_parts = not free and (args.mode == "inventory" or args.parts_file is not None or parts_path(ctx).is_file())
    parts_body = read_parts_upload(ctx, args.parts_file) if send_parts else None
    setup(ctx)
    ensure_user(ctx)
    fields = [("model", model.name, "text/plain; charset=utf-8", model_bytes)]
    if parts_body is not None:
        fields.append(("parts", "parts.json", "application/json", parts_body))
    if args.mode:
        fields.append(("mode", None, None, args.mode.encode("ascii")))
    if design is not None:
        fields.append(("design", "design.json", "application/json", design))
    if args.moc:
        fields.append(("moc_id", None, None, args.moc.encode("ascii")))
    if title:
        fields.append(("title", None, None, title.encode("utf-8")))
    if brief:
        fields.append(("brief", None, None, brief.encode("utf-8")))
    body, content_type = multipart_form(fields)
    say("Submitting {} ({} part line(s)){} to {} ...".format(
        model, part_lines, " as a new version of MOC " + args.moc if args.moc else "", ctx["server"]))
    try:
        resp = api(ctx, "POST", "/mocs", body, content_type, timeout=UPLOAD_TIMEOUT_S, retry="refused")
    except ApiError as e:
        raise Fatal(submit_failed(e, args.moc))
    moc_id, version = resp.get("moc_id"), resp.get("version")
    if not valid_id(moc_id):
        raise Fatal("the server answered the submission without a valid MOC ID")
    target = new_target(moc_id, version if positive_int(version) else None, resp, pinned=True,
                        poll_s=poll_seconds(resp.get("poll_after_s"), POLL_DEFAULT_S))
    target["resubmit_model"] = str(model)
    rep["moc"]["targets"].append(target)  # so that RESULT names the MOC whatever happens next
    update_moc_pending(ctx, add=[moc_id])  # first on disk: the ID must survive anything that happens next
    if target["version"] is None:
        raise Fatal("the server accepted the model as MOC {} but sent no version number; check it with {}".format(
            moc_id, script_cmd("moc status " + moc_id)))
    copy = moc_dir(ctx) / moc_id / "v{}.ldr".format(version)
    write_atomic(copy, model_bytes)
    target["model_file"] = str(copy)
    line = "Accepted as MOC {} version {}{}".format(
        moc_id, version, " (free build: not checked against the inventory)" if resp.get("mode") == "free" else "")
    if resp.get("queue_ahead") is not None:
        line += ", {} ahead in the queue".format(resp["queue_ahead"])
    if resp.get("eta_s") is not None:
        line += ", estimate ~{} s".format(resp["eta_s"])
    say(line)
    say("Copy of the submitted file (the report's line numbers refer to it):", copy)
    if args.no_wait:
        say("Not waiting (--no-wait). The MOC ID is saved in", moc_pending_path(ctx))
    else:
        say("Waiting for the check (up to {} s; stopping early is safe, the MOC ID is saved in "
            "moc/pending.json) ...".format(args.wait))
        track_mocs(ctx, rep, args.wait)
    finish_moc(ctx, rep)
    return moc_exit_code(rep)


def cmd_moc_status(ctx, rep, args):
    if args.moc_id is not None and not valid_id(args.moc_id):
        raise UsageError("not a MOC ID: " + args.moc_id)
    setup(ctx)
    pending = read_moc_pending(ctx)
    ids = [args.moc_id] if args.moc_id is not None else pending
    if not ctx["user_id"]:
        if ids:
            raise Fatal("{} is missing, so MOC {} cannot be checked: a MOC belongs to the user ID that "
                        "submitted it".format(ctx["home"] / "user.json", ", ".join(ids)))
        say("No user ID on this computer yet ({}), so there is no MOC to check.".format(ctx["home"] / "user.json"))
        return EXIT_OK
    if not ids:
        say("No pending MOC submissions; nothing was checked.")
        show_recent_mocs(ctx)
        return EXIT_OK
    for moc_id in ids:
        target = new_target(moc_id)
        target["untracked"] = moc_id not in pending
        rep["moc"]["targets"].append(target)
    track_mocs(ctx, rep, args.wait)
    finish_moc(ctx, rep)
    return moc_exit_code(rep)


def open_targets(rep):
    return [t for t in rep["moc"]["targets"] if not t["done"] and not t["missing"]]


def track_mocs(ctx, rep, wait_s):
    """Poll the open MOCs until each reached a terminal state or wait_s seconds have passed."""
    deadline = time.monotonic() + wait_s
    shown = {}
    while open_targets(rep):
        for target in open_targets(rep):
            fetch_moc(ctx, rep, target)
        if wait_s > 0:
            show_moc_progress(ctx, rep, shown)
        left = deadline - time.monotonic()
        waiting = open_targets(rep)
        if not waiting or left <= 0:
            break
        time.sleep(min(min(t["poll_s"] for t in waiting), left))


def fetch_moc(ctx, rep, t):
    path = "/mocs/" + t["moc_id"] + ("?version={}".format(t["version"]) if t["pinned"] else "")
    try:
        data = api(ctx, "GET", path)
    except ApiError as e:
        if e.status == 404:
            return forget_moc(ctx, rep, t)
        if t["poll_error"] != describe(e):
            say("WARNING: could not check MOC {}: {}".format(t["moc_id"], describe(e)))
        t["poll_error"] = describe(e)
        return
    t["poll_error"] = None
    t["data"] = data
    if positive_int(data.get("version")):
        t["version"] = data["version"]
    t["poll_s"] = poll_seconds(data.get("poll_after_s"), t["poll_s"])
    if data.get("status") in MOC_TERMINAL:
        collect_moc(ctx, t, data)
    elif t["untracked"]:  # named on the command line but not in moc/pending.json: track it from now on
        update_moc_pending(ctx, add=[t["moc_id"]])
        t["untracked"] = False


def forget_moc(ctx, rep, t):
    t["missing"] = True
    tracked = t["moc_id"] in read_moc_pending(ctx)
    update_moc_pending(ctx, remove=[t["moc_id"]])
    msg = "MOC {}{} is unknown to the server for this user ID".format(
        t["moc_id"], " version {}".format(t["version"]) if t["pinned"] else "")
    if tracked:
        msg += "; removed it from moc/pending.json"
    rep["errors"].append(msg)
    say("ERROR:", msg)


def collect_moc(ctx, t, data):
    """A terminal answer: save it as report.v<N>.json and result.json, then stop tracking the MOC."""
    folder = moc_dir(ctx) / t["moc_id"]
    if t["version"]:
        report = folder / "report.v{}.json".format(t["version"])
        write_atomic(report, data)
        t["report_file"] = str(report)
    write_atomic(folder / "result.json", data)
    latest = data.get("latest_version")
    if not (positive_int(latest) and t["version"] and latest > t["version"]):
        update_moc_pending(ctx, remove=[t["moc_id"]])  # kept while a newer version still has to be fetched
    t["done"] = True


def moc_state_text(data):
    status = data.get("status") or "unknown"
    extra = []
    if status == "queued" and data.get("queue_ahead") is not None:
        extra.append("{} ahead".format(data["queue_ahead"]))
    if status not in MOC_TERMINAL and data.get("eta_s") is not None:
        extra.append("~{} s".format(data["eta_s"]))
    return status + (" (" + ", ".join(extra) + ")" if extra else "")


def show_moc_progress(ctx, rep, shown):
    """Print a line for each MOC whose status or queue position changed."""
    for t in rep["moc"]["targets"]:
        data = t["data"] or {}
        signature = (data.get("status"), data.get("queue_ahead"), t["version"])
        if t["missing"] or shown.get(t["moc_id"]) == signature:
            continue
        shown[t["moc_id"]] = signature
        say("[{}] MOC {} v{}: {}".format(elapsed(ctx), t["moc_id"], t["version"] or "?", moc_state_text(data)))


def issues_of(data):
    """(report dict or None, fail issues, other issues) of a GET /mocs answer."""
    report = data.get("report") if isinstance(data.get("report"), dict) else None
    issues = [i for i in (report or {}).get("issues") or [] if isinstance(i, dict)]
    fails = [i for i in issues if i.get("severity") == "fail"]
    return report, fails, [i for i in issues if i.get("severity") != "fail"]


def part_label(p):
    if positive_int(p.get("line")):
        return "line {}".format(p["line"])
    return "part #{}".format(p["index"]) if isinstance(p.get("index"), int) else "part"


def part_text(p):
    pos = p.get("pos")
    where = ("({})".format(", ".join(num(v) for v in pos)) if isinstance(pos, list) and len(pos) == 3
             else "(position not given)")
    color = p.get("color")
    return "{}: {} colour {} at {}".format(part_label(p), p.get("part") or "?", "?" if color is None else color,
                                           where)


def issue_parts(issue):
    return [p for p in issue.get("parts") or [] if isinstance(p, dict)]


def print_warnings(warnings):
    if not warnings:
        return
    say("Warnings ({}): they do not fail the model, but tell the user:".format(len(warnings)))
    for issue in warnings:
        parts = issue_parts(issue)
        labels = [part_label(p) for p in parts[:ISSUE_PARTS_SHOWN]]
        if len(parts) > ISSUE_PARTS_SHOWN:
            labels.append("+{} more".format(len(parts) - ISSUE_PARTS_SHOWN))
        say("  WARNING {}: {}{}".format(issue.get("rule") or "?", issue.get("message") or "",
                                        " (" + ", ".join(labels) + ")" if labels else ""))


def error_detail(data, report):
    err = data.get("error")
    if isinstance(err, dict) and err.get("message"):
        return "[{}] {}".format(err.get("code"), err["message"]) if err.get("code") else err["message"]
    if isinstance(err, str) and err:
        return err
    return (report or {}).get("summary") or ""


def print_moc(ctx, t):
    data = t["data"] or {}
    status = data.get("status")
    report, fails, warnings = issues_of(data)
    head = "MOC {} version {}".format(t["moc_id"], t["version"] or "?")
    model = '"{}"'.format(t["resubmit_model"]) if t.get("resubmit_model") else "<model.ldr>"
    resubmit = script_cmd("moc submit {} --moc {}".format(model, t["moc_id"]))
    say("")
    if status == "passed":
        say("== {}: PASSED ==".format(head))
    elif status == "failed":
        say("== {}: NOT PASSED - {} ==".format(head, (report or {}).get("summary") or "{} fail(s), {} warning(s)".format(
            len(fails), len(warnings))))
    elif status == "error":
        say("== {}: SERVER ERROR ==".format(head))
    else:
        say("== {}: not finished ({}) ==".format(head, moc_state_text(data)))
    if data.get("title"):
        say("Title:", data["title"])
    print_usage(data)
    if data.get("mode") == "free":
        say("Mode: free build. Not checked against the inventory; tell the user the model is not limited to their "
            "parts, the page's parts list is what they would need to get, and a part may not exist in every colour.")
    if status == "failed":
        stats = (report or {}).get("stats")
        if isinstance(stats, dict) and stats:
            say("Checked: " + ", ".join("{} {}".format(v, k) for k, v in stats.items()))
        for n, issue in enumerate(fails, 1):
            say("FAIL {}/{} {}: {}".format(n, len(fails), issue.get("rule") or "?", issue.get("message") or ""))
            if issue.get("hint"):
                say("  Hint:", issue["hint"])
            parts = issue_parts(issue)
            for p in parts[:ISSUE_PARTS_SHOWN]:
                say("  " + part_text(p))
            if len(parts) > ISSUE_PARTS_SHOWN:
                say("  +{} more (all are listed in the report file)".format(len(parts) - ISSUE_PARTS_SHOWN))
        if not fails:
            say("The server listed no fail issue{}; read the report file.".format(
                ": " + error_detail(data, report) if error_detail(data, report) else ""))
    if status in ("passed", "failed"):
        print_warnings(warnings)
    model_file = t["model_file"] or local_model_copy(ctx, t)
    if model_file:
        say("Submitted file{}: {}".format(" (line numbers count its lines from 1)" if status == "failed" else "",
                                          model_file))
    if t["report_file"]:
        say("Report:", t["report_file"])
    previews = [p for p in data.get("previews") or [] if isinstance(p, str) and p]
    if status == "passed" and previews:
        say("Preview pictures (look at them before you describe the model to the user):", " ".join(previews))
    if status == "passed":
        say("{} parts, {} building steps. Passing means the model is physically consistent in the verifier's "
            "simulation; it does not guarantee the real build holds.".format(data.get("parts", "?"),
                                                                              data.get("steps", "?")))
        say("MODEL PAGE (public, anyone with the link can view it; 3D view and step-by-step building "
            "instructions): {}".format(data.get("url") or "(the server sent no URL)"))
    elif status == "failed":
        say("NOT PASSED: fix the lines named above, then submit a new version of this MOC: " + resubmit)
    elif status == "error":
        detail = error_detail(data, report)
        say("The server failed while checking this version{}. This is a server-side error, not a problem with "
            "the design. The same file can be submitted again unchanged: {}".format(
                " (" + detail + ")" if detail else "", resubmit))
    else:
        say("STILL RUNNING: the check has not finished. Run: " + script_cmd("moc status {} --wait {}".format(
            t["moc_id"], MOC_WAIT_S)))


def usage_of(data):
    usage = data.get("usage")
    return usage if isinstance(usage, dict) else None


def print_usage(data):
    """The server's usage block (since v2.0): how many of the usable parts the model uses, and what is left."""
    usage = usage_of(data)
    if not usage:
        return
    say("Parts used: {} of {} usable ({}%; target at least {}%)".format(
        usage.get("used", "?"), usage.get("usable", "?"), usage.get("percent", "?"),
        usage.get("target_percent", "?")))
    unused = [u for u in usage.get("unused") or [] if isinstance(u, dict)]
    if unused:
        say("Most plentiful unused parts: " + "; ".join(
            "{} x {} {} ({})".format(u.get("quantity"), u.get("color_name") or "colour {}".format(u.get("ldraw_color")),
                                     u.get("name") or "?", u.get("key") or u.get("ldraw_part"))
            for u in unused[:UNUSED_SHOWN]) + ("; ..." if len(unused) > UNUSED_SHOWN or usage.get("unused_truncated")
                                               else ""))


def local_model_copy(ctx, t):
    if not t["version"]:
        return None
    copy = moc_dir(ctx) / t["moc_id"] / "v{}.ldr".format(t["version"])
    return str(copy) if copy.is_file() else None


def finish_moc(ctx, rep):
    for t in rep["moc"]["targets"]:
        if t["poll_error"] and not t["done"]:  # only the last poll counts; earlier ones were just warnings
            msg = "could not check MOC {}: {}".format(t["moc_id"], t["poll_error"])
            rep["errors"].append(msg)
            say("ERROR:", msg)
        if t["done"] and (t["data"] or {}).get("status") == "error":
            rep["errors"].append("MOC {} version {}: server-side error while checking; the same file can be "
                                 "submitted again".format(t["moc_id"], t["version"]))
    for t in rep["moc"]["targets"]:
        if not t["missing"]:
            print_moc(ctx, t)


def show_recent_mocs(ctx, limit=5):
    found = []
    for path in moc_dir(ctx).glob("*/result.json"):
        try:
            data = read_json(path)
            found.append((path.stat().st_mtime, path.parent.name, data if isinstance(data, dict) else {}))
        except (OSError, ValueError):
            continue
    if not found:
        return
    found.sort(key=lambda item: item[0], reverse=True)
    say("Latest results saved on this computer (re-check one with {}):".format(script_cmd("moc status MOC_ID")))
    for _, moc_id, data in found[:limit]:
        say("  {}  v{}  {}{}".format(moc_id, data.get("version", "?"), data.get("status", "?"),
                                     "  " + data["url"] if data.get("url") else ""))


def moc_exit_code(rep):
    if rep["errors"]:
        return EXIT_ERROR
    statuses = [(t["data"] or {}).get("status") for t in rep["moc"]["targets"] if not t["missing"]]
    if "error" in statuses:
        return EXIT_ERROR
    if any(s not in MOC_TERMINAL for s in statuses):
        return EXIT_PENDING
    return EXIT_MOC_FAILED if "failed" in statuses else EXIT_OK


MOC_KEYS = ("moc_id", "version", "status", "url", "fails", "warnings", "report_file", "result_file", "title",
            "parts", "steps", "model_file", "usage", "previews", "mode")


def moc_fields(ctx, t):
    data = t["data"] or {}
    report, fails, warnings = issues_of(data)
    usage = usage_of(data)
    return {"moc_id": t["moc_id"], "version": t["version"], "status": None if t["missing"] else data.get("status"),
            "url": data.get("url"), "fails": len(fails) if report is not None else None,
            "warnings": len(warnings) if report is not None else None, "report_file": t["report_file"],
            "result_file": str(moc_dir(ctx) / t["moc_id"] / "result.json") if t["done"] else None,
            "title": data.get("title"), "parts": data.get("parts"), "steps": data.get("steps"),
            "model_file": t["model_file"] or local_model_copy(ctx, t),
            "usage": {k: usage.get(k) for k in ("used", "usable", "percent", "target_percent")} if usage else None,
            "previews": [p for p in data.get("previews") or [] if isinstance(p, str)],
            "mode": data.get("mode") if data.get("mode") in ("inventory", "free") else None}


def moc_result(ctx, rep, code):
    m = rep["moc"]
    mocs = [moc_fields(ctx, t) for t in m["targets"]]
    # Top-level fields describe one MOC: the one that decides the exit code (error/unknown, then still
    # running, then failed, then passed), the latest of those when several tie. All are in "mocs".
    rank = {None: 0, "error": 0, "failed": 2, "passed": 3}
    main_moc = (min(reversed(mocs), key=lambda f: rank.get(f["status"], 1)) if mocs
                else dict.fromkeys(MOC_KEYS))
    obj = {"exit_code": code, "command": rep["command"]}
    obj.update(main_moc)
    obj.update({
        "mocs": mocs, "pending_moc_ids": load_ids(moc_pending_path(ctx), "moc_ids")[0],
        "guide_file": m["guide_file"], "connectors_file": m["connectors_file"],
        "connector_parts": m["connector_parts"], "connector_requests": m["connector_requests"],
        "unsupported_parts": m["unsupported_parts"], "errors": rep["errors"],
        "user_id": ctx.get("user_id"), "server": ctx.get("server"), "home": str(ctx["home"]),
        "moc_dir": str(moc_dir(ctx)),
    })
    return obj


# ---------------------------------------------------------------- MCP: local stdio bridge (coord/api-skill.md v2.0, 3.5)
#
# "lego.py mcp" is an MCP server on stdin/stdout (one JSON-RPC message per line) that agent hosts start themselves.
# initialize and ping are answered here; tools/list is the server's list plus the local scan_photos; tools/call runs
# scan_photos here (it reads photo files on this computer) and forwards every other tool to {server}/skill/mcp with
# X-Lego-User. stdout carries protocol messages only: in this mode say() and print() go to stderr.

MCP_PROTOCOL_VERSIONS = ("2025-06-18", "2025-03-26", "2024-11-05")  # newest first; an unknown request gets the first
MCP_HEADER_VERSIONS = ("2025-06-18",)  # HTTP clients send MCP-Protocol-Version from this version on
MCP_NAME = "lego-moc"
MCP_PATH = "/skill/mcp"
MCP_LIST_TIMEOUT_S = 15
MCP_CALL_TIMEOUT_S = 120   # the server answers every tool call within 50 s; the rest is slack for slow links
MCP_WORKERS = 8            # tool calls run in parallel, so a ping or a short call never waits behind a long one
MCP_EOF_GRACE_S = 10.0     # on end of input, running calls get this long to finish
MCP_READ_ONLY = ("scan_status", "inventory", "design_guide", "connectors", "find_parts", "moc_status")  # safe to send twice
PARSE_ERROR, INVALID_REQUEST, METHOD_NOT_FOUND, INVALID_PARAMS, INTERNAL_ERROR = -32700, -32600, -32601, -32602, -32603

MCP_INSTRUCTIONS = (
    "lego-moc turns photos of loose LEGO parts into an inventory, then checks a LEGO model (MOC) that you design "
    "as an LDraw file; a passing model gets a public page with a 3D view and building steps. Two design modes: "
    "inventory (default: only parts the user owns) and free (free build: any supported LDraw part in any colour "
    "and quantity, same physics check). Use free only when the user asks for it (free build, unlimited parts, "
    "自由创作, 不限零件) or design_guide reports default_mode free (no usable parts); never switch to it on your own "
    "because the inventory is short, offer it instead. In a free build look up part numbers with find_parts, pass "
    "mode=free to submit_model, aim for the strongest design the 400-part limit allows, and tell the user the model "
    "is not limited to their parts, its parts list is a shopping list, and a part may not exist in every colour. "
    "Flow: scan_photos (absolute paths of photos on this computer) -> scan_status with wait_s=50 until pending is 0 "
    "-> inventory -> edit_inventory only on the user's word -> design_guide, then connectors for the parts you plan "
    "to use -> submit_model (pass the user's request as brief) -> moc_status while it is not finished. "
    "Rules: relay every notice to the user verbatim, in the user's language. When you show the inventory, show the "
    "overview picture and give inventory_url, never a table of bare part numbers. Low-confidence rows may be "
    "misidentified: rely on them only after the user confirms them (edit_inventory op confirm). Say a model can be "
    "built only when its status is passed; passing means it is physically consistent in the verifier's simulation, "
    "not that the real build is guaranteed to hold. The model link is public. At most 5 resubmissions per model. "
    "In inventory mode use only usable parts. Design comes first: a recognisable subject and a planned colour scheme (one dominant, "
    "one secondary, one accent colour from what the inventory has most of). Use many parts to add detail and "
    "presence (a rich model often uses about 60% of the usable pieces), never to pad: a pyramid, tower or block of "
    "mixed colours that just uses up the inventory is a failure; leave out parts that would spoil the design. "
    "The user ID and every link containing it (inventory_url) are credentials: never post them anywhere public. "
    "A photo uploaded before is refused (duplicate_photo) and not recognised again; a new photo of parts already "
    "scanned counts them twice.")

SCAN_PHOTOS_TOOL = {
    "name": "scan_photos",
    "title": "Upload photos of LEGO parts",
    "description": (
        "Upload 1-30 photos of loose LEGO parts from this computer for recognition. Returns at once with one task "
        "per photo; recognition takes minutes, so then call scan_status with wait_s=50, again until pending is 0, "
        "and then inventory. paths: absolute paths of image files (JPEG, PNG, WEBP, HEIC, at most 25 MB each), "
        "folders (their image files) or glob patterns. Rules: tell the user every rejected or not uploaded file "
        "with its reason. A photo uploaded before is refused as duplicate_photo and not recognised again (its "
        "earlier result, 'previous', is already in the inventory); a new photo of parts already scanned counts "
        "them twice. For good results the parts lie spread out on a plain surface, not touching, shot from "
        "straight above in good light. If no user ID exists on this computer yet, one is created and saved "
        "(user_id_created); tell the user."),
    "inputSchema": {
        "type": "object",
        "properties": {
            "paths": {"type": "array", "items": {"type": "string"}, "minItems": 1,
                      "description": "Absolute paths of photo files, folders or glob patterns; 1-30 photos in all."},
        },
        "required": ["paths"],
    },
    "annotations": {"title": "Upload photos of LEGO parts", "readOnlyHint": False, "destructiveHint": False,
                    "idempotentHint": False, "openWorldHint": True},
}


def offline_tools():
    """A copy of the server's tool list (app/skill/mcp.py tools(), 2.1.0), for when the live list cannot be fetched
    (server unreachable). Calls are still forwarded; the real list replaces this one once the server answers."""
    return (
    [{'name': 'scan_status',
      'title': 'Photo scan status',
      'description': "Status and results of this ID's photo scans (recognition of loose LEGO parts). Pass the "
                     'task_ids returned by scan_photos, or omit them to get the unfinished tasks plus the most '
                     'recently finished ones (at most 30). wait_s (0-50) waits for unfinished tasks before '
                     'answering; while some are still pending, call again. Rules: relay every entry of notices to '
                     'the user word for word (they explain why a photo gave poor results and how to retake it). '
                     'When all tasks are done, call inventory and show the user the overview picture and the '
                     "inventory_url. The inventory_url contains the user's ID: never post it anywhere public.",
      'inputSchema': {'type': 'object',
                      'properties': {'task_ids': {'type': 'array',
                                                  'items': {'type': 'string'},
                                                  'maxItems': 100,
                                                  'description': "Task IDs from scan_photos. Omit for this ID's "
                                                                 'recent tasks.'},
                                     'wait_s': {'type': 'integer',
                                                'minimum': 0,
                                                'maximum': 50,
                                                'default': 0,
                                                'description': 'Seconds to wait for unfinished tasks (0 = answer '
                                                               'now).'}}},
      'annotations': {'readOnlyHint': True, 'openWorldHint': False}},
     {'name': 'inventory',
      'title': 'Parts inventory',
      'description': "This ID's parts inventory: recognised parts summed per LDraw part and colour, with the "
                     "user's edits applied. filter: all; usable (designable and not low-confidence, or confirmed "
                     'by the user: the parts to design with by default); low_confidence (rows to check against the '
                     'photos). Returns a compact table (paged with offset/limit) and, when image is true and '
                     'offset is 0, an overview picture. Rules: whenever you show the inventory to the user, show '
                     'the overview picture and give the inventory_url, where the user can see the photos and fix '
                     "rows; the inventory_url contains the user's ID, never post it anywhere public. Design only "
                     'with usable rows unless the user says otherwise. Before designing, count the pieces per '
                     'colour and plan a colour scheme from the most plentiful ones.',
      'inputSchema': {'type': 'object',
                      'properties': {'filter': {'type': 'string',
                                                'enum': ['all', 'usable', 'low_confidence'],
                                                'default': 'all'},
                                     'offset': {'type': 'integer', 'minimum': 0, 'default': 0},
                                     'limit': {'type': 'integer', 'minimum': 1, 'maximum': 400, 'default': 200},
                                     'image': {'type': 'boolean',
                                               'default': True,
                                               'description': 'Attach the overview picture (only when offset is '
                                                              '0).'}}},
      'annotations': {'readOnlyHint': True, 'openWorldHint': False}},
     {'name': 'edit_inventory',
      'title': 'Correct the inventory',
      'description': "Correct this ID's inventory when the user says a row is wrong. changes (1-50) are applied in "
                     'order, each on its own: set_quantity {key, quantity 0-999}; remove {key}; confirm {key} (the '
                     'row is right: it stops being low-confidence and becomes usable); replace {key, ldraw_part, '
                     'ldraw_color} (every piece of the row is really another part or colour; the new row is '
                     'confirmed); add {ldraw_part, ldraw_color, quantity 1-999} (confirmed); undo {key} (drop this '
                     'row\'s edits); undo_all (drop every edit). key is the row key from inventory, e.g. "3001|4" '
                     '= LDraw part 3001 in LDraw colour 4. Edits are kept apart from recognition, so later scans '
                     'still add their pieces. Only make edits the user asked for or agreed to. At most 200 changes '
                     'per ID per day.',
      'inputSchema': {'type': 'object',
                      'required': ['changes'],
                      'properties': {'changes': {'type': 'array',
                                                 'minItems': 1,
                                                 'maxItems': 50,
                                                 'items': {'type': 'object',
                                                           'required': ['op'],
                                                           'properties': {'op': {'type': 'string',
                                                                                 'enum': ['set_quantity',
                                                                                          'remove',
                                                                                          'confirm',
                                                                                          'replace',
                                                                                          'add',
                                                                                          'undo',
                                                                                          'undo_all']},
                                                                          'key': {'type': 'string',
                                                                                  'description': 'Row key from '
                                                                                                 'inventory, e.g. '
                                                                                                 '"3001|4".'},
                                                                          'quantity': {'type': 'integer',
                                                                                       'minimum': 0,
                                                                                       'maximum': 999},
                                                                          'ldraw_part': {'type': 'string',
                                                                                         'description': 'LDraw '
                                                                                                        'part '
                                                                                                        'number, '
                                                                                                        'e.g. '
                                                                                                        '"3001".'},
                                                                          'ldraw_color': {'type': 'integer',
                                                                                          'description': 'LDraw '
                                                                                                         'colour '
                                                                                                         'code, '
                                                                                                         'e.g. 4 '
                                                                                                         '(red).'}}}}}},
      'annotations': {'readOnlyHint': False,
                      'destructiveHint': False,
                      'idempotentHint': False,
                      'openWorldHint': False}},
     {'name': 'design_guide',
      'title': 'Design guide',
      'description': 'The design guide for LDraw models this server can check: file format, coordinates, how parts '
                     'connect, every check rule, the two design modes and how to declare moving parts. Also '
                     "returns the size of this ID's usable inventory, the usage target and default_mode: "
                     '"inventory", or "free" when this ID has no usable parts. Read it before writing a model. '
                     'Rules: in inventory mode design only with usable parts unless the user says otherwise; use '
                     'free mode only when the user asks for a free build or default_mode is free. Design first '
                     '(subject, silhouette, colour plan), then use many parts for detail and presence; about 60% '
                     'usage is a gauge of a rich model, not a quota, and never a reason to pad.',
      'inputSchema': {'type': 'object', 'properties': {}},
      'annotations': {'readOnlyHint': True, 'openWorldHint': False}},
     {'name': 'connectors',
      'title': 'Connector sheets',
      'description': "Connector sheets for 1-40 LDraw part numbers: each part's bounding box and every connector "
                     "(type, position, axis, length) in the part's own coordinates. Compute part positions in a "
                     'model from these. Parts listed in unsupported cannot be checked: do not use them. Long '
                     'answers are cut: parts listed in deferred were left out, call connectors again with them.',
      'inputSchema': {'type': 'object',
                      'required': ['parts'],
                      'properties': {'parts': {'type': 'array',
                                               'items': {'type': 'string'},
                                               'minItems': 1,
                                               'maxItems': 40,
                                               'description': 'LDraw part numbers, e.g. ["3001", "3020"].'}}},
      'annotations': {'readOnlyHint': True, 'openWorldHint': False}},
     {'name': 'find_parts',
      'title': 'Find supported parts',
      'description': 'Look up LDraw part numbers the verifier supports, for a free build (mode "free") where the '
                     'model is not limited to the inventory. query: words that must all appear in the LDraw part '
                     'name (e.g. "slope 45 2 x 2", "wheel", "plate 1 x 4", "window"), or the start of a part '
                     'number. Returns up to limit matches (number and name), plain parts before printed variants; '
                     'page with offset. Then get the connector sheets of the parts you choose with connectors. A '
                     'part that is not found here cannot be used in a model.',
      'inputSchema': {'type': 'object',
                      'required': ['query'],
                      'properties': {'query': {'type': 'string',
                                               'maxLength': 80,
                                               'description': 'Words from the part name, or a part number prefix.'},
                                     'offset': {'type': 'integer', 'minimum': 0, 'default': 0},
                                     'limit': {'type': 'integer', 'minimum': 1, 'maximum': 100, 'default': 40}}},
      'annotations': {'readOnlyHint': True, 'openWorldHint': False}},
     {'name': 'submit_model',
      'title': 'Check a model',
      'description': "Submit an LDraw model (the full text of a flat .ldr file: '1' part lines and '0' comments, "
                     'no sub-models, no steps) to be checked by the physics verifier. mode "inventory" also checks '
                     'it against this ID\'s current inventory (with edits); mode "free" (free build) allows any '
                     'supported part in any colour and quantity and skips the inventory check: pass it only when '
                     'the user asked for a free build or has no usable parts. Without mode: a new model is '
                     'inventory (free when this ID has no usable parts), a new version keeps the mode of the '
                     'model. Waits up to wait_s seconds (default 45) for the verdict; if status is still queued, '
                     'checking or stepping, call moc_status with the moc_id. Pass moc_id to submit a corrected '
                     "version of an earlier model. brief is the user's request in their own words (shown on the "
                     'page). design is the optional design.json object (title, description, motions) described in '
                     "the guide. The result has the issues with the file's line numbers, the inventory usage "
                     '(inventory mode) and, when the model passed, its public page url and two preview pictures. '
                     'Rules: only say the model can be built, is valid or works when status is "passed". On '
                     '"failed", fix the lines named in issues and submit again with the same moc_id (at most 5 '
                     'resubmissions; then stop and tell the user honestly which rules still fail on which parts). '
                     '"error" is a server problem: submit the same model again. The page url and preview pictures '
                     'are public: tell the user that anyone with the link can view the model. Passing means the '
                     "model is physically consistent in the verifier's simulation, not a guarantee that the real "
                     'build will hold: say so. Relay every warning.',
      'inputSchema': {'type': 'object',
                      'required': ['ldr'],
                      'properties': {'ldr': {'type': 'string',
                                             'description': 'The whole LDraw file text (at most 1 MB).'},
                                     'title': {'type': 'string', 'maxLength': 80},
                                     'brief': {'type': 'string',
                                               'maxLength': 500,
                                               'description': "The user's request, in their words."},
                                     'moc_id': {'type': 'string',
                                                'description': 'An earlier model of this ID: makes a new version '
                                                               'of it.'},
                                     'mode': {'type': 'string',
                                              'enum': ['inventory', 'free'],
                                              'description': 'inventory = only parts the user owns; free = free '
                                                             'build, any supported part.'},
                                     'design': {'type': 'object',
                                                'description': 'design.json: {title, description, motions[]}.'},
                                     'wait_s': {'type': 'integer',
                                                'minimum': 0,
                                                'maximum': 50,
                                                'default': 45,
                                                'description': 'Seconds to wait for the verdict.'}}},
      'annotations': {'readOnlyHint': False,
                      'destructiveHint': False,
                      'idempotentHint': False,
                      'openWorldHint': False}},
     {'name': 'moc_status',
      'title': 'Model check status',
      'description': 'Status and report of a submitted model (its latest version, or `version`), optionally '
                     'waiting wait_s seconds (0-50) for the check to finish. Same result as submit_model. Rules: '
                     'only say the model can be built, is valid or works when status is "passed". On "failed", fix '
                     'the lines named in issues and submit again with the same moc_id (at most 5 resubmissions; '
                     'then stop and tell the user honestly which rules still fail on which parts). "error" is a '
                     'server problem: submit the same model again. The page url and preview pictures are public: '
                     'tell the user that anyone with the link can view the model. Passing means the model is '
                     "physically consistent in the verifier's simulation, not a guarantee that the real build will "
                     'hold: say so. Relay every warning.',
      'inputSchema': {'type': 'object',
                      'required': ['moc_id'],
                      'properties': {'moc_id': {'type': 'string'},
                                     'version': {'type': 'integer', 'minimum': 1},
                                     'wait_s': {'type': 'integer',
                                                'minimum': 0,
                                                'maximum': 50,
                                                'default': 0,
                                                'description': 'Seconds to wait for the verdict (0 = answer '
                                                               'now).'}}},
      'annotations': {'readOnlyHint': True, 'openWorldHint': False}}]
    )


def new_ctx():
    return {"start": time.monotonic(), "home": home_dir(), "user_id": None, "server": None}


def log(*parts):
    print(*parts, file=sys.stderr, flush=True)


def mcp_server_version():
    return ".".join((VERSION.split(".") + ["0", "0"])[:3])


def valid_rpc_id(value):
    """MCP request IDs are strings or numbers, never null (and a JSON true is not a number)."""
    return isinstance(value, str) or (isinstance(value, (int, float)) and not isinstance(value, bool))


def rpc_key(value):
    return json.dumps(value)


def rpc_error(mid, code, message):
    return {"jsonrpc": "2.0", "id": mid, "error": {"code": code, "message": message}}


def rpc_result(mid, result):
    return {"jsonrpc": "2.0", "id": mid, "result": result}


def tool_text(text, is_error=False, structured=None):
    """A tool result. An error result carries no structuredContent: hosts validate it against outputSchema."""
    out = {"content": [{"type": "text", "text": text}], "isError": bool(is_error)}
    if structured is not None and not is_error:
        out["structuredContent"] = structured
    return out


def jsonrpc_reply(raw, mid):
    """The JSON-RPC response for request mid in a reply body: plain JSON (one message or an array), or a
    text/event-stream whose data lines carry it. None when there is none."""
    if not raw:
        return None
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return None
    found = []
    try:
        found.append(json.loads(text))
    except (ValueError, RecursionError):
        data = []
        for line in text.splitlines() + [""]:
            if line.startswith("data:"):
                data.append(line[6:] if line[5:6] == " " else line[5:])
            elif not line.strip() and data:
                try:
                    found.append(json.loads("\n".join(data)))
                except (ValueError, RecursionError):
                    pass
                data = []
    for item in found:
        for one in item if isinstance(item, list) else [item]:
            if not isinstance(one, dict) or one.get("jsonrpc") != "2.0":
                continue  # e.g. the REST error envelope {"error": {"code": "not_found", ...}} of an older server
            if "result" in one and "error" not in one and one.get("id") == mid:
                return one
            if ("error" in one and "result" not in one and isinstance(one["error"], dict)
                    and isinstance(one["error"].get("code"), int) and one.get("id") in (mid, None)):
                return one
    return None


def new_id_note(ctx):
    return ("Note: there was no user ID on this computer yet, so a new one was created and saved in {}. Tell the "
            "user. The ID is the key to their inventory and models: links that contain it (inventory_url) must "
            "stay private.".format(ctx["home"] / "user.json"))


class McpBridge(object):
    """MCP server on a binary stdin/stdout pair (newline-delimited JSON-RPC, protocol versions in
    MCP_PROTOCOL_VERSIONS). Malformed input gets a JSON-RPC error; nothing ends the loop but end of input."""

    def __init__(self, stdin, stdout):
        self.stdin, self.stdout = stdin, stdout
        self.text_out = isinstance(stdout, io.TextIOBase)
        self.write_lock, self.state_lock = threading.Lock(), threading.Lock()
        self.slots = threading.Semaphore(MCP_WORKERS)
        self.threads, self.inflight, self.cancelled = [], set(), set()
        self.version = MCP_PROTOCOL_VERSIONS[0]
        self.ready = False        # initialize was answered
        self.broken = False       # stdout is gone: the host has quit
        self.offline = False      # the last tools/list answer was the offline copy
        self.reached = False      # a call reached the server since then
        self.last_tools = None    # the server's tools as last fetched
        self.annotations = {}

    # ------------------------------------------------------------ transport

    def run(self):
        log("lego-moc MCP bridge {} started (local folder {}); waiting for MCP messages on stdin".format(
            mcp_server_version(), home_dir()))
        while not self.broken:
            try:
                line = self.stdin.readline()
            except (OSError, ValueError):
                break
            except KeyboardInterrupt:
                return EXIT_OK
            if not line:
                break  # end of input: the host closed the connection
            try:
                self.handle_line(line)
            except Exception:  # one bad message must never end the bridge
                traceback.print_exc(file=sys.stderr)
        deadline = time.monotonic() + MCP_EOF_GRACE_S
        with self.state_lock:
            threads = list(self.threads)
        for thread in threads:
            thread.join(max(0.0, deadline - time.monotonic()))
        return EXIT_OK

    def send(self, message):
        line = json.dumps(message, ensure_ascii=True, separators=(",", ":")) + "\n"  # pure ASCII, one line
        with self.write_lock:
            if self.broken:
                return
            try:
                self.stdout.write(line if self.text_out else line.encode("ascii"))
                self.stdout.flush()
            except (OSError, ValueError):
                self.broken = True

    def handle_line(self, line):
        if not isinstance(line, bytes):
            line = line.encode("utf-8", "surrogateescape")
        line = line.strip()
        if line.startswith(b"\xef\xbb\xbf"):
            line = line[3:].strip()
        if not line:
            return
        try:
            msg = json.loads(line.decode("utf-8"))
        except UnicodeDecodeError:
            return self.send(rpc_error(None, PARSE_ERROR, "Parse error: the line is not UTF-8 text"))
        except (ValueError, RecursionError) as e:
            return self.send(rpc_error(None, PARSE_ERROR, "Parse error: each line must be one JSON-RPC message "
                                                          "({})".format(e)))
        if isinstance(msg, list):  # a batch (protocol 2025-03-26)
            if not msg:
                return self.send(rpc_error(None, INVALID_REQUEST, "Invalid Request: empty batch"))
            return self.spawn(None, lambda: [r for r in (self.process(m) for m in msg) if r is not None] or None)
        if (isinstance(msg, dict) and msg.get("method") in ("tools/list", "tools/call")
                and valid_rpc_id(msg.get("id"))):
            return self.spawn(msg["id"], lambda: self.process(msg))
        reply = self.process(msg)
        if reply is not None:
            self.send(reply)

    def spawn(self, mid, work):
        """Run work() in a thread and send its reply, unless the host cancelled the request meanwhile."""
        key = rpc_key(mid) if mid is not None else None

        def run():
            reply = None
            with self.slots:
                try:
                    reply = work()
                except Exception as e:
                    traceback.print_exc(file=sys.stderr)
                    if mid is not None:
                        reply = rpc_error(mid, INTERNAL_ERROR, "Internal error in the lego-moc bridge: {!r}".format(e))
            with self.state_lock:
                cancelled = key in self.cancelled
                self.cancelled.discard(key)
                self.inflight.discard(key)
            if reply is not None and not cancelled:
                self.send(reply)
            self.notify_list_changed()

        thread = threading.Thread(target=run, name="mcp-request", daemon=True)
        with self.state_lock:
            if key is not None:
                self.inflight.add(key)
            self.threads = [t for t in self.threads if t.is_alive()] + [thread]
        thread.start()

    def notify_list_changed(self):
        """After the host got the offline tool list, the first call that reaches the server makes it list again."""
        with self.state_lock:
            if not (self.ready and self.offline and self.reached):
                return
            self.offline = self.reached = False
        self.send({"jsonrpc": "2.0", "method": "notifications/tools/list_changed"})

    # ------------------------------------------------------------ JSON-RPC

    def process(self, msg):
        """One message -> its response, or None for a notification (or a response, which needs none)."""
        if not isinstance(msg, dict):
            return rpc_error(None, INVALID_REQUEST, "Invalid Request: a message must be a JSON object")
        has_id = "id" in msg
        mid = msg.get("id")
        if has_id and not valid_rpc_id(mid):
            return rpc_error(None, INVALID_REQUEST, "Invalid Request: the id must be a string or a number, not null")
        reply_id = mid if has_id else None
        if msg.get("jsonrpc") != "2.0":
            return rpc_error(reply_id, INVALID_REQUEST, 'Invalid Request: "jsonrpc" must be "2.0"')
        method = msg.get("method")
        if not isinstance(method, str):
            if has_id and ("result" in msg or "error" in msg):
                return None  # a response: this bridge sends the host no requests, so there is nothing to match
            return rpc_error(reply_id, INVALID_REQUEST, 'Invalid Request: "method" must be a string')
        params = msg.get("params")
        if params is None:
            params = {}
        if not has_id:
            if isinstance(params, dict):
                self.notification(method, params)
            return None
        if not isinstance(params, dict):
            return rpc_error(mid, INVALID_PARAMS, 'Invalid params: "params" must be an object')
        try:
            if method == "initialize":
                return rpc_result(mid, self.initialize(params))
            if method == "ping":
                return rpc_result(mid, {})
            if method == "tools/list":
                return rpc_result(mid, self.tools_list(mid, params))
            if method == "tools/call":
                return self.tools_call(mid, params)
        except Exception as e:
            traceback.print_exc(file=sys.stderr)
            return rpc_error(mid, INTERNAL_ERROR, "Internal error in the lego-moc bridge: {!r}".format(e))
        return rpc_error(mid, METHOD_NOT_FOUND, "Method not found: {}".format(method[:100]))

    def notification(self, method, params):
        if method == "notifications/cancelled" and valid_rpc_id(params.get("requestId")):
            key = rpc_key(params["requestId"])
            with self.state_lock:
                if key in self.inflight:
                    self.cancelled.add(key)
        # notifications/initialized and anything else need no action

    def initialize(self, params):
        requested = params.get("protocolVersion")
        self.version = requested if requested in MCP_PROTOCOL_VERSIONS else MCP_PROTOCOL_VERSIONS[0]
        client = params.get("clientInfo") if isinstance(params.get("clientInfo"), dict) else {}
        log("initialize from {} {}: protocol {} (asked for {})".format(
            client.get("name") or "an MCP client", client.get("version") or "", self.version, requested))
        self.ready = True
        return {"protocolVersion": self.version, "capabilities": {"tools": {"listChanged": True}},
                "serverInfo": {"name": MCP_NAME, "title": "LEGO parts and MOC check", "version": mcp_server_version()},
                "instructions": MCP_INSTRUCTIONS}

    # ------------------------------------------------------------ tools

    def context(self):
        """(ctx with user ID and server address as the script resolves them, problem text or None)."""
        ctx = new_ctx()
        try:
            setup(ctx)
        except Fatal as e:
            return ctx, str(e)
        return ctx, None

    def tools_list(self, mid, params):
        cursor = params.get("cursor")
        ctx, problem = self.context()
        reply = None
        if problem is None:
            reply, problem = self.post(ctx, {"jsonrpc": "2.0", "id": mid, "method": "tools/list", "params": params},
                                       MCP_LIST_TIMEOUT_S, True)
        result = reply.get("result") if isinstance(reply, dict) else None
        if isinstance(result, dict) and isinstance(result.get("tools"), list):
            tools = [t for t in result["tools"] if isinstance(t, dict) and t.get("name") != SCAN_PHOTOS_TOOL["name"]]
            with self.state_lock:
                self.offline = False
                self.annotations.update({t["name"]: t.get("annotations") for t in tools if isinstance(t.get("name"), str)})
                if not cursor and not result.get("nextCursor"):
                    self.last_tools = tools
            out = dict(result)
            out["tools"] = tools + ([] if cursor else [SCAN_PHOTOS_TOOL])
            return out
        if problem is None and isinstance(reply, dict):
            problem = "the server answered {}".format(json.dumps(reply.get("error"))[:300])
        why = describe(problem) if isinstance(problem, ApiError) else problem
        with self.state_lock:
            cached = self.last_tools
            self.offline = cached is None
            self.reached = False
        log("tools/list: the server's tool list is not available ({}); answering with {}".format(
            why, "the list fetched earlier" if cached else "the offline copy"))
        if cursor:
            return {"tools": []}
        return {"tools": (cached or offline_tools()) + [SCAN_PHOTOS_TOOL]}

    def tools_call(self, mid, params):
        name = params.get("name")
        if not isinstance(name, str) or not name.strip():
            return rpc_error(mid, INVALID_PARAMS, 'Invalid params: tools/call needs the tool\'s "name"')
        arguments = params.get("arguments")
        if arguments is not None and not isinstance(arguments, dict):
            return rpc_error(mid, INVALID_PARAMS, 'Invalid params: "arguments" must be an object')
        if name == SCAN_PHOTOS_TOOL["name"]:
            return rpc_result(mid, self.scan_photos(arguments or {}))
        return self.forward(mid, name, params)

    def read_only(self, name):
        hints = self.annotations.get(name)
        hints = hints if isinstance(hints, dict) else {}
        return name in MCP_READ_ONLY or hints.get("readOnlyHint") is True or hints.get("idempotentHint") is True

    def post(self, ctx, message, timeout, retryable):
        """POST one JSON-RPC message to {server}/skill/mcp -> (the server's JSON-RPC response, None), also when it
        came with an HTTP error status, or (None, ApiError) when there is none. Nothing is sent twice unless the
        connection was refused, or the tool only reads and a proxy failed (502/503/504) or the connection broke."""
        headers = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream"}
        if ctx.get("user_id"):
            headers["X-Lego-User"] = ctx["user_id"]
        if self.version in MCP_HEADER_VERSIONS:
            headers["MCP-Protocol-Version"] = self.version
        body = json.dumps(message, ensure_ascii=False).encode("utf-8")
        for attempt in range(3):
            try:
                status, raw = http_request("POST", ctx["server"] + MCP_PATH, body, headers, timeout)
            except ApiError as e:
                again = e.refused or (retryable and attempt == 0 and (
                    e.status in (502, 503, 504) or (e.status is None and e.code == "network"
                                                    and "timed out" not in e.message)))
                if again and attempt < 2:
                    time.sleep(1.0 + attempt)
                    continue
                if e.status is not None and e.status != 401:
                    reply = jsonrpc_reply(e.body, message.get("id"))
                    if reply is not None:
                        return reply, None
                return None, e
            reply = jsonrpc_reply(raw, message.get("id"))
            if reply is None:
                return None, ApiError(status, "bad_response", "the server sent no JSON-RPC answer to {} (HTTP {})".format(
                    message.get("method"), status))
            return reply, None
        return None, ApiError(None, "network", "no answer")  # not reached

    def call_problem(self, ctx, name, err):
        """Text for a forwarded call that got no JSON-RPC answer: what happened and what to do next."""
        server = ctx.get("server")
        if err.status == 401 or err.code == "bad_user":
            return bad_user_message(ctx)
        if err.status in (404, 405):
            return ("The server {} has no MCP endpoint ({} answered HTTP {}), so the {} tool cannot be used there; it "
                    "probably runs an older version. Meanwhile use the script commands instead (see SKILL.md, "
                    "\"Script fallback\").".format(server, MCP_PATH, err.status, name))
        if err.status is None and "timed out" in err.message:
            text = "The server {} did not answer the {} call within {} s.".format(server, name, MCP_CALL_TIMEOUT_S)
        elif err.status is None and err.code == "network":
            text = "The LEGO server {} cannot be reached ({}; {}).".format(server, err.message, HINTS["network"])
        else:
            text = "The {} call failed: {}.".format(name, describe(err))
        if not err.refused and name == "submit_model":
            text += (" The server may have received the model anyway: check with moc_status if you have its moc_id, "
                     "or on the works page (inventory_url followed by /works), before you submit it again; every "
                     "submission counts towards the 5 per model.")
        elif not err.refused and name == "edit_inventory":
            text += " Some changes may have been applied: call inventory to see the current state before repeating them."
        return text + " The bridge keeps running: try the same call again in a minute; if it keeps failing, tell the user."

    def forward(self, mid, name, params):
        ctx, problem = self.context()
        if problem:
            return rpc_result(mid, tool_text(problem, True))
        try:
            created = ensure_user(ctx)
        except Fatal as e:
            return rpc_result(mid, tool_text(str(e), True))
        except ApiError as e:
            return rpc_result(mid, tool_text("There is no user ID on this computer yet, and creating one failed: {}. "
                                             "Nothing was sent to the {} tool.".format(describe(e), name), True))
        reply, err = self.post(ctx, {"jsonrpc": "2.0", "id": mid, "method": "tools/call", "params": params},
                               MCP_CALL_TIMEOUT_S, self.read_only(name))
        if reply is None:
            text = self.call_problem(ctx, name, err)
            return rpc_result(mid, tool_text(text + ("\n" + new_id_note(ctx) if created else ""), True))
        reply = dict(reply, jsonrpc="2.0", id=mid)  # the server's answer, untouched apart from these two fields
        result = reply.get("result")
        if isinstance(result, dict):
            with self.state_lock:
                self.reached = True
            if created and isinstance(result.get("content"), list):
                reply["result"] = dict(result, content=result["content"] + [{"type": "text", "text": new_id_note(ctx)}])
        return reply

    def scan_photos(self, arguments):
        paths = arguments.get("paths")
        if isinstance(paths, str):
            paths = [paths]
        if not isinstance(paths, list) or not paths or not all(isinstance(p, str) and p.strip() for p in paths):
            return tool_text('scan_photos needs "paths": a list of 1-30 absolute paths of photo files, folders or glob '
                             "patterns on this computer. Nothing was uploaded.", True)
        paths = [p.strip() for p in paths]
        try:
            photos = expand_photos(paths)
        except UsageError as e:
            text = str(e).replace("several scan commands", "several scan_photos calls").rstrip(".") + "."
            if any(not os.path.isabs(os.path.expanduser(p)) for p in paths):
                text += (" Relative paths are read from the bridge's own folder ({}), not from your workspace: give "
                         "absolute paths.".format(os.getcwd()))
            return tool_text(text + " Nothing was uploaded.", True)
        ctx, problem = self.context()
        if problem:
            return tool_text(problem + " Nothing was uploaded.", True)
        try:
            created = ensure_user(ctx)
        except Fatal as e:
            return tool_text(str(e) + " Nothing was uploaded.", True)
        except ApiError as e:
            return tool_text("There is no user ID on this computer yet, and creating one failed: {}. Nothing was "
                             "uploaded.".format(describe(e)), True)
        rep = new_report("scan_photos")
        try:
            upload(ctx, rep, photos)
        except Fatal as e:  # e.g. the server does not know this user ID
            rep["errors"].append(str(e))
        if rep["submitted"]:
            with self.state_lock:
                self.reached = True
        return scan_photos_result(ctx, rep, created)


def scan_photos_result(ctx, rep, created):
    tasks = [{"task_id": tid, "filename": (rep["tasks"].get(tid) or {}).get("filename")} for tid in rep["submitted"]]
    duplicates = [r for r in rep["rejected"] if r.get("code") == "duplicate_photo"]
    lines = []
    if tasks:
        lines.append("Uploaded {} photo(s); recognition has started on the server: {}.".format(
            len(tasks), ", ".join(t["filename"] or t["task_id"] for t in tasks)))
        if rep.get("eta_s"):
            lines.append("Estimated time until all are recognised: about {} s.".format(int(rep["eta_s"])))
        lines.append("Next: call scan_status with wait_s=50 and repeat until pending is 0 (do not upload these photos "
                     "again), then call inventory.")
    else:
        lines.append("No new photo was uploaded for recognition.")
    for r in rep["rejected"]:
        line = "REJECTED {}: [{}] {}".format(r.get("filename"), r.get("code"), r.get("message"))
        if r.get("previous"):
            line += " First upload: {}.".format(previous_text(r["previous"]))
        lines.append(line)
    if duplicates:
        lines.append("A photo uploaded before is not recognised again: its parts are in the inventory already. A new "
                     "photo of the same parts would count them twice, so photograph only parts not scanned yet.")
    if rep["not_uploaded"]:
        lines.append("NOT UPLOADED: " + ", ".join(rep["not_uploaded"]))
    lines += ["ERROR: " + e for e in rep["errors"]]
    if rep["rejected"] or rep["not_uploaded"]:
        lines.append("Tell the user each rejected or not uploaded file and the reason.")
    if created:
        lines.append(new_id_note(ctx))
    only_duplicates = (not tasks and not rep["errors"] and not rep["not_uploaded"] and bool(duplicates)
                       and len(duplicates) == len(rep["rejected"]))
    structured = {"tasks": tasks, "rejected": rep["rejected"], "not_uploaded": rep["not_uploaded"],
                  "eta_s": rep.get("eta_s"), "user_id_created": created, "errors": rep["errors"]}
    result = tool_text("\n".join(lines), not tasks and not only_duplicates, structured)
    if result["isError"]:
        result["structuredContent"] = structured  # scan_photos declares no outputSchema: keep the details
    return result


def mcp_main(argv):
    """lego.py mcp / mcp-config: stdout is reserved for the protocol (or the JSON); all other output goes to stderr."""
    out = sys.stdout
    sys.stdout = sys.stderr
    try:
        try:
            args = build_parser().parse_args(argv)
        except SystemExit as e:
            return EXIT_OK if e.code in (0, None) else EXIT_USAGE
        if args.command == "mcp":
            stdin = getattr(sys.stdin, "buffer", sys.stdin)
            return McpBridge(stdin, getattr(out, "buffer", out)).run()
        return cmd_mcp_config(args, out)
    except KeyboardInterrupt:
        return EXIT_OK
    finally:
        sys.stdout = out


def cmd_mcp_config(args, out):
    ctx = new_ctx()
    try:
        if args.remote:
            setup(ctx)
            ensure_user(ctx)
            entry = {"type": "http", "url": "{}{}/{}".format(ctx["server"], MCP_PATH, ctx["user_id"])}
        else:
            setup(ctx, need_server=False)
            entry = {"command": os.path.abspath(sys.executable) if sys.executable else python_cmd(),
                     "args": [os.path.abspath(__file__), "mcp"]}
            env = {k: os.environ[k].strip() for k in ("LEGO_PARTS_SERVER", "LEGO_PARTS_HOME")
                   if os.environ.get(k, "").strip()}
            if env:
                entry["env"] = env
    except (Fatal, UsageError) as e:
        log("ERROR:", e)
        return EXIT_ERROR
    except ApiError as e:
        log("ERROR:", describe(e))
        return EXIT_ERROR
    text = json.dumps({"mcpServers": {MCP_NAME: entry}}, indent=2, ensure_ascii=True)
    out.write(text + "\n")
    out.flush()
    log("Paste the JSON above into the MCP settings of the agent (the \"mcpServers\" part of its MCP config file "
        "or settings page; if the host already has other servers, add only the \"{}\" entry), then restart the "
        "agent or reload its MCP servers.".format(MCP_NAME))
    if args.remote:
        log("This address contains the user ID, the key to the inventory and models: keep it private. The remote "
            "server cannot read files on this computer, so it has no scan_photos; upload photos with the local "
            "bridge (mcp-config without --remote) or with the scan command.")
    else:
        log("The agent then starts the bridge itself: no shell commands are needed for scanning and designing.")
        log("Claude Code: claude mcp add {} -- {} {} mcp".format(
            MCP_NAME, json.dumps(entry["command"]), json.dumps(entry["args"][0])))
        log("Codex, in ~/.codex/config.toml:\n[mcp_servers.{}]\ncommand = {}\nargs = {}".format(
            MCP_NAME, json.dumps(entry["command"]), json.dumps(entry["args"])))
        if not server_configured(ctx["server"]):
            log("WARNING: " + no_server_message())
    return EXIT_OK


# ---------------------------------------------------------------- commands

def finish(ctx, rep, images, force_refresh=False):
    """Refresh parts.json when something was collected (or asked for), then print the summary."""
    if rep["poll_error"]:  # only the last poll round counts; earlier transient failures were just warnings
        rep["errors"].append("could not check task status: " + rep["poll_error"])
        say("ERROR:", rep["errors"][-1])
    if ctx.get("user_id") and (rep["collected"] or images or force_refresh):
        try:
            refresh_parts(ctx, rep, images)
        except ApiError as e:
            msg = "could not refresh parts.json: {} (results are saved in tasks/; run parts later)".format(
                describe(e))
            rep["errors"].append(msg)
            say("ERROR:", msg)
    print_summary(ctx, rep)


def no_user_yet(ctx):
    if read_pending(ctx):
        raise Fatal("pending.json lists tasks but {} is missing, so they cannot be checked".format(
            ctx["home"] / "user.json"))
    say("No user ID on this computer yet ({}), so there is nothing to check. Run scan first.".format(
        ctx["home"] / "user.json"))


def cmd_scan(ctx, rep, args):
    photos = expand_photos(args.photos)
    setup(ctx)
    ensure_user(ctx)
    earlier = read_pending(ctx)
    if earlier:
        say("Checking {} task(s) left from earlier runs ...".format(len(earlier)))
        track(ctx, rep, earlier, 0)
    upload(ctx, rep, photos)
    if not rep["submitted"] and not rep["errors"]:
        if rep["rejected"] and all(r.get("code") == "duplicate_photo" for r in rep["rejected"]):
            rep["errors"].append("no photo was accepted: every one was uploaded before (duplicate_photo), so its "
                                 "parts are in the inventory already and it was not recognised again")
        else:
            rep["errors"].append("no photo was accepted by the server (see REJECTED lines)")
    if args.no_wait:
        if rep["submitted"]:
            say("Not waiting (--no-wait). Task IDs are saved in", ctx["home"] / "pending.json")
    else:
        watch = list(dict.fromkeys(rep["submitted"] + read_pending(ctx)))
        if watch:
            say("Waiting for results (up to {} s; stopping early is safe, task IDs are saved in "
                "pending.json) ...".format(args.wait))
            track(ctx, rep, watch, args.wait)
    finish(ctx, rep, args.images)


def cmd_status(ctx, rep, args):
    for tid in args.task_ids:
        if not valid_id(tid):
            raise UsageError("not a task ID: " + tid)
    setup(ctx)
    if not ctx["user_id"]:
        return no_user_yet(ctx)
    watch = list(dict.fromkeys(args.task_ids)) or read_pending(ctx)
    if watch:
        track(ctx, rep, watch, args.wait)
    else:
        say("No pending tasks.")
    finish(ctx, rep, args.images)


def cmd_parts(ctx, rep, args):
    setup(ctx)
    if not ctx["user_id"]:
        return no_user_yet(ctx)
    pending = read_pending(ctx)
    if pending:
        track(ctx, rep, pending, 0)
    finish(ctx, rep, args.images, force_refresh=True)


def cmd_whoami(ctx, rep, args):
    setup(ctx, need_server=False)
    configured = server_configured(ctx["server"])
    say("User ID:    {}".format(ctx["user_id"] or "(none yet; the first scan creates one)"))
    say("Server:     {}".format("{} (from {})".format(ctx["server"], ctx["server_source"]) if configured
                                else "(not configured)"))
    say("Local dir:  {}".format(ctx["home"]))
    say("Pending:    {} task(s)".format(len(read_pending(ctx))))
    rows, total, problem = load_inventory(ctx)
    say("parts.json: {}".format(problem or "{} pieces in {} rows".format(total, len(rows))))
    say("MOCs:       {} submission(s) waiting for their check result".format(len(read_moc_pending(ctx))))
    add_unique(rep["scope"], read_pending(ctx))
    if not configured:
        rep["errors"].append(no_server_message())
        say("ERROR:", no_server_message())
        return EXIT_ERROR
    return EXIT_OK


def wait_seconds(text):
    try:
        value = int(text)
    except ValueError:
        raise argparse.ArgumentTypeError("must be a whole number of seconds")
    if value < 0:
        raise argparse.ArgumentTypeError("must be 0 or more")
    return value


def build_parser():
    parser = argparse.ArgumentParser(
        prog="lego.py", description="Recognise loose LEGO parts from photos and check LEGO models (MOCs) "
                                    "designed from them; results go to ~/.lego-parts/.",
        epilog="Exit codes: 0 all finished / MOC passed, 4 MOC did not pass, 3 still running (run status --wait "
               "or moc status --wait), 1 error, 2 usage error.")
    sub = parser.add_subparsers(dest="command", metavar="COMMAND")
    sub.required = True
    scan = sub.add_parser("scan", help="upload 1-30 photos and wait for the result")
    scan.add_argument("photos", nargs="+", metavar="PHOTO", help="image files, folders or glob patterns")
    scan.add_argument("--no-wait", action="store_true", help="return right after uploading")
    scan.add_argument("--wait", type=wait_seconds, default=SCAN_WAIT_S, metavar="SECONDS",
                      help="wait at most this long (default %(default)s)")
    scan.add_argument("--images", action="store_true", help="also download part images into images/")
    scan.set_defaults(func=cmd_scan)
    status = sub.add_parser("status", help="check pending (or the given) tasks and collect finished ones")
    status.add_argument("task_ids", nargs="*", metavar="TASK_ID")
    status.add_argument("--wait", type=wait_seconds, default=0, metavar="SECONDS",
                        help="keep polling up to this long (default 0: check once)")
    status.add_argument("--images", action="store_true", help="also download part images into images/")
    status.set_defaults(func=cmd_status)
    parts = sub.add_parser("parts", help="collect finished tasks, then refresh parts.json from the server")
    parts.add_argument("--images", action="store_true", help="also download part images into images/")
    parts.set_defaults(func=cmd_parts)
    whoami = sub.add_parser("whoami", help="show user ID, server and local directory")
    whoami.set_defaults(func=cmd_whoami)

    moc = sub.add_parser("moc", help="design check: guide, submit a model, check a submission")
    moc_sub = moc.add_subparsers(dest="moc_command", metavar="MOC_COMMAND")
    moc_sub.required = True
    guide = moc_sub.add_parser("guide", help="download the design guide and the connector sheets of your parts")
    guide.add_argument("--parts-file", metavar="PATH", help="inventory to use instead of parts.json")
    guide.add_argument("--parts", metavar="LIST", help="comma-separated LDraw part numbers to fetch connector sheets "
                                                       "for instead of the inventory's (free build)")
    guide.set_defaults(func=cmd_moc_guide)
    find = moc_sub.add_parser("find", help="look up supported part numbers by name words (free build)")
    find.add_argument("words", nargs="+", metavar="WORD", help="words from the LDraw part name, or a part number prefix")
    find.add_argument("--offset", type=int, default=0, metavar="N", help="skip the first N matches")
    find.set_defaults(func=cmd_moc_find)
    submit = moc_sub.add_parser("submit", help="submit an LDraw model for the check and wait for the result")
    submit.add_argument("model", metavar="MODEL.ldr", help="the LDraw model file")
    submit.add_argument("--title", metavar="NAME", help="name of the model, at most 80 characters")
    submit.add_argument("--brief", metavar="TEXT", help="the user's request in their own words, at most 500 characters")
    submit.add_argument("--design", metavar="design.json", help="optional design file (title, description, motions)")
    submit.add_argument("--moc", metavar="MOC_ID", help="submit a new version of this existing MOC")
    submit.add_argument("--mode", choices=("inventory", "free"),
                        help="inventory: only parts you own (default); free: free build, any supported part in any "
                             "colour and quantity, not checked against the inventory")
    submit.add_argument("--parts-file", metavar="PATH", help="inventory to send instead of parts.json")
    submit.add_argument("--no-wait", action="store_true", help="return right after submitting")
    submit.add_argument("--wait", type=wait_seconds, default=MOC_WAIT_S, metavar="SECONDS",
                        help="wait at most this long (default %(default)s)")
    submit.set_defaults(func=cmd_moc_submit)
    mstatus = moc_sub.add_parser("status", help="check pending (or the given) MOC submission and fetch its report")
    mstatus.add_argument("moc_id", nargs="?", metavar="MOC_ID")
    mstatus.add_argument("--wait", type=wait_seconds, default=0, metavar="SECONDS",
                         help="keep polling up to this long (default 0: check once)")
    mstatus.set_defaults(func=cmd_moc_status)

    mcp = sub.add_parser("mcp", help="run as a local MCP server on stdin/stdout (agent hosts start it themselves)")
    mcp.set_defaults(func=None)
    mcp_config = sub.add_parser("mcp-config", help="print the JSON to paste into an agent host's MCP settings")
    mcp_config.add_argument("--remote", action="store_true",
                            help="the server's own MCP address (contains the user ID; no photo upload) instead of "
                                 "the local bridge")
    mcp_config.set_defaults(func=None)
    return parser


def main(argv=None):
    setup_stdout()
    raw_args = sys.argv[1:] if argv is None else list(argv)
    if raw_args[:1] in (["mcp"], ["mcp-config"]):  # no RESULT line: stdout belongs to the protocol / the JSON
        return mcp_main(raw_args)
    ctx = new_ctx()
    rep = new_report(None)
    if raw_args[:1] == ["moc"]:  # so that even a usage error gets the moc RESULT fields
        rep["command"] = "moc"
    try:
        try:
            args = build_parser().parse_args(argv)
        except SystemExit as e:
            if e.code in (0, None):  # --help
                return EXIT_OK
            raise UsageError("invalid arguments (see the usage message above)")
        rep["command"] = args.command if args.command != "moc" else "moc " + args.moc_command
        code = args.func(ctx, rep, args)
        if code is None:
            code = exit_code(rep)
    except UsageError as e:
        say("USAGE ERROR:", e)
        rep["errors"].append(str(e))
        code = EXIT_USAGE
    except Fatal as e:
        say("ERROR:", e)
        rep["errors"].append(str(e))
        code = EXIT_ERROR
    except ApiError as e:
        say("ERROR:", describe(e))
        rep["errors"].append(describe(e))
        code = EXIT_ERROR
    except KeyboardInterrupt:
        msg = "interrupted. Submitted task IDs are kept in pending.json; run status to collect them."
        if (rep["command"] or "").startswith("moc"):
            msg = "interrupted. A submitted MOC ID is kept in moc/pending.json; run moc status to fetch its result."
        say("ERROR:", msg)
        rep["errors"].append(msg)
        code = EXIT_ERROR
    except Exception as e:  # a bug: show it, but still end with a RESULT line
        traceback.print_exc(file=sys.stdout)
        rep["errors"].append("internal error: {!r}".format(e))
        code = EXIT_ERROR
    emit_result(ctx, rep, code)
    return code


if __name__ == "__main__":
    sys.exit(main())
