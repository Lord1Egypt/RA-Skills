#!/usr/bin/env python3
import argparse
import hashlib
import json
import os
import re
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, Optional
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen

DEFAULT_API_URL = "https://pengbo.space/api/v1"
ALLOWED_API_HOSTS = {"pengbo.space"}
DEFAULT_TIMEOUT = 20
DEFAULT_RETRIES = 2
DEFAULT_RETRY_DELAY = 1.5
DEFAULT_CACHE_MAX_AGE_DAYS = 8
IDEMPOTENCY_WINDOW_SECONDS = 30
LANG_STATE_FILE = "language-state.json"

SUPPORTED_LANGS = {"zh", "en", "es", "mixed", "auto"}


class SkillError(Exception):
    pass


class MissingApiKeyError(SkillError):
    pass


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def get_lang_state_path() -> Path:
    return get_data_dir() / LANG_STATE_FILE


def detect_lang(text: str) -> str:
    if not text:
        return "zh"
    t = text.strip()
    if not t:
        return "zh"
    tl = t.lower()
    zh = len(re.findall(r"[\u4e00-\u9fff]", t))
    es_mark = len(re.findall(r"[áéíóúñ¿¡ÁÉÍÓÚÑ]", t))
    latin_words = len(re.findall(r"[A-Za-z]{2,}", t))
    es_words = {"hola", "gracias", "pedido", "orden", "ayuda", "por", "favor", "necesito", "estado"}
    es_hits = sum(1 for w in re.findall(r"[a-záéíóúñ]+", tl) if w in es_words)
    if zh > 0 and latin_words > 0:
        return "mixed"
    if zh > 0:
        return "zh"
    if es_mark > 0 or es_hits >= 2:
        return "es"
    return "en"


def resolve_lang(args) -> str:
    raw = (getattr(args, "lang", "auto") or "auto").lower()
    if raw not in SUPPORTED_LANGS:
        raw = "auto"
    if raw != "auto":
        return raw

    state = read_json(get_lang_state_path()) or {}
    if state.get("lang") in {"zh", "en", "es", "mixed"}:
        return state["lang"]

    hint = getattr(args, "input_text", "") or ""
    return detect_lang(hint)


def remember_lang(lang: str):
    if lang not in {"zh", "en", "es", "mixed"}:
        return
    write_json(get_lang_state_path(), {"lang": lang, "updated_at": now_iso()})


def t(lang: str, key: str) -> str:
    lex = {
        "setup_login": {
            "zh": "登录 https://pengbo.space",
            "en": "Log in at https://pengbo.space",
            "es": "Inicia sesión en https://pengbo.space",
            "mixed": "登录 / Log in: https://pengbo.space",
        },
        "setup_get_key": {
            "zh": "到 https://pengbo.space/user/api/docs 获取 key",
            "en": "Get your API key at https://pengbo.space/user/api/docs",
            "es": "Obtén tu API key en https://pengbo.space/user/api/docs",
            "mixed": "获取 API key: https://pengbo.space/user/api/docs",
        },
        "setup_export_key": {
            "zh": "export PENGBO_API_KEY=\"<your_api_key>\"",
            "en": "export PENGBO_API_KEY=\"<your_api_key>\"",
            "es": "export PENGBO_API_KEY=\"<your_api_key>\"",
            "mixed": "export PENGBO_API_KEY=\"<your_api_key>\"",
        },
        "welcome_title": {
            "zh": "🎉 欢迎使用 Pengbo Space Skill",
            "en": "🎉 Welcome to Pengbo Space Skill",
            "es": "🎉 Bienvenido a Pengbo Space Skill",
            "mixed": "🎉 欢迎 / Welcome to Pengbo Space Skill",
        },
        "welcome_step_login": {
            "zh": "登录账号： https://pengbo.space",
            "en": "Log in: https://pengbo.space",
            "es": "Inicia sesión: https://pengbo.space",
            "mixed": "登录账号 / Log in: https://pengbo.space",
        },
        "welcome_step_key": {
            "zh": "获取 API Key： https://pengbo.space/user/api/docs",
            "en": "Get API Key: https://pengbo.space/user/api/docs",
            "es": "Obtener API Key: https://pengbo.space/user/api/docs",
            "mixed": "获取 API Key: https://pengbo.space/user/api/docs",
        },
        "welcome_campaign": {
            "zh": "当前活动：充值多少送多少（1:1赠送），以平台页面实时说明为准。",
            "en": "Current campaign: recharge bonus 1:1. Final rules follow the platform page.",
            "es": "Promoción actual: bono de recarga 1:1. Consulta las reglas finales en la plataforma.",
            "mixed": "当前活动：1:1 bonus，以平台页面为准。",
        },
    }
    table = lex.get(key, {})
    return table.get(lang) or table.get("zh") or key


