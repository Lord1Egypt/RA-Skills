#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Huawei Cloud KMS key (CMK) inventory helper — strictly read-only.

Queries the KMS (Data Encryption Workshop / 数据加密服务) master-key list of the
current account in one region and prints alias / key ID / state / usage / type /
rotation / creation time.

Executed operations (both read-only):

    ListKeys               POST /v1.0/{project_id}/kms/list-keys
    ShowKeyRotationStatus  POST /v1.0/{project_id}/kms/get-key-rotation-status

Backends:

- primary:  KooCLI subprocess ``hcloud KMS ListKeys``
- fallback: official ``huaweicloudsdk`` KMS SDK (``huaweicloudsdkkms``)

Output modes:

- default:  compact list of 别名 | 密钥ID | 状态
- ``--table``: full 8-column table (密钥ID / 别名 / 状态 / 密钥用途 / 密钥类型 /
  轮转周期 / 创建时间 / region)
- ``--json``: the raw (merged) response body

Filtering: ``--alias`` (exact; ``--fuzzy`` for substring), ``--key-id``,
``--state`` (client-side; accepts 1-5 or state names), ``--region``.

Every mutating intent (create / enable / disable / schedule-deletion /
cancel-deletion / rotate / create-grant / ...) is rejected with exit code 1
before any command runs — this skill never writes to KMS.

Credentials are never hardcoded and never read by this script: the KooCLI
profile / environment is used by ``hcloud``; the SDK path reads AK/SK from
environment variables only.

Usage:
    python3 scripts/list_kms_keys.py [--region cn-north-4]
    python3 scripts/list_kms_keys.py --table
    python3 scripts/list_kms_keys.py --json
    python3 scripts/list_kms_keys.py --alias my-key --fuzzy
    python3 scripts/list_kms_keys.py --state enabled --key-id <id>
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from types import SimpleNamespace

SKILL_NAME = "huawei-cloud-kms-key-list"
DEFAULT_REGION = os.environ.get("HUAWEICLOUD_SDK_REGION", "cn-north-4")
DEFAULT_LIMIT = 100
MAX_LIMIT = 200
DEFAULT_MAX_PAGES = 50
DEFAULT_TIMEOUT = 60
MAX_ROTATION_QUERIES = 50

HCLOUD_BIN_ENV = ("HUAWEI_CLOUD_KMS_KEY_LIST_HCLOUD_BIN", "KMS_HCLOUD_BIN")

# Read-only operation whitelist: anything else is refused.
READONLY_OPERATIONS = ("ListKeys", "ShowKeyRotationStatus")
ALLOWED_ACTIONS = ("list", "ls", "query", "show")

# Tokens that indicate a mutating intent supplied by the caller.
WRITE_INTENT_TOKENS = (
    "create", "delete", "enable", "disable", "schedule", "cancel", "rotate",
    "rotation-enable", "rotation-disable", "grant", "revoke", "update",
    "modify", "import", "restore", "destroy", "put", "patch", "revoke-grant",
)


class KmsError(Exception):
    """Classified failure with a user-actionable message."""

    def __init__(self, kind, message, detail=""):
        Exception.__init__(self, message)
        self.kind = kind
        self.message = message
        self.detail = detail


# ---------------------------------------------------------------------------
# Write-intent guard
# ---------------------------------------------------------------------------

