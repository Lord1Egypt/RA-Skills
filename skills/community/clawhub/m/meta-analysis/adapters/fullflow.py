"""Fullflow HITL 控制器（spec: contracts/fullflow/v0.1.0/SPEC.md · 设计期草稿）。

把 Block A（方向/文献/数据准备）→ Block B（分析）→ Block C（撰稿）串成一条
**可交互流水线**：每个低准确度环节提供人工闸，暂停 → 展示 AI 草稿 →
人工「确认 / 修改 / 跳过」→ 把人工结果回写信封后续跑。会话状态落盘 JSON，
任意时刻可从上次闸位续跑（会话文件即审计日志）。

设计原则（用户 2026-08-31 定）：人-AI 协作，非全自动——控制器**绝不**伪造
人工决策；🔴 红线闸（A4/B4/C3/C4）只能由人放行，不接受 skip。

交互模式：agent-mediated。agent 收到 await_human 信封 → 渲染给用户 →
收集答复（HumanDecision，§6）→ 调 resume_fullflow(session_path, decision)。

已知限制（v0.1）：
- 续跑 = 重跑当前块（块层无断点续跑入口）；A1/A4 为确定性本地启发式，重跑幂等。
  例外（2026-09-10）：合并节点 A2 已批准且无 revise 时**复用缓存信封只跑 A4**，
  避免重复全库检索（~2.5 min）并保住人工在 Excel 上的复核。
- 例外（2026-09-11）：A1 修订（选题 / 检索范围 / PICOS）属「检索前最后可改点」，
  **只回写信封并停回 A1**，绝不重跑整块检索——改个检索范围不应触发全库检索，
  也不应越过 A1 批准闸；用户复核新检索范围后于 A1 批准，才触发真正的检索。
- revision 走输入参数的接缝：A2（query 检索式 / screened 裁决）与 A4
  （extracted_rows → Block B studies）；
  其余阶段的 revision 为记录后的 stage_result 事后补丁（下游已按原值计算，
  人工修订以补丁形式呈现于信封与审计日志）。

落盘格式（2026-09-20）：`save()` 会先过 `_dehydrate()` 摘掉「可由信封推导」的
重复副本（`envelope.final` / `last_view.fullflow.await.{stage_result,nha,editable_payload}`），
`load()` / `load_session_data()` 用 `_rehydrate()` 原样还原 —— 内存语义完全不变，
磁盘上省掉约 69%（实测最大会话 2382 KB → 735 KB）。代价是**直接 `json.load()` 会话
文件看到的是落盘态**（多出 `_final_idx` / `_derive_from` 两个标记键），
所以外部读会话请统一走 `load_session_data()`。
"""

import copy
import datetime
import json
import os
import re
import time
import uuid

import coze_client as cc
import block_a
import block_b
import block_c
import features  # 网页功能开关（2026-09-17：A4 数据提取隐藏 → 下载完即终点）
import session_store  # 会话落盘加速层（2026-09-20：本地先落地 + 后台回写网络盘）

SESSION_VERSION = "0.1.0"

# ---------------------------------------------------------------------------
# 停靠点配置（spec §3）
# ---------------------------------------------------------------------------
DEFAULT_PAUSE_AT = {
    "A1.topic_selection",
    "A2.literature_search",
    "A3.pdf_download",
    "A4.data_extraction",
    "B1.meta_analysis",
    "B2.grade",              # 🟡 GRADE 降级规则复核入口
    "B3.overclaim",          # 🟡 过度声明复核入口
    "B4.quality_gate",       # 🔴 红线
    "C1.draft",
    "C2.ai_review",          # 🟡 AI 评审修订复核
    "C3.ref_verify",         # 🔴 红线
    "C4.evidence_qa",        # 🔴 红线终闸
}

# 红线闸 → 阶段 id（与 coze_client._REDLINE_GATES 对齐）
GATE_TO_STAGE = {
    "extraction_review": "A4.data_extraction",
    "final_inclusion": "B4.quality_gate",
    "reference_verification": "C3.ref_verify",
    "manuscript_approval": "C4.evidence_qa",
}
STAGE_TO_GATE = {v: k for k, v in GATE_TO_STAGE.items()}

# 可被 revise 替换的 stage_result 键（spec §5 editable_payload / §6.4 接缝）
# 收录规则（2026-09-20 立，2026-09-22 按一致性审计复核）：键必须**真的能被消费** ——
#   ① 输入接缝：`_run_block` 用 `latest_revision(sid)[key]` 把它当重算参数读入
#      （A2.query / A2.screened / A3.extracted_rows / A3–A4.pdf_dir / A4.extracted_rows），
#      这类键**不必**出现在 stage_result 里；
#   ② 事后补丁：`_apply_revisions` 把 revision 补丁进信封的 stage_result（B/C 节点），
#      这类键**必须**在 stage_result 里真实存在，否则补丁静静落空。
# 只写声明不写消费 = 用户改完提交、下游纹丝不动的静默失效，比不提供该能力更糟。
#
# 2026-09-22 删键（一致性审计 P1-8：两侧都无入口、后端也不消费 → 删了零功能损失）：
#   B1 的 data / params / figure —— stage_result 里根本没有这三个键；
#   B2 的 risk_of_bias / indirectness / inconsistency / imprecision / publication_bias
#       —— 真实键是 grade / domain_ratings / downgrades / reasons；那五个是 B2 的**入参名**，
#          不是返回键，页面无面板、后端也不读 revision；
#   C2 的 manuscript / C3 的 references / C4 的 manuscript —— stage_result 里均无此键
#       （C3 是 ref_verifications / refs_verified，C4 是 qa / evidence_table）。
#   C1 保留 sections（stage_result 真实存在，可事后补丁）。
EDITABLE_KEYS = {
    "A1.topic_selection": ["report", "include_reviews", "sources"],
    "A2.literature_search": ["query", "screened"],
    "A3.pdf_download": ["pdf_dir", "extracted_rows"],
    "A4.data_extraction": ["extracted_rows", "pdf_dir"],
    "B1.meta_analysis": ["pairwise", "nma"],
    # B3.overclaim 刻意**不**收录（2026-09-20 移除）：
    #   claims_text 是 B3 的**输入**（由 _build_claims_text 从选题 + A2 文献标题/摘要派生），
    #   不在 B3 的 stage_result 里 → 原来的 editable_payload 恒为 {}；
    #   且 _run_block 的 B 分支每次都重拼文本、从不读 latest_revision("B3.overclaim")
    #   → 收录了也传不下去。B3 按裁定保持 gate_type="auto"（不可修订）。
    #   若将来要开放「人工补充待扫描文本」，需同时：① 在本表收录；② 在 _run_block B 分支
    #   加 latest_revision 消费；③ 在 form_schema 给 B3 一个 revision_key=claims_text 的面板。
    "B4.quality_gate": ["report"],
    "C1.draft": ["manuscript", "sections"],
}

ACTIONS = {"approved", "revised", "skipped", "rejected"}
_BLOCK_SEQ = ["A", "B", "C"]


def _now():
    return datetime.datetime.now(datetime.timezone.utc).astimezone().isoformat(timespec="seconds")


# ---------------------------------------------------------------------------
# 落盘去重（2026-09-20 提速，语义零改动）
#
# 实测一个 104 篇 studies 的会话（2382 KB）里，有 **1197 KB / 50.3%** 是纯重复：
#
#   blocks.A.envelope.final     513.1 KB  ≡ blocks.A.envelope.stages[-1]（逐字节相同）
#   last_view.fullflow.await    684.3 KB  ≡ 同一份 envelope.final 的三个字段
#       ├─ stage_result         333.9 KB  ≡ final.stage_result
#       ├─ nha                  178.0 KB  ≡ final.next_human_action
#       └─ editable_payload     171.0 KB  ≡ {k: stage_result[k] for k in EDITABLE_KEYS[sid]}
#
# 而 `last_view` 与 `_final_idx` 的目的地只在本模块内部被 `_view()` 消费，
# 前端从不读 `blocks` / `last_view`（只读 `/api/session` 重建后的 state）。
# 于是落盘时摘掉这些**可推导副本**，load 时原样还原 → 文件 2382 → 1185 KB，
# 每步的 read / parse / serialize / 下发全部减半。
#
# 安全性：只摘「能逐字节对上」的副本。任何一处对不上（例如 editable_payload
# 与当前 EDITABLE_KEYS 规则不符）就原样保留，宁可文件大一点也不丢字段。
# ---------------------------------------------------------------------------
_DERIVE_KEYS = ("stage_result", "nha", "editable_payload")


def load_session_data(path):
    """读取会话文件并还原落盘去重（**外部工具读会话请一律走这里**）。

    直接 `json.load()` 看到的是落盘态：`envelope._final_idx` 与
    `last_view.fullflow.await._derive_from`（见 `_dehydrate`），
    缺 `final` / `await.stage_result` / `await.nha` / `await.editable_payload`。
    这几个键都是**同一份数据的副本**，`_rehydrate` 会按记录原样补回。
    """
    with open(path, "rb") as f:
        return _rehydrate(json.loads(f.read()))


def _canon_json(obj):
    """稳定序列化，仅用于「是否逐字节相同」的比对。"""
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, default=str)


def _same(a, b):
    """a 与 b 是否**同一份数据**（可安全地只留一份）？

    三层短路，按成本从低到高（2026-09-20 提速）：

    ① 身份：`_view()` 塞进 `await` 的 stage_result / next_human_action 就是
       `envelope.final` 里**同一个对象**，所以内存里恒为 `a is b` → 零成本。
    ② 值比较：从磁盘读回后再存时引用已被 json 拆开，退到 C 层的 `==`（对
       几十万字节的 dict 也就零点几毫秒）。不等就直接否决。
    ③ 逐字节确认：只在值相等时做一次规范化序列化比对，守住「摘掉的一定逐字节
       相同」这个前提 —— 否则 `1 == 1.0` / `True == 1` 这类等价会让还原出的
       类型和原值不同。

    没有这三层短路时，全程硬做 `_canon_json()` 对比，实测 `_dehydrate()` 要
    **35 ms**（占 save() 的 87%）；加了短路后掉到 1~2 ms。
    """
    if a is b:
        return True
    if a is None or b is None:
        return False
    try:
        if a != b:
            return False
    except Exception:  # noqa: BLE001 — 类型怪异时保守判定为「不同」
        return False
    return _canon_json(a) == _canon_json(b)


