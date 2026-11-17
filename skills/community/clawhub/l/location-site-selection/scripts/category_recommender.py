#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
餐饮品类选址推荐引擎 (Category Recommender)
==========================================
基于地图 MCP 采集 / 人工评估得到的商圈特征，输出**数据驱动**的餐饮品类排序与回避建议。

设计原则（透明、可解释）：
  - 每个品类有「适配画像」(preferred_ta / pref_consumption / impulse / barrier / needs_vent)。
  - 基础适配分 = 商圈类型匹配 + 消费水平匹配。
  - 再叠加 竞争强度 / TQI / 商业密度 / 合规硬伤 四类修正。
  - 最终 0–100 分，映射为 绿(推荐)/黄(慎选)/红(回避)。

输入特征 dict（可由地图 MCP 输出或人工填写）：
  trade_area_type   : 商圈型 / 办公型 / 社区型 / 校园型 / 交通枢纽型 / 旅游型
  consumption_level : High / Medium / Low
  commercial_density: High / Medium / Low   （Buffer Zone 内 POI 密度）
  competition_intensity: Low / Medium / High （同业态竞品密度）
  tqi               : float                   （来自 roi_calculator 的客流质量指数）
  red_flags         : list                    （合规硬伤，命中排烟/消防则否决需排烟品类）
  avg_rent_per_sqm  : float (可选)            （元/㎡/月，辅助推断消费水平）

输出：
  recommend(features) -> {
     ranked: [ {category, score, tier, reason, watchout}, ... ],
     best: "茶饮咖啡",
     avoid: ["火锅"],
  }
