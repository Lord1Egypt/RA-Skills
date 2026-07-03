#!/usr/bin/env python3
"""
update_memory.py - 增量更新 memory 文件(由 Skill 调用)

支持的操作:
  - add_corpus: 添加新语料,自动更新画像各字段
  - add_rehearsal: 添加预演记录
  - update_profile: 修改画像综述
  - delete_corpus: 注释掉(不真删)某条 corpus

用法:
  python update_memory.py --file memory-L001.md --action add_corpus --signals signals.json
"""

import argparse
import json
import sys
from datetime import date
from pathlib import Path
from typing import Optional

# 让脚本能直接 import 同目录的 memory_io
sys.path.insert(0, str(Path(__file__).parent))
from memory_io import (
    load, save, init_empty, add_corpus_entry, next_corpus_id,
    CorpusEntry, Memory,
)


def ema_update(old: Optional[float], new: float, alpha: float = 0.15) -> float:
    """指数移动平均更新"""
    if old is None:
        return round(new, 3)
    return round(alpha * new + (1 - alpha) * old, 3)


def update_decision_axes(memory: Memory, signals: dict) -> list[str]:
    """根据新信号更新 decision_axes"""
    changes = []
    axes = memory.frontmatter.setdefault("decision_axes", {})
    evidence = memory.frontmatter.setdefault("evidence_by_axis", {})
    
    for pref in signals.get("preferences_expressed", []):
        dim = pref.get("dimension")
        direction = pref.get("direction")
        strength = pref.get("strength", 0.5)
        
        if not dim or direction is None:
            continue
        
        target = float(direction) if isinstance(direction, (int, float)) else (1.0 if direction == "high" else 0.0)
        weighted = target * strength + (axes.get(dim) or 0.5) * (1 - strength)
        
        old = axes.get(dim)
        new = ema_update(old, weighted)
        axes[dim] = new
        evidence[dim] = evidence.get(dim, 0) + 1
        changes.append(f"decision_axes.{dim}: {old} → {new} (累计证据 {evidence[dim]})")
    
    return changes


def update_challenges(memory: Memory, signals: dict, corpus_id: str) -> list[str]:
    """更新 frequent_challenges"""
    changes = []
    challenges = memory.frontmatter.setdefault("frequent_challenges", [])
    
    for ch in signals.get("challenges_raised", []):
        theme = ch.get("theme")
        intensity = ch.get("intensity", "medium")
        if not theme:
            continue
        
        intensity_val = {"low": 0.3, "medium": 0.6, "high": 0.9}.get(intensity, 0.5)
        
        existing = next((c for c in challenges if c.get("theme") == theme), None)
        if existing:
            old_w = existing.get("weight", 0)
            new_w = ema_update(old_w, intensity_val)
            existing["weight"] = new_w
            if corpus_id not in existing.setdefault("evidence", []):
                existing["evidence"].append(corpus_id)
            changes.append(f"challenges.{theme}: weight {old_w} → {new_w}")
        else:
            challenges.append({
                "theme": theme,
                "weight": round(intensity_val, 3),
                "evidence": [corpus_id],
            })
            changes.append(f"challenges: 新主题 '{theme}' (weight={intensity_val})")
    
    challenges.sort(key=lambda c: c.get("weight", 0), reverse=True)
    return changes


def update_redlines(memory: Memory, signals: dict) -> list[str]:
    """更新 redlines"""
    changes = []
    redlines = memory.frontmatter.setdefault("redlines", [])
    for rl in signals.get("redline_signals", []):
        text = rl if isinstance(rl, str) else rl.get("text", "")
        if text and text not in redlines:
            redlines.append(text)
            changes.append(f"redlines: + '{text}'")
    return changes


def update_style(memory: Memory, signals: dict) -> list[str]:
    """更新 communication_style"""
    changes = []
    style = memory.frontmatter.setdefault("communication_style", {})
    for st in signals.get("style_signals", []):
        if not isinstance(st, dict):
            continue
        for k, v in st.items():
            if v is None:
                continue
            if style.get(k) != v:
                old = style.get(k)
                style[k] = v
                changes.append(f"style.{k}: {old} → {v}")
    return changes