def _same_editable(got, expect):
    """`editable_payload` 的专用比对。

    `_view()` 用 `{k: stage_result[k] for k in ...}` 现搭一个 dict —— 外层 dict
    是新对象，但**值仍是原引用**。所以先比键集合 + 值身份，命中就完全不用序列化
    （这份 payload 在 A2 上就有 171 KB）。
    """
    if got is expect:
        return True
    if not isinstance(got, dict):
        return False
    if set(got) != set(expect):
        return False
    if all(got[k] is expect[k] for k in expect):
        return True
    return _same(got, expect)


def _dehydrate(data):
    """返回可落盘的浅拷贝：摘掉可由信封推导的重复副本（不修改入参）。"""
    if not isinstance(data, dict):
        return data
    out = dict(data)

    blocks = out.get("blocks")
    if isinstance(blocks, dict):
        blocks = dict(blocks)
        out["blocks"] = blocks
    finals = {}
    if isinstance(blocks, dict):
        for b in _BLOCK_SEQ:
            blk = blocks.get(b)
            if not isinstance(blk, dict):
                continue
            blk = dict(blk)
            blocks[b] = blk
            env = blk.get("envelope")
            if isinstance(env, dict):
                env = dict(env)
                blk["envelope"] = env
                finals[b] = env.get("final")

    # (1) last_view.fullflow.await 的三个推导键
    lv = out.get("last_view")
    ff = lv.get("fullflow") if isinstance(lv, dict) else None
    aw = ff.get("await") if isinstance(ff, dict) else None
    if isinstance(aw, dict) and isinstance(aw.get("stage_result"), (dict, list)):
        hit = None
        for b, fin in finals.items():
            if not isinstance(fin, dict) or fin.get("stage_result") is None:
                continue
            if not _same(aw.get("stage_result"), fin.get("stage_result")):
                continue
            if not _same(aw.get("nha"), fin.get("next_human_action")):
                continue
            hit = b
            break
        if hit:
            sid = aw.get("stage_id")
            sr = aw.get("stage_result") or {}
            expect_ed = {k: sr[k] for k in EDITABLE_KEYS.get(sid, []) if k in sr}
            # editable_payload 必须与当前规则完全一致才可摘（否则保留原值防丢）
            if _same_editable(aw.get("editable_payload"), expect_ed):
                aw = dict(aw)
                keys = [k for k in _DERIVE_KEYS if k in aw]
                for k in keys:
                    aw.pop(k, None)
                aw["_derive_from"] = {"block": hit, "keys": keys}
                ff = dict(ff)
                ff["await"] = aw
                lv = dict(lv)
                lv["fullflow"] = ff
                out["last_view"] = lv

    # (2) 各块 envelope.final ≡ stages[k]
    if isinstance(blocks, dict):
        for b in _BLOCK_SEQ:
            env = (blocks.get(b) or {}).get("envelope") if isinstance(blocks.get(b), dict) else None
            if not isinstance(env, dict):
                continue
            fin = env.get("final")
            stages = env.get("stages")
            if fin is None or not isinstance(stages, list) or not stages:
                continue
            k = next((i for i, s in enumerate(stages) if _same(s, fin)), None)
            if k is None:
                continue
            env.pop("final", None)
            env["_final_idx"] = k
    return out


def _rehydrate(data):
    """加载后原地还原 `_dehydrate` 摘掉的字段（顺序：先 final，再 await）。

    顺带做一次**引用归一**：把 `envelope.final` 换成 `stages[k]` 本身。
    旧格式的会话文件里 `final` 与 `stages[k]` 是 json 解析出的两份独立对象
    （值相同、身份不同），于是每次 `save()` 的 `_dehydrate` 都得退到逐字节确认
    （实测 A2 会话每次 ~35 ms）。在本函数里归一一次之后，下游全部走身份短路。
    """
    if not isinstance(data, dict):
        return data
    blocks = data.get("blocks") or {}
    for b in _BLOCK_SEQ:
        blk = blocks.get(b) if isinstance(blocks, dict) else None
        env = blk.get("envelope") if isinstance(blk, dict) else None
        if not isinstance(env, dict):
            continue
        stages = env.get("stages")
        k = env.pop("_final_idx", None)
        if k is not None:
            if isinstance(stages, list) and isinstance(k, int) and 0 <= k < len(stages):
                env["final"] = stages[k]
            continue
        fin = env.get("final")
        if fin is not None and isinstance(stages, list) and stages:
            j = next((i for i, s in enumerate(stages) if _same(s, fin)), None)
            if j is not None:
                env["final"] = stages[j]
    lv = data.get("last_view")
    ff = lv.get("fullflow") if isinstance(lv, dict) else None
    aw = ff.get("await") if isinstance(ff, dict) else None
    if isinstance(aw, dict):
        spec = aw.pop("_derive_from", None)
        if isinstance(spec, dict):
            b = spec.get("block")
            keys = spec.get("keys") or []
            blk = blocks.get(b) if isinstance(blocks, dict) else None
            fin = (blk.get("envelope") or {}).get("final") if isinstance(blk, dict) else None
            fin = fin if isinstance(fin, dict) else {}
            if "stage_result" in keys:
                aw["stage_result"] = fin.get("stage_result")
            if "nha" in keys:
                aw["nha"] = fin.get("next_human_action") or {}
            if "editable_payload" in keys:
                sid = aw.get("stage_id")
                sr = aw.get("stage_result") or {}
                aw["editable_payload"] = {k: sr[k] for k in EDITABLE_KEYS.get(sid, [])
                                          if k in sr}
    return data