"""
import sys


# ---------- 品类适配画像 ----------
# barrier: 启动壁垒（影响竞争红海程度）；needs_vent: 是否需排烟（受 red_flag 约束）
CATEGORY_PROFILE = {
    "茶饮咖啡": {
        "pref_ta": ["商圈型", "交通枢纽型", "校园型", "办公型"],
        "pref_consumption": ["任意"],
        "impulse": True, "barrier": "低", "needs_vent": False,
        "cap": 0.06, "invest": "低",
        "desc": "冲动型高频消费，捕获率高，无需排烟，试错成本低",
    },
    "烘焙面包": {
        "pref_ta": ["社区型", "商圈型", "办公型"],
        "pref_consumption": ["Medium", "High"],
        "impulse": True, "barrier": "低", "needs_vent": False,
        "cap": 0.05, "invest": "低",
        "desc": "早高峰连带购买，品牌溢价空间大",
    },
    "轻食沙拉": {
        "pref_ta": ["办公型", "商圈型"],
        "pref_consumption": ["Medium", "High"],
        "impulse": False, "barrier": "低", "needs_vent": False,
        "cap": 0.04, "invest": "低",
        "desc": "健康刚需，办公客群复购稳，无需排烟",
    },
    "快餐": {
        "pref_ta": ["办公型", "交通枢纽型", "社区型", "商圈型"],
        "pref_consumption": ["Low", "Medium", "High"],
        "impulse": False, "barrier": "中", "needs_vent": True,
        "cap": 0.04, "invest": "中",
        "desc": "高频刚需，对消费水平不敏感，但需合规排烟",
    },
    "正餐": {
        "pref_ta": ["社区型", "商圈型"],
        "pref_consumption": ["Medium", "High"],
        "impulse": False, "barrier": "中", "needs_vent": True,
        "cap": 0.015, "invest": "中",
        "desc": "客单高、毛利稳，但受竞争与消费水平双重约束",
    },
    "火锅": {
        "pref_ta": ["商圈型", "社区型"],
        "pref_consumption": ["Medium", "High"],
        "impulse": False, "barrier": "高", "needs_vent": True,
        "cap": 0.015, "invest": "高",
        "desc": "客单与翻台双高，投资大且强依赖排烟与排风",
    },
}

VENT_FLAGS = {"no_fume", "no_vent", "排烟", "fire_hazard", "fire", "消防",
              "no_sewage", "排污", "unknow_title", "产权", "illegal"}

# 品类竞争敏感度（红海脆弱度）：冲动型/低壁垒品类对竞品密度最敏感
COMP_SENS = {
    "茶饮咖啡": 1.2, "烘焙面包": 1.2, "轻食沙拉": 1.0,
    "快餐": 0.9, "正餐": 0.8, "火锅": 0.7,
}


def _norm(s):
    return str(s or "").strip()


def _has_vent_flag(red_flags):
    rfs = [_norm(x).lower() for x in (red_flags or [])]
    return any(any(t in rf for t in VENT_FLAGS) for rf in rfs)


def recommend(features: dict) -> dict:
    ta = _norm(features.get("trade_area_type")) or "社区型"
    cons = _norm(features.get("consumption_level")) or "Medium"
    dens = _norm(features.get("commercial_density")) or "Medium"
    comp = _norm(features.get("competition_intensity")) or "Medium"
    tqi = float(features.get("tqi", 1.0) or 1.0)
    vent_blocked = _has_vent_flag(features.get("red_flags"))

    ranked = []
    for cat, p in CATEGORY_PROFILE.items():
        score = 0
        reasons = []

        # —— 基础适配 ——
        if ta in p["pref_ta"]:
            score += 50
            reasons.append(f"商圈类型[{ta}]适配")
        else:
            score += 30
            reasons.append(f"商圈类型[{ta}]次优（基准分）")

        if "任意" in p["pref_consumption"] or cons in p["pref_consumption"]:
            score += 15
            reasons.append(f"消费水平[{cons}]匹配")
        else:
            score -= 5
            reasons.append(f"消费水平[{cons}]偏低，客单承压")

        # —— 商业密度（客流基数）——
        if dens == "High":
            score += 6 if p["impulse"] or p["barrier"] == "低" else 3
            reasons.append("商业密度高→曝光基数大")
        elif dens == "Low":
            score -= 6 if p["impulse"] else 3
            reasons.append("商业密度低→自然客流不足")

        # —— 竞争强度（按品类竞争敏感度加权）——
        base_comp = {"High": 14, "Medium": 7, "Low": 0}[comp]
        comp_penalty = int(base_comp * COMP_SENS.get(cat, 1.0))
        score -= comp_penalty
        if comp_penalty:
            reasons.append(f"竞争强度[{comp}]→扣{comp_penalty}")

        # —— 消费水平溢价/折价 ——
        if cons == "High" and cat in ("正餐", "火锅", "烘焙面包"):
            score += 5
            reasons.append("消费水平高→溢价品类受益")
        elif cons == "Low" and cat in ("正餐", "火锅"):
            score -= 10
            reasons.append("消费水平低→高客单品类承压")

        # —— TQI（门头可视+物理阻抗）——
        if tqi < 0.7:
            score -= 15
            reasons.append(f"TQI={tqi:.2f}过低→进店率受限")
        elif tqi < 0.8:
            score -= 8
            reasons.append(f"TQI={tqi:.2f}偏弱→需补可视性")

        # —— 合规硬伤（排烟否决）——
        watchout = ""
        if p["needs_vent"] and vent_blocked:
            score = 5
            reasons.append("⛔ 命中排烟/消防硬伤→直接否决")
            watchout = "本点位无合规排烟，涉油烟品类一票否决"

        score = max(0, min(100, score))

        tier = "绿(推荐)" if score >= 70 else ("黄(慎选)" if score >= 50 else "红(回避)")
        if not watchout and p["needs_vent"] and comp == "High":
            watchout = "需确认排烟合规 + 错位产品避免贴脸肉搏"
        elif not watchout and p["impulse"] and comp == "High":
            watchout = "红海预警：以差异化产品/侧招突围"

        ranked.append({
            "category": cat,
            "score": score,
            "tier": tier,
            "barrier": p["barrier"],
            "invest": p["invest"],
            "capture": p["cap"],
            "reason": "；".join(reasons),
            "watchout": watchout,
        })

    ranked.sort(key=lambda x: x["score"], reverse=True)
    best = ranked[0]["category"] if ranked[0]["score"] >= 50 else "（暂无强推荐，建议重选点位）"
    avoid = [r["category"] for r in ranked if r["score"] < 50]
    return {"ranked": ranked, "best": best, "avoid": avoid}


def print_rec(r: dict):
    print("=" * 60)
    print("  餐饮品类选址推荐（数据驱动）")
    print("=" * 60)
    print(f"  首选品类: {r['best']}")
    if r["avoid"]:
        print(f"  回避品类: {', '.join(r['avoid'])}")
    print("-" * 60)
    for x in r["ranked"]:
        print(f"  [{x['tier']}] {x['category']:<6} 分={x['score']:>3}  壁垒={x['barrier']} 投资={x['invest']}")
        print(f"       依据: {x['reason']}")
        if x["watchout"]:
            print(f"       警示: {x['watchout']}")
    print("=" * 60)


def main():
    import json
    import argparse
    p = argparse.ArgumentParser(description="餐饮品类选址推荐引擎")
    p.add_argument("--json", help="商圈特征 JSON 文件")
    p.add_argument("--demo", action="store_true", help="运行内置示例")
    args = p.parse_args()

    if args.demo:
        feats = DEMO_FEATURES
    elif args.json:
        with open(args.json, "r", encoding="utf-8") as fh:
            feats = json.load(fh)
    else:
        print("请通过 --json <file> 或 --demo 提供商圈特征。", file=sys.stderr)
        sys.exit(2)

    res = recommend(feats)
    print_rec(res)
    print("\n===JSON===")
    print(json.dumps(res, ensure_ascii=False, indent=2))


DEMO_FEATURES = {
    "trade_area_type": "商圈型",
    "consumption_level": "Medium",
    "commercial_density": "High",
    "competition_intensity": "High",
    "tqi": 0.85,
    "red_flags": [],
}


if __name__ == "__main__":
    main()
