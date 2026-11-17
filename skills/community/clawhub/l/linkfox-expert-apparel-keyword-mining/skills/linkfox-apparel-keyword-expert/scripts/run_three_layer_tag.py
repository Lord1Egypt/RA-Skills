#!/usr/bin/env python3
"""
Three-layer tagging architecture:
  Layer 1: Rules (0 LLM) - brand names, attribute conflicts, non-dress
  Layer 2: LLM lightweight coarse split (positive/negative/review only)
  Layer 3: LLM detailed tagging (only for positives from Layer 2)

This reduces LLM work from 1183 keywords to ~400 (layer 2) + ~150 (layer 3).
"""
import json, os, sys, re, time

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.dirname(SCRIPTS_DIR)
MINED_JSON = "/root/.linkfox/workspaces/linkfox/2026-08-09/adC1jVcn0LFCnZRb94Rpr/data/linkfox-amazon-suggestion-miner-1786285592612667.json"
OUT_XLSX = "/root/.linkfox/workspaces/linkfox/2026-08-09/adC1jVcn0LFCnZRb94Rpr/data/apparel_keywords_tagged.xlsx"

sys.path.insert(0, SCRIPTS_DIR)
sys.path.insert(0, SKILL_ROOT)
os.chdir(SCRIPTS_DIR)

from llm_tagger import validate_item, batch_list
from excel_writer import write_apparel_excel
from suggestion_miner import linkfox_llm_call

# ============================================================
# Load data
# ============================================================
with open(MINED_JSON) as f:
    mined = json.load(f)
raw_kws = [kw.get("keyword","") for kw in mined.get("keywords",[]) if kw.get("keyword")]
pc = mined.get("product_context","")
seed = mined.get("seed","women long sleeve dress")
modes = mined.get("modes",["expand","az","numbers","reverse","gap"])

print(f"Loaded {len(raw_kws)} keywords", flush=True)

# ============================================================
# Layer 1: Rule-based pre-filtering (0 LLM)
# ============================================================

# Known competitor/irrelevant brands
BRAND_NAMES = {
    "zara", "adidas", "nike", "h&m", "shein", "amazon", "dokotoo", "dowerme",
    "zanzea", "veromoda", "only", "gucci", "chanel", "dior", "louis vuitton",
    "tommy", "ralph lauren", "calvin klein", "gap", "old navy", "forever 21",
    "urban outfitters", "free people", "anthropologie", "nordstrom", "macy",
    "target", "walmart", "costco", "temu", "aliexpress"
}

# Non-dress items (when seed is "dress")
NON_DRESS_TERMS = {
    "dress shirt", "dressy tops", "dress tops", "dress blouse",
    "swim dress", "swimsuit", "swimwear", "cover up", "coverup",
    "jumpsuit", "romper", "overalls", "leggings", "jeans", "pants",
    "skirt only", "shorts", "underwear", "lingerie", "bra",
}

# Attribute conflicts based on product_context
# Product: women's long sleeve, above-the-knee, V-neck, shift, black, floral
CONFLICT_RULES = {
    "wrong_sleeve": ["short sleeve", "short-sleeve", "sleeveless", "cap sleeve",
                      "puff sleeve", "bell sleeve", "flutter sleeve", "cold shoulder",
                      "3/4 sleeve", "quarter sleeve"],
    "wrong_length": ["maxi", "floor length", "ankle length", "tea length"],
    "wrong_gender": ["for men", "mens", "men's", "men ", "boy", "boys"],
    "wrong_silhouette": ["bodycon", "body con", "fit and flare", "fit & flare",
                          "empire waist", "peplum", "babydoll"],
    "wrong_neckline": ["off shoulder", "off-shoulder", "off the shoulder",
                        "one shoulder", "halter", "square neck", "sweetheart",
                        "cowl neck", "boat neck", "scoop neck"],
}