# ---------------------------------------------------------------------------
# 会话持久化（spec §7）
# ---------------------------------------------------------------------------
class FullflowSession:
    """会话状态（schema §7）：加载/保存/游标推进。文件即审计日志。"""

    def __init__(self, data, path):
        self.data = data
        self.path = path

    # -- 构造 ---------------------------------------------------------------
    @classmethod
    def new(cls, topic, cfg, session_dir):
        pid = "ff-" + uuid.uuid4().hex[:12]
        data = {
            "session_version": SESSION_VERSION,
            "pipeline_id": pid,
            "topic": topic,
            "created_at": _now(),
            "updated_at": _now(),
            "cfg": cfg,
            "cursor": {"block": "A", "stage_id": None, "await_kind": None},
            "blocks": {b: {"envelope": None, "status": "pending"} for b in _BLOCK_SEQ},
            "human_decisions": [],
            "handoff": {},
        }
        os.makedirs(session_dir, exist_ok=True)
        return cls(data, os.path.join(session_dir, f"fullflow_session_{pid}.json"))

    @classmethod
    def load(cls, path):
        # 优先本地副本（本进程刚写过 / 有未回写修订）；否则读原文件。
        # 读网络盘 2.4MB ≈ 33 ms，可接受；写网络盘 ≈ 272 ms，才是瓶颈（见 session_store）。
        text = session_store.read_text(path)
        if text is None:
            with open(path, "rb") as f:
                data = json.loads(f.read())
        else:
            data = json.loads(text)
        return cls(_rehydrate(data), path)

    # -- 持久化（原子写：临时文件 + rename） --------------------------------
    def save(self):
        """落盘。**先 dumps 再单次 write**，并改由 `session_store` 落地（2026-09-20 提速）。

        两处历史瓶颈，分两次修的：

        ① `json.dump(obj, f, indent=2)` 是 token 级写出：一份 2.3MB 会话（A2 含 104 篇
           studies + abstracts）会触发 ~11 万次 `write()` 调用 → 改 `json.dumps` 后单次
           写出，实测 2.5 s → 0.3 s。

        ② 剩下的 0.3 s 几乎全是**网络盘写延迟**（skill 目录是 SMB 软链接：写 2.4MB
           实测 272.3 ms，本机 C: 仅 2.6 ms，差 105 倍），而一次打回/回退要落盘
           3~5 次 → 纯 I/O 吃掉 8~13 秒。现在改成 `session_store.write_text()`：
           本地镜像同步落地（几毫秒），网络盘那份由后台单写者按序回写。

        落盘内容先过 `_dehydrate()` 去掉重复副本；`load()` 用 `_rehydrate()` 原样还原，
        因此**读写语义与文件可读性（indent=2 / ensure_ascii=False）完全不变**。
        """
        self.data["updated_at"] = _now()
        payload = json.dumps(_dehydrate(self.data), ensure_ascii=False, indent=2)
        session_store.write_text(self.path, payload,
                                 updated_at=self.data["updated_at"])

    # -- 便捷视图 -----------------------------------------------------------
    @property
    def cursor(self):
        return self.data["cursor"]

    def effective_pause_at(self):
        """cfg.pause_at 减去被人工 skipped 的软停阶段（skip = 本会话不再停靠）。"""
        skipped = {d["stage_id"] for d in self.data["human_decisions"]
                   if d.get("action") == "skipped" and d.get("stage_id")}
        return set(self.data["cfg"].get("pause_at") or []) - skipped

    def decisions_for_block(self, letter):
        """本块已放行凭据列表 → 传给块层 human_decision。

        spec §6.3 降级映射：approved 原样传；revised 的 revision 已由控制器
        写进输入参数/补丁（_extraction_input / _apply_revisions），此处同样
        降级为 approved 凭据放行闸——块层零改动消费人工修改。
        """
        # 阶段 id 形如 "A1.topic_selection"（块字母 + 序号），按首字母归块
        # 已作废（invalidated）的凭据不再放行闸：回退/打回后闸必须重新问人。
        return [{"stage_id": d["stage_id"], "action": "approved"}
                for d in self.data["human_decisions"]
                if d.get("action") in ("approved", "revised")
                and not d.get("invalidated")
                and isinstance(d.get("stage_id"), str)
                and d["stage_id"][:1] == letter]

    def revisions_for_block(self, letter):
        """本块各阶段最新 revision（stage_id → revision dict）；已作废的不计入。"""
        out = {}
        for d in self.data["human_decisions"]:
            if (d.get("action") == "revised" and isinstance(d.get("stage_id"), str)
                    and not d.get("invalidated")
                    and d["stage_id"][:1] == letter
                    and isinstance(d.get("revision"), dict)):
                out[d["stage_id"]] = d["revision"]
        return out

    def latest_revision(self, stage_id):
        """某阶段最近一次带 revision 的人工决策的 revision dict（不限 action：
        approved 亦可携带 revision，如 A1 的 include_reviews 开关随批准一并提交）。
        已作废的不计入；无则返回 None。"""
        rev = None
        for d in self.data["human_decisions"]:
            if (d.get("stage_id") == stage_id and isinstance(d.get("revision"), dict)
                    and not d.get("invalidated")):
                rev = d["revision"]
        return rev

    def invalidate_decisions(self, from_stage_id):
        """作废「from_stage_id 及其之后所有阶段」的人工凭据（回退语义）。

        为什么必须做（2026-09-18 实测 bug）：`rewind()` 只清块信封、**刻意保留
        human_decisions（审计不丢）**，而 `decisions_for_block()` 会把历史
        approved 当凭据重放 → 重跑时同一道闸被历史凭据直接放行，回退点根本不停。
        典型表现：打回到 A1 却因为 A1 的旧 approved 仍在而被跳过，整块检索重跑
        约 2 分钟后又停在 A2 —— 用户看到「打回按钮不起作用 / 一直停在原地」。

        处理方式：**只在记录上打 invalidated 标记，不删除记录**。审计（谁在何时
        批准过什么）完整保留，且能看出是哪次回退使其失效；同时
        decisions_for_block / revisions_for_block / latest_revision 一致忽略作废项，
        避免旧 revision（如人工 Excel 裁决、手改检索式）被重新注入覆盖新决策。

        返回被作废的记录条数。
        """
        key0 = _stage_order_key(from_stage_id)
        if key0 is None:
            return 0
        n = 0
        for d in self.data["human_decisions"]:
            k = _stage_order_key(d.get("stage_id"))
            if k is None or k < key0 or d.get("invalidated"):
                continue
            d["invalidated"] = {"by": "rewind", "to": from_stage_id, "at": _now()}
            n += 1
        return n

    def record_decision(self, decision):
        rec = {
            "decision_id": decision.get("decision_id") or f"d-{uuid.uuid4().hex[:8]}",
            "stage_id": decision.get("stage_id"),
            "gate": decision.get("gate"),
            "action": decision.get("action"),
            "revision": decision.get("revision"),
            "note": decision.get("note"),
            "decided_by": decision.get("decided_by") or "user",
            "decided_at": decision.get("decided_at") or _now(),
        }
        self.data["human_decisions"].append(rec)
        return rec

    def rewind(self, target_block):
        """Phase 2：回退到 target_block 起点，清空该块及下游块信封/状态，重置 cursor。
        保留 human_decisions（审计不丢）。块内为整体重跑（无块内断点）。
        target_block 可为块字母或 stage_id，自动解析为块字母。

        handoff 只在回退进 **A 块**时清空（2026-09-20 修复）。handoff 的全部键都由 A 块
        产出（`studies_for_b`：A3 上传 / A4 抽取；`ref_sections`：A3/A4 已落盘 PDF 的章节
        切片；`merged_json`：A2 检索产物），对 B/C 而言它是**上游**产物而非待作废的下游结果。
        原先无条件 `handoff = {}` 造成两个后果，回退到 B1 时最明显：
          ① **丢数据**：`_run_block("B")` 读 `handoff.studies_for_b` 得 0 行 → B1 停靠在
             「待补数据」，用户必须重新上传，回退等于白退；
          ② **白重算**：Block C 的 `_extract_c_grounding` 见 `ref_sections` 为空 → 重抽
             全部已缓存 PDF 的章节，实测 ~2.7 s/篇（59 篇 ≈ 2.5 min），纯属重复劳动。
        回退进 A 时清空仍是对的（A 会重跑并重新产出这些键）。
        """
        letter = _block_of(target_block)
        if letter is None:
            raise ValueError(f"无法解析回退目标块：{target_block!r}")
        affected = _downstream_blocks(letter)
        for b in affected:
            # A 块例外（2026-09-20）：**保留信封**作为「检索复用源」，只把状态置回 pending。
            # `run_block_a` 会比对检索指纹（检索式/年限/上限/数据源/纳入综述）——
            # 一致就复用已检索的 studies 与 ct-registry 查重探针，跳过联网重跑
            # （A1 探针 timeout 180s + A2 全库检索约 2 分钟）；不一致（改了任何检索输入）
            # 则照旧走真实联网检索。下游块（B/C）仍原样清空信封，因为它们的重跑必须从头来。
            # 强制刷新时这里同样被清空（见 rewind_fullflow 的 force_refresh）。
            if b == "A":
                self.data["blocks"][b]["status"] = "pending"
                self.data["blocks"][b].setdefault("envelope", None)
            else:
                self.data["blocks"][b] = {"envelope": None, "status": "pending"}
        if letter == "A":
            self.data["handoff"] = {}
        self.data["cursor"] = {"block": letter, "stage_id": None, "await_kind": None}
        self.save()
        return affected


# ---------------------------------------------------------------------------
# 块运行（控制器 → 三块驱动器；复用既有闸语义，不重造）
# ---------------------------------------------------------------------------
def _run_block(letter, sess, debug, on_line=None, on_a4_event=None):
    cfg = sess.data["cfg"]
    creds = sess.decisions_for_block(letter) or None
    pause = sess.effective_pause_at() or None
    if letter == "A":
        # live 路径默认开启 A4 自动落盘（auto_fetch=True）：文献集（A2）门控 → 下载 OA PDF →
        # 抽取 2×2 草稿。extracted_rows 经 handoff.studies_for_b 直送 B1。
        # extraction_table 为 None（演示/人工数据路径）时走 Path A，否则走 Path B 自动抽取。
        # Phase 2 真接缝：把本块 revision 解成覆盖参数注入块内重算（A2.query / A2.screened，
        # 后者即 Excel 回传的裁决），使 revise 真正 propagate 到下游（A4 / studies_for_b /
        # Block B），而非仅补丁信封。
        revs = sess.revisions_for_block("A")
        # 合并节点「文献集」（A2）承载两个可编辑键：query=改检索式、screened=裁决回传。
        a2_rev = revs.get("A2.literature_search") or {}
        # 旧会话兼容：A2/A3 合并前的 A3 修订（screened）仍要能消费
        a3_rev = revs.get("A3.screening") or {}
        if not a2_rev.get("screened") and a3_rev.get("screened"):
            a2_rev = {**a2_rev, "screened": a3_rev.get("screened")}
        # A1 页面「纳入综述」开关随批准提交（action=approved + revision），
        # 覆盖启动配置的 include_reviews —— A1 是选题闸，此处是检索前最后可改点。
        a1_rev = sess.latest_revision("A1.topic_selection") or {}
        include_reviews = a1_rev.get("include_reviews", cfg.get("include_reviews", False))
        if not isinstance(include_reviews, bool):
            include_reviews = bool(include_reviews)
        # A1 页面「检索数据源」随批准提交，覆盖启动配置的 sources（选题阶段
        # 用户增减的源子集；None/空 → 用核心源 CORE_SOURCES 全量）。
        _src = a1_rev.get("sources", cfg.get("sources")) or list(block_a.CORE_SOURCES)
        sources = [str(s) for s in _src if str(s).strip()]
        # 合并节点已批准且无任何 A2/A3 修订 → 仅跑 A4，复用缓存的 A1/A2，避免整块重跑。
        # 修掉「批准即重跑检索」（2026-09-10）：原实现只在 **A3 已批准**时才复用，
        # 故批准 A2 会整块重算（含全库检索），既耗时 ~2.5 分钟又作废人工的 Excel 复核。
        cached_env = sess.data["blocks"]["A"].get("envelope")
        a2_approved = bool(creds) and any(
            block_a._decision_approves(d, "A2") for d in
            (creds if isinstance(creds, list) else [creds]))
        # A2 已批准且无 A2 修订 → 复用缓存信封，直接跑 A3（PDF 下载）/ A4（提取），
        # 避免重复全库检索（~2.5 min）并保住人工在 Excel 上的复核。
        start_stage = ("A3" if (a2_approved and not a2_rev and cached_env)
                       else None)
        # 本地 PDF 路径（修订键 pdf_dir，或启动配置 cfg.pdf_dir）→ 注入 run_block_a
        # 作为 PDF 缓存目录，优先消费本地 PDF。A3（下载）与 A4（提取）两个节点都可登记。
        a3_rev = revs.get("A3.pdf_download") or {}
        a4_rev = revs.get("A4.data_extraction") or {}
        pdf_dir = a3_rev.get("pdf_dir") or a4_rev.get("pdf_dir") or cfg.get("pdf_dir")
        return block_a.run_block_a(
            sess.data["topic"], max_results=cfg.get("max_results", 50),
            year_from=cfg.get("year_from"),
            extraction_table=_extraction_input(sess),
            human_decision=creds, pause_at=pause, debug=debug,
            out_dir=cfg.get("session_dir", "."),
            auto_fetch=True,
            auto_fetch_dir=cfg.get("session_dir"),
            pdf_dir=pdf_dir,
            pdf_email=cfg.get("pdf_email"),
            max_attempts=cfg.get("max_attempts", 12),
            inclusion_hints=None,
            override_query=a2_rev.get("query"),
            a1_report_override=_a1_report_search_override(sess),
            override_screened=a2_rev.get("screened"), on_line=on_line,
            on_a4_event=on_a4_event,
            start_stage=start_stage,
            # 始终透传缓存信封（2026-09-20）：`run_block_a` 在 start_stage=None 时会拿它做
            # **检索指纹比对** —— 指纹一致（检索式/年限/上限/数据源/纳入综述全未变）就复用
            # 上次 studies，跳过全库检索；不一致才真实联网重跑。覆盖两个此前会白等 ~2 分钟的路径：
            #   ① 回退进 A 块（rewind 保留信封作复用源）；② 只回传裁决（screened）的 A2 修订。
            cached_envelope=cached_env,
            include_reviews=include_reviews, sources=sources)
    if letter == "B":
        # B3 过度声明检测：拼 claims_text（从 A2 检索结果标题/摘要 + 选题）
        # 修复 2026-09-17：此前未传 claims_text → detect_overclaims("") 文本模式全失效
        # 2026-09-20：同时回收来源说明（claims_meta），供 B3 页面自证扫了哪些文本
        _claims_text, _claims_meta = _build_claims_text(sess, with_meta=True)
        return block_b.run_block_b(
            sess.data["handoff"].get("studies_for_b") or [],
            effect_measure=cfg.get("effect_measure", "OR"),
            nma=cfg.get("nma", False),
            human_decision=creds, pause_at=pause, debug=debug,
            claims_text=_claims_text, claims_meta=_claims_meta)
    # C 档：把 Block A 的真实素材（文献集/PICOS/PRISMA 流/检索源 + PDF 章节切片）透传给 C1 写稿
    _ground = _extract_c_grounding(sess)
    # 真实文献接地（2026-09-22）：快速通道（draft / 无 A2 文献集）没有上游文献可引，
    # 此时按研究主题**真实检索** Europe PMC，把真实论文喂给 C1 —— 否则初稿的
    # 背景/讨论/参考文献只剩 "(to be added)" 占位符。检索失败静默降级，不阻断流程。
    _topic_en = (sess.data.get("topic_en") or "").strip() or None
    # 中文主题且未给英文题名 → 自动翻译（2026-09-22 用户纠正：技能上下文里 LLM 会翻译，
    # 网页端是独立进程、Agent 不在回路，必须自己补这一步）。翻不出来则维持原状，
    # 由 block_c.evidence_status 的 no_topic_en 提示兜底（不阻断）。
    if not _topic_en:
        try:
            import topic_translate
            _auto_en = topic_translate.translate_to_english(sess.data.get("topic") or "")
            if _auto_en:
                _topic_en = _auto_en
                sess.data["topic_en"] = _auto_en
                sess.data["topic_en_source"] = "auto"
        except Exception:  # noqa: BLE001 - 翻译不可用不能阻断流程
            pass
    # ── 证据来源优先级（2026-09-22 用户要求「C1 允许上传自备文献」）──
    # ① 作者自备文献（C1 上传的 Excel 清单 / PDF 打包）—— 用户自己筛过改过，
    #    权威性最高；有它就不再联网检索（既省时，也避免用检索结果盖掉用户的清单）。
    # ② 上游 A2 文献集（_ground 里已带）。
    # ③ Europe PMC 自动检索（draft / 快速通道无上游文献时的兜底）。
    _user_ev = (sess.data.get("c_grounding") or {}).get("user_evidence")
    _evidence = _user_ev or _ground.get("evidence")
    if not _user_ev and not _ground["studies_list"] and _evidence is None:
        _evidence = _probe_evidence_for_draft(sess, _topic_en)
    # 检索层的异常（断网/限流/接口报错）单独取出，交给 C1 生成「为什么没有文献」
    # 的提示文案 —— evidence=None 与「检索失败」是两回事，必须区分（2026-09-22）。
    # 用作者自备文献时，历史上那次检索失败与本稿无关，不能带进提示（否则稿子明明
    # 引的是用户清单，提示条却在报「Europe PMC 检索失败」）。
    _ev_err = None if _user_ev else (sess.data.get("c_grounding") or {}).get("evidence_error")
    return block_c.run_block_c(
        topic=sess.data["topic"], b_env=sess.data["blocks"]["B"].get("envelope"),
        human_decision=creds, pause_at=pause,
        studies_list=_ground["studies_list"], prisma_flow=_ground["prisma_flow"],
        picos=_ground["picos"], search_info=_ground["search_info"],
        rob_summary=_ground["rob_summary"], merged_json=_ground["merged_json"],
        ref_sections=_ground.get("ref_sections"),
        topic_en=_topic_en, evidence=_evidence, evidence_error=_ev_err,
        language=sess.data.get("cfg", {}).get("language", "zh"))


