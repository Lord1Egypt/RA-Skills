"""补跑上一轮因传输层原因（429/断流等, finish_reason=error）失败的题目。

复用 intel_check 的 run_one / 题目构造逻辑（prompt、temperature=1.0、top_p=0.95、
effort=high 完全一致），只是把并发降到 2，并且只跑指定的失败题。
用法: python rerun_failed.py <上轮results.jsonl>
"""
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import intel_check as k3_check  # 复用: make_client / run_one / gpqa_items / load_jsonl

ROOT = Path(__file__).resolve().parent


def main():
    prev_path = Path(sys.argv[1])
    prev = [json.loads(l) for l in open(prev_path, encoding="utf-8") if l.strip()]
    failed = {(r["kind"], r["id"]) for r in prev if r.get("finish_reason") in ("error", None)}
    if not failed:
        sys.exit("上一轮没有 error/断流 题，无需补跑")

    gpqa_all = k3_check.gpqa_items(k3_check.load_jsonl(k3_check.DATA / "gpqa_diamond_50.jsonl"), 50)
    aime_all = k3_check.load_jsonl(k3_check.DATA / "aime2025.jsonl")

    jobs = []  # (kind, item, correct_letter)
    for it in gpqa_all:
        if ("gpqa", it["id"]) in failed:
            jobs.append(("gpqa", it, it["correct_letter"]))
    for i, it in enumerate(aime_all):
        if ("aime", str(it["id"])) in failed or ("aime", it["id"]) in failed:
            jobs.append(("aime", it, None))

    print(f"补跑 {len(jobs)} 题 | concurrency=2")
    client = k3_check.make_client()
    model = "kimi-k3"
    results = []
    with ThreadPoolExecutor(max_workers=2) as ex:
        futs = {ex.submit(k3_check.run_one, client, model, it, kind, cl): (kind, it["id"])
                for kind, it, cl in jobs}
        for fut in as_completed(futs):
            kind, iid = futs[fut]
            try:
                r = fut.result()
            except Exception as e:
                r = {"kind": kind, "id": iid, "target": None, "extracted": None,
                     "correct": False, "finish_reason": "error", "completion": f"ERROR: {e}"}
            results.append(r)
            print(f"[{len(results)}/{len(jobs)}] {r['kind']}#{r['id']} "
                  f"{'OK ' if r['correct'] else 'MISS'} extracted={r.get('extracted')!r} finish={r['finish_reason']}")

    stamp = time.strftime("%Y%m%d_%H%M%S")
    out = ROOT / "results" / f"rerun_{stamp}.jsonl"
    out.parent.mkdir(exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        for r in sorted(results, key=lambda x: (x["kind"], str(x["id"]))):
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    ok = sum(r["correct"] for r in results)
    err = sum(1 for r in results if r["finish_reason"] == "error")
    print(f"\n补跑结果: {ok}/{len(results)} 正确, 仍失败 {err} 题 | 明细: {out}")


if __name__ == "__main__":
    main()
