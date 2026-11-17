#!/usr/bin/env python3
"""Sequential tagging: batch_size=100, proven reliable. ~20 min for 1183 keywords."""
import json, os, sys, time

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

with open(MINED_JSON) as f:
    mined = json.load(f)
raw_kws = [kw.get("keyword","") for kw in mined.get("keywords",[]) if kw.get("keyword")]
pc = mined.get("product_context","")
seed = mined.get("seed","women long sleeve dress")
modes = mined.get("modes",["expand","az","numbers","reverse","gap"])

BATCH = 100
total_batches = (len(raw_kws) + BATCH - 1) // BATCH
print(f"Loaded {len(raw_kws)} keywords, batch_size={BATCH}, {total_batches} batches", flush=True)
print(f"Estimated: ~{total_batches * 100 // 60} min", flush=True)

all_results = []
t_start = time.time()

for bi, batch in enumerate(batch_list(raw_kws, BATCH)):
    bn = bi + 1
    t0 = time.time()
    print(f"Batch {bn}/{total_batches} ({len(batch)} kws)...", flush=True)

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
            for item in parsed.get("results", []):
                all_results.append(validate_item(item))
            ok = True
            break
        except Exception as e:
            print(f"  attempt {attempt+1} failed: {e}", flush=True)
            time.sleep(3)

    if not ok:
        for kw in batch:
            all_results.append(validate_item({
                "keyword": kw, "primary_type": "Other", "secondary_types": [],
                "attribute_categories": [], "is_complete_attribute_phrase": False,
                "relevance": "medium", "library": "review",
                "suggested_positions": [], "confidence": 0.2
            }))

    t1 = time.time()
    pos_cnt = sum(1 for r in all_results if r.get("library") == "positive")
    elapsed = t1 - t_start
    print(f"  done {t1-t0:.0f}s | total_pos={pos_cnt} elapsed={elapsed:.0f}s", flush=True)

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

t_end = time.time()
print(f"\n=== DONE in {t_end-t_start:.0f}s ({(t_end-t_start)/60:.1f} min) ===")
print(f"Positive: {summary['positive_count']}")
print(f"Negative: {summary['negative_count']}")
print(f"Review:   {summary['review_count']}")
print(f"High relevance: {summary['high_relevance_count']}")
print(f"Complete attribute phrases: {summary['complete_attribute_phrase_count']}")

os.makedirs(os.path.dirname(OUT_XLSX), exist_ok=True)
write_apparel_excel(
    output_path=OUT_XLSX, seed=seed, product_context=pc,
    tagged_results=all_results, positive=pos, negative=neg, review=rev,
    raw_keywords=raw_kws, summary=summary, modes=modes, market="US"
)
print(f"\nExcel: {OUT_XLSX}")