def guard_write_intent(action, alias, key_id):
    """Reject mutating intent before any cloud call.

    Returns the error message when a write intent is detected, else None.
    """
    if action:
        if str(action).strip().lower() not in ALLOWED_ACTIONS:
            return (
                "此技能为只读查询（KMS 密钥列表），拒绝执行非查询动作: {0}。"
                "支持的动作仅限 list（默认）。".format(action)
            )
    for field, value in (("--alias", alias), ("--key-id", key_id)):
        if not value:
            continue
        lowered = str(value).lower()
        for token in WRITE_INTENT_TOKENS:
            if token in lowered:
                return (
                    "此技能为只读查询（KMS 密钥列表），不支持对密钥执行写操作。"
                    "在 {0} 中检测到疑似写操作意图: {1}".format(field, token)
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
    binaries = hcloud_binary()
    if not binaries:
        raise KmsError(
            "cli_missing",
            "未找到 hcloud（KooCLI），无法查询 KMS 密钥列表。",
            "安装后可重试（见 references/cli-installation-guide.md），"
            "或改用 --backend sdk 走 SDK 回退。",
        )
    cmd = [binaries] + list(args)
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        raise KmsError(
            "timeout",
            "调用 hcloud 超时（{0} 秒），请检查网络或稍后重试。".format(timeout),
        )
    except OSError as exc:
        raise KmsError("cli_error", "无法执行 hcloud: {0}".format(exc))
    if proc.returncode != 0:
        detail = (proc.stderr or proc.stdout or "").strip()
        raise classify_cli_error(detail, proc.returncode)
    body = (proc.stdout or "").strip()
    try:
        return json.loads(body)
    except ValueError:
        match = re.search(r"\{.*\}", body, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except ValueError:
                pass
        raise KmsError(
            "bad_output",
            "hcloud 返回了非 JSON 输出，无法解析密钥列表。",
            body[:300],
        )


def classify_cli_error(detail, returncode=None):
    """Map a hcloud failure message onto an actionable KmsError."""
    text = detail or ""
    lowered = text.lower()
    if "[use_error]" in lowered:
        return KmsError(
            "use_error",
            "KooCLI 参数/用法错误（[USE_ERROR]），请检查 --region / --limit 取值"
            "（limit 需在 1~200 之间）。",
            text,
        )
    if ("403" in text or "not authorized" in lowered or "accessdenied" in lowered
            or "permission" in lowered or "kms.0301" in lowered
            or "pdp.permission" in lowered):
        return KmsError(
            "forbidden",
            "无权限访问 KMS 密钥列表（403），请检查 IAM 权限 kms:cmk:list"
            "（密钥轮转状态需 kms:cmk:getRotation）。",
            text,
        )
    if ("credential" in lowered or "ak/sk" in lowered or "ak, sk" in lowered
            or "no valid authentication" in lowered
            or "auth" in lowered.split()):
        return KmsError(
            "credentials",
            "缺少或无效的华为云凭据（AK/SK）。请在终端离线配置 KooCLI profile，"
            "或设置 HUAWEICLOUD_SDK_AK / HUAWEICLOUD_SDK_SK 环境变量后重试。",
            text,
        )
    if "404" in text:
        return KmsError(
            "not_found",
            "KMS 接口不存在（404），请确认 --region 是否支持 KMS（如 cn-north-4）。",
            text,
        )
    return KmsError(
        "cli_error",
        "hcloud 调用失败（exit={0}）。".format(returncode), text
    )


def fetch_pages_hcloud(region, limit, max_pages, timeout=DEFAULT_TIMEOUT,
                       key_spec="ALL"):
    """Call ListKeys page by page until truncated is false."""
    base = ["KMS", "ListKeys", "--cli-region=" + region, "--limit=" + str(limit)]
    if key_spec:
        base.append("--key_spec=" + key_spec)
    pages = []
    marker = None
    for _ in range(max_pages):
        args = list(base)
        if marker:
            args.append("--marker=" + str(marker))
        body = run_hcloud(args, timeout)
        pages.append(body)
        if not _is_truncated(body):
            break
        marker = body.get("next_marker") or body.get("nextMarker")
        if not marker:
            break
    return pages


def fetch_rotation_hcloud(region, key_id, timeout=DEFAULT_TIMEOUT):
    """ShowKeyRotationStatus for one key (read-only, best effort)."""
    return run_hcloud(
        ["KMS", "ShowKeyRotationStatus", "--cli-region=" + region,
         "--key_id=" + str(key_id)],
        timeout,
    )


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
        raise KmsError(
            "credentials",
            "缺少华为云凭据（AK/SK）。请在终端离线配置 KooCLI profile 或导出 "
            "HUAWEICLOUD_SDK_AK / HUAWEICLOUD_SDK_SK 环境变量后重试。"
        )
    return ak, sk


def sdk_client(region):
    """Build a KMS SDK client (lazy import keeps the CLI path dependency-free)."""
    try:
        from huaweicloudsdkcore.auth.credentials import BasicCredentials
        from huaweicloudsdkkms.v2 import KmsClient
        from huaweicloudsdkkms.v2.region.kms_region import KmsRegion
    except ImportError as exc:
        raise KmsError(
            "sdk_missing",
            "未安装华为云 KMS SDK（huaweicloudsdkkms），无法走 SDK 回退。",
            "pip install huaweicloudsdkcore huaweicloudsdkkms；"
            "或安装 KooCLI 走 CLI 主路径。原始错误: {0}".format(exc),
        )
    ak, sk = env_credentials()
    builder = KmsClient.new_builder().with_credentials(BasicCredentials(ak, sk))
    try:
        return builder.with_region(KmsRegion.value_of(region)).build()
    except Exception:
        from huaweicloudsdkcore.region.region import Region
        endpoint = "https://kms.{0}.myhuaweicloud.com".format(region)
        return builder.with_region(Region(id=region, endpoint=endpoint)).build()


def _sdk_request(name, **fields):
    """Build an SDK request model, or a plain attribute holder.

    The real model is used whenever ``huaweicloudsdkkms`` is importable; the
    light fallback keeps the code path testable (fake client) and keeps the
    error message about a missing SDK to the credential/client stage.
    """
    try:
        module = __import__("huaweicloudsdkkms.v2", fromlist=[name])
        request = getattr(module, name)()
    except Exception:
        request = SimpleNamespace()
    for key, value in fields.items():
        if value is not None:
            setattr(request, key, value)
    return request


def sdk_page(region, limit, marker=None):
    """One ListKeys page through the SDK, returned as a plain dict."""
    request = _sdk_request("ListKeysRequest", limit=str(limit),
                           key_spec="ALL", marker=marker)
    response = sdk_client(region).list_keys(request)
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
    for attr in ("keys", "key_details", "total", "truncated", "next_marker"):
        value = getattr(response, attr, None)
        if value is None:
            continue
        if isinstance(value, list) and value and hasattr(value[0], "to_dict"):
            data[attr] = [item.to_dict() for item in value]
        else:
            data[attr] = value
    return data


def fetch_pages_sdk(region, limit, max_pages):
    pages = []
    marker = None
    for _ in range(max_pages):
        body = sdk_page(region, limit, marker)
        pages.append(body)
        if not _is_truncated(body):
            break
        marker = body.get("next_marker") or body.get("nextMarker")
        if not marker:
            break
    return pages


def fetch_rotation_sdk(region, key_id):
    request = _sdk_request("ShowKeyRotationStatusRequest", key_id=str(key_id))
    return _response_to_dict(sdk_client(region).show_key_rotation_status(request))


# ---------------------------------------------------------------------------
# Normalization / filtering
# ---------------------------------------------------------------------------

def _is_truncated(body):
    value = body.get("truncated")
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() == "true"


STATE_LABELS = {
    "1": "待激活",
    "2": "启用",
    "3": "禁用",
    "4": "计划删除",
    "5": "待导入",
}

STATE_ALIASES = {
    "pending-activation": "1", "pending_activation": "1", "pendingactivation": "1",
    "enabled": "2", "enable": "2", "active": "2",
    "disabled": "3", "disable": "3",
    "pending-deletion": "4", "pending_deletion": "4", "pendingdeletion": "4",
    "pending-import": "5", "pending_import": "5", "pendingimport": "5",
}


def normalize_state(value):
    """Normalize a --state argument to the canonical 1-5 code, else None."""
    if value is None:
        return None
    text = str(value).strip().lower()
    if text in STATE_LABELS:
        return text
    return STATE_ALIASES.get(text)


def state_text(value):
    code = normalize_state(value)
    if code:
        return "{0}({1})".format(STATE_LABELS[code], code)
    return str(value) if value not in (None, "") else ""


def format_timestamp(value):
    """Render KMS creation_date (epoch ms or s, or plain string) as UTC time."""
    if value in (None, ""):
        return ""
    raw = str(value).strip()
    if raw.isdigit():
        number = int(raw)
        if number > 10 ** 11:  # milliseconds
            number = number / 1000.0
        try:
            return datetime.fromtimestamp(number, tz=timezone.utc).strftime(
                "%Y-%m-%d %H:%M:%S")
        except (ValueError, OverflowError, OSError):
            return raw
    return raw


def normalize_keys(pages):
    """Flatten ListKeys pages into a list of normalized key dicts."""
    results = []
    seen = set()
    for body in pages:
        details = body.get("key_details") or []
        if not isinstance(details, list):
            details = []
        if details:
            for item in details:
                if not isinstance(item, dict):
                    continue
                key_id = item.get("key_id")
                if key_id and key_id in seen:
                    continue
                if key_id:
                    seen.add(key_id)
                results.append({
                    "key_id": key_id or "",
                    "key_alias": item.get("key_alias") or "",
                    "key_state": item.get("key_state") or "",
                    "key_usage": item.get("key_usage") or "",
                    "key_spec": item.get("key_spec") or "",
                    "key_type": item.get("key_type") or "",
                    "key_rotation_enabled": _as_flag(
                        item.get("key_rotation_enabled")),
                    "creation_date": item.get("creation_date") or "",
                    "origin": item.get("origin") or "",
                    "realm": item.get("realm") or "",
                })
            continue
        # Fallback: only key IDs are returned (older/simplified responses).
        for key_id in (body.get("keys") or []):
            if isinstance(key_id, dict):
                key_id = key_id.get("key_id")
            if not key_id or key_id in seen:
                continue
            seen.add(key_id)
            results.append({
                "key_id": key_id,
                "key_alias": "",
                "key_state": "",
                "key_usage": "",
                "key_spec": "",
                "key_type": "",
                "key_rotation_enabled": None,
                "creation_date": "",
                "origin": "",
                "realm": "",
            })
    return results


def _as_flag(value):
    if value is None or value == "":
        return None
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() == "true"


def filter_keys(keys, alias=None, fuzzy=False, key_id=None, state=None):
    selected = keys
    if key_id:
        needle = key_id.strip().lower()
        selected = [k for k in selected if needle in (k["key_id"] or "").lower()]
    if alias:
        needle = alias.strip().lower()
        if fuzzy:
            selected = [k for k in selected if needle in (k["key_alias"] or "").lower()]
        else:
            selected = [k for k in selected if (k["key_alias"] or "").lower() == needle]
    code = normalize_state(state)
    if code:
        selected = [k for k in selected if str(k["key_state"]).strip() == code]
    return selected


def merge_pages(pages):
    """Merge ListKeys pages into one raw response body."""
    merged = {"keys": [], "key_details": [], "truncated": "false",
              "next_marker": "", "total": 0}
    for body in pages:
        for key_id in (body.get("keys") or []):
            merged["keys"].append(key_id)
        for item in (body.get("key_details") or []):
            merged["key_details"].append(item)
        if body.get("total") not in (None, ""):
            merged["total"] = body.get("total")
    merged["total"] = merged["total"] or len(merged["key_details"]) or len(merged["keys"])
    return merged


# ---------------------------------------------------------------------------
# Presentation
# ---------------------------------------------------------------------------

def render_rows(keys, region, rotation=None):
    rows = []
    for key in keys:
        rows.append([
            key["key_id"] or "",
            key["key_alias"] or "",
            state_text(key["key_state"]),
            key["key_usage"] or "",
            key["key_spec"] or "",
            _rotation_text(key, rotation),
            format_timestamp(key["creation_date"]),
            region,
        ])
    return rows


def _rotation_text(key, rotation):
    rotation = rotation or {}
    interval = rotation.get(key["key_id"])
    enabled = key["key_rotation_enabled"]
    if interval:
        return "开启({0}天)".format(interval)
    if enabled is True:
        return "开启"
    if enabled is False:
        return "关闭"
    return "-"


def render_table(header, rows):
    widths = [len(header[i]) for i in range(len(header))]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(str(cell)))
    lines = [" | ".join(header[i].ljust(widths[i]) for i in range(len(header)))]
    lines.append("-+-".join("-" * w for w in widths))
    for row in rows:
        lines.append(" | ".join(str(row[i]).ljust(widths[i])
                                for i in range(len(header))))
    return "\n".join(lines)


def rotation_intervals(keys, region, backend, cli_bin, timeout):
    """Fetch rotation intervals for rotation-enabled keys (best effort)."""
    intervals = {}
    queried = 0
    for key in keys:
        if key["key_rotation_enabled"] is not True:
            continue
        if queried >= MAX_ROTATION_QUERIES:
            break
        queried += 1
        try:
            if backend == "sdk":
                body = fetch_rotation_sdk(region, key["key_id"])
            else:
                body = fetch_rotation_hcloud(region, key["key_id"], timeout)
        except KmsError:
            continue
        except Exception:
            continue
        value = body.get("rotation_interval")
        if value not in (None, ""):
            intervals[key["key_id"]] = value
    return intervals


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser():
    parser = argparse.ArgumentParser(
        prog="list_kms_keys.py",
        description="查询华为云 KMS 密钥（CMK）列表（严格只读）",
    )
    parser.add_argument("--region", default=DEFAULT_REGION,
                        help="区域，默认 {0}".format(DEFAULT_REGION))
    parser.add_argument("--alias", default=None, help="按密钥别名过滤（默认精确匹配）")
    parser.add_argument("--fuzzy", action="store_true",
                        help="--alias 使用模糊（子串）匹配")
    parser.add_argument("--key-id", dest="key_id", default=None,
                        help="按密钥 ID 过滤（子串匹配）")
    parser.add_argument("--state", default=None,
                        help="按密钥状态过滤: 1-5 或 enabled/disabled/"
                             "pending-deletion/pending-import/pending-activation")
    parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT,
                        help="每页数量 1~200，默认 {0}".format(DEFAULT_LIMIT))
    parser.add_argument("--max-pages", type=int, default=DEFAULT_MAX_PAGES,
                        help="最大分页数，默认 {0}".format(DEFAULT_MAX_PAGES))
    parser.add_argument("--table", action="store_true",
                        help="输出完整表格（8 列，含用途/类型/轮转/创建时间）")
    parser.add_argument("--json", action="store_true", help="输出原始响应 JSON")
    parser.add_argument("--no-rotation-detail", action="store_true",
                        help="表格不逐 key 查询轮转周期（省去 N 次只读调用）")
    parser.add_argument("--backend", choices=("auto", "cli", "sdk"), default="auto",
                        help="后端: auto=CLI 优先、失败回退 SDK（默认）")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT,
                        help="单次调用超时秒数，默认 {0}".format(DEFAULT_TIMEOUT))
    parser.add_argument("--action", default="list",
                        help="动作，仅支持 list（默认）；其它值会被只读守卫拒绝")
    return parser


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    parser = build_parser()
    args = parser.parse_args(argv)

    guard_msg = guard_write_intent(args.action, args.alias, args.key_id)
    if guard_msg:
        print(guard_msg)
        return 1

    if args.limit < 1 or args.limit > MAX_LIMIT:
        print("--limit 取值须在 1~{0} 之间，当前为 {1}。".format(MAX_LIMIT, args.limit),
              file=sys.stderr)
        return 1
    if args.state is not None and normalize_state(args.state) is None:
        print("--state 取值无效: {0}。可选 1-5 或 enabled/disabled/"
              "pending-deletion/pending-import/pending-activation。".format(args.state),
              file=sys.stderr)
        return 1
    if args.fuzzy and not args.alias:
        print("提示: --fuzzy 仅在配合 --alias 时生效。", file=sys.stderr)

    region = args.region
    backend = args.backend
    cli_bin = hcloud_binary()
    pages = []
    used_backend = None

    try:
        if backend in ("auto", "cli"):
            if cli_bin:
                try:
                    pages = fetch_pages_hcloud(region, args.limit, args.max_pages,
                                               args.timeout)
                    used_backend = "cli"
                except KmsError as exc:
                    if backend == "cli" or exc.kind in ("forbidden", "credentials"):
                        raise
                    print("hcloud 调用失败，回退 SDK：{0}".format(exc.message),
                          file=sys.stderr)
            elif backend == "cli":
                raise KmsError(
                    "cli_missing",
                    "未找到 hcloud（KooCLI），无法查询 KMS 密钥列表。",
                    "安装 KooCLI 后重试（见 references/cli-installation-guide.md）。",
                )
        if used_backend is None and backend in ("auto", "sdk"):
            pages = fetch_pages_sdk(region, args.limit, args.max_pages)
            used_backend = "sdk"
    except KmsError as exc:
        print(exc.message, file=sys.stderr)
        if exc.detail:
            print("详情: {0}".format(str(exc.detail)[:300]), file=sys.stderr)
        return 1

    if args.json:
        merged = merge_pages(pages)
        merged["region"] = region
        print(json.dumps(merged, ensure_ascii=False, indent=2))
        return 0

    keys = filter_keys(normalize_keys(pages), alias=args.alias, fuzzy=args.fuzzy,
                       key_id=args.key_id, state=args.state)

    if not keys:
        if args.alias or args.key_id or args.state:
            print("未找到匹配的 KMS 密钥（区域: {0}）。".format(region))
            print("可去掉过滤条件后重试，或确认密钥是否创建在其他区域。")
        else:
            print("当前区域无 KMS 密钥（区域: {0}）。".format(region))
            print("可更换 --region（如 cn-north-1 / cn-east-3）后重试；"
                  "该账号也可能尚未创建自定义密钥。")
        return 0

    rotation = None
    if args.table and not args.no_rotation_detail:
        rotation = rotation_intervals(keys, region, used_backend, cli_bin,
                                      args.timeout)

    if args.table:
        header = ["密钥ID", "别名", "状态", "密钥用途", "密钥类型",
                  "轮转周期", "创建时间", "region"]
        print(render_table(header, render_rows(keys, region, rotation)))
    else:
        header = ["别名", "密钥ID", "状态"]
        rows = [[k["key_alias"] or "", k["key_id"] or "", state_text(k["key_state"])]
                for k in keys]
        print(render_table(header, rows))

    print("\n共 {0} 个密钥（区域: {1}，后端: {2}）".format(len(keys), region, used_backend))
    return 0


if __name__ == "__main__":
    sys.exit(main())