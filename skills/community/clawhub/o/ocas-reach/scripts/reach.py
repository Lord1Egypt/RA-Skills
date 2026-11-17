#!/usr/bin/env python3
"""
Reach orchestrator — routes queries to registered sources.

Usage:
  reach.py query <source> <action> [params_json]
  reach.py sources                          # list registered sources
  reach.py source <name>                    # show one source's actions + auth + quota
  reach.py usage [--month YYYY-MM]          # show usage tally per source

Auth: each source declares its env var. Missing required auth → exit 1
with an actionable message. Per-source monthly/daily quotas are enforced
from {agent_root}/commons/data/ocas-reach/usage.jsonl.
"""
import json
import os
import sys
import time
import urllib.parse
import urllib.request
import urllib.error
import importlib
import re
from datetime import datetime, timezone
from pathlib import Path
from _load_yaml import _load_yaml_min

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent.parent
REGISTRY = SCRIPT_DIR / "sources.yml"
USAGE_LOG = Path(os.environ.get("HERMES_HOME", Path.home() / ".hermes")) / "commons/data/ocas-reach/usage.jsonl"
DATA_DIR = Path(os.environ.get("HERMES_HOME", Path.home() / ".hermes")) / "commons/data/ocas-reach"
JOURNAL_DIR = Path(os.environ.get("HERMES_HOME", Path.home() / ".hermes")) / "commons/journals/ocas-reach"

USER_AGENT = "ocas-reach (contact: " + os.environ.get("OCAS_AGENT_EMAIL", "agent@example.com") + ")"

# ---------------------------------------------------------------------------
# Registry access
# ---------------------------------------------------------------------------
def load_registry():
    if not REGISTRY.exists():
        return {"sources": {}}
    text = REGISTRY.read_text()
    data = _load_yaml_min(text)
    if not isinstance(data, dict) or "sources" not in data:
        raise SystemExit(f"sources.yml malformed: top-level must contain 'sources:' mapping (got {type(data).__name__})")
    return data


def get_source(registry, name):
    src = registry.get("sources", {}).get(name)
    if not src:
        raise SystemExit(f"Unknown source: {name!r}. Run `reach.py sources` to list registered sources.")
    return src


# ---------------------------------------------------------------------------
# Auth resolution
# ---------------------------------------------------------------------------
def resolve_auth(source):
    auth = source.get("auth", "none")
    if auth in (None, "none"):
        return None
    env_var = source.get("env_var")
    if not env_var:
        return None
    val = os.environ.get(env_var)
    if not val and auth == "required":
        msg = f"Auth required for {source.get('name', '?')}: set {env_var} in ~/.hermes/.env"
        if source.get("account_url"):
            msg += f"\nRegister an account at: {source['account_url']}"
        print(msg, file=sys.stderr)
        sys.exit(1)
    return val


# ---------------------------------------------------------------------------
# Quota enforcement
# ---------------------------------------------------------------------------
def quota_remaining(name, source):
    monthly = source.get("monthly")
    daily = source.get("daily")
    if not monthly and not daily:
        return {"daily_remaining": None, "monthly_remaining": None}
    now = datetime.now(timezone.utc)
    today_prefix = now.strftime("%Y-%m-%d")
    month_prefix = now.strftime("%Y-%m")
    used_today = 0
    used_month = 0
    if USAGE_LOG.exists():
        for line in USAGE_LOG.read_text().splitlines():
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except Exception:
                continue
            if row.get("source") != name or row.get("status") == "quota_blocked":
                continue
            ts = row.get("ts", "")
            if ts.startswith(today_prefix):
                used_today += 1
            if ts.startswith(month_prefix):
                used_month += 1
    return {
        "daily_used": used_today,
        "daily_remaining": (daily - used_today) if daily else None,
        "monthly_used": used_month,
        "monthly_remaining": (monthly - used_month) if monthly else None,
    }


def check_quota(name, source):
    q = quota_remaining(name, source)
    if q["daily_remaining"] is not None and q["daily_remaining"] <= 0:
        return ("daily", q)
    if q["monthly_remaining"] is not None and q["monthly_remaining"] <= 0:
        return ("monthly", q)
    return (None, q)


