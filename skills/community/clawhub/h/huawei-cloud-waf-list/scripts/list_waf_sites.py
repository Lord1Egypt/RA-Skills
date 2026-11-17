#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Huawei Cloud WAF protected-website list helper.

Queries the list of domain names protected by Web Application Firewall (WAF)
under the current account through KooCLI (``hcloud WAF <Operation>``),
covering both cloud-mode (弹性云模式) and dedicated/premium-mode (独享模式)
protected domains.

Executed operations (all read-only GET, REST paths from the KooCLI WAF
metadata ``ListHost_origin_en.yaml`` / ``ListCompositeHosts_origin_en.yaml``):

    ListCompositeHosts   GET /v1/{project_id}/composite-waf/host
    ListHost             GET /v1/{project_id}/waf/instance

Output modes:

- default: a compact table of 防护域名 | 防护状态 | 接入方式 | 保活方式 | 是否独享IP for every
  protected domain (all WAF modes when ``--all-modes`` is used).
- ``--json``: the raw response body (list of host objects).
- ``--names-only``: one domain name per line (unique), sorted.

Write intents (create / delete / update / migrate / rename / batch / ...) are
rejected with an explicit error before any command runs — this skill is
strictly read-only.

Secrets are never hardcoded: AK/SK come from the active KooCLI profile or the
environment. The script never reads, echoes, or stores them.

Usage:
    python3 scripts/list_waf_sites.py [--region cn-north-4]
    python3 scripts/list_waf_sites.py [--all-modes|--mode cloud|--mode premium] --json
    python3 scripts/list_waf_sites.py --names-only
    python3 scripts/list_waf_sites.py --hostname example.com --protect-status enabled
