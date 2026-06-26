#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitCode 合入 PR 质量抽检：按时间范围拉取已合并 PR，按多维度检查，输出表格。
仅使用 Python 3.7+ 标准库；需 GITCODE_TOKEN。
支持 Linux / macOS / Windows。
"""

import argparse
import csv
import json
import os
import random
import subprocess
import sys
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

GITCODE_API_BASE = "https://api.gitcode.com/api/v5"
SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent

DEFAULT_TIMEZONE = "Asia/Shanghai"
SHANGHAI_UTC_OFFSET_HOURS = 8
REQUEST_SLEEP_SEC = 0.3
REQUEST_TIMEOUT_SEC = 30
RETRY_TIMES = 2
RETRY_INTERVAL_SEC = 2
DEFAULT_DAYS = 30
SAMPLE_MIN, SAMPLE_MAX = 5, 10

# 表格列：无单独“链接”，PR 列含链接；各维度列为详情文案
HEADERS = [
    "仓库", "PR", "标题",
    "评论未解决", "缺必选标签", "新增超行数", "无测试", "多Issue", "缺检视", "标题/描述不清晰",
    "问题汇总",
]
DIMENSION_KEYS = [
    "comment_detail", "labels_detail", "additions_detail", "no_test_detail",
    "multi_issue_detail", "lack_review_detail", "title_body_unclear_detail",
]
DIMENSION_NAMES_CN = [
    "评论未解决", "缺必选标签", "新增超行数", "无测试", "多Issue", "缺检视", "标题/描述不清晰",
]
# 用于 problem_summary 的布尔键（与详情对应）
DIMENSION_BOOL_KEYS = [
    "comment_unresolved", "missing_labels", "over_additions", "no_test",
    "multi_issue", "lack_review", "title_body_unclear",
]


def _get_token_windows(scope):
    """Windows 下读取用户级或系统级 GITCODE_TOKEN。"""
    if sys.platform != "win32":
        return None
    try:
        out = subprocess.check_output(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                "[Environment]::GetEnvironmentVariable('GITCODE_TOKEN','%s')" % scope,
            ],
            creationflags=0x08000000,
            timeout=5,
            stderr=subprocess.DEVNULL,
        )
        if out:
            return out.decode("utf-8", errors="replace").strip()
    except Exception:
        pass
    return None


def get_token():
    """GITCODE_TOKEN：进程环境变量 → Windows 用户级 → 系统级。"""
    token = os.environ.get("GITCODE_TOKEN")
    if token:
        return token.strip()
    for scope in ("User", "Machine"):
        t = _get_token_windows(scope)
        if t:
            return t
    return None


def _err_detail(e, path, url=None):
    parts = [path]
    if isinstance(e, HTTPError):
        parts.append("HTTP %s" % e.code)
        try:
            body = e.read().decode("utf-8", errors="replace")[:500]
            if body.strip():
                parts.append("body: %s" % body.strip())
        except Exception:
            pass
    else:
        parts.append(str(e))
    if url:
        parts.append("url: %s" % url)
    return " | ".join(parts)


def api_get(token, path, params=None, timeout_sec=REQUEST_TIMEOUT_SEC):
    """请求 GitCode API；请求后 sleep；失败重试。返回 (data, error_str)。"""
    url = GITCODE_API_BASE.rstrip("/") + "/" + path.lstrip("/")
    if params:
        url = url + ("&" if "?" in url else "?") + urlencode(params)
    url = url.replace(" ", "%20")
    req = Request(url, headers={"PRIVATE-TOKEN": token})
    last_err = None
    for attempt in range(RETRY_TIMES + 1):
        try:
            with urlopen(req, timeout=timeout_sec) as resp:
                time.sleep(REQUEST_SLEEP_SEC)
                raw = resp.read().decode("utf-8")
                return (json.loads(raw), None)
        except HTTPError as e:
            last_err = _err_detail(e, path, url)
            if e.code == 429:
                wait = int(e.headers.get("Retry-After", 60))
                time.sleep(min(wait, 120))
            else:
                time.sleep(RETRY_INTERVAL_SEC)
        except (URLError, OSError, ValueError) as e:
            last_err = _err_detail(e, path, url)
            time.sleep(RETRY_INTERVAL_SEC)
        except Exception as e:
            last_err = _err_detail(e, path, url)
            break
    return None, (last_err or "请求失败")


def get_branches(token, owner, repo):
    """GET /repos/:owner/:repo/branches。"""
    return api_get(token, "repos/%s/%s/branches" % (owner, repo), {"per_page": 100})


def resolve_branch(token, owner, repo, specified_branch=None):
    """
    若 specified_branch 有值则校验该分支存在；否则依次尝试 master → develop → main。
    返回 (branch_name, error)。
    """
    data, err = get_branches(token, owner, repo)
    if err:
        return None, "获取分支列表失败: %s" % err
    names = {b.get("name") for b in (data or []) if b.get("name")}
    if specified_branch:
        if specified_branch in names:
            return specified_branch, None
        return None, "仓库 %s/%s 中未找到分支: %s" % (owner, repo, specified_branch)
    for candidate in ("master", "develop", "main"):
        if candidate in names:
            return candidate, None
    return None, "仓库 %s/%s 中未找到 master、develop 或 main，请使用 --branch 指定。当前: %s" % (
        owner, repo, ", ".join(sorted(names)[:20]) or "无",
    )


def parse_date_utc(date_str, end_of_day=False):
    """YYYY-MM-DD 转为 UTC 时间（上海 00:00 或 23:59:59），带 timezone。"""
    try:
        local_dt = datetime.strptime(date_str.strip()[:10], "%Y-%m-%d")
        utc_dt = local_dt - timedelta(hours=SHANGHAI_UTC_OFFSET_HOURS)
        if end_of_day:
            utc_dt = utc_dt.replace(hour=23, minute=59, second=59, microsecond=999999)
        return utc_dt.replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def load_config(config_path=None):
    """加载 config.json，缺失键用默认值。"""
    path = Path(config_path) if config_path else (SKILL_ROOT / "config.json")
    defaults = {
        "required_labels": ["ci-pipeline-passed", "approved", "lgtm"],
        "max_additions": 1000,
        "review_lines_threshold": 500,
        "title_min_length": 5,
        "body_min_length": 10,
        "test_substrings": ["test", "ut"],
    }
    if not path.is_file():
        return defaults
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        for k, v in defaults.items():
            if k not in data:
                data[k] = v
        return data
    except Exception:
        return defaults


def list_merged_pulls(token, owner, repo, base_ref, since_utc, until_utc):
    """
    拉取 state=merged 的 PR，过滤 base.ref == base_ref 且 merged_at 在 [since_utc, until_utc]。
    返回 (list of {number, title, merged_at, html_url}, error)。
    """
    result = []
    page = 1
    per_page = 100
    while True:
        data, err = api_get(
            token,
            "repos/%s/%s/pulls" % (owner, repo),
            {"state": "merged", "per_page": per_page, "page": page},
        )
        if err:
            return [], err
        lst = data if isinstance(data, list) else []
        if not lst:
            break
        for pr in lst:
            base = pr.get("base") or {}
            ref = (base.get("ref") or base.get("name") or "").strip()
            if ref != base_ref:
                continue
            merged_at = pr.get("merged_at") or ""
            if not merged_at:
                continue
            try:
                if "T" in merged_at:
                    dt = datetime.fromisoformat(merged_at.replace("Z", "+00:00"))
                else:
                    dt = datetime.strptime(merged_at[:10], "%Y-%m-%d").replace(tzinfo=timezone.utc)
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
            except Exception:
                continue
            if since_utc and dt < since_utc:
                continue
            if until_utc and dt > until_utc:
                continue
            result.append({
                "number": pr.get("number") or pr.get("id"),
                "title": (pr.get("title") or "").strip(),
                "merged_at": merged_at,
                "html_url": (pr.get("html_url") or pr.get("url") or "").strip(),
            })
        if len(lst) < per_page:
            break
        page += 1
    return result, None


def get_pull_detail(token, owner, repo, number):
    """GET 单个 PR 详情。"""
    return api_get(token, "repos/%s/%s/pulls/%s" % (owner, repo, number))


def get_pull_labels(token, owner, repo, number):
    """GET PR 标签列表（先 pulls 再 merge_requests），返回 label name 集合。"""
    for path_prefix in ("pulls", "merge_requests"):
        data, err = api_get(token, "repos/%s/%s/%s/%s/labels" % (owner, repo, path_prefix, number))
        if err or not data:
            continue
        names = set()
        for item in (data if isinstance(data, list) else [data]):
            n = item.get("name") if isinstance(item, dict) else None
            if n:
                names.add(str(n).strip())
        if names or data:
            return names
    return set()


def _is_diff_comment(c):
    """判断是否为 diff/行内检视评论（兼容多种 API 字段）。"""
    ct = (c.get("comment_type") or c.get("type") or c.get("noteable_type") or "").strip().lower()
    if ct in ("diff_comment", "diffcomment", "diff", "line_note", "note"):
        return True
    # 有 line_code / position / path 的也视为行内评论
    if c.get("line_code") or c.get("position") or c.get("path") or c.get("line"):
        return True
    return False


def _is_resolved(c):
    """判断评论是否已解决（兼容多种 API 字段）。"""
    resolved = c.get("resolved")
    if resolved is True or (isinstance(resolved, str) and resolved.lower() in ("true", "1", "yes")):
        return True
    if c.get("resolved_at"):
        return True
    if (c.get("state") or "").strip().lower() in ("resolved", "closed"):
        return True
    if resolved is False or (isinstance(resolved, str) and resolved.lower() in ("false", "0", "no")):
        return False
    return False


def get_pull_comments(token, owner, repo, number):
    """GET PR 评论；先试 pulls，再试 merge_requests。返回原始列表。"""
    for path_prefix in ("pulls", "merge_requests"):
        path = "repos/%s/%s/%s/%s/comments" % (owner, repo, path_prefix, number)
        data, err = api_get(token, path)
        if err:
            continue
        if data is not None:
            return data if isinstance(data, list) else [data]
    return []


def get_pull_files(token, owner, repo, number):
    """GET PR 变更文件（先 pulls 再 merge_requests；/files/json 或 /files），返回 list of { filename, additions }。"""
    for path_prefix in ("pulls", "merge_requests"):
        for path_suffix in ("/files/json", "/files"):
            data, err = api_get(
                token,
                "repos/%s/%s/%s/%s%s" % (owner, repo, path_prefix, number, path_suffix),
            )
            if err:
                continue
            lst = data if isinstance(data, list) else []
            out = []
            for item in lst:
                if isinstance(item, dict):
                    fn = item.get("filename") or item.get("file_name") or item.get("new_file") or ""
                    add = item.get("additions")
                    if add is None:
                        add = 0
                    try:
                        add = int(add)
                    except (TypeError, ValueError):
                        add = 0
                    out.append({"filename": fn, "additions": add})
            if out:
                return out
    return []


def get_pull_issues(token, owner, repo, number):
    """GET PR 关联 issues（先 pulls 再 merge_requests），返回列表长度。"""
    for path_prefix in ("pulls", "merge_requests"):
        data, err = api_get(token, "repos/%s/%s/%s/%s/issues" % (owner, repo, path_prefix, number))
        if not err and data is not None:
            lst = data if isinstance(data, list) else [data] if data else []
            return len(lst)
    return 0


def _get_pull_detail_any_path(token, owner, repo, number):
    """获取 PR 详情，先试 pulls 再试 merge_requests。"""
    for path_prefix in ("pulls", "merge_requests"):
        path = "repos/%s/%s/%s/%s" % (owner, repo, path_prefix, number)
        data, err = api_get(token, path)
        if not err and data and isinstance(data, dict):
            return data, None
    return None, "无法获取 PR 详情（pulls 与 merge_requests 均失败）"


def audit_one_pr(token, owner, repo, pr_info, config):
    """
    对单个 PR 做 8 维检查，返回 dict：含 DIMENSION_BOOL_KEYS、详情文案（*_detail）及 title, link 等。
    """
    number = pr_info.get("number")
    title = (pr_info.get("title") or "").strip()
    link = (pr_info.get("html_url") or "").strip()
    if not link and owner and repo and number:
        link = "https://gitcode.com/%s/%s/merge_requests/%s" % (owner, repo, number)
    if not link:
        link = "https://gitcode.com/%s/%s/pulls/%s" % (owner, repo, number)

    detail, err = _get_pull_detail_any_path(token, owner, repo, number)
    if err:
        return None, err
    body = (detail.get("body") or "").strip() if isinstance(detail, dict) else ""
    if not title and isinstance(detail, dict):
        title = (detail.get("title") or "").strip()

    labels = get_pull_labels(token, owner, repo, number)
    required = set(config.get("required_labels") or [])
    missing_set = required - labels if required else set()
    missing_labels = bool(missing_set)
    labels_detail = "是（缺：%s）" % "、".join(sorted(missing_set)) if missing_set else "否"

    comments = get_pull_comments(token, owner, repo, number)
    diff_total = 0
    diff_resolved = 0
    for c in comments:
        if not _is_diff_comment(c):
            continue
        diff_total += 1
        if _is_resolved(c):
            diff_resolved += 1
    unresolved_count = diff_total - diff_resolved
    comment_unresolved = unresolved_count > 0
    if diff_total == 0:
        comment_detail = "否（0/0）"
    elif comment_unresolved:
        comment_detail = "是（%s/%s）" % (unresolved_count, diff_total)
    else:
        comment_detail = "否（%s/%s）" % (diff_resolved, diff_total)

    files = get_pull_files(token, owner, repo, number)
    total_additions = sum(f.get("additions", 0) for f in files)
    max_additions = int(config.get("max_additions") or 1000)
    over_additions = total_additions > max_additions
    additions_detail = "是（%s）" % total_additions if over_additions else "否（%s）" % total_additions

    test_substrings = config.get("test_substrings") or ["test", "ut"]
    has_test = False
    for f in files:
        fn = (f.get("filename") or "").lower()
        for sub in test_substrings:
            if sub.lower() in fn:
                has_test = True
                break
        if has_test:
            break
    no_test = not has_test and bool(files)
    no_test_detail = "是" if no_test else "否"

    issue_count = get_pull_issues(token, owner, repo, number)
    multi_issue = issue_count > 1
    multi_issue_detail = "是（%s）" % issue_count if multi_issue else "否（%s）" % issue_count

    review_threshold = int(config.get("review_lines_threshold") or 500)
    lack_review = total_additions > review_threshold and diff_total == 0
    if lack_review:
        lack_review_detail = "是（新增%s行，0个检视）" % total_additions
    elif total_additions > review_threshold and diff_total > 0:
        lack_review_detail = "否（新增%s行，%s个检视）" % (total_additions, diff_total)
    else:
        lack_review_detail = "否"

    title_min = int(config.get("title_min_length") or 5)
    body_min = int(config.get("body_min_length") or 10)
    title_short = len(title) < title_min
    body_short = len(body) < body_min
    generic_titles = ("fix", "update", "修改", "优化", "fix.", "updates")
    title_generic = title.lower().strip() in generic_titles and (body_short or len(body) < 20)
    title_body_unclear = title_short or body_short or title_generic
    unclear_reasons = []
    if title_short:
        unclear_reasons.append("标题过短（%s字）" % len(title))
    if body_short:
        unclear_reasons.append("描述过短（%s字）" % len(body))
    if title_generic and not title_short and not body_short:
        unclear_reasons.append("标题或描述过于笼统")
    title_body_unclear_detail = "是（%s）" % "；".join(unclear_reasons) if unclear_reasons else "否"

    row = {
        "repo": "%s/%s" % (owner, repo),
        "number": number,
        "title": title[:80] + "..." if len(title) > 80 else title,
        "link": link,
        "comment_unresolved": comment_unresolved,
        "comment_detail": comment_detail,
        "missing_labels": missing_labels,
        "labels_detail": labels_detail,
        "over_additions": over_additions,
        "additions_detail": additions_detail,
        "no_test": no_test,
        "no_test_detail": no_test_detail,
        "multi_issue": multi_issue,
        "multi_issue_detail": multi_issue_detail,
        "lack_review": lack_review,
        "lack_review_detail": lack_review_detail,
        "title_body_unclear": title_body_unclear,
        "title_body_unclear_detail": title_body_unclear_detail,
    }
    return row, None


def problem_summary(row):
    """根据维度布尔值生成「问题汇总」字符串。"""
    parts = []
    for key in DIMENSION_BOOL_KEYS:
        if row.get(key):
            parts.append(DIMENSION_NAMES_CN[DIMENSION_BOOL_KEYS.index(key)])
    return "; ".join(parts) if parts else "无"


def to_markdown_table(rows):
    """生成 Markdown 表格字符串。PR 列含链接 [#num](url)，无单独链接列；维度列为详情文案。"""
    if not rows:
        return "无数据。"
    cn_headers = HEADERS
    col_keys = ["repo", "pr_display", "title"] + DIMENSION_KEYS + ["summary"]
    lines = []
    lines.append("| " + " | ".join(cn_headers) + " |")
    lines.append("| " + " | ".join(["---"] * len(cn_headers)) + " |")
    for r in rows:
        r["summary"] = problem_summary(r)
        pr_display = "[#%s](%s)" % (r.get("number"), r.get("link", ""))
        r["pr_display"] = pr_display
        cells = []
        for k in col_keys:
            v = r.get(k, "")
            cells.append(str(v).replace("|", "\\|").replace("\n", " "))
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def to_csv_rows(rows):
    """生成 CSV 行（含表头）；PR 列为 #num，链接列为 URL；维度列为详情文案。"""
    col_keys = ["repo", "number", "title", "link"] + DIMENSION_KEYS + ["summary"]
    csv_headers = ["仓库", "PR", "标题", "链接"] + DIMENSION_NAMES_CN + ["问题汇总"]
    out = [csv_headers]
    for r in rows:
        r["summary"] = problem_summary(r)
        out_row = []
        for k in col_keys:
            v = r.get(k, "")
            if k == "number":
                v = "#%s" % v
            out_row.append(str(v))
        out.append(out_row)
    return out


def main():
    parser = argparse.ArgumentParser(
        description="GitCode 合入 PR 质量抽检：按时间范围拉取已合并 PR，多维度检查，输出表格。",
    )
    parser.add_argument("--repo", action="append", metavar="owner/repo", help="仓库，可多次指定")
    parser.add_argument("--pr", type=int, action="append", metavar="N", help="指定 PR 编号，可多次传入；与时间范围二选一，指定后仅检查这些 PR（需且仅需一个 --repo）")
    parser.add_argument("--branch", default="", help="目标分支；未传时依次尝试 master、develop、main")
    parser.add_argument("--since", metavar="YYYY-MM-DD", help="起始日期（含该日 00:00 上海时间）")
    parser.add_argument("--until", metavar="YYYY-MM-DD", help="结束日期（含该日 24:00 前）")
    parser.add_argument("--days", type=int, default=DEFAULT_DAYS, metavar="N", help="最近 N 天，默认 %s" % DEFAULT_DAYS)
    parser.add_argument("--all", action="store_true", help="不抽样，全部检查")
    parser.add_argument("--output", metavar="path", help="输出文件路径，.md 或 .csv（UTF-8，CSV 带 BOM）")
    parser.add_argument("--config", metavar="path", help="配置文件路径，默认技能根目录 config.json")
    args = parser.parse_args()

    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
        except Exception:
            pass

    repos = args.repo or []
    if not repos:
        sys.stderr.write("错误: 请至少指定一个 --repo owner/repo\n")
        sys.exit(1)
    repo_list = []
    for r in repos:
        r = (r or "").strip()
        if "/" not in r:
            sys.stderr.write("错误: --repo 必须为 owner/repo 格式: %s\n" % r)
            sys.exit(1)
        owner, repo = r.split("/", 1)
        repo_list.append((owner.strip(), repo.strip()))

    pr_numbers = args.pr or []
    if pr_numbers:
        if len(repo_list) != 1:
            sys.stderr.write("错误: 使用 --pr 时需且仅需指定一个 --repo\n")
            sys.exit(1)

    token = get_token()
    if not token:
        sys.stderr.write("错误: 未配置 GITCODE_TOKEN。请到 https://gitcode.com/setting/token-classic 创建并设置环境变量 GITCODE_TOKEN。\n")
        sys.exit(1)

    config = load_config(args.config)
    branch_spec = (args.branch or "").strip()

    all_rows = []

    if pr_numbers:
        owner, repo = repo_list[0]
        for num in pr_numbers:
            pr_info, err = _get_pull_detail_any_path(token, owner, repo, num)
            if err or not pr_info:
                sys.stderr.write("警告: 无法获取 PR #%s: %s\n" % (num, err or "无详情"))
                continue
            pr_info["number"] = num
            pr_info.setdefault("html_url", "https://gitcode.com/%s/%s/merge_requests/%s" % (owner, repo, num))
            row, err = audit_one_pr(token, owner, repo, pr_info, config)
            if err:
                sys.stderr.write("警告: PR #%s 检查失败: %s\n" % (num, err))
                continue
            if row:
                all_rows.append(row)
    else:
        since_utc = None
        until_utc = None
        if args.since or args.until:
            if args.since:
                since_utc = parse_date_utc(args.since, end_of_day=False)
                if not since_utc:
                    sys.stderr.write("错误: --since 格式应为 YYYY-MM-DD\n")
                    sys.exit(1)
            if args.until:
                until_utc = parse_date_utc(args.until, end_of_day=True)
                if not until_utc:
                    sys.stderr.write("错误: --until 格式应为 YYYY-MM-DD\n")
                    sys.exit(1)
            if since_utc and until_utc and since_utc > until_utc:
                sys.stderr.write("错误: --since 不能晚于 --until\n")
                sys.exit(1)
        else:
            until_utc = datetime.now(timezone.utc)
            since_utc = until_utc - timedelta(days=max(1, args.days))

        for owner, repo in repo_list:
            branch, err = resolve_branch(token, owner, repo, branch_spec or None)
            if err:
                sys.stderr.write("错误: %s\n" % err)
                sys.exit(1)
            merged, err = list_merged_pulls(token, owner, repo, branch, since_utc, until_utc)
            if err:
                sys.stderr.write("错误: %s/%s 拉取 PR 列表失败: %s\n" % (owner, repo, err))
                sys.exit(1)
            if not merged:
                continue
            if args.all:
                sample = merged
            else:
                n = min(len(merged), random.randint(SAMPLE_MIN, SAMPLE_MAX)) if len(merged) >= SAMPLE_MIN else len(merged)
                sample = random.sample(merged, n) if n else []
            for pr_info in sample:
                row, err = audit_one_pr(token, owner, repo, pr_info, config)
                if err:
                    sys.stderr.write("警告: PR #%s 检查失败: %s\n" % (pr_info.get("number"), err))
                    continue
                if row:
                    all_rows.append(row)

    table_md = to_markdown_table(all_rows)
    try:
        sys.stdout.buffer.write(table_md.encode("utf-8"))
        sys.stdout.buffer.write(b"\n")
        sys.stdout.buffer.flush()
    except (AttributeError, OSError):
        print(table_md)

    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        suffix = out_path.suffix.lower()
        try:
            if suffix == ".csv":
                csv_rows = to_csv_rows(all_rows)
                with open(out_path, "w", encoding="utf-8-sig", newline="") as f:
                    w = csv.writer(f)
                    for r in csv_rows:
                        w.writerow(r)
            else:
                with open(out_path, "w", encoding="utf-8") as f:
                    f.write(table_md)
                    f.write("\n")
        except OSError as e:
            sys.stderr.write("错误: 写入文件失败: %s\n" % e)
            sys.exit(1)


if __name__ == "__main__":
    main()
