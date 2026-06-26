#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prepare data for replying to a GitCode issue.
Read-only: fetches issue, comments, history, DeepWiki; outputs JSON. No comments posted.

Usage:
  python prepare_issue_reply.py --issue-url "https://gitcode.com/owner/repo/issues/123"
"""

import sys
import re
import json
import argparse
import time
import hashlib
import os
import urllib.request
import urllib.error
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import quote

# SKILL_ROOT 是脚本所在目录的父目录（即 skill 根目录）
SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
CONFIG_FILE = SKILL_ROOT / "config.json"
PROMPTS_DIR = SKILL_ROOT / "references" / "prompts"

sys.path.insert(0, str(SCRIPT_DIR))
from _common import get_token, print_json, parse_issue_url, api_get, init_windows_encoding
from bm25_kb import BM25KnowledgeBase
from security_filter import PromptInjectionDetector
from utils import extract_image_urls, download_image, deepwiki_query, image_to_base64

DEFAULT_CONFIG = {
    "issue_content_max_chars": 3000,
    "history_issues_limit": 100,
    "history_days": 365,
    "deepwiki_timeout": 120,
    "deepwiki_max_retries": 3,
    "bm25_similarity_threshold": 5.0,  # 相似度阈值，BM25得分通常在0-20之间，5.0为中等相似度
    "bm25_top_k": 5,
    "dry_run": False,
    "enable_deepwiki": True,
    "api_timeout": 30,
    "cache_ttl_seconds": 300,  # 缓存有效期 5 分钟
    "enable_cache": True,
}

BOT_INDICATORS = ["bot", "[bot]", "ci-bot", "gitcode-bot", "webhook"]


def load_config() -> Dict:
    cfg = DEFAULT_CONFIG.copy()
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                user_cfg = json.load(f)
                cfg.update(user_cfg)
        except Exception as e:
            sys.stderr.write("Warning: failed to load config.json: %s\n" % e)
    return cfg


def replace_images_with_placeholder(text: str) -> str:
    if not text or not isinstance(text, str):
        return ""
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", "[图片]", text)
    text = re.sub(
        r"https?://[^\s)]+\.(?:png|jpe?g|gif|webp|bmp|svg)(?:\?[^\s)]*)?",
        "[图片链接]", text, flags=re.I,
    )
    return text.strip()


def _is_bot_user(user_dict: Dict) -> bool:
    if not user_dict:
        return False
    if (user_dict.get("type") or "").lower() == "bot":
        return True
    login = (user_dict.get("login") or user_dict.get("username") or "").lower()
    return any(ind in login for ind in BOT_INDICATORS)


def _is_substantive_comment(body_text: str) -> bool:
    if not body_text:
        return False
    stripped = body_text.strip()
    if stripped.startswith("/"):
        return False
    return len(stripped) >= 10


def fetch_issue(token: str, owner: str, repo: str, number: int) -> Dict:
    return api_get(token, f"repos/{owner}/{repo}/issues/{number}")


def fetch_comments(token: str, owner: str, repo: str, number: int) -> List[Dict]:
    comments = []
    page = 1
    while True:
        try:
            batch = api_get(token,
                            f"repos/{owner}/{repo}/issues/{number}/comments?per_page=100&page={page}")
        except Exception as e:
            sys.stderr.write("Warning: failed to fetch comments page %d: %s\n" % (page, e))
            break
        if not isinstance(batch, list) or not batch:
            break
        comments.extend(batch)
        if len(batch) < 100:
            break
        page += 1
        if page > 10:
            break
    return comments


def fetch_history_issues(token: str, owner: str, repo: str, number: int, 
                         history_max: int, history_days: int) -> List[Dict]:
    """获取历史 Issues，优先获取已关闭且有解决方案的"""
    now = datetime.now(timezone.utc)
    since_date = (now - timedelta(days=history_days)).strftime("%Y-%m-%dT%H:%M:%SZ")
    history_issues = []

    # 首先获取已关闭的 Issues（通常包含有价值的解决方案）
    for state in ["closed", "open"]:
        if len(history_issues) >= history_max:
            break
        page = 1
        while len(history_issues) < history_max:
            try:
                items = api_get(
                    token,
                    f"repos/{owner}/{repo}/issues?state={state}&since={since_date}"
                    f"&per_page=100&page={page}&sort=updated&direction=desc")
            except Exception as e:
                sys.stderr.write("Warning: failed to fetch history page %d: %s\n" % (page, e))
                break
            if not isinstance(items, list) or not items:
                break
            for i in items:
                if i.get("number") == number:
                    continue
                if "CVE" in (i.get("title") or "").upper():
                    continue
                # 跳过 PR（pull request 也有 issue 接口）
                if i.get("pull_request"):
                    continue
                num = i.get("number")
                if num is not None:
                    history_issues.append({
                        "number": int(num) if isinstance(num, str) else num,
                        "title": (i.get("title") or "")[:200],
                        "body": (i.get("body") or "")[:1000],
                        "state": i.get("state", ""),
                        "labels": [l.get("name") for l in (i.get("labels") or []) if l.get("name")],
                        "created_at": i.get("created_at", ""),
                        "updated_at": i.get("updated_at", ""),
                    })
                if len(history_issues) >= history_max:
                    break
            if len(items) < 100:
                break
            page += 1
            if page > 5:  # 减少页面数以避免过多 API 调用
                break

    # 按更新时间和状态排序（closed 优先，然后按更新时间）
    history_issues.sort(key=lambda x: (x.get("state") != "closed", x.get("updated_at", "")), reverse=True)

    return history_issues[:history_max]


def check_new_contributor(token: str, owner: str, repo: str, number: int,
                          author_id: Optional[int], author_login: str) -> bool:
    is_new_contributor = True
    try:
        if author_login:
            check_issues = api_get(
                token,
                f"repos/{owner}/{repo}/issues?state=all"
                f"&creator={quote(author_login)}&per_page=5")
            other_issues = [i for i in (check_issues or []) if i.get("number") != number]
            if other_issues:
                is_new_contributor = False
        if is_new_contributor and author_login:
            check_pulls = api_get(
                token,
                f"repos/{owner}/{repo}/pulls?state=all&per_page=20")
            for p in (check_pulls or []):
                u = p.get("user") or {}
                if (u.get("id") == author_id
                        or (u.get("login") or u.get("username") or "") == author_login):
                    is_new_contributor = False
                    break
    except Exception as e:
        sys.stderr.write("Warning: new contributor check failed: %s\n" % e)
    return is_new_contributor


def get_issue_temp_dir(owner: str, repo: str, issue_number: int) -> Path:
    """获取当前 Issue 的临时目录（按 owner_repo_issuenumber 组织）"""
    base_dir = SKILL_ROOT / "temp_dir" / f"{owner}_{repo}_{issue_number}"
    base_dir.mkdir(parents=True, exist_ok=True)
    return base_dir


def get_cache_dir() -> Path:
    """获取缓存目录（位于 skill 目录下的 temp_dir）"""
    base_dir = SKILL_ROOT / "temp_dir" / "cache"
    base_dir.mkdir(parents=True, exist_ok=True)
    return base_dir


def get_cache_key(prefix: str, *args) -> str:
    """生成缓存键"""
    content = "|".join(str(a) for a in args)
    return f"{prefix}_{hashlib.md5(content.encode()).hexdigest()[:16]}"


def get_cached_data(cache_key: str, ttl_seconds: int) -> Optional[Dict]:
    """获取缓存数据"""
    cache_file = get_cache_dir() / f"{cache_key}.json"
    if not cache_file.exists():
        return None

    try:
        # 检查是否过期
        mtime = cache_file.stat().st_mtime
        if time.time() - mtime > ttl_seconds:
            cache_file.unlink()
            return None

        with open(cache_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def set_cached_data(cache_key: str, data: Dict) -> bool:
    """设置缓存数据"""
    try:
        cache_file = get_cache_dir() / f"{cache_key}.json"
        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
        return True
    except Exception:
        return False


def get_kb_dir(owner: str, repo: str) -> Path:
    """获取知识库存储目录（位于 skill 目录下的 temp_dir/kb）"""
    base_dir = SKILL_ROOT / "temp_dir" / "kb"
    return base_dir / f"{owner}_{repo}"


def load_or_update_knowledge_base(owner: str, repo: str, history_issues: List[Dict],
                                   current_issue: Dict, config: Dict) -> BM25KnowledgeBase:
    kb_dir = get_kb_dir(owner, repo)
    kb = BM25KnowledgeBase.load_from_disk(str(kb_dir))

    existing_ids = set(kb.documents.keys()) if kb else set()
    all_issues = history_issues.copy()

    current_number = str(current_issue.get("number", ""))
    if current_number and current_number not in existing_ids:
        all_issues.append({
            "number": current_issue.get("number"),
            "title": current_issue.get("title", ""),
            "body": current_issue.get("body", ""),
            "state": current_issue.get("state", ""),
            "labels": [l.get("name") for l in (current_issue.get("labels") or []) if l.get("name")],
            "created_at": current_issue.get("created_at", ""),
        })

    if kb is None:
        kb = BM25KnowledgeBase()

    new_count = 0
    for issue in all_issues:
        doc_id = str(issue.get("number", ""))
        if doc_id in existing_ids:
            continue
        title = issue.get("title", "")
        body = issue.get("body", "")
        content = f"{title}\n{body}"
        metadata = {
            "state": issue.get("state", ""),
            "labels": issue.get("labels", []),
            "created_at": issue.get("created_at", ""),
        }
        if kb.add_document(doc_id, content, title, metadata):
            new_count += 1

    if new_count > 0:
        kb_dir.mkdir(parents=True, exist_ok=True)
        kb.save_to_disk(str(kb_dir))
        sys.stderr.write("Knowledge base updated: %d new documents\n" % new_count)

    return kb


def find_similar_issues(kb: BM25KnowledgeBase, issue_title: str, issue_body: str,
                        history_issues: List[Dict], current_issue_number: int,
                        current_issue_created_at: str, config: Dict) -> Tuple[List[int], List[Dict]]:
    """
    查找相似 Issue

    规则：
    1. 排除当前 Issue 自己
    2. 只比较创建时间更早的 Issue（历史 Issue）
    3. 返回相似 Issue 编号列表和详细的相似度信息
    """
    if not kb or not kb.documents:
        return [], []

    query = f"{issue_title}\n{issue_body}"
    threshold = config.get("bm25_similarity_threshold", 5.0)
    top_k = config.get("bm25_top_k", 10)  # 多取一些，过滤后再取前5

    results = kb.search(query, top_k=top_k)

    # 解析当前 Issue 的创建时间
    current_created = None
    if current_issue_created_at:
        try:
            current_created = datetime.fromisoformat(current_issue_created_at.replace('Z', '+00:00'))
        except:
            pass

    similar_numbers = []
    similarity_details = []

    for r in results:
        try:
            issue_num = int(r.doc_id)

            # 规则1：排除自己
            if issue_num == current_issue_number:
                continue

            # 规则2：只比较历史 Issue（创建时间更早）
            if current_created:
                # 查找该 Issue 的创建时间
                issue_info = next((h for h in history_issues if int(h.get("number", 0)) == issue_num), None)
                if issue_info:
                    issue_created = issue_info.get("created_at")
                    if issue_created:
                        try:
                            issue_created_dt = datetime.fromisoformat(issue_created.replace('Z', '+00:00'))
                            if issue_created_dt >= current_created:
                                continue  # 跳过比当前 Issue 晚创建的
                        except:
                            pass

            if r.score >= threshold:
                similar_numbers.append(issue_num)
                similarity_details.append({
                    "number": issue_num,
                    "score": round(r.score, 4),
                    "title": r.document.title[:100] if r.document else ""
                })
        except ValueError:
            pass

    # 只返回前5个
    return similar_numbers[:5], similarity_details[:5]


def security_check_content(detector: PromptInjectionDetector, content: str, 
                           content_type: str) -> Optional[Dict]:
    if not content:
        return None

    result = detector.check(content)
    if not result.passed:
        return {
            "content_type": content_type,
            "risk_level": result.risk_level.value,
            "threats": result.threats,
            "suggestion": result.suggestion,
        }
    return None


def main():
    parser = argparse.ArgumentParser(
        description="Prepare issue reply data (read-only, no comments posted)")
    parser.add_argument("--issue-url", required=True, help="Full issue URL")
    parser.add_argument("--token", help="GitCode API token (optional, will use GITCODE_TOKEN env var if not provided)")
    parser.add_argument("--no-cache", action="store_true", help="Disable cache, force fresh data fetch")
    args = parser.parse_args()

    init_windows_encoding()

    token = get_token(args.token)
    if not token:
        print_json({"status": "error",
                     "message": "GITCODE_TOKEN 未配置。请访问 https://gitcode.com/setting/token-classic 创建令牌。"})
        sys.exit(1)

    try:
        owner, repo, number = parse_issue_url(args.issue_url)
    except ValueError as e:
        print_json({"status": "error", "message": str(e)})
        sys.exit(1)

    config = load_config()
    content_max = config.get("issue_content_max_chars", 3000)
    history_max = config.get("history_issues_limit", 100)
    history_days = config.get("history_days", 365)
    enable_deepwiki = config.get("enable_deepwiki", True)
    enable_cache = config.get("enable_cache", True) and not args.no_cache
    cache_ttl = config.get("cache_ttl_seconds", 300)

    # 尝试从缓存获取
    if enable_cache:
        cache_key = get_cache_key("issue_reply", owner, repo, number, token[:8])
        cached_result = get_cached_data(cache_key, cache_ttl)
        if cached_result:
            sys.stderr.write("Using cached data (use --no-cache to force refresh)\n")
            print_json(cached_result)
            return

    security_detector = PromptInjectionDetector()

    issue = None
    comments = []
    history_issues = []
    deepwiki_answer = ""
    deepwiki_status = "skipped"

    deepwiki_timeout = config.get("deepwiki_timeout", 120)

    try:
        issue = fetch_issue(token, owner, repo, number)
    except HTTPError as e:
        body = e.read().decode("utf-8", errors="replace") if e.fp else ""
        error_msg = "Issue 不存在或无权限访问" if e.code == 404 else f"获取 Issue 失败: {e.code}"
        print_json({"status": "error", "message": error_msg})
        sys.exit(1)
    except Exception as e:
        print_json({"status": "error", "message": "获取 Issue 失败: %s" % str(e)})
        sys.exit(1)

    try:
        comments = fetch_comments(token, owner, repo, number)
    except Exception as e:
        sys.stderr.write("Warning: failed to fetch comments: %s\n" % e)
        comments = []

    try:
        history_issues = fetch_history_issues(token, owner, repo, number, 
                                              history_max, history_days)
    except Exception as e:
        sys.stderr.write("Warning: failed to fetch history: %s\n" % e)
        history_issues = []

    security_warnings = []

    issue_body = issue.get("body") or ""
    body_security = security_check_content(security_detector, issue_body, "issue_body")
    if body_security:
        security_warnings.append(body_security)

    for idx, c in enumerate(comments):
        comment_body = c.get("body") or ""
        comment_security = security_check_content(security_detector, comment_body, 
                                                   f"comment_{idx}")
        if comment_security:
            security_warnings.append(comment_security)

    if security_warnings:
        sys.stderr.write("Security warnings detected: %d issues\n" % len(security_warnings))
        for w in security_warnings:
            sys.stderr.write("  - %s: %s\n" % (w["content_type"], w["risk_level"]))

    author_id = (issue.get("user") or {}).get("id")
    author_login = ((issue.get("user") or {}).get("login")
                    or (issue.get("user") or {}).get("username") or "")

    has_other_reply = False
    for c in comments:
        u = c.get("user") or {}
        if _is_bot_user(u):
            continue
        uid = u.get("id")
        ulogin = u.get("login") or u.get("username") or ""
        if uid == author_id or (ulogin and ulogin == author_login):
            continue
        if _is_substantive_comment(c.get("body", "")):
            has_other_reply = True
            break

    if has_other_reply:
        print_json({
            "status": "already_replied",
            "owner": owner, "repo": repo, "issue_number": number,
            "message": "该 Issue 已有其他人回复，已跳过",
        })
        return

    has_label_comment = any("/label add" in (c.get("body") or "").lower() for c in comments)
    dry_run = config.get("dry_run", False)
    label_needed = not has_label_comment and not dry_run

    parts = [issue.get("title") or "", "\n\n", issue.get("body") or ""]
    for c in sorted(comments, key=lambda x: (x.get("created_at") or "")):
        body_text = (c.get("body") or "").strip()
        if body_text.startswith("/"):
            continue
        parts.append("\n\n[评论] ")
        parts.append((c.get("user") or {}).get("login")
                      or (c.get("user") or {}).get("username") or "?")
        parts.append(": ")
        parts.append(body_text)
    issue_content_plain = replace_images_with_placeholder("".join(parts))

    if len(issue_content_plain) > content_max:
        issue_content_plain = issue_content_plain[:content_max] + "\n\n[内容已截断]"

    if enable_deepwiki:
        try:
            query_text = ((issue.get("title") or "") + "\n"
                          + ((issue.get("body") or "")[:500]))
            if query_text.strip():
                deepwiki_answer, deepwiki_status = deepwiki_query(
                    f"{owner}/{repo}",
                    query_text.strip(),
                    base_timeout=config.get("deepwiki_timeout", 120),
                    max_retries=config.get("deepwiki_max_retries", 3),
                )
        except Exception as e:
            sys.stderr.write("Warning: DeepWiki query failed: %s\n" % e)
            deepwiki_status = "failed"

    is_new_contributor = check_new_contributor(token, owner, repo, number, 
                                                author_id, author_login)

    labels = [lb.get("name") for lb in (issue.get("labels") or []) if lb.get("name")]
    meta = {
        "title": (issue.get("title") or "")[:500],
        "labels": labels,
        "is_new_contributor": is_new_contributor,
    }

    similar_issue_numbers = []
    similarity_details = []
    try:
        kb = load_or_update_knowledge_base(owner, repo, history_issues, issue, config)
        similar_issue_numbers, similarity_details = find_similar_issues(
            kb, issue.get("title", ""), 
            issue.get("body", ""), 
            history_issues, 
            int(issue.get("number", 0)),
            issue.get("created_at", ""),
            config
        )
    except Exception as e:
        sys.stderr.write("Warning: BM25 search failed: %s\n" % e)

    if similar_issue_numbers:
        history_fmt = "\n".join(
            "#%s" % num for num in similar_issue_numbers[:5])
    else:
        history_fmt = "\n".join(
            "#%s %s" % (h["number"], (h.get("title") or "").strip())
            for h in history_issues[:5])

    # 提取图片 URL（必须在生成 prompt 之前）
    image_urls = extract_image_urls(issue.get("body") or "")
    for c in comments:
        image_urls.extend(extract_image_urls(c.get("body") or ""))
    image_urls = list(dict.fromkeys(image_urls))

    prompt_draft_partial = ""
    if PROMPTS_DIR.exists():
        draft_path = PROMPTS_DIR / "draft_reply.txt"
        if draft_path.exists():
            try:
                issue_base_url = "https://gitcode.com/%s/%s" % (owner, repo)
                tpl = draft_path.read_text(encoding="utf-8")
                tpl = tpl.replace("{issue_content_plain}", issue_content_plain)
                tpl = tpl.replace("{issue_metadata.title}", meta["title"])
                tpl = tpl.replace("{issue_metadata.labels}",
                                  ", ".join(meta["labels"]) if meta["labels"] else "（无）")
                tpl = tpl.replace("{issue_metadata.is_new_contributor}",
                                  "是" if meta["is_new_contributor"] else "否")
                tpl = tpl.replace("{deepwiki_answer}",
                                  deepwiki_answer if deepwiki_answer else "（无）")
                tpl = tpl.replace("{issue_base_url}", issue_base_url)
                # 传入图片信息
                if image_urls:
                    image_info_lines = ["检测到以下图片（AI 助手必须查看这些图片）："]
                    for i, url in enumerate(image_urls[:5], 1):
                        image_info_lines.append(f"  - 图片{i}: {url}")
                    image_info = "\n".join(image_info_lines)
                else:
                    image_info = "（无图片）"
                tpl = tpl.replace("{image_info}", image_info)
                prompt_draft_partial = tpl
            except Exception as e:
                sys.stderr.write("Warning: failed to read draft prompt: %s\n" % e)

    similar_formatted = ", ".join("#%s" % n for n in similar_issue_numbers[:3]) if similar_issue_numbers else "（无）"

    # 下载图片到本地（按 owner_repo_issuenumber 组织）
    image_local_paths = []
    image_base64_list = []  # 存储 base64 编码的图片
    if image_urls:
        issue_temp_dir = get_issue_temp_dir(owner, repo, number)
        images_dir = issue_temp_dir / "images"
        images_dir.mkdir(parents=True, exist_ok=True)

        for i, url in enumerate(image_urls[:5]):  # 最多处理5张图片
            local_path = download_image(url, images_dir, index=i)
            if local_path:
                image_local_paths.append(str(local_path))
                # 转换为 base64
                base64_data = image_to_base64(local_path)
                if base64_data:
                    image_base64_list.append(base64_data)

    # 收集警告信息
    warnings = []
    if security_warnings:
        warnings.extend([w.get("suggestion", str(w)) for w in security_warnings])
    if deepwiki_status == "failed":
        warnings.append("DeepWiki 查询失败，回复可能缺少项目背景信息")
    if not similar_issue_numbers and not history_issues:
        warnings.append("未找到相似历史 Issue")

    out = {
        "status": "ok",
        "owner": owner,
        "repo": repo,
        "issue_number": number,
        "issue_url": args.issue_url,
        "issue_content_plain": issue_content_plain,
        "issue_metadata": meta,
        "image_urls": image_urls,
        "image_local_paths": image_local_paths,  # 本地图片路径列表
        "image_base64_list": image_base64_list,  # base64 编码的图片列表（用于 AI 识别）
        "history_issues": history_issues,
        "similar_issues": similar_issue_numbers,
        "similarity_details": similarity_details,  # 详细的相似度信息
        "deepwiki_answer": deepwiki_answer,
        "deepwiki_status": deepwiki_status,
        "label_needed": label_needed,
        "prompt_draft_partial": prompt_draft_partial,
        "security_warnings": security_warnings if security_warnings else None,
        "warnings": warnings if warnings else None,
        "cached": False,
        "cached_at": datetime.now(timezone.utc).isoformat(),
    }

    # 保存到缓存
    if enable_cache:
        set_cached_data(cache_key, out)

    # 输出到文件（不输出到stdout，避免Windows终端编码问题）
    output_file = SKILL_ROOT / f"output_{owner}_{repo}_{number}.json"
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(out, f, ensure_ascii=False, indent=2)
            f.write('\n')
    except Exception as e:
        sys.stderr.write(f"Error: Failed to write output file: {e}\n")
        sys.exit(1)

    # 输出重要提醒到stderr
    sys.stderr.write("\n" + "="*60 + "\n")
    sys.stderr.write(f"✓ 输出文件: {output_file}\n")

    # 提醒查看图片
    if image_urls:
        sys.stderr.write("\n" + "⚠️"*20 + "\n")
        sys.stderr.write(f"⚠️  重要提醒：该 Issue 包含 {len(image_urls)} 张图片！\n")
        sys.stderr.write("⚠️  根据 SKILL.md 要求，必须在生成回复前查看这些图片！\n")
        for i, path in enumerate(image_local_paths, 1):
            sys.stderr.write(f"   图片{i}: {path}\n")
        sys.stderr.write("⚠️"*20 + "\n")

    # 提醒检查关键字段
    sys.stderr.write("\n📋 执行检查清单：\n")
    sys.stderr.write(f"   [✓] status: {out['status']}\n")
    sys.stderr.write(f"   [{'✓' if image_urls else ' '}] image_urls: {len(image_urls)} 张图片{' (必须查看!)' if image_urls else ''}\n")
    sys.stderr.write(f"   [{'✓' if out['deepwiki_status'] == 'ok' else ' '}] deepwiki_status: {out['deepwiki_status']}\n")
    if out['security_warnings']:
        sys.stderr.write(f"   [⚠️] security_warnings: 检测到 {len(out['security_warnings'])} 个警告\n")
    sys.stderr.write("="*60 + "\n")


if __name__ == "__main__":
    main()