def _probe_evidence_for_draft(sess, topic_en=None):
    """draft / 快速通道缺少 A2 文献集时，用真实 Europe PMC 检索给 C1 接地。

    - 只在**没有**上游文献集时触发（有 A2 结果时优先用真实的 A2 文献）。
    - 结果按会话缓存（sess.data["c_grounding"]["evidence"]），避免重跑时重复出站。
    - 任何失败（断网 / 主题过窄 / 中文主题无命中）都返回 None：这是 best-effort
      接地层，**不是硬闸门**，C1 必须能在没有它的情况下照样出稿。
    """
    cached = (sess.data.get("c_grounding") or {}).get("evidence")
    if cached:
        return cached
    topic = (topic_en or sess.data.get("topic") or "").strip()
    if not topic:
        return None
    try:
        import literature_probe
        ev = literature_probe.search_evidence(topic, n_primary=10, n_synthesis=5)
    except Exception as e:  # noqa: BLE001 - best-effort grounding, never fatal
        sess.data.setdefault("c_grounding", {})["evidence_error"] = str(e)
        return None
    sess.data.setdefault("c_grounding", {})["evidence"] = ev
    return ev


def _build_claims_text(sess, with_meta=False):
    """为 B3 过度声明检测拼 claims_text（从 A2 检索结果 + 选题）。

    修复 2026-09-17：此前 fullflow 路径未传 claims_text → detect_overclaims("") 只能做
    CI 跨零统计，12 种文本模式（OC1/OC3/OC4/OC6-OC12）全部失效。

    2026-09-20：新增 with_meta —— B3 是**自动**节点，页面上「0 命中」既可能是真没风险、
    也可能是压根没扫到文本（A 块被跳过 / 无摘要）。故同时回收这段文本的**来源说明**
    （谁拼的、几篇文献、多少字），透传进 B3 stage_result 供页面自证，避免误读成「已排查干净」。
    """
    parts = []
    meta = {"source": "", "topic_included": False, "studies_total": None,
            "n_studies": 0, "n_titles": 0, "n_abstracts": 0,
            "abstract_chars": 0, "total_chars": 0}
    topic = sess.data.get("topic")
    if topic:
        parts.append(str(topic))
        meta["topic_included"] = True
    a_env = (sess.data.get("blocks") or {}).get("A", {}).get("envelope")
    n_studies = n_titles = n_abstracts = abs_chars = 0
    if isinstance(a_env, dict):
        stages = a_env.get("stages", [])
        by_id = {s["stage"]["id"]: s for s in stages if isinstance(s, dict) and "stage" in s}
        a2 = by_id.get("A2")
        if a2:
            studies = (a2.get("stage_result") or {}).get("studies") or []
            meta["studies_total"] = len(studies)
            for s in studies[:20]:
                if isinstance(s, dict):
                    t = s.get("title")
                    if t:
                        parts.append(str(t))
                        n_titles += 1
                    ab = s.get("abstract") or s.get("abstract_snippet")
                    if ab:
                        parts.append(str(ab)[:500])
                        n_abstracts += 1
                        abs_chars += len(str(ab)[:500])
            n_studies = min(len(studies), 20)
    text = "\n".join(parts)
    meta.update({"n_studies": n_studies, "n_titles": n_titles, "n_abstracts": n_abstracts,
                 "abstract_chars": abs_chars, "total_chars": len(text)})
    if not text.strip():
        meta["source"] = ("本次没有可比对文本（A 块检索结果为空或已被跳过）——"
                          "12 类文本模式全部无从触发，0 命中不代表「无风险」。")
    else:
        meta["source"] = (
            "选题 + A2 检索到的文献标题/摘要（最多前 20 篇）。"
            "注意：扫的是上游文献的措辞，不是你写的稿子（C1 初稿在 B3 之后才生成）。"
        )
    return (text, meta) if with_meta else text


def _extract_c_grounding(sess):
    """从 Block A 信封抽取 C1 写稿所需的真实素材（文献集 / PICOS / PRISMA 流 / 检索源 / PDF 章节切片）。

    返回 dict(studies_list, prisma_flow, picos, search_info, rob_summary, merged_json, ref_sections)。
    仅透传确实存在的字段；缺失时留空，C1 优雅降级（相应段标记「待补」）。
    draft 快进模式无 A 信封时全部为 None。
    """
    a_env = (sess.data.get("blocks") or {}).get("A", {}).get("envelope")
    out = {"studies_list": None, "prisma_flow": None, "picos": None,
           "search_info": None, "rob_summary": None, "merged_json": None,
           "ref_sections": None}
    if not isinstance(a_env, dict):
        return out
    stages = a_env.get("stages", [])
    by_id = {s["stage"]["id"]: s for s in stages if isinstance(s, dict) and "stage" in s}
    a1 = by_id.get("A1")
    if a1:
        out["picos"] = (a1.get("stage_result") or {}).get("picos")
    a2 = by_id.get("A2")
    if a2:
        sr = a2.get("stage_result") or {}
        studies = sr.get("studies") or []
        if studies:
            out["studies_list"] = studies
        n = sr.get("n")
        n_screened = sr.get("n_screened")
        cov = sr.get("coverage") or {}
        identified = cov.get("total") if isinstance(cov, dict) else None
        if identified is not None or n_screened is not None or n is not None:
            prisma = {}
            if identified is not None:
                prisma["identified"] = identified
            if n_screened is not None:
                prisma["screened"] = n_screened
            if n is not None:
                prisma["included"] = n
            if isinstance(n_screened, int) and isinstance(n, int):
                prisma["excluded"] = max(n_screened - n, 0)
            out["prisma_flow"] = prisma
        sources = (cov.get("sources") if isinstance(cov, dict) else None) or \
                  (sr.get("params") or {}).get("sources")
        if sources:
            out["search_info"] = {"databases": [str(x) for x in sources]}
    mj = (sess.data.get("handoff") or {}).get("merged_json") or \
         (sess.data.get("cfg") or {}).get("merged_json")
    if mj:
        out["merged_json"] = mj

    # rob_summary：B4 产出的 RoB 汇总（从 B 块 stages 抽取）
    b_env = (sess.data.get("blocks") or {}).get("B", {}).get("envelope")
    if isinstance(b_env, dict):
        b_stages = b_env.get("stages", [])
        b_by_id = {s["stage"]["id"]: s for s in b_stages if isinstance(s, dict) and "stage" in s}
        b4 = b_by_id.get("B4.quality_gate")
        if b4:
            b4_sr = b4.get("stage_result") or {}
            rob = b4_sr.get("rob_summary") or b4_sr.get("risk_of_bias")
            if rob:
                out["rob_summary"] = rob

    # ref_sections：从 A4 或 A3 缓存抽取章节切片（写作风格参考）
    _cached_sections = (sess.data.get("handoff") or {}).get("ref_sections")
    if _cached_sections:
        out["ref_sections"] = _cached_sections
    else:
        # 尝试从 pdf_cache 目录现抽
        _pdf_dir = block_a.A4_PDF_CACHE_DIR
        _studies = out.get("studies_list")
        if _studies and _pdf_dir and os.path.isdir(_pdf_dir):
            _extracted = block_a._a4_extract_section_texts(_studies, _pdf_dir)
            if _extracted:
                out["ref_sections"] = _extracted
                sess.data.setdefault("handoff", {})["ref_sections"] = _extracted
                sess.save()
    return out


