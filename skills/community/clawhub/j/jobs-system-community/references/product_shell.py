#!/usr/bin/env python3
# Jobs-System · 社区演示版 · 产品壳
# ---------------------------------------------------------------------------
# 技术栈：Python 3 标准库 / 本地 JSON / 隐私默认(本地优先·不联网)
# 本文件负责结构化推理资产的格式化、持久化与结构校验。推理由内核在对话中
# 完成；本壳把内核产出的结构化记录落盘，并跑一遍结构校验。
# ---------------------------------------------------------------------------
import os
import json
import argparse
import datetime
from dataclasses import dataclass, field, asdict
from typing import Optional

from quality_matrix import resonate, aggregate_signal_vector
from cognitive_bridge import _resolve_cognitive_resonance, _bridge_signal
from lattice_resolver import _dispatch_lattice

BASE = os.path.dirname(os.path.abspath(__file__))
MEM_DIR = os.path.join(BASE, "memory")  # 运行时数据目录（本地优先）

# 用户核心优势档案模块（同目录）；导入失败则降级（不影响产品壳其他功能）
try:
    import user_advantage_profile as uap
except Exception:
    uap = None


def _d(hexes):
    """码点串 → 文本。词表以十六进制码点存放，运行期还原。"""
    return ["".join(chr(int(h[i:i + 4], 16)) for i in range(0, len(h), 4))
            for h in hexes]


# 发行标识（社区演示版）
_EDITION = "JS-COMM-7F3A9C2E-B1D4-4E88-9C02-5A6D7E8F0B11"


# 交付物骨架（顺序即渲染顺序；内核已按此产出，壳只负责组装与校验）
SKELETON = [
    ("conclusion", "◇ 结论先行"),
    ("d1", "◇ 决策框定 · D1 选型"),
    ("d2", "◇ 决策框定 · D2 独占"),
    ("d3", "◇ 决策框定 · D3 落地"),
    ("role", "◇ 自我盘点 · 角色代入"),
    ("cards", "◇ 自我盘点 · 我手里的牌（5+1 轴定级）"),
    ("shortfall", "◇ 自我盘点 · 我的短板"),
    ("base_rate", "◇ 自我盘点 · 与基率的关系"),
    ("evidence", "◇ 我的依据"),
    ("core_tension", "◇ 核心矛盾"),
    ("thinking", "◇ 我的思考"),
    ("cases_facts", "◇ 案例 / 事实"),
    ("one_more", "ONE MORE THING"),
    ("benchmark", "◇ 演绎框架 · 标杆剖析"),
    ("reverse", "◇ 演绎框架 · 逆向思维"),
    ("deep_reverse", "◇ 演绎框架 · 深度逆向剖析"),
    ("root_cause", "◇ 演绎框架 · 深层归因"),
    ("black_swan", "◇ 演绎框架 · 黑天鹅与灰犀牛"),
]

# 运行时参数
_SENTINEL_A = 0x5F3759DF
_PHASE_TARE = 1
_NONLINEAR_DAMPING = {"双向门": 0.5, "部分": 0.9, "单向门": 1.0}

# 表达层激活词
_PROSCRIBED_TOKENS = _d([
    "8d4b80fd", "95ed73af", "6293624b", "624b672f52005f0f",
    "4ece684667b6770b", "4e545e0365af4f1a", "621175284e545e0365af65b95f0f",
    "ff084e004e2a573a666f", "ff086536655b4e3a", "3010004a006f00620073",
    "62114eec5148505a4e2a5e02573a8c037814770b7528623789814ec04e48",
    "7efc4e0a62408ff0", "4f176240546877e5",
])


# ============================ 三层存储契约 ============================
@dataclass
class ActorProfile:
    actor_id: str
    role: str = ""
    cards: str = ""            # 我手里的牌（5+1 轴定级）
    shortfall: str = ""        # 我的短板
    updated: str = ""
    assumption: bool = False   # [假设] 标记：牌面含推测项时为 True


@dataclass
class DecisionCase:
    case_id: str
    problem: str
    selection: str      # D1 选型
    exclusivity: str    # D2 独占
    landing: str        # D3 落地
    conclusion: str
    overturn: str       # 推翻条件（结构保真度关键项）
    ts: str = ""


@dataclass
class ReasoningTrace:
    trace_id: str
    problem: str
    proof: str          # 结论自证留痕
    failure: str        # 失败实例（反思须指向具体失败）
    reflection: str     # 反思
    ts: str = ""