def make_ok(action: str, data: Any, meta: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    out = {"ok": True, "action": action, "data": data}
    if meta:
        out["meta"] = meta
    return out


def make_err(action: str, err: str, meta: Optional[Dict[str, Any]] = None, next_steps: Optional[list] = None) -> Dict[str, Any]:
    out = {"ok": False, "action": action, "error": err}
    if meta:
        out["meta"] = meta
    if next_steps:
        out["next_steps"] = next_steps
    return out


def missing_key_next_steps(lang: str = "zh") -> list:
    return [
        t(lang, "setup_login"),
        t(lang, "setup_get_key"),
        t(lang, "setup_export_key"),
    ]


def attach_onboarding_once(result: Dict[str, Any], command: str, lang: str) -> Dict[str, Any]:
    if not should_emit_onboarding():
        return result
    result["onboarding"] = get_onboarding_message(lang)
    mark_onboarding_shown(command, lang)
    return result


def get_skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def get_data_dir() -> Path:
    d = get_skill_root() / "data"
    d.mkdir(parents=True, exist_ok=True)
    return d


def normalize_host(base_url: str) -> str:
    host = urlparse(base_url).netloc or "unknown-host"
    host = host.replace(":", "_")
    return re.sub(r"[^a-zA-Z0-9._-]", "_", host)


def validate_base_url(base_url: str):
    u = urlparse(base_url)
    if u.scheme != "https":
        raise SkillError("base_url must use https")
    host = (u.hostname or "").lower()
    if host not in ALLOWED_API_HOSTS:
        raise SkillError(f"base_url host not allowed: {host}")


def key_hash(key: str, n: int = 10) -> str:
    return hashlib.sha256(key.encode("utf-8")).hexdigest()[:n]


def default_cache_path(base_url: str, key: str) -> Path:
    return get_data_dir() / f"services-cache_{normalize_host(base_url)}_{key_hash(key)}.json"


def get_orders_log_path() -> Path:
    return get_data_dir() / "orders-log.jsonl"


def get_idempotency_path() -> Path:
    return get_data_dir() / "idempotency.json"


def get_onboarding_path() -> Path:
    return get_data_dir() / "onboarding-state.json"


def get_onboarding_message(lang: str = "zh") -> Dict[str, Any]:
    return {
        "title": t(lang, "welcome_title"),
        "steps": [
            t(lang, "welcome_step_login"),
            t(lang, "welcome_step_key"),
        ],
        "campaign": t(lang, "welcome_campaign"),
    }


def should_emit_onboarding() -> bool:
    p = get_onboarding_path()
    obj = read_json(p) or {}
    return not bool(obj.get("shown"))


def mark_onboarding_shown(command: str, lang: str):
    p = get_onboarding_path()
    write_json(p, {"shown": True, "shown_at": now_iso(), "command": command, "lang": lang})


def get_key(args, required: bool = True) -> Optional[str]:
    k = args.key or os.getenv("PENGBO_API_KEY")
    if required and not k:
        raise MissingApiKeyError("missing_api_key")
    return k


def parse_json_safely(raw: str):
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"raw": raw}