def _apply_a3_upload(sess):
    """A3「上传数据 → 跳到 B」接缝（2026-09-17）。

    用户在 A3（PDF 下载）节点上传/粘贴自己整理好的 2×2 数据 → 前端随「批准」提交
    revision.extracted_rows → 此处把它直接接成 Block B 的 studies_for_b，
    从而**跳过 A4（数据提取）直达 Block B**。返回是否成功接入。
    """
    rev = sess.latest_revision("A3.pdf_download") or {}
    rows = rev.get("extracted_rows")
    if isinstance(rows, list) and rows:
        sess.data.setdefault("handoff", {})["studies_for_b"] = rows
        sess.save()
        return True
    return False


def _a1_report_search_override(sess):
    """A1 编辑版 PICOS 报告 → A2 检索主题覆盖（用户需求 2026-09-19）。

    仅当 A1 revision.report 与系统预填原文**不同**（用户真的改过/补充过）才解析，
    避免只点批准未改内容也覆盖原始主题。抽不到可检索值返回 None（回落原始 topic）。
    优先级：A2 手改检索式（query revision）> 此覆盖 > 原始 topic。
    """
    rev = sess.latest_revision("A1.topic_selection") or {}
    rep = rev.get("report")
    if not isinstance(rep, str) or not rep.strip():
        return None
    env = sess.data["blocks"]["A"].get("envelope") or {}
    orig = None
    for s in (env.get("stages") or []):
        if (s.get("stage") or {}).get("id") == block_a.A1:
            orig = (s.get("stage_result") or {}).get("report")
            break
    if orig is not None and rep.strip() == str(orig).strip():
        return None
    return block_a._picos_report_to_query(rep)


def _extraction_input(sess):
    """A4 extraction_table：优先人工 revision rows（list），否则原始配置值。

    A4 红线放行（approved）也携带 revision.extracted_rows（前端把逐篇抽取行 +
    剔除状态打包提交，见 workbench approveA4），故用 latest_revision（不限 action）
    而非 revisions_for_block（仅 revised）——否则「放行即重抽」会吞掉人工剔除。
    """
    rev = sess.latest_revision("A4.data_extraction") or {}
    rows = rev.get("extracted_rows")
    if isinstance(rows, list) and rows:
        return rows
    return sess.data["cfg"].get("extraction_table")


def _apply_revisions(env, revisions):
    """把人工 revision 补丁进信封对应 stage_result（A4 之外为事后补丁，见模块 docstring）。"""
    if not revisions:
        return env
    env = copy.deepcopy(env)
    for st in env.get("stages") or []:
        sid = (st.get("stage") or {}).get("id")
        rev = revisions.get(sid)
        if rev:
            base = st.get("stage_result") or {}
            st["stage_result"] = {**base, **{k: _maybe_json(v) for k, v in rev.items()
                                             if not str(k).startswith("_")}}
    return env


def _maybe_json(v):
    """revision 值若是合法 JSON 容器字符串 → 解析回 dict/list（2026-09-19）。

    背景：前端「完整质量报告（可编辑 · 兜底）」等 json 面板以 pretty JSON 文本
    提交 revision（textarea），而 stage_result.report 原为 dict——下游面板
    （闸门判定等）按对象取字段，字符串会全显「—」。这里把合法 JSON 容器串
    还原为对象；非容器（如 A1 PICOS 报告 markdown）原样保留。
    """
    if isinstance(v, str):
        s = v.strip()
        if len(s) >= 2 and s[0] in "{[" and s[-1] in "}]":
            try:
                parsed = json.loads(s)
                if isinstance(parsed, (dict, list)):
                    return parsed
            except Exception:
                pass
    return v


def _extraction_guard_check(sess):
    """进 B 前守卫双保险（spec §8.4）：extraction_table 为 CSV 路径时核验人工 stamp。"""
    table = _extraction_input(sess)
    if not (isinstance(table, str) and table.strip()):
        return None  # 非 CSV 路径（list / None）不适用守卫
    try:
        from extraction_guard import check_verified  # scripts/ 已在 sys.path（由调用方保证）
    except ImportError:
        try:
            import sys
            sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                            "..", "scripts"))
            from extraction_guard import check_verified
        except ImportError:
            return None  # 守卫不可用时不阻塞（与 run_meta --trust-data 语义一致由人工闸兜底）
    ok, reason, status = check_verified(os.path.abspath(table))
    if ok:
        return None
    return {"gate": "extraction_review", "stage_id": "A4.data_extraction",
            "status": status, "reason": reason, "csv": os.path.abspath(table)}


# ---------------------------------------------------------------------------
# 控制器返回视图（FullflowView，spec §5）
# ---------------------------------------------------------------------------
def _stage_sid(stage):
    return (stage.get("stage") or {}).get("id")


def _view(sess, env):
    ff = {
        "session_path": sess.path,
        "cursor": None,  # 返回前统一刷新（cursor 在各分支会被推进）
        "await": {"kind": "done"},
        "handoff_preview": None,
    }
    if env is None:
        return {"fullflow": ff}
    ff["pipeline_id"] = env.get("pipeline_id")

    if env.get("await_human"):
        stage = env.get("final") or {}
        sid = _stage_sid(stage)
        gate = env.get("gate")
        nha = stage.get("next_human_action") or {}
        if gate:
            kind = "gate"
            options = ["approved", "revised", "rejected"]          # 🔴 红线闸拒 skip
        else:
            kind = "pause"
            options = ["approved", "revised", "skipped", "rejected"]  # 软停可 skip
        editable = {k: (stage.get("stage_result") or {}).get(k)
                    for k in EDITABLE_KEYS.get(sid, []) if k in (stage.get("stage_result") or {})}
        ff["await"] = {"kind": kind, "gate": gate, "stage_id": sid,
                       "prompt": nha.get("prompt"), "options": options,
                       "editable_payload": editable,
                       "stage_result": stage.get("stage_result"),
                       "nha": nha}  # 富载荷（覆盖/逐条决策等）供工作台与 agent 渲染
        sess.cursor.update({"stage_id": sid, "await_kind": kind})
        ff["cursor"] = dict(sess.cursor)
        return {"fullflow": ff}

    # 块完成 → handoff 确认 / 终态
    letter = sess.cursor["block"]
    if letter == "C":
        ff["await"] = {"kind": "done", "stage_id": _stage_sid(env.get("final") or {})}
        sess.cursor.update({"block": "done", "stage_id": None, "await_kind": "done"})
        ff["cursor"] = dict(sess.cursor)
        return {"fullflow": ff}

    nxt = "B" if letter == "A" else "C"
    if letter == "A":
        # 收集 Block A 产出的可算数据：A4（数据提取，启用时）优先；A3（PDF 下载）阶段
        # 本身不抽取，其 extracted_rows 恒空，故实际数据主要来自下面的人工上传接缝。
        rows = None
        for st in env.get("stages") or []:
            if _stage_sid(st) in ("A3.pdf_download", "A4.data_extraction"):
                r = (st.get("stage_result") or {}).get("extracted_rows")
                if r:
                    rows = r
        # A3「上传数据 → 跳到 B」：人工自备数据优先级最高（revision 接缝）
        rev_rows = (sess.latest_revision("A3.pdf_download") or {}).get("extracted_rows")
        if isinstance(rev_rows, list) and rev_rows:
            rows = rev_rows
        sess.data["handoff"]["studies_for_b"] = rows or []
        n_studies = len(rows or [])
        fields = sorted({k for r in (rows or []) if isinstance(r, dict) for k in r})
    else:
        n_studies = len(sess.data["handoff"].get("studies_for_b") or [])
        fields = None
    ff["await"] = {"kind": "handoff_confirm", "gate": None, "stage_id": None,
                   "prompt": f"Block {letter} 完成，即将进入 Block {nxt}。请确认交接数据。",
                   "options": ["approved", "rejected"]}
    ff["handoff_preview"] = {"next": f"Block {nxt}", "n_studies": n_studies, "fields": fields}
    sess.cursor.update({"block": nxt, "stage_id": None, "await_kind": "handoff_confirm"})
    ff["cursor"] = dict(sess.cursor)
    return {"fullflow": ff}


