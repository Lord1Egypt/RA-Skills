#!/usr/bin/env python3
"""
Optimized tagging: Rule pre-filter → LLM coarse split → LLM fine tag for positives only.

Flow:
  Mining results
    ↓
  Rule pre-filter (obvious neg/pos → direct library, no LLM)
    ↓
  Remaining ambiguous → LLM coarse split (library + relevance only)
    ↓
  Only positive → LLM fine tag (primary_type + is_complete_attribute_phrase)
    ↓
  Merge output → Excel
"""
import json, os, sys, re, time

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.dirname(SCRIPTS_DIR)
MINED_JSON = "/root/.linkfox/workspaces/linkfox/2026-08-09/adC1jVcn0LFCnZRb94Rpr/data/linkfox-amazon-suggestion-miner-1786285592612667.json"
OUT_XLSX = "/root/.linkfox/workspaces/linkfox/2026-08-09/adC1jVcn0LFCnZRb94Rpr/data/apparel_keywords_tagged.xlsx"

sys.path.insert(0, SCRIPTS_DIR)
sys.path.insert(0, SKILL_ROOT)
os.chdir(SCRIPTS_DIR)

from llm_tagger import validate_item
from excel_writer import write_apparel_excel
from suggestion_miner import linkfox_llm_call

# ============================================================
# Load data
# ============================================================
with open(MINED_JSON) as f:
    mined = json.load(f)
raw_kws = [kw.get("keyword", "") for kw in mined.get("keywords", []) if kw.get("keyword")]
pc = mined.get("product_context", "")
seed = mined.get("seed", "women long sleeve dress")
modes = mined.get("modes", ["expand", "az", "numbers", "reverse", "gap"])

print(f"Loaded {len(raw_kws)} keywords", flush=True)

# ============================================================
# Stage 0: Rule pre-filter
# ============================================================

# Competitor brands (auto-detected from keyword patterns)
COMPETITOR_BRANDS = {
    "zara", "h&m", "shein", "forever 21", "nordstrom", "macy", "target",
    "walmart", "amazon essentials", "old navy", "gap", "banana republic",
    "american eagle", "loft", "ann taylor", "j.crew", "jcrew",
    "dokotoo", "zanzea", "dowerme", "bobsrun", "oisdo", "yeenor",
    "catherines", "coldwater creek", "roamans", "woman within",
    "efsle", "yimoon", "tianermu", "luvamia", "tanming",
}

# Attributes from product_context (parsed)
PC_LOWER = pc.lower()

# Product gender
IS_WOMENS = any(w in PC_LOWER for w in ["women", "women's", "ladies", "her"])
IS_MENS = any(w in PC_LOWER for w in ["men", "men's", "him"])

# Product sleeve type
HAS_LONG_SLEEVE = "long sleeve" in PC_LOWER
HAS_SHORT_SLEEVE = "short sleeve" in PC_LOWER
HAS_SLEEVELESS = "sleeveless" in PC_LOWER

# Product length
IS_MINI = "above the knee" in PC_LOWER or "mini" in PC_LOWER or "above-the-knee" in PC_LOWER
IS_MIDI = "midi" in PC_LOWER
IS_MAXI = "maxi" in PC_LOWER

# Product category
IS_DRESS = "dress" in PC_LOWER
IS_TOP = any(w in PC_LOWER for w in ["top", "blouse", "shirt", "t-shirt"])
IS_PANTS = any(w in PC_LOWER for w in ["pants", "trouser", "jean"])
IS_SKIRT = "skirt" in PC_LOWER

# Conflict categories
NON_DRESS_CATS = ["jacket", "coat", "pants", "jeans", "shorts", "skirt", "leggings",
                  "sweater", "hoodie", "cardigan", "jumpsuit", "romper", "swim",
                  "bikini", "bra", "underwear", "lingerie", "pajama", "sleep"]
if IS_DRESS:
    CONFLICT_CATS = [c for c in NON_DRESS_CATS if c not in ["skirt"]]
elif IS_TOP:
    CONFLICT_CATS = ["dress", "jacket", "pants", "jeans", "shorts", "skirt"]
else:
    CONFLICT_CATS = []


