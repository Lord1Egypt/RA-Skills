#!/usr/bin/env python3
"""
scripts/account_trust_scorer.py — 账号人因验证器（v1.1.0 · P0b / HF-R1）

对社交账号做「真人验证」评分：区分 真人 / 机器人 / 水军 / 可疑账号。
纯规则启发式（零外部依赖、零网络、零成本），信号维度（HF-R1：四维 → 五维）：

  ① 账号成熟度    (20%)  账号年龄 + 发帖总量合理性（新号刷量/幽灵号暴露）
  ② 粉丝真实性    (20%)  粉丝/关注比 + 僵尸粉比例 + 互动率（水军互关/僵尸粉暴露）
  ③ 行为自然度    (20%)  发帖间隔规律性 + 活跃时段分布 + 回复速率（机器人定时/秒回暴露）
  ④ 内容一致性    (20%)  话题多样性 + 跨平台内容重叠（单一话题机器 / 多平台同文暴露）
  ⑤ 内容伪造特征  (20%)  模板化相似度 + AI 生成占比 + 重复内容率（HF-P0 新增；
                          属「账号公域内容属性」，非设备/客户端指纹，不涉红线）

HF-P0 判据：仅扩展字段 + 规则，不新增能力项、不改 network_boundary、不动默认开关；
本模块输出契约向后兼容（dimensions 多一个键，confidence 分母随维度数自适应）。

设计对齐 infoseek 架构：
  - 输入容错：字段可选，缺省信号按「信息不足」处理，不误判
  - 输出统一：{trust_score, verdict, dimensions, flags, confidence}
  - verdict: real / likely_real / suspicious / bot / unknown（缺关键信号）
  - 与 capability_compensator 兼容：L2 人因验证层，degrade_to manual_review

用法:
    from account_trust_scorer import score_account
    res = score_account({"username": "alice", "account_age_days": 800, ...})

CLI:
    python scripts/account_trust_scorer.py --demo        # 演示各标签用例
    python scripts/account_trust_scorer.py --json '{"username":"x","account_age_days":30,...}'
"""

from __future__ import annotations

import json
import sys
from typing import Dict, List, Optional

# ── 维度权重（HF-R1：四维 → 五维，各 0.20，权重和 = 1.0）──
DIM_WEIGHTS = {
    "maturity": 0.20,     # 账号成熟度
    "audience": 0.20,     # 粉丝真实性
    "behavior": 0.20,     # 行为自然度
    "content": 0.20,      # 内容一致性
    "forge": 0.20,        # 内容伪造特征（HF-P0 新增）
}

# ── 判定阈值 ──
VERDICT_THRESHOLDS = [
    (80, "real", "高置信真人"),
    (60, "likely_real", "大概率真人"),
    (40, "suspicious", "可疑（需人工核实）"),
    (0, "bot", "高概率机器人/水军"),
]


def _clamp(v: float, lo: float = 0.0, hi: float = 100.0) -> float:
    return max(lo, min(hi, v))


# ═══════════════════════════════════════════════════════════════
# 单维评分（每个返回 (score, flags)）
# ═══════════════════════════════════════════════════════════════

def _score_maturity(a: Dict) -> tuple:
    """① 账号成熟度：年龄 + 发帖总量合理性。"""
    flags: List[str] = []
    age = a.get("account_age_days")
    posts = a.get("post_count")
    if age is None and posts is None:
        return 50.0, ["缺账号年龄/发帖量信号"]
    score, weight_sum = 0.0, 0.0
    if age is not None:
        # <7 天新号重罚；7-30 天轻罚；>180 天满分
        if age < 7:
            s = 10
            flags.append("新号(<7天)")
        elif age < 30:
            s = 40
            flags.append("年轻账号(<30天)")
        elif age < 180:
            s = 70
        else:
            s = 100
        score += s * 0.6
        weight_sum += 0.6
    if posts is not None:
        # 幽灵号（极低）与刷量号（日均>200）均重罚
        rate = posts / max(age or 1, 1)
        if posts == 0:
            s = 15
            flags.append("幽灵号(0发帖)")
        elif rate > 200:
            s = 10
            flags.append("刷量号(日均>200)")
        elif rate > 50:
            s = 40
            flags.append("高频刷帖(日均>50)")
        elif posts < 5 and (age or 0) > 90:
            s = 50
            flags.append("低活跃")
        else:
            s = 100
        score += s * 0.4
        weight_sum += 0.4
    return _clamp(score / max(weight_sum, 0.01)), flags