# ---------------------------------------------------------------------------
# 公开入口（spec §4）
# ---------------------------------------------------------------------------
def run_fullflow(topic: str, *, max_results: int = 50, year_from=None,
                 effect_measure: str = "OR", nma: bool = False,
                 pause_at=None, extraction_table=None,
                 session_dir: str = ".", debug: bool = False,
                 pdf_email: str = None, max_attempts: int = 12,
                 include_reviews: bool = False,
                 on_line=None, on_a4_event=None) -> dict:
    """启动 fullflow：跑 Block A，遇停靠点即停。返回 = 块信封 + fullflow 视图。

    pdf_email / max_attempts 透传给 Block A 的 A4 自动落盘（文献集门控 → OA PDF
    下载 → 抽取 2×2 表草稿）。live 路径默认开启 auto_fetch，使「检索→A4→B1」
    真正贯通：A4 产出的 extracted_rows 经 handoff.studies_for_b 直接喂给 B1。
    """
    # 入口标识：标记本次调用来自工作台 web 应用（2026-10-07）
    cc.set_entry_point("workbench")
    if pause_at is None:
        pause_at = DEFAULT_PAUSE_AT
    cfg = {"max_results": max_results, "year_from": year_from,
           "effect_measure": effect_measure, "nma": nma,
           "pause_at": sorted(pause_at), "extraction_table": extraction_table,
           "session_dir": session_dir, "pdf_email": pdf_email,
           "max_attempts": max_attempts, "include_reviews": include_reviews}
    sess = FullflowSession.new(topic, cfg, session_dir)
    return _advance(sess, debug=debug, on_line=on_line, on_a4_event=on_a4_event)


def run_fastpath(topic: str, data_mode: str, *, rows=None, a4_result=None,
                 b_env=None, effect_measure: str = "OR", nma: bool = False,
                 session_dir: str = ".", debug: bool = False, demo: bool = False,
                 topic_en: str = None, defer_advance: bool = False) -> dict:
    """快速通道：跳过 Block A 的选题/检索/筛选，按 data_mode 直接进入分析起点。

    data_mode:
      - "raw_csv": rows（已解析的 extracted_rows 列表）就绪 → 跳过 A，直接进 Block B 合并计算
        （对应「我已备好原始数据，跳到 B 部分准备输入数据进行分析」）。
      - "pdf": a4_result（已抽取的逐篇 per_doc 结果）就绪 → 落停在 A4 红线闸
        （对应「我已备好全文 PDF，跳到从 PDF 数据中提取数据那一步」）。
      - "draft": b_env（Block B 信封/结果）就绪 → 跳过 A+B，停在 C1 软停闸
        （对应「我已备好分析结果，直接跳到写稿 / 改稿阶段」；b_env 为必填）。

    返回：成功返回 FullflowSession（已落盘）；失败返回 {"error": ...}。
    约定：raw_csv 返回前已 _advance 跑完 Block B（停在 B4 红线）；pdf 返回前停在 A4 红线
    （cursor.block 均置为 "B"，使放行后直接进入 Block B，不再重跑空 Block A）；draft 返回前
    停在 C1 软停闸（cursor.block 置为 "C"）。

    defer_advance（2026-09-27 网关 504 修复 · 方案 A）：raw_csv / draft 不在本请求内
    同步跑 _advance（C1 初稿含 LLM 扩写，实测 50~70s，贴着 Cloudflare 60s 网关超时线，
    时好时坏 504）。改为：建会话、落 cursor 后打 `data["_starting"]={"status":"advancing",
    "started_at":...}` 即返回，由调用方（server 端点）交给后台线程执行
    advance_started_session()；前端轮询 /api/session 直到 _starting ∈ {done, error}。
    pdf 模式不经 _advance（停在 A4 人工闸），不受影响。
    """
    # 功能开关（2026-09-17）：两条快速通道已从网页隐藏；接口层同样拒绝，
    # 避免绕过 UI 生成「走了半截又无法继续」的会话。
    if data_mode == "pdf" and not features.enabled("fastpath_pdf"):
        return {"error": "「自备全文 PDF」通道当前未开放（features.fastpath_pdf=False）。"}
    if data_mode == "raw_csv" and not features.enabled("fastpath_raw_csv"):
        return {"error": "「自备原始数据」通道当前未开放（features.fastpath_raw_csv=False）。"}

    cfg = {"max_results": 0, "year_from": None,
           "effect_measure": effect_measure, "nma": nma,
           "pause_at": sorted(DEFAULT_PAUSE_AT), "extraction_table": None,
           "session_dir": session_dir, "pdf_email": None, "max_attempts": 0,
           "include_reviews": False, "fast_path": data_mode}
    sess = FullflowSession.new(topic, cfg, session_dir)
    pid = sess.data["pipeline_id"]
    # 英文题名（2026-09-22）：C 档初稿是英文稿件。显式传入优先；演示模式配套
    # 内置英文题名（与 demo_b_env 现算的效应量同主题），避免正文出现中英混杂。
    if topic_en and str(topic_en).strip():
        sess.data["topic_en"] = str(topic_en).strip()
    elif demo:
        sess.data["topic_en"] = block_b.DEMO_TOPIC_EN
    if demo:
        # 演示会话标记（2026-09-22 用户要求）：调用方没给真实 B 信封、用了内置示例
        # 信封时必须**明说**。否则用户会把接下来的初稿（标题/效应量/GRADE/参考
        # 文献全是 omega-3 示例主题的）当成「我自己那份分析的结果」——而它跟用户
        # 输入的主题毫无关系。
        # 落库而非只放内存：重载会话后标记仍在，build_state 据此下发提示条。
        sess.data["demo"] = True

    if data_mode == "raw_csv":
        if not rows:
            return {"error": "raw_csv 模式缺少解析后的行数据（rows 为空）"}
        # a4_result 补齐缺失字段（n_extracted / n_screened / per_doc）
        a4_result_for_env = {"extracted_rows": rows, "n_extracted": len(rows),
                             "n_screened": len(rows), "per_doc": [{}] * len(rows),
                             "coze_ready": False,
                             "note": ("内置示例数据（演示），跳至 Block B 分析" if demo
                                      else "用户自备原始数据（已上传 CSV），跳至 Block B 分析")}
        a_env = {
            "pipeline_id": pid, "pipeline": "A",
            "stages": [{
                "stage": {"id": "A4.data_extraction"}, "status": "completed",
                "stage_result": a4_result_for_env,
            }],
            "done": True, "await_human": False,
        }
        sess.data["blocks"]["A"] = {"envelope": a_env, "status": "done"}
        sess.data["handoff"]["studies_for_b"] = rows
        sess.data["cursor"] = {"block": "B", "stage_id": None, "await_kind": None}
        if defer_advance:
            sess.data["_starting"] = {"status": "advancing",
                                      "started_at": datetime.datetime.now().isoformat(timespec="seconds")}
            sess.save()
            return sess
        sess.save()
        res = _advance(sess, debug=debug)
        if isinstance(res, dict) and "error" in res:
            return res
        return sess

    if data_mode == "pdf":
        if not a4_result:
            return {"error": "pdf 模式缺少 a4_result"}
        # 补齐可能缺失的字段，避免前端渲染回退到通用空面板
        a4_result.setdefault("n_extracted", len(a4_result.get("per_doc") or []))
        a4_result.setdefault("n_screened", a4_result["n_extracted"])
        a4_result.setdefault("per_doc", [])
        a4_stage = {"stage": {"id": "A4.data_extraction"}, "status": "await_human",
                    "stage_result": a4_result}
        a_env = {
            "pipeline_id": pid, "pipeline": "A",
            "stages": [
                {"stage": {"id": "A1.topic_selection"}, "status": "completed",
                 "stage_result": {"picos": {}, "report": topic, "missing_dimensions": [],
                                  "registry_probe": {"status": "skipped",
                                                     "note": "自备 PDF 模式跳过选题/检索"},
                                  "include_reviews": False}},
                {"stage": {"id": "A2.literature_search"}, "status": "completed",
                 "stage_result": {"studies": [], "n": 0, "screened": [], "n_screened": 0,
                                  "coverage": {"total": 0, "search_status": "skipped",
                                               "by_source": {}}}},
                a4_stage,
            ],
            "done": True, "await_human": True, "final": a4_stage,
        }
        sess.data["blocks"]["A"] = {"envelope": a_env, "status": "done"}
        sess.data["cursor"] = {"block": "B", "stage_id": "A4.data_extraction",
                               "await_kind": "gate"}
        # 同步 last_view → build_state 能产出正确的 A4 渲染 schema
        lv = sess.data.setdefault("last_view", {})
        ff = lv.setdefault("fullflow", {})
        nha = a4_stage.get("next_human_action") or {
            "prompt": "已据上传的全文 PDF 抽取 2×2 表，请逐篇核验放行"
                      "（或剔除误抽/综述篇目）后进入 Block B。",
            "options": ["approved", "revised", "rejected"],
        }
        ff["await"] = {
            "kind": "gate", "gate": True,
            "stage_id": "A4.data_extraction",
            "prompt": nha.get("prompt"),
            "options": nha.get("options") or ["approved", "revised", "rejected"],
            "editable_payload": {},
            "stage_result": a4_result,
            "a4_result": a4_result,
            "nha": nha,
        }
        sess.save()
        from block_a import a4_persist_result
        a4_persist_result(sess.path, a4_result)
        return sess

    if data_mode == "draft":
        if not b_env:
            return {"error": "draft 模式缺少 b_env（Block B 信封，必填）"}
        sess.data["blocks"]["A"] = {"envelope": {
            "pipeline_id": pid, "pipeline": "A",
            "stages": [
                {"stage": {"id": "A1.topic_selection"}, "status": "completed",
                 "stage_result": {"picos": {}, "report": topic, "missing_dimensions": [],
                                  "registry_probe": {"status": "skipped",
                                                     "note": "draft 模式跳过 A/B，直达写稿"},
                                  "include_reviews": False}},
                {"stage": {"id": "A2.literature_search"}, "status": "completed",
                 "stage_result": {"studies": [], "n": 0, "screened": [], "n_screened": 0,
                                  "coverage": {"total": 0, "search_status": "skipped",
                                               "by_source": {}}}},
                {"stage": {"id": "A4.data_extraction"}, "status": "completed",
                 "stage_result": {"extracted_rows": [], "n_extracted": 0,
                                  "n_screened": 0, "coze_ready": False,
                                  "note": ("内置示例 B 信封（演示），跳至 Block C 撰稿" if demo
                                           else "draft 模式跳过 A/B，直达写稿")}},
            ],
            "done": True, "await_human": False}, "status": "done"}
        sess.data["blocks"]["B"] = {"envelope": b_env, "status": "done"}
        sess.data["cursor"] = {"block": "C", "stage_id": None, "await_kind": None}
        if defer_advance:
            sess.data["_starting"] = {"status": "advancing",
                                      "started_at": datetime.datetime.now().isoformat(timespec="seconds")}
            sess.save()
            return sess
        sess.save()
        res = _advance(sess, debug=debug)
        if isinstance(res, dict) and "error" in res:
            return res
        return sess

    return {"error": f"未知 data_mode: {data_mode!r}"}


