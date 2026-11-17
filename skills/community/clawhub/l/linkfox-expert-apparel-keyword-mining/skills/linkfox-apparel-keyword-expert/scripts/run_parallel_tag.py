#!/usr/bin/env python3
"""
All-in-one: split keywords → tag 5 shards in parallel (threading) → combine → write Excel.
Run: python3 run_parallel_tag.py
"""
import json, os, sys, time, threading

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.dirname(SCRIPTS_DIR)
MINED_JSON = "/root/.linkfox/workspaces/linkfox/2026-08-09/adC1jVcn0LFCnZRb94Rpr/data/linkfox-amazon-suggestion-miner-1786285592612667.json"
OUT_XLSX = "/root/.linkfox/workspaces/linkfox/2026-08-09/adC1jVcn0LFCnZRb94Rpr/data/apparel_keywords_tagged.xlsx"

sys.path.insert(0, SCRIPTS_DIR)
sys.path.insert(0, SKILL_ROOT)
os.chdir(SCRIPTS_DIR)

from prompts.apparel_tagging import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE
from llm_tagger import validate_item, batch_list
from excel_writer import write_apparel_excel
from suggestion_miner import linkfox_llm_call

# Load mined data
with open(MINED_JSON) as f:
    mined = json.load(f)
raw_kws = [kw.get("keyword", "") for kw in mined.get("keywords", []) if kw.get("keyword")]
pc = mined.get("product_context", "")
seed = mined.get("seed", "women long sleeve dress")
modes = mined.get("modes", ["expand", "az", "numbers", "reverse", "gap"])

print(f"Loaded {len(raw_kws)} keywords", flush=True)

# Split into 5 shards
N_SHARDS = 5
shard_size = (len(raw_kws) + N_SHARDS - 1) // N_SHARDS
shards = [raw_kws[i*shard_size:(i+1)*shard_size] for i in range(N_SHARDS)]
print(f"Split into {N_SHARDS} shards: {[len(s) for s in shards]}", flush=True)

# Tag function for one shard
def tag_shard(shard_id, keywords, results_list, lock):
    BATCH = 100
    total_batches = (len(keywords) + BATCH - 1) // BATCH
    print(f"[Shard {shard_id}] {len(keywords)} kws, {total_batches} batches", flush=True)

    for bi, batch in enumerate(batch_list(keywords, BATCH)):
        bn = bi + 1
        t0 = time.time()
        print(f"[Shard {shard_id}] Batch {bn}/{total_batches}...", flush=True)

        user_prompt = USER_PROMPT_TEMPLATE.format(
            product_context=pc or "Not provided", seed=seed,
            n=len(batch),
            keyword_list="\n".join(f"{i+1}. {kw}" for i, kw in enumerate(batch))
        )

        ok = False
        for attempt in range(2):
            try:
                raw = linkfox_llm_call(SYSTEM_PROMPT, user_prompt)
                parsed = json.loads(raw)
                with lock:
                    for item in parsed.get("results", []):
                        results_list.append(validate_item(item))
                ok = True
                break
            except Exception as e:
                print(f"[Shard {shard_id}]   attempt {attempt+1} fail: {e}", flush=True)
                time.sleep(3)

        if not ok:
            with lock:
                for kw in batch:
                    results_list.append(validate_item({
                        "keyword": kw, "primary_type": "Other", "secondary_types": [],
                        "attribute_categories": [], "is_complete_attribute_phrase": False,
                        "relevance": "medium", "library": "review",
                        "suggested_positions": [], "confidence": 0.2
                    }))

        t1 = time.time()
        print(f"[Shard {shard_id}]   batch {bn} done {t1-t0:.0f}s", flush=True)

    print(f"[Shard {shard_id}] COMPLETE", flush=True)

# Launch 5 threads in parallel
all_results = []
lock = threading.Lock()
threads = []
t_start = time.time()

for i, shard in enumerate(shards):
    t = threading.Thread(target=tag_shard, args=(i+1, shard, all_results, lock))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

t_end = time.time()
print(f"\nAll shards done in {t_end-t_start:.0f}s ({(t_end-t_start)/60:.1f} min)", flush=True)

# Summary
pos = [r for r in all_results if r.get("library") == "positive"]
neg = [r for r in all_results if r.get("library") == "negative"]
rev = [r for r in all_results if r.get("library") == "review"]
summary = {
    "positive_count": len(pos), "negative_count": len(neg),
    "review_count": len(rev),
    "high_relevance_count": sum(1 for r in all_results if r.get("relevance") == "high"),
    "complete_attribute_phrase_count": sum(1 for r in all_results if r.get("is_complete_attribute_phrase")),
}

print(f"Positive: {summary['positive_count']}", flush=True)
print(f"Negative: {summary['negative_count']}", flush=True)
print(f"Review:   {summary['review_count']}", flush=True)
print(f"High relevance: {summary['high_relevance_count']}", flush=True)
print(f"Complete attribute phrases: {summary['complete_attribute_phrase_count']}", flush=True)

# Write Excel
os.makedirs(os.path.dirname(OUT_XLSX), exist_ok=True)
write_apparel_excel(
    output_path=OUT_XLSX, seed=seed, product_context=pc,
    tagged_results=all_results, positive=pos, negative=neg, review=rev,
    raw_keywords=raw_kws, summary=summary, modes=modes, market="US"
)
print(f"\nExcel: {OUT_XLSX}", flush=True)
