"""
OpenClaw newspaper-ocr skill runtime — 下载导向最小契约.

三个核心能力:
  1. updates       — 查询今天/近期更新了哪些期次
  2. issue-info    — 按报纸名+日期定位某一期，返回基础信息+下载链接
  3. download-links — 批量列出近期期次的 PDF 下载链接

查询不鉴权；下载需要 Import Token。

This module is intentionally self-contained:
- No third-party dependencies (uses only urllib).
- No hard-coded credentials.
- Runtime defaults are defined in-code.
"""

import argparse
import datetime as dt
import json
import os
import ssl
import sys
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib import error as urllib_error
from urllib import request as urllib_request

# ─────────────────────── 配置 ───────────────────────

def _load_config() -> Dict[str, Any]:
    """从 skill 目录（scripts 的上一级）加载 config.json，字段缺失时静默跳过."""
    config_path = Path(__file__).parent.parent / "config.json"
    if config_path.exists():
        try:
            with open(config_path, encoding="utf-8") as f:
                data = json.load(f)
            return {k: v for k, v in data.items() if not k.startswith("_")}
        except (json.JSONDecodeError, OSError):
            pass
    return {}

_CONFIG = _load_config()

OCR_API_BASE = os.environ.get("OCR_API_BASE") or _CONFIG.get("api_base") or "https://pick-read.vip/api"
IMPORT_TOKEN = os.environ.get("IMPORT_TOKEN") or _CONFIG.get("import_token") or ""
DEFAULT_OUTPUT_DIR = Path.cwd() / "miaoxiang" / "mx_newspaper_ocr"
TIMEOUT_SECONDS = 30
_MANIFEST_CACHE: Dict[str, Any] | None = None

# ─────────────────────── 报纸别名 ───────────────────────

_ALIASES: Dict[str, List[str]] = {
    "wsj": ["wall street journal"],
    "nyt": ["new york times"],
    "wapo": ["washington post"],
    "la times": ["los angeles times"],
    "latimes": ["los angeles times"],
    "nyp": ["new york post"],
    "ft": ["financial times"],
    "华盛顿邮报": ["washington post"],
    "纽约时报": ["new york times"],
    "华尔街日报": ["wall street journal"],
    "洛杉矶时报": ["los angeles times"],
    "中国日报": ["china daily"],
    "波士顿环球报": ["boston globe"],
    "环球邮报": ["globe and mail"],
    "今日美国": ["usa today"],
    "独立报": ["independent"],
}

# ─────────────────────── HTTP 层 ───────────────────────

def _build_ssl_contexts() -> List[ssl.SSLContext]:
    """构建多个 SSL 上下文，按宽松度递增排列，用于自动 fallback."""
    ctxs: List[ssl.SSLContext] = []
    # 策略 1: 默认上下文 + 关闭证书校验
    try:
        c1 = ssl.create_default_context()
        c1.check_hostname = False
        c1.verify_mode = ssl.CERT_NONE
        ctxs.append(c1)
    except Exception:
        pass
    # 策略 2: 完全不验证的上下文（兼容旧 OpenSSL）
    try:
        c2 = ssl._create_unverified_context()  # noqa: SLF001
        ctxs.append(c2)
    except Exception:
        pass
    if not ctxs:
        ctxs.append(ssl.create_default_context())
    return ctxs


def _build_opener() -> urllib_request.OpenerDirector:
    """构建绕过系统代理的 urllib opener.

    许多运行环境（Windows 系统代理、企业代理、AI 平台沙箱）的 HTTPS 代理
    与目标服务器 TLS 不兼容，导致 'EOF occurred in violation of protocol'。
    显式使用空 ProxyHandler 绕过所有代理，直连目标服务器。
    """
    return urllib_request.build_opener(
        urllib_request.ProxyHandler({}),
        urllib_request.HTTPSHandler(context=_build_ssl_contexts()[0]),
    )

_SSL_CONTEXTS = _build_ssl_contexts()
_OPENER = _build_opener()
_MAX_RETRIES = 2