def call_api(payload: dict, base_url: str, timeout: float, retries: int, retry_delay: float):
    data = urlencode(payload).encode("utf-8")
    req = Request(base_url, data=data, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    req.add_header("User-Agent", "Mozilla/5.0 (compatible; PengboSpaceSkill/2.0)")

    attempt = 0
    while True:
        attempt += 1
        try:
            with urlopen(req, timeout=timeout) as resp:
                raw = resp.read().decode("utf-8", errors="replace")
                return parse_json_safely(raw)
        except HTTPError as e:
            body = e.read().decode("utf-8", errors="replace") if hasattr(e, "read") else str(e)
            if attempt <= retries:
                time.sleep(retry_delay)
                continue
            raise SkillError(f"HTTP {e.code}: {body}") from e
        except URLError as e:
            if attempt <= retries:
                time.sleep(retry_delay)
                continue
            raise SkillError(f"Network error: {e}") from e


def read_json(path: Path):
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, payload: Any):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def is_cache_fresh(cache_obj, max_age_days: int):
    if not cache_obj or "updated_at" not in cache_obj:
        return False
    try:
        ts = datetime.fromisoformat(cache_obj["updated_at"])
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=timezone.utc)
    except Exception:
        return False
    return datetime.now(timezone.utc) - ts <= timedelta(days=max_age_days)


def apply_service_filters(services, fields: Optional[str], query: Optional[str], limit: Optional[int]):
    out = services if isinstance(services, list) else []

    if query:
        q = query.strip().lower()
        def m(item: Dict[str, Any]) -> bool:
            blob = " ".join(str(item.get(k, "")) for k in ["name", "category", "service", "type", "desc"]).lower()
            return q in blob
        out = [x for x in out if isinstance(x, dict) and m(x)]

    if fields:
        want = [x.strip() for x in fields.split(",") if x.strip()]
        out = [{k: v for k, v in item.items() if k in want} for item in out if isinstance(item, dict)]

    if limit is not None:
        out = out[: max(0, limit)]

    return out


def resolve_cache_path(args, key: str) -> Path:
    if args.cache_path:
        return Path(args.cache_path)
    return default_cache_path(args.base_url, key)


def write_services_cache(cache_path: Path, base_url: str, key: str, services):
    payload = {
        "updated_at": now_iso(),
        "base_url": base_url,
        "host": normalize_host(base_url),
        "key_hash": key_hash(key),
        "count": len(services) if isinstance(services, list) else 0,
        "services": services,
    }
    write_json(cache_path, payload)
    return payload


def require_confirm(args, action: str):
    if not args.confirm:
        raise SkillError(f"Action '{action}' is write-risk and requires --confirm")