def rule_classify(keyword, product_context):
    """Return (library, primary_type, reason) or None if needs LLM."""
    kw_lower = keyword.lower()

    # Check brand names
    for brand in BRAND_NAMES:
        if brand in kw_lower:
            return ("negative", "Competitor", f"brand:{brand}")

    # Check non-dress terms
    for term in NON_DRESS_TERMS:
        if term in kw_lower:
            return ("negative", "Other", f"not_dress:{term}")

    # Check attribute conflicts
    for conflict_type, terms in CONFLICT_RULES.items():
        for term in terms:
            if term in kw_lower:
                return ("negative", conflict_type, f"conflict:{conflict_type}:{term}")

    # Check question-style keywords
    if kw_lower.startswith(("what ", "how ", "which ", "why ", "is ", "are ", "can ", "do ")):
        return ("negative", "Question", "question_style")

    # Auto-positive: exact seed match or very close
    if kw_lower == seed.lower() or kw_lower == seed.lower() + "es" or kw_lower == seed.lower() + "s":
        return ("positive", "Core Product", "exact_seed_match")

    # Auto-positive: contains all key matching attributes
    has_women = "women" in kw_lower or "womens" in kw_lower
    has_long_sleeve = "long sleeve" in kw_lower or "long-sleeve" in kw_lower
    has_dress = "dress" in kw_lower
    if has_women and has_long_sleeve and has_dress:
        # But check for conflicting attributes first
        if not any(term in kw_lower for terms in CONFLICT_RULES.values() for term in terms):
            if not any(b in kw_lower for b in BRAND_NAMES):
                return ("positive", "Core Product", "rule:auto_positive")

    # Not classifiable by rules → needs LLM
    return None

# Apply Layer 1
t0 = time.time()
rule_results = []
llm_keywords = []

for kw in raw_kws:
    result = rule_classify(kw, pc)
    if result:
        library, ptype, reason = result
        rule_results.append({
            "keyword": kw,
            "primary_type": ptype,
            "secondary_types": [],
            "attribute_categories": [],
            "is_complete_attribute_phrase": False,
            "relevance": "high" if library == "positive" else "low",
            "library": library,
            "suggested_positions": ["title","bullet"] if library == "positive" else ["negative"],
            "confidence": 0.95,
            "normalized": kw,
            "relevance_reason": reason,
            "notes": "rule_based",
        })
    else:
        llm_keywords.append(kw)

t1 = time.time()
rule_pos = sum(1 for r in rule_results if r["library"] == "positive")
rule_neg = sum(1 for r in rule_results if r["library"] == "negative")
print(f"\nLayer 1 (Rules): {len(rule_results)} classified in {t1-t0:.1f}s", flush=True)
print(f"  auto-positive: {rule_pos}", flush=True)
print(f"  auto-negative: {rule_neg}", flush=True)
print(f"  → {len(llm_keywords)} keywords need LLM (was {len(raw_kws)})", flush=True)

# ============================================================
# Layer 2: LLM lightweight coarse split
# Only outputs: keyword + library (positive/negative/review)
# ~50 chars per keyword (vs ~376 in full tagging)
# ============================================================

LAYER2_PROMPT = """You are an apparel keyword classifier. Given a product context and a keyword list, classify each keyword as positive, negative, or review.

Rules:
- positive: keyword matches the product's real attributes (sleeve type, length, neckline, pattern, color, occasion, audience)
- negative: keyword conflicts with product attributes (wrong sleeve, wrong length, wrong color, wrong gender, different product type, competitor brand)
- review: ambiguous or partially matching, needs human review

Output ONLY a JSON array. Each item: {"keyword":"","library":""}. No other fields. No explanations.

Product Context: """ + pc + "\n\nKeywords:\n"

BATCH2 = 100
all_layer2_results = []
t_start_l2 = time.time()

print(f"\nLayer 2 (LLM coarse): {len(llm_keywords)} keywords, batch_size={BATCH2}", flush=True)

