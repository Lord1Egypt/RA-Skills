#!/usr/bin/env python3
"""
scan_hooks.py — 枚举 Claude Code 中所有【真正生效】的 hook，并标注来源可信度。

关键点：hooks.json 存在 != 生效。必须区分：
  - 用户 settings.json / settings.local.json  → 生效（你自己配的）
  - skills/<name>/hooks/hooks.json            → 生效（skill 自带，装了就常驻）
  - plugins/cache/<mkt>/<plugin>/...          → 仅当 enabledPlugins 为 true 才生效
  - plugins/marketplaces/**                   → 仓库缓存，永不生效（最易误判）

用法:
    python scan_hooks.py              # 人类可读报告
    python scan_hooks.py --json       # 机器可读
"""
import json
import os
import sys
from pathlib import Path

HOME = Path(os.path.expanduser("~"))
CLAUDE = HOME / ".claude"

# 每轮对话都会跑的事件 = token/延迟成本最高
PER_TURN = {"UserPromptSubmit", "PreToolUse", "PostToolUse", "Stop"}
# prompt 型 hook 直接往上下文注入文字 = 直接烧 token
EVENT_COST = {
    "UserPromptSubmit": "每次你提交都跑",
    "PreToolUse": "每次工具调用前都跑（可拦截/改写）",
    "PostToolUse": "每次工具调用后都跑",
    "Stop": "每轮回答结束都跑",
    "SubagentStop": "每个子 agent 结束时跑",
    "PreCompact": "上下文压缩前跑",
    "SessionStart": "会话启动时跑一次",
    "SessionEnd": "会话结束时跑一次",
    "Notification": "通知时跑",
    "PermissionRequest": "弹权限询问时跑",
}


def load_json(p):
    try:
        return json.loads(Path(p).read_text(encoding="utf-8"))
    except Exception:
        return None


def enabled_plugins():
    """合并 settings 与 settings.local 的 enabledPlugins（local 优先）。"""
    out = {}
    for name in ("settings.json", "settings.local.json"):
        d = load_json(CLAUDE / name) or {}
        out.update(d.get("enabledPlugins", {}) or {})
    return out


def iter_hook_entries(cfg, origin, active, note):
    """把一个 hooks 配置块展开成扁平记录。"""
    for event, blocks in (cfg or {}).items():
        if not isinstance(blocks, list):
            continue
        for blk in blocks:
            matcher = blk.get("matcher", "(无)") if isinstance(blk, dict) else "(无)"
            for hk in (blk.get("hooks", []) if isinstance(blk, dict) else []):
                if not isinstance(hk, dict):
                    continue
                htype = hk.get("type", "?")
                cmd = hk.get("command") or ("[prompt 型：直接注入提示词到上下文]" if htype == "prompt" else "?")
                yield {
                    "event": event,
                    "matcher": matcher,
                    "type": htype,
                    "command": cmd,
                    "origin": origin,
                    "active": active,
                    "note": note,
                    "per_turn": event in PER_TURN,
                    "when": EVENT_COST.get(event, "未知时机"),
                }


def collect():
    rows = []

    # 1) 用户级 settings —— 你自己配的，视为可信
    for name in ("settings.json", "settings.local.json"):
        d = load_json(CLAUDE / name)
        if d and d.get("hooks"):
            rows += list(iter_hook_entries(
                d["hooks"], f"用户 settings ({name})", True, "你自己配置的"))

    # 2) skill 自带 hook —— 装了就生效，是「意外 hook」的主要来源
    for hj in sorted((CLAUDE / "skills").glob("*/hooks/hooks.json")):
        skill = hj.parent.parent.name
        d = load_json(hj)
        if d and d.get("hooks"):
            rows += list(iter_hook_entries(
                d["hooks"], f"skill: {skill}", True,
                f"来自 skill「{skill}」，安装即常驻（无需调用该 skill）"))

    # 3) 已安装 plugin —— 只有 enabledPlugins=true 才生效
    ep = enabled_plugins()
    inst = load_json(CLAUDE / "plugins" / "installed_plugins.json") or {}
    for pid, entries in (inst.get("plugins", {}) or {}).items():
        on = bool(ep.get(pid, False))
        for e in entries if isinstance(entries, list) else []:
            ip = e.get("installPath")
            if not ip:
                continue
            for hj in Path(ip).glob("hooks/hooks.json"):
                d = load_json(hj)
                if d and d.get("hooks"):
                    rows += list(iter_hook_entries(
                        d["hooks"], f"plugin: {pid}", on,
                        "已启用" if on else "enabledPlugins=false → 不生效"))

    # 4) marketplace 缓存 —— 永不生效，仅统计数量供对照
    mkt = list((CLAUDE / "plugins" / "marketplaces").glob("*/**/hooks/hooks.json"))

    return rows, mkt


def main():
    rows, mkt = collect()
    active = [r for r in rows if r["active"]]
    inactive = [r for r in rows if not r["active"]]

    if "--json" in sys.argv:
        print(json.dumps({"active": active, "inactive": inactive,
                          "marketplace_cached_files": len(mkt)},
                         ensure_ascii=False, indent=2))
        return

    print("=" * 74)
    print("生效中的 HOOK")
    print("=" * 74)
    if not active:
        print("  （无）")
    else:
        by_origin = {}
        for r in active:
            by_origin.setdefault(r["origin"], []).append(r)
        for origin, items in by_origin.items():
            turn = sum(1 for i in items if i["per_turn"])
            flag = f"  [每轮触发 {turn} 个]" if turn else ""
            print(f"\n▸ {origin}{flag}")
            print(f"  {items[0]['note']}")
            for r in items:
                mark = "!" if r["per_turn"] else " "
                print(f"   {mark} {r['event']:<18} matcher={str(r['matcher'])[:26]:<26} {r['command'][:56]}")

    print("\n" + "=" * 74)
    print("成本提示")
    print("=" * 74)
    pt = [r for r in active if r["per_turn"]]
    print(f"  每轮/每次工具调用都会跑的 hook: {len(pt)} 个")
    for r in pt:
        print(f"    - {r['event']} ({r['when']}) ← {r['origin']}")
    pr = [r for r in active if r["type"] == "prompt"]
    if pr:
        print(f"\n  prompt 型（直接往上下文注入文字，最烧 token）: {len(pr)} 个")
        for r in pr:
            print(f"    - {r['event']} ← {r['origin']}")

    if inactive:
        print("\n" + "=" * 74)
        print("不生效（勿误判为生效）")
        print("=" * 74)
        for r in inactive:
            print(f"  {r['event']:<18} {r['origin']}  — {r['note']}")

    if mkt:
        print(f"\n  另有 {len(mkt)} 个 marketplace 缓存中的 hooks.json —— 仓库副本，永不生效。")

    print("\n" + "=" * 74)
    print(f"合计：生效 {len(active)} 个 / 不生效 {len(inactive)} 个 / 缓存 {len(mkt)} 文件")
    print("=" * 74)


if __name__ == "__main__":
    main()
