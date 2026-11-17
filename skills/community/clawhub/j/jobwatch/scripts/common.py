"""JobWatcher shared helpers: env, HTTP (stdlib only), state, logging."""
import json
import os
import sys
import time
import uuid
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent


def _resolve_home():
    """运行数据主目录。

    优先 env JOBWATCH_HOME；否则：若本 skill 安装在 <workspace>/skills/jobwatch/
    下，数据放 <workspace>/jobwatch/（skill 目录保持只读、可随时升级重装）；
    若是独立工作区形态（template/作业实例），数据就在工作区根目录。
    """
    env = os.environ.get("JOBWATCH_HOME")
    if env:
        return Path(env).expanduser()
    parts = SKILL_DIR.parts
    if "skills" in parts:
        ws = Path(*parts[: parts.index("skills")])
        return ws / "jobwatch"
    return SKILL_DIR


ROOT = _resolve_home()


def _load_config():
    """HOME/config.json（用户态，入职时生成/修改）→ 缺省回退 skill 自带默认值。"""
    user_cfg = ROOT / "config.json"
    if user_cfg.exists():
        return json.loads(user_cfg.read_text())
    default = SKILL_DIR / "config.default.json"
    if default.exists():
        ROOT.mkdir(parents=True, exist_ok=True)
        user_cfg.write_text(default.read_text())  # 首跑落地一份供用户/入职流程修改
        return json.loads(user_cfg.read_text())
    return json.loads((SKILL_DIR / "config.json").read_text())


CONFIG = _load_config()
STATE_FILE = ROOT / "state" / "seen_jobs.json"
QUEUE_FILE = ROOT / "queue" / "p2_digest.jsonl"
RUNS_DIR = ROOT / "runs"

OPENCLAW_DIR = Path(os.environ.get("OPENCLAW_DIR", str(Path.home() / ".openclaw")))


def load_env():
    """Load ROOT/.env into os.environ (existing env wins)."""
    for env_file in (ROOT / ".env", SKILL_DIR / ".env"):
        if env_file.exists():
            _parse_env(env_file)


def _parse_env(env_file):
    for line in env_file.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        os.environ.setdefault(k.strip(), v.strip())


load_env()


def now_iso():
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def http(url, method="GET", headers=None, data=None, json_body=None, timeout=45):
    """Returns (status_code, body_bytes). Raises on network errors."""
    h = {"User-Agent": "JobWatch/1.0 (personal job monitor)"}
    if headers:
        h.update(headers)
    body = data
    if json_body is not None:
        body = json.dumps(json_body).encode()
        h.setdefault("Content-Type", "application/json")
    req = urllib.request.Request(url, data=body, headers=h, method=method)
    import http.client
    for attempt in (1, 2):  # 瞬断（截断/重置/超时）自动重试一次
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.status, r.read()
        except urllib.error.HTTPError as e:
            return e.code, e.read()
        except (http.client.IncompleteRead, ConnectionResetError, TimeoutError,
                urllib.error.URLError) as e:
            if attempt == 2:
                raise
            time.sleep(2)


def http_json(url, **kw):
    status, body = http(url, **kw)
    if status >= 300:
        raise RuntimeError(f"HTTP {status} for {url}: {body[:300]!r}")
    return json.loads(body)


def multipart_post(url, fields, file_field, filename, file_bytes,
                   content_type="text/markdown", headers=None, timeout=120):
    """Multipart/form-data POST using stdlib only."""
    boundary = f"----jobwatch{uuid.uuid4().hex}"
    parts = []
    for k, v in (fields or {}).items():
        parts.append(
            f"--{boundary}\r\nContent-Disposition: form-data; name=\"{k}\"\r\n\r\n{v}\r\n".encode()
        )
    parts.append(
        (f"--{boundary}\r\nContent-Disposition: form-data; name=\"{file_field}\"; "
         f"filename=\"{filename}\"\r\nContent-Type: {content_type}\r\n\r\n").encode()
        + file_bytes + b"\r\n"
    )
    parts.append(f"--{boundary}--\r\n".encode())
    body = b"".join(parts)
    h = {"Content-Type": f"multipart/form-data; boundary={boundary}"}
    if headers:
        h.update(headers)
    return http(url, method="POST", headers=h, data=body, timeout=timeout)