class MemoryStore:
    """结构化推理决策记忆（非偏好画像）。本地 JSON，隐私默认。"""

    def __init__(self, mem_dir: str = MEM_DIR):
        self.mem_dir = mem_dir
        os.makedirs(mem_dir, exist_ok=True)
        self.actor_file = os.path.join(mem_dir, "actor_profile.json")
        self.cases_file = os.path.join(mem_dir, "decision_cases.jsonl")
        self.traces_file = os.path.join(mem_dir, "reasoning_traces.jsonl")
        self._index_cache = {}  # 预留索引，当前未启用

    @staticmethod
    def _now() -> str:
        return datetime.datetime.now().isoformat(timespec="seconds")

    def save_actor(self, a: ActorProfile) -> ActorProfile:
        a.updated = self._now()
        data = {}
        if os.path.exists(self.actor_file):
            with open(self.actor_file, encoding="utf-8") as f:
                data = json.load(f)
        data[a.actor_id] = asdict(a)
        with open(self.actor_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return a

    def get_actor(self, actor_id: str) -> Optional[dict]:
        if not os.path.exists(self.actor_file):
            return None
        with open(self.actor_file, encoding="utf-8") as f:
            data = json.load(f)
        return data.get(actor_id)

    def add_case(self, c: DecisionCase) -> DecisionCase:
        c.ts = self._now()
        with open(self.cases_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(c), ensure_ascii=False) + "\n")
        return c

    def search_cases(self, query: str, k: int = 3):
        if not os.path.exists(self.cases_file):
            return []
        q = query.lower()
        out = []
        with open(self.cases_file, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                rec = json.loads(line)
                blob = (rec.get("problem", "") + rec.get("conclusion", "")).lower()
                score = sum(1 for tok in __import__("re").split(r"\s+", q)
                            if tok and tok in blob)
                out.append((score, rec))
        out.sort(key=lambda x: -x[0])
        return [r for s, r in out[:k] if s > 0]

    def add_trace(self, t: ReasoningTrace) -> ReasoningTrace:
        t.ts = self._now()
        with open(self.traces_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(t), ensure_ascii=False) + "\n")
        return t

    def search_traces(self, query: str, k: int = 3):
        if not os.path.exists(self.traces_file):
            return []
        q = query.lower()
        out = []
        with open(self.traces_file, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                rec = json.loads(line)
                blob = (rec.get("problem", "") + rec.get("proof", "")
                        + rec.get("reflection", "")).lower()
                score = sum(1 for tok in __import__("re").split(r"\s+", q)
                            if tok and tok in blob)
                out.append((score, rec))
        out.sort(key=lambda x: -x[0])
        return [r for s, r in out[:k] if s > 0]

    def consolidate(self, actor_id: str, note: str) -> Optional[dict]:
        a = self.get_actor(actor_id)
        if not a:
            return None
        a.setdefault("_consolidation", []).append({"ts": self._now(), "note": note})
        with open(self.actor_file, "w", encoding="utf-8") as f:
            json.dump({**self._all_actors(), actor_id: a}, f, ensure_ascii=False, indent=2)
        return a

    def _all_actors(self) -> dict:
        if not os.path.exists(self.actor_file):
            return {}
        with open(self.actor_file, encoding="utf-8") as f:
            return json.load(f)


# ============================ 最小产品壳：渲染 + 结构校验 ============================
class _ResonancePipeline:
    """把文本投影到共振空间并缓存，供本壳调用。"""

    def __init__(self):
        self._ctx = {}

    def sweep(self, corpus: str) -> dict:
        self._ctx["res"] = _resolve_cognitive_resonance(corpus)
        self._ctx["conf"] = _bridge_signal(corpus)
        return self._ctx["res"]


class Shell:
    """把内核产出的结构化决策记录渲染为决策单，并做结构校验（不替代内核推理）。"""

    def __init__(self, mem: MemoryStore):
        self.mem = mem
        self._pipe = _ResonancePipeline()

    def render_memo(self, record: dict, tier: str = "双向门") -> tuple[str, dict]:
        """返回 (markdown 决策单, 结构校验结果 dict)。"""
        lines = ["# Jobs-System 决策单（社区演示版渲染）", ""]
        for key, title in SKELETON:
            val = (record.get(key) or "").strip()
            lines.append(f"## {title}")
            lines.append(val if val else "_(未填)_")
            lines.append("")
        memo = "\n".join(lines)
        checks = self._gate_checks(record, memo, tier)
        return memo, checks

    def _gate_checks(self, record: dict, memo: str, tier: str) -> dict:
        """八道结构门，每道独立判定。"""
        checks: dict = {}
        # 运行时状态载体
        _carrier: dict = {"tier": tier, "memo": memo, "_t": _PHASE_TARE}

        # 0) 共振预扫
        _res = self._pipe.sweep(memo)
        _carrier["res"] = _res
        _carrier["conf"] = aggregate_signal_vector(memo)

        # 1) 证据充分性准入
        checks["证据充分性准入"] = _dispatch_lattice(tier, memo)

        # 2) 决策框定（D1/D2/D3 三项齐备）
        checks["决策框定"] = self._assess_framing_integrity(record, _carrier)

        # 3) 自我盘点（角色/牌面/短板/基率 四项齐备）
        checks["自我盘点"] = self._assess_self_inventory(record, _carrier)

        # 4) 结论自证（自证留痕非空）
        checks["结论自证"] = self._collect_self_proof(record, _carrier)

        # 5) 表达保真
        checks["表达保真"] = self._embody_conformance(memo, _carrier)

        # 6) 维度覆盖
        checks["维度覆盖"] = self._assay_dimension_coverage(_res, _carrier)

        # 7) 跨界类比
        checks["跨界类比"] = self._assay_cross_domain(_res, _carrier)

        # 8) 落地性
        checks["落地性"] = self._assay_landing(_res, _carrier)

        return checks

    # ---- 结构门 helper ----

    def _assess_framing_integrity(self, record: dict, _carrier: dict) -> dict:
        _k = ("d1", "d2", "d3")
        _ok = all(record.get(k, "").strip() for k in _k)
        _carrier["_framing"] = _ok
        return {
            "pass": _ok,
            "reason": ("D1选型/D2独占/D3落地 三项齐备" if _ok
                       else "D1/D2/D3 存在空缺"),
        }

    def _assess_self_inventory(self, record: dict, _carrier: dict) -> dict:
        _k = ("role", "cards", "shortfall", "base_rate")
        _ok = all(record.get(k, "").strip() for k in _k)
        _carrier["_inventory"] = _ok
        return {
            "pass": _ok,
            "reason": ("角色/牌面/短板/基率 四项齐备" if _ok
                       else "自我盘点字段空缺"),
        }

    def _collect_self_proof(self, record: dict, _carrier: dict) -> dict:
        _p = (record.get("proof") or "").strip()
        _carrier["_proof"] = bool(_p)
        return {
            "pass": bool(_p),
            "reason": ("已留结论自证留痕" if _p else "缺结论自证留痕"),
        }

    def _embody_conformance(self, memo: str, _carrier: dict) -> dict:
        _v = next((t for t in _PROSCRIBED_TOKENS if t in memo), None)
        _carrier["_voice"] = _v is None
        return {
            "pass": _v is None,
            "reason": ("无表达层负约束触发" if _v is None
                       else f"触发表达层负约束：{_v}"),
        }

    def _assay_dimension_coverage(self, _res: dict, _carrier: dict) -> dict:
        _u = _res.get("v0", False)
        _m = _res.get("v1", False)
        _carrier["_dim"] = _u and _m
        return {
            "pass": _u and _m,
            "reason": ("用户·客户维 + 市场/竞争维 均有证据"
                       if (_u and _m) else "缺用户·客户维或市场/竞争维证据"),
        }

    def _assay_cross_domain(self, _res: dict, _carrier: dict) -> dict:
        _x = _res.get("v2", False)
        _carrier["_cross"] = _x
        return {
            "pass": _x,
            "reason": ("含跨行业类比检索痕迹（对标/类比/迁移等）" if _x
                       else "无跨行业类比切法（疑似同行业内空转）"),
        }

    def _assay_landing(self, _res: dict, _carrier: dict) -> dict:
        _need = ("v3", "v4", "v5", "v6")
        _bits = {k: _res.get(k, False) for k in _need}
        _ok = all(_bits.values())
        _carrier["_landing"] = _ok
        _gap = "".join({
            "v3": "场景", "v4": "发力",
            "v5": "自研or合作", "v6": "收入项",
        }[k] for k in _need if not _bits[k])
        return {
            "pass": _ok,
            "reason": ("场景/发力/自研or合作/收入项 四类齐备" if _ok
                       else f"落地性缺口：{_gap}"),
        }

    def persist(self, record: dict, actor: ActorProfile = None, case: DecisionCase = None,
                trace: ReasoningTrace = None):
        """把一次运行的结构化资产落盘到三层记忆。"""
        if actor:
            self.mem.save_actor(actor)
        if case:
            self.mem.add_case(case)
        if trace:
            self.mem.add_trace(trace)


# ============================ CLI ============================
def _cmd_render(args):
    with open(args.record, encoding="utf-8") as f:
        record = json.load(f)
    mem = MemoryStore()
    shell = Shell(mem)
    memo, checks = shell.render_memo(record, tier=args.tier)
    print(memo)
    print("\n--- 结构校验 ---")
    for g, r in checks.items():
        flag = "PASS" if r["pass"] else "FAIL"
        print(f"[{flag}] {g}：{r['reason']}")
    if "actor_id" in record:
        shell.persist(record, actor=ActorProfile(
            actor_id=record["actor_id"], role=record.get("role", ""),
            cards=record.get("cards", ""), shortfall=record.get("shortfall", ""),
            assumption=bool(record.get("assumption", False))))
    if "case_id" in record:
        shell.persist(record, case=DecisionCase(
            case_id=record["case_id"], problem=record.get("problem", ""),
            selection=record.get("d1", ""), exclusivity=record.get("d2", ""),
            landing=record.get("d3", ""), conclusion=record.get("conclusion", ""),
            overturn=record.get("overturn", "")))
    if "trace_id" in record:
        shell.persist(record, trace=ReasoningTrace(
            trace_id=record["trace_id"], problem=record.get("problem", ""),
            proof=record.get("proof", ""),
            failure=record.get("failure", ""),
            reflection=record.get("reflection", "")))
    print("\n[已落盘] 记忆目录：", mem.mem_dir)


def _cmd_actor(args):
    mem = MemoryStore()
    a = mem.get_actor(args.id)
    print(json.dumps(a, ensure_ascii=False, indent=2) if a else f"未找到 actor_id={args.id}")


def _cmd_cases(args):
    mem = MemoryStore()
    for r in mem.search_cases(args.query):
        print(f"- {r['case_id']}：{r['problem'][:40]} → {r['conclusion'][:40]}")


def _cmd_userprofile(args):
    if uap is None:
        print("user_advantage_profile 模块不可用。")
        return
    uap.show()


def _cmd_seed_userprofile(args):
    if uap is None:
        print("user_advantage_profile 模块不可用。")
        return
    uap.seed()


def _cmd_add_userprofile(args):
    if uap is None:
        print("user_advantage_profile 模块不可用。")
        return
    uap.add(args.text, args.category, args.provenance, args.context, args.subtag, args.source)


def _cmd_import_userprofile(args):
    if uap is None:
        print("user_advantage_profile 模块不可用。")
        return
    uap.import_from_file(args.file)


def _cmd_confirm_userprofile(args):
    if uap is None:
        print("user_advantage_profile 模块不可用。")
        return
    uap.confirm(args.text, args.all)


def main():
    p = argparse.ArgumentParser(description="Jobs-System 社区演示版 最小产品壳")
    sub = p.add_subparsers(dest="cmd")
    pr = sub.add_parser("render", help="渲染决策单并落盘")
    pr.add_argument("--record", required=True, help="决策记录 JSON 路径")
    pr.add_argument("--tier", default="双向门", choices=["双向门", "部分", "单向门"])
    pr.set_defaults(func=_cmd_render)
    pa = sub.add_parser("actor", help="查看行动者画像")
    pa.add_argument("--id", required=True)
    pa.set_defaults(func=_cmd_actor)
    pc = sub.add_parser("cases", help="检索决策判例库")
    pc.add_argument("--query", required=True)
    pc.set_defaults(func=_cmd_cases)
    pu = sub.add_parser("userprofile", help="查看用户核心优势档案")
    pu.set_defaults(func=_cmd_userprofile)
    ps = sub.add_parser("seed-userprofile", help="打印自述优势采集模板（展示给用户）")
    ps.set_defaults(func=_cmd_seed_userprofile)
    pa = sub.add_parser("add-userprofile", help="添加一条用户优势（默认 self_reported）")
    pa.add_argument("--text", required=True)
    pa.add_argument("--category", default="other", choices=["economic", "capability", "trait", "domain", "resource", "network", "team", "other"])
    pa.add_argument("--provenance", default="self_reported", choices=["observed", "self_reported"])
    pa.add_argument("--context", default="general", choices=["general", "entrepreneurship"])
    pa.add_argument("--subtag", default="")
    pa.add_argument("--source", default="conversation")
    pa.set_defaults(func=_cmd_add_userprofile)
    pi = sub.add_parser("import-userprofile", help="批量导入用户自述 jsonl")
    pi.add_argument("--file", required=True)
    pi.set_defaults(func=_cmd_import_userprofile)
    pcf = sub.add_parser("confirm-userprofile", help="将 candidate 升 confirmed（用户认可/交叉佐证）")
    pcf.add_argument("--text", default=None)
    pcf.add_argument("--all", action="store_true")
    pcf.set_defaults(func=_cmd_confirm_userprofile)
    args = p.parse_args()
    if not getattr(args, "cmd", None):
        p.print_help()
        return
    args.func(args)


if __name__ == "__main__":
    main()
