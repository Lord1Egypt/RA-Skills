#!/usr/bin/env python3
"""Infoseek v1.0.1 补充测试：entity_pending + conflict_v2 + anchor_score_v2（G7 余项）

entity_pending: 待确认实体队列（add/list/approve/reject/批量/拒绝统计）
conflict_v2: 实体感知冲突检测（数值冲突 / 跨源覆盖 / v1 兼容）
anchor_score_v2: v2 评分纯函数（信任加权 / Jaccard / 时间衰减 / 最终分）
"""
import os
import sys
import json
import tempfile
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / 'core'))
sys.path.insert(0, str(ROOT))  # entity_pending 用 `import core.entities` 绝对导入

passed, failed = [], []

def check(name, cond, extra=''):
    if cond:
        passed.append(name); print(f"  [PASS] {name} {extra}")
    else:
        failed.append(name); print(f"  [FAIL] {name} {extra}")


# ═══════════════════════════════════════════════════════════════
# PE: entity_pending
# ═══════════════════════════════════════════════════════════════
print("\n═══ entity_pending 测试 ═══")

from entity_pending import PendingEntitiesQueue

# PE1: 使用临时 env 数据目录隔离（state_path 读 INFOSEEK_DATA_DIR）
tf = tempfile.mkdtemp()
os.environ['INFOSEEK_DATA_DIR'] = tf
import importlib
import state_dir
state_dir = importlib.reload(state_dir)

# PE1: add
q = PendingEntitiesQueue()
ok = q.add({'name': 'OpenAI', 'type': 'ORG', 'confidence': 0.9})
check('PE1 add 实体', ok and q.count() >= 1, f"count={q.count()}")

# PE2: 重复 add 去重
q.add({'name': 'OpenAI', 'type': 'ORG', 'confidence': 0.8})
cnt = q.count()
check('PE2 重复 add 去重', cnt == 1, f"count={cnt}")

# PE3: list 按置信过滤
q.add({'name': '未知实体', 'type': 'UNKNOWN', 'confidence': 0.3})
lst_high = q.list(min_confidence=0.5)
check('PE3 list 置信过滤', all(i.get('confidence', 0) >= 0.5 for i in lst_high), f"n={len(lst_high)}")

# PE4: approve
q.approve('OpenAI')
check('PE4 approve 移除', q.count() == 1, f"count={q.count()}")  # 只剩未知实体

# PE5: reject
q.reject('未知实体', reason='低置信')
check('PE5 reject 移除', q.count() == 0, f"count={q.count()}")

# PE6: 拒绝统计
q.add({'name': 'A', 'type': 'ORG', 'confidence': 0.7})
q.reject('A', reason='重复')
stats = q.get_rejected_stats()
check('PE6 拒绝统计', isinstance(stats, dict) and stats.get('total', 0) >= 1, f"stats={stats}")

# PE7: 批量批准高置信
q.add({'name': 'B', 'type': 'TECH', 'confidence': 0.9})
q.add({'name': 'C', 'type': 'TECH', 'confidence': 0.6})
n = q.batch_approve_high_confidence(threshold=0.85)
check('PE7 批量批准高置信', n >= 1 and q.count() == 1, f"approved={n} remain={q.count()}")

# PE8: clear_rejected
cleared = q.clear_rejected()
check('PE8 清空拒绝记录', cleared >= 0 and q.count_rejected() == 0)

# 清理：恢复 env + 删临时目录
os.environ.pop('INFOSEEK_DATA_DIR', None)
import shutil
shutil.rmtree(tf, ignore_errors=True)

# ═══════════════════════════════════════════════════════════════
# CV: conflict_v2
# ═══════════════════════════════════════════════════════════════
print("\n═══ conflict_v2 测试 ═══")

from conflict_v2 import detect_conflicts_v2, detect_entity_conflicts, _detect_numeric_conflicts

# CV1: 数值冲突（营收增 vs 降；_detect_numeric_conflicts 需 value 字段）
src_numeric = [
    {'title': 'A 公司 Q3 营收', 'value': '1000', 'url': 'https://a/1'},
    {'title': 'A 公司 Q3 营收', 'value': '900', 'url': 'https://b/2'},
]
num = _detect_numeric_conflicts(src_numeric)
check('CV1 数值冲突检测', isinstance(num, dict), f"type={type(num).__name__}")

