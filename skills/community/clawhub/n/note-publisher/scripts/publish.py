#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图文笔记发布脚本（note-publisher skill）

从 markdown 文案解析 title / content / tags / images，
通过用户配置的 MCP 发布后端（Streamable HTTP）发布，并回查 note_id。

用法：
  python3 publish.py check                     # 检查 MCP 服务 + 登录状态
  python3 publish.py <笔记.md> [--title 标题]  # 发布单篇（缺省用 md 第一行 # 标题）
  python3 publish.py --dir <目录>              # 批量发布目录下所有 .md（按文件名排序）

markdown 格式约定：
  # 标题（≤20 字，会做长度校验）
  正文……（可带 emoji）
  #话题1 #话题2 #话题3        ← 这行会被解析为 tags
  ---                        ← 分隔线（可选）
  ## 配图（可选，表格列出任意 .jpg/.png 路径，相对路径相对于 md 所在目录，自动按顺序提取）

后端地址配置（二选一，缺省报错）：
  1. 环境变量 MCP_PUBLISHER_URL
  2. 本 skill 目录下的 config.json：{ "mcp_url": "http://localhost:18060/mcp" }
"""
import json
import subprocess
import re
import sys
import os
import time
import argparse

TITLE_MAX = 20  # 图文笔记标题上限（字符）

CONFIG_HINT = (
    "未配置 MCP 发布后端地址。\n"
    "本 skill 是通用发布框架，不自带任何平台的发布能力。\n"
    "请二选一配置后再运行：\n"
    "  1) 环境变量：export MCP_PUBLISHER_URL=\"http://localhost:18060/mcp\"\n"
    "  2) 在 skill 目录放 config.json：{ \"mcp_url\": \"http://localhost:18060/mcp\" }\n"
)


def _load_mcp_url():
    """读取后端地址：优先环境变量，其次 skill 目录下的 config.json。"""
    env_url = os.environ.get("MCP_PUBLISHER_URL", "").strip()
    if env_url:
        return env_url
    cfg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "config.json")
    try:
        with open(cfg_path, encoding="utf-8") as f:
            url = json.load(f).get("mcp_url", "")
            if url and str(url).strip():
                return str(url).strip()
    except Exception:
        pass
    return ""


MCP_URL = _load_mcp_url()


# ---------- MCP 调用封装 ----------
def curl(payload, session=None, timeout=300):
    """发一个 MCP JSON-RPC 请求，返回响应体字符串。"""
    cmd = [
        "curl", "--noproxy", "*", "-s", "--max-time", str(timeout),
        "-X", "POST", MCP_URL,
        "-H", "Content-Type: application/json",
    ]
    if session:
        cmd += ["-H", "Mcp-Session-Id: {}".format(session)]
    cmd += ["-d", json.dumps(payload, ensure_ascii=False)]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 30)
    return p.stdout


def mcp_call(tool, args, timeout=300):
    """完整 MCP 调用：initialize → initialized 通知 → tools/call。返回 (status, text)。"""
    init_payload = {
        "jsonrpc": "2.0", "id": 1, "method": "initialize",
        "params": {"protocolVersion": "2024-11-05", "capabilities": {},
                   "clientInfo": {"name": "note-publisher", "version": "1.0"}},
    }
    cmd = [
        "curl", "--noproxy", "*", "-s", "-i", "--max-time", "30",
        "-X", "POST", MCP_URL, "-H", "Content-Type: application/json",
        "-d", json.dumps(init_payload),
    ]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    sid = ""
    for line in p.stdout.splitlines():
        if line.lower().startswith("mcp-session-id:"):
            sid = line.split(":", 1)[1].strip()
    if not sid:
        return ("ERROR", "无法获取 MCP Session ID，请确认后端 MCP 服务已启动，且 MCP_PUBLISHER_URL 配置正确（当前: {}）".format(MCP_URL))

    curl({"jsonrpc": "2.0", "method": "notifications/initialized"}, session=sid, timeout=30)

    raw = curl({"jsonrpc": "2.0", "id": 2, "method": "tools/call",
                "params": {"name": tool, "arguments": args}}, session=sid, timeout=timeout)
    return result_text(raw)


def result_text(raw):
    try:
        d = json.loads(raw)
        if d.get("error"):
            return ("ERROR", json.dumps(d["error"], ensure_ascii=False))
        for c in d.get("result", {}).get("content", []):
            if c.get("type") == "text":
                return ("OK", c["text"])
        return ("RAW", raw[:500])
    except Exception:
        return ("RAW", raw[:500])


# ---------- markdown 解析 ----------
def parse_md(path):
    """解析 markdown，返回 (title, content, tags, images)。"""
    with open(path, encoding="utf-8") as f:
        text = f.read()
    lines = text.split("\n")

    title = None
    content_lines, started = [], False
    for ln in lines:
        if not started:
            if ln.startswith("# "):
                title = ln[2:].strip()
                started = True
            continue
        if ln.strip() == "---":
            break
        content_lines.append(ln)
    content = "\n".join(content_lines).strip()

    tags = []
    for ln in content_lines:
        for m in re.findall(r"#([\u4e00-\u9fa5A-Za-z0-9]+)", ln):
            tags.append(m)
    seen = set()
    tags = [t for t in tags if not (t in seen or seen.add(t))]

    base = os.path.dirname(os.path.abspath(path))
    images = []
    # 关键：精确匹配到扩展名，避免吞掉全角括号尺寸注释「（1920×1280）」
    # 支持相对路径（相对 md 所在目录）与绝对路径
    for ln in lines:
        m = re.search(r"[\w\-./~]+\.(?:jpg|png|jpeg|webp)", ln)
        if m:
            p = m.group(0)
            if p.startswith("/") or p.startswith("~"):
                images.append(os.path.expanduser(p))
            else:
                images.append(os.path.join(base, p))
    seen2 = set()
    images = [p for p in images if not (p in seen2 or seen2.add(p))]
    return title, content, tags, images


# ---------- 业务 ----------
def _require_config():
    """未配置后端地址则报错退出。"""
    if not MCP_URL:
        print(CONFIG_HINT)
        sys.exit(1)


def check():
    """检查 MCP 服务与登录状态。"""
    _require_config()
    print("MCP 端点:", MCP_URL)
    status, text = mcp_call("check_login_status", {}, timeout=60)
    print("登录状态:", text.strip())


def publish(md_path, title_override=None):
    _require_config()
    title, content, tags, images = parse_md(md_path)
    if title_override:
        title = title_override
    if not title:
        print("错误：无法从 markdown 提取标题（需第一行 `# 标题`），或用 --title 指定")
        return None
    if len(title) > TITLE_MAX:
        print("警告：标题 {} 字，超过 {} 字上限，请缩短".format(len(title), TITLE_MAX))
    if not images:
        print("警告：未解析到配图，图文笔记至少需要 1 张图")

    print("=" * 60)
    print("发布: {} | 图片 {} 张 | 话题 {}".format(title, len(images), tags))
    status, text = mcp_call("publish_content", {
        "title": title, "content": content, "images": images, "tags": tags,
    }, timeout=300)
    print("结果:", text[:400])

    # 回查 note_id
    if "成功" in text:
        note_id = fetch_note_id(title)
        if note_id:
            print("NOTE_ID:", note_id)
            return note_id
    return None


def fetch_note_id(title):
    """通过 get_my_profile 拿最近发布的笔记 id（按标题匹配）。"""
    status, text = mcp_call("get_my_profile", {}, timeout=60)
    try:
        obj = json.loads(text)
        feeds = obj.get("feeds", [])
        for f in feeds:
            if f.get("noteCard", {}).get("displayTitle", "") == title:
                return f.get("id")
        # 兜底：返回最新一条
        if feeds:
            return feeds[0].get("id")
    except Exception:
        pass
    return None


def main():
    ap = argparse.ArgumentParser(description="图文笔记发布")
    ap.add_argument("md", nargs="?", help="markdown 文件路径")
    ap.add_argument("--title", "-t", help="标题覆盖（缺省用 md 第一行 # 标题）")
    ap.add_argument("--dir", "-d", help="批量发布目录下所有 .md")
    ap.add_argument("--check", action="store_true", help="检查登录状态")
    args = ap.parse_args()

    if args.check or args.md == "check":
        check()
        return

    if args.dir:
        files = sorted(f for f in os.listdir(args.dir) if f.endswith(".md"))
        if not files:
            print("目录下没有 .md 文件:", args.dir)
            return
        print("批量发布 {} 篇".format(len(files)))
        for f in files:
            publish(os.path.join(args.dir, f))
            time.sleep(3)  # 两篇之间稍作间隔
        return

    if args.md:
        publish(args.md, args.title)
        return

    ap.print_help()


if __name__ == "__main__":
    main()