def _http_get(path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """对 OCR API 发起 GET 请求并返回解析后的 JSON.

    使用无代理 opener + 多 SSL 上下文自动 fallback + 重试。
    """
    url = f"{OCR_API_BASE.rstrip('/')}{path}"
    if params:
        qs = "&".join(f"{k}={urllib_request.quote(str(v))}" for k, v in params.items() if v is not None)
        if qs:
            url = f"{url}?{qs}"

    req = urllib_request.Request(url, method="GET", headers={
        "Accept": "application/json",
        "User-Agent": "SkillBot/2.0",
        "Connection": "close",
    })
    last_exc: Optional[Exception] = None

    for ctx in _SSL_CONTEXTS:
        opener = urllib_request.build_opener(
            urllib_request.ProxyHandler({}),
            urllib_request.HTTPSHandler(context=ctx),
        )
        for attempt in range(_MAX_RETRIES):
            try:
                with opener.open(req, timeout=TIMEOUT_SECONDS) as resp:
                    raw = resp.read().decode("utf-8", errors="replace")
                try:
                    parsed = json.loads(raw)
                except json.JSONDecodeError as exc:
                    raise RuntimeError(f"OCR API {path} returned invalid JSON") from exc
                return parsed if isinstance(parsed, dict) else {"data": parsed}
            except urllib_error.HTTPError as exc:
                err_body = exc.read().decode("utf-8", errors="replace") if exc.fp else ""
                error_code, message = "unknown", err_body[:300]
                try:
                    err_json = json.loads(err_body)
                    if isinstance(err_json.get("detail"), dict):
                        d = err_json["detail"]
                        error_code = d.get("error_code", "unknown")
                        message = d.get("message", message)
                except (json.JSONDecodeError, KeyError, TypeError):
                    pass
                raise RuntimeError(f"OCR API {path} [{error_code}] {exc.code}: {message}") from exc
            except (urllib_error.URLError, ssl.SSLError, OSError, EOFError) as exc:
                last_exc = exc
                continue

    reason = str(last_exc) if last_exc else "unknown network error"
    raise RuntimeError(
        f"OCR API {path} failed after trying {len(_SSL_CONTEXTS)} SSL strategies: {reason}. "
        f"请检查网络连接或 Python/OpenSSL 版本（建议 Python>=3.8, OpenSSL>=1.1.1）。"
    )

# ─────────────────────── OCR API 封装 ───────────────────────

def api_manifest(
    limit: int = 200,
    offset: int = 0,
    pub_name: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
) -> Dict[str, Any]:
    """GET /ocr/manifest — 列出所有已完成 OCR 的期次."""
    return _http_get("/ocr/manifest", {
        "limit": limit, "offset": offset,
        "pub_name": pub_name, "date_from": date_from, "date_to": date_to,
    })


def api_manifest_cached(
    limit: int = 200,
    offset: int = 0,
    pub_name: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
) -> Dict[str, Any]:
    """在一次 skill 运行中复用 manifest，减少重复请求。有筛选参数时不走缓存。"""
    global _MANIFEST_CACHE
    has_filters = pub_name is not None or date_from is not None or date_to is not None
    if offset != 0 or has_filters:
        return api_manifest(limit=limit, offset=offset, pub_name=pub_name, date_from=date_from, date_to=date_to)
    if _MANIFEST_CACHE is None:
        _MANIFEST_CACHE = api_manifest(limit=limit)
    return _MANIFEST_CACHE


def api_resolve_issue(pub_name: str, issue_date: Optional[str] = None) -> Dict[str, Any]:
    """GET /ocr/issues/resolve — 按报纸名解析 issue_id。"""
    return _http_get("/ocr/issues/resolve", {"pub_name": pub_name, "issue_date": issue_date})


def api_issue_info(issue_id: str) -> Dict[str, Any]:
    """GET /ocr/issues/{id}/info — 单期基础信息。"""
    return _http_get(f"/ocr/issues/{issue_id}/info")

# ─────────────────────── 报纸名解析 ───────────────────────

def _match_pub_name(query: str, candidate: str) -> bool:
    q = query.lower().strip()
    c = candidate.lower().strip()
    if q in c or c in q:
        return True
    for alias in _ALIASES.get(q, []):
        if alias in c or c in alias:
            return True
    return False


def resolve_issue(pub_name: str, issue_date: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """优先使用 resolve 聚合接口，失败时再回退 manifest 本地匹配。"""
    resolved = api_resolve_issue(pub_name, issue_date)
    if resolved.get("matched"):
        return {
            "issue_id": resolved.get("issue_id"),
            "pub_name": resolved.get("pub_name"),
            "issue_date": resolved.get("issue_date"),
        }

    manifest = api_manifest_cached()
    candidates = []
    for item in manifest.get("items", []):
        name = item.get("pub_name", "")
        if not _match_pub_name(pub_name, name):
            continue
        if issue_date and item.get("issue_date") != issue_date:
            continue
        candidates.append(item)

    if not candidates:
        return None
    pub_lower = pub_name.lower().strip()
    for candidate in candidates:
        if candidate["pub_name"].lower() == pub_lower:
            return candidate
    return candidates[0]

# ─────────────────────── Manifest 过滤 ───────────────────────

def _parse_updated_at(value: str) -> dt.datetime:
    return dt.datetime.fromisoformat(value.replace("Z", "+00:00"))


def _latest_updated_date(items: List[Dict[str, Any]]) -> Optional[dt.date]:
    values = [item.get("updated_at") for item in items if item.get("updated_at")]
    if not values:
        return None
    return max(_parse_updated_at(value).date() for value in values)


def _filter_manifest_items(
    items: List[Dict[str, Any]],
    issue_date: Optional[str] = None,
    days: Optional[int] = None,
) -> List[Dict[str, Any]]:
    if issue_date:
        return [item for item in items if item.get("issue_date") == issue_date]
    if days and days > 0:
        cutoff = dt.datetime.utcnow().date() - dt.timedelta(days=days - 1)
        filtered = []
        for item in items:
            raw = item.get("updated_at")
            if not raw:
                continue
            if _parse_updated_at(raw).date() >= cutoff:
                filtered.append(item)
        filtered.sort(key=lambda x: (x.get("updated_at") or "", x.get("issue_date") or ""), reverse=True)
        return filtered
    latest_updated = _latest_updated_date(items)
    if latest_updated is not None:
        latest_items = [
            item for item in items
            if item.get("updated_at") and _parse_updated_at(item["updated_at"]).date() == latest_updated
        ]
        latest_items.sort(key=lambda x: (x.get("updated_at") or "", x.get("issue_date") or ""), reverse=True)
        return latest_items
    return items

# ─────────────────────── 三个核心能力 ───────────────────────

def list_recent_updates(
    issue_date: Optional[str] = None,
    days: Optional[int] = None,
    limit: Optional[int] = None,
) -> Dict[str, Any]:
    """能力 1: 查询今天/近期更新了哪些期次。"""
    manifest = api_manifest_cached()
    items = _filter_manifest_items(manifest.get("items", []), issue_date=issue_date, days=days)
    if limit is not None:
        items = items[:limit]
    return {
        "type": "recent_updates",
        "issue_date": issue_date,
        "days": days,
        "total": len(items),
        "items": items,
    }


def get_issue_info(
    pub_name: str,
    issue_date: Optional[str] = None,
    token: Optional[str] = None,
) -> Dict[str, Any]:
    """能力 2: 按报纸名+日期定位某一期，返回基础信息+下载链接。"""
    issue = resolve_issue(pub_name, issue_date)
    if not issue:
        return {"type": "issue_info", "matched": False,
                "reason": f"未找到: {pub_name}" + (f" ({issue_date})" if issue_date else "")}

    info = api_issue_info(issue["issue_id"])
    effective_token = token or IMPORT_TOKEN
    base = OCR_API_BASE.rstrip("/")
    iid = info.get("issue_id", issue["issue_id"])

    result: Dict[str, Any] = {
        "type": "issue_info",
        "matched": True,
        "issue_id": iid,
        "pub_name": info.get("pub_name", issue.get("pub_name")),
        "issue_date": info.get("issue_date", issue.get("issue_date")),
        "page_count": info.get("page_count", 0),
    }
    if effective_token:
        result["download_url"] = f"{base}/import-pdf/{iid}?token={effective_token}"
    else:
        result["download_url"] = None
        result["note"] = "缺少 import_token，请通过 --token 参数或 IMPORT_TOKEN 环境变量传入"
    return result


def get_download_links(
    days: Optional[int] = None,
    issue_date: Optional[str] = None,
    pub_name: Optional[str] = None,
    token: Optional[str] = None,
    limit: Optional[int] = None,
) -> Dict[str, Any]:
    """能力 3: 批量列出近期新增期次的 PDF 下载链接。

    token 优先级: 参数 > IMPORT_TOKEN 环境变量。
    下载链接格式: {OCR_API_BASE}/import-pdf/{issue_id}?token={token}
    """
    effective_token = token or IMPORT_TOKEN
    manifest = api_manifest_cached(pub_name=pub_name) if pub_name else api_manifest_cached()
    items = _filter_manifest_items(
        [i for i in manifest.get("items", []) if not pub_name or _match_pub_name(pub_name, i.get("pub_name", ""))],
        issue_date=issue_date,
        days=days if days is not None else 1,
    )
    if limit is not None:
        items = items[:limit]

    base = OCR_API_BASE.rstrip("/")
    result_items = []
    for item in items:
        iid = item.get("issue_id", "")
        entry: Dict[str, Any] = {
            "issue_id": iid,
            "pub_name": item.get("pub_name", ""),
            "issue_date": item.get("issue_date", ""),
            "page_count": item.get("page_count"),
        }
        if effective_token:
            entry["download_url"] = f"{base}/import-pdf/{iid}?token={effective_token}"
        else:
            entry["download_url"] = None
            entry["note"] = "缺少 import_token，请通过 --token 参数或 IMPORT_TOKEN 环境变量传入"
        result_items.append(entry)

    return {
        "type": "download_links",
        "issue_date": issue_date,
        "days": days if days is not None else 1,
        "pub_name": pub_name,
        "has_token": bool(effective_token),
        "total": len(result_items),
        "items": result_items,
    }

# ─────────────────────── 输出 ───────────────────────

def _save_result(result: Dict[str, Any], output_dir: Optional[Path] = None) -> Dict[str, Any]:
    if "error" in result:
        return result
    out_dir = Path(output_dir or DEFAULT_OUTPUT_DIR)
    out_dir.mkdir(parents=True, exist_ok=True)
    suffix = uuid.uuid4().hex[:8]
    output_path = out_dir / f"mx_newspaper_ocr_{result.get('type', 'query')}_{suffix}.txt"
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    result["output_path"] = str(output_path)
    return result


# ─────────────────────── CLI ───────────────────────

def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="报纸 OCR 下载工具 — 三个核心能力: updates / issue-info / download-links",
    )
    subparsers = parser.add_subparsers(dest="command")

    up = subparsers.add_parser("updates", help="查询今天/近期更新了哪些期次")
    up.add_argument("--issue-date", help="指定日期 YYYY-MM-DD")
    up.add_argument("--days", type=int, help="最近 N 天")
    up.add_argument("--limit", type=int, help="最多返回 N 条")
    up.add_argument("--no-save", action="store_true", help="不落盘")

    res = subparsers.add_parser("resolve", help="按报纸名+日期定位期次 (底层辅助)")
    res.add_argument("pub_name")
    res.add_argument("--issue-date", help="指定日期 YYYY-MM-DD")
    res.add_argument("--no-save", action="store_true", help="不落盘")

    info = subparsers.add_parser("issue-info", help="查询指定某一期的基础信息+下载链接")
    info.add_argument("pub_name")
    info.add_argument("--issue-date", help="指定日期 YYYY-MM-DD")
    info.add_argument("--token", help="导入令牌（也可通过 IMPORT_TOKEN 环境变量设置）")
    info.add_argument("--no-save", action="store_true", help="不落盘")

    dl = subparsers.add_parser("download-links", help="批量列出近期期次的 PDF 下载链接")
    dl.add_argument("--days", type=int, default=1, help="最近 N 天（默认 1 = 今天）")
    dl.add_argument("--issue-date", help="指定期次日期 YYYY-MM-DD")
    dl.add_argument("--pub-name", help="按刊物名筛选")
    dl.add_argument("--token", help="导入令牌（也可通过 IMPORT_TOKEN 环境变量设置）")
    dl.add_argument("--limit", type=int, help="最多返回 N 条")
    dl.add_argument("--no-save", action="store_true", help="不落盘")

    return parser


def run_cli() -> None:
    parser = _build_arg_parser()
    args = parser.parse_args()

    command = args.command
    if command is None:
        parser.print_help()
        raise SystemExit(1)
    elif command == "updates":
        result = list_recent_updates(issue_date=args.issue_date, days=args.days, limit=args.limit)
        if not args.no_save:
            result = _save_result(result)
    elif command == "resolve":
        resolved = resolve_issue(args.pub_name, args.issue_date)
        result = {"type": "resolve_issue", "matched": bool(resolved), "issue": resolved}
        if not args.no_save:
            result = _save_result(result)
    elif command == "issue-info":
        result = get_issue_info(args.pub_name, issue_date=args.issue_date, token=args.token)
        if not args.no_save:
            result = _save_result(result)
    elif command == "download-links":
        result = get_download_links(
            days=args.days,
            issue_date=getattr(args, "issue_date", None),
            pub_name=getattr(args, "pub_name", None),
            token=getattr(args, "token", None),
            limit=getattr(args, "limit", None),
        )
        if not args.no_save:
            result = _save_result(result)
    else:
        parser.print_help()
        raise SystemExit(1)

    if "error" in result:
        print(f"Error: {result['error']}")
        raise SystemExit(2)
    if result.get("output_path"):
        print(f"Saved: {result['output_path']}")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    run_cli()
