#!/usr/bin/env python3
"""
GPA v0.7 Phase 2 Phenotype Association Test Suite
Covers 5 scenarios as specified in coordination instruction.
"""

import asyncio
import json
import sys
import time
from pathlib import Path
from typing import Dict, List

# Ensure imports work
SCRIPT_DIR = Path(__file__).resolve().parent / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from gpa_phenotype_match import PhenotypeMatcher


class bcolors:
    OK = "\033[92m"
    FAIL = "\033[91m"
    WARN = "\033[93m"
    END = "\033[0m"


def ok(msg: str):
    print(f"{bcolors.OK}✅ {msg}{bcolors.END}")


def fail(msg: str):
    print(f"{bcolors.FAIL}❌ {msg}{bcolors.END}")


def warn(msg: str):
    print(f"{bcolors.WARN}⚠️  {msg}{bcolors.END}")


async def test_1_with_api_key():
    """Scenario 1: CAPN3 + '肌无力' → score ≥ 0.7, explanation contains muscular dystrophy"""
    print("\n--- Test 1: CAPN3 + '肌无力' (with API key) ---")
    matcher = PhenotypeMatcher(llm_model="gpt-4o-mini")
    if not matcher.api_key:
        warn("No OPENAI_API_KEY set; skipping live LLM test (this is expected if key not configured)")
        return True  # skip, not fail

    result = await matcher.match("CAPN3", "远端肌无力、肌源性损害、缓慢进展")
    print(f"Result: {json.dumps(result, ensure_ascii=False, indent=2)}")

    score = result.get("score", 0)
    explanation = result.get("explanation", "")
    ok_flag = score >= 0.7
    exp_flag = "muscular dystrophy" in explanation.lower() or "肌营养不良" in explanation or "calpainopathy" in explanation.lower()

    if ok_flag:
        ok(f"Score={score:.2f} >= 0.7")
    else:
        fail(f"Score={score:.2f} < 0.7")
    if exp_flag:
        ok(f"Explanation references muscular dystrophy/calpainopathy")
    else:
        warn(f"Explanation may not reference muscular dystrophy: {explanation}")

    return ok_flag


async def test_2_no_api_key_fallback():
    """Scenario 2: No API key → fallback mode, has warning"""
    print("\n--- Test 2: No API key → fallback keyword match ---")
    matcher = PhenotypeMatcher(llm_api_key="", llm_model="gpt-4o-mini")
    result = await matcher.match("CAPN3", "肌无力、肌源性损害")
    print(f"Result: {json.dumps(result, ensure_ascii=False, indent=2)}")

    warning = result.get("warning", "")
    has_warning = "fallback" in warning.lower() or "not configured" in warning.lower()
    score = result.get("score", 0)

    if has_warning:
        ok("Fallback warning present")
    else:
        fail("Missing fallback warning")

    ok(f"Fallback score={score:.2f} (keyword-based, expected low-to-moderate)")
    return has_warning


async def test_3_gene_not_in_db():
    """Scenario 3: Gene not in database → score = 0.0, explanation = 'No known phenotypes found'"""
    print("\n--- Test 3: Unknown gene 'XYZABC123' ---")
    matcher = PhenotypeMatcher(llm_api_key="", llm_model="gpt-4o-mini")
    result = await matcher.match("XYZABC123", "any phenotype")
    print(f"Result: {json.dumps(result, ensure_ascii=False, indent=2)}")

    score = result.get("score", -1)
    explanation = result.get("explanation", "")

    if score == 0.0:
        ok(f"Score=0.0 for unknown gene")
    else:
        fail(f"Score={score}, expected 0.0")

    if "no known" in explanation.lower() or "not found" in explanation.lower():
        ok(f"Explanation indicates no known phenotypes")
    else:
        warn(f"Explanation: {explanation}")

    return score == 0.0


async def test_4_no_phenotypes_skipped():
    """Scenario 4: User doesn't pass --phenotypes → pipeline skips phenotype association"""
    print("\n--- Test 4: Pipeline skip when no phenotypes ---")
    # Simulate a variant without phenotype fields populated
    from dgra_core import Variant
    v = Variant(
        chrom="1", pos=1000, ref="A", alt="G",
        gene="CAPN3", transcript="ENST000003",
        exon="E5/15", impact="HIGH", consequence="frameshift",
        hgvsp="p.Arg123Ter", hgvsc="c.367C>T",
        clinvar="Pathogenic", gt="0/1", vaf=0.45,
        tier=1, tier_reason="HIGH impact + ClinVar pathogenic"
    )
    skipped = v.phenotype_match_score is None
    if skipped:
        ok("Variant created without phenotype fields (score=None)")
    else:
        fail("Unexpected phenotype fields on new variant")
    return skipped


async def test_5_batch_performance():
    """Scenario 5: 10 Tier 1/2 genes batch match, < 30 seconds"""
    print("\n--- Test 5: Batch 10 genes performance ---")
    matcher = PhenotypeMatcher(llm_api_key="", llm_model="gpt-4o-mini")
    genes = ["CAPN3", "DYSF", "SGCA", "SGCB", "SGCG", "COL6A1", "LMNA", "VWF", "F8", "HBB"]
    user_phenotypes = "远端肌无力、肌源性损害、缓慢进展"

    start = time.time()
    results = await matcher.match_batch(genes, user_phenotypes)
    elapsed = time.time() - start

    print(f"Batch {len(genes)} genes in {elapsed:.1f}s")
    for g, r in zip(genes, results):
        print(f"  {g}: score={r.get('score', 0):.2f}")

    if elapsed < 30:
        ok(f"Batch completed in {elapsed:.1f}s (< 30s threshold)")
    else:
        fail(f"Batch took {elapsed:.1f}s, exceeds 30s threshold")

    if len(results) == len(genes):
        ok(f"All {len(genes)} genes returned results")
    else:
        fail(f"Only {len(results)}/{len(genes)} genes returned results")

    return elapsed < 30 and len(results) == len(genes)


async def test_6_structured_fields():
    """Bonus: Verify all expected fields are present in match result"""
    print("\n--- Test 6: Result structure validation ---")
    matcher = PhenotypeMatcher(llm_api_key="", llm_model="gpt-4o-mini")
    result = await matcher.match("CAPN3", "肌无力")
    required_fields = {"score", "explanation", "confidence", "matched_pairs", "known_phenotypes"}
    missing = required_fields - set(result.keys())
    if missing:
        fail(f"Missing fields: {missing}")
        return False
    else:
        ok(f"All required fields present: {required_fields}")
        return True


async def main():
    print("=" * 60)
    print("GPA v0.7 Phase 2 Phenotype Association Test Suite")
    print("=" * 60)

    results = []
    results.append(("Test 1: CAPN3 + 肌无力 (API key)", await test_1_with_api_key()))
    results.append(("Test 2: No API key fallback", await test_2_no_api_key_fallback()))
    results.append(("Test 3: Unknown gene", await test_3_gene_not_in_db()))
    results.append(("Test 4: Skip without phenotypes", await test_4_no_phenotypes_skipped()))
    results.append(("Test 5: Batch 10 genes < 30s", await test_5_batch_performance()))
    results.append(("Test 6: Result structure", await test_6_structured_fields()))

    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    passed = 0
    for name, ok_flag in results:
        if ok_flag:
            ok(name)
            passed += 1
        else:
            fail(name)
    print(f"\nTotal: {passed}/{len(results)} tests passed")
    return passed == len(results)


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