def _score_audience(a: Dict) -> tuple:
    """② 粉丝真实性：粉丝/关注比 + 僵尸粉 + 互动率。"""
    flags: List[str] = []
    followers = a.get("followers")
    following = a.get("following")
    zombie = a.get("zombie_follower_ratio")
    engagement = a.get("engagement_rate")
    if followers is None and zombie is None and engagement is None:
        return 50.0, ["缺粉丝/互动信号"]
    score, weight_sum = 0.0, 0.0
    if followers is not None and following is not None:
        if followers + following > 0:
            ratio = followers / (followers + following)
            # 真人：关注/粉丝比通常在 0.1-0.9；全关注0粉丝=水军特征
            if ratio < 0.02 and followers < 100:
                s = 20
                flags.append("几乎无粉丝(关注型)")
            elif ratio < 0.1:
                s = 50
            elif ratio > 0.95 and followers > 10000:
                s = 70  # 高粉丝低关注可接受
            else:
                s = 100
            score += s * 0.4
            weight_sum += 0.4
    if zombie is not None:
        s = 100 - _clamp(zombie * 150)  # 僵尸粉 20% → -30
        if zombie > 0.5:
            flags.append(f"僵尸粉高占比({zombie:.0%})")
        score += s * 0.4
        weight_sum += 0.4
    if engagement is not None:
        # 粉丝量大但互动率极低（<0.1%）→ 疑似买粉
        if engagement < 0.001:
            s = 20
            flags.append("互动率极低(<0.1%)")
        elif engagement < 0.01:
            s = 60
        else:
            s = 100
        score += s * 0.2
        weight_sum += 0.2
    return _clamp(score / max(weight_sum, 0.01)), flags


def _score_behavior(a: Dict) -> tuple:
    """③ 行为自然度：发帖间隔规律性 + 活跃时段 + 回复速率。"""
    flags: List[str] = []
    interval_std = a.get("post_interval_std")     # 小时；机器人极低
    active_hours = a.get("active_hours")          # 24h 分布覆盖时段数
    reply_rate = a.get("reply_rate")              # 回复速率（次/时）
    if interval_std is None and active_hours is None and reply_rate is None:
        return 50.0, ["缺行为信号"]
    score, weight_sum = 0.0, 0.0
    if interval_std is not None:
        if interval_std < 0.2:
            s = 10
            flags.append("发帖间隔极规律(疑似定时)")
        elif interval_std < 0.5:
            s = 35
        elif interval_std < 2:
            s = 80
        else:
            s = 100
        score += s * 0.4
        weight_sum += 0.4
    if active_hours is not None:
        if active_hours <= 2:
            s = 20
            flags.append("活跃时段过窄(疑似脚本)")
        elif active_hours <= 6:
            s = 60
        else:
            s = 100
        score += s * 0.3
        weight_sum += 0.3
    if reply_rate is not None:
        if reply_rate > 60:
            s = 20
            flags.append("回复速率异常高(疑似自动)")
        elif reply_rate == 0 and a.get("post_count", 0) > 50:
            s = 60
        else:
            s = 100
        score += s * 0.3
        weight_sum += 0.3
    return _clamp(score / max(weight_sum, 0.01)), flags


def _score_content(a: Dict) -> tuple:
    """④ 内容一致性：话题多样性 + 跨平台内容重叠。"""
    flags: List[str] = []
    diversity = a.get("topic_diversity")           # 0-1
    overlap = a.get("cross_platform_overlap")      # 0-1 同文多发（高=疑似矩阵号）
    cross_matches = a.get("cross_platform_matches")  # 跨平台同名命中数（多=真实存在）
    if diversity is None and overlap is None and cross_matches is None:
        return 50.0, ["缺内容信号"]
    score, weight_sum = 0.0, 0.0
    if diversity is not None:
        if diversity < 0.1:
            s = 15
            flags.append("话题极度单一(疑似主题机器人)")
        elif diversity < 0.3:
            s = 55
        else:
            s = 100
        score += s * 0.5
        weight_sum += 0.5
    if overlap is not None:
        if overlap > 0.8:
            s = 15
            flags.append("跨平台同文多发(疑似矩阵号)")
        elif overlap > 0.5:
            s = 55
        else:
            s = 100
        score += s * 0.3
        weight_sum += 0.3
    if cross_matches is not None:
        # 跨平台同名多命中：人因存在性强（Maigret 产出），加分但非充分
        s = 100 if cross_matches >= 2 else (60 if cross_matches == 1 else 40)
        score += s * 0.2
        weight_sum += 0.2
    return _clamp(score / max(weight_sum, 0.01)), flags