# ---------------------------------------------------------------------------
# HTTP (stdlib-only)
# ---------------------------------------------------------------------------
def http_call(method, url, headers=None, body=None):
    headers = dict(headers or {})
    headers.setdefault("User-Agent", USER_AGENT)
    headers.setdefault("Accept", "application/json")
    data = None
    if body is not None:
        if headers.get("Content-Type") == "text/plain":
            data = body if isinstance(body, bytes) else body.encode()
        else:
            headers.setdefault("Content-Type", "application/json")
            data = json.dumps(body).encode() if not isinstance(body, (bytes, str)) else (body.encode() if isinstance(body, str) else body)
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read()
            ct = resp.headers.get("Content-Type", "")
            if "json" in ct or raw.startswith(b"{") or raw.startswith(b"["):
                try:
                    return {"ok": True, "status": resp.status, "data": json.loads(raw.decode("utf-8", "replace"))}
                except Exception:
                    pass
            return {"ok": True, "status": resp.status, "data": raw.decode("utf-8", "replace")}
    except urllib.error.HTTPError as e:
        body_text = e.read().decode("utf-8", "replace")[:1000]
        # Actionable error envelope: retry-backoff guidance per spec-ocas-scripts.md
        guidance = (
            "Retry after backoff if status in (429, 500, 502, 503, 504): "
            "wait 2**(retry+1)*5s then re-issue; for 401/403 verify the API key/credential; "
            "for 404 verify the request path/params; escalate lingering 5xx to the source status page."
        )
        return {"ok": False, "error": "http_error", "status": e.code, "message": body_text,
                "actionable_guidance": guidance}
    except urllib.error.URLError as e:
        return {"ok": False, "error": "network_error", "message": str(e.reason),
                "actionable_guidance": "Network unreachable (DNS, timeout, connection reset). Retry with backoff; if persistent, check the source endpoint reachability and local connectivity."}


# ---------------------------------------------------------------------------
# Generic dispatch (when source has no `custom` module)
# ---------------------------------------------------------------------------
def _format_path(path, params):
    used = set()

    def repl(match):
        key = match.group(1)
        used.add(key)
        if key not in params:
            raise SystemExit(f"Missing required path param: {key!r}")
        return urllib.parse.quote(str(params[key]), safe="/,")

    out = re.sub(r"\{([a-zA-Z_][a-zA-Z0-9_]*)\}", repl, path or "")
    return out, used


def dispatch_generic(source, action_name, params, auth_value):
    actions = source.get("actions", {}) or {}
    action = actions.get(action_name)
    if not action:
        raise SystemExit(f"Unknown action {action_name!r} for source {source.get('name', '?')}. "
                         f"Available: {sorted(actions.keys())}")
    method = (action.get("method") or "GET").upper()
    base = action.get("base_override") or source.get("base_url")
    if not base:
        raise SystemExit("Source has no base_url and action has no base_override.")
    path = action.get("path") or ""
    defaults = action.get("defaults") or {}
    params_in = action.get("params_in") or "query"
    headers = {}
    body = None

    # Merge defaults with user params (user wins)
    merged = dict(defaults)
    merged.update(params or {})

    # Auth injection
    if auth_value:
        if action.get("auth_param"):
            merged[action["auth_param"]] = auth_value
        elif action.get("auth_field") and params_in == "body":
            merged[action["auth_field"]] = auth_value
        elif action.get("auth_header"):
            prefix = action.get("auth_prefix", "")
            headers[action["auth_header"]] = f"{prefix}{auth_value}"

    # Path substitution
    formatted_path, used_keys = _format_path(path, merged)
    for k in used_keys:
        merged.pop(k, None)

    url = base.rstrip("/") + formatted_path

    if params_in == "query":
        if merged:
            qs = urllib.parse.urlencode(merged, doseq=True)
            url = f"{url}?{qs}"
    elif params_in == "body":
        body = merged
        if action.get("content_type") == "text/plain":
            headers["Content-Type"] = "text/plain"
            body = merged.get("query") or merged.get("data") or ""
    elif params_in == "path":
        pass  # already done
    else:
        raise SystemExit(f"Unsupported params_in: {params_in}")

    return http_call(method, url, headers=headers, body=body)


# ---------------------------------------------------------------------------
# Logging + journaling
# ---------------------------------------------------------------------------
def _ensure_dirs():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    JOURNAL_DIR.mkdir(parents=True, exist_ok=True)


def log_usage(source_name, action, status, extra=None):
    _ensure_dirs()
    row = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "source": source_name,
        "action": action,
        "status": status,
    }
    if extra:
        row.update(extra)
    with USAGE_LOG.open("a") as f:
        f.write(json.dumps(row) + "\n")


def write_journal(source_name, action, params, result, outcome):
    _ensure_dirs()
    now = datetime.now(timezone.utc)
    day_dir = JOURNAL_DIR / now.strftime("%Y-%m-%d")
    day_dir.mkdir(parents=True, exist_ok=True)
    run_id = now.strftime("%Y%m%dT%H%M%SZ") + f"-{source_name}-{action}"
    payload = {
        "skill": "ocas-reach",
        "run_id": run_id,
        "kind": "observation",
        "ts": now.isoformat(),
        "source": source_name,
        "action": action,
        "params": params,
        "outcome": outcome,
    }
    if isinstance(result, dict):
        # Don't bloat journal with full data — just citation/meta if present
        meta = {k: v for k, v in result.items() if k in ("status", "error", "message")}
        if isinstance(result.get("data"), dict):
            for k in ("meta", "citation", "quality"):
                if k in result["data"]:
                    meta[k] = result["data"][k]
        payload["result_meta"] = meta
    (day_dir / f"{run_id}.json").write_text(json.dumps(payload, indent=2))


