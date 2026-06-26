#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
jisu-find-skill：ClawHub 技能发现与安装（search / inspect / install / stats / verify / installed）。
search / list 依赖 clawhub CLI 解析全站结果。无需 JISU_API_KEY。
默认终端人类可读；加 --json 输出结构化 JSON。
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# clawhub search 输出中的 https://clawhub.ai/org/skill 形式
CLAWHUB_ANY_RE = re.compile(
    r"https://clawhub\.ai/([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)",
)
# clawhub search 新版文本输出常见行首 slug（不含 URL），如：weather  Weather  (3.877)
CLAWHUB_SEARCH_SLUG_RE = re.compile(
    r"^\s*([A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)?)\s{2,}.+?\(\d+(?:\.\d+)?\)\s*$"
)
# 宽松：行首 slug，兼容无分数、无双空格等变体（与 strict 分支配合；黑名单见 _extract_clawhub_urls_from_text）
CLAWHUB_SEARCH_SLUG_LOOSE_RE = re.compile(
    r"^\s*([A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)?)\b"
)
# 连续汉字（用于中文查询：无空格时拆出二字/三字片段，否则整句无法命中「全国天气预报」等子串）
_CJK_RE = re.compile(r"[\u4e00-\u9fff\u3400-\u4dbf]+")
STATS_API_TMPL = "https://clawhub.ai/api/v1/skills/{slug}"
_KEYWORD_CAP = 100
_DETAIL_FETCH_TIMEOUT = 15
_DESCRIPTION_LINE_MAX = 800


def _json_out(obj: Any) -> None:
    print(json.dumps(obj, ensure_ascii=False, indent=2))


def _human_result_title(text: str) -> str:
    """每条结果标题用 Markdown 粗体 **…** 包裹，在支持 Markdown 的客户端里显示为粗体。"""
    t = (text or "").strip()
    if not t:
        return t
    if (os.environ.get("NO_COLOR") or "").strip():
        return t
    return "**%s**" % t


def _print_search_human(payload: Dict[str, Any]) -> None:
    """终端可读：不含完整 clawhub 原始 stdout，仅摘要与每条展示行。"""
    q = payload.get("query") or ""
    tried = payload.get("clawhub_queries_tried") or []
    sort_by = payload.get("sort_by") or ""
    cnt = int(payload.get("count") or 0)
    merged = payload.get("results") or []
    note = (payload.get("merge_note") or "").strip()
    avail = payload.get("clawhub_cli_available")

    print("查询: %s" % q)
    if tried:
        print("尝试关键词/变体: %s" % " → ".join(str(x) for x in tried))
    if sort_by:
        print("排序: %s" % sort_by)
    print("条数: %d（clawhub CLI: %s）" % (cnt, "可用" if avail else "不可用"))
    if note:
        print("说明: %s" % note)
    print()
    if not merged:
        print("（无结果）")
        return
    for r in merged:
        title = (r.get("name") or r.get("clawhub_path") or "—").strip()
        print(_human_result_title(title))
        dl = (r.get("detail_line") or "").strip()
        if dl:
            print("  %s" % dl)
        ds = (r.get("description_line") or "").strip()
        if ds:
            print("  %s" % ds)
        hint = (r.get("install_hint") or "").strip()
        if hint:
            print("  安装: %s" % hint)
        if r.get("installed_locally"):
            print("  本地: 已安装")
        print()


def _print_list_human(payload: Dict[str, Any]) -> None:
    total = int(payload.get("total") or 0)
    items = payload.get("results") or []
    ok = payload.get("ok")
    print("list 查询: %s" % (payload.get("list_query") or "jisuapi"))
    print("状态: %s | 条数: %d" % ("成功" if ok else "失败", total))
    print()
    if not items:
        print("（无结果）")
        return
    for r in items:
        title = (r.get("name") or r.get("clawhub_path") or "—").strip()
        print(_human_result_title(title))
        hint = (r.get("install_hint") or "").strip()
        if hint:
            print("  安装: %s" % hint)
        print()