def rule_prefilter(keyword):
    """Return (library, primary_type, reason) or None if ambiguous (needs LLM)."""
    kw_lower = keyword.lower()

    # --- Obvious NEGATIVE ---
    # 1. Competitor brand
    for brand in COMPETITOR_BRANDS:
        if brand in kw_lower:
            return ("negative", "Competitor", f"brand:{brand}")

    # 2. Gender conflict
    if IS_WOMENS and not IS_MENS:
        if re.search(r'\bmen\b|\bmen\'s\b|\bboys?\b|\bgentleman\b', kw_lower):
            # But allow "women" in the keyword
            if not re.search(r'\bwomen\b|\bwomen\'s\b|\bladies?\b', kw_lower):
                return ("negative", "Audience", "gender_conflict:men_for_womens_product")
    if IS_MENS and not IS_WOMENS:
        if re.search(r'\bwomen\b|\bwomen\'s\b|\bladies?\b|\bgirls?\b', kw_lower):
            return ("negative", "Audience", "gender_conflict:women_for_mens_product")

    # 3. Sleeve conflict
    if HAS_LONG_SLEEVE and not HAS_SHORT_SLEEVE:
        if "sleeveless" in kw_lower or "short sleeve" in kw_lower or "short-sleeve" in kw_lower:
            return ("negative", "Sleeve Type", "sleeve_conflict:short/sleeveless_for_long_sleeve")
    if HAS_SHORT_SLEEVE and not HAS_LONG_SLEEVE:
        if "long sleeve" in kw_lower or "long-sleeve" in kw_lower:
            return ("negative", "Sleeve Type", "sleeve_conflict:long_for_short_sleeve")
    if HAS_SLEEVELESS and not HAS_LONG_SLEEVE and not HAS_SHORT_SLEEVE:
        if "long sleeve" in kw_lower or "short sleeve" in kw_lower:
            return ("negative", "Sleeve Type", "sleeve_conflict:has_sleeves_for_sleeveless")

    # 4. Length conflict
    if IS_MINI and not IS_MIDI and not IS_MAXI:
        if "maxi" in kw_lower or "floor length" in kw_lower or "ankle length" in kw_lower:
            return ("negative", "Dress Length", "length_conflict:maxi_for_mini_product")
        if "midi" in kw_lower and "above the knee" not in kw_lower:
            return ("negative", "Dress Length", "length_conflict:midi_for_mini_product")
    if IS_MAXI and not IS_MINI and not IS_MIDI:
        if "above the knee" in kw_lower or "mini" in kw_lower or "mid thigh" in kw_lower:
            return ("negative", "Dress Length", "length_conflict:mini_for_maxi_product")

    # 5. Category conflict (dress product but keyword is about non-dress)
    if CONFLICT_CATS:
        for cat in CONFLICT_CATS:
            if re.search(r'\b' + re.escape(cat) + r'\b', kw_lower):
                # Allow if keyword also contains the product category (e.g., "dress shirt" for dress)
                if IS_DRESS and "dress" in kw_lower:
                    # "dress shirt" is not a dress → negative
                    if cat in ["shirt", "blouse", "top"]:
                        return ("negative", "Other", f"category_conflict:{cat}_not_dress")
                    continue
                if IS_TOP and ("top" in kw_lower or "blouse" in kw_lower or "shirt" in kw_lower):
                    continue
                return ("negative", "Other", f"category_conflict:{cat}")

    # 6. Non-apparel (swim, underwear, etc.)
    for non_apparel in ["swim", "bikini", "bra", "underwear", "lingerie", "pajama", "sleepwear"]:
        if non_apparel in kw_lower:
            return ("negative", "Other", f"non_apparel:{non_apparel}")

    # --- Obvious POSITIVE (core product match) ---
    # 7. Exact seed or very close variant
    if kw_lower == seed.lower() or kw_lower == seed.lower() + "s":
        return ("positive", "Core Product", "seed_match")

    # 8. Keyword contains product's key attributes + product category
    if IS_DRESS and IS_WOMENS:
        has_dress = "dress" in kw_lower
        has_women = any(w in kw_lower for w in ["women", "women's", "ladies"])
        has_long_sleeve = "long sleeve" in kw_lower or "long-sleeve" in kw_lower
        has_floral = "floral" in kw_lower
        has_v_neck = "v neck" in kw_lower or "v-neck" in kw_lower
        has_pockets = "pocket" in kw_lower

        # If keyword has 2+ matching attributes + category → likely positive
        match_count = sum([has_dress, has_long_sleeve, has_floral, has_v_neck, has_pockets, has_women])
        if match_count >= 3 and has_dress:
            return ("positive", "Core Product", f"attribute_match:{match_count}")

    # --- AMBIGUOUS: needs LLM ---
    return None