def _score_forge(a: Dict) -> tuple:
    """⑤ 内容伪造特征（HF-P0 新增）：模板化相似度 + AI 生成占比 + 重复内容率。

    仅消费「账号公域内容属性」字段（非设备/客户端指纹，不触红线）：
      - template_similarity : 帖文 n-gram 模板化相似度 0-1（高 = 批量套模板）
      - ai_generated_ratio  : 判定为 AI 生成文本的占比 0-1
      - duplicate_ratio     : 跨帖/跨账号重复内容占比 0-1
    缺省信号按「信息不足」中性处理，不误判。
    """
    flags: List[str] = []
    tpl = a.get("template_similarity")
    ai = a.get("ai_generated_ratio")
    dup = a.get("duplicate_ratio")
    if tpl is None and ai is None and dup is None:
        return 50.0, ["缺内容伪造信号"]
    score, weight_sum = 0.0, 0.0
    if tpl is not None:
        if tpl > 0.8:
            s = 15
            flags.append("高度模板化内容(疑似伪造)")
        elif tpl > 0.5:
            s = 50
        else:
            s = 100
        score += s * 0.4
        weight_sum += 0.4
    if ai is not None:
        if ai > 0.7:
            s = 20
            flags.append("AI生成内容占比高(疑似伪造)")
        elif ai > 0.4:
            s = 55
        else:
            s = 100
        score += s * 0.35
        weight_sum += 0.35
    if dup is not None:
        if dup > 0.6:
            s = 20
            flags.append("重复内容占比高(疑似搬运)")
        elif dup > 0.3:
            s = 55
        else:
            s = 100
        score += s * 0.25
        weight_sum += 0.25
    return _clamp(score / max(weight_sum, 0.01)), flags


# ═══════════════════════════════════════════════════════════════
# 主入口
# ═══════════════════════════════════════════════════════════════

def _verdict(score: float) -> str:
    for thr, label, _ in VERDICT_THRESHOLDS:
        if score >= thr:
            return label
    return "bot"


def _verdict_cn(verdict: str) -> str:
    for _, v, cn in VERDICT_THRESHOLDS:
        if v == verdict:
            return cn
    return "未知"


def score_account(account: Dict) -> Dict:
    """对单个账号做人因验证评分。

    参数: account 含以下可选字段（缺省信号按中性处理）：
        username, account_age_days, post_count, post_interval_std,
        active_hours, reply_rate, followers, following, zombie_follower_ratio,
        engagement_rate, topic_diversity, cross_platform_overlap, cross_platform_matches,
        template_similarity, ai_generated_ratio, duplicate_ratio   # HF-R1 内容伪造特征

    返回: {
        username, trust_score, verdict, verdict_cn, confidence,
        dimensions: {name: {score, weight, flags}},
        flags: [...], missing: [...]
    }
    """
    dims: Dict[str, Dict] = {}
    all_flags: List[str] = []
    missing: List[str] = []

    scorers = {
        "maturity": (_score_maturity, ["account_age_days", "post_count"]),
        "audience": (_score_audience, ["followers", "following", "zombie_follower_ratio", "engagement_rate"]),
        "behavior": (_score_behavior, ["post_interval_std", "active_hours", "reply_rate"]),
        "content": (_score_content, ["topic_diversity", "cross_platform_overlap", "cross_platform_matches"]),
        "forge": (_score_forge, ["template_similarity", "ai_generated_ratio", "duplicate_ratio"]),
    }
    total, weight_sum = 0.0, 0.0
    for name, (fn, sig_fields) in scorers.items():
        score, flags = fn(account)
        weight = DIM_WEIGHTS[name]
        dims[name] = {"score": round(score, 1), "weight": weight, "flags": flags}
        total += score * weight
        weight_sum += weight
        all_flags.extend(flags)
        if not any(account.get(f) is not None for f in sig_fields):
            missing.append(name)

    trust_score = round(_clamp(total / max(weight_sum, 0.01)), 1)
    verdict = _verdict(trust_score)

    # 信息不足 → unknown（不误判真人/机器人）
    if len(missing) >= 2:
        verdict = "unknown"

    # 强机器人 flag 计数 ≥3 → 强制降级一档（防「成熟账号+机器人行为」被高估）
    _STRONG_BOT_FLAGS = (
        "发帖间隔极规律(疑似定时)", "活跃时段过窄(疑似脚本)", "回复速率异常高(疑似自动)",
        "话题极度单一(疑似主题机器人)", "跨平台同文多发(疑似矩阵号)", "僵尸粉高占比",
        "高度模板化内容(疑似伪造)", "AI生成内容占比高(疑似伪造)", "重复内容占比高(疑似搬运)",
    )
    strong_hits = sum(1 for f in all_flags if f.startswith(_STRONG_BOT_FLAGS))
    if strong_hits >= 3 and verdict in ("real", "likely_real"):
        verdict = "suspicious"
    elif strong_hits >= 4 and verdict in ("suspicious", "likely_real"):
        verdict = "bot"

    # 置信度：有信号的维度占比（分母随维度数自适应，HF-R1 四维→五维）
    confidence = round(1.0 - len(missing) / len(scorers), 2)

    return {
        "username": account.get("username", ""),
        "trust_score": trust_score,
        "verdict": verdict,
        "verdict_cn": _verdict_cn(verdict),
        "confidence": confidence,
        "dimensions": dims,
        "flags": all_flags,
        "missing": missing,
    }