"""

import argparse
import json
import os
import shutil
import subprocess
import sys

SKILL_NAME = "huawei-cloud-waf-list"
SKILL_VERSION = "1.0.0"
DEFAULT_REGION = "cn-north-4"
DEFAULT_TIMEOUT = 60

# ---------------------------------------------------------------------------
# CLI backend helpers
# ---------------------------------------------------------------------------

def _hcloud_binary():
    """Return the hcloud binary path or None."""
    return shutil.which("hcloud")


def _hcloud(args, timeout=DEFAULT_TIMEOUT):
    """Run hcloud and return parsed JSON.

    Raises RuntimeError on non-zero exit or unparseable output.
    """
    proc = subprocess.run(
        args,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    if proc.returncode != 0:
        detail = (proc.stderr or proc.stdout or "").strip()
        raise RuntimeError(
            f"hcloud command failed (exit={proc.returncode}): {detail[:500]}"
        )
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError:
        raise RuntimeError(
            f"hcloud returned non-JSON output: {(proc.stdout or '')[:300]}"
        )


# ---------------------------------------------------------------------------
# WAF operations
# ---------------------------------------------------------------------------

def _list_cloud_hosts(region, cli_bin, extra, timeout=DEFAULT_TIMEOUT):
    """hcloud WAF ListHost — cloud-mode protected domains.

    GET /v1/{project_id}/waf/instance
    """
    cmd = [cli_bin, "WAF", "ListHost", "--cli-region=" + region]
    for param in ("enterprise_project_id", "hostname", "page", "pagesize",
                  "policyname"):
        val = extra.get(param)
        if val is not None:
            cmd.append("--{0}={1}".format(param, val))
    data = _hcloud(cmd, timeout)
    items = data.get("items") or []
    for it in items:
        it.setdefault("waf_type", "cloud")
    return _extract_hosts(data, items)


def _list_composite_hosts(region, cli_bin, extra, timeout=DEFAULT_TIMEOUT):
    """hcloud WAF ListCompositeHosts — domains across all WAF instances.

    GET /v1/{project_id}/composite-waf/host
    """
    cmd = [cli_bin, "WAF", "ListCompositeHosts", "--cli-region=" + region]
    for param in ("enterprise_project_id", "hostname", "is_https", "page",
                  "pagesize", "policyname", "protect_status"):
        val = extra.get(param)
        if val is not None:
            cmd.append("--{0}={1}".format(param, val))
    data = _hcloud(cmd, timeout)
    items = data.get("items") or []
    return _extract_hosts(data, items)


def _extract_hosts(data, items):
    """Normalize a host list response into a flat list of host objects."""
    results = []
    for it in (items or []):
        results.append({
            "hostname": it.get("hostname"),
            "hostid": it.get("hostid") or it.get("id"),
            "protect_status": it.get("protect_status"),
            "access_status": it.get("access_status"),
            "proxy": it.get("proxy"),
            "exclusive_ip": it.get("exclusive_ip"),
            "waf_type": it.get("waf_type"),
            "policyid": it.get("policyid"),
            "web_tag": it.get("web_tag"),
            "server": it.get("server") or [],
        })
    return data, results


# ---------------------------------------------------------------------------
# Presentation
# ---------------------------------------------------------------------------

_PROTECT_DESC = {-1: "bypass(已绕过)", 0: "suspended(仅转发)", 1: "enabled(已防护)"}
_MODE_DESC = {"cloud": "云模式", "premium": "独享模式"}
_KEEP_DESC = {True: "proxy(代理)", False: "direct(直连)"}


def _protect_text(val):
    try:
        return _PROTECT_DESC.get(int(val), str(val))
    except (TypeError, ValueError):
        return str(val)


def _mode_text(val):
    return _MODE_DESC.get(val, val)


def _keep_text(val):
    if val is None:
        return ""
    try:
        return _KEEP_DESC.get(bool(val), str(val))
    except ValueError:
        return str(val)


def _render_table(results):
    """Render the default compact table (Chinese key labels)."""
    rows = []
    for h in results:
        rows.append([
            h["hostname"] or "",
            _protect_text(h["protect_status"]),
            _mode_text(h.get("waf_type")),
            _keep_text(h.get("proxy")),
            "是" if h.get("exclusive_ip") else "否",
            h.get("hostid") or "",
        ])
    header = ["防护域名", "防护状态", "接入方式", "保活方式", "独享IP", "Domain ID"]
    widths = [max(len(header[i]), *(len(r[i]) for r in rows)) if rows else len(header[i])
              for i in range(len(header))]
    lines = [" | ".join(header[i].ljust(widths[i]) for i in range(len(header)))]
    lines.append("-+-".join("-" * w for w in widths))
    for r in rows:
        lines.append(" | ".join(str(r[i]).ljust(widths[i]) for i in range(len(r))))
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Guard: strictly read-only
# ---------------------------------------------------------------------------

_WRITE_INTENT = (
    "create", "delete", "update", "remove", "rename", "migrate", "batch",
    "apply", "switch", "change", "modify", "add", "set", "restore",
    "publish", "unpublish", "import", "export",
)


def _check_read_only(hostname):
    """Reject any write-like intent in the domain parameter.

    Returns the error message when a write intent is detected, else None.
    """
    if not hostname:
        return None
    lowered = hostname.lower()
    for token in _WRITE_INTENT:
        if token in lowered:
            return (
                "此技能为只读查询（WAF 防护网站列表），不支持对防护域名进行操作。"
                "检测到疑似写操作意图: {0}".format(token)
            )
    return None


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="list_waf_sites.py",
        description="查询华为云 WAF 已防护网站/域名列表（只读）",
    )
    parser.add_argument("--region", default=os.environ.get(
        "HUAWEICLOUD_SDK_REGION", DEFAULT_REGION),
        help="区域，默认 cn-north-4")
    parser.add_argument("--json", action="store_true",
                        help="输出原始 JSON 响应体")
    parser.add_argument("--names-only", action="store_true",
                        help="仅输出域名列表（去重排序）")
    parser.add_argument("--all-modes", action="store_true",
                        help="查询所有 WAF 模式（云模式 + 独享模式）防护域名")
    parser.add_argument("--mode", choices=("cloud", "premium"),
                        default=None,
                        help="接入方式: cloud=云模式 / premium=独享模式（需 --all-modes 下无意义）")
    parser.add_argument("--hostname", default=None,
                        help="按域名过滤")
    parser.add_argument("--protect-status", choices=("-1", "0", "1"),
                        default=None,
                        help="防护状态: -1 绕过 / 0 暂停 / 1 已防护")
    parser.add_argument("--enterprise-project-id", default=None,
                        help="企业项目 ID，默认 0；查询全部企业项目用 all_granted_eps")
    parser.add_argument("--policyname", default=None,
                        help="防护策略名过滤")
    parser.add_argument("--pagesize", default="-1",
                        help="每页数量 1-100，-1 表示一次查询全部（默认 -1）")
    args = parser.parse_args(argv)

    guard_msg = _check_read_only(args.hostname)
    if guard_msg:
        print(guard_msg)
        return 1

    cli_bin = _hcloud_binary()
    if not cli_bin:
        print("未找到 hcloud CLI。请先安装并配置 KooCLI："
              "https://support.huaweicloud.com/qs-hcli/hcli_02_003.html",
              file=sys.stderr)
        return 1

    extra = {
        "enterprise_project_id": args.enterprise_project_id,
        "hostname": args.hostname,
        "pagesize": args.pagesize,
        "policyname": args.policyname,
        "protect_status": args.protect_status,
    }

    try:
        if args.mode == "premium":
            # 独享模式：使用 ListCompositeHosts 并按 waf_type=premium 过滤
            data, results = _list_composite_hosts(args.region, cli_bin, extra)
            results = [h for h in results if h.get("waf_type") == "premium"]
            data = {"items": results}
        elif args.mode == "cloud" or not args.all_modes:
            data, results = _list_cloud_hosts(args.region, cli_bin, extra)
        else:
            data, results = _list_composite_hosts(args.region, cli_bin, extra)
    except RuntimeError as exc:
        msg = str(exc)
        if "WAF.00012006" in msg or "not authorized" in msg or "pdp.permission" in msg:
            print("无权限访问 WAF 防护网站列表，请检查 IAM 权限（waf:host:list）。", file=sys.stderr)
        elif "APIGW.0802" in msg:
            print("当前账号在该区域不可用（APIGW.0802），请更换 --region。", file=sys.stderr)
        else:
            print(msg, file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return 0

    if args.names_only:
        names = sorted({h["hostname"] for h in results if h.get("hostname")})
        for n in names:
            print(n)
        return 0

    if not results:
        print("当前区域无 WAF 防护网站。" if not (args.hostname or args.protect_status)
              else "未找到匹配的防护网站。")
        return 0

    print(_render_table(results))
    print("\n共 {0} 个防护网站（区域: {1}）".format(len(results), args.region))
    return 0


if __name__ == "__main__":
    sys.exit(main())