def _print_inspect_human(p: Dict[str, Any]) -> None:
    cmd = p.get("command")
    name = cmd[-1] if isinstance(cmd, list) and cmd else "?"
    ok = p.get("ok")
    print("inspect: %s" % name)
    print("状态: %s | 退出码: %s" % ("成功" if ok else "失败", p.get("exit_code")))
    out = (p.get("stdout") or "").rstrip()
    err = (p.get("stderr") or "").rstrip()
    if out:
        print("\n--- clawhub 输出 ---\n%s" % out)
    if err:
        print("\n--- clawhub 错误 ---\n%s" % err)


def _print_install_human(p: Dict[str, Any]) -> None:
    if p.get("dry_run"):
        print(p.get("message") or "未执行安装（dry run）。")
        print("将执行: %s" % " ".join(p.get("command") or []))
        print("装完可执行: %s" % (p.get("verify_after") or ""))
        return
    ok = p.get("ok")
    cmd = p.get("command")
    print("install: %s" % (cmd[-1] if isinstance(cmd, list) and cmd else "?"))
    print("状态: %s | 退出码: %s" % ("成功" if ok else "失败", p.get("exit_code")))
    out = (p.get("stdout") or "").rstrip()
    err = (p.get("stderr") or "").rstrip()
    if out:
        print("\n--- clawhub 输出 ---\n%s" % out)
    if err:
        print("\n--- clawhub 错误 ---\n%s" % err)
    if p.get("verify_hint"):
        print("\n建议: %s" % p["verify_hint"])


def _print_stats_human(p: Dict[str, Any]) -> None:
    print("URL: %s" % p.get("url"))
    if p.get("note"):
        print("说明: %s" % p["note"])
    data = p.get("data")
    print()
    if isinstance(data, dict):
        for k in sorted(data.keys()):
            val = data[k]
            if isinstance(val, (dict, list)):
                print("%s: （嵌套数据，需完整内容请加 --json）" % k)
            else:
                print("%s: %s" % (k, val))
    else:
        print(str(data)[:4000])


def _print_stats_error_human(p: Dict[str, Any]) -> None:
    print("stats 请求失败")
    for k, v in p.items():
        if k == "tried_urls":
            print("已尝试 URL: %s" % " | ".join(str(x) for x in (v or [])))
        elif k == "body" and v:
            print("响应正文(截断): %s" % str(v)[:800])
        elif k not in ("body",):
            print("%s: %s" % (k, v))


def _print_verify_human(p: Dict[str, Any]) -> None:
    print("技能名: %s" % p.get("skill_name"))
    print("工作区: %s" % p.get("workspace_skills_dir"))
    if p.get("skill_md_found"):
        print("SKILL.md: 已找到 → %s" % p.get("skill_md_path"))
    else:
        print("SKILL.md: 未找到")
    if p.get("hint"):
        print("提示: %s" % p["hint"])


def _print_installed_human(p: Dict[str, Any]) -> None:
    print("技能根目录: %s" % p.get("workspace_skills_dir"))
    names = p.get("installed_with_skill_md") or []
    print("本地已安装（目录内含 SKILL.md）: 共 %d 个" % len(names))
    for n in names:
        print("  · %s" % n)
    code = p.get("clawhub_list_exit_code")
    if code is not None and code >= 0:
        print("\nclawhub list 退出码: %s" % code)
        err = (p.get("clawhub_list_stderr") or "").strip()
        out = (p.get("clawhub_list_stdout") or "").strip()
        if out:
            print("--- clawhub list 输出 ---\n%s" % out[:4000])
        if err:
            print("--- clawhub list 错误 ---\n%s" % err[:2000])


def _workspace_skills_dir() -> Path:
    env = os.environ.get("OPENCLAW_SKILLS_DIR", "").strip()
    if env:
        return Path(env)
    return Path.home() / ".openclaw" / "workspace" / "skills"


def _installed_skill_dir_names(root: Path) -> set[str]:
    names: set[str] = set()
    if not root.is_dir():
        return names
    for p in root.iterdir():
        if p.is_dir() and (p / "SKILL.md").is_file():
            names.add(p.name)
    return names


def _skill_installed_locally(installed: set[str], r: Dict[str, Any]) -> bool:
    slug = (r.get("slug") or "").strip()
    path = (r.get("clawhub_path") or "").strip()
    if slug and slug in installed:
        return True
    if path:
        if path in installed:
            return True
        if "/" in path:
            leaf = path.split("/")[-1]
            if leaf in installed:
                return True
    return False


