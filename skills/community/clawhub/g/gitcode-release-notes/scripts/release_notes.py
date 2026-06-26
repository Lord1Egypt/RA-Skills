#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitCode 版本发布公告：按 tag 区间或 --since-date 拉取提交，按 feat/fix/docs/其他 分组，输出 Markdown 到 stdout。
仅使用 Python 3.7+ 标准库；需 GITCODE_TOKEN。
API: https://docs.gitcode.com/docs/apis/get-api-v-5-repos-owner-repo-commits

Usage:
  python release_notes.py --repo owner/repo [--branch BRANCH] [--from TAG] [--to TAG] [--since-date YYYY-MM-DD]
"""

import json
import sys
import re
import argparse
import os
import subprocess
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path

from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode

GITCODE_API_BASE = "https://api.gitcode.com/api/v5"
SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent

# 默认时区（--since-date 的 00:00 使用）
DEFAULT_TIMEZONE = "Asia/Shanghai"
SHANGHAI_UTC_OFFSET_HOURS = 8

# 请求间隔与重试（避免 API 限流与失败）
REQUEST_SLEEP_SEC = 0.2
REQUEST_TIMEOUT_SEC = 30
RETRY_TIMES = 2
RETRY_INTERVAL_SEC = 2

# 每类（新特性/修复/文档/其他）最多展示条数，只保留前 N 条（按提交顺序，通常为较重要或最近）
MAX_PER_CATEGORY_DEFAULT = 10


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
    """构造详细错误信息。"""
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
    """
    请求 GitCode API；请求后 sleep；失败重试；429 时等待 Retry-After。
    返回 (data, error_str)。data 为 list/dict，error 为 None 或详细错误字符串。
    """
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
                wait = 60
                if e.headers.get("Retry-After"):
                    try:
                        wait = int(e.headers["Retry-After"])
                    except ValueError:
                        pass
                time.sleep(wait)
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
    """GET /repos/:owner/:repo/branches，返回 (branches_list, error)。"""
    return api_get(token, "repos/%s/%s/branches" % (owner, repo), {"per_page": 100})


def resolve_branch(token, owner, repo):
    """
    未指定分支时依次尝试 master → develop → main；都不存在则报错。
    返回 (branch_name, error)。
    """
    data, err = get_branches(token, owner, repo)
    if err:
        return None, "获取分支列表失败: %s" % err
    names = {b.get("name") for b in (data or []) if b.get("name")}
    for candidate in ("master", "develop", "main"):
        if candidate in names:
            return candidate, None
    return None, "仓库中未找到分支 master、develop 或 main，请使用 --branch 指定分支。当前分支列表: %s" % (", ".join(sorted(names)[:20]) or "无")


def get_tags(token, owner, repo):
    """GET /repos/:owner/:repo/tags，返回 (tags_list, error)。"""
    return api_get(token, "repos/%s/%s/tags" % (owner, repo), {"per_page": 100})


def tag_to_sha(tags_list, tag_name):
    """从 tags 列表中按 name 查找，返回 commit sha。"""
    tag_name = (tag_name or "").strip()
    for t in tags_list or []:
        if (t.get("name") or "").strip() == tag_name:
            c = t.get("commit")
            if isinstance(c, dict):
                return (c.get("id") or c.get("sha") or "").strip()
            if isinstance(c, str):
                return c.strip()
    return None


def get_commits_since_date(token, owner, repo, branch, since_date_utc_start_iso):
    """拉取 branch 上 since 之后的提交（API since 参数）；不支持 since 时按日期过滤。"""
    all_commits = []
    page = 1
    per_page = 100
    while True:
        params = {"sha": branch, "per_page": per_page, "page": page}
        if since_date_utc_start_iso:
            params["since"] = since_date_utc_start_iso
        data, err = api_get(token, "repos/%s/%s/commits" % (owner, repo), params)
        if err:
            return all_commits, err
        lst = data if isinstance(data, list) else []
        if not lst:
            break
        all_commits.extend(lst)
        if len(lst) < per_page:
            break
        page += 1
    return all_commits, None


def get_commits_from_to(token, owner, repo, to_sha_or_branch, stop_at_sha=None):
    """
    拉取从 to_sha_or_branch（ref）开始的提交，直到遇到 stop_at_sha（from_sha）或页数上限。
    即：commits 顺序为从新到旧，收集到 stop_at_sha 之前（不包含 stop_at_sha）。
    """
    all_commits = []
    page = 1
    per_page = 100
    while True:
        data, err = api_get(
            token,
            "repos/%s/%s/commits" % (owner, repo),
            {"sha": to_sha_or_branch, "per_page": per_page, "page": page},
        )
        if err:
            return all_commits, err
        lst = data if isinstance(data, list) else []
        if not lst:
            break
        for c in lst:
            sha = (c.get("sha") or c.get("id") or "").strip()
            if stop_at_sha and sha == stop_at_sha:
                return all_commits, None
            all_commits.append(c)
        if len(lst) < per_page:
            break
        page += 1
    return all_commits, None


# 仅当「整条短描述」恰好等于下列词之一时才过滤（不含其它文字）。例如 "add structured log" 不会过滤。
_NOISE_WORDS = frozenset(["log", "label", "wip", "temp", "merge", "n/a", "-"])
# 纯类型词：仅写 fix/feat/docs 等、无实质描述时视为无信息量，不单独展示（可合并为「多项修复」等）
_TYPE_ONLY_WORDS = frozenset(["feat", "fix", "docs", "feature", "bugfix", "doc"])
# merge 提交的正则：!2912 merge xxx into master 等
_MERGE_PATTERN = re.compile(r"^!?\d*\s*merge\s+.+\s+into\s+\w+", re.I)


def _is_merge_commit(first_line):
    """是否为合并提交（merge xxx into master）。"""
    return bool(first_line and _MERGE_PATTERN.match(first_line.strip()))


def _strip_noise_prefix(desc):
    """
    去掉展示用描述中的噪音前缀，得到给人看的说明。
    - 去掉开头的 !数字、[模块名]、<doc>[xxx] 等
    - 去掉末尾的 merge xxx into master
    """
    if not desc or not isinstance(desc, str):
        return ""
    s = desc.strip()
    # 去掉 !1234 或 !1234 
    s = re.sub(r"^!\d+\s*", "", s)
    # 去掉 [xxx][yyy] 或 [xxx] 或 <doc>[xxx]
    s = re.sub(r"^(\[([^\]]+)\]\s*)+", "", s)
    s = re.sub(r"^<[^>]+>(\[[^\]]+\]\s*)*", "", s)
    s = s.strip()
    # 整行就是 merge xxx into master 的，返回空（后续当 merge 处理）
    if _MERGE_PATTERN.match(s):
        return ""
    # 去掉末尾的 merge xxx into master（有时描述后面带这句）
    s = re.sub(r"\s*merge\s+.+\s+into\s+\w+\s*$", "", s, flags=re.I).strip()
    return s[:200] if len(s) > 200 else s


def _should_skip_description(desc):
    """描述过短或无信息量则跳过。仅当整条描述恰好为噪音词（如单写 log/label）或纯类型词（fix/feat/docs）时才过滤。"""
    if not desc or not isinstance(desc, str):
        return True
    s = desc.strip()
    if len(s) < 3:
        return True
    if s.lower() in _NOISE_WORDS:  # 整条等于 log/label/… 才滤，含 "add log" 等不滤
        return True
    if s.lower() in _TYPE_ONLY_WORDS:  # 仅写 fix/feat/docs 无实质描述，不单独展示
        return True
    return False


def _first_line_from_body(msg):
    """从 commit message 正文（第二行起）取第一条非空、且非纯类型词的行，用作短描述兜底。"""
    if not msg or not isinstance(msg, str):
        return ""
    for line in msg.split("\n")[1:]:
        s = line.strip()
        if len(s) < 4:
            continue
        if s.lower() in _TYPE_ONLY_WORDS:
            continue
        return s[:200] if len(s) > 200 else s
    return ""


def parse_commit_message(msg):
    """
    解析 commit message 第一行，返回 (type_key, short_desc, raw_first)。
    type_key: 'feat'|'fix'|'docs'|'other'
    短描述：去掉 type(scope): 或 type: 后的部分，无则整行；若仍无实质内容则尝试用正文首行兜底。
    """
    first = (msg or "").split("\n")[0].strip()
    if not first:
        return "other", "", ""
    first_lower = first.lower()
    if first_lower.startswith("feat"):
        t = "feat"
    elif first_lower.startswith("fix"):
        t = "fix"
    elif first_lower.startswith("docs"):
        t = "docs"
    else:
        t = "other"
    colon = first.find(":")
    paren = first.find(")")
    if colon >= 0 and (paren < 0 or colon < paren):
        desc = first[colon + 1 :].strip()
    elif paren >= 0:
        rest = first[paren + 1 :].lstrip()
        if rest.startswith(":"):
            rest = rest[1:].strip()
        desc = rest
    else:
        if t != "other":
            desc = first[4:].lstrip()
            if desc.startswith("("):
                idx = desc.find(")")
                if idx >= 0:
                    desc = desc[idx + 1 :].lstrip().lstrip(":")
            desc = desc.strip()
        else:
            desc = first
    short = (desc[:200] if len(desc) > 200 else desc) if desc else ""
    if not short and msg:
        short = _first_line_from_body(msg)
    return t, short, first


def build_markdown(owner, repo, commits, title_line=None, max_per_category=MAX_PER_CATEGORY_DEFAULT):
    """
    将 commits 按四组输出 Markdown；过滤无信息量项与纯 merge，规范化描述，合并展示。
    每类最多展示 max_per_category 条；other 中多条 merge 合并为一条说明。
    """
    base_url = "https://gitcode.com/%s/%s/commit/" % (owner, repo)
    groups = {"feat": [], "fix": [], "docs": [], "other": []}
    merge_count_other = 0
    type_only_count = {"feat": 0, "fix": 0, "docs": 0}  # 仅类型词、无实质描述的提交数，合并为一条说明

    for c in commits:
        sha = (c.get("sha") or c.get("id") or "").strip()
        commit_obj = c.get("commit") or c
        msg = commit_obj.get("message") if isinstance(commit_obj, dict) else (c.get("message") or "")
        if not msg and isinstance(commit_obj, dict):
            msg = (commit_obj.get("message") or "")
        t, raw_desc, raw_first = parse_commit_message(msg)
        normalized = _strip_noise_prefix(raw_desc or raw_first)

        # 纯 merge 提交（other 类）：不逐条展示，只计数，最后合并为一条
        if _is_merge_commit(raw_first) or (t == "other" and not normalized and raw_first.strip()):
            if t == "other":
                merge_count_other += 1
            continue

        # 仅类型词（fix/feat/docs）无实质描述：不单独展示，计数后合并为「多项修复（共 N 条）」等
        if normalized.strip().lower() in _TYPE_ONLY_WORDS and t in type_only_count:
            type_only_count[t] += 1
            continue

        if _should_skip_description(normalized):
            continue

        link = "([%s](%s%s))" % (sha[:7] if len(sha) >= 7 else sha, base_url, sha)
        line = "- %s %s" % (normalized, link)
        groups[t].append(line)

    n = max(1, min(50, int(max_per_category)))
    lines = []

    if title_line:
        lines.append(title_line)
        lines.append("")

    _type_only_labels = {"feat": "新特性与改进", "fix": "修复", "docs": "文档更新"}

    if groups["feat"] or type_only_count["feat"] > 0:
        lines.append("### 🚀 新特性")
        if type_only_count["feat"] > 0:
            lines.append("- 多项%s（共 %d 条）" % (_type_only_labels["feat"], type_only_count["feat"]))
        lines.extend(groups["feat"][:n])
        lines.append("")

    if groups["fix"] or type_only_count["fix"] > 0:
        lines.append("### 🐛 修复")
        if type_only_count["fix"] > 0:
            lines.append("- 多项%s（共 %d 条）" % (_type_only_labels["fix"], type_only_count["fix"]))
        lines.extend(groups["fix"][:n])
        lines.append("")

    if groups["docs"] or type_only_count["docs"] > 0:
        lines.append("### 📚 文档")
        if type_only_count["docs"] > 0:
            lines.append("- 多项%s（共 %d 条）" % (_type_only_labels["docs"], type_only_count["docs"]))
        lines.extend(groups["docs"][:n])
        lines.append("")

    if groups["other"] or merge_count_other > 0:
        lines.append("### 🔧 其他更改")
        if merge_count_other > 0:
            lines.append("- 合并多项分支与依赖更新（共 %d 条）" % merge_count_other)
        lines.extend(groups["other"][:n])
        lines.append("")

    return "\n".join(lines).rstrip()


def since_date_to_utc_iso(date_str, tz_offset_hours=SHANGHAI_UTC_OFFSET_HOURS):
    """将 YYYY-MM-DD 转为该日 00:00 本地时间对应的 UTC ISO 字符串。"""
    try:
        local_dt = datetime.strptime(date_str.strip()[:10], "%Y-%m-%d")
        utc_dt = local_dt - timedelta(hours=tz_offset_hours)
        return utc_dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        return None


def _commit_date(c):
    """从 API 返回的 commit 对象中提取日期 YYYY-MM-DD。"""
    co = c.get("commit") or c
    if not isinstance(co, dict):
        return None
    ad = co.get("author") or co.get("committer") or {}
    if not isinstance(ad, dict):
        return None
    dt = ad.get("date")
    return dt[:10] if isinstance(dt, str) and len(dt) >= 10 else None


def build_json_output(owner, repo, commits, title_line, from_tag, to_tag, since_date, branch):
    """
    仅做获取与简单过滤后输出 JSON，供 Agent 总结与生成最终 release note。
    简单过滤：排除空 message、排除纯 merge 提交；其余全部保留，含 type 与 first_line/body。
    """
    base_url = "https://gitcode.com/%s/%s/commit/" % (owner, repo)
    repo_spec = "%s/%s" % (owner, repo)
    merge_count = 0
    out_commits = []

    for c in commits:
        sha = (c.get("sha") or c.get("id") or "").strip()
        commit_obj = c.get("commit") or c
        msg = commit_obj.get("message") if isinstance(commit_obj, dict) else (c.get("message") or "")
        if not msg and isinstance(commit_obj, dict):
            msg = (commit_obj.get("message") or "")

        if not (msg or "").strip():
            continue

        first_line = (msg or "").split("\n")[0].strip()
        if _is_merge_commit(first_line):
            merge_count += 1
            continue

        t, _short, _raw = parse_commit_message(msg)
        body_lines = (msg or "").split("\n")[1:]
        body = "\n".join(body_lines).strip() if body_lines else ""

        out_commits.append({
            "sha": sha,
            "short_sha": sha[:7] if len(sha) >= 7 else sha,
            "url": base_url + sha,
            "message": msg.strip(),
            "first_line": first_line,
            "body": body,
            "type": t,
            "date": _commit_date(c),
        })

    return {
        "repo": repo_spec,
        "branch": branch,
        "from_tag": from_tag or None,
        "to_tag": to_tag or None,
        "since_date": since_date or None,
        "title_line": title_line,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "commits": out_commits,
        "stats": {"merge_count": merge_count},
    }


def main():
    parser = argparse.ArgumentParser(
        description="按 tag 或日期拉取提交，生成版本发布公告 Markdown（默认中文，每类最多展示若干条）",
    )
    parser.add_argument("--repo", required=True, metavar="owner/repo", help="仓库，格式 owner/repo（必填）")
    parser.add_argument("--branch", default="", help="分支；未传时依次尝试 master、develop、main")
    parser.add_argument("--since-date", metavar="YYYY-MM-DD", help="从该日 00:00（上海时间）至今的提交")
    parser.add_argument("--from", dest="from_tag", metavar="TAG", help="起始 tag（到当前或 --to）")
    parser.add_argument("--to", metavar="TAG", help="结束 tag，与 --from 一起表示区间")
    parser.add_argument("--max-per-category", type=int, default=MAX_PER_CATEGORY_DEFAULT, metavar="N",
                        help="新特性/修复/文档/其他每类最多展示条数，默认 %s（5–10 条即可）" % MAX_PER_CATEGORY_DEFAULT)
    parser.add_argument("--json", action="store_true",
                        help="输出 JSON（仅拉取与简单过滤），由 Agent 负责总结并生成最终 release note")
    args = parser.parse_args()

    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
        except Exception:
            pass

    repo_spec = (args.repo or "").strip()
    if "/" not in repo_spec:
        sys.stderr.write("错误: --repo 必须为 owner/repo 格式\n")
        sys.exit(1)
    owner, repo = repo_spec.split("/", 1)
    owner = owner.strip()
    repo = repo.strip()
    if not owner or not repo:
        sys.stderr.write("错误: --repo 不能为空\n")
        sys.exit(1)

    token = get_token()
    if not token:
        sys.stderr.write("错误: 未配置 GITCODE_TOKEN。请到 https://gitcode.com/setting/token-classic 创建个人访问令牌并设置环境变量 GITCODE_TOKEN（当前进程或 Windows 用户/系统变量）。\n")
        sys.exit(1)

    branch = (args.branch or "").strip()
    if not branch:
        branch, err = resolve_branch(token, owner, repo)
        if err:
            sys.stderr.write("错误: %s\n" % err)
            sys.exit(1)

    from_tag = (getattr(args, "from_tag") or "").strip()
    to_tag = (args.to or "").strip()
    since_date = (args.since_date or "").strip()

    commits = []
    title_line = None

    if args.since_date:
        since_iso = since_date_to_utc_iso(args.since_date)
        if not since_iso:
            sys.stderr.write("错误: --since-date 格式应为 YYYY-MM-DD\n")
            sys.exit(1)
        commits, err = get_commits_since_date(token, owner, repo, branch, since_iso)
        if err:
            sys.stderr.write("错误: 拉取提交失败: %s\n" % err)
            sys.exit(1)
    else:
        from_tag = (getattr(args, "from_tag") or "").strip()
        to_tag = (args.to or "").strip()
        if not from_tag and not to_tag:
            sys.stderr.write("错误: 请指定 --since-date 或 --from [--to] 以确定提交区间\n")
            sys.exit(1)
        tags_data, err = get_tags(token, owner, repo)
        if err:
            sys.stderr.write("错误: 获取标签列表失败: %s\n" % err)
            sys.exit(1)
        if to_tag:
            to_sha = tag_to_sha(tags_data, to_tag)
            if not to_sha:
                sys.stderr.write("错误: 未找到标签: %s\n" % to_tag)
                sys.exit(1)
            from_sha = tag_to_sha(tags_data, from_tag) if from_tag else None
            commits, err = get_commits_from_to(token, owner, repo, to_sha, from_sha)
            if err:
                sys.stderr.write("错误: 拉取提交失败: %s\n" % err)
                sys.exit(1)
            # 有结束版本：标题取 to_tag + 日期（最后一笔提交的日期或当前）
            try:
                last_date = None
                for c in commits:
                    co = c.get("commit") or c
                    if isinstance(co, dict):
                        ad = co.get("author") or co.get("committer") or {}
                        dt = ad.get("date") if isinstance(ad, dict) else None
                        if dt:
                            last_date = dt[:10]
                            break
                date_str = last_date or datetime.now(timezone.utc).strftime("%Y-%m-%d")
            except Exception:
                date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            title_line = "## %s (%s)" % (to_tag, date_str)
        else:
            from_sha = tag_to_sha(tags_data, from_tag)
            if not from_sha:
                sys.stderr.write("错误: 未找到标签: %s\n" % from_tag)
                sys.exit(1)
            commits, err = get_commits_from_to(token, owner, repo, branch, from_sha)
            if err:
                sys.stderr.write("错误: 拉取提交失败: %s\n" % err)
                sys.exit(1)
            title_line = None

    if getattr(args, "json", False):
        payload = build_json_output(owner, repo, commits, title_line, from_tag, to_tag, since_date, branch)
        try:
            sys.stdout.buffer.write(json.dumps(payload, ensure_ascii=False).encode("utf-8"))
            sys.stdout.buffer.flush()
        except (AttributeError, OSError):
            print(json.dumps(payload, ensure_ascii=False))
        return

    out = build_markdown(owner, repo, commits, title_line, getattr(args, "max_per_category", MAX_PER_CATEGORY_DEFAULT))
    try:
        sys.stdout.buffer.write(out.encode("utf-8"))
        sys.stdout.buffer.write(b"\n")
        sys.stdout.buffer.flush()
    except (AttributeError, OSError):
        print(out)


if __name__ == "__main__":
    main()
