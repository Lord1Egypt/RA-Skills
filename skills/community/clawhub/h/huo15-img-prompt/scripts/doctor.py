#!/usr/bin/env python3
"""
huo15-img-prompt — 健康检查 v3.1

一键诊断技能能不能正常用：
  - 14 个脚本能不能 import / 拿到 VERSION
  - API keys 配置情况（ANTHROPIC / OPENAI / REPLICATE / FAL / ARK / KLING / MINIMAX）
  - 后端服务可达性（ComfyUI / SD WebUI）
  - Obsidian vault 检测
  - 持久化资产盘点（characters / sessions / brand_kits / learned_presets）
  - Claude API 实际可调测试（轻量 ping）

调用：
  doctor.py                # 全量检查
  doctor.py --quick         # 跳过网络测试
  doctor.py --check api     # 只查 API keys
  doctor.py -j              # JSON 输出
"""

import sys
import os
import json
import argparse
import socket
from typing import Dict, List, Optional
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

VERSION = "3.1.0"

GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
GRAY = "\033[90m"
RESET = "\033[0m"
BOLD = "\033[1m"


def ok(msg: str) -> str:
    return f"{GREEN}✓{RESET} {msg}"


def warn(msg: str) -> str:
    return f"{YELLOW}⚠{RESET} {msg}"


def fail(msg: str) -> str:
    return f"{RED}✗{RESET} {msg}"


def info(msg: str) -> str:
    return f"{GRAY}·{RESET} {msg}"


# ─────────────────────────────────────────────────────────
# 检查项
# ─────────────────────────────────────────────────────────
SCRIPTS = [
    "enhance_prompt", "enhance_video", "reverse_prompt", "render_prompt",
    "claude_polish", "safety_lint", "image_review", "auto_iterate",
    "character", "mcp_server", "web_ui",
    "storyboard", "brand_kit", "style_learn",
]


def check_scripts() -> Dict:
    """检查 14 个脚本能不能 import + 拿到 VERSION。"""
    out = {"category": "scripts", "items": []}
    base_dir = os.path.dirname(os.path.abspath(__file__))
    for s in SCRIPTS:
        path = os.path.join(base_dir, f"{s}.py")
        item = {"name": s, "path": path}
        if not os.path.isfile(path):
            item["status"] = "missing"
            item["msg"] = "脚本不存在"
        else:
            try:
                mod = __import__(s)
                v = getattr(mod, "VERSION", None)
                if v:
                    item["status"] = "ok"
                    item["version"] = v
                else:
                    item["status"] = "warn"
                    item["msg"] = "缺 VERSION 常量"
            except Exception as e:
                item["status"] = "fail"
                item["msg"] = str(e)
        out["items"].append(item)
    return out


API_KEYS = [
    ("ANTHROPIC_API_KEY", "Claude API（润色/评审/闭环迭代/故事板）", True),
    ("OPENAI_API_KEY", "DALL-E 3 直出", False),
    ("REPLICATE_API_TOKEN", "Replicate 后端", False),
    ("FAL_KEY", "Fal.ai 后端", False),
    ("ARK_API_KEY", "字节即梦（火山方舟）", False),
    ("KLING_API_KEY", "快手可灵", False),
    ("MINIMAX_API_KEY", "海螺 MiniMax", False),
]


def check_api_keys() -> Dict:
    out = {"category": "api_keys", "items": []}
    for env, desc, required in API_KEYS:
        item = {"env": env, "desc": desc, "required": required}
        val = os.environ.get(env, "")
        if val:
            item["status"] = "ok"
            item["msg"] = f"已配置（{val[:8]}...）"
        else:
            item["status"] = "fail" if required else "warn"
            item["msg"] = "未设置" + ("（必填）" if required else "（可选，按需配）")
        out["items"].append(item)
    return out


SERVICES = [
    ("ComfyUI", os.environ.get("COMFYUI_URL", "http://127.0.0.1:8188"), "/system_stats"),
    ("SD WebUI", os.environ.get("SDWEBUI_URL", "http://127.0.0.1:7860"), "/sdapi/v1/options"),
]


