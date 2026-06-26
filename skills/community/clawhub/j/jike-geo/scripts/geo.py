#!/usr/bin/env python3
"""
极义GEO CLI — OpenClaw skill script for GEO platform API.

Usage:
  python3 geo.py check
  python3 geo.py quota
  python3 geo.py products list|create|get|update|delete
  python3 geo.py company get|save
  python3 geo.py keywords list|add|delete
  python3 geo.py questions generate|list|toggle
  python3 geo.py drafts generate|list|latest|get|update|delete
  python3 geo.py gallery categories-list|categories-create|categories-update|categories-delete|images-list|images-upload|images-delete
  python3 geo.py search create|batch|status|batch-status|history
  python3 geo.py articles generate|list|get|update|delete
  python3 geo.py publish record|list
  python3 geo.py platforms list
  python3 geo.py ai-platforms
  python3 geo.py sentiment

Configuration:
  Edit scripts/config.json to set secret_key and base_url.
  Environment variables JIKE_GEO_SECRET_KEY / JIKE_GEO_BASE_URL override config.json.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(SCRIPT_DIR, "config.json")

DEFAULT_BASE_URL = "https://api.jike-geo.100.city"
POLL_INTERVAL = 3
MAX_POLL_SECONDS = 300

_config_cache = None


def load_config() -> dict:
    """Load config from config.json, cache it."""
    global _config_cache
    if _config_cache is not None:
        return _config_cache

    if not os.path.exists(CONFIG_PATH):
        _config_cache = {}
        return _config_cache

    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            _config_cache = json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        print(f"Warning: Failed to read config.json: {e}", file=sys.stderr)
        _config_cache = {}
    return _config_cache


def get_config():
    """Resolve secret_key and base_url. Environment variable overrides config.json for key."""
    cfg = load_config()

    # secret_key: env > config.json
    key = os.environ.get("JIKE_GEO_SECRET_KEY", "").strip()
    if not key:
        key = (cfg.get("secret_key") or "").strip()
    if not key:
        print("Error: secret_key not configured.", file=sys.stderr)
        print(f"  Set it in {CONFIG_PATH} or via JIKE_GEO_SECRET_KEY env var.", file=sys.stderr)
        print("  Get your API Key at: https://jike-geo.100.city", file=sys.stderr)
        sys.exit(1)

    base = DEFAULT_BASE_URL

    return key, base


def get_default_product_id() -> str | None:
    """Get default product_id from config.json."""
    cfg = load_config()
    pid = cfg.get("product_id")
    return str(pid) if pid else None


def get_poll_settings() -> tuple[int, int]:
    """Get poll_interval and poll_timeout from config.json."""
    cfg = load_config()
    interval = cfg.get("poll_interval", POLL_INTERVAL)
    timeout = cfg.get("poll_timeout", MAX_POLL_SECONDS)
    return int(interval), int(timeout)

def api_request(method: str, path: str, body=None, product_id=None,
                 query: dict | None = None, raw: bool = False) -> dict:
    """Send HTTP request to GEO API. Returns parsed JSON response."""
    key, base = get_config()
    url = f"{base}{path}"
    if query:
        url += "?" + urllib.parse.urlencode({k: v for k, v in query.items() if v is not None})

    headers = {
        "X-API-Key": key,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    if product_id:
        headers["X-Product-ID"] = str(product_id)

    data = json.dumps(body).encode("utf-8") if body else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")
        try:
            err_json = json.loads(err_body)
            msg = err_json.get("message", err_body)
        except Exception:
            msg = err_body
        print(f"Error: HTTP {e.code} — {msg}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Error: Connection failed — {e.reason}", file=sys.stderr)
        sys.exit(1)

    if raw:
        return result
    if isinstance(result, dict) and result.get("code", 0) != 0:
        print(f"Error: {result.get('message', 'Unknown error')}", file=sys.stderr)
        sys.exit(1)
    return result.get("data") if isinstance(result, dict) else result


def fmt_json(data, use_json: bool = False):
    """Print data as JSON or return for formatting."""
    if use_json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return True
    return False


def resolve_product_id(args) -> str:
    """Resolve product_id from args or config.json default."""
    pid = getattr(args, "product_id", None)
    if not pid:
        pid = get_default_product_id()
    if not pid:
        print("Error: --product-id required (or set product_id in config.json)", file=sys.stderr)
        sys.exit(1)
    return pid


# ---------------------------------------------------------------------------
# Commands: check / quota
# ---------------------------------------------------------------------------


def cmd_check(_args):
    key, base = get_config()
    print(f"Config:   {CONFIG_PATH}")
    print(f"Base URL: {base}")
    print(f"Key:      {key[:8]}...{key[-4:]}" if len(key) > 12 else f"Key: {key}")
    pid = get_default_product_id()
    if pid:
        print(f"Product:  {pid} (default)")
    try:
        data = api_request("GET", "/api/v1/user/info")
        print(f"Status:   OK")
        if data:
            print(f"Phone:    {data.get('phone', 'N/A')}")
            print(f"User ID:  {data.get('id', 'N/A')}")
    except SystemExit:
        print("Status:   FAILED — check your secret key")
        print("  Get your API Key at: https://jike-geo.100.city")
        sys.exit(1)


def cmd_quota(args):
    data = api_request("GET", "/api/v1/user/quota")
    if fmt_json(data, args.json):
        return
    print(f"套餐: {data.get('package_name', 'N/A')}")
    print(f"产品: {data.get('products_used', 0)}/{data.get('max_products', 0) or '∞'}")
    print(f"问题: {data.get('questions_used', 0)}/{data.get('max_questions', 0) or '∞'}")
    print(f"文章: {data.get('articles_used', 0)}/{data.get('max_articles', 0) or '∞'}")
    exp = data.get("expire_at", "")
    expired = data.get("expired", False)
    print(f"到期: {exp}" + (" ⚠️ 已过期" if expired else ""))


# ---------------------------------------------------------------------------
# Commands: products
# ---------------------------------------------------------------------------


def cmd_products(args):
    action = args.action
    if action == "list":
        data = api_request("GET", "/api/v1/products")
        if fmt_json(data, args.json):
            return
        if not data:
            print("暂无产品")
            return
        for p in data:
            print(f"[{p['id']}] {p['name']}  — {p.get('description', '')}")

    elif action == "create":
        if not args.name:
            print("Error: --name required", file=sys.stderr); sys.exit(1)
        body = {"name": args.name, "description": args.description or ""}
        data = api_request("POST", "/api/v1/products", body)
        if fmt_json(data, args.json):
            return
        print(f"产品创建成功: [{data['id']}] {data['name']}")

    elif action == "get":
        if not args.id:
            print("Error: --id required", file=sys.stderr); sys.exit(1)
        data = api_request("GET", f"/api/v1/products/{args.id}")
        if fmt_json(data, args.json):
            return
        print(json.dumps(data, ensure_ascii=False, indent=2))

    elif action == "update":
        if not args.id:
            print("Error: --id required", file=sys.stderr); sys.exit(1)
        body = {}
        if args.name: body["name"] = args.name
        if args.description: body["description"] = args.description
        data = api_request("PUT", f"/api/v1/products/{args.id}", body)
        print("产品更新成功")

    elif action == "delete":
        if not args.id:
            print("Error: --id required", file=sys.stderr); sys.exit(1)
        api_request("DELETE", f"/api/v1/products/{args.id}")
        print(f"产品 {args.id} 已删除")


# ---------------------------------------------------------------------------
# Commands: company
# ---------------------------------------------------------------------------


COMPANY_FIELDS = [
    "product_name", "company_name", "industry", "business_scope",
    "cities", "contact_phone", "website", "editor_name",
    "description", "company_description", "product_description",
    "target_customer_type", "customer_description", "competitors",
    "writing_style",
]

COMPANY_LABELS = {
    "product_name": "产品名称",
    "company_name": "公司名称",
    "industry": "所属行业",
    "business_scope": "业务范围",
    "cities": "服务城市",
    "contact_phone": "联系电话",
    "website": "官网地址",
    "editor_name": "编辑署名",
    "description": "简要描述",
    "company_description": "企业介绍",
    "product_description": "产品介绍",
    "target_customer_type": "客户类型",
    "customer_description": "目标客户",
    "competitors": "竞争对手",
    "writing_style": "写作风格",
}


def cmd_company(args):
    pid = resolve_product_id(args)

    if args.action == "get":
        data = api_request("GET", "/api/v1/company", product_id=pid)
        if fmt_json(data, args.json):
            return
        if not data:
            print("该产品暂无公司信息")
            return
        for k in COMPANY_FIELDS:
            label = COMPANY_LABELS.get(k, k)
            val = data.get(k, "")
            if val:
                print(f"{label}: {val}")

    elif args.action == "save":
        body = {}
        for k in COMPANY_FIELDS:
            v = getattr(args, k.replace("-", "_"), None)
            if v is not None:
                body[k] = v
        if not body:
            print("Error: at least one field required", file=sys.stderr); sys.exit(1)
        data = api_request("POST", "/api/v1/company", body, product_id=pid)
        if fmt_json(data, args.json):
            return
        print("公司信息保存成功")


# ---------------------------------------------------------------------------
# Commands: keywords
# ---------------------------------------------------------------------------


def cmd_keywords(args):
    pid = resolve_product_id(args)

    if args.action == "list":
        data = api_request("GET", "/api/v1/keywords", product_id=pid)
        if fmt_json(data, args.json):
            return
        if not data:
            print("暂无核心词")
            return
        for kw in data:
            print(f"[{kw['id']}] {kw['word']}")

    elif args.action == "add":
        if not args.word:
            print("Error: --word required", file=sys.stderr); sys.exit(1)
        data = api_request("POST", "/api/v1/keywords", {"word": args.word}, product_id=pid)
        if fmt_json(data, args.json):
            return
        print(f"核心词添加成功: [{data['id']}] {data['word']}")

    elif args.action == "delete":
        if not args.id:
            print("Error: --id required", file=sys.stderr); sys.exit(1)
        api_request("DELETE", f"/api/v1/keywords/{args.id}", product_id=pid)
        print(f"核心词 {args.id} 已删除")


# ---------------------------------------------------------------------------
# Commands: questions
# ---------------------------------------------------------------------------


def cmd_questions(args):
    pid = resolve_product_id(args)

    if args.action == "generate":
        if not args.keywords:
            print("Error: --keywords required (comma-separated keyword texts)", file=sys.stderr); sys.exit(1)
        words = [x.strip() for x in args.keywords.split(",") if x.strip()]
        data = api_request("POST", "/api/v1/questions/generate",
                           {"keywords": words}, product_id=pid)
        if fmt_json(data, args.json):
            return
        if isinstance(data, list):
            print(f"生成了 {len(data)} 个问题:")
            for q in data:
                print(f"  [{q['id']}] ({q.get('stage', '?')}) {q['content']}")
        else:
            print(json.dumps(data, ensure_ascii=False, indent=2))

    elif args.action == "list":
        query = {}
        if args.keyword_id:
            query["keyword_id"] = args.keyword_id
        data = api_request("GET", "/api/v1/questions", product_id=pid, query=query)
        if fmt_json(data, args.json):
            return
        stages = {"inquiry": "L1 认知", "understanding": "L2 探索",
                  "consideration": "L3 评估", "purchase": "L4 决策"}
        if isinstance(data, dict):
            for stage_key, label in stages.items():
                qs = data.get(stage_key, [])
                if qs:
                    print(f"\n{label}:")
                    for q in qs:
                        sel = "✓" if q.get("selected") else " "
                        print(f"  [{sel}] [{q['id']}] {q['content']}")
        else:
            print(json.dumps(data, ensure_ascii=False, indent=2))

    elif args.action == "toggle":
        if not args.id:
            print("Error: --id required", file=sys.stderr); sys.exit(1)
        api_request("PUT", f"/api/v1/questions/{args.id}/toggle", product_id=pid)
        print(f"问题 {args.id} 选中状态已切换")


# ---------------------------------------------------------------------------
# Commands: search (core GEO functionality)
# ---------------------------------------------------------------------------


def poll_task(task_id, product_id, is_batch=False):
    """Poll a search task until completion."""
    interval, timeout = get_poll_settings()
    endpoint = "batch" if is_batch else "task"
    elapsed = 0
    while elapsed < timeout:
        data = api_request("GET", f"/api/v1/geo-search/{endpoint}/{task_id}",
                           product_id=product_id)
        status = data.get("status", "unknown")
        if status in ("completed", "done", "finished"):
            return data
        if status in ("failed", "error"):
            print(f"Error: Task failed — {data.get('error', 'unknown')}", file=sys.stderr)
            sys.exit(1)
        # Show progress
        if is_batch:
            total = data.get("total_tasks", 0)
            done = data.get("completed_tasks", 0)
            print(f"  进度: {done}/{total} ({status})", end="\r")
        else:
            results = data.get("results", [])
            print(f"  已完成: {len(results)} 个平台 ({status})", end="\r")
        time.sleep(interval)
        elapsed += interval
    print("\nWarning: Polling timeout, use 'search status' to check later", file=sys.stderr)
    return data


def format_search_result(data, use_json=False):
    """Format GEO search results for display."""
    if use_json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return

    question = data.get("question", "")
    brand = data.get("brand", "")
    status = data.get("status", "")
    print(f"问题: {question}")
    print(f"品牌: {brand}")
    print(f"状态: {status}")

    results = data.get("results", [])
    if not results:
        print("暂无结果")
        return

    mentioned = sum(1 for r in results if r.get("brand_mentioned"))
    print(f"品牌提及: {mentioned}/{len(results)} 个平台\n")

    for r in results:
        platform = r.get("platform", "unknown")
        bm = "✓ 提及" if r.get("brand_mentioned") else "✗ 未提及"
        rank = r.get("brand_rank", 0)
        sentiment = r.get("sentiment", "N/A")
        print(f"【{platform}】{bm}  排名: {rank or '-'}  情感: {sentiment}")

        citations = r.get("citations", [])
        if citations:
            print(f"  引用来源 ({len(citations)}):")
            for c in citations[:5]:
                print(f"    [{c.get('position', '?')}] {c.get('title', '')} — {c.get('domain', '')}")

        answer = r.get("answer", "")
        if answer:
            preview = answer[:150].replace("\n", " ")
            print(f"  回答: {preview}...")
        print()


def cmd_search(args):
    pid = resolve_product_id(args)

    if args.action == "create":
        if not args.question:
            print("Error: --question required", file=sys.stderr); sys.exit(1)
        body = {
            "question": args.question,
            "brand": args.brand or "",
            "mode": args.mode or "api",
        }
        if args.platforms:
            body["platforms"] = [p.strip() for p in args.platforms.split(",")]
        data = api_request("POST", "/api/v1/geo-search/task", body, product_id=pid)
        task_id = data.get("task_id", "")
        print(f"搜索任务已创建: {task_id}")

        if not args.no_wait:
            print("等待搜索完成...")
            result = poll_task(task_id, pid)
            print()
            format_search_result(result, args.json)
        else:
            print(f"使用 'search status --task-id {task_id}' 查看结果")

    elif args.action == "batch":
        if not args.question_ids:
            print("Error: --question-ids required (comma-separated)", file=sys.stderr); sys.exit(1)
        ids = [int(x.strip()) for x in args.question_ids.split(",")]
        body = {"question_ids": ids}
        if args.platforms:
            body["platforms"] = [p.strip() for p in args.platforms.split(",")]
        data = api_request("POST", "/api/v1/geo-search/batch", body, product_id=pid)
        batch_id = data.get("batch_id", "")
        print(f"批量任务已创建: {batch_id}")

        if not args.no_wait:
            print("等待批量搜索完成...")
            result = poll_task(batch_id, pid, is_batch=True)
            print()
            if fmt_json(result, args.json):
                return
            total = result.get("total_tasks", 0)
            done = result.get("completed_tasks", 0)
            print(f"批量任务完成: {done}/{total}")
            tasks = result.get("tasks", [])
            for t in tasks:
                bm = "✓" if any(r.get("brand_mentioned") for r in t.get("results", [])) else "✗"
                print(f"  [{t.get('task_id', '?')[:8]}] {bm} {t.get('question', '')}")
        else:
            print(f"使用 'search batch-status --batch-id {batch_id}' 查看进度")

    elif args.action == "status":
        if not args.task_id:
            print("Error: --task-id required", file=sys.stderr); sys.exit(1)
        data = api_request("GET", f"/api/v1/geo-search/task/{args.task_id}",
                           product_id=pid)
        format_search_result(data, args.json)

    elif args.action == "batch-status":
        if not args.batch_id:
            print("Error: --batch-id required", file=sys.stderr); sys.exit(1)
        data = api_request("GET", f"/api/v1/geo-search/batch/{args.batch_id}",
                           product_id=pid)
        if fmt_json(data, args.json):
            return
        total = data.get("total_tasks", 0)
        done = data.get("completed_tasks", 0)
        status = data.get("status", "unknown")
        print(f"批量任务: {status}  进度: {done}/{total}")
        tasks = data.get("tasks", [])
        for t in tasks:
            print(f"  [{t.get('task_id', '?')[:8]}] {t.get('status', '?')} — {t.get('question', '')}")

    elif args.action == "history":
        query = {}
        if args.page: query["page"] = args.page
        if args.size: query["size"] = args.size
        data = api_request("GET", "/api/v1/geo-search/history",
                           product_id=pid, query=query)
        if fmt_json(data, args.json):
            return
        records = data if isinstance(data, list) else data.get("list", [])
        if not records:
            print("暂无搜索历史")
            return
        for r in records:
            tid = r.get("task_id", "")[:8]
            q = r.get("question", "")
            s = r.get("status", "")
            print(f"  [{tid}] {s} — {q}")


# ---------------------------------------------------------------------------
# Commands: articles
# ---------------------------------------------------------------------------


def cmd_articles(args):
    pid = resolve_product_id(args)

    if args.action == "generate":
        if not args.question_id:
            print("Error: --question-id required", file=sys.stderr); sys.exit(1)
        body = {"question_id": int(args.question_id)}
        if args.instruction:
            body["instruction"] = args.instruction
        if args.image_ids:
            body["image_ids"] = [int(x.strip()) for x in args.image_ids.split(",")]
        data = api_request("POST", "/api/v1/articles/generate", body, product_id=pid)
        if fmt_json(data, args.json):
            return
        print(f"文章生成成功: [{data.get('id', '?')}] {data.get('title', '')}")
        content = data.get("content", "")
        if content:
            preview = content[:300].replace("\n", "\n  ")
            print(f"\n  {preview}...")

    elif args.action == "list":
        query = {}
        if args.question_id:
            query["question_id"] = args.question_id
        data = api_request("GET", "/api/v1/articles", product_id=pid, query=query)
        if fmt_json(data, args.json):
            return
        if not data:
            print("暂无文章")
            return
        for a in data:
            status = a.get("status", "draft")
            print(f"[{a['id']}] ({status}) {a.get('title', 'Untitled')}")

    elif args.action == "get":
        if not args.id:
            print("Error: --id required", file=sys.stderr); sys.exit(1)
        data = api_request("GET", f"/api/v1/articles/{args.id}", product_id=pid)
        if fmt_json(data, args.json):
            return
        article = data.get("article", data)
        print(f"标题: {article.get('title', '')}")
        print(f"状态: {article.get('status', '')}")
        print(f"\n{article.get('content', '')}")

    elif args.action == "update":
        if not args.id:
            print("Error: --id required", file=sys.stderr); sys.exit(1)
        body = {}
        if args.title: body["title"] = args.title
        if args.content: body["content"] = args.content
        if args.status: body["status"] = args.status
        api_request("PUT", f"/api/v1/articles/{args.id}", body, product_id=pid)
        print("文章更新成功")

    elif args.action == "delete":
        if not args.id:
            print("Error: --id required", file=sys.stderr); sys.exit(1)
        api_request("DELETE", f"/api/v1/articles/{args.id}", product_id=pid)
        print(f"文章 {args.id} 已删除")


# ---------------------------------------------------------------------------
# Commands: publish / platforms / ai-platforms
# ---------------------------------------------------------------------------


def cmd_publish(args):
    pid = resolve_product_id(args)

    if args.action == "record":
        if not args.article_id or not args.platform_id:
            print("Error: --article-id and --platform-id required", file=sys.stderr); sys.exit(1)
        body = {
            "article_id": int(args.article_id),
            "platform_id": int(args.platform_id),
        }
        if args.platform_name:
            body["platform"] = args.platform_name
        api_request("POST", "/api/v1/publish", body, product_id=pid)
        print("发布记录已保存")

    elif args.action == "list":
        query = {}
        if args.article_id:
            query["article_id"] = args.article_id
        data = api_request("GET", "/api/v1/publish/records", product_id=pid, query=query)
        if fmt_json(data, args.json):
            return
        if not data:
            print("暂无发布记录")
            return
        for r in data:
            print(f"[{r.get('id', '?')}] 文章{r.get('article_id', '?')} → {r.get('platform', '?')}")


def cmd_platforms(args):
    data = api_request("GET", "/api/v1/platforms")
    if fmt_json(data, args.json):
        return
    if not data:
        print("暂无平台")
        return
    for p in data:
        ptype = "预设" if p.get("type") == "preset" else "自定义"
        print(f"[{p['id']}] {p['name']} ({ptype}) — {p.get('url', '')}")


def cmd_ai_platforms(args):
    data = api_request("GET", "/api/v1/ai-platforms")
    if fmt_json(data, args.json):
        return
    if not data:
        print("暂无 AI 平台")
        return
    for p in data:
        color = p.get("color", "")
        print(f"[{p['id']}] {p['name']}  {color}")


def cmd_sentiment(args):
    data = api_request("GET", "/api/v1/sentiment/status")
    if fmt_json(data, args.json):
        return
    enabled = data.get("enabled", False)
    status = "已开启" if enabled else "未开启"
    print(f"情感分析: {status}")


# ---------------------------------------------------------------------------
# Commands: drafts (question drafts v2 — async + history)
# ---------------------------------------------------------------------------


def cmd_drafts(args):
    pid = resolve_product_id(args)

    if args.action == "generate":
        if not args.keywords:
            print("Error: --keywords required", file=sys.stderr); sys.exit(1)
        body = {"keywords": args.keywords}
        data = api_request("POST", "/api/v1/question-drafts/generate", body, product_id=pid)
        if fmt_json(data, args.json):
            return
        print(f"草稿生成任务已创建: [{data.get('id', '?')}] 状态: {data.get('status', '?')}")
        draft_id = data.get("id")
        if draft_id and not args.no_wait:
            print("等待生成完成...")
            interval, timeout = get_poll_settings()
            elapsed = 0
            while elapsed < timeout:
                time.sleep(interval)
                elapsed += interval
                detail = api_request("GET", f"/api/v1/question-drafts/detail/{draft_id}",
                                     product_id=pid)
                status = detail.get("status", "unknown")
                if status == "completed":
                    print("生成完成!")
                    _print_draft_detail(detail, args.json)
                    return
                if status == "failed":
                    print(f"Error: 生成失败 — {detail.get('error_msg', 'unknown')}", file=sys.stderr)
                    sys.exit(1)
                print(f"  状态: {status}...", end="\r")
            print("\nWarning: 轮询超时，使用 'drafts get --id <id>' 查看结果", file=sys.stderr)

    elif args.action == "list":
        query = {}
        if args.page: query["page"] = args.page
        if args.page_size: query["page_size"] = args.page_size
        data = api_request("GET", "/api/v1/question-drafts", product_id=pid, query=query)
        if fmt_json(data, args.json):
            return
        items = data.get("list", []) if isinstance(data, dict) else data
        if not items:
            print("暂无问题草稿")
            return
        total = data.get("total", len(items)) if isinstance(data, dict) else len(items)
        print(f"共 {total} 条记录:\n")
        for d in items:
            qcount = d.get("question_count", 0)
            print(f"[{d['id']}] ({d.get('status', '?')}) 关键词: {d.get('keywords', '')}  问题数: {qcount}  {d.get('created_at', '')}")

    elif args.action == "latest":
        data = api_request("GET", "/api/v1/question-drafts/latest", product_id=pid)
        if data is None:
            print("暂无草稿")
            return
        _print_draft_detail(data, args.json)

    elif args.action == "get":
        if not args.id:
            print("Error: --id required", file=sys.stderr); sys.exit(1)
        data = api_request("GET", f"/api/v1/question-drafts/detail/{args.id}",
                           product_id=pid)
        _print_draft_detail(data, args.json)

    elif args.action == "update":
        if not args.id:
            print("Error: --id required", file=sys.stderr); sys.exit(1)
        body = {}
        if args.keywords is not None: body["keywords"] = args.keywords
        if args.inquiry is not None: body["inquiry"] = args.inquiry
        if args.understanding is not None: body["understanding"] = args.understanding
        if args.consideration is not None: body["consideration"] = args.consideration
        if args.purchase is not None: body["purchase"] = args.purchase
        if not body:
            print("Error: at least one field required", file=sys.stderr); sys.exit(1)
        api_request("PUT", f"/api/v1/question-drafts/detail/{args.id}", body, product_id=pid)
        print("草稿更新成功")

    elif args.action == "delete":
        if not args.id:
            print("Error: --id required", file=sys.stderr); sys.exit(1)
        api_request("DELETE", f"/api/v1/question-drafts/detail/{args.id}", product_id=pid)
        print(f"草稿 {args.id} 已删除")


def _print_draft_detail(data, use_json=False):
    """Print draft detail."""
    if fmt_json(data, use_json):
        return
    print(f"ID:       {data.get('id', '?')}")
    print(f"关键词:   {data.get('keywords', '')}")
    print(f"状态:     {data.get('status', '')}")
    err = data.get("error_msg", "")
    if err:
        print(f"错误:     {err}")
    content = data.get("content")
    if content:
        stages = {"inquiry": "L1 认知", "understanding": "L2 探索",
                  "consideration": "L3 评估", "purchase": "L4 决策"}
        for key, label in stages.items():
            text = content.get(key, "")
            if text:
                print(f"\n{label}:")
                for line in text.split("\n"):
                    line = line.strip()
                    if line:
                        print(f"  {line}")
    print(f"\n创建: {data.get('created_at', '')}  更新: {data.get('updated_at', '')}")


# ---------------------------------------------------------------------------
# Commands: gallery (image categories + images)
# ---------------------------------------------------------------------------


def cmd_gallery(args):
    pid = resolve_product_id(args)

    if args.action == "categories-list":
        query = {}
        if args.scope: query["scope"] = args.scope
        data = api_request("GET", "/api/v1/gallery/categories", product_id=pid, query=query)
        if fmt_json(data, args.json):
            return
        if not data:
            print("暂无分类")
            return
        for c in data:
            default_tag = " (默认)" if c.get("is_default") else ""
            print(f"[{c['id']}] {c['name']}  scope: {c.get('scope', '')}  排序: {c.get('sort_order', 0)}{default_tag}")

    elif args.action == "categories-create":
        if not args.name:
            print("Error: --name required", file=sys.stderr); sys.exit(1)
        body = {
            "scope": args.scope or "product",
            "name": args.name,
        }
        data = api_request("POST", "/api/v1/gallery/categories", body, product_id=pid)
        if fmt_json(data, args.json):
            return
        print(f"分类创建成功: [{data.get('id', '?')}] {data.get('name', '')}")

    elif args.action == "categories-update":
        if not args.id:
            print("Error: --id required", file=sys.stderr); sys.exit(1)
        if not args.name:
            print("Error: --name required", file=sys.stderr); sys.exit(1)
        body = {"name": args.name}
        data = api_request("PUT", f"/api/v1/gallery/categories/{args.id}", body, product_id=pid)
        if fmt_json(data, args.json):
            return
        print("分类更新成功")

    elif args.action == "categories-delete":
        if not args.id:
            print("Error: --id required", file=sys.stderr); sys.exit(1)
        api_request("DELETE", f"/api/v1/gallery/categories/{args.id}", product_id=pid)
        print(f"分类 {args.id} 已删除")

    elif args.action == "images-list":
        query = {}
        if args.scope: query["scope"] = args.scope
        if args.category_id: query["category_id"] = args.category_id
        data = api_request("GET", "/api/v1/gallery/images", product_id=pid, query=query)
        if fmt_json(data, args.json):
            return
        if not data:
            print("暂无图片")
            return
        for img in data:
            size_kb = img.get("file_size", 0) / 1024
            print(f"[{img['id']}] {img.get('file_name', '')}  {size_kb:.1f}KB  分类: {img.get('category_id', '?')}  {img.get('file_path', '')}")

    elif args.action == "images-upload":
        if not args.file:
            print("Error: --file required (one or more file paths)", file=sys.stderr); sys.exit(1)
        if not args.category_id:
            print("Error: --category-id required", file=sys.stderr); sys.exit(1)
        # multipart upload
        import mimetypes
        key, base = get_config()
        url = f"{base}/api/v1/gallery/images"
        boundary = "----GEOUploadBoundary"
        body_parts = []
        # scope field
        scope = args.scope or "product"
        body_parts.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"scope\"\r\n\r\n{scope}")
        # category_id field
        body_parts.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"category_id\"\r\n\r\n{args.category_id}")
        # file fields
        for fpath in args.file:
            if not os.path.isfile(fpath):
                print(f"Error: file not found: {fpath}", file=sys.stderr); sys.exit(1)
            fname = os.path.basename(fpath)
            mime = mimetypes.guess_type(fpath)[0] or "application/octet-stream"
            with open(fpath, "rb") as f:
                file_data = f.read()
            body_parts.append(
                f"--{boundary}\r\nContent-Disposition: form-data; name=\"files\"; filename=\"{fname}\"\r\n"
                f"Content-Type: {mime}\r\n\r\n".encode("utf-8") + file_data
            )
        # build final body
        final_parts = []
        for part in body_parts:
            if isinstance(part, str):
                final_parts.append(part.encode("utf-8"))
            else:
                final_parts.append(part)
        closing = f"\r\n--{boundary}--\r\n".encode("utf-8")
        separator = b"\r\n"
        data_bytes = separator.join(final_parts) + closing

        headers = {
            "X-API-Key": key,
            "X-Product-ID": str(pid),
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "Accept": "application/json",
        }
        req = urllib.request.Request(url, data=data_bytes, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                result = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="replace")
            print(f"Error: HTTP {e.code} — {err_body}", file=sys.stderr)
            sys.exit(1)
        except urllib.error.URLError as e:
            print(f"Error: Connection failed — {e.reason}", file=sys.stderr)
            sys.exit(1)

        resp_data = result.get("data", result)
        if fmt_json(resp_data, args.json):
            return
        uploaded = resp_data.get("uploaded", [])
        errors_list = resp_data.get("errors", [])
        print(f"上传成功: {len(uploaded)} 张")
        for img in uploaded:
            print(f"  [{img.get('id', '?')}] {img.get('file_name', '')} — {img.get('file_path', '')}")
        if errors_list:
            print(f"上传失败: {len(errors_list)} 张")
            for e in errors_list:
                print(f"  {e}")

    elif args.action == "images-delete":
        if not args.id:
            print("Error: --id required", file=sys.stderr); sys.exit(1)
        api_request("DELETE", f"/api/v1/gallery/images/{args.id}", product_id=pid)
        print(f"图片 {args.id} 已删除")


# ---------------------------------------------------------------------------
# Argument parser
# ---------------------------------------------------------------------------


def build_parser():
    parser = argparse.ArgumentParser(
        prog="geo.py",
        description="极义GEO CLI — AI 搜索引擎优化平台",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # check
    sub.add_parser("check", help="检查连接和认证")

    # quota
    p = sub.add_parser("quota", help="查询额度")
    p.add_argument("--json", action="store_true")

    # products
    p = sub.add_parser("products", help="产品管理")
    p.add_argument("action", choices=["list", "create", "get", "update", "delete"])
    p.add_argument("--id", type=int)
    p.add_argument("--name")
    p.add_argument("--description")
    p.add_argument("--json", action="store_true")

    # company
    p = sub.add_parser("company", help="公司信息")
    p.add_argument("action", choices=["get", "save"])
    p.add_argument("--product-id", type=int)
    p.add_argument("--product-name")
    p.add_argument("--company-name")
    p.add_argument("--industry")
    p.add_argument("--business-scope")
    p.add_argument("--cities")
    p.add_argument("--contact-phone")
    p.add_argument("--website")
    p.add_argument("--editor-name")
    p.add_argument("--description")
    p.add_argument("--company-description")
    p.add_argument("--product-description")
    p.add_argument("--target-customer-type")
    p.add_argument("--customer-description")
    p.add_argument("--competitors")
    p.add_argument("--writing-style")
    p.add_argument("--json", action="store_true")

    # keywords
    p = sub.add_parser("keywords", help="核心词管理")
    p.add_argument("action", choices=["list", "add", "delete"])
    p.add_argument("--product-id", type=int)
    p.add_argument("--id", type=int)
    p.add_argument("--word")
    p.add_argument("--json", action="store_true")

    # questions
    p = sub.add_parser("questions", help="问题管理")
    p.add_argument("action", choices=["generate", "list", "toggle"])
    p.add_argument("--product-id", type=int)
    p.add_argument("--id", type=int)
    p.add_argument("--keyword-id", type=int)
    p.add_argument("--keywords", help="关键词文本，逗号分隔")
    p.add_argument("--json", action="store_true")

    # search
    p = sub.add_parser("search", help="GEO 搜索")
    p.add_argument("action", choices=["create", "batch", "status", "batch-status", "history"])
    p.add_argument("--product-id", type=int)
    p.add_argument("--question")
    p.add_argument("--brand")
    p.add_argument("--platforms")
    p.add_argument("--mode", default="api", choices=["api", "plugin"])
    p.add_argument("--task-id")
    p.add_argument("--batch-id")
    p.add_argument("--question-ids")
    p.add_argument("--no-wait", action="store_true", help="不等待结果")
    p.add_argument("--page", type=int)
    p.add_argument("--size", type=int)
    p.add_argument("--json", action="store_true")

    # articles
    p = sub.add_parser("articles", help="文章管理")
    p.add_argument("action", choices=["generate", "list", "get", "update", "delete"])
    p.add_argument("--product-id", type=int)
    p.add_argument("--id", type=int)
    p.add_argument("--question-id", type=int)
    p.add_argument("--instruction")
    p.add_argument("--image-ids")
    p.add_argument("--title")
    p.add_argument("--content")
    p.add_argument("--status", choices=["draft", "published"])
    p.add_argument("--json", action="store_true")

    # publish
    p = sub.add_parser("publish", help="发布记录")
    p.add_argument("action", choices=["record", "list"])
    p.add_argument("--product-id", type=int)
    p.add_argument("--article-id", type=int)
    p.add_argument("--platform-id", type=int)
    p.add_argument("--platform-name")
    p.add_argument("--json", action="store_true")

    # platforms
    p = sub.add_parser("platforms", help="自媒体平台列表")
    p.add_argument("--json", action="store_true")

    # ai-platforms
    p = sub.add_parser("ai-platforms", help="AI 搜索平台列表")
    p.add_argument("--json", action="store_true")

    # drafts (question drafts v2)
    p = sub.add_parser("drafts", help="问题草稿管理（新版）")
    p.add_argument("action", choices=["generate", "list", "latest", "get", "update", "delete"])
    p.add_argument("--product-id", type=int)
    p.add_argument("--id", type=int)
    p.add_argument("--keywords")
    p.add_argument("--inquiry")
    p.add_argument("--understanding")
    p.add_argument("--consideration")
    p.add_argument("--purchase")
    p.add_argument("--page", type=int)
    p.add_argument("--page-size", type=int)
    p.add_argument("--no-wait", action="store_true", help="不等待生成完成")
    p.add_argument("--json", action="store_true")

    # gallery
    p = sub.add_parser("gallery", help="图片素材库")
    p.add_argument("action", choices=[
        "categories-list", "categories-create", "categories-update", "categories-delete",
        "images-list", "images-upload", "images-delete",
    ])
    p.add_argument("--product-id", type=int)
    p.add_argument("--id", type=int)
    p.add_argument("--name")
    p.add_argument("--scope", choices=["public", "product"])
    p.add_argument("--category-id", type=int)
    p.add_argument("--file", nargs="+", help="上传文件路径（可多个）")
    p.add_argument("--json", action="store_true")

    # sentiment
    p = sub.add_parser("sentiment", help="情感分析状态")
    p.add_argument("--json", action="store_true")

    return parser


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

COMMAND_MAP = {
    "check": cmd_check,
    "quota": cmd_quota,
    "products": cmd_products,
    "company": cmd_company,
    "keywords": cmd_keywords,
    "questions": cmd_questions,
    "drafts": cmd_drafts,
    "gallery": cmd_gallery,
    "search": cmd_search,
    "articles": cmd_articles,
    "publish": cmd_publish,
    "platforms": cmd_platforms,
    "ai-platforms": cmd_ai_platforms,
    "sentiment": cmd_sentiment,
}


def main():
    parser = build_parser()
    args = parser.parse_args()
    handler = COMMAND_MAP.get(args.command)
    if handler:
        handler(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