# ---------------------------------------------------------------------------
# Top-level commands
# ---------------------------------------------------------------------------
def cmd_query(source_name, action_name, params):
    registry = load_registry()
    source = get_source(registry, source_name)
    source["name"] = source_name

    # Quota check
    blocked, quota = check_quota(source_name, source)
    if blocked:
        envelope = {
            "ok": False,
            "error": "quota_exhausted",
            "scope": blocked,
            "quota": quota,
            "source": source_name,
            "action": action_name,
        }
        log_usage(source_name, action_name, "quota_blocked", {"quota": quota})
        write_journal(source_name, action_name, params, envelope, "quota_blocked")
        print(json.dumps(envelope, indent=2))
        return 2

    auth_value = resolve_auth(source)

    # Custom module override
    if source.get("custom"):
        try:
            mod = importlib.import_module(f"sources.{source['custom']}")
        except ImportError:
            sys.path.insert(0, str(SKILL_DIR / "scripts"))
            mod = importlib.import_module(f"sources.{source['custom']}")
        try:
            data = mod.query(action_name, params or {}, {"value": auth_value, "user_agent": USER_AGENT})
            result = {"ok": True, "data": data}
        except Exception as e:
            result = {"ok": False, "error": "source_error", "message": str(e), "source": source_name, "action": action_name}
    else:
        result = dispatch_generic(source, action_name, params or {}, auth_value)

    outcome = "success" if result.get("ok") else result.get("error", "error")
    log_usage(source_name, action_name, outcome, {"http_status": result.get("status")})
    write_journal(source_name, action_name, params, result, outcome)
    print(json.dumps(result, indent=2, default=str))
    return 0 if result.get("ok") else 1


def cmd_sources():
    registry = load_registry()
    rows = []
    for name, src in sorted(registry.get("sources", {}).items()):
        auth = src.get("auth") or "none"
        env = src.get("env_var") or "—"
        cat = src.get("category") or "—"
        daily = src.get("daily") or "—"
        monthly = src.get("monthly") or "—"
        ref = src.get("reference") or "—"
        rows.append({
            "name": name, "category": cat, "auth": auth, "env_var": env,
            "daily": daily, "monthly": monthly, "reference": ref,
        })
    print(json.dumps({"sources": rows, "count": len(rows)}, indent=2))


def cmd_source(name):
    registry = load_registry()
    src = get_source(registry, name)
    src["name"] = name
    quota = quota_remaining(name, src)
    out = dict(src)
    out["quota"] = quota
    print(json.dumps(out, indent=2, default=str))


def cmd_usage(month=None):
    if not USAGE_LOG.exists():
        print(json.dumps({"summary": {}, "month": month}, indent=2))
        return
    by_source = {}
    for line in USAGE_LOG.read_text().splitlines():
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except Exception:
            continue
        ts = row.get("ts", "")
        if month and not ts.startswith(month):
            continue
        s = row.get("source", "?")
        bucket = by_source.setdefault(s, {"calls": 0, "errors": 0, "blocked": 0})
        bucket["calls"] += 1
        if row.get("status") in ("quota_blocked",):
            bucket["blocked"] += 1
        elif row.get("status") not in ("success",):
            bucket["errors"] += 1
    print(json.dumps({"summary": by_source, "month": month or "all"}, indent=2))


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------
def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)
    cmd = sys.argv[1]
    if cmd == "query":
        if len(sys.argv) < 4:
            print("Usage: reach.py query <source> <action> [params_json]", file=sys.stderr)
            sys.exit(1)
        params = {}
        if len(sys.argv) > 4:
            try:
                params = json.loads(sys.argv[4])
            except json.JSONDecodeError as e:
                print(f"Invalid JSON params: {e}", file=sys.stderr)
                sys.exit(1)
        sys.exit(cmd_query(sys.argv[2], sys.argv[3], params))
    elif cmd == "sources":
        cmd_sources()
    elif cmd == "source":
        if len(sys.argv) < 3:
            print("Usage: reach.py source <name>", file=sys.stderr)
            sys.exit(1)
        cmd_source(sys.argv[2])
    elif cmd == "usage":
        month = None
        if "--month" in sys.argv:
            i = sys.argv.index("--month")
            month = sys.argv[i + 1] if i + 1 < len(sys.argv) else None
        cmd_usage(month)
    else:
        print(f"Unknown command: {cmd}", file=sys.stderr)
        print(__doc__, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
