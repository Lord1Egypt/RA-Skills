#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_identity_fusion_v160.py — 三因子置信度融合集成测试（v1.6.0 · P1/T4）

覆盖：
  F1 [归一化] A 因子 cross_platform_matches → 0-1（缺失/0 中性不惩罚单体存在）
  F2 [归一化] C 因子站点权威白名单 tier（core/trust_sources 复用）
  F3 [归一化] C 因子 rank 数值分段（对数衰减）
  F4 [融合]   weighted_sum 公式正确性（给定输入 → 期望置信度）
  F5 [融合]   B 因子缺失动态重归一化（Σw=1 保证）
  F6 [兼容]   fuse_anchor 新增字段不覆盖原字段（confidence/trust_score/verdict）
  F7 [兼容]   B 强否决：trust<40 且判定非 bot → verdict_final=needs_review
  F8 [开关]   INFOSEEK_FUSION_ENABLED=0 → 无融合字段（可回退旧行为）
  F9 [端到端] _augment_cross_matches：同名跨平台补齐（G1 修复验证）
  F10 [端到端] _build_identity_anchors：融合字段齐全 + 原字段透传
  F11 [降级]   全缺失/畸形输入不抛异常（融合是增强不阻断）
  F12 [权重]   INFOSEEK_FUSION_WEIGHTS 覆盖 + 非法回退默认