def advance_started_session(session_path: str, *, debug: bool = False) -> dict:
    """defer_advance 会话的后台推进包装（2026-09-27 · 网关 504 修复方案 A）。

    由 server 端点在 run_fastpath(defer_advance=True) 之后交给后台线程调用：
    跑 _advance（raw_csv → Block B 合并计算；draft → Block C 初稿含 LLM 扩写），
    结束后把状态写进会话顶层键 `_starting`（done / error），供前端轮询 /api/session 判定：
      - advancing → 继续等；done → 正常渲染当前 await 闸；error → 展示 _starting.message。
    _advance 自身已「遇停即存即返」（内部多次 sess.save()），本函数只负责终态标记与
    异常兜底（LLM / coze / 网络异常不得逃逸到线程外）。
    返回 {"ok": bool, "error": str|None, "cursor": ...} 供日志。
    """
    try:
        sess = FullflowSession.load(session_path)
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "error": f"会话加载失败: {type(e).__name__}: {e}"}
    t0 = time.time()
    try:
        res = _advance(sess, debug=debug)
    except Exception as e:  # noqa: BLE001 — _advance 有内层捕获，这里是最后防线
        res = {"error": f"{type(e).__name__}: {e}"}
    try:
        sess = FullflowSession.load(session_path)   # 重读（_advance 内部已 save，取最新落盘态）
        elapsed = round(time.time() - t0, 1)
        if isinstance(res, dict) and "error" in res:
            sess.data["_starting"] = {"status": "error", "message": str(res["error"]),
                                      "elapsed_sec": elapsed}
        else:
            sess.data["_starting"] = {"status": "done", "elapsed_sec": elapsed}
        sess.save()
        return {"ok": "error" not in (res or {}), "error": (res or {}).get("error")
                if isinstance(res, dict) else None, "cursor": dict(sess.cursor)}
    except Exception as e:  # noqa: BLE001 — 标记写失败只记日志，不影响会话本体
        return {"ok": False, "error": f"_starting 标记失败: {type(e).__name__}: {e}"}


#: 批准后自动产出「供人工审阅」的 Excel 的节点（用户裁定 2026-09-10）：
#: A2（文献集：检索 + 初筛合并节点）批准 → 直接出一张合并表
#: （检索结果 + 裁决/理由/文献类型确认列）。
AUTO_EXPORT_ON_APPROVE = ("A2.literature_search",)


def auto_export_filename(stage_id: str, pipeline_id: str) -> str:
    """自动产物的文件名（稳定、可预测，便于人工在工作目录里找到）。"""
    label = {"A2.literature_search": "A2_文献集"}.get(stage_id, stage_id)
    return f"{label}_{pipeline_id}.xlsx"


def _auto_export_on_approve(sess, decision):
    """节点批准后**直接**生成 Excel 交付物，供人工审阅。

    当前仅合并节点 A2「文献集」：一张表 = 检索结果 + 裁决/理由/文献类型确认列
    （用户裁定 2026-09-10）。设计约束：**绝不因产物导出失败而中断流程** ——
    任何异常一律吞掉返回 None（决策已落盘，流程照常推进）。
    成功返回绝对路径，由 resume_fullflow 挂到结果 dict 的 `artifacts`。
    """
    try:
        if decision.get("action") != "approved":
            return None
        sid = decision.get("stage_id")
        if sid not in AUTO_EXPORT_ON_APPROVE:
            return None
        sdir = (sess.data.get("cfg") or {}).get("session_dir") or os.path.dirname(sess.path)
        pid = (sess.data.get("pipeline_id")
               or os.path.basename(sess.path)
               .replace("fullflow_session_", "").replace(".json", ""))
        out = os.path.join(sdir, auto_export_filename(sid, pid))
        if sid == "A2.literature_search":
            block_a.export_screening_xlsx(sess.path, out, lang="zh")
        else:  # pragma: no cover — 预留扩展位
            return None
        return os.path.abspath(out)
    except Exception:  # noqa: BLE001 — 产物导出失败不得影响主流程
        return None


def resume_fullflow(session_path: str, decision: dict, *, debug: bool = False,
                    on_line=None, on_a4_event=None) -> dict:
    """带人工决策续跑。自动判断该进下一阶段 / 下一块 / 结束。返回同 run_fullflow。"""
    # 入口标识：标记本次调用来自工作台 web 应用（2026-10-07）
    cc.set_entry_point("workbench")
    sess = FullflowSession.load(session_path)
    err = _validate_decision(sess, decision)
    if err:
        return {"error": err, **_view(sess, sess.data["blocks"][sess._awaiting_block()]
                                      .get("envelope"))}
    action = decision.get("action")
    # Phase 2：revise 已离开的块 → 回退该块并重算下游（真重跑，而非仅补丁信封）
    if action == "revised":
        sid = decision.get("stage_id")
        # A1 修订（选题 / 检索范围 / PICOS）属「检索前最后可改点」：只回写信封并
        # 停回 A1，绝不重跑整块检索（否则改个检索范围就触发全库检索，并越过 A1
        # 批准闸直接跳到 A2）。用户复核新检索范围后于 A1 批准，才触发真正的检索。
        # 仅当信封已存在（正常停靠在 A1 时必然存在）时生效；异常缺失则回退通用重跑。
        if sid == "A1.topic_selection":
            env = sess.data["blocks"]["A"].get("envelope")
            if env is not None:
                sess.record_decision(decision)
                rev = decision.get("revision") or {}
                for st in env.get("stages") or []:
                    if _stage_sid(st) == "A1.topic_selection":
                        base = st.setdefault("stage_result", {})
                        base.update({k: v for k, v in rev.items()
                                     if not str(k).startswith("_") and v is not None})
                sess.data["blocks"]["A"]["envelope"] = env
                sess.cursor.update({"block": "A", "stage_id": "A1.topic_selection",
                                    "await_kind": "pause"})
                view = _view(sess, env)
                sess.data["last_view"] = view
                sess.save()
                return {"fullflow": view["fullflow"],
                        **{k: v for k, v in env.items() if k not in ("fullflow",)}}
        tgt = _block_of(sid)
        cur = sess.cursor.get("block")
        if tgt is not None and cur in _BLOCK_SEQ and _BLOCK_SEQ.index(tgt) < _BLOCK_SEQ.index(cur):
            # 与 rewind_fullflow 同款失败回滚（2026-09-17）：修订已离开的块时重跑下游若崩，
            # 整体还原到修订前，避免「块被清 + 旧 last_view」半成品态（LRN-20260917-rewind-rollback）。
            sess.record_decision(decision)
            snapshot = copy.deepcopy(sess.data)
            sess.rewind(tgt)
            out = _advance_until_pause(sess, debug=debug, on_line=on_line, on_a4_event=on_a4_event)
            if "error" in out:
                sess.data = snapshot
                sess.save()
            return out
    sess.record_decision(decision)
    sess.save()
    if action == "rejected":
        # 打回重做：停在原地，重放上一视图（决策已留痕审计）
        view = sess.data.get("last_view") or _view(
            sess, sess.data["blocks"][sess._awaiting_block()].get("envelope"))
        view = copy.deepcopy(view)
        view["fullflow"]["note"] = decision.get("note") or "人工打回，请修订后重新决策。"
        return view
    res = _advance(sess, debug=debug, on_a4_event=on_a4_event)
    art = _auto_export_on_approve(sess, decision)
    if art:
        res = dict(res or {})
        res["artifacts"] = list(res.get("artifacts") or []) + [art]
    return res


def _awaiting_block(self):
    """当前等待人工的块（cursor.block 的前一个块；done 时为 C）。"""
    b = self.cursor["block"]
    if b in _BLOCK_SEQ:
        return b
    return "C"


FullflowSession._awaiting_block = _awaiting_block


def _validate_decision(sess, decision):
    """红线校验（spec §8）：绝不自动 approve；红线闸拒 skip；stage/gate 必须对得上。"""
    if not isinstance(decision, dict):
        return "decision 必须是 dict（spec §6.1）"
    action = decision.get("action")
    if action not in ACTIONS:
        return f"action 须为 {sorted(ACTIONS)} 之一，收到 {action!r}"
    kind = sess.cursor.get("await_kind")
    if kind == "done":
        return "会话已完成，无待决策项"
    if kind == "handoff_confirm":
        if action not in ("approved", "rejected"):
            return "块间交接确认仅接受 approved / rejected"
        return None
    expect_sid = sess.cursor.get("stage_id")
    sid = decision.get("stage_id")
    if sid != expect_sid:
        # Phase 2：revise 已离开的块（如 cursor 在 B、revise A3）允许，将触发 rewind 重算
        if action == "revised":
            tgt = _block_of(sid)
            cur = sess.cursor.get("block")
            if tgt is not None and cur in _BLOCK_SEQ and _BLOCK_SEQ.index(tgt) < _BLOCK_SEQ.index(cur):
                return None
        return f"stage_id 不匹配：当前停靠在 {expect_sid!r}，收到 {sid!r}"
    if action == "revised" and not isinstance(decision.get("revision"), dict):
        return "action=revised 须提供 revision dict（可编辑键见 editable_payload）"
    if action == "skipped":
        gate = STAGE_TO_GATE.get(sid)
        if gate and gate in cc._REDLINE_GATES:
            return f"🔴 红线闸 {gate} 不接受 skipped（spec §8.2），请 approve/revise/reject"
    return None