def _demo() -> int:
    cases = [
        ("真人账号", {"username": "alice", "account_age_days": 800, "post_count": 1200,
                      "post_interval_std": 3.5, "active_hours": 14, "reply_rate": 1.2,
                      "followers": 5000, "following": 300, "zombie_follower_ratio": 0.05,
                      "engagement_rate": 0.03, "topic_diversity": 0.7,
                      "cross_platform_overlap": 0.1, "cross_platform_matches": 3,
                      "template_similarity": 0.15, "ai_generated_ratio": 0.1,
                      "duplicate_ratio": 0.1}),
        ("定时机器人", {"username": "bot1", "account_age_days": 400, "post_count": 4000,
                        "post_interval_std": 0.05, "active_hours": 1, "reply_rate": 0,
                        "followers": 50, "following": 5000, "zombie_follower_ratio": 0.8,
                        "engagement_rate": 0.0001, "topic_diversity": 0.02,
                        "cross_platform_overlap": 0.95, "cross_platform_matches": 0,
                        "template_similarity": 0.9, "ai_generated_ratio": 0.85,
                        "duplicate_ratio": 0.7}),
        ("矩阵水军", {"username": "mob", "account_age_days": 15, "post_count": 3000,
                      "post_interval_std": 0.1, "active_hours": 2, "reply_rate": 80,
                      "followers": 10, "following": 200, "zombie_follower_ratio": 0.9,
                      "engagement_rate": 0.0002, "topic_diversity": 0.05,
                      "cross_platform_overlap": 0.9, "cross_platform_matches": 1,
                      "template_similarity": 0.85, "ai_generated_ratio": 0.6,
                      "duplicate_ratio": 0.65}),
        ("信息不足", {"username": "ghost"}),
    ]
    for name, acc in cases:
        r = score_account(acc)
        print(f"\n[{name}] {r['username']} → {r['verdict']} ({r['verdict_cn']}) score={r['trust_score']} conf={r['confidence']}")
        for d, v in r["dimensions"].items():
            print(f"  {d}: {v['score']}{' ⚠ ' + ','.join(v['flags']) if v['flags'] else ''}")
    return 0


def main() -> int:
    import argparse
    ap = argparse.ArgumentParser(description="账号人因验证器")
    ap.add_argument("--demo", action="store_true", help="演示用例")
    ap.add_argument("--json", metavar="ACC", help='账号 JSON（如 \'{"username":"x","account_age_days":30}\'）')
    args = ap.parse_args()
    if args.demo or not args.json:
        return _demo()
    try:
        acc = json.loads(args.json)
    except Exception as e:
        print(f"JSON 解析失败: {e}")
        return 1
    print(json.dumps(score_account(acc), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
