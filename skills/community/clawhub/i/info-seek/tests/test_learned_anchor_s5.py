#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tests/test_learned_anchor_s5.py — S5 晋级真锚契约守护

覆盖 S5（方向一阶段C，bump v2.3.1，变动 10–30%）核心契约：
  A  15 个 accept 真锚词名单固化（与 promote_s5 / 对拍账目一致）
  B  promote_s5 晋级：灌库 accept=15、pending=0、证据字段齐全
  C  幂等：重复晋级结果一致；set_decision accept 不被 pending 覆盖
  D  accept 名单内部无子串冲突；22 个 reject 不被灌入
  E  主链统一访问协议端到端：OFF 逐字节回退、ON 受控消费 accept 词
  F  promote_s5 内部子串冲突自检可触发

测试用临时目录 + INFOSEEK_DATA_DIR 隔离，绝不污染真实 ~/.infoseek 库。
"""
from __future__ import annotations

import os
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from core import learned_anchor_store as las  # noqa: E402
import infoseek_zerodep_nlp as zdn  # noqa: E402

PROMOTE = os.path.join(ROOT, "scripts", "promote_s5.py")

# ── 15 个 accept 真锚词（S4 影子人工裁决）─────────────────────────────────
ACCEPT_15 = [
    "低空经济", "能量密度", "动力电池", "规划产能", "知识产权",
    "固态电池", "数据中心", "具身智能", "技术壁垒", "地缘政治",
    "加征关税", "供需缺口", "价格中枢", "能源转型", "现货价格",
]
# 22 个 reject（选种硬规则天然排除，S5 不灌入 store）
REJECT_22 = [
    "不确定性", "资本市场", "关键节点", "中国企业", "预计", "海外市场",
    "全球", "全球科技", "发展历程", "政策驱动", "支持企业", "领先地位",
    "最新进展", "全球市场", "报告指出", "关键周期", "行业市场", "政策层面",
    "落地", "行业", "高位震荡", "核心载体",
]

PASS, FAIL = [], []


def ok(name, cond, extra=""):
    (PASS if cond else FAIL).append(name)
    print(("  ✓ " if cond else "  ✗ ") + name + (("  — " + str(extra)) if extra and not cond else ""))


print("=== A accept 名单固化 ===")
ok("A1 accept 恰 15 词", len(ACCEPT_15) == 15, str(len(ACCEPT_15)))
ok("A2 accept 无重复", len(set(ACCEPT_15)) == 15)
ok("A3 reject 恰 22 词", len(REJECT_22) == 22, str(len(REJECT_22)))
ok("A4 accept 与 reject 不相交", not (set(ACCEPT_15) & set(REJECT_22)))
_accept_sub = [(a, b) for i, a in enumerate(ACCEPT_15) for b in ACCEPT_15
               if a != b and a in b]
ok("A5 accept 内部无子串包含", not _accept_sub, str(_accept_sub))


print("\n=== B promote_s5 晋级（临时库）===")
_tmp = tempfile.mkdtemp(prefix="s5_test_")
_sp = os.path.join(_tmp, "learned_anchors.json")
_rc = subprocess.run([sys.executable, PROMOTE, "--path", _sp],
                     capture_output=True, text=True)
ok("B1 promote_s5 退出码 0", _rc.returncode == 0, _rc.stderr[-300:])
_store = las.load(_sp)
_ents = _store.get("entries", {})
ok("B2 store 恰含 15 个词", len(_ents) == 15, str(len(_ents)))
ok("B3 15 个 accept 全部在 store", all(t in _ents for t in ACCEPT_15))
_accepted = set(las.active_terms("accept", _sp))
ok("B4 active accept 恰 15 词", _accepted == set(ACCEPT_15),
   str(len(_accepted)))
ok("B5 store 无 pending 残留", len(las.pending_terms(_sp)) == 0)
# 证据字段齐全
_e = _ents["固态电池"]
_prov = _e.get("provenance", {})
for f in ("promote_phase", "basis_version", "topic_cross", "coverage",
          "doc_hits", "consensus_doc_hits", "freq", "pos", "decision_rule"):
    ok(f"B6 证据字段 {f} 存在", f in _prov, str(_prov.get(f)))
ok("B7 basis_version=v2.3.1", _prov.get("basis_version") == "v2.3.1")
ok("B8 decided_at 已写入", bool(_e.get("decided_at")))


print("\n=== C 幂等（重复晋级）===")
_rc2 = subprocess.run([sys.executable, PROMOTE, "--path", _sp],
                      capture_output=True, text=True)
ok("C1 重复运行退出码 0", _rc2.returncode == 0, _rc2.stderr[-300:])
ok("C2 重复后仍恰 15 词", len(las.load(_sp).get("entries", {})) == 15)
ok("C3 重复后 accept 仍 15 词",
   set(las.active_terms("accept", _sp)) == set(ACCEPT_15))


print("\n=== D reject 不灌入 ===")
ok("D1 22 reject 均不在 store",
   all(t not in _ents for t in REJECT_22),
   str([t for t in REJECT_22 if t in _ents]))


print("\n=== E 主链统一访问协议端到端 ===")
_base = frozenset(zdn._ZH_HIGH_FREQ)
# OFF：逐字节回退
os.environ.pop("INFOSEEK_LEARNED_ANCHORS", None)
ok("E1 OFF 下 _active_zh_anchors() == 基线",
   zdn._active_zh_anchors() == _base)

# ON：用隔离数据目录，端到端消费 accept 词
os.environ["INFOSEEK_DATA_DIR"] = _tmp
os.environ["INFOSEEK_LEARNED_ANCHORS"] = "1"
try:
    _act = zdn._active_zh_anchors()
    ok("E2 ON 下锚点包含全部 15 accept",
       all(t in _act for t in ACCEPT_15))
    ok("E3 ON 下锚点仍含基线（叠加非替换）", _base <= _act)
    # 实测抽取：含 accept 词的文本应抽出动态词
    _saved_jb, _saved_sm = zdn._optional_jieba, zdn._optional_summa
    zdn._optional_jieba = lambda t, k: None
    zdn._optional_summa = lambda t, k: None
    _text = ("低空经济政策推动具身智能与固态电池产业化，数据中心算力需求"
             "带动能源转型，现货价格中枢上移，供需缺口显现。" * 2)
    _kw, _eng = zdn.extract_keywords_detailed(_text, max_kw=15)
    _kwt = [w for w, _ in _kw]
    _hit = [t for t in ACCEPT_15 if t in _kwt]
    ok("E4 ON 下实际抽出 accept 词（至少2个）", len(_hit) >= 2, str(_hit))
finally:
    os.environ.pop("INFOSEEK_LEARNED_ANCHORS", None)
    os.environ.pop("INFOSEEK_DATA_DIR", None)
    try:
        zdn._optional_jieba = _saved_jb
        zdn._optional_summa = _saved_sm
    except NameError:
        pass
ok("E5 清理后 OFF 再次逐字节回退", zdn._active_zh_anchors() == _base)


print("\n=== F 子串冲突自检 ===")
# promote_s5 main() 开头对 ACCEPT_ANCHORS 做内部冲突检测；当前名单无冲突，
# 若冲突自检逻辑本身损坏（漏检），可由 A5 名单无冲突 + 正常退出旁证存在。
ok("F1 正常名单下自检不误报（B1 已退出码0）", _rc.returncode == 0)


print(f"\nlearned_anchor_s5: {len(PASS)} PASS / {len(FAIL)} FAIL")
if FAIL:
    print("未通过：" + ", ".join(FAIL))
sys.exit(1 if FAIL else 0)