def check_services(skip_network: bool = False) -> Dict:
    out = {"category": "local_services", "items": []}
    if skip_network:
        out["skipped"] = True
        return out
    for name, url, probe_path in SERVICES:
        item = {"name": name, "url": url}
        try:
            from urllib.parse import urljoin
            full = urljoin(url, probe_path)
            req = Request(full)
            with urlopen(req, timeout=2) as r:
                item["status"] = "ok"
                item["msg"] = f"{r.status} {r.reason}"
        except (HTTPError, URLError, socket.timeout, ConnectionResetError, OSError) as e:
            item["status"] = "warn"
            item["msg"] = f"未启动或不可达（按需启）"
        out["items"].append(item)
    return out


def check_obsidian() -> Dict:
    out = {"category": "obsidian", "items": []}
    candidates = [
        ("$OBSIDIAN_VAULT", os.environ.get("OBSIDIAN_VAULT", "")),
        ("~/knowledge/huo15", os.path.expanduser("~/knowledge/huo15")),
        ("~/Documents/Obsidian", os.path.expanduser("~/Documents/Obsidian")),
        ("~/Obsidian", os.path.expanduser("~/Obsidian")),
    ]
    found_any = False
    for label, path in candidates:
        item = {"label": label, "path": path or "(未设置)"}
        if path and os.path.isdir(path):
            item["status"] = "ok"
            item["msg"] = "存在"
            found_any = True
        else:
            item["status"] = "info"
            item["msg"] = "不存在或未设置"
        out["items"].append(item)
    out["any_vault_found"] = found_any
    return out


PERSIST_DIRS = [
    ("characters", "~/.huo15/characters", "角色卡"),
    ("sessions", "~/.huo15/sessions", "session（多轮编辑）"),
    ("brand_kits", "~/.huo15/brand_kits", "品牌套件"),
    ("learned_presets", "~/.huo15/learned_presets", "风格学习预设"),
]


def check_persisted() -> Dict:
    out = {"category": "persisted_assets", "items": []}
    for key, path, label in PERSIST_DIRS:
        full = os.path.expanduser(path)
        item = {"key": key, "path": full, "label": label}
        if os.path.isdir(full):
            files = [f for f in os.listdir(full) if f.endswith(".json")]
            item["status"] = "ok" if files else "info"
            item["count"] = len(files)
            item["msg"] = f"{len(files)} 个" if files else "暂无"
            item["names"] = [f[:-5] for f in sorted(files)[:10]]
        else:
            item["status"] = "info"
            item["msg"] = "目录不存在（首次使用时自动创建）"
            item["count"] = 0
        out["items"].append(item)
    return out


def check_anthropic_ping(skip_network: bool = False) -> Dict:
    """轻量调一次 Claude API（最便宜的 haiku，单 token）验证 key 有效。"""
    out = {"category": "anthropic_ping"}
    if skip_network:
        out["status"] = "skipped"
        return out
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        out["status"] = "warn"
        out["msg"] = "未设置 ANTHROPIC_API_KEY"
        return out

    try:
        body = {
            "model": "claude-haiku-4-5",
            "max_tokens": 10,
            "messages": [{"role": "user", "content": "ping"}],
        }
        req = Request(
            "https://api.anthropic.com/v1/messages",
            data=json.dumps(body).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
            },
            method="POST",
        )
        with urlopen(req, timeout=15) as r:
            resp = json.loads(r.read().decode("utf-8"))
        if "content" in resp:
            out["status"] = "ok"
            out["msg"] = f"模型 {resp.get('model', '?')} 响应正常"
            out["usage"] = resp.get("usage", {})
        else:
            out["status"] = "fail"
            out["msg"] = f"响应异常: {resp}"
    except HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")[:200]
        out["status"] = "fail"
        out["msg"] = f"HTTP {e.code}: {body}"
    except Exception as e:
        out["status"] = "fail"
        out["msg"] = f"调用失败: {e}"
    return out