def _which_clawhub() -> Optional[str]:
    return shutil.which("clawhub")


def _run_clawhub(args: List[str], timeout: int = 90) -> Tuple[int, str, str]:
    exe = _which_clawhub()
    if not exe:
        return -1, "", "clawhub CLI not found in PATH"
    try:
        p = subprocess.run(
            [exe] + args,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            shell=False,
        )
        return p.returncode, p.stdout or "", p.stderr or ""
    except subprocess.TimeoutExpired:
        return -2, "", "clawhub command timeout"
    except Exception as e:
        return -3, "", str(e)


def _keywords(q: str) -> List[str]:
    """从查询中提取关键词。中文无分词时按空白/标点切分；并对连续汉字生成 2/3 字片段，用于与 slug 路径做简单匹配打分。"""
    q0 = (q or "").strip()
    if not q0:
        return []
    seen: set[str] = set()
    out: List[str] = []

    def add(tok: str) -> None:
        if len(out) >= _KEYWORD_CAP:
            return
        t = tok.strip()
        if not t:
            return
        key = t.lower() if t.isascii() else t
        if key in seen:
            return
        seen.add(key)
        out.append(key)

    for p in re.split(r"[\s，,、；;]+", q0):
        if p:
            add(p.lower() if p.isascii() else p)

    for m in _CJK_RE.finditer(q0):
        run = m.group(0)
        if len(run) >= 2:
            add(run)
            for i in range(len(run) - 1):
                add(run[i : i + 2])
        if len(run) >= 3:
            for i in range(len(run) - 2):
                add(run[i : i + 3])

    return out


def _dedupe_key(url: str) -> str:
    return url.rstrip("/").lower()


def _extract_clawhub_urls_from_text(text: str) -> List[str]:
    seen: set[str] = set()
    out: List[str] = []
    for m in CLAWHUB_ANY_RE.finditer(text):
        u = "https://clawhub.ai/%s" % m.group(1)
        k = _dedupe_key(u)
        if k not in seen:
            seen.add(k)
            out.append(u)
    # 兼容 clawhub search 不再输出 URL、仅输出 slug 的情况
    for line in (text or "").splitlines():
        s = line.strip()
        if not s or s.startswith("- "):
            continue
        mm = CLAWHUB_SEARCH_SLUG_RE.match(s)
        if not mm:
            continue
        u = "https://clawhub.ai/%s" % mm.group(1)
        k = _dedupe_key(u)
        if k not in seen:
            seen.add(k)
            out.append(u)
    # 二次兜底：更宽松地解析首列 slug（例如：slug<TAB>Title 或 slug Title）
    blacklist = {"searching", "found", "skills", "results", "result", "score"}
    for line in (text or "").splitlines():
        s = line.strip()
        if not s or s.startswith("- "):
            continue
        lm = CLAWHUB_SEARCH_SLUG_LOOSE_RE.match(s)
        if not lm:
            continue
        slug = lm.group(1).strip()
        if slug.lower() in blacklist:
            continue
        # 过短且全字母的普通词通常不是 skill slug
        if len(slug) <= 2 and slug.isalpha():
            continue
        u = "https://clawhub.ai/%s" % slug
        k = _dedupe_key(u)
        if k not in seen:
            seen.add(k)
            out.append(u)
    return out


def _clawhub_query_variants(query: str, kws: List[str]) -> List[str]:
    """为 clawhub CLI 生成查询变体。优先原词；中文需求补充少量高频英文别名以兼容英文索引。"""
    base = (query or "").strip()
    seen: set[str] = set()
    out: List[str] = []

    def add(q: str) -> None:
        q = (q or "").strip()
        if not q:
            return
        key = q.lower()
        if key in seen:
            return
        seen.add(key)
        out.append(q)

    add(base)

    alias_map = {
        "天气": ["weather", "forecast"],
        "气温": ["weather", "temperature"],
        "预报": ["forecast", "weather"],
        "股票": ["stock", "stocks"],
        "新闻": ["news"],
        "公众号": ["wechat", "wechatmp"],
        "微信": ["wechat"],
        "飞书": ["feishu"],
        "文档": ["document", "docs"],
    }

    hay = " ".join([base] + kws)
    for zh, aliases in alias_map.items():
        if zh in hay:
            for alias in aliases:
                add(alias)

    return out