for bi, batch in enumerate(batch_list(llm_keywords, BATCH2)):
    bn = bi + 1
    total_b = (len(llm_keywords) + BATCH2 - 1) // BATCH2
    t0 = time.time()
    print(f"  Batch {bn}/{total_b} ({len(batch)} kws)...", flush=True)

    keyword_list = "\n".join(f"{i+1}. {kw}" for i, kw in enumerate(batch))
    user_prompt = LAYER2_PROMPT + keyword_list + f"\n\nTotal: {len(batch)}"

    ok = False
    for attempt in range(2):
        try:
            raw = linkfox_llm_call(user_prompt, "")
            # Try to parse JSON array
            parsed = json.loads(raw)
            if isinstance(parsed, list):
                for item in parsed:
                    kw = item.get("keyword", "")
                    lib = item.get("library", "review")
                    if lib not in ("positive", "negative", "review"):
                        lib = "review"
                    all_layer2_results.append({"keyword": kw, "library": lib})
                ok = True
                break
            elif isinstance(parsed, dict) and "results" in parsed:
                for item in parsed["results"]:
                    kw = item.get("keyword", "")
                    lib = item.get("library", "review")
                    if lib not in ("positive", "negative", "review"):
                        lib = "review"
                    all_layer2_results.append({"keyword": kw, "library": lib})
                ok = True
                break
        except Exception as e:
            print(f"    attempt {attempt+1} failed: {e}", flush=True)
            time.sleep(3)

    if not ok:
        print(f"    -> fallback to review", flush=True)
        for kw in batch:
            all_layer2_results.append({"keyword": kw, "library": "review"})

    t1 = time.time()
    pos_cnt = sum(1 for r in all_layer2_results[-len(batch):] if r["library"] == "positive")
    print(f"    done {t1-t0:.0f}s, pos={pos_cnt}", flush=True)

t_end_l2 = time.time()
l2_pos = sum(1 for r in all_layer2_results if r["library"] == "positive")
l2_neg = sum(1 for r in all_layer2_results if r["library"] == "negative")
l2_rev = sum(1 for r in all_layer2_results if r["library"] == "review")
print(f"Layer 2 done in {t_end_l2-t_start_l2:.0f}s: pos={l2_pos} neg={l2_neg} rev={l2_rev}", flush=True)

# ============================================================
# Layer 3: LLM detailed tagging (only for positives)
# Full attribute tagging with complete schema
# ============================================================

positive_keywords = [r["keyword"] for r in all_layer2_results if r["library"] == "positive"]
# Also include rule-based positives
positive_keywords.extend([r["keyword"] for r in rule_results if r["library"] == "positive"])
# Deduplicate
positive_keywords = list(dict.fromkeys(positive_keywords))

print(f"\nLayer 3 (LLM detailed): {len(positive_keywords)} positive keywords need detailed tagging", flush=True)

from prompts.apparel_tagging import SYSTEM_PROMPT as DETAILED_SYSTEM_PROMPT
from prompts.apparel_tagging import USER_PROMPT_TEMPLATE as DETAILED_USER_TEMPLATE

BATCH3 = 100
all_layer3_results = []
t_start_l3 = time.time()

if positive_keywords:
    total_b3 = (len(positive_keywords) + BATCH3 - 1) // BATCH3
    for bi, batch in enumerate(batch_list(positive_keywords, BATCH3)):
        bn = bi + 1
        t0 = time.time()
        print(f"  Batch {bn}/{total_b3} ({len(batch)} kws)...", flush=True)

        user_prompt = DETAILED_USER_TEMPLATE.format(
            product_context=pc or "Not provided", seed=seed,
            n=len(batch),
            keyword_list="\n".join(f"{i+1}. {kw}" for i, kw in enumerate(batch))
        )

        ok = False
        for attempt in range(2):
            try:
                raw = linkfox_llm_call(DETAILED_SYSTEM_PROMPT, user_prompt)
                parsed = json.loads(raw)
                for item in parsed.get("results", []):
                    all_layer3_results.append(validate_item(item))
                ok = True
                break
            except Exception as e:
                print(f"    attempt {attempt+1} failed: {e}", flush=True)
                time.sleep(3)

        if not ok:
            for kw in batch:
                all_layer3_results.append(validate_item({
                    "keyword": kw, "primary_type": "Core Product",
                    "secondary_types": [], "attribute_categories": [],
                    "is_complete_attribute_phrase": False,
                    "relevance": "high", "library": "positive",
                    "suggested_positions": ["title","bullet"], "confidence": 0.5
                }))

        t1 = time.time()
        print(f"    done {t1-t0:.0f}s", flush=True)

