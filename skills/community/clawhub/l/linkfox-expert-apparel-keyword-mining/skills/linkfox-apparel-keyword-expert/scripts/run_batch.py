#!/usr/bin/env python3
"""
Run one batch at a time. Usage: python3 run_batch.py <batch_num>
Each batch = 80 keywords. Results saved to /root/.linkfox/workspaces/linkfox/2026-08-09/adC1jVcn0LFCnZRb94Rpr/data/batch_<n>.json
"""
import json, os, sys, time

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.dirname(SCRIPTS_DIR)
MINED_JSON = "/root/.linkfox/workspaces/linkfox/2026-08-09/adC1jVcn0LFCnZRb94Rpr/data/linkfox-amazon-suggestion-miner-1786285592612667.json"
DATA_DIR = os.path.dirname(MINED_JSON)

sys.path.insert(0, SCRIPTS_DIR)
sys.path.insert(0, SKILL_ROOT)
os.chdir(SCRIPTS_DIR)

from prompts.apparel_tagging import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE
from llm_tagger import validate_item, batch_list
from suggestion_miner import linkfox_llm_call

with open(MINED_JSON) as f:
    mined = json.load(f)

raw_kws = [kw.get("keyword","") for kw in mined.get("keywords",[]) if kw.get("keyword")]
pc = mined.get("product_context","")
seed = mined.get("seed","women long sleeve dress")

BATCH = 100
all_batches = batch_list(raw_kws, BATCH)
total_batches = len(all_batches)

batch_num = int(sys.argv[1])
if batch_num < 1 or batch_num > total_batches:
    print(f"Invalid batch number. Range: 1-{total_batches}")
    sys.exit(1)

batch = all_batches[batch_num - 1]
out_path = os.path.join(DATA_DIR, f"batch_{batch_num}.json")

print(f"Batch {batch_num}/{total_batches} ({len(batch)} keywords)", flush=True)
print(f"Keywords: {batch[0][:40]} ... {batch[-1][:40]}", flush=True)

user_prompt = USER_PROMPT_TEMPLATE.format(
    product_context=pc or "Not provided", seed=seed,
    n=len(batch),
    keyword_list="\n".join(f"{i+1}. {kw}" for i, kw in enumerate(batch))
)

t0 = time.time()
ok = False
for attempt in range(2):
    try:
        raw = linkfox_llm_call(SYSTEM_PROMPT, user_prompt)
        parsed = json.loads(raw)
        results = [validate_item(item) for item in parsed.get("results", [])]

        with open(out_path, "w") as f:
            json.dump(results, f, ensure_ascii=False)

        t1 = time.time()
        pos = sum(1 for r in results if r.get("library") == "positive")
        neg = sum(1 for r in results if r.get("library") == "negative")
        rev = sum(1 for r in results if r.get("library") == "review")
        phrases = sum(1 for r in results if r.get("is_complete_attribute_phrase"))

        print(f"\n=== Batch {batch_num} DONE in {t1-t0:.0f}s ===", flush=True)
        print(f"Results: {len(results)} | pos={pos} neg={neg} rev={rev} phrases={phrases}", flush=True)
        print(f"\nPositive keywords:", flush=True)
        for r in results:
            if r.get("library") == "positive":
                star = " ★" if r.get("is_complete_attribute_phrase") else ""
                print(f"  {r['keyword'][:50]:<50} {r['primary_type']}{star}", flush=True)
        print(f"\nNegative keywords (first 10):", flush=True)
        for r in [r for r in results if r.get("library") == "negative"][:10]:
            print(f"  {r['keyword'][:50]:<50} {r['primary_type']}", flush=True)
        if neg > 10:
            print(f"  ... and {neg-10} more", flush=True)
        print(f"\nSaved to: {out_path}", flush=True)
        ok = True
        break
    except Exception as e:
        print(f"  attempt {attempt+1} failed: {e}", flush=True)
        time.sleep(3)

if not ok:
    print(f"FAILED after 2 attempts", flush=True)
    sys.exit(1)