# Apply rule pre-filter
rule_pos = []
rule_neg = []
ambiguous = []

for kw in raw_kws:
    result = rule_prefilter(kw)
    if result is None:
        ambiguous.append(kw)
    else:
        library, ptype, reason = result
        item = validate_item({
            "keyword": kw, "primary_type": ptype,
            "secondary_types": [], "attribute_categories": [],
            "is_complete_attribute_phrase": False,
            "relevance": "high" if library == "positive" else "low",
            "library": library,
            "suggested_positions": ["title", "bullet"] if library == "positive" else ["negative"],
            "confidence": 0.95,
        })
        item["relevance_reason"] = reason
        if library == "positive":
            rule_pos.append(item)
        else:
            rule_neg.append(item)

print(f"\n=== Rule Pre-filter ===")
print(f"  Direct positive: {len(rule_pos)}")
print(f"  Direct negative: {len(rule_neg)}")
print(f"  Ambiguous (→ LLM): {len(ambiguous)}")
print(f"  LLM reduction: {100*(1 - len(ambiguous)/len(raw_kws)):.0f}% keywords handled by rules")

# ============================================================
# Stage 1: LLM coarse split (ambiguous keywords only)
# ============================================================

COARSE_SYSTEM = """You are an Amazon Apparel Keyword classifier. Classify each keyword into exactly one library based on the Product Context.

Rules:
- positive: keyword attributes match the product in the Product Context
- negative: keyword attributes conflict with the product (wrong sleeve, wrong length, wrong gender, wrong category, competitor brand)
- review: ambiguous or uncertain

Output ONLY a JSON array of objects with fields: keyword, library, relevance.
No explanations. No markdown. Just JSON array."""

COARSE_USER_TMPL = """【Product Context】
{product_context}

【Seed Keyword】
{seed}

【Keywords to Classify】(Total: {n})
{keyword_list}

Output JSON array. Each item: {{"keyword":"","library":"positive|negative|review","relevance":"high|medium|low|irrelevant"}}. No other fields."""

BATCH = 100
print(f"\n=== Stage 1: LLM Coarse Split ({len(ambiguous)} keywords, batch={BATCH}) ===")

coarse_results = []
t_start = time.time()

for i in range(0, len(ambiguous), BATCH):
    batch = ambiguous[i:i+BATCH]
    bn = i // BATCH + 1
    total_bn = (len(ambiguous) + BATCH - 1) // BATCH
    t0 = time.time()

    user_prompt = COARSE_USER_TMPL.format(
        product_context=pc, seed=seed, n=len(batch),
        keyword_list="\n".join(f"{j+1}. {kw}" for j, kw in enumerate(batch))
    )

    ok = False
    for attempt in range(2):
        try:
            raw = linkfox_llm_call(COARSE_SYSTEM, user_prompt)
            # Parse JSON array (might be wrapped in {"results":[...]} or just [...])
            raw_stripped = raw.strip()
            if raw_stripped.startswith("{"):
                parsed = json.loads(raw_stripped)
                items = parsed.get("results", parsed.get("data", []))
                if isinstance(items, dict):
                    items = [items]
            else:
                items = json.loads(raw_stripped)

            for item in items:
                coarse_results.append({
                    "keyword": item.get("keyword", ""),
                    "library": item.get("library", "review"),
                    "relevance": item.get("relevance", "medium"),
                })
            ok = True
            break
        except Exception as e:
            print(f"  Batch {bn}/{total_bn}: attempt {attempt+1} failed: {e}", flush=True)
            time.sleep(3)

    if not ok:
        for kw in batch:
            coarse_results.append({"keyword": kw, "library": "review", "relevance": "medium"})

    t1 = time.time()
    pos_cnt = sum(1 for r in coarse_results[-len(batch):] if r["library"] == "positive")
    print(f"  Batch {bn}/{total_bn}: done {t1-t0:.0f}s, pos={pos_cnt}, elapsed={t1-t_start:.0f}s", flush=True)

