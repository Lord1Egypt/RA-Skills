#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Huawei Cloud SCM (SSL certificate) inventory helper — strictly read-only.

Queries the certificate list of the current account in one region through
KooCLI ``hcloud SCM ListCertificates`` and prints name / bound domain / expiry
time (plus type, status, days left and region in the table view).

Executed operations (read-only only):

    ListCertificates   GET /v3/scm/certificates

Backends:

- primary:  KooCLI subprocess ``hcloud SCM ListCertificates``
- fallback: official ``huaweicloudsdk`` SCM SDK (``huaweicloudsdkscm``)

Output modes:

- default:  compact list of 证书名称 | 绑定域名 | 到期时间
- ``--table``: full 8-column table (证书ID / 名称 / 域名 / 类型 / 状态 /
  到期时间 / 剩余天数 / region)
- ``--json``: the raw (merged) response body

Filtering: ``--content`` (pass-through fuzzy search by certificate name or
domain, plus a client-side check), ``--expiring N`` (client-side "expires in at
most N days"), ``--region`` (default cn-north-4).

Every mutating intent (create / delete / update / import / push / deploy /
revoke / ...) is rejected with exit code 1 before any command runs — this skill
never writes to SCM.

Credentials are never hardcoded and never read by this script: the KooCLI
profile / environment is used by ``hcloud``; the SDK path reads AK/SK from
environment variables only.

Usage:
    python3 scripts/list_scm_certs.py [--region cn-north-4]
    python3 scripts/list_scm_certs.py --table
    python3 scripts/list_scm_certs.py --json
    python3 scripts/list_scm_certs.py --content example.com
    python3 scripts/list_scm_certs.py --expiring 30
"""

import argparse
import json
import math
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from types import SimpleNamespace

SKILL_NAME = "huawei-cloud-scm-cert-list"
DEFAULT_REGION = os.environ.get("HUAWEICLOUD_SDK_REGION", "cn-north-4")
DEFAULT_LIMIT = 50
API_LIMITS = (10, 20, 50)
DEFAULT_MAX_PAGES = 200
DEFAULT_TIMEOUT = 60

HCLOUD_BIN_ENV = ("HUAWEI_CLOUD_SCM_CERT_LIST_HCLOUD_BIN", "SCM_HCLOUD_BIN")

# Read-only operation whitelist: anything else is refused.
READONLY_OPERATIONS = ("ListCertificates",)
ALLOWED_ACTIONS = ("list", "ls", "query", "show")

# Tokens that indicate a mutating intent supplied by the caller.
WRITE_INTENT_TOKENS = (
    "create", "delete", "update", "import", "push", "deploy", "revoke",
    "replace", "renew", "apply", "purchase", "buy", "upload", "cancel",
    "modify", "export", "destroy",
)

# Certificate type prefixes (API values) mapped to the DV/OV/EV family.
TYPE_FAMILY = {"DV": "DV", "OV": "OV", "EV": "EV"}

# Status values that mean the certificate is issued/managed by SCM itself.
SCM_ISSUED_STATUSES = (
    "PAID", "ISSUED", "CHECKING", "ISSUING", "CHECKING_ORG",
    "SUPPLEMENTCHECKING", "UNPASSED", "CANCELCHECKING",
)


class ScmError(Exception):
    """Classified failure with a user-actionable message."""

    def __init__(self, kind, message, detail=""):
        Exception.__init__(self, message)
        self.kind = kind
        self.message = message
        self.detail = detail


# ---------------------------------------------------------------------------
# Write-intent guard
# ---------------------------------------------------------------------------

def guard_write_intent(action, content=None):
    """Reject mutating intent before any cloud call.

    Returns the error message when a write intent is detected, else None.
    """
    if action:
        if str(action).strip().lower() not in ALLOWED_ACTIONS:
            return (
                "此技能为只读查询（SCM 证书列表），拒绝执行非查询动作: {0}。"
                "支持的动作仅限 list（默认）；证书申请/购买/导入/部署推送/"
                "吊销/删除等写操作不在本技能范围内。".format(action)
            )
    if content:
        lowered = str(content).strip().lower()
        if lowered in WRITE_INTENT_TOKENS:
            return (
                "此技能为只读查询（SCM 证书列表），不支持对证书执行写操作。"
                "在 --content 中检测到疑似写操作意图: {0}".format(lowered)
            )
    return None


# ---------------------------------------------------------------------------
# KooCLI backend
# ---------------------------------------------------------------------------

def hcloud_binary():
    """Return the hcloud binary path or None (env override wins for tests)."""
    for name in HCLOUD_BIN_ENV:
        override = os.environ.get(name)
        if override:
            return override
    return shutil.which("hcloud")


def run_hcloud(args, timeout=DEFAULT_TIMEOUT):
    """Run hcloud and return the parsed JSON body."""
    binary = hcloud_binary()
    if not binary:
        raise ScmError(
            "cli_missing",
            "未找到 hcloud（KooCLI），无法查询 SCM 证书列表。",
            "安装后可重试（见 references/cli-installation-guide.md），"
            "或改用 --backend sdk 走 SDK 回退。",
        )
    cmd = [binary] + list(args)
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        raise ScmError(
            "network",
            "调用 hcloud 超时（{0} 秒），请检查网络后重试。".format(timeout),
        )
    except OSError as exc:
        raise ScmError("cli_error", "无法执行 hcloud: {0}".format(exc))
    if proc.returncode != 0:
        detail = (proc.stderr or proc.stdout or "").strip()
        raise classify_cli_error(detail, proc.returncode)
    raw = (proc.stdout or "").strip()
    payload = None
    try:
        payload = json.loads(raw)
    except ValueError:
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if match:
            try:
                payload = json.loads(match.group(0))
            except ValueError:
                payload = None
    if payload is None:
        raise ScmError(
            "bad_output",
            "hcloud 返回了非 JSON 输出，无法解析证书列表。",
            raw[:300],
        )
    # KooCLI exits 0 even when the API returns an error body; an error payload
    # must never be mistaken for an empty certificate list.
    if isinstance(payload, dict) and "certificates" not in payload:
        if any(key in payload for key in ("error_code", "error_msg", "error")):
            raise classify_cli_error(
                json.dumps(payload, ensure_ascii=False), proc.returncode)
    return payload


def classify_cli_error(detail, returncode=None):
    """Map a hcloud failure message onto an actionable ScmError."""
    text = detail or ""
    lowered = text.lower()
    if "[use_error]" in lowered:
        return ScmError(
            "use_error",
            "KooCLI 参数/用法错误（[USE_ERROR]），请检查 --region / --limit / "
            "--offset 取值（--limit 仅支持 10 / 20 / 50）。",
            text,
        )
    if ("scm.4002" in lowered or "403" in text or "not authorized" in lowered
            or "accessdenied" in lowered or "permission denied" in lowered
            or "permission" in lowered or "pdp.permission" in lowered):
        return ScmError(
            "forbidden",
            "无权限访问 SCM 证书列表（403），请授予 IAM 只读权限 scm:cert:list "
            "后重试。",
            text,
        )
    if ("credential" in lowered or "ak/sk" in lowered or "ak, sk" in lowered
            or "no valid authentication" in lowered
            or "authentication" in lowered):
        return ScmError(
            "credentials",
            "缺少或无效的华为云凭据（AK/SK）。请在终端离线配置 KooCLI profile，"
            "或设置 HUAWEICLOUD_SDK_AK / HUAWEICLOUD_SDK_SK 环境变量后重试。",
            text,
        )
    if ("timeout" in lowered or "timed out" in lowered or "connection" in lowered
            or "network" in lowered or "getaddrinfo" in lowered
            or "max retries" in lowered or "ssl" in lowered):
        return ScmError(
            "network",
            "连接华为云 SCM 接口失败（网络异常/超时），请检查网络与代理后重试。",
            text,
        )
    if "404" in text:
        return ScmError(
            "not_found",
            "SCM 接口不存在（404），请确认 --region 是否支持 SCM"
            "（如 cn-north-4 / ap-southeast-1）。",
            text,
        )
    return ScmError(
        "cli_error",
        "hcloud 调用失败（exit={0}）。".format(returncode), text
    )


def _query_args(region, limit, offset, content=None, expired_days_since=None,
                enterprise_project_id=None):
    args = [
        "SCM", "ListCertificates",
        "--cli-region=" + region,
        "--limit=" + str(limit),
        "--offset=" + str(offset),
    ]
    if content:
        args.append("--content=" + str(content))
    if expired_days_since is not None:
        args.append("--expired_days_since=" + str(expired_days_since))
    if enterprise_project_id:
        args.append("--enterprise_project_id=" + str(enterprise_project_id))
    return args


def fetch_pages_hcloud(region, limit, offset=0, max_pages=DEFAULT_MAX_PAGES,
                       content=None, expired_days_since=None,
                       enterprise_project_id=None, timeout=DEFAULT_TIMEOUT):
    """Call ListCertificates page by page (offset + limit) until exhausted."""
    pages = []
    current = max(0, int(offset or 0))
    for _ in range(max_pages):
        body = run_hcloud(
            _query_args(region, limit, current, content, expired_days_since,
                        enterprise_project_id),
            timeout,
        )
        pages.append(body)
        items = body.get("certificates") or []
        if not isinstance(items, list) or len(items) < limit:
            break
        current += limit
        total = body.get("total_count")
        try:
            if total is not None and current >= int(total):
                break
        except (TypeError, ValueError):
            pass
    return pages


# ---------------------------------------------------------------------------
# SDK backend (fallback)
# ---------------------------------------------------------------------------

def env_credentials():
    ak = (os.environ.get("HUAWEICLOUD_SDK_AK")
          or os.environ.get("HUAWEI_ACCESS_KEY")
          or os.environ.get("HUAWEI_AK"))
    sk = (os.environ.get("HUAWEICLOUD_SDK_SK")
          or os.environ.get("HUAWEI_SECRET_KEY")
          or os.environ.get("HUAWEI_SK"))
    if not ak or not sk:
        raise ScmError(
            "credentials",
            "缺少华为云凭据（AK/SK）。请在终端离线配置 KooCLI profile 或导出 "
            "HUAWEICLOUD_SDK_AK / HUAWEICLOUD_SDK_SK 环境变量后重试。"
        )
    return ak, sk


def env_domain_id():
    """Optional account domain ID; lets GlobalCredentials skip the IAM lookup."""
    return (os.environ.get("HUAWEICLOUD_SDK_DOMAIN_ID")
            or os.environ.get("HUAWEI_DOMAIN_ID"))


def sdk_client(region):
    """Build an SCM SDK client (lazy import keeps the CLI path dependency-free).

    SCM is a global service: ``ScmClient`` only accepts ``GlobalCredentials``
    (``ScmClient.new_builder()`` validates the credential type), so a
    ``BasicCredentials`` client fails at build time with
    ``credential type error, supported credential type is GlobalCredentials``.
    """
    try:
        from huaweicloudsdkcore.auth.credentials import GlobalCredentials
        from huaweicloudsdkscm.v3 import ScmClient
        from huaweicloudsdkscm.v3.region.scm_region import ScmRegion
    except ImportError as exc:
        raise ScmError(
            "sdk_missing",
            "未安装华为云 SCM SDK（huaweicloudsdkscm），无法走 SDK 回退。",
            "pip install huaweicloudsdkcore huaweicloudsdkscm；"
            "或安装 KooCLI 走 CLI 主路径。原始错误: {0}".format(exc),
        )
    ak, sk = env_credentials()
    credentials = GlobalCredentials(ak, sk, env_domain_id())
    builder = ScmClient.new_builder().with_credentials(credentials)
    try:
        return builder.with_region(ScmRegion.value_of(region)).build()
    except Exception:
        from huaweicloudsdkcore.region.region import Region
        endpoint = "https://scm.{0}.myhuaweicloud.com".format(region)
        return builder.with_region(Region(id=region, endpoint=endpoint)).build()


def _sdk_request(name, **fields):
    """Build an SDK request model, or a plain attribute holder for tests."""
    try:
        module = __import__("huaweicloudsdkscm.v3", fromlist=[name])
        request = getattr(module, name)()
    except Exception:
        request = SimpleNamespace()
    for key, value in fields.items():
        if value is not None:
            setattr(request, key, value)
    return request


def sdk_page(region, limit, offset=0, content=None, expired_days_since=None,
             enterprise_project_id=None):
    """One ListCertificates page through the SDK, returned as a plain dict."""
    request = _sdk_request(
        "ListCertificatesRequest",
        limit=int(limit), offset=int(offset), content=content,
        expired_days_since=expired_days_since,
        enterprise_project_id=enterprise_project_id,
    )
    try:
        response = sdk_client(region).list_certificates(request)
    except ScmError:
        raise
    except Exception as exc:  # SDK raises request exceptions, never tracebacks
        status = getattr(exc, "status_code", None)
        raise classify_cli_error(str(exc), status)
    return _response_to_dict(response)


def _response_to_dict(response):
    if hasattr(response, "to_dict"):
        try:
            data = response.to_dict()
            if isinstance(data, dict):
                return data
        except Exception:
            pass
    data = {}
    for attr in ("certificates", "total_count"):
        value = getattr(response, attr, None)
        if value is None:
            continue
        if isinstance(value, list) and value and hasattr(value[0], "to_dict"):
            data[attr] = [item.to_dict() for item in value]
        else:
            data[attr] = value
    return data


def fetch_pages_sdk(region, limit, offset=0, max_pages=DEFAULT_MAX_PAGES,
                    content=None, expired_days_since=None,
                    enterprise_project_id=None):
    pages = []
    current = max(0, int(offset or 0))
    for _ in range(max_pages):
        body = sdk_page(region, limit, current, content, expired_days_since,
                        enterprise_project_id)
        pages.append(body)
        items = body.get("certificates") or []
        if not isinstance(items, list) or len(items) < limit:
            break
        current += limit
        total = body.get("total_count")
        try:
            if total is not None and current >= int(total):
                break
        except (TypeError, ValueError):
            pass
    return pages


# ---------------------------------------------------------------------------
# Normalization / filtering
# ---------------------------------------------------------------------------

def _parse_time(value):
    """Parse an SCM expire_time value into an aware UTC datetime (or None)."""
    if value in (None, ""):
        return None
    raw = str(value).strip()
    if raw.isdigit():
        number = int(raw)
        if number > 10 ** 11:  # milliseconds
            number = number / 1000.0
        try:
            return datetime.fromtimestamp(number, tz=timezone.utc)
        except (ValueError, OverflowError, OSError):
            return None
    text = raw.replace("Z", "+00:00")
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"):
        try:
            naive = datetime.strptime(text.split("+")[0].strip(), fmt)
            return naive.replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    try:
        parsed = datetime.fromisoformat(text)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc)
    except ValueError:
        return None


def format_time(value):
    parsed = _parse_time(value)
    if parsed is None:
        return str(value) if value not in (None, "") else ""
    return parsed.strftime("%Y-%m-%d %H:%M:%S")


def days_left(value, now=None):
    parsed = _parse_time(value)
    if parsed is None:
        return None
    now = now or datetime.now(timezone.utc)
    return int(math.floor((parsed - now).total_seconds() / 86400.0))


def type_family(value):
    """Map API certificate type values to the DV / OV / EV family."""
    if value in (None, ""):
        return "-"
    text = str(value).upper()
    for key, label in TYPE_FAMILY.items():
        if text.startswith(key):
            return label
    return str(value)


def cert_source(item):
    """Derive the certificate source from its status (no fabricated API field)."""
    status = str(item.get("status") or "").upper()
    if status == "UPLOAD":
        return "上传托管"
    if status in SCM_ISSUED_STATUSES:
        return "SCM签发"
    return "-"


def normalize_certificates(pages):
    """Flatten ListCertificates pages into a list of normalized cert dicts."""
    results = []
    seen = set()
    now = datetime.now(timezone.utc)
    for body in pages:
        items = body.get("certificates") or []
        if not isinstance(items, list):
            continue
        for item in items:
            if not isinstance(item, dict):
                continue
            cert_id = item.get("id")
            if cert_id and cert_id in seen:
                continue
            if cert_id:
                seen.add(cert_id)
            expire = item.get("expire_time")
            results.append({
                "id": cert_id or "",
                "name": item.get("name") or "",
                "domain": item.get("domain") or "",
                "sans": item.get("sans") or "",
                "type": type_family(item.get("type")),
                "type_raw": item.get("type") or "",
                "status": item.get("status") or "",
                "expire_time_raw": expire or "",
                "expire_time": format_time(expire),
                "days_left": days_left(expire, now),
                "source": cert_source(item),
                "brand": item.get("brand") or "",
                "domain_type": item.get("domain_type") or "",
                "deploy_support": item.get("deploy_support"),
                "enterprise_project_id": item.get("enterprise_project_id") or "",
            })
    return results


def filter_certs(certs, content=None, expiring=None):
    selected = certs
    if content:
        needle = str(content).strip().lower()
        selected = [
            c for c in selected
            if needle in (c["name"] or "").lower()
            or needle in (c["domain"] or "").lower()
            or needle in (c["sans"] or "").lower()
        ]
    if expiring is not None:
        selected = [c for c in selected
                    if c["days_left"] is not None and c["days_left"] <= expiring]
    return selected


def merge_pages(pages, region):
    """Merge ListCertificates pages into one raw response body."""
    merged = {"certificates": [], "total_count": 0, "region": region}
    for body in pages:
        for item in (body.get("certificates") or []):
            merged["certificates"].append(item)
        if body.get("total_count") not in (None, ""):
            merged["total_count"] = body.get("total_count")
    merged["total_count"] = merged["total_count"] or len(merged["certificates"])
    return merged


def source_distribution(certs):
    counts = {}
    for cert in certs:
        key = cert["source"] or "-"
        counts[key] = counts.get(key, 0) + 1
    return " / ".join("{0} {1}".format(k, counts[k]) for k in sorted(counts))


# ---------------------------------------------------------------------------
# Presentation
# ---------------------------------------------------------------------------

def render_table(header, rows):
    widths = [len(str(header[i])) for i in range(len(header))]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(str(cell)))
    lines = [" | ".join(str(header[i]).ljust(widths[i]) for i in range(len(header)))]
    lines.append("-+-".join("-" * w for w in widths))
    for row in rows:
        lines.append(" | ".join(str(row[i]).ljust(widths[i])
                                for i in range(len(header))))
    return "\n".join(lines)


def _days_text(cert):
    if cert["days_left"] is None:
        return "-"
    return str(cert["days_left"])


def render_rows(certs, region):
    rows = []
    for cert in certs:
        rows.append([
            cert["id"] or "-",
            cert["name"] or "-",
            cert["domain"] or "-",
            cert["type"] or "-",
            cert["status"] or "-",
            cert["expire_time"] or "-",
            _days_text(cert),
            region,
        ])
    return rows


def render_compact_rows(certs):
    rows = []
    for cert in certs:
        rows.append([
            cert["name"] or "-",
            cert["domain"] or "-",
            cert["expire_time"] or "-",
        ])
    return rows


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser():
    parser = argparse.ArgumentParser(
        prog="list_scm_certs.py",
        description="查询华为云 SCM（SSL 证书）列表（严格只读）",
    )
    parser.add_argument("--region", default=DEFAULT_REGION,
                        help="区域，默认 {0}".format(DEFAULT_REGION))
    parser.add_argument("--content", default=None,
                        help="按证书名称或绑定域名模糊查询（服务端 + 客户端双重过滤）")
    parser.add_argument("--expiring", type=int, default=None,
                        help="仅显示 N 天内到期的证书（客户端按到期时间精确过滤）")
    parser.add_argument("--expired-days-since", dest="expired_days_since",
                        type=int, default=None,
                        help="服务端过滤：有效期内或 N 天内到期")
    parser.add_argument("--enterprise-project-id", dest="enterprise_project_id",
                        default=None, help="企业项目 ID（可选，默认查询全部）")
    parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT,
                        help="每页数量，仅支持 10 / 20 / 50，默认 {0}".format(DEFAULT_LIMIT))
    parser.add_argument("--offset", type=int, default=0, help="起始偏移，默认 0")
    parser.add_argument("--max-pages", type=int, default=DEFAULT_MAX_PAGES,
                        help="最大分页数，默认 {0}".format(DEFAULT_MAX_PAGES))
    parser.add_argument("--table", action="store_true",
                        help="输出完整表格（8 列：ID/名称/域名/类型/状态/到期时间/剩余天数/region）")
    parser.add_argument("--json", action="store_true", help="输出原始响应 JSON")
    parser.add_argument("--backend", choices=("auto", "cli", "sdk"), default="auto",
                        help="后端: auto=CLI 优先、失败回退 SDK（默认）")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT,
                        help="单次调用超时秒数，默认 {0}".format(DEFAULT_TIMEOUT))
    parser.add_argument("--action", default="list",
                        help="动作，仅支持 list（默认）；其它值会被只读守卫拒绝")
    return parser


def _validate_args(args):
    if args.limit not in API_LIMITS:
        print("--limit 仅支持 {0}，当前为 {1}。".format(
            " / ".join(str(v) for v in API_LIMITS), args.limit), file=sys.stderr)
        return False
    if args.offset < 0:
        print("--offset 不能为负数，当前为 {0}。".format(args.offset), file=sys.stderr)
        return False
    if args.max_pages < 1:
        print("--max-pages 至少为 1，当前为 {0}。".format(args.max_pages),
              file=sys.stderr)
        return False
    if args.expiring is not None and args.expiring < 0:
        print("--expiring 不能为负数，当前为 {0}。".format(args.expiring),
              file=sys.stderr)
        return False
    return True


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    parser = build_parser()
    args = parser.parse_args(argv)

    guard_msg = guard_write_intent(args.action, args.content)
    if guard_msg:
        print(guard_msg)
        return 1

    if not _validate_args(args):
        return 1

    region = args.region
    backend = args.backend
    cli_bin = hcloud_binary()
    pages = []
    used_backend = None

    try:
        if backend in ("auto", "cli"):
            if cli_bin:
                try:
                    pages = fetch_pages_hcloud(
                        region, args.limit, args.offset, args.max_pages,
                        args.content, args.expired_days_since,
                        args.enterprise_project_id, args.timeout)
                    used_backend = "cli"
                except ScmError as exc:
                    if backend == "cli" or exc.kind in (
                            "forbidden", "credentials", "use_error"):
                        raise
                    print("hcloud 调用失败，回退 SDK：{0}".format(exc.message),
                          file=sys.stderr)
            elif backend == "cli":
                raise ScmError(
                    "cli_missing",
                    "未找到 hcloud（KooCLI），无法查询 SCM 证书列表。",
                    "安装 KooCLI 后重试（见 references/cli-installation-guide.md）。",
                )
        if used_backend is None and backend in ("auto", "sdk"):
            pages = fetch_pages_sdk(
                region, args.limit, args.offset, args.max_pages,
                args.content, args.expired_days_since,
                args.enterprise_project_id)
            used_backend = "sdk"
    except ScmError as exc:
        print(exc.message, file=sys.stderr)
        if exc.detail:
            print("详情: {0}".format(str(exc.detail)[:300]), file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("已取消。", file=sys.stderr)
        return 1
    except Exception as exc:  # never leak a traceback to the operator
        print("查询 SCM 证书列表时发生未预期错误：{0}".format(exc), file=sys.stderr)
        print("可尝试 --region <region> 或安装 KooCLI（见 references/"
              "cli-installation-guide.md）。", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(merge_pages(pages, region), ensure_ascii=False, indent=2))
        return 0

    certs = filter_certs(normalize_certificates(pages),
                         content=args.content, expiring=args.expiring)

    if not certs:
        if args.content or args.expiring is not None:
            print("未找到匹配的 SSL 证书（区域: {0}）。".format(region))
            print("可去掉过滤条件（--content / --expiring）后重试，"
                  "或确认证书是否创建在其他区域。")
        else:
            print("未找到 SSL 证书（区域: {0}）。".format(region))
            print("可更换 --region（如 cn-north-1 / ap-southeast-1）后重试；"
                  "该账号也可能尚未在 SCM 中签发或托管证书。")
        return 0

    if args.table:
        header = ["证书ID", "名称", "域名", "类型", "状态", "到期时间",
                  "剩余天数", "region"]
        print(render_table(header, render_rows(certs, region)))
    else:
        header = ["证书名称", "绑定域名", "到期时间"]
        print(render_table(header, render_compact_rows(certs)))

    print("\n共 {0} 个证书（区域: {1}，后端: {2}，来源: {3}）".format(
        len(certs), region, used_backend, source_distribution(certs)))
    return 0


if __name__ == "__main__":
    sys.exit(main())