def _clawhub_search_cli(query: str, kws: Optional[List[str]] = None) -> Tuple[int, str, str, List[str], List[str]]:
    tried: List[str] = []
    merged_out: List[str] = []
    merged_err: List[str] = []
    urls: List[str] = []
    seen_urls: set[str] = set()
    final_code = -1

    for q in _clawhub_query_variants(query, kws or []):
        tried.append(q)
        code, out, err = _run_clawhub(["search", q])
        final_code = code
        if out:
            merged_out.append(out)
        if err:
            merged_err.append(err)
        blob = (out or "") + "\n" + (err or "")
        for url in _extract_clawhub_urls_from_text(blob):
            dk = _dedupe_key(url)
            if dk in seen_urls:
                continue
            seen_urls.add(dk)
            urls.append(url)
        if urls:
            break

    return final_code, "\n".join(merged_out), "\n".join(merged_err), urls, tried


def _result_from_clawhub_url(url: str, kws: List[str]) -> Dict[str, Any]:
    m = CLAWHUB_ANY_RE.search(url)
    slug_full = m.group(1) if m else url.replace("https://clawhub.ai/", "")
    org, _, rest = slug_full.partition("/")
    is_jisu = org.lower() == "jisuapi"
    hay = (url + " " + slug_full).lower()
    bonus = 0.0
    for kw in kws:
        if kw and kw in hay:
            bonus += 1.0
    return {
        "sort_rank": 0,
        "source": "clawhub_search",
        "match_score": round(bonus, 2),
        "name": slug_full,
        "slug": rest or org,
        "clawhub_path": slug_full,
        "clawhub_url": url,
        "category": "",
        "requires_jisu_api_key": is_jisu,
        "install_hint": "clawhub install %s" % slug_full,
        "verify_hint": "ls %s" % (_workspace_skills_dir() / rest / "SKILL.md")
        if rest
        else "ls %s/<skill-dir>/SKILL.md" % _workspace_skills_dir(),
    }


def _skill_api_candidate_urls(skill_slug: str) -> List[str]:
    candidates: List[str] = []
    q1 = urllib.parse.quote(skill_slug, safe="")
    candidates.append(STATS_API_TMPL.format(slug=q1))
    if "/" in skill_slug:
        last = skill_slug.split("/")[-1].strip()
        if last and last != skill_slug:
            q2 = urllib.parse.quote(last, safe="")
            u2 = STATS_API_TMPL.format(slug=q2)
            if u2 not in candidates:
                candidates.append(u2)
    return candidates


def _fetch_clawhub_skill_detail(skill_slug: str, timeout: int = _DETAIL_FETCH_TIMEOUT) -> Dict[str, Any]:
    """GET ClawHub skill 详情，提取星标、下载量、摘要、作者。与 stats 子命令同源 API。"""
    out: Dict[str, Any] = {
        "ok": False,
        "api_url": None,
        "stars": None,
        "downloads": None,
        "summary": None,
        "display_name": None,
        "owner_handle": None,
        "owner_display_name": None,
        "author": None,
        "error": None,
    }
    for url in _skill_api_candidate_urls(skill_slug):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "jisu-find-skill/1.2"})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                body = resp.read().decode("utf-8", errors="replace")
            data = json.loads(body)
            if not isinstance(data, dict):
                out["error"] = "invalid_response"
                continue
            sk = data.get("skill")
            own = data.get("owner")
            if not isinstance(sk, dict):
                out["error"] = "invalid_response"
                continue
            stats = sk.get("stats") if isinstance(sk.get("stats"), dict) else {}
            out["ok"] = True
            out["api_url"] = url
            out["stars"] = stats.get("stars")
            out["downloads"] = stats.get("downloads")
            out["summary"] = sk.get("summary")
            out["display_name"] = sk.get("displayName")
            if isinstance(own, dict):
                out["owner_handle"] = own.get("handle")
                od = own.get("displayName")
                out["owner_display_name"] = od
                oh = out["owner_handle"]
                if od and oh:
                    out["author"] = "%s (@%s)" % (od, oh)
                elif oh:
                    out["author"] = "@%s" % oh
                elif od:
                    out["author"] = od
            return out
        except urllib.error.HTTPError:
            out["error"] = "http_error"
            continue
        except Exception as e:
            out["error"] = str(e)
            continue
    return out