# ---------- egress consent (runtime gate) ----------
# This skill sends data to third parties. The rule enforced here, in code and not
# only in documentation: every outbound call that carries user data must first pass
# through require_egress_consent(), which fails closed and prints exactly what is
# about to leave the machine and where it is going.
#
# Consent is granted per destination, by either:
#   - JOBWATCH_EGRESS_ALLOW="llm,firecrawl,jina,twobrain,telegram" (or "all"), or
#   - a consent record written during onboarding at <HOME>/state/egress_consent.json
# Calls to public ATS job boards (Greenhouse / Ashby / Lever) send only the company
# slug you configured, which is public information, and are therefore not gated.

EGRESS_TARGETS = {
    "llm": "the full text of your JOB_PROFILE.md and the full job-description text",
    "firecrawl": "the URL of a job posting you are watching",
    "jina": "the URL of a job posting you are watching",
    "twobrain": "archived job-description documents and the questions you ask",
    "telegram": "the notification message body",
}
_EGRESS_WARNED = set()


def _egress_allowed(target):
    env = os.environ.get("JOBWATCH_EGRESS_ALLOW", "").strip().lower()
    if env in ("all", "*"):
        return True
    if target in [t.strip() for t in env.split(",") if t.strip()]:
        return True
    record = ROOT / "state" / "egress_consent.json"
    if record.exists():
        try:
            granted = json.loads(record.read_text()).get("granted", [])
            return target in granted or "all" in granted
        except (OSError, ValueError):
            return False
    return False


def require_egress_consent(target, detail=None):
    """Fail closed unless the user has consented to this destination.

    Raises RuntimeError when consent is absent, and prints a one-line warning to
    stderr the first time each destination is used in a run, so the transmission is
    never silent.
    """
    what = detail or EGRESS_TARGETS.get(target, "user data")
    if not _egress_allowed(target):
        raise RuntimeError(
            f"jobwatch: refusing to send data to '{target}' without consent.\n"
            f"  About to send: {what}\n"
            f"  To allow, either re-run onboarding, or set "
            f"JOBWATCH_EGRESS_ALLOW={target} (comma-separated, or 'all')."
        )
    if target not in _EGRESS_WARNED:
        _EGRESS_WARNED.add(target)
        print(f"[jobwatch] sending to '{target}': {what}", file=sys.stderr)
    return True


# ---------- credentials ----------
# Least privilege: by default this skill reads only the keys you put in HOME/.env.
# Reading credentials that belong to the host (the OpenClaw auth store, or the bot
# token in openclaw.json) is a cross-scope read. It is OFF by default and happens
# only when the user explicitly sets JOBWATCH_ALLOW_HOST_CREDS=1. When it does
# happen, a warning is printed so the read is never silent.
# See SKILL.md, "Privacy & Data Flow — ③ credential reads".

_HOST_CRED_WARNED = set()

# Exactly three host credentials can ever be read, each behind its own name so the
# opt-in can be scoped to one rather than granted wholesale.
HOST_CRED_SCOPES = ("openrouter", "telegram_token", "telegram_chat")


def _host_creds_allowed(scope):
    """True only if the user opted in to *this specific* host credential.

    JOBWATCH_ALLOW_HOST_CREDS accepts a comma-separated list of the scopes above —
    e.g. "telegram_token" grants the bot token and nothing else. The legacy values
    1/true/yes/all still grant all three, so existing setups keep working.
    """
    raw = os.environ.get("JOBWATCH_ALLOW_HOST_CREDS", "").strip().lower()
    if not raw:
        return False
    if raw in ("1", "true", "yes", "all", "*"):
        return True
    return scope in [s.strip() for s in raw.split(",") if s.strip()]


def _warn_host_cred_read(what):
    if what not in _HOST_CRED_WARNED:
        _HOST_CRED_WARNED.add(what)
        print(
            f"[jobwatch] reading host credential ({what}) because "
            f"JOBWATCH_ALLOW_HOST_CREDS=1. Unset it to keep this skill to its own .env.",
            file=sys.stderr,
        )


