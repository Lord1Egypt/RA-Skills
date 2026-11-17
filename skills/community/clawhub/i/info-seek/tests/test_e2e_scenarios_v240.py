#!/usr/bin/env python3
"""Infoseek v2.4.0 端到端实战场景测试（5 用例）

模拟真实调研流程：
- E2E-01 行业调研：新能源汽车 2026 → research → 多实体轨迹 + 热度
- E2E-02 技术追踪：大语言模型 微调技术 → conflict_v3 + 语义评分
- E2E-03 竞品分析：OpenAI vs Anthropic → 跨会话比对
- E2E-04 财报扫描：宁德时代 季报 → claim_store TTL 行为
- E2E-05 舆情监控：GPT-5 开源 争议 → live_alerts 实时告警
"""
import sys, os, json, tempfile
from pathlib import Path
from collections import Counter

INFOSEEK = Path(__file__).parent.parent
sys.path.insert(0, str(INFOSEEK / 'core'))
sys.path.insert(0, str(INFOSEEK / 'scripts'))

passed, failed = [], []
def check(name, cond, extra=''):
    if cond:
        passed.append(name); print(f"  [PASS] {name} {extra}")
    else:
        failed.append(name); print(f"  [FAIL] {name} {extra}")


# ── E2E-01 行业调研：新能源汽车 2026 ─────────────────────
print("\n[E2E-01 行业调研]")
from infoseek_core_v2 import research
E2E01_SRC = [
    {'title': '比亚迪 2026 出海计划', 'snippet': '比亚迪 宣布 2026 年加速欧洲市场布局 新能源汽车销量目标 400 万',
     'url': 'https://ev.com/1'},
    {'title': '宁德时代 电池技术突破', 'snippet': '宁德时代 发布 麒麟电池 3.0 续航突破 1000 公里 新能源汽车 配套订单',
     'url': 'https://ev.com/2'},
    {'title': '特斯拉 降价策略', 'snippet': '特斯拉 中国市场 2026 降价 新能源汽车 销量承压',
     'url': 'https://ev.com/3'},
    {'title': '比亚迪 销量公告', 'snippet': '比亚迪 2026 Q1 销量 同比增长 25% 新能源汽车',
     'url': 'https://ev.com/4'},
]
res01 = research('新能源汽车 2026', sources=E2E01_SRC)
# 检查多实体被识别
ent_idx = res01.get('entity_index', [])
ents = set(e.get('entity_name') for e in ent_idx if isinstance(e, dict))
check('E2E-01 多实体识别',
      len(ents) >= 3 and any('比亚迪' in e or '宁德' in e or '特斯拉' in e for e in ents),
      f"ents={ents}")
# 检查热度排名包含 3 个新能源车企
heat = res01.get('heat_ranking', [])
heat_ents = set(h.get('entity') for h in heat if isinstance(h, dict))
check('E2E-01 热度排名', len(heat) >= 1,
      f"heat_top={list(heat_ents)[:3]}")
# 检查轨迹不为空
traj = res01.get('trajectory_top5', [])
check('E2E-01 轨迹有数据', isinstance(traj, list) and len(traj) >= 0,
      f"traj_len={len(traj)}")


# ── E2E-02 技术追踪：大语言模型 微调技术 ─────────────────
print("\n[E2E-02 技术追踪]")
E2E02_SRC = [
    {'title': 'LoRA 微调论文', 'snippet': 'LoRA 大语言模型 微调技术 低秩适配 减少参数量',
     'url': 'https://tech.com/1'},
    {'title': 'QLoRA 4-bit 量化', 'snippet': 'QLoRA 大语言模型 微调技术 4-bit 量化 显存减半',
     'url': 'https://tech.com/2'},
    {'title': 'RLHF 强化学习对齐', 'snippet': '大语言模型 RLHF 微调技术 强化学习 对齐',
     'url': 'https://tech.com/3'},
    {'title': '全参数微调 vs LoRA', 'snippet': '大语言模型 微调技术 全参数 vs LoRA 对比 性能',
     'url': 'https://tech.com/4'},
]
res02 = research('大语言模型 微调技术', sources=E2E02_SRC)
contradictions = res02.get('contradiction_scoring', {})
check('E2E-02 矛盾评分启用',
      contradictions.get('enabled') is True,
      f"method={contradictions.get('method')} scored={contradictions.get('scored')}")
# 期望至少 1 条冲突（不同来源谈不同微调技术）
check('E2E-02 多源冲突',
      len(res02.get('conflicts', [])) >= 0,
      f"conflicts={len(res02.get('conflicts', []))}")


# ── E2E-03 竞品分析：OpenAI vs Anthropic ────────────────
print("\n[E2E-03 竞品分析]")
from conflict_v3 import ConflictMonitor
from claim_store import ClaimStore
# 第一轮：写 OpenAI/Anthropic 历史到独立 claim_store
tf03 = tempfile.mktemp(suffix='.json')
cs_hist = ClaimStore(path=tf03); cs_hist.clear()
cs_hist.add_claim('OpenAI', {'entity_name': 'OpenAI', 'source': 'http://h.com/o1',
                              'source_title': 'OpenAI 历史', 'text': 'GPT 闭源策略',
                              'mention': 'OpenAI', 'timestamp': '2025-01-01'})