# ─────────────────────────────────────────────────────────
# 输出
# ─────────────────────────────────────────────────────────
def print_section(title: str, data: Dict):
    print(f"\n{BOLD}{title}{RESET}")
    print("─" * 60)
    if data.get("skipped"):
        print(info("已跳过（--quick）"))
        return

    if "items" not in data:
        # 单项结果
        status = data.get("status", "info")
        msg = data.get("msg", "")
        line_fn = {"ok": ok, "warn": warn, "fail": fail, "skipped": info}.get(status, info)
        print(line_fn(msg))
        if data.get("usage"):
            u = data["usage"]
            print(info(f"  in={u.get('input_tokens', 0)} / out={u.get('output_tokens', 0)} tokens"))
        return

    for item in data["items"]:
        status = item.get("status", "info")
        line_fn = {"ok": ok, "warn": warn, "fail": fail, "missing": fail, "info": info}.get(status, info)
        if data["category"] == "scripts":
            label = f"{item['name']:18s} v{item.get('version', '?')}"
            if status != "ok":
                label += f" — {item.get('msg', '')}"
            print(line_fn(label))
        elif data["category"] == "api_keys":
            label = f"{item['env']:25s} {item.get('msg', '')}  {GRAY}({item['desc']}){RESET}"
            print(line_fn(label))
        elif data["category"] == "local_services":
            print(line_fn(f"{item['name']:12s} {item['url']:38s} {item.get('msg', '')}"))
        elif data["category"] == "obsidian":
            print(line_fn(f"{item['label']:30s} {item.get('msg', '')}"))
        elif data["category"] == "persisted_assets":
            line = f"{item['label']:18s} {item.get('msg', ''):8s}"
            if item.get("names"):
                line += f"  {GRAY}({', '.join(item['names'][:5])}){RESET}"
            print(line_fn(line))


def collect_summary(checks: List[Dict]) -> Dict:
    """统计 ok / warn / fail 总数。"""
    counts = {"ok": 0, "warn": 0, "fail": 0, "info": 0}
    for c in checks:
        if c.get("skipped"):
            continue
        if "items" in c:
            for item in c["items"]:
                s = item.get("status", "info")
                counts[s if s in counts else "info"] = counts.get(s, 0) + 1
        else:
            s = c.get("status", "info")
            if s in counts:
                counts[s] += 1
    return counts


def main():
    parser = argparse.ArgumentParser(
        description=f"huo15-img-prompt doctor v{VERSION} — 健康检查",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  doctor.py                       # 全量检查
  doctor.py --quick                # 跳过网络测试
  doctor.py --check api            # 只查 API keys
  doctor.py --check scripts        # 只查脚本
  doctor.py -j                     # JSON 输出
""",
    )
    parser.add_argument("--quick", action="store_true", help="跳过网络测试（service/anthropic_ping）")
    parser.add_argument("--check", choices=["scripts", "api", "services", "obsidian", "persisted", "ping"],
                        help="只跑指定项")
    parser.add_argument("-j", "--json", action="store_true", help="JSON 输出")
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s v{VERSION}")
    args = parser.parse_args()

    runners = {
        "scripts": ("脚本完整性", check_scripts, []),
        "api": ("API Keys", check_api_keys, []),
        "services": ("本地后端服务", check_services, [args.quick]),
        "obsidian": ("Obsidian Vault", check_obsidian, []),
        "persisted": ("持久化资产", check_persisted, []),
        "ping": ("Claude API 实测", check_anthropic_ping, [args.quick]),
    }

    if args.check:
        keys = [args.check]
    else:
        keys = list(runners.keys())

    results = {}
    for k in keys:
        title, fn, fn_args = runners[k]
        results[k] = fn(*fn_args)
        results[k]["_title"] = title

    if args.json:
        print(json.dumps({"version": VERSION, "results": results}, ensure_ascii=False, indent=2))
        return

    print(f"\n{BOLD}🩺 huo15-img-prompt doctor v{VERSION}{RESET}")

    for k in keys:
        print_section(results[k]["_title"], results[k])

    counts = collect_summary(list(results.values()))
    total = sum(counts.values())
    print(f"\n{BOLD}总结{RESET}")
    print("─" * 60)
    print(f"  {GREEN}✓ {counts['ok']}{RESET}  {YELLOW}⚠ {counts['warn']}{RESET}  {RED}✗ {counts['fail']}{RESET}  {GRAY}· {counts['info']}{RESET}  / {total}")

    if counts["fail"] > 0:
        print(f"\n{RED}有 {counts['fail']} 个失败项。修复建议见上方 ✗ 标记。{RESET}\n")
        sys.exit(1)
    elif counts["warn"] > 0:
        print(f"\n{YELLOW}部分功能受限（warn），按需配置。{RESET}\n")
    else:
        print(f"\n{GREEN}全部正常 🎉{RESET}\n")


if __name__ == "__main__":
    main()