def _openrouter_key_from_store():
    """OpenClaw 凭证存储兜底：旧版 JSON 文件 → 新版（2026.7.1+）SQLite。
    仅在 JOBWATCH_ALLOW_HOST_CREDS 开启时读取宿主 auth store。"""
    if not _host_creds_allowed("openrouter"):
        return None
    _warn_host_cred_read("OpenClaw OpenRouter key")
    legacy = OPENCLAW_DIR / "agents" / "main" / "agent" / "auth-profiles.json"
    if legacy.exists():
        profiles = json.loads(legacy.read_text()).get("profiles", {})
        key = (profiles.get("openrouter:default") or {}).get("key")
        if key:
            return key
    db = OPENCLAW_DIR / "agents" / "main" / "agent" / "openclaw-agent.sqlite"
    if db.exists():
        try:
            import sqlite3
            con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
            row = con.execute(
                "SELECT store_json FROM auth_profile_store WHERE store_key='primary'"
            ).fetchone()
            con.close()
            if row:
                profiles = json.loads(row[0]).get("profiles", {})
                key = (profiles.get("openrouter:default") or {}).get("key")
                if key:
                    return key
        except Exception:  # noqa: BLE001
            pass
    return None


def openrouter_key():
    k = os.environ.get("OPENROUTER_API_KEY") or _openrouter_key_from_store()
    if k:
        return k
    raise RuntimeError(
        "No OpenRouter API key found. 在 HOME/.env 填 OPENROUTER_API_KEY；"
        "或设 JOBWATCH_ALLOW_HOST_CREDS=1 复用 OpenClaw 已存的 key。")


def telegram_token():
    t = os.environ.get("TELEGRAM_BOT_TOKEN")
    if t:
        return t
    if _host_creds_allowed("telegram_token"):  # 复用 openclaw.json 里的 bot token 需显式开启
        _warn_host_cred_read("Telegram bot token from openclaw.json")
        p = OPENCLAW_DIR / "openclaw.json"
        if p.exists():
            cfg = json.loads(p.read_text())
            tok = cfg.get("channels", {}).get("telegram", {}).get("botToken")
            if tok:
                return tok
    raise RuntimeError("No Telegram bot token (env TELEGRAM_BOT_TOKEN；或 JOBWATCH_ALLOW_HOST_CREDS=1 复用 openclaw.json)")


def telegram_chat_id():
    cid = os.environ.get("TELEGRAM_CHAT_ID") or CONFIG["telegram"].get("chat_id")
    if cid:
        return cid
    if _host_creds_allowed("telegram_chat"):  # 复用 openclaw allowFrom 需显式开启
        _warn_host_cred_read("Telegram allowFrom list from OpenClaw credentials")
        p = OPENCLAW_DIR / "credentials" / "telegram-default-allowFrom.json"
        if p.exists():
            allow = json.loads(p.read_text()).get("allowFrom", [])
            if allow:
                return str(allow[0])
    raise RuntimeError("No Telegram chat id (env TELEGRAM_CHAT_ID / config.json；或 JOBWATCH_ALLOW_HOST_CREDS=1)")


# ---------- endpoint / credential binding ----------
# A credential is only ever attached to the endpoint it was issued for. Without
# this rule a user who points LLM_BASE_URL (or screen.base_url) at an arbitrary
# host would silently ship their OpenRouter Bearer token — possibly the *host*
# OpenClaw one — to that host. Provider A's key must never travel to provider B.

OPENROUTER_HOST = "openrouter.ai"
_CRED_WARNED = set()


def endpoint_host(url):
    from urllib.parse import urlparse
    return (urlparse(url).hostname or "").lower()


def _is_local(host):
    return host in ("localhost", "127.0.0.1", "::1", "") or host.endswith(".local")


def _warn_no_cred(host, hint):
    if host not in _CRED_WARNED:
        _CRED_WARNED.add(host)
        print(f"[jobwatch] sending no credential to '{host}' — {hint}", file=sys.stderr)