def _format_search_detail_line(r: Dict[str, Any]) -> str:
    """第一行：星标 | 下载 | 作者（用 | 分隔；描述见 description_line）。"""

    def one(label: str, val: Any) -> str:
        if val is None:
            return "%s: —" % label
        if isinstance(val, (int, float)) and not isinstance(val, bool):
            s = str(int(val)) if float(val) == int(val) else str(val)
            return "%s: %s" % (label, s)
        s = str(val).strip()
        if not s:
            return "%s: —" % label
        return "%s: %s" % (label, s)

    return " | ".join(
        [
            one("星标", r.get("stars")),
            one("下载", r.get("downloads")),
            one("作者", r.get("author")),
        ]
    )


def _format_search_description_line(r: Dict[str, Any]) -> str:
    """第二行：描述（单独一行，过长截断）。"""
    desc = r.get("description")
    if desc is None:
        return "描述: —"
    s = str(desc).strip()
    if not s:
        return "描述: —"
    s = s.replace("\r\n", "\n").replace("\r", "\n")
    if len(s) > _DESCRIPTION_LINE_MAX:
        s = s[: _DESCRIPTION_LINE_MAX - 1] + "…"
    return "描述: %s" % s


def _apply_search_display_lines(r: Dict[str, Any]) -> None:
    r["detail_line"] = _format_search_detail_line(r)
    r["description_line"] = _format_search_description_line(r)


def _apply_ordered_skill_name_prefix(results: List[Dict[str, Any]]) -> None:
    """输出前为每条 `name` 加上「1、」「2、」… 序号；`sort_rank` 为 1 起。`clawhub_path` / `install_hint` 不变。"""
    for i, r in enumerate(results, start=1):
        r["sort_rank"] = i
        base = (r.get("clawhub_path") or r.get("name") or "").strip()
        r["name"] = ("%d、%s" % (i, base)) if base else ("%d、" % i)


def _enrich_search_results_with_api(results: List[Dict[str, Any]], timeout: int) -> None:
    """为每条结果拉取 ClawHub API，写入 detail 及扁平字段 stars/description/author 等。"""
    for r in results:
        slug = (r.get("clawhub_path") or r.get("name") or "").strip()
        if not slug:
            r["detail"] = {"ok": False, "error": "no_slug", "api_url": None}
            r["stars"] = None
            r["downloads"] = None
            r["description"] = None
            r["author"] = None
            r["skill_display_name"] = None
            _apply_search_display_lines(r)
            continue
        d = _fetch_clawhub_skill_detail(slug, timeout=timeout)
        r["detail"] = d
        if d.get("ok"):
            r["stars"] = d.get("stars")
            r["downloads"] = d.get("downloads")
            r["description"] = d.get("summary")
            r["author"] = d.get("author")
            r["skill_display_name"] = d.get("display_name")
        else:
            r["stars"] = None
            r["downloads"] = None
            r["description"] = None
            r["author"] = None
            r["skill_display_name"] = None
        _apply_search_display_lines(r)


def cmd_list(*, as_json: bool = False) -> None:
    """`clawhub search jisuapi` 的封装，用于快速扫一批与极速相关的条目。"""
    if not _which_clawhub():
        err = {
            "ok": False,
            "error": "clawhub_not_found",
            "message": "未在 PATH 中找到 clawhub，无法执行 list。",
        }
        if as_json:
            _json_out(err)
        else:
            print(err["message"], file=sys.stderr)
        return
    kws_j = ["jisuapi"]
    code, out, err, urls, tried = _clawhub_search_cli("jisuapi", kws_j)
    items = [_result_from_clawhub_url(u, kws_j) for u in urls]
    _apply_ordered_skill_name_prefix(items)
    payload = {
        "ok": code == 0,
        "list_query": "jisuapi",
        "clawhub_queries_tried": tried,
        "clawhub_search_exit_code": code,
        "clawhub_search_stdout": out[:8000] if out else "",
        "clawhub_search_stderr": err[:4000] if err else "",
        "total": len(items),
        "results": items,
    }
    if as_json:
        _json_out(payload)
    else:
        _print_list_human(payload)