def _advance(sess, debug=False, on_line=None, on_a4_event=None):
    """推进：跑 cursor 所指块（含 revision 补丁），遇停即存即返。"""
    letter = sess.cursor["block"]
    if letter == "done":
        return {"fullflow": {"session_path": sess.path, "cursor": dict(sess.cursor),
                             "await": {"kind": "done"}}}

    # A3「上传数据 → 跳到 B」（2026-09-17）：把人工自备的 extracted_rows 接成 studies_for_b。
    # **无条件先试**（无 A3 revision 时为 no-op）—— 上传后 cursor 可能仍在 A 块（A3 停靠点），
    # 若只在 letter=="B" 时调用，就会出现「上传了数据却仍被判为无数据」。必须在下面的
    # 「无数据则终止」判断之前执行。
    _apply_a3_upload(sess)

    # 2026-09-19：A3 之后**强制进入 Block B**（无论是否提取/上传数据）。
    # 无数据时由 run_block_b 在 B1 以 await_data 停靠（前端在 B1 内提供上传入口），
    # 不再在此直接判定为终点；B/C 节点定义与代码原样保留。

    # 进 B 前守卫双保险（spec §8.4）
    if letter == "B":
        guard = _extraction_guard_check(sess)
        if guard:
            sess.cursor["await_kind"] = "guard_blocked"
            sess.save()
            return {"fullflow": {"session_path": sess.path, "cursor": dict(sess.cursor),
                                 "await": {"kind": "guard_blocked", **guard,
                                           "prompt": (f"提取数据 CSV 未通过人工核验闸：{guard['reason']} "
                                                      "请先 extract_assist.py stamp --confirm 后再 approve。"),
                                           "options": ["approved"]},
                                 "handoff_preview": None}}

    try:
        env = _run_block(letter, sess, debug, on_line=on_line, on_a4_event=on_a4_event)
    except Exception as e:  # noqa: BLE001 — coze 失败/网络异常返回结构化错误，不推进
        sess.cursor["await_kind"] = sess.cursor.get("await_kind") or "error"
        sess.save()
        return {"error": f"{type(e).__name__}: {e}",
                "fullflow": {"session_path": sess.path, "cursor": dict(sess.cursor),
                             "await": {"kind": "error"}, "handoff_preview": None}}

    env = _apply_revisions(env, sess.revisions_for_block(letter))

    block = sess.data["blocks"][letter]
    block["envelope"] = env
    block["status"] = "done" if env.get("done") else "await_human"

    # 2026-09-19：A 块完成后**强制进入 Block B**（无论是否提取/上传数据）。
    #   · 有可算数据（A3 上传 / A4 提取）→ 直接进入 B1 合并计算；
    #   · 无数据 → 进入 B1，由 run_block_b 以「待补数据」停靠（await_data），
    #     前端在 B1 内提供上传/录入入口，上传后就地重算。
    if letter == "A" and env.get("done"):
        sess.cursor.update({"block": "B", "stage_id": None, "await_kind": None})
        sess.save()
        return _advance(sess, debug=debug, on_line=on_line, on_a4_event=on_a4_event)

    # 2026-09-17 用户要求：B 块完成后**不再插入「交接确认」**（handoff_confirm，stage_id=None
    # → 前端显示「通用确认节点」），直接推进 Block C（撰写）。
    if letter == "B" and env.get("done"):
        sess.cursor.update({"block": "C", "stage_id": None, "await_kind": None})
        sess.save()
        return _advance(sess, debug=debug, on_line=on_line, on_a4_event=on_a4_event)

    view = _view(sess, env)
    # handoff / done 时 cursor 已推进；gate/pause 时停在块内
    sess.data["last_view"] = view
    sess.save()
    return {"fullflow": view["fullflow"], **{k: v for k, v in env.items()
                                             if k not in ("fullflow",)}}


# ---------------------------------------------------------------------------
# Phase 2：_rewind(target) 回退重跑 + revise 真重跑下游
# ---------------------------------------------------------------------------
def _block_of(stage_id):
    """stage_id 形如 'A2.literature_search' 或块字母 'A'/'B'/'C' → 块字母；无法解析返回 None。"""
    if stage_id in _BLOCK_SEQ:
        return stage_id
    if isinstance(stage_id, str) and stage_id[:1] in _BLOCK_SEQ:
        return stage_id[:1]
    return None


def _downstream_blocks(letter):
    """letter 及其下游块（含自身）。A→[A,B,C]; B→[B,C]; C→[C]。"""
    return _BLOCK_SEQ[_BLOCK_SEQ.index(letter):]


_STAGE_RE = re.compile(r"^([A-Za-z])(\d+)")


def _stage_order_key(stage_id):
    """stage_id → (块序, 阶段序号) 可比较键；无法解析返回 None。

    'A2.literature_search' → (0, 2)；'B1.meta_analysis' → (1, 1)；
    块字母 'A'/'B'/'C' → (块序, 0)（表示「整块起点」，故能覆盖该块所有阶段）。
    """
    if not isinstance(stage_id, str):
        return None
    s = stage_id.strip()
    if s.upper() in _BLOCK_SEQ:
        return (_BLOCK_SEQ.index(s.upper()), 0)
    m = _STAGE_RE.match(s)
    if not m:
        return None
    b = m.group(1).upper()
    if b not in _BLOCK_SEQ:
        return None
    return (_BLOCK_SEQ.index(b), int(m.group(2)))


def _advance_until_pause(sess, debug=False, on_line=None, on_a4_event=None):
    """rewind 后自动续跑：遇 handoff_confirm 自动批准续跑，遇 pause/gate/done/error 即停。
    使回退后下游真正重算到原闸位/完成态。"""
    for _ in range(len(_BLOCK_SEQ) + 2):
        kind = sess.cursor.get("await_kind")
        if kind == "handoff_confirm":
            sess.record_decision({
                "stage_id": None, "gate": None, "action": "approved",
                "note": "rewind 自动续跑：handoff 自动批准", "decided_by": "system_rewind",
            })
            view = _advance(sess, debug=debug, on_line=on_line, on_a4_event=on_a4_event)
        elif kind in (None,):
            view = _advance(sess, debug=debug, on_line=on_line, on_a4_event=on_a4_event)
        else:
            return {"fullflow": {"session_path": sess.path, "cursor": dict(sess.cursor),
                                 "await": {"kind": kind}}}
        if "error" in view:
            return view
        k = view.get("fullflow", {}).get("await", {}).get("kind")
        if k in ("pause", "gate", "done", "error"):
            return view
        # k == handoff_confirm → 下一轮循环继续
    return view


def rewind_fullflow(session_path: str, target_stage_id: str, *, debug: bool = False,
                    on_line=None, on_a4_event=None, force_refresh: bool = False) -> dict:
    """Phase 2 公开入口：回退到 target 所属块并重算下游，直到回到原闸位/完成。

    target 可为块字母（'A'/'B'/'C'）或 stage_id（'A2.literature_search' 等）；
    回退粒度为块级（块内整体重跑）。清空下游块信封 + handoff，重置 cursor 到该块起点，
    保留 human_decisions 审计。

    检索复用与强制刷新（2026-09-20）：回退进 A 块时**保留其信封**作为复用源，由
    `run_block_a` 按检索指纹决定「复用上次检索结果」还是「真实联网重跑」——
    免掉 A1 的 ct-registry 查重探针（timeout 180s）与 A2 的全库检索（约 2 分钟）。
    `force_refresh=True`（工作台「强制重新联网检索」勾选）则连该信封一并清空，
    使本次回退及后续阶段一律走真实检索。

    失败回滚（2026-09-17）：回退重跑（跑下游块）若抛异常 → `_advance` 捕为 error 返回，
    但 `rewind()` 已把块信封清空并落盘、而 `last_view` 仍是回退前旧视图 → 会话磁盘态处于
    「块被清 + 旧视图」的半成品，重载后 build_state 读到旧 last_view 显得「回退没生效 / 报错」。
    故在回退前拍快照，重跑失败时整体还原，使 failed rewind 成为会话无副作用的 no-op。

    凭据作废（2026-09-18 修复）：清信封不够 —— human_decisions 里的历史 approved 会被
    `decisions_for_block()` 当凭据重放，导致回退点那道闸直接放行。故回退时同步作废
    「target 及其之后」的凭据（见 `invalidate_decisions`），回退点才会真正停下来问人。
    """
    sess = FullflowSession.load(session_path)
    snapshot = copy.deepcopy(sess.data)   # 回退前完整快照（含 blocks / cursor / last_view / human_decisions）
    letter = _block_of(target_stage_id)
    if letter is None:
        return {"error": f"无法解析回退目标块：{target_stage_id!r}"}
    sess.rewind(letter)
    if force_refresh:
        # 强制刷新：丢掉 A 的复用源（rewind 默认保留），本次及后续阶段一律真实联网检索。
        sess.data["blocks"]["A"]["envelope"] = None
        if on_line:
            on_line("[A] 已勾选「强制重新联网检索」→ 丢弃上次检索结果，本次真实重跑")
    # 作废回退目标及其下游的人工凭据：否则重跑时该闸被历史 approved 直接放行，
    # 「打回到 A1」会静默跳过 A1 → 重跑整块检索 → 又停在 A2（用户看到「打回无效」）。
    sess.invalidate_decisions(target_stage_id)
    sess.save()
    out = _advance_until_pause(sess, debug=debug, on_line=on_line, on_a4_event=on_a4_event)
    if "error" in out:
        # 重跑失败：还原到回退前，避免半成品态；API 层仍按 400 透传 out["error"] 详情。
        sess.data = snapshot
        sess.save()
    return out