t_coarse = time.time() - t_start
coarse_pos = [r for r in coarse_results if r["library"] == "positive"]
coarse_neg = [r for r in coarse_results if r["library"] == "negative"]
coarse_rev = [r for r in coarse_results if r["library"] == "review"]

print(f"\n  Coarse split done in {t_coarse:.0f}s")
print(f"  positive={len(coarse_pos)} negative={len(coarse_neg)} review={len(coarse_rev)}")

# ============================================================
# Stage 2: LLM fine tag (positive keywords only)
# ============================================================

FINE_SYSTEM = """You are an Amazon Apparel Keyword attribute expert. For each keyword, identify its primary_type and whether it contains a complete attribute phrase.

Multi-word attributes are complete units: "Above the Knee", "Off-the-Shoulder", "Fit & Flare", "3/4 Sleeve", "V Neck".

primary_type enum (single choice):
Core Product, Dress Length, Neckline, Sleeve Type, Silhouette, Fit, Occasion, Pattern, Material, Size Type, Color, Style, Closure Type, Care, Feature, Selling Point, Scenario, Audience, Specification, Question, Brand, Competitor, Other

Output ONLY a JSON array. Each item: keyword, primary_type, attribute_categories, is_complete_attribute_phrase, suggested_positions, confidence.
No explanations."""

FINE_USER_TMPL = """【Product Context】
{product_context}

【Keywords to Tag】(Total: {n})
{keyword_list}

Output JSON array. Each: {{"keyword":"","primary_type":"","attribute_categories":[],"is_complete_attribute_phrase":false,"suggested_positions":[],"confidence":0.0}}"""

# Only positive keywords need fine tagging
fine_kws = [r["keyword"] for r in coarse_pos]
# Also include rule-filtered positive keywords
fine_kws_all = [r["keyword"] for r in rule_pos] + fine_kws

print(f"\n=== Stage 2: LLM Fine Tag ({len(fine_kws_all)} positive keywords, batch={BATCH}) ===")

fine_results = {}
t_start = time.time()

for i in range(0, len(fine_kws_all), BATCH):
    batch = fine_kws_all[i:i+BATCH]
    bn = i // BATCH + 1
    total_bn = (len(fine_kws_all) + BATCH - 1) // BATCH
    t0 = time.time()

    user_prompt = FINE_USER_TMPL.format(
        product_context=pc, n=len(batch),
        keyword_list="\n".join(f"{j+1}. {kw}" for j, kw in enumerate(batch))
    )

    ok = False
    for attempt in range(2):
        try:
            raw = linkfox_llm_call(FINE_SYSTEM, user_prompt)
            raw_stripped = raw.strip()
            if raw_stripped.startswith("{"):
                parsed = json.loads(raw_stripped)
                items = parsed.get("results", parsed.get("data", []))
                if isinstance(items, dict):
                    items = [items]
            else:
                items = json.loads(raw_stripped)

            for item in items:
                kw = item.get("keyword", "")
                fine_results[kw] = {
                    "primary_type": item.get("primary_type", "Other"),
                    "attribute_categories": item.get("attribute_categories", []),
                    "is_complete_attribute_phrase": bool(item.get("is_complete_attribute_phrase", False)),
                    "suggested_positions": item.get("suggested_positions", []),
                    "confidence": float(item.get("confidence", 0.8)),
                }
            ok = True
            break
        except Exception as e:
            print(f"  Batch {bn}/{total_bn}: attempt {attempt+1} failed: {e}", flush=True)
            time.sleep(3)

    if not ok:
        for kw in batch:
            fine_results[kw] = {
                "primary_type": "Core Product",
                "attribute_categories": [],
                "is_complete_attribute_phrase": False,
                "suggested_positions": ["title", "bullet"],
                "confidence": 0.6,
            }

    t1 = time.time()
    phrases = sum(1 for kw in batch if fine_results.get(kw, {}).get("is_complete_attribute_phrase"))
    print(f"  Batch {bn}/{total_bn}: done {t1-t0:.0f}s, phrases={phrases}, elapsed={t1-t_start:.0f}s", flush=True)

t_fine = time.time() - t_start
print(f"\n  Fine tag done in {t_fine:.0f}s")

# ============================================================
# Merge all results
# ============================================================

all_results = []