t_end_l3 = time.time()
print(f"Layer 3 done in {t_end_l3-t_start_l3:.0f}s", flush=True)

# ============================================================
# Merge all layers
# ============================================================

# Build a lookup for layer 3 detailed results
l3_lookup = {r["keyword"]: r for r in all_layer3_results}

# Build final results
final_results = []

# 1. Rule-based negatives (no LLM)
for r in rule_results:
    if r["library"] == "negative":
        final_results.append(r)

# 2. LLM coarse results
for r in all_layer2_results:
    kw = r["keyword"]
    lib = r["library"]
    if lib == "positive" and kw in l3_lookup:
        # Has detailed tagging from Layer 3
        final_results.append(l3_lookup[kw])
    else:
        # Use coarse result with minimal fields
        final_results.append({
            "keyword": kw,
            "primary_type": "Other",
            "secondary_types": [],
            "attribute_categories": [],
            "is_complete_attribute_phrase": False,
            "relevance": "low" if lib == "negative" else "medium",
            "library": lib,
            "suggested_positions": ["negative"] if lib == "negative" else [],
            "confidence": 0.8,
            "normalized": kw,
            "relevance_reason": f"llm_coarse:{lib}",
            "notes": "layer2_coarse",
        })

# 3. Rule-based positives (have detailed tagging from Layer 3 if they went through)
for r in rule_results:
    if r["library"] == "positive":
        if r["keyword"] in l3_lookup:
            # Use detailed result from Layer 3
            final_results.append(l3_lookup[r["keyword"]])
        else:
            final_results.append(r)

# ============================================================
# Summary & Excel
# ============================================================
pos = [r for r in final_results if r.get("library") == "positive"]
neg = [r for r in final_results if r.get("library") == "negative"]
rev = [r for r in final_results if r.get("library") == "review"]
summary = {
    "positive_count": len(pos),
    "negative_count": len(neg),
    "review_count": len(rev),
    "high_relevance_count": sum(1 for r in final_results if r.get("relevance") == "high"),
    "complete_attribute_phrase_count": sum(1 for r in final_results if r.get("is_complete_attribute_phrase")),
}

t_total = time.time()
print(f"\n=== ALL LAYERS DONE ===", flush=True)
print(f"Total time: {t_total-t0:.0f}s", flush=True)
print(f"  Layer 1 (rules): {len(rule_results)} keywords, 0s LLM", flush=True)
print(f"  Layer 2 (coarse LLM): {len(all_layer2_results)} keywords, {t_end_l2-t_start_l2:.0f}s", flush=True)
print(f"  Layer 3 (detailed LLM): {len(all_layer3_results)} keywords, {t_end_l3-t_start_l3:.0f}s", flush=True)
print(f"\nFinal results: {len(final_results)} keywords", flush=True)
print(f"  Positive: {summary['positive_count']}", flush=True)
print(f"  Negative: {summary['negative_count']}", flush=True)
print(f"  Review:   {summary['review_count']}", flush=True)
print(f"  High relevance: {summary['high_relevance_count']}", flush=True)
print(f"  Complete attribute phrases: {summary['complete_attribute_phrase_count']}", flush=True)

os.makedirs(os.path.dirname(OUT_XLSX), exist_ok=True)
write_apparel_excel(
    output_path=OUT_XLSX, seed=seed, product_context=pc,
    tagged_results=final_results, positive=pos, negative=neg, review=rev,
    raw_keywords=raw_kws, summary=summary, modes=modes, market="US"
)
print(f"\nExcel: {OUT_XLSX}", flush=True)