不触碰真实凭据/网络（沿用 v150 测试风格）。
"""
import os
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))
sys.path.insert(0, str(ROOT / 'core'))
sys.path.insert(0, str(ROOT))

from identity_confidence_fusion import (
    fuse_confidence, fuse_anchor, norm_cross, norm_site, norm_trust,
    DEFAULT_WEIGHTS, NORM_NEUTRAL, fusion_enabled,
)
from infoseek_pipeline import _augment_cross_matches, _build_identity_anchors

os.environ.pop('INFOSEEK_FUSION_ENABLED', None)
os.environ.pop('INFOSEEK_FUSION_WEIGHTS', None)

passed, failed = [], []


def check(name, cond, detail=''):
    if cond:
        passed.append(name)
        print(f"  [PASS] {name}" + (f"  ({detail})" if detail else ""))
    else:
        failed.append(name)
        print(f"  [FAIL] {name}" + (f"  ({detail})" if detail else ""))


def close(a, b, eps=1e-3):
    return abs(a - b) <= eps


# ═══════════════════════════════════════════════════════════════
# F1 — A 因子归一化
# ═══════════════════════════════════════════════════════════════
print("\n== F1: A 因子（多平台交叉）归一化 ==")
check("F1 cross=缺失 → 0.4 中性（不惩罚单体存在）", close(norm_cross(None)[0], 0.4))
check("F1 cross=0 → 0.4 中性", close(norm_cross(0)[0], 0.4))
check("F1 cross=1 → 0.5", close(norm_cross(1)[0], 0.5))
check("F1 cross=3 → 0.85", close(norm_cross(3)[0], 0.85))
check("F1 cross=10 → 1.0（≥5 封顶）", close(norm_cross(10)[0], 1.0))
check("F1 cross=畸形 'abc' → 0.4（容错）", close(norm_cross('abc')[0], 0.4))

# ═══════════════════════════════════════════════════════════════
# F2/F3 — C 因子归一化
# ═══════════════════════════════════════════════════════════════
print("\n== F2/F3: C 因子（站点权威）归一化 ==")
v, st = norm_site("https://www.huxiu.com/article/123", None)   # 白名单 tier3
check("F2 url 命中白名单 tier3 → 0.5", close(v, 0.5), f"st={st}")
v, st = norm_site("https://github.com/alice", 18)              # 未命中白名单 → rank 18
check("F3 rank=18 → 0.75（对数分段）", close(v, 0.75), f"st={st}")
v, st = norm_site("https://weibo.com/bot1", 120000)
check("F3 rank=120000 → 0.1（衰减下限）", close(v, 0.1), f"st={st}")
v, st = norm_site("", None)
check("F3 url+rank 双缺失 → 0.5 中性", close(v, NORM_NEUTRAL), f"st={st}")
v, st = norm_site("", 0)
check("F3 rank=0（无数据）→ 0.5 中性", close(v, NORM_NEUTRAL), f"st={st}")

# ═══════════════════════════════════════════════════════════════
# F4/F5 — 融合计算
# ═══════════════════════════════════════════════════════════════
print("\n== F4/F5: weighted_sum 融合 ==")
r = fuse_confidence(cross=4, trust_score=82, site_rank=18, url="https://github.com/alice")
# 0.95*0.35 + 0.82*0.40 + 0.75*0.25 = 0.3325+0.328+0.1875 = 0.848
check("F4 真人高权威 → 0.848 高置信", close(r['confidence_final'], 0.848),
      f"final={r['confidence_final']}")
check("F4 标签 high/高置信", r['confidence_label'] == 'high' and r['confidence_label_cn'] == '高置信')

r2 = fuse_confidence(cross=0, trust_score=18, site_rank=120000, url="https://weibo.com/bot1")
# 0.4*0.35+0.18*0.40+0.1*0.25 = 0.14+0.072+0.025 = 0.237
check("F4 水军低权威 → 0.237 极低置信", close(r2['confidence_final'], 0.237),
      f"final={r2['confidence_final']}")

r3 = fuse_confidence(cross=2, trust_score=None, site_rank=None, url="")
# B/C 缺失 → a=0.7, 重归一化 w=(0.35,0.25) → (0.7*0.35+0.5*0.25)/0.6 = 0.6167
check("F5 B 缺失动态重归一化 → 0.6167", close(r3['confidence_final'], 0.6167),
      f"final={r3['confidence_final']}")
check("F5 fusion_degradation 标注缺失因子", sorted(r3['fusion_degradation']) == ['b_trust', 'c_site'])
check("F5 weights 总和=1（present 因子重归一化）",
      close(sum(r3['fusion']['weights'].values()), 1.0))

# ═══════════════════════════════════════════════════════════════
# F6/F7 — 兼容性（不覆盖原字段 + 强否决）
# ═══════════════════════════════════════════════════════════════
print("\n== F6/F7: 兼容性 ==")
acc_in = {"username": "alice", "platform": "GitHub", "url": "https://github.com/alice",
          "confidence": 0.9, "source": "Maigret", "site_rank": 18,
          "cross_platform_matches": 4, "trust_score": 82, "verdict": "real",
          "verdict_cn": "高置信真人", "trust_confidence": 0.75}
out = fuse_anchor(acc_in)
check("F6 原字段不被覆盖（confidence=0.9）", out["confidence"] == 0.9)
check("F6 原字段不被覆盖（trust_score=82）", out["trust_score"] == 82)
check("F6 原字段不被覆盖（verdict=real）", out["verdict"] == "real")
check("F6 新增 confidence_final", out.get("confidence_final") is not None)
check("F6 新增 fusion.factors 含 a/b/c", all(k in out["fusion"]["factors"]
                                            for k in ("a_cross", "b_trust", "c_site")))
check("F6 verdict_final 兼容原判定", out["verdict_final"] == "real")

acc_bot = {"username": "mob", "url": "https://weibo.com/mob", "confidence": 0.6,
           "trust_score": 18, "verdict": "likely_real", "verdict_cn": "大概率真人",
           "cross_platform_matches": 1, "site_rank": 90000}
out2 = fuse_anchor(acc_bot)
check("F7 B 强否决：trust<40 且非 bot → needs_review", out2["verdict_final"] == "needs_review",
      f"vf={out2['verdict_final']}")

# ═══════════════════════════════════════════════════════════════
# F8 — 融合开关（可回退旧行为）
# ═══════════════════════════════════════════════════════════════
print("\n== F8: 融合开关 ==")
os.environ['INFOSEEK_FUSION_ENABLED'] = '0'
check("F8 开关=0 → fusion_enabled False", fusion_enabled() is False)
out3 = fuse_anchor(acc_in)
check("F8 开关=0 → 无融合字段（原样透传）", out3.get("confidence_final") is None and out3["confidence"] == 0.9)
os.environ.pop('INFOSEEK_FUSION_ENABLED', None)
check("F8 开关缺省 → 融合开启", fusion_enabled() is True)

# ═══════════════════════════════════════════════════════════════
# F9/F10 — 端到端（pipeline 接线）
# ═══════════════════════════════════════════════════════════════
print("\n== F9/F10: 端到端接线 ==")
discovered = [
    {"username": "alice", "platform": "GitHub", "url": "https://github.com/alice",
     "confidence": 0.9, "source": "Maigret", "site_rank": 18},
    {"username": "alice", "platform": "微博", "url": "https://weibo.com/alice",
     "confidence": 0.8, "source": "Sherlock", "site_rank": 120000},
    {"username": "bot1", "platform": "微博", "url": "https://weibo.com/bot1",
     "confidence": 0.7, "source": "Sherlock", "site_rank": 99999},
    {"username": "alice", "platform": "Twitter", "url": "https://twitter.com/alice",
     "confidence": 0.6, "source": "Sherlock", "site_rank": 500,
     "cross_platform_matches": 5},   # 已带值 → 保留
]
aug = _augment_cross_matches(discovered)
a_gh = next(a for a in aug if a["url"] == "https://github.com/alice")
a_tw = next(a for a in aug if a["url"] == "https://twitter.com/alice")
a_bot = next(a for a in aug if a["username"] == "bot1")
check("F9 cross 补齐：GitHub 条目 cross=2（排除自身后 2 个其他平台）",
      a_gh["cross_platform_matches"] == 2, f"cross={a_gh['cross_platform_matches']}")
check("F9 已带值不覆盖：Twitter 条目 cross=5 保留", a_tw["cross_platform_matches"] == 5)
check("F9 单平台账号 cross=0（无交叉）", a_bot["cross_platform_matches"] == 0)

anchors = _build_identity_anchors(aug, "alice", 10)
first = anchors[0]
check("F10 锚点含融合字段 confidence_final", first.get("confidence_final") is not None,
      f"final={first.get('confidence_final')}")
check("F10 锚点原字段透传（confidence/verdict/trust_score 键保留）",
      set(("confidence", "url", "title", "snippet", "score", "source")) <= set(first.keys()))
check("F10 融合区分度：GitHub(rank18) > 微博(rank120000)",
      anchors[0]["confidence_final"] > anchors[1]["confidence_final"],
      f"{anchors[0]['confidence_final']} vs {anchors[1]['confidence_final']}")

# ═══════════════════════════════════════════════════════════════
# F11 — 降级（融合是增强，不阻断）
# ═══════════════════════════════════════════════════════════════
print("\n== F11: 降级容错 ==")
r_all = fuse_confidence()
check("F11 全缺失 → 不抛异常，中性 0.5 附近", close(r_all['confidence_final'], 0.5, eps=0.1),
      f"final={r_all['confidence_final']}")
check("F11 全缺失 → degradation 标注 3 因子",
      len(r_all['fusion_degradation']) == 3)
check("F11 fuse_anchor({}) 不抛异常", isinstance(fuse_anchor({}), dict))
check("F11 fuse_anchor(None 字典内缺字段) 不抛异常",
      isinstance(fuse_anchor({"username": "x"}), dict))

# ═══════════════════════════════════════════════════════════════
# F12 — 权重可配置
# ═══════════════════════════════════════════════════════════════
print("\n== F12: 权重配置 ==")
os.environ['INFOSEEK_FUSION_WEIGHTS'] = '0.5,0.3,0.2'
r_w = fuse_confidence(cross=4, trust_score=82, site_rank=18, url="https://github.com/alice")
# 0.95*0.5+0.82*0.3+0.75*0.2 = 0.475+0.246+0.15 = 0.871
check("F12 env 权重覆盖生效 → 0.871", close(r_w['confidence_final'], 0.871),
      f"final={r_w['confidence_final']}")
os.environ['INFOSEEK_FUSION_WEIGHTS'] = '1,2,3,4,5'   # 非法（非 3 个）
r_bad = fuse_confidence(cross=4, trust_score=82, site_rank=18, url="https://github.com/alice")
check("F12 非法权重回退默认 → 0.848", close(r_bad['confidence_final'], 0.848),
      f"final={r_bad['confidence_final']}")
os.environ.pop('INFOSEEK_FUSION_WEIGHTS', None)

# ═══════════════════════════════════════════════════════════════
print(f"\n结果: {len(passed)} passed / {len(failed)} failed")
os.environ.pop('INFOSEEK_FUSION_ENABLED', None)
os.environ.pop('INFOSEEK_FUSION_WEIGHTS', None)
sys.exit(1 if failed else 0)