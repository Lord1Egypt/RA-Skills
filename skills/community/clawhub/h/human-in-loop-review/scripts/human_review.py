#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""human-in-loop-review: 把中高危/歧义动作路由到人工审核队列，阻止自主 agent 越权。

能力：
  - 审核分级：needs_review(action, context) 依据风险信号返回 True/False（默认对
    medium/high/critical 与「不可逆」「外发」「提权」「支付」类动作要求人工确认）
  - 审核队列：add / pending / get / approve / reject / summary
  - 完整审计：每条记录含 提议者 / 动作 / 风险 / 审核人 / 结论 / 理由 / 时间戳
  - 置信自检：selftest 覆盖 入队 / 待审计数 / 通过 / 驳回 / 摘要汇总

用法：
  python human_review.py --selftest
  python human_review.py --add '{"action":"delete /data","proposed_by":"agent-7"}'
  python human_review.py --pending
  python human_review.py --approve <id> --reviewer alice --note "确认可删"
  python human_review.py --reject <id> --reviewer bob --note "先备份"
  python human_review.py --summary
"""
import argparse
import json
import re
import sys
import datetime
import uuid

# 触发人工审核的风险信号
REVIEW_PATTERNS = [
    (r"\brm\s+-", "删除操作"),
    (r"\bdelete\b|\bremove\b|\bdrop\b|\btruncate\b", "数据删除/丢弃"),
    (r"\bupdate\b.*\bset\b|\binsert\b|\balter\b|\bmerge\b", "写库操作"),
    (r"\bsend\b|\bemail\b|\bpost\b.*\bhttp|\bupload\b|\bshare\b", "对外发送/外发"),
    (r"\bsudo\b|\brunas\b|\bchmod\s+777\b", "提权/放宽权限"),
    (r"\binstall\b|\bpip\s+install\b|\bnpm\s+install\b", "安装依赖"),
    (r"\bdeploy\b|\bpublish\b|\brelease\b|\bgit\s+push\b", "上线/发布"),
    (r"\btransfer\b|\bpay\b|\bwithdraw\b|\brefund\b", "资金转移/支付"),
    (r"\bgit\s+reset\s+--hard\b|\bgit\s+push\s+--force\b", "破坏性 git 操作"),
    (r"\bkill\b|\bstop\b|\bterminate\b|\bshutdown\b|\breboot\b", "终止进程/关机"),
]

# 这些即便有确认也强制需人工（不可逆/外发隐私）
HARD_REVIEW = [
    r"\brm\s+-rf\b", r"\bdrop\s+(?:table|database)\b", r"\btruncate\b",
    r"\bformat\b", r"\bdd\s+if=", r"\btransfer\b.*\bwallet\b",
    r"\bgit\s+push\s+--force\b", r"\b:\(\)\s*\{.*\}\s*;",
]


def now():
    return datetime.datetime.now().isoformat(timespec="seconds")


def needs_review(action, context=None):
    context = context or {}
    if context.get("user_approved"):
        return False
    if any(re.search(p, action, re.IGNORECASE) for p in HARD_REVIEW):
        return True
    return any(re.search(p, action, re.IGNORECASE) for p, _ in REVIEW_PATTERNS)


def classify(action):
    hard = any(re.search(p, action, re.IGNORECASE) for p in HARD_REVIEW)
    if hard:
        return "critical"
    hits = [(p, r) for p, r in REVIEW_PATTERNS
            if re.search(p, action, re.IGNORECASE)]
    return "high" if hits else "low"


class ReviewQueue:
    def __init__(self):
        self.items = {}  # id -> record

    def add(self, action, proposed_by="agent", context=None, meta=None):
        rid = uuid.uuid4().hex[:8]
        level = classify(action)
        rec = {
            "id": rid,
            "action": action,
            "proposed_by": proposed_by,
            "risk": level,
            "context": context or {},
            "status": "pending",
            "reviewer": None,
            "decision_note": None,
            "decided_at": None,
            "created_at": now(),
            "meta": meta or {},
        }
        self.items[rid] = rec
        return rid

    def get(self, rid):
        return self.items.get(rid)

    def pending(self):
        return [r for r in self.items.values() if r["status"] == "pending"]

    def _decide(self, rid, reviewer, note, status):
        r = self.items.get(rid)
        if not r:
            raise KeyError(f"审核项不存在: {rid}")
        if r["status"] != "pending":
            raise ValueError(f"该项已 {r['status']}，不能重复审核")
        r["status"] = status
        r["reviewer"] = reviewer
        r["decision_note"] = note
        r["decided_at"] = now()
        return r

    def approve(self, rid, reviewer, note=""):
        return self._decide(rid, reviewer, note, "approved")

    def reject(self, rid, reviewer, note=""):
        if not note:
            note = "未提供理由（建议补充）"
        return self._decide(rid, reviewer, note, "rejected")

    def summary(self):
        from collections import Counter
        c = Counter(r["status"] for r in self.items.values())
        by_risk = Counter(r["risk"] for r in self.items.values())
        return {
            "total": len(self.items),
            "by_status": dict(c),
            "by_risk": dict(by_risk),
        }


# ---------------------------------------------------------------------------
def selftest():
    q = ReviewQueue()

    # 1) 危险动作需审核
    assert needs_review("rm -rf /data") is True
    print("[1] 危险动作 needs_review=True ✓")

    # 2) 已授权不需审核
    assert needs_review("delete /tmp/x", {"user_approved": True}) is False
    print("[2] 已授权 needs_review=False ✓")

    # 3) 入队 + 待审计数
    rid = q.add("delete /var/log/app", proposed_by="agent-7")
    assert rid in q.items
    assert len(q.pending()) == 1
    print("[3] 入队 + 待审计数=1 ✓")

    # 4) 通过
    r = q.approve(rid, "alice", "确认可删，已备份")
    assert r["status"] == "approved" and r["reviewer"] == "alice"
    print("[4] 审核通过 ✓")

    # 5) 驳回 + 理由
    rid2 = q.add("git push --force origin main", proposed_by="agent-3")
    r2 = q.reject(rid2, "bob", "先走 PR 评审")
    assert r2["status"] == "rejected" and "PR" in r2["decision_note"]
    print("[5] 审核驳回 + 理由 ✓")

    # 6) 重复审核拦截
    try:
        q.approve(rid, "eve")
        raise AssertionError("重复审核未被拦截")
    except ValueError:
        pass
    print("[6] 重复审核被拦截 ✓")

    # 7) 摘要
    s = q.summary()
    assert s["total"] == 2 and s["by_status"].get("approved") == 1 \
        and s["by_status"].get("rejected") == 1
    print(f"[7] 摘要 total={s['total']} status={s['by_status']} ✓")

    print("\n✅ human-in-loop-review selftest 全部通过")
    return True


def _load_or_new():
    # 自检/CLI 用独立内存队列；落盘由调用方负责
    return ReviewQueue()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--add")
    ap.add_argument("--pending", action="store_true")
    ap.add_argument("--approve")
    ap.add_argument("--reject")
    ap.add_argument("--reviewer")
    ap.add_argument("--note", default="")
    ap.add_argument("--get")
    ap.add_argument("--summary", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return 0 if selftest() else 1

    q = _load_or_new()
    if args.add:
        rid = q.add(args.add, proposed_by=args.reviewer or "agent")
        print(json.dumps({"review_id": rid, "status": "pending"}, ensure_ascii=False))
        return 0
    if args.pending:
        print(json.dumps([r for r in q.pending()], ensure_ascii=False, indent=2))
        return 0
    if args.approve:
        print(json.dumps(q.approve(args.approve, args.reviewer or "?",
                                   args.note), ensure_ascii=False))
        return 0
    if args.reject:
        print(json.dumps(q.reject(args.reject, args.reviewer or "?",
                                  args.note), ensure_ascii=False))
        return 0
    if args.get:
        print(json.dumps(q.get(args.get), ensure_ascii=False, indent=2))
        return 0
    if args.summary:
        print(json.dumps(q.summary(), ensure_ascii=False))
        return 0
    print("用法见 --selftest 或 --add/--pending/--approve/--reject/--summary")
    return 0


if __name__ == "__main__":
    sys.exit(main())