def cmd_search(
    query: str,
    limit: int,
    use_clawhub: bool,
    with_details: bool,
    *,
    as_json: bool = False,
) -> None:
    kws = _keywords(query)
    if not kws:
        err = {
            "ok": False,
            "error": "empty_query",
            "message": "请提供搜索关键词，或 JSON {\"q\":\"天气 股票\"}，或使用 stdin / @文件。",
        }
        if as_json:
            _json_out(err)
        else:
            print(err["message"], file=sys.stderr)
        return

    seen: set[str] = set()
    merged: List[Dict[str, Any]] = []

    clawhub_available = _which_clawhub() is not None
    clawhub_code: Optional[int] = None
    clawhub_stdout = ""
    clawhub_stderr = ""
    clawhub_queries_tried: List[str] = []
    extra_urls: List[str] = []

    if use_clawhub and clawhub_available:
        clawhub_code, clawhub_stdout, clawhub_stderr, extra_urls, clawhub_queries_tried = _clawhub_search_cli(query, kws)
        for url in extra_urls:
            dk = _dedupe_key(url)
            if dk in seen:
                continue
            seen.add(dk)
            merged.append(_result_from_clawhub_url(url, kws))

    ws = _workspace_skills_dir()
    installed_names = _installed_skill_dir_names(ws)
    for r in merged:
        r["installed_locally"] = _skill_installed_locally(installed_names, r)

    sort_by = "match_score"
    if with_details and merged:
        _enrich_search_results_with_api(merged, _DETAIL_FETCH_TIMEOUT)
        merged.sort(
            key=lambda r: (
                -int(r.get("downloads") or 0),
                -int(r.get("stars") or 0),
                -float(r.get("match_score") or 0),
                r.get("name") or "",
            )
        )
        sort_by = "downloads_stars_match_score"
        merged = merged[:limit]
    else:
        merged.sort(
            key=lambda r: (
                -float(r.get("match_score") or 0),
                r.get("name") or "",
            )
        )
        merged = merged[:limit]
        for r in merged:
            r["stars"] = None
            r["downloads"] = None
            r["description"] = None
            r["author"] = None
            _apply_search_display_lines(r)

    _apply_ordered_skill_name_prefix(merged)

    payload = {
        "ok": True,
        "query": query,
        "keywords": kws,
        "with_details": bool(with_details and merged),
        "sort_by": sort_by,
        "workspace_skills_dir": str(ws),
        "clawhub_cli_available": clawhub_available,
        "clawhub_search_exit_code": clawhub_code,
        "clawhub_queries_tried": clawhub_queries_tried,
        "clawhub_search_stdout": clawhub_stdout[:8000] if clawhub_stdout else "",
        "clawhub_search_stderr": clawhub_stderr[:4000] if clawhub_stderr else "",
        "merge_note": "结果来自 clawhub search 解析。"
        + (
            " 已拉取 API 后按 下载量↓、星标↓、match_score↓、名称 排序，再取 --limit。"
            if sort_by == "downloads_stars_match_score"
            else " 未拉 API 时按 match_score↓、名称 排序后取 --limit；加默认详情拉取后可按下载量排序。"
        )
        + " 未安装 clawhub 或使用 --no-clawhub 时 results 为空。",
        "count": len(merged),
        "results": merged,
        "disclaimer": "安装第三方 Skill 前请阅读其 SKILL.md 与源码；星标/描述/作者来自 ClawHub API，可能与本地不同步；短 slug 在多组织下可能不唯一；installed_locally 按目录名启发式判断。",
    }
    if as_json:
        _json_out(payload)
    else:
        _print_search_human(payload)


def cmd_inspect(skill_name: str, *, as_json: bool = False) -> None:
    code, out, err = _run_clawhub(["inspect", skill_name])
    payload = {
        "ok": code == 0,
        "command": ["clawhub", "inspect", skill_name],
        "exit_code": code,
        "stdout": out,
        "stderr": err,
    }
    if as_json:
        _json_out(payload)
    else:
        _print_inspect_human(payload)