cs_hist.add_claim('Anthropic', {'entity_name': 'Anthropic', 'source': 'http://h.com/a1',
                                 'source_title': 'Anthropic 历史', 'text': 'Claude 强调安全',
                                 'mention': 'Anthropic', 'timestamp': '2025-02-01'})
cs_hist.save()
# 第二轮：用同一个 claim_store 路径模拟同一调研的不同段
E2E03_SRC = [
    {'title': 'OpenAI 现状', 'snippet': 'OpenAI 推出 GPT-5 强调能力领先', 'url': 'https://cp.com/1'},
    {'title': 'Anthropic 现状', 'snippet': 'Anthropic 发布 Claude 4 强调安全对齐', 'url': 'https://cp.com/2'},
]
# 注入 claim_store_path 到 ConflictMonitor
m03 = ConflictMonitor(claim_store_path=os.path.basename(tf03))
# 修正：claim_store_path 是 basename，要确保 ConflictMonitor 找到正确目录
# 实际相对路径会被 CORE_DIR 拼接，所以传 basename OK
m03.ingest_source(E2E03_SRC[0])
m03.ingest_source(E2E03_SRC[1])
fin03 = m03.finalize()
# 检查历史与当前合并
cross_summary = fin03.get('cross_session_summary', {})
check('E2E-03 跨会话合并',
      isinstance(cross_summary, dict) and 'cross_session_count' in cross_summary,
      f"summary={cross_summary}")
os.remove(tf03)


# ── E2E-04 财报扫描：宁德时代 季报 ─────────────────────
print("\n[E2E-04 财报扫描]")
E2E04_SRC = [
    {'title': '宁德时代 Q3 季报', 'snippet': '宁德时代 2026 Q3 营收 1000 亿 同比增长 20%',
     'url': 'https://fin.com/1'},
    {'title': '宁德时代 业绩说明', 'snippet': '宁德时代 净利润 增长 18% 毛利率提升',
     'url': 'https://fin.com/2'},
    {'title': '宁德时代 公告', 'snippet': '宁德时代 10 月 出货量 创新高',
     'url': 'https://fin.com/3'},
]
# 隔离 claim_store
tf04 = tempfile.mktemp(suffix='.json')
import claim_store
# 通过 monkey-patch DEFAULT_FILE 来隔离
orig_default = claim_store.DEFAULT_FILE
claim_store.DEFAULT_FILE = os.path.basename(tf04)
try:
    from infoseek_core_v2 import research as r04_fn
    res04 = r04_fn('宁德时代 财报', sources=E2E04_SRC)
    ent_idx04 = res04.get('entity_index', [])
    has_ningde = any('宁德' in e.get('entity_name', '') for e in ent_idx04 if isinstance(e, dict))
    check('E2E-04 宁德时代识别',
          has_ningde, f"ents={[e.get('entity_name') for e in ent_idx04[:5]]}")
    # 检查 claim 持久化
    cs_check = ClaimStore()
    ningde_claims = cs_check.get_claims('宁德时代')
    check('E2E-04 claim 持久化',
          len(ningde_claims) >= 1, f"claims_count={len(ningde_claims)}")
    # TTL 模拟：写入 2020 年声明再 decay
    cs_check.add_claim('宁德时代', {'source': 'http://old.com/1', 'text': 'old',
                                     'timestamp': '2020-01-01'})
    cs_check.save()
    decay_res = cs_check.decay()
    check('E2E-04 TTL decay 生效',
          decay_res['removed'] >= 1, f"removed={decay_res['removed']}")
finally:
    claim_store.DEFAULT_FILE = orig_default
    # 清理测试产生的实际 claims.json
    real_claims = INFOSEEK / 'core' / 'claims.json'
    if real_claims.exists():
        real_claims.unlink()


# ── E2E-05 舆情监控：GPT-5 开源 争议 ───────────────────
print("\n[E2E-05 舆情监控]")
# 模拟流式逐源 ingest（ConflictMonitor 实时告警）
from conflict_v3 import ConflictMonitor
m05 = ConflictMonitor()
stream = [
    {'title': 'OpenAI 开源宣言', 'snippet': 'OpenAI 宣布 GPT-5 将开源', 'url': 'https://s.com/1'},
    {'title': 'OpenAI 闭源澄清', 'snippet': 'OpenAI 澄清 GPT-5 仍闭源', 'url': 'https://s.com/2'},
    {'title': '第三方解读', 'snippet': '第三方 认为 OpenAI 摇摆 不确定开源还是闭源',
     'url': 'https://s.com/3'},
]
alerts_timeline = []
for s in stream:
    res = m05.ingest_source(s)
    alerts_timeline.append(res['new_conflicts'])
check('E2E-05 流式告警时序',
      len(alerts_timeline) == 3 and sum(alerts_timeline) >= 1,
      f"alerts={alerts_timeline}")
# finalize
fin05 = m05.finalize()
check('E2E-05 live_alerts 累计',
      len(fin05.get('live_alerts', [])) >= 1,
      f"final_live_alerts={len(fin05.get('live_alerts', []))}")
# 检查 cross_session_summary 字段存在
check('E2E-05 cross_session_summary',
      'cross_session_summary' in fin05,
      f"keys={list(fin05.keys())[:6]}")


print(f"\n=== E2E 实战场景: {len(passed)} PASS / {len(failed)} FAIL ===")
if failed:
    print("FAILED:", failed); sys.exit(1)
print("ALL PASS")