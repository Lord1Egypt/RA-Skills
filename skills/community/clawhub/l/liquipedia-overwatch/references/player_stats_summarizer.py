#!/usr/bin/env python3
"""
OWTV 选手数据分析器 + 最佳选手评选器 v3
==========================================

【v3 公平 MPS 评选机制 — 按角色核心职责设计】

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  重新设计原则：核心职责 × 非重叠指标
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

问题：原版让 Tank 比伤害、Sup 比伤害，DPS 比治疗——完全不合理。

新设计：
  每个角色有且仅有一个核心指标（Primary）
  其他指标作为补充背景（Secondary），仅用于同分时打破平局

  ┌──────────────────────────────────────────────┐
  │  Tank 核心 = Damage Blocked（Mits）           │
  │  DPS  核心 = Damage Dealt                    │
  │  Sup  核心 = Healing                         │
  │                                              │
  │  通用次要 = Eliminations（击杀数）             │
  │  通用背景 = KDA（生存效率）                  │
  └──────────────────────────────────────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  公式设计（v3）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Tank MPS  = 0.50 × blk_norm       [核心：阻挡伤害]
            + 0.30 × elim_norm       [次要：击杀贡献]
            + 0.20 × kda_norm        [背景：存活效率]

  DPS  MPS  = 0.50 × dmg_norm        [核心：伤害输出]
            + 0.30 × elim_norm       [次要：击杀贡献]
            + 0.20 × kda_norm       [背景：存活效率]

  Sup  MPS  = 0.50 × heal_norm       [核心：治疗量]
            + 0.30 × elim_norm       [次要：击杀贡献（部分辅助如Kiriko）]
            + 0.20 × kda_norm       [背景：存活效率]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Per-Map Normalization（消除局数差异）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  elim_norm  = elim_per_map / 所有Tank选手 elim/m 的最大值
  dmg_norm  = dmg_per_map / 所有DPS选手 dmg/m 的最大值
  blk_norm  = blk_per_map / 所有Tank选手 blk/m 的最大值（仅Tank）
  heal_norm = heal_per_map / 所有Sup选手 heal/m 的最大值（仅Sup）
  kda_norm = ln(kda_value + 1) / 10
           （归一化到 ~0~4 范围，对数平滑处理）

  → 每项指标都在 [0, 1] 范围内，直接可比
  → 解决了不同局数 → 不同总量的问题

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  胜方 ×1.10 加成（不变）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import json
import math
import sys
import os
from typing import Any

# ────────────────────────────────────────────────────────────
# 辅助
# ────────────────────────────────────────────────────────────

def ln(x: float) -> float:
    return math.log(max(x, 0.001))


def normalize(val: float, max_val: float) -> float:
    """归一化到 [0, 1]，max_val=0 时返回 0"""
    return val / max_val if max_val > 0 else 0.0


def kda_norm(kills: int, assists: int, deaths: int) -> float:
    """KDA 归一化：对数处理避免极值爆炸，再压缩到 ~0~4 范围"""
    deaths = max(deaths, 1)
    kda = (kills + assists * 0.5) / deaths
    return min(ln(kda + 1) / 4.0, 1.0)   # ln(10+1)/4 ≈ 0.92 为上界


# ────────────────────────────────────────────────────────────
# 数据读取
# ────────────────────────────────────────────────────────────

def load(path: str) -> list:
    with open(path) as f:
        data = json.load(f)
    return data.get("matches", [])


# ────────────────────────────────────────────────────────────
# Per-Map 基础统计
# ────────────────────────────────────────────────────────────

def per_map_stats(raw: dict, maps: int) -> dict:
    m = max(maps, 1)
    return {
        "elim_pm":  raw.get("elim", 0) / m,
        "dmg_pm":   raw.get("dmg",  0) / m,
        "heal_pm":  raw.get("heal", 0) / m,
        "blk_pm":   raw.get("blk",  0) / m,
        "ast_pm":    raw.get("ast",  0) / m,
        "maps":     maps,
        "kda_raw":  (raw.get("elim", 0) + raw.get("ast", 0) * 0.5) / max(raw.get("dth", 1), 1),
    }


# ────────────────────────────────────────────────────────────
# v3 MPS 计算（两步：先归一化，再加权）
# ────────────────────────────────────────────────────────────

def calc_mps_v3(
    raw: dict,
    maps: int,
    role: str,
    won: bool,
    # 全角色池的 per-map 最大值（用于归一化）
    max_elim_pm: float,
    max_dmg_pm:  float,
    max_blk_pm:  float,
    max_heal_pm: float,
) -> dict:
    """
    v3 算法：
      Step 1: Per-map normalization（消除局数差异）
      Step 2: Z-Score-ish 归一化（每个指标 ÷ 全角色池最大值 → [0,1]）
      Step 3: 角色专属 MPS 加权
      Step 4: 胜方 ×1.10
    """
    m  = max(maps, 1)
    pm = per_map_stats(raw, maps)

    # ── Step 1: 局均统计（已在 per_map_stats 完成）
    elim_pm  = pm["elim_pm"]
    dmg_pm   = pm["dmg_pm"]
    heal_pm  = pm["heal_pm"]
    blk_pm   = pm["blk_pm"]
    kda_raw  = pm["kda_raw"]

    # ── Step 2: 归一化到 [0, 1]
    elim_n  = normalize(elim_pm, max_elim_pm)
    dmg_n   = normalize(dmg_pm,  max_dmg_pm)
    blk_n   = normalize(blk_pm,  max_blk_pm)
    heal_n  = normalize(heal_pm, max_heal_pm)
    kda_n   = kda_norm(raw.get("elim", 0), raw.get("ast", 0), raw.get("dth", 1))

    # ── Step 3: 角色专属 MPS
    if role == "Tank":
        mps_raw = 0.50 * blk_n + 0.30 * elim_n + 0.20 * kda_n
        primary_stat = f"阻挡伤害 {blk_pm:,.0f}/m"
    elif role == "Dps":
        mps_raw = 0.50 * dmg_n + 0.30 * elim_n + 0.20 * kda_n
        primary_stat = f"伤害输出 {dmg_pm:,.0f}/m"
    else:  # Sup
        mps_raw = 0.50 * heal_n + 0.30 * elim_n + 0.20 * kda_n
        primary_stat = f"治疗量 {heal_pm:,.0f}/m"

    # ── Step 4: 胜方加成
    bonus = 1.10 if won else 1.00
    mps   = round(mps_raw * bonus, 4)

    return {
        "role":        role,
        "maps":        maps,
        "won":         won,
        "bonus_applied": bonus > 1.0,
        # 原始
        "elim": raw.get("elim", 0),
        "dmg":  raw.get("dmg",  0),
        "heal": raw.get("heal", 0),
        "blk":  raw.get("blk",  0),
        "dth":  raw.get("dth", 0),
        "ast":  raw.get("ast",  0),
        # Per-map 均值（用于展示）
        "elim_pm":  round(elim_pm,  1),
        "dmg_pm":   round(dmg_pm,   0),
        "heal_pm":  round(heal_pm,  0),
        "blk_pm":   round(blk_pm,   0),
        "kda_raw":  round(kda_raw, 2),
        # 归一化分（用于展示辅助理解 MPS）
        "elim_n": round(elim_n, 3),
        "dmg_n":  round(dmg_n,  3),
        "blk_n":  round(blk_n,  3),
        "heal_n": round(heal_n, 3),
        "kda_n":  round(kda_n,  3),
        # MPS 核心
        "primary_stat": primary_stat,
        "mps":    mps,
        "mps_raw": round(mps_raw, 4),
    }


# ────────────────────────────────────────────────────────────
# 批量计算所有选手 MPS
# ────────────────────────────────────────────────────────────

def score_all(matches: list) -> tuple:
    """返回 (tank_scores, dps_scores, sup_scores)"""

    # 第一遍：收集所有选手的局均基础统计（算全局最大值）
    tank_raw, dps_raw, sup_raw = [], [], []

    for match in matches:
        winner   = match.get("winner", "")
        maps     = match.get("maps", 0)
        players  = match.get("players", {})

        for team_key, roster in players.items():
            won = (team_key == winner)
            for pid, stats in roster.items():
                role = (stats.get("role") or "").capitalize()
                if role not in ("Tank", "Dps", "Sup"):
                    role = stats.get("role", "Sup")
                pm = per_map_stats(stats, maps)
                entry = {"pid": pid, "team": team_key, "won": won,
                         "stats": stats, "pm": pm, "role": role}

                if role == "Tank": tank_raw.append(entry)
                elif role == "Dps": dps_raw.append(entry)
                else: sup_raw.append(entry)

    # 全局 per-map 最大值（用于归一化）
    max_elim_pm = max((e["pm"]["elim_pm"]  for e in tank_raw + dps_raw + sup_raw), default=1)
    max_dmg_pm  = max((e["pm"]["dmg_pm"]   for e in tank_raw + dps_raw + sup_raw), default=1)
    max_blk_pm  = max((e["pm"]["blk_pm"]   for e in tank_raw), default=1)
    max_heal_pm = max((e["pm"]["heal_pm"]  for e in sup_raw), default=1)

    def score_entry(e: dict) -> dict:
        scored = calc_mps_v3(
            raw=e["stats"], maps=e["pm"]["maps"],
            role=e["role"], won=e["won"],
            max_elim_pm=max_elim_pm, max_dmg_pm=max_dmg_pm,
            max_blk_pm=max_blk_pm, max_heal_pm=max_heal_pm,
        )
        return {**scored, "player": e["pid"], "team": e["team"]}

    tank = sorted([score_entry(e) for e in tank_raw], key=lambda x: x["mps"], reverse=True)
    dps  = sorted([score_entry(e) for e in dps_raw],  key=lambda x: x["mps"], reverse=True)
    sup  = sorted([score_entry(e) for e in sup_raw],   key=lambda x: x["mps"], reverse=True)

    return tank, dps, sup


# ────────────────────────────────────────────────────────────
# 展示
# ────────────────────────────────────────────────────────────

def fmt(entry: dict, rank: int) -> str:
    bonus = " ✅胜" if entry["bonus_applied"] else ""
    n = entry["role"]
    # 归一化分展示
    elim_s = f"击杀={entry['elim_n']:.2f}" if n == "Tank" else f"击杀={entry['elim_n']:.2f}"
    dmg_s  = f"伤害={entry['dmg_n']:.2f}"  if n == "Dps"  else ""
    blk_s  = f"抵挡={entry['blk_n']:.2f}"  if n == "Tank" else f"治疗={entry['heal_n']:.2f}"
    kda_s  = f"KDA={entry['kda_raw']:.2f}(n={entry['kda_n']:.2f})"
    norm_s = f"({elim_s} {blk_s or dmg_s} {kda_s})"
    return (
        f"  {rank}. **{entry['player']}** ({entry['team']})\n"
        f"     MPS={entry['mps']:.4f} | {entry['primary_stat']} | 局数={entry['maps']}{bonus}\n"
        f"     归一化分: {norm_s}"
    )


def report(tank: list, dps: list, sup: list, matches: list) -> dict:
    all_players = tank + dps + sup
    overall = sorted(all_players, key=lambda x: x["mps"], reverse=True)[:10]

    W = 64
    print("\n" + "=" * W)
    print("  🏆 OWTV 选手数据分析报告  —  v3 公平角色核心 MPS 评选")
    print("=" * W)
    print("  ┌────────────────────────────────────────────────────────┐")
    print("  │  Tank MPS = 0.50×blk_n + 0.30×elim_n + 0.20×kda_n   │")
    print("  │  DPS  MPS = 0.50×dmg_n  + 0.30×elim_n + 0.20×kda_n  │")
    print("  │  Sup  MPS = 0.50×heal_n + 0.30×elim_n + 0.20×kda_n  │")
    print("  │  ※ 每项指标 ÷ 该指标全局最大值（归一化到 0~1）        │")
    print("  │  ※ 胜方 ×1.10 | 局数归一化（消除Bo3/Bo5总量差异）   │")
    print("  └────────────────────────────────────────────────────────┘")
    print(f"\n  分析范围：{len(matches)} 场比赛\n")

    print("  ── 🛡️ Tank — 核心：阻挡伤害 ──")
    for i, e in enumerate(tank[:5], 1): print(fmt(e, i))

    print("\n  ── 💥 DPS — 核心：伤害输出 ──")
    for i, e in enumerate(dps[:5], 1): print(fmt(e, i))

    print("\n  ── 💚 Support — 核心：治疗量 ──")
    for i, e in enumerate(sup[:5], 1): print(fmt(e, i))

    print("\n  ── 🏅 全位置 MPS 总榜 TOP 10 ──")
    for i, e in enumerate(overall, 1): print(fmt(e, i))

    return {
        "matches_analyzed": len(matches),
        "mechanism_v3": {
            "description": ("角色核心指标归一化 MPS，"
                            "Tank=0.5blk+0.3elim+0.2kda，"
                            "DPS=0.5dmg+0.3elim+0.2kda，"
                            "Sup=0.5heal+0.3elim+0.2kda，"
                            "胜方×1.10，每指标归一化到[0,1]"),
            "primary_tank": "Damage Blocked（Mits）",
            "primary_dps":  "Damage Dealt",
            "primary_sup":  "Healing",
            "normalization": "per_map_stat ÷ max_per_map_stat_in_pool",
            "win_bonus": "1.10x for winning team",
        },
        "tank": tank[:5],
        "dps":  dps[:5],
        "sup":  sup[:5],
        "overall": overall,
    }


# ────────────────────────────────────────────────────────────
# CLI
# ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 player_stats_summarizer.py <hero_picks.json> [--json]")
        sys.exit(1)

    path = sys.argv[1]
    if not os.path.exists(path):
        print(f"❌ 文件不存在: {path}")
        sys.exit(1)

    matches = load(path)
    print(f"📂 读取 {len(matches)} 场比赛 ...")

    tank, dps, sup = score_all(matches)
    result = report(tank, dps, sup, matches)

    if "--json" in sys.argv:
        print("\n\n--- JSON OUTPUT ---")
        print(json.dumps(result, indent=2, ensure_ascii=False))