def cmd_install(skill_name: str, execute: bool, *, as_json: bool = False) -> None:
    if not execute:
        payload = {
            "ok": True,
            "dry_run": True,
            "message": "未执行安装。确认信任该 Skill 后使用：find_skills.py install <name> --execute",
            "command": ["clawhub", "install", skill_name],
            "verify_after": "find_skills.py verify %s" % skill_name,
        }
        if as_json:
            _json_out(payload)
        else:
            _print_install_human(payload)
        return
    code, out, err = _run_clawhub(["install", skill_name])
    payload = {
        "ok": code == 0,
        "command": ["clawhub", "install", skill_name],
        "exit_code": code,
        "stdout": out,
        "stderr": err,
        "verify_hint": "find_skills.py verify %s" % skill_name,
    }
    if as_json:
        _json_out(payload)
    else:
        _print_install_human(payload)


def cmd_stats(skill_slug: str, *, as_json: bool = False) -> None:
    """GET ClawHub stats API。当前服务端对 `org/skill` 多段路径常返回 404，会自动再试仅 **最后一段 skill 名**。"""
    candidates = _skill_api_candidate_urls(skill_slug)

    last_err: Optional[Dict[str, Any]] = None
    for url in candidates:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "jisu-find-skill/1.1"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                body = resp.read().decode("utf-8", errors="replace")
            try:
                data = json.loads(body)
            except Exception:
                data = {"raw": body[:5000]}
            payload = {
                "ok": True,
                "url": url,
                "tried_urls": candidates,
                "data": data,
                "note": "若同一 skill 名多组织并存，短名结果可能不唯一；请以 ClawHub 页面为准。",
            }
            if as_json:
                _json_out(payload)
            else:
                _print_stats_human(payload)
            return
        except urllib.error.HTTPError as e:
            last_err = {
                "ok": False,
                "url": url,
                "error": "http_error",
                "status": e.code,
                "body": e.read().decode("utf-8", errors="replace")[:2000],
            }
        except Exception as e:
            last_err = {"ok": False, "url": url, "error": str(e)}

    if last_err:
        last_err["tried_urls"] = candidates
        if as_json:
            _json_out(last_err)
        else:
            _print_stats_error_human(last_err)


def cmd_verify(skill_name: str, *, as_json: bool = False) -> None:
    root = _workspace_skills_dir()
    candidates = [
        root / skill_name / "SKILL.md",
        root / skill_name.replace("/", os.sep) / "SKILL.md",
    ]
    found: Optional[Path] = None
    for c in candidates:
        if c.is_file():
            found = c
            break
    payload = {
        "ok": True,
        "skill_name": skill_name,
        "workspace_skills_dir": str(root),
        "skill_md_found": found is not None,
        "skill_md_path": str(found) if found else None,
        "hint": "若未找到，可检查 OPENCLAW_SKILLS_DIR 或实际安装目录是否与 OpenClaw 一致。",
    }
    if as_json:
        _json_out(payload)
    else:
        _print_verify_human(payload)


def cmd_installed(*, as_json: bool = False) -> None:
    root = _workspace_skills_dir()
    names: List[str] = []
    if root.is_dir():
        for p in sorted(root.iterdir()):
            if p.is_dir() and (p / "SKILL.md").is_file():
                names.append(p.name)
    code, out, err = (-1, "", "")
    if _which_clawhub():
        code, out, err = _run_clawhub(["list"])
    payload = {
        "ok": True,
        "workspace_skills_dir": str(root),
        "installed_with_skill_md": names,
        "clawhub_list_exit_code": code,
        "clawhub_list_stdout": out[:8000] if out else "",
        "clawhub_list_stderr": err[:4000] if err else "",
    }
    if as_json:
        _json_out(payload)
    else:
        _print_installed_human(payload)


def _read_arg_query(argv: List[str]) -> str:
    if len(argv) < 3:
        return ""
    raw = argv[2].strip()
    if raw == "-":
        return sys.stdin.read().strip()
    if raw.startswith("@") and len(raw) > 1:
        return Path(raw[1:]).read_text(encoding="utf-8").strip()
    if raw.startswith("{") and raw.endswith("}"):
        try:
            obj = json.loads(raw)
            if isinstance(obj, dict) and obj.get("q") is not None:
                return str(obj.get("q", "")).strip()
        except Exception:
            pass
    return raw


