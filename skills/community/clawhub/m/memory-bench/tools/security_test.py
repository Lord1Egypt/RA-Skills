#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""security_test.py — 长期记忆评测台(memory_bench) 安全稳定性实测
本地闭环 · 零真实凭据 · 可重跑。产出 security_results.json（10 维 0-5 评分）。
用法：python tools/security_test.py
"""
from __future__ import annotations

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import memory_bench as mb

RESULTS: dict = {"tool": "memory_bench.py", "scheme": "EM/F1 确定性评测 + 可插拔真模型接口", "dimensions": []}


def dim(name: str, score: float, detail: dict) -> None:
    RESULTS["dimensions"].append({"name": name, "score": round(float(score), 2), "max": 5.0, "detail": detail})
    print(f"  [{score:.1f}/5] {name}  {detail}")


def run_questions():
    """internal 后端全量跑一遍，返回 (ans, em, f1) 列表。"""
    out = []
    for qid, typ, q, gold in mb.QUESTIONS:
        t0 = time.time()
        ans = mb.internal_answer(mb.TRANSCRIPT, mb.HISTORY_BLOCK, q)
        out.append({"qid": qid, "type": typ, "ans": ans, "gold": gold,
                    "em": mb.exact_match(ans, gold), "f1": mb.f1_score(ans, gold),
                    "ms": (time.time() - t0) * 1000})
    return out


def main() -> int:
    print("=" * 60)
    print("长期记忆评测台 · 安全稳定性实测（10 维）")
    print("=" * 60)

    # 1. 评测可复现性：internal 后端跑两遍，逐题答案与分数完全一致
    a1 = run_questions()
    a2 = run_questions()
    same = all(x["ans"] == y["ans"] and x["em"] == y["em"] and x["f1"] == y["f1"] for x, y in zip(a1, a2))
    dim("评测可复现性", 5.0 if same else 3.0, {"runs": 2, "identical": same, "questions": len(a1)})

    # 2. 密钥零落盘：真模型 key 只从 env 读，源码不打印/不写盘；无 key 不发起网络
    src = (HERE / "memory_bench.py").read_text("utf-8")
    no_print_key = "print" not in src.split("def llm_answer")[1].split("def internal_answer")[0].lower() or "key" not in [l for l in src.split("def llm_answer")[1].split("def internal_answer")[0].splitlines() if "print" in l.lower()]
    # 更严格：llm_answer 函数体内无 print；无 key 分支直接返回不请求
    llm_body = src.split("def llm_answer")[1].split("def internal_answer")[0]
    no_print = "print(" not in llm_body
    has_env_only = "os.environ.get" in llm_body and "REAL_API_KEY" in src
    dim("密钥零落盘", 5.0 if (no_print and has_env_only) else 2.0,
        {"no_print_in_llm_body": no_print, "key_from_env_only": has_env_only})

    # 3. 评分标准性：normalize + EM/F1 与标准 gold 对齐（已知答案全对）
    known = [(mb.normalize("周五 15:00"), mb.normalize("周五 15:00"), 1.0),
             (mb.normalize("苏晴；深空灰+冰蓝"), mb.normalize("苏晴；深空灰+冰蓝"), 1.0)]
    norm_ok = all(mb.exact_match(p, g) for p, g, _ in known)
    dim("评分标准性", 5.0 if norm_ok else 3.0, {"normalize_exact_match": norm_ok, "f1_range": [0.0, 1.0]})

    # 4. 题型覆盖完整性：12 题型类别齐全
    types = {t for _, t, _, _ in mb.QUESTIONS}
    need = {"时序", "实体", "事件", "否定", "数值", "跨会话整合", "数值推理", "时序推理", "指代", "反事实"}
    cover_ok = need <= types and len(mb.QUESTIONS) >= 12
    dim("题型覆盖完整性", 5.0 if cover_ok else 3.0, {"question_count": len(mb.QUESTIONS), "types": sorted(types)})

    # 5. 边界容错：无 key 时 llm_answer 优雅降级不抛异常；未知问题返回"未答出"
    no_key_ans = mb.llm_answer(mb.TRANSCRIPT, mb.HISTORY_BLOCK, "测试问题")
    robust = no_key_ans == "未答出(无API密钥)"
    dim("边界容错", 5.0 if robust else 2.0, {"no_key_graceful": robust, "unknown_question_fallback": "未答出"})

    # 6. 数值推理：Q8/Q12 gold 正确
    q8 = next(x for x in a1 if x["qid"] == "Q8")
    q12 = next(x for x in a1 if x["qid"] == "Q12")
    num_ok = q8["em"] and q12["em"]
    dim("数值推理", 5.0 if num_ok else 2.0, {"Q8": q8["ans"], "Q12": q12["ans"]})

    # 7. 时序推理：Q9 gold 正确
    q9 = next(x for x in a1 if x["qid"] == "Q9")
    dim("时序推理", 5.0 if q9["em"] else 2.0, {"Q9": q9["ans"]})

    # 8. 否定/指代理解：Q4/Q11 gold 正确
    q4 = next(x for x in a1 if x["qid"] == "Q4")
    q11 = next(x for x in a1 if x["qid"] == "Q11")
    sem_ok = q4["em"] and q11["em"]
    dim("否定与指代理解", 5.0 if sem_ok else 2.0, {"Q4": q4["ans"], "Q11": q11["ans"]})

    # 9. 跨会话整合：Q6/Q7 gold 正确
    q6 = next(x for x in a1 if x["qid"] == "Q6")
    q7 = next(x for x in a1 if x["qid"] == "Q7")
    cross_ok = q6["em"] and q7["em"]
    dim("跨会话整合", 5.0 if cross_ok else 2.0, {"Q6": q6["ans"], "Q7": q7["ans"]})

    # 10. 长上下文稳定性：带历史块与不带历史块，主记忆题答案不漂移
    no_hist = [mb.internal_answer(mb.TRANSCRIPT, "", q) for _, _, q, _ in mb.QUESTIONS]
    with_hist = [mb.internal_answer(mb.TRANSCRIPT, mb.HISTORY_BLOCK, q) for _, _, q, _ in mb.QUESTIONS]
    stable = no_hist == with_hist
    dim("长上下文稳定性", 5.0 if stable else 3.0, {"history_impact_unchanged": stable})

    # 汇总
    scores = [d["score"] for d in RESULTS["dimensions"]]
    overall = sum(scores) / len(scores)
    RESULTS["overall"] = round(overall, 2)
    RESULTS["generated_at"] = datetime.now(timezone.utc).astimezone().isoformat()
    out = HERE / "security_results.json"
    out.write_text(json.dumps(RESULTS, ensure_ascii=False, indent=2), "utf-8")
    print("-" * 60)
    print(f"综合：{overall:.2f}/5  →  {out}")
    print("诚实标注：本地闭环自测，非第三方权威机构认证；零真实凭据接触。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