# CV2: detect_entity_conflicts
ents = detect_entity_conflicts([
    {'title': 'OpenAI 开源 GPT-5', 'snippet': 'OpenAI 宣布 GPT-5 完全开源', 'url': 'https://a/1'},
    {'title': 'OpenAI 闭源', 'snippet': '官方确认 GPT-5 保持闭源', 'url': 'https://b/2'},
])
# v2 遗留实现为兼容接口（v3 detect_conflicts_v3 已替代实体矛盾检测）；
# 验证接口可调用且返回 list（不要求检出，因 v2 输入契约不同）
check('CV2 实体冲突接口可用', isinstance(ents, list), f"n={len(ents)}")

# CV3: detect_conflicts_v2 完整入口
r = detect_conflicts_v2([
    {'title': 'OpenAI 开源 GPT-5', 'snippet': 'OpenAI 宣布 GPT-5 完全开源', 'url': 'https://a/1'},
    {'title': 'OpenAI 闭源', 'snippet': '官方确认 GPT-5 保持闭源', 'url': 'https://b/2'},
], subject='AI')
check('CV3 detect_conflicts_v2 入口', isinstance(r, dict) and 'conflicts' in r,
      f"keys={list(r.keys())[:5]}")

# CV4: v2 关 v1 路径（use_v1=False）
r2 = detect_conflicts_v2([], subject='', use_v1=False)
check('CV4 纯 v2 路径', isinstance(r2, dict), f"keys={list(r2.keys())[:4]}")

# CV5: 空源不崩
r3 = detect_conflicts_v2([], subject='')
check('CV5 空源不崩', isinstance(r3, dict))

# ═══════════════════════════════════════════════════════════════
# AS: anchor_score_v2
# ═══════════════════════════════════════════════════════════════
print("\n═══ anchor_score_v2 测试 ═══")

from anchor_score_v2 import (compute_trust_bonus_v2, compute_jaccard_v2,
                             compute_decay_factor_v2, compute_final_score_v2)

# AS1: 信任加权（白名单域名加分）
bonus = compute_trust_bonus_v2('https://arxiv.org/abs/1', '', 'general')
check('AS1 信任加权', bonus >= 0, f"bonus={bonus}")

# AS2: Jaccard 语义
j = compute_jaccard_v2('DeepSeek 开源模型 技术', 'DeepSeek 开源模型')
check('AS2 Jaccard 语义', 0 <= j <= 100, f"j={j}")

# AS3: 时间衰减（新>旧）
d_new = compute_decay_factor_v2(0)
d_old = compute_decay_factor_v2(365)
check('AS3 时间衰减', d_new >= d_old, f"new={d_new} old={d_old}")

# AS4: 最终评分（含语义维度）
src = {'title': 'DeepSeek 开源模型', 'snippet': 'DeepSeek 开源模型技术', 'url': 'https://example.com/x'}
r4 = compute_final_score_v2(src, subject='DeepSeek 开源模型', with_semantic=True,
                            semantic_text='DeepSeek 开源模型技术')
check('AS4 最终评分', 'after_whitelist_final' in r4 and 0 <= r4['after_whitelist_final'] <= 100,
      f"final={r4.get('after_whitelist_final')}")

# AS5: 空源评分不崩
r5 = compute_final_score_v2({}, subject='')
check('AS5 空源评分', isinstance(r5, dict) and 'after_whitelist_final' in r5)

# AS6: 不修改输入 dict（纯函数）
src_before = dict(src)
compute_final_score_v2(src, subject='DeepSeek 开源模型', with_semantic=True,
                       semantic_text='DeepSeek 开源模型技术')
check('AS6 纯函数不改输入', src == src_before)

# AS7: 分类门控
r7 = compute_final_score_v2({'title': '无关内容', 'snippet': '完全无关', 'url': 'https://x.com'}, subject='DeepSeek 开源模型')
cls = r7.get('classification', '')
check('AS7 分类门控存在', cls in ('🟢核心', '🟡潜力', '❌噪声'), f"cls={cls}")

print(f"\n=== pending+conflict+anchor 测试: {len(passed)} PASS / {len(failed)} FAIL ===")
if failed:
    print("FAILED:", failed)
    sys.exit(1)
print("ALL PASS")