def _usage() -> str:
    return (
        "通过 Python 运行本文件（非 PATH 命令；技能名 jisu-find-skill 不可直接当 shell 命令用）。\n"
        "示例: python skills/jisu-find-skill/find_skills.py installed\n"
        "Usage:\n"
        "  find_skills.py search <关键词|JSON|@file|-> [--limit N] [--no-clawhub] [--no-details] [--json]\n"
        "  find_skills.py list [--json]\n"
        "  find_skills.py inspect <org/skill 或 skill 名>\n"
        "  find_skills.py install <org/skill> [--execute]\n"
        "  find_skills.py stats <org/skill>     # HTTP GET ClawHub API\n"
        "  find_skills.py verify <本地目录名>\n"
        "  find_skills.py installed\n"
        "Env: OPENCLAW_SKILLS_DIR (默认 ~/.openclaw/workspace/skills)\n"
        "可读结果每条标题为 Markdown **粗体**；NO_COLOR=1 时不加 **。\n"
        "可选：PATH 中提供 clawhub CLI 以启用全站 search / inspect / install / list。\n"
        "默认输出人类可读文本；需要结构化数据时请加 --json（便于 Agent / jq 等）。\n"
    )


def main() -> None:
    raw = sys.argv[1:]
    limit = 15
    use_clawhub = True
    with_details = True
    as_json = False
    try:
        while "--limit" in raw:
            i = raw.index("--limit")
            limit = int(raw[i + 1])
            raw = raw[:i] + raw[i + 2 :]
        if "--no-clawhub" in raw:
            raw = [x for x in raw if x != "--no-clawhub"]
            use_clawhub = False
        if "--no-details" in raw:
            raw = [x for x in raw if x != "--no-details"]
            with_details = False
        if "--json" in raw:
            raw = [x for x in raw if x != "--json"]
            as_json = True
        limit = max(1, min(limit, 100))
    except Exception:
        limit = 15

    if len(raw) < 1:
        print(_usage(), file=sys.stderr)
        sys.exit(1)
    cmd = raw[0].strip().lower()

    if cmd == "list":
        cmd_list(as_json=as_json)
        return
    if cmd == "search":
        fake = [sys.argv[0], "search"] + raw[1:]
        q = _read_arg_query(fake)
        cmd_search(q, limit, use_clawhub, with_details, as_json=as_json)
        return
    if cmd == "inspect":
        if len(raw) < 2:
            if as_json:
                _json_out({"ok": False, "error": "missing_skill_name"})
            else:
                print("缺少技能名：find_skills.py inspect <org/skill>", file=sys.stderr)
            sys.exit(1)
        cmd_inspect(raw[1], as_json=as_json)
        return
    if cmd == "install":
        parts = [x for x in raw[1:] if x != "--execute"]
        execute = "--execute" in raw
        if not parts:
            if as_json:
                _json_out({"ok": False, "error": "missing_skill_name"})
            else:
                print("缺少技能名：find_skills.py install <org/skill>", file=sys.stderr)
            sys.exit(1)
        cmd_install(parts[0], execute, as_json=as_json)
        return
    if cmd == "stats":
        if len(raw) < 2:
            if as_json:
                _json_out({"ok": False, "error": "missing_skill_slug"})
            else:
                print("缺少 slug：find_skills.py stats <org/skill>", file=sys.stderr)
            sys.exit(1)
        cmd_stats(raw[1], as_json=as_json)
        return
    if cmd == "verify":
        if len(raw) < 2:
            if as_json:
                _json_out({"ok": False, "error": "missing_skill_name"})
            else:
                print("缺少本地目录名：find_skills.py verify <name>", file=sys.stderr)
            sys.exit(1)
        cmd_verify(raw[1], as_json=as_json)
        return
    if cmd == "installed":
        cmd_installed(as_json=as_json)
        return

    print("unknown command: %s" % cmd, file=sys.stderr)
    print(_usage(), file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