def build_corpus_body(corpus_id: str, signals: dict) -> str:
    """从信号字典生成 corpus 的 markdown 区块"""
    title = signals.get("title") or signals.get("scene", "(未命名)")
    
    metadata_lines = [
        f"- date: {signals.get('date', date.today().isoformat())}",
        f"- scene: {signals.get('scene', '未知')}",
        f"- channel: {signals.get('channel', signals.get('scene', '未知'))}",
        f"- attribution: {signals.get('attribution', 'paraphrased')}",
        f"- weight: {signals.get('weight', 1.0)}",
    ]
    tags = signals.get("tags", [])
    if tags:
        metadata_lines.append(f"- tags: [{', '.join(tags)}]")
    if signals.get("source_url"):
        metadata_lines.append(f"- source_url: {signals['source_url']}")
    
    body_parts = [
        f"## {corpus_id} · {title}",
        "",
        "\n".join(metadata_lines),
        "",
    ]
    
    if signals.get("scene_background"):
        body_parts.extend([
            "**场景背景**:",
            "",
            signals["scene_background"],
            "",
        ])
    
    if signals.get("content"):
        body_parts.extend([
            "**内容**:",
            "",
            "\n".join(f"> {line}" for line in signals["content"].split("\n")),
            "",
        ])
    
    # 抽取信号摘要
    sig_lines = []
    for ch in signals.get("challenges_raised", []):
        sig_lines.append(f"- challenges_raised: {ch.get('theme')} (intensity: {ch.get('intensity', 'medium')})")
    for pref in signals.get("preferences_expressed", []):
        sig_lines.append(f"- preferences: {pref.get('dimension')} direction={pref.get('direction')} strength={pref.get('strength', 0.5)}")
    for st in signals.get("style_signals", []):
        if isinstance(st, dict):
            for k, v in st.items():
                sig_lines.append(f"- style: {k}={v}")
    
    if sig_lines:
        body_parts.extend([
            "**抽取信号**:",
            "",
            "\n".join(sig_lines),
            "",
        ])
    
    if signals.get("judgment"):
        body_parts.extend([
            "**我的判断**:",
            "",
            signals["judgment"],
            "",
        ])
    
    return "\n".join(body_parts).rstrip()


def action_add_corpus(memory: Memory, signals: dict) -> list[str]:
    """添加新 corpus + 更新画像"""
    corpus_id = signals.get("corpus_id") or next_corpus_id(memory)
    
    body = build_corpus_body(corpus_id, signals)
    entry = CorpusEntry(
        corpus_id=corpus_id,
        title=signals.get("title", signals.get("scene", "")),
        raw_body=body,
        metadata={
            "date": signals.get("date", date.today().isoformat()),
            "scene": signals.get("scene", ""),
            "attribution": signals.get("attribution", "paraphrased"),
            "weight": signals.get("weight", 1.0),
        },
    )
    add_corpus_entry(memory, entry)
    
    changes = [f"新增 corpus: {corpus_id}"]
    
    # 低密度信号只入库,不更新画像
    if not signals.get("low_density", False):
        changes.extend(update_decision_axes(memory, signals))
        changes.extend(update_challenges(memory, signals, corpus_id))
        changes.extend(update_redlines(memory, signals))
        changes.extend(update_style(memory, signals))
    else:
        changes.append("(低密度信号,不更新画像决策维度)")
    
    return changes


def action_delete_corpus(memory: Memory, corpus_id: str) -> list[str]:
    """注释掉某条 corpus(不真删)"""
    for entry in memory.corpus_entries:
        if entry.corpus_id == corpus_id:
            # 把 raw_body 用 HTML 注释包起来
            entry.raw_body = f"<!-- DELETED {date.today().isoformat()}\n{entry.raw_body}\n-->"
            return [f"已注释 corpus: {corpus_id}"]
    return [f"未找到 corpus: {corpus_id}"]


def main():
    parser = argparse.ArgumentParser(description="增量更新 memory 文件")
    parser.add_argument("--file", required=True, type=Path, help="memory 文件路径")
    parser.add_argument("--action", required=True, choices=[
        "add_corpus", "delete_corpus", "init",
    ])
    parser.add_argument("--signals", type=Path, help="信号 JSON 文件(用于 add_corpus)")
    parser.add_argument("--corpus-id", help="用于 delete_corpus")
    parser.add_argument("--npc-id", help="用于 init")
    parser.add_argument("--relation", default="other", help="用于 init")
    parser.add_argument("--dry-run", action="store_true", help="只显示变更,不写入")
    
    args = parser.parse_args()
    
    if args.action == "init":
        if args.file.exists():
            print(f"[!] 文件已存在: {args.file}", file=sys.stderr)
            sys.exit(1)
        if not args.npc_id:
            print("[!] init 需要 --npc-id", file=sys.stderr)
            sys.exit(1)
        m = init_empty(args.npc_id, args.relation)
        if not args.dry_run:
            args.file.parent.mkdir(parents=True, exist_ok=True)
            save(m, args.file)
            print(f"[OK] 已创建空白 memory: {args.file}")
        else:
            print(f"[DRY] 将创建: {args.file}")
        return
    
    # 加载现有 memory
    memory = load(args.file)
    
    if args.action == "add_corpus":
        if not args.signals or not args.signals.exists():
            print("[!] add_corpus 需要 --signals JSON 文件", file=sys.stderr)
            sys.exit(1)
        signals = json.loads(args.signals.read_text(encoding="utf-8"))
        changes = action_add_corpus(memory, signals)
    elif args.action == "delete_corpus":
        if not args.corpus_id:
            print("[!] delete_corpus 需要 --corpus-id", file=sys.stderr)
            sys.exit(1)
        changes = action_delete_corpus(memory, args.corpus_id)
    
    if args.dry_run:
        print("=== DRY RUN ===")
        for c in changes:
            print(f"  {c}")
        print(f"=== 不会写入 {args.file} ===")
    else:
        save(memory)
        for c in changes:
            print(f"  · {c}")
        print(f"[OK] 已更新: {args.file}")
        print(f"[OK] evidence_count: {memory.frontmatter.get('evidence_count')}, confidence: {memory.frontmatter.get('confidence')}")


if __name__ == "__main__":
    main()