def credential_for_endpoint(base_url, purpose="judge"):
    """The API key the user provisioned *for this endpoint*, or "" if none.

    judge  : LLM_API_KEY is paired with LLM_BASE_URL / config judge.base_url by the
             user, so it is sent to that endpoint. OPENROUTER_API_KEY and the host
             OpenClaw OpenRouter key belong to OpenRouter and go nowhere else.
    screen : an overridden screen.base_url is a *separate* endpoint and never
             inherits the judge credential — it needs SCREEN_LLM_API_KEY. Pointing
             screen at a local model therefore needs no key at all, which is the
             intended zero-cost setup.
    """
    host = endpoint_host(base_url)
    if purpose == "screen":
        key = os.environ.get("SCREEN_LLM_API_KEY")
        if key:
            return key
        # Same endpoint as judge → same credential is legitimately in scope.
        judge_base = (os.environ.get("LLM_BASE_URL")
                      or CONFIG.get("judge", {}).get("base_url")
                      or f"https://{OPENROUTER_HOST}/api/v1")
        if host and host == endpoint_host(judge_base):
            return credential_for_endpoint(base_url, purpose="judge")
        if host == OPENROUTER_HOST:
            return _openrouter_credential()
        if not _is_local(host):
            _warn_no_cred(host, "set SCREEN_LLM_API_KEY if this endpoint needs one "
                                "(the judge/OpenRouter key is deliberately not reused)")
        return ""
    key = os.environ.get("LLM_API_KEY")
    if key:
        return key
    if host == OPENROUTER_HOST:
        return _openrouter_credential()
    if not _is_local(host):
        _warn_no_cred(host, "set LLM_API_KEY if this endpoint needs one "
                            "(your OpenRouter key is deliberately not reused)")
    return ""


def _openrouter_credential():
    try:
        return openrouter_key()
    except RuntimeError:
        return ""


# ---------- state ----------

def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {}


def save_state(state):
    STATE_FILE.parent.mkdir(exist_ok=True)
    tmp = STATE_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, ensure_ascii=False, indent=1))
    tmp.replace(STATE_FILE)


def append_queue(record):
    QUEUE_FILE.parent.mkdir(exist_ok=True)
    with QUEUE_FILE.open("a") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def log_run(record):
    RUNS_DIR.mkdir(exist_ok=True)
    record.setdefault("ts", now_iso())
    day = datetime.now().strftime("%Y-%m-%d")
    with (RUNS_DIR / f"{day}.jsonl").open("a") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


OUTBOX_FILE = ROOT / "queue" / "outbox.jsonl"
PENDING_FILE = ROOT / "queue" / "pending_judgment.jsonl"
JUDGMENTS_FILE = ROOT / "queue" / "judgments.jsonl"


def judge_mode():
    """agent（默认，零配置：判级交给被唤醒的 agent 本人）| api（OpenAI 兼容端点）"""
    return os.environ.get("JUDGE_MODE") or CONFIG.get("judge", {}).get("mode", "agent")


def notify_mode():
    """agent（默认：消息写 outbox，由 agent 用任意渠道播报）| telegram（直连 bot API）"""
    return os.environ.get("NOTIFY_MODE") or CONFIG.get("notify", {}).get("mode", "agent")


def append_outbox(kind, text, meta=None):
    OUTBOX_FILE.parent.mkdir(exist_ok=True)
    with OUTBOX_FILE.open("a") as f:
        f.write(json.dumps({"ts": now_iso(), "kind": kind, "text": text,
                            "meta": meta or {}}, ensure_ascii=False) + "\n")


def kb_hint():
    """通知消息里的知识库提示行，随 KB 后端自适应。"""
    import os
    backend = os.environ.get("KB_BACKEND") or CONFIG.get("kb", {}).get("backend", "local")
    if backend == "twobrain":
        return f"已入库 2brain，可提问追溯：{CONFIG['twobrain']['ask_url']}"
    return "已入库本地知识库（kb_local/）"


def slug(text, maxlen=48):
    out = "".join(c if c.isalnum() else "-" for c in text.lower())
    while "--" in out:
        out = out.replace("--", "-")
    return out.strip("-")[:maxlen]
