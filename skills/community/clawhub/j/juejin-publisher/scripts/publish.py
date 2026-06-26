#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
juejin-publisher: 发布 Markdown 文章到稀土掘金
Usage:
  python3 publish.py <markdown-file> [options]

Options:
  --category <id>     文章分类 ID（覆盖默认值）
  --tags <ids>        标签 ID，逗号分隔（覆盖默认值）
  --draft-only        仅创建草稿，不发布
  --help              显示帮助
"""

import sys
import os
import json
import re
import argparse
import urllib.request
import urllib.error

# 配置优先级说明：
#   1. 命令行参数 --cookie（最高优先级）
#   2. 环境变量 JUEJIN_COOKIE
#   3. juejin.env 配置文件（本地私有，不随 Skill 发布）

# ─── 颜色输出 ────────────────────────────────────────────────
RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[1;33m"
BLUE = "\033[0;34m"
NC = "\033[0m"

def log_info(msg):  print(f"{GREEN}✅ {msg}{NC}")
def log_warn(msg):  print(f"{YELLOW}⚠️  {msg}{NC}")
def log_error(msg): print(f"{RED}❌ {msg}{NC}")
def log_step(msg):  print(f"{BLUE}➡️  {msg}{NC}")

# ─── 路径配置 ────────────────────────────────────────────────
SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT  = os.path.dirname(SCRIPT_DIR)
CONFIG_FILE = os.path.join(SKILL_ROOT, "juejin.env")

# 掘金 API 基础 URL
API_BASE = "https://api.juejin.cn"

# 默认分类（后端）
DEFAULT_CATEGORY_ID = "6809637769959178254"
# 默认标签（Python）
DEFAULT_TAG_IDS = ["6809640408797167623"]

# ─── 配置加载 ────────────────────────────────────────────────
def load_config(cli_cookie=None):
    """
    按优先级加载配置：
      1. 命令行参数 --cookie（最高优先级）
      2. 环境变量 JUEJIN_COOKIE / JUEJIN_DEFAULT_CATEGORY_ID / JUEJIN_DEFAULT_TAG_IDS
      3. juejin.env 配置文件（本地私有，不随 Skill 包发布）
    """
    config = {}

    # 优先级 3：从 juejin.env 文件加载（最低优先级）
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("#") or "=" not in line:
                    continue
                line = line.removeprefix("export").strip()
                key, _, val = line.partition("=")
                val = val.strip().strip('"').strip("'")
                config[key.strip()] = val

    # 优先级 2：环境变量覆盖文件配置
    for env_key in ("JUEJIN_COOKIE", "JUEJIN_DEFAULT_CATEGORY_ID", "JUEJIN_DEFAULT_TAG_IDS"):
        env_val = os.environ.get(env_key, "")
        if env_val:
            config[env_key] = env_val

    # 优先级 1：命令行参数覆盖一切
    if cli_cookie:
        config["JUEJIN_COOKIE"] = cli_cookie

    # 验证必填项
    cookie = config.get("JUEJIN_COOKIE", "").strip()
    if not cookie or cookie in ("请填入你的掘金Cookie", "sessionid=your_session_id_here; ..."):
        log_error("未找到有效的掘金 Cookie，请通过以下任一方式配置：")
        print()
        print("  方式一（推荐）：环境变量")
        print("    export JUEJIN_COOKIE='你的Cookie'")
        print()
        print("  方式二：命令行参数")
        print("    python3 publish.py article.md --cookie '你的Cookie'")
        print()
        print("  方式三：配置文件（本地私有）")
        print(f"    cp {SKILL_ROOT}/juejin.env.example {CONFIG_FILE}")
        print(f"    # 然后编辑 {CONFIG_FILE}，填入 JUEJIN_COOKIE")
        print()
        print("  如何获取 Cookie：登录 juejin.cn → F12 → Network → 任意请求 → Request Headers → Cookie")
        sys.exit(1)

    return config

# ─── Markdown 解析 ───────────────────────────────────────────
def parse_markdown(filepath):
    """解析 Markdown 文件，提取 frontmatter 和正文"""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    meta = {}
    body = content

    # 提取 YAML frontmatter
    fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if fm_match:
        fm_text = fm_match.group(1)
        body = content[fm_match.end():]
        for line in fm_text.splitlines():
            if ":" in line:
                k, _, v = line.partition(":")
                meta[k.strip()] = v.strip().strip('"').strip("'")

    # 从正文提取标题（取第一个 # 标题）
    if "title" not in meta:
        title_match = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
        if title_match:
            meta["title"] = title_match.group(1).strip()
        else:
            meta["title"] = os.path.splitext(os.path.basename(filepath))[0]

    return meta, body.strip()

# ─── 摘要生成 ────────────────────────────────────────────────
def generate_brief(meta, body, min_len=50, max_len=100):
    """生成符合掘金要求的摘要（50-100字）"""
    if "description" in meta:
        brief = meta["description"]
        if min_len <= len(brief) <= max_len:
            return brief
        if len(brief) > max_len:
            return brief[:max_len]
        # 太短则补充正文内容
        plain = re.sub(r"[#*`>\[\]!]", "", body)
        plain = re.sub(r"\s+", " ", plain).strip()
        brief = (brief + " " + plain)[:max_len]
        return brief

    # 从正文生成摘要
    plain = re.sub(r"```.*?```", "", body, flags=re.DOTALL)
    plain = re.sub(r"[#*`>\[\]!]", "", plain)
    plain = re.sub(r"\s+", " ", plain).strip()
    if len(plain) < min_len:
        return plain + " " * (min_len - len(plain))
    return plain[:max_len]

# ─── HTTP 请求封装 ───────────────────────────────────────────
def api_post(path, data, cookie):
    """发送 POST 请求到掘金 API"""
    url = f"{API_BASE}{path}"
    payload = json.dumps(data).encode("utf-8")
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Cookie": cookie,
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Referer": "https://juejin.cn/",
        "Origin": "https://juejin.cn",
    }
    req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        log_error(f"HTTP {e.code}: {body}")
        sys.exit(1)
    except Exception as e:
        log_error(f"请求失败: {e}")
        sys.exit(1)

# ─── 掘金 API 操作 ───────────────────────────────────────────
def create_draft(title, content, brief, category_id, tag_ids, cover_image, cookie):
    """创建文章草稿，返回 draft_id"""
    log_step(f"创建草稿: {title}")
    data = {
        "category_id": category_id,
        "tag_ids": tag_ids,
        "link_url": "",
        "cover_image": cover_image,
        "title": title,
        "brief_content": brief,
        "edit_type": 10,          # 10 = Markdown 模式
        "html_content": "deprecated",
        "mark_content": content,
        "theme_ids": [],
    }
    resp = api_post("/content_api/v1/article_draft/create", data, cookie)
    if resp.get("err_no") != 0:
        log_error(f"创建草稿失败: {resp.get('err_msg', '未知错误')} (err_no={resp.get('err_no')})")
        sys.exit(1)
    draft_id = resp["data"]["id"]
    log_info(f"草稿创建成功，draft_id: {draft_id}")
    return draft_id

def publish_draft(draft_id, cookie):
    """发布草稿，返回文章 ID"""
    log_step(f"发布草稿: {draft_id}")
    data = {
        "draft_id": draft_id,
        "sync_to_org": False,
        "column_ids": [],
        "theme_ids": [],
    }
    resp = api_post("/content_api/v1/article/publish", data, cookie)
    if resp.get("err_no") != 0:
        log_error(f"发布失败: {resp.get('err_msg', '未知错误')} (err_no={resp.get('err_no')})")
        sys.exit(1)
    article_id = resp["data"]["article_id"]
    log_info(f"发布成功！文章 ID: {article_id}")
    return article_id

# ─── 主流程 ─────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="发布 Markdown 文章到稀土掘金",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 publish.py article.md
  python3 publish.py article.md --category 6809637767543259144
  python3 publish.py article.md --tags "6809640407484334093,6809640445233070094"
  python3 publish.py article.md --draft-only
        """
    )
    parser.add_argument("file", help="Markdown 文件路径")
    parser.add_argument("--cookie", help="掘金 Cookie（优先级高于环境变量和配置文件）")
    parser.add_argument("--category", help="文章分类 ID（覆盖默认值）")
    parser.add_argument("--tags", help="标签 ID，逗号分隔（覆盖默认值）")
    parser.add_argument("--draft-only", action="store_true", help="仅创建草稿，不发布")
    args = parser.parse_args()

    # 检查文件
    if not os.path.exists(args.file):
        log_error(f"文件不存在: {args.file}")
        sys.exit(1)

    # 加载配置（支持 --cookie 参数、环境变量、juejin.env 三种方式）
    config = load_config(cli_cookie=args.cookie)
    cookie = config["JUEJIN_COOKIE"]
    category_id = args.category or config.get("JUEJIN_DEFAULT_CATEGORY_ID", DEFAULT_CATEGORY_ID)
    if args.tags:
        tag_ids = [t.strip() for t in args.tags.split(",") if t.strip()]
    else:
        raw_tags = config.get("JUEJIN_DEFAULT_TAG_IDS", "")
        tag_ids = [t.strip() for t in raw_tags.split(",") if t.strip()] or DEFAULT_TAG_IDS

    # 解析 Markdown
    log_step(f"解析文件: {args.file}")
    meta, body = parse_markdown(args.file)
    title = meta.get("title", "无标题")
    cover_image = meta.get("cover", "")

    # 如果 frontmatter 有 category_id / tag_ids 则优先使用
    if "category_id" in meta and not args.category:
        category_id = meta["category_id"]
    if "tag_ids" in meta and not args.tags:
        tag_ids = [t.strip() for t in meta["tag_ids"].split(",") if t.strip()]

    # 生成摘要
    brief = generate_brief(meta, body)

    print()
    print(f"  📄 标题:   {title}")
    print(f"  📁 分类:   {category_id}")
    print(f"  🏷️  标签:   {', '.join(tag_ids)}")
    print(f"  📝 摘要:   {brief[:40]}..." if len(brief) > 40 else f"  📝 摘要:   {brief}")
    print(f"  🖼️  封面:   {cover_image or '（无）'}")
    print()

    # 创建草稿
    draft_id = create_draft(title, body, brief, category_id, tag_ids, cover_image, cookie)

    if args.draft_only:
        log_info("已创建草稿（--draft-only 模式，未发布）")
        print(f"\n  草稿地址: https://juejin.cn/editor/drafts/{draft_id}")
        return

    # 发布
    article_id = publish_draft(draft_id, cookie)
    print(f"\n  🎉 文章已发布: https://juejin.cn/post/{article_id}")

if __name__ == "__main__":
    main()