# Rule-positive + fine tag
for item in rule_pos:
    kw = item["keyword"]
    if kw in fine_results:
        item["primary_type"] = fine_results[kw]["primary_type"]
        item["attribute_categories"] = fine_results[kw]["attribute_categories"]
        item["is_complete_attribute_phrase"] = fine_results[kw]["is_complete_attribute_phrase"]
        item["suggested_positions"] = fine_results[kw]["suggested_positions"]
        item["confidence"] = fine_results[kw]["confidence"]
    all_results.append(item)

# Coarse results → merge with fine tag
for r in coarse_results:
    kw = r["keyword"]
    library = r["library"]
    relevance = r["relevance"]

    if library == "positive" and kw in fine_results:
        ft = fine_results[kw]
        all_results.append(validate_item({
            "keyword": kw,
            "primary_type": ft["primary_type"],
            "secondary_types": [],
            "attribute_categories": ft["attribute_categories"],
            "is_complete_attribute_phrase": ft["is_complete_attribute_phrase"],
            "relevance": relevance,
            "library": library,
            "suggested_positions": ft["suggested_positions"],
            "confidence": ft["confidence"],
        }))
    elif library == "positive":
        # Positive but no fine tag (shouldn't happen, but fallback)
        all_results.append(validate_item({
            "keyword": kw, "primary_type": "Core Product",
            "secondary_types": [], "attribute_categories": [],
            "is_complete_attribute_phrase": False,
            "relevance": relevance, "library": library,
            "suggested_positions": ["title", "bullet"], "confidence": 0.7,
        }))
    else:
        # Negative or review - no fine tag needed
        all_results.append(validate_item({
            "keyword": kw, "primary_type": "Other",
            "secondary_types": [], "attribute_categories": [],
            "is_complete_attribute_phrase": False,
            "relevance": relevance, "library": library,
            "suggested_positions": ["negative"] if library == "negative" else [],
            "confidence": 0.8,
        }))

# Rule-negative
all_results.extend(rule_neg)

# Summary
pos = [r for r in all_results if r.get("library") == "positive"]
neg = [r for r in all_results if r.get("library") == "negative"]
rev = [r for r in all_results if r.get("library") == "review"]
summary = {
    "positive_count": len(pos),
    "negative_count": len(neg),
    "review_count": len(rev),
    "high_relevance_count": sum(1 for r in all_results if r.get("relevance") == "high"),
    "complete_attribute_phrase_count": sum(1 for r in all_results if r.get("is_complete_attribute_phrase")),
}

t_total = time.time() - t_start if 't_start' not in dir() else 0
print(f"\n=== FINAL RESULTS ===")
print(f"  Total: {len(all_results)}")
print(f"  Positive: {summary['positive_count']}")
print(f"  Negative: {summary['negative_count']}")
print(f"  Review:   {summary['review_count']}")
print(f"  High relevance: {summary['high_relevance_count']}")
print(f"  Complete attribute phrases: {summary['complete_attribute_phrase_count']}")
print(f"  Rule-handled: {len(rule_pos) + len(rule_neg)} ({100*(len(rule_pos)+len(rule_neg))/len(raw_kws):.0f}%)")
print(f"  LLM coarse: {len(ambiguous)} keywords in {t_coarse:.0f}s")
print(f"  LLM fine: {len(fine_kws_all)} keywords in {t_fine:.0f}s")

# Save intermediate results (in case Excel writing fails)
_intermediate_path = os.path.join(os.path.dirname(OUT_XLSX), "tagged_results.json")
os.makedirs(os.path.dirname(_intermediate_path), exist_ok=True)
with open(_intermediate_path, "w", encoding="utf-8") as f:
    json.dump({"results": all_results, "summary": summary, "seed": seed,
               "product_context": pc, "modes": modes, "raw_keywords": raw_kws}, f, ensure_ascii=False)
print(f"  Intermediate results saved: {_intermediate_path}")

# Write Excel
os.makedirs(os.path.dirname(OUT_XLSX), exist_ok=True)
write_apparel_excel(
    output_path=OUT_XLSX, seed=seed, product_context=pc,
    tagged_results=all_results, positive=pos, negative=neg, review=rev,
    raw_keywords=raw_kws, summary=summary, modes=modes, market="US"
)
print(f"\nExcel: {OUT_XLSX}")