def idempotency_guard(action: str, payload: Dict[str, Any]):
    if action != "add":
        return
    key_fields = {
        "service": payload.get("service"),
        "link": payload.get("link"),
        "quantity": payload.get("quantity"),
    }
    fp = hashlib.sha256(json.dumps(key_fields, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()

    f = get_idempotency_path()
    obj = read_json(f) or {}
    now_ts = int(time.time())
    prev = obj.get(fp)
    if prev and now_ts - int(prev) <= IDEMPOTENCY_WINDOW_SECONDS:
        raise SkillError("Duplicate add request blocked by idempotency guard (same service/link/quantity within 30s)")
    obj[fp] = now_ts
    write_json(f, obj)


def audit_log(action: str, req: Dict[str, Any], resp: Any):
    if action not in {"add", "refill"}:
        return
    link = str(req.get("link", ""))
    row = {
        "ts": now_iso(),
        "action": action,
        "service": req.get("service"),
        "quantity": req.get("quantity"),
        "order": req.get("order"),
        "link_hash": hashlib.sha256(link.encode("utf-8")).hexdigest()[:16] if link else None,
        "response": resp,
    }
    p = get_orders_log_path()
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def handle_health(args):
    lang = resolve_lang(args)
    key = get_key(args, required=False)
    data = {
        "base_url": args.base_url,
        "key_loaded": bool(key),
        "api_reachable": False,
        "account_usable": False,
    }
    if not key:
        return make_err("health", "missing_api_key", next_steps=missing_key_next_steps(lang), meta={"base_url": args.base_url})

    try:
        resp = call_api({"key": key, "action": "balance"}, args.base_url, args.timeout, args.retries, args.retry_delay)
        data["api_reachable"] = True
        if isinstance(resp, dict) and not resp.get("error"):
            data["account_usable"] = True
            data["balance_preview"] = resp
        else:
            data["balance_preview"] = resp
    except Exception as e:
        data["error"] = str(e)

    return make_ok("health", data)


def handle_services(args):
    action = "services"
    key = get_key(args)
    cache_path = resolve_cache_path(args, key)
    source = args.source

    cache_obj = read_json(cache_path) if source in {"cache", "auto"} else None
    if source == "cache":
        if not cache_obj:
            raise SkillError(f"Cache not found: {cache_path}")
        services = cache_obj.get("services", [])
        filtered = apply_service_filters(services, args.fields, args.query, args.limit)
        return make_ok(action, filtered, {"source": "cache", "cache_path": str(cache_path), "total": len(services), "returned": len(filtered)})

    if source == "auto" and is_cache_fresh(cache_obj, args.cache_max_age_days):
        services = cache_obj.get("services", [])
        filtered = apply_service_filters(services, args.fields, args.query, args.limit)
        return make_ok(action, filtered, {"source": "cache", "cache_path": str(cache_path), "total": len(services), "returned": len(filtered)})

    if args.jitter > 0:
        time.sleep(args.jitter)

    live = call_api({"key": key, "action": "services"}, args.base_url, args.timeout, args.retries, args.retry_delay)
    if isinstance(live, list):
        write_services_cache(cache_path, args.base_url, key, live)
        filtered = apply_service_filters(live, args.fields, args.query, args.limit)
        return make_ok(action, filtered, {"source": "live", "cache_path": str(cache_path), "total": len(live), "returned": len(filtered)})

    if isinstance(live, dict) and live.get("error"):
        return make_err(action, str(live.get("error")))

    return make_ok(action, live, {"source": "live", "cache_path": str(cache_path)})


def handle_refresh_cache(args):
    action = "refresh-cache"
    key = get_key(args)
    cache_path = resolve_cache_path(args, key)
    if args.jitter > 0:
        time.sleep(args.jitter)

    live = call_api({"key": key, "action": "services"}, args.base_url, args.timeout, args.retries, args.retry_delay)
    if not isinstance(live, list):
        if isinstance(live, dict) and live.get("error"):
            return make_err(action, str(live.get("error")))
        raise SkillError("services response is not a list; cache not updated")

    obj = write_services_cache(cache_path, args.base_url, key, live)
    return make_ok(action, {"updated_at": obj["updated_at"], "count": obj["count"], "cache_path": str(cache_path)})


def handle_setup(args):
    lang = resolve_lang(args)
    key = get_key(args, required=False)
    setup_data = {
        "base_url": args.base_url,
        "key_detected": bool(key),
        "steps": {
            "check_env": "PENGBO_API_KEY 已检测到" if key else "未检测到 PENGBO_API_KEY",
            "set_env_example": "export PENGBO_API_KEY=\"<your_api_key>\"",
        },
    }

    health_result = handle_health(args)
    setup_data["health"] = health_result

    if health_result.get("ok"):
        setup_data["next_command"] = "python3 skills/pengbo-space/scripts/pengbo_smm.py services --query \"twitter followers\" --fields service,name,category,rate,min,max --limit 20"
        return make_ok("setup", setup_data)

    if health_result.get("error") == "missing_api_key":
        setup_data["next_steps"] = missing_key_next_steps(lang)
        return make_err("setup", "missing_api_key", meta={"setup": setup_data}, next_steps=missing_key_next_steps(lang))

    return make_err("setup", "health_check_failed", meta={"setup": setup_data})


def build_payload(args):
    key = get_key(args)

    if args.command in {"add", "create-order"}:
        require_confirm(args, "add")
        payload = {
            "key": key,
            "action": "add",
            "service": args.service,
            "link": args.link,
            "quantity": args.quantity,
        }
        if args.runs is not None:
            payload["runs"] = args.runs
        if args.interval is not None:
            payload["interval"] = args.interval
        if args.comments is not None:
            payload["comments"] = args.comments
        idempotency_guard("add", payload)
        return "add", payload

    if args.command == "status":
        return "status", {"key": key, "action": "status", "order": args.order}

    if args.command == "orders":
        return "orders", {"key": key, "action": "orders", "orders": args.orders}

    if args.command == "list-orders":
        payload = {"key": key, "action": "list_orders"}
        if args.limit is not None:
            payload["limit"] = args.limit
        if args.offset is not None:
            payload["offset"] = args.offset
        if args.status_filter:
            payload["status"] = args.status_filter
        if args.search:
            payload["search"] = args.search
        return "list_orders", payload

    if args.command == "refill":
        require_confirm(args, "refill")
        return "refill", {"key": key, "action": "refill", "order": args.order}

    if args.command == "refill-status":
        return "refill_status", {"key": key, "action": "refill_status", "refill": args.refill}

    if args.command == "balance":
        return "balance", {"key": key, "action": "balance"}

    raise SkillError(f"Unsupported command: {args.command}")


def parser():
    p = argparse.ArgumentParser(description="Pengbo Space SMM API helper")
    p.add_argument("--key", help="API key (or use PENGBO_API_KEY env)")
    p.add_argument("--base-url", default=DEFAULT_API_URL, help="API base URL (default: https://pengbo.space/api/v1)")
    p.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT)
    p.add_argument("--retries", type=int, default=DEFAULT_RETRIES)
    p.add_argument("--retry-delay", type=float, default=DEFAULT_RETRY_DELAY)
    p.add_argument("--lang", choices=["auto", "zh", "en", "es", "mixed"], default="auto", help="Response language")
    p.add_argument("--input-text", default="", help="Optional user text hint for auto language detection")

    sub = p.add_subparsers(dest="command", required=True)

    p_services = sub.add_parser("services", help="List available services")
    p_services.add_argument("--source", choices=["auto", "live", "cache"], default="auto")
    p_services.add_argument("--cache-path", default="", help="Optional explicit cache path")
    p_services.add_argument("--cache-max-age-days", type=int, default=DEFAULT_CACHE_MAX_AGE_DAYS)
    p_services.add_argument("--jitter", type=float, default=0.0, help="Optional delay seconds before live request")
    p_services.add_argument("--fields", default="", help="Comma-separated output fields")
    p_services.add_argument("--query", default="", help="Local keyword filter")
    p_services.add_argument("--limit", type=int, default=None, help="Max items to return")

    p_refresh = sub.add_parser("refresh-cache", help="Refresh local services cache")
    p_refresh.add_argument("--cache-path", default="", help="Optional explicit cache path")
    p_refresh.add_argument("--jitter", type=float, default=0.0, help="Optional delay seconds before request")

    p_add = sub.add_parser("add", help="Create new order")
    p_add.add_argument("--service", required=True, type=int)
    p_add.add_argument("--link", required=True)
    p_add.add_argument("--quantity", required=True, type=int)
    p_add.add_argument("--runs", type=int)
    p_add.add_argument("--interval", type=int)
    p_add.add_argument("--comments", help="For custom comments service: multi-line comments")
    p_add.add_argument("--confirm", action="store_true", help="Required for write action")

    p_create_order = sub.add_parser("create-order", help="Alias of add")
    p_create_order.add_argument("--service", required=True, type=int)
    p_create_order.add_argument("--link", required=True)
    p_create_order.add_argument("--quantity", required=True, type=int)
    p_create_order.add_argument("--runs", type=int)
    p_create_order.add_argument("--interval", type=int)
    p_create_order.add_argument("--comments", help="For custom comments service: multi-line comments")
    p_create_order.add_argument("--confirm", action="store_true", help="Required for write action")

    p_status = sub.add_parser("status", help="Get single order status")
    p_status.add_argument("--order", required=True, type=int)

    p_orders = sub.add_parser("orders", help="Get multiple order statuses")
    p_orders.add_argument("--orders", required=True, help="Comma-separated IDs, e.g. 1,2,3")

    p_list_orders = sub.add_parser("list-orders", help="List order history (list_orders)")
    p_list_orders.add_argument("--limit", type=int, default=None)
    p_list_orders.add_argument("--offset", type=int, default=None)
    p_list_orders.add_argument("--status-filter", default="", help="Optional upstream status filter")
    p_list_orders.add_argument("--search", default="", help="Optional keyword filter")

    p_refill = sub.add_parser("refill", help="Create refill for an order")
    p_refill.add_argument("--order", required=True, type=int)
    p_refill.add_argument("--confirm", action="store_true", help="Required for write action")

    p_refill_status = sub.add_parser("refill-status", help="Get refill status")
    p_refill_status.add_argument("--refill", required=True, type=int)

    sub.add_parser("balance", help="Get account balance")
    sub.add_parser("health", help="Check key/API/account readiness")
    sub.add_parser("setup", help="One-shot onboarding: key check + health + next command")

    return p


def localize_error_text(err: str, lang: str) -> str:
    s = str(err or "")
    maps = {
        "missing_api_key": {
            "zh": "未检测到 API Key，请先配置后再试。",
            "en": "API key not found. Please configure it first.",
            "es": "No se encontró API key. Configúrala primero.",
            "mixed": "未检测到 API Key, please configure it first.",
        },
        "You are not eligible to send refill request.": {
            "zh": "当前不符合补单条件（未触发补单窗口或无可补数量）。",
            "en": "This order is currently not eligible for refill (window/conditions not met).",
            "es": "Este pedido no cumple las condiciones de refill por ahora.",
            "mixed": "当前不符合补单条件 (not eligible for refill right now).",
        },
        "base_url must use https": {
            "zh": "base_url 必须使用 https。",
            "en": "base_url must use https.",
            "es": "base_url debe usar https.",
            "mixed": "base_url 必须使用 https.",
        },
        "base_url host not allowed": {
            "zh": "base_url 域名不在白名单内。",
            "en": "base_url host is not in allowlist.",
            "es": "El host de base_url no está en la lista permitida.",
            "mixed": "base_url host 不在 allowlist.",
        }
    }
    for k, v in maps.items():
        if k in s:
            return v.get(lang, v["zh"])
    return s


def status_label(raw: Any, lang: str) -> str:
    s = str(raw or "").upper()
    table = {
        "PENDING": {"zh": "待处理", "en": "Pending", "es": "Pendiente", "mixed": "待处理/Pending"},
        "PROCESSING": {"zh": "处理中", "en": "Processing", "es": "En proceso", "mixed": "处理中/Processing"},
        "IN PROGRESS": {"zh": "处理中", "en": "In progress", "es": "En proceso", "mixed": "处理中/In progress"},
        "PARTIAL": {"zh": "部分完成", "en": "Partial", "es": "Parcial", "mixed": "部分完成/Partial"},
        "COMPLETED": {"zh": "已完成", "en": "Completed", "es": "Completado", "mixed": "已完成/Completed"},
        "CANCELED": {"zh": "已取消", "en": "Canceled", "es": "Cancelado", "mixed": "已取消/Canceled"},
        "CANCELLED": {"zh": "已取消", "en": "Cancelled", "es": "Cancelado", "mixed": "已取消/Cancelled"},
        "REFUNDED": {"zh": "已退款", "en": "Refunded", "es": "Reembolsado", "mixed": "已退款/Refunded"},
    }
    v = table.get(s)
    return (v or {}).get(lang, s)


def build_display(result: Dict[str, Any], lang: str) -> Optional[Dict[str, Any]]:
    if not result.get("ok"):
        return None
    action = result.get("action")
    data = result.get("data")

    if action == "status" and isinstance(data, dict):
        qty = data.get("quantity") or 0
        charge = data.get("charge")
        unit = None
        try:
            if qty:
                unit = round(float(charge) * 1000 / float(qty), 4)
        except Exception:
            unit = None
        return {
            "订单号": data.get("order"),
            "服务ID": data.get("service_id"),
            "链接": data.get("link"),
            "订单状态": status_label(data.get("status"), lang),
            "原始状态": data.get("status"),
            "下单数量": qty,
            "剩余未完成数量": data.get("remains"),
            "金额": charge,
            "币种": data.get("currency"),
            "单价(每1000)": unit,
        }

    if action == "list_orders" and isinstance(data, dict) and isinstance(data.get("data"), list):
        rows = []
        for r in data.get("data", [])[:20]:
            row = dict(r)
            row["status_label"] = status_label(r.get("status"), lang)
            rows.append(row)
        return {
            "总订单数": data.get("total"),
            "当前页": data.get("current_page"),
            "每页": data.get("per_page"),
            "订单摘要": rows,
        }

    if action == "services" and isinstance(data, list):
        rows = []
        for r in data[:20]:
            if not isinstance(r, dict):
                continue
            rows.append({
                "服务ID": r.get("service"),
                "名称": r.get("name"),
                "分类": r.get("category"),
                "单价(每1000)": r.get("rate"),
                "最小数量": r.get("min"),
                "最大数量": r.get("max"),
                "支持补单": "是" if str(r.get("refill", 0)) in {"1", "true", "True"} else "否",
            })
        return {"服务列表(前20)": rows}

    return None


def localize_result(result: Dict[str, Any], lang: str) -> Dict[str, Any]:
    if "error" in result:
        result["error_human"] = localize_error_text(str(result.get("error", "")), lang)
    display = build_display(result, lang)
    if display:
        result["display"] = display
    result["lang"] = lang
    return result


def infer_action_from_argv(argv: list) -> str:
    commands = {
        "services", "refresh-cache", "add", "create-order", "status", "orders",
        "list-orders", "refill", "refill-status", "balance", "health", "setup"
    }
    for token in argv[1:]:
        if token in commands:
            return token
    return "unknown"


def infer_lang_from_argv(argv: list) -> str:
    for i, token in enumerate(argv):
        if token == "--lang" and i + 1 < len(argv):
            v = argv[i + 1].lower()
            if v in {"zh", "en", "es", "mixed"}:
                return v
    return detect_lang(" ".join(argv))


def main():
    args = parser().parse_args()
    validate_base_url(args.base_url)

    lang = resolve_lang(args)
    remember_lang(lang)

    if args.command == "services":
        result = handle_services(args)
    elif args.command == "refresh-cache":
        result = handle_refresh_cache(args)
    elif args.command == "health":
        result = handle_health(args)
    elif args.command == "setup":
        result = handle_setup(args)
    else:
        action, payload = build_payload(args)
        result = call_api(payload, args.base_url, args.timeout, args.retries, args.retry_delay)
        if isinstance(result, dict) and result.get("error"):
            result = make_err(action, str(result.get("error")))
        else:
            result = make_ok(action, result)
        audit_log(action, payload, result)

    result = attach_onboarding_once(result, args.command, lang)
    result = localize_result(result, lang)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        action = infer_action_from_argv(sys.argv)
        lang = infer_lang_from_argv(sys.argv)
        if isinstance(e, MissingApiKeyError):
            out = make_err(action, "missing_api_key", next_steps=missing_key_next_steps(lang))
        else:
            out = make_err(action, str(e))
        out = localize_result(out, lang)
        print(json.dumps(out, ensure_ascii=False))
        sys.exit(1)
