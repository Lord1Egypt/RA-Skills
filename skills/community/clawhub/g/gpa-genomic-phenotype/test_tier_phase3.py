#!/usr/bin/env python3
"""
GPA v0.7 Phase 3 Tier Logic Refinement Test Suite
Covers 6 scenarios as specified in coordination instruction.
"""

import asyncio
import json
import sys
from pathlib import Path
from typing import Dict, List

SCRIPT_DIR = Path(__file__).resolve().parent / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from dgra_core import (
    Variant, Evidence, GPAConfig, classify_variant_tier,
    _is_rare_disease_gene, _load_rare_disease_genes
)


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


def make_variant(**kwargs) -> Variant:
    defaults = dict(
        chrom="1", pos=1000, ref="A", alt="G",
        gene="TEST", transcript="ENST000001", exon="E1/10",
        impact="HIGH", consequence="frameshift",
        hgvsp="p.Arg123Ter", hgvsc="c.367C>T",
        clinvar="Pathogenic", gt="0/1", vaf=0.45,
        tier=None, tier_reason="", tier_actions=[],
    )
    defaults.update(kwargs)
    return Variant(**defaults)


def mock_tissue_assessment(relevance="primary"):
    return {"relevance": relevance, "fast_track": False}


def mock_gnomad_info(status="rare", af=0.0001):
    return {"status": status, "af": af}


def mock_domain_info():
    return {"domain": "TEST_DOMAIN", "domain_integrity": "partially_destroyed"}


def test_1_clinvar_pathogenic_high_phenotype_match():
    """Scenario 1: ClinVar Pathogenic + phenotype_match_score=0.8 → Tier 1"""
    print("\n--- Test 1: ClinVar Pathogenic + phenotype_match_score=0.8 → Tier 1 ---")
    v = make_variant(
        gene="CAPN3", clinvar="Pathogenic", impact="HIGH",
        phenotype_match_score=0.8,
    )
    tissue = mock_tissue_assessment("primary")
    gnomad = mock_gnomad_info("rare", 0.0001)
    domain = mock_domain_info()

    tier, reason, actions = classify_variant_tier(
        v, domain, tissue, gnomad, None, None, {}, GPAConfig()
    )
    print(f"Tier={tier}, reason={reason}")

    if tier == 1:
        ok("Tier 1 for ClinVar Pathogenic + HIGH + phenotype_match=0.8")
    else:
        fail(f"Expected Tier 1, got Tier {tier}")
    return tier == 1


def test_2_clinvar_pathogenic_low_phenotype_match():
    """Scenario 2: ClinVar Pathogenic + phenotype_match_score=0.2 → Tier 2"""
    print("\n--- Test 2: ClinVar Pathogenic + phenotype_match_score=0.2 → Tier 2 ---")
    v = make_variant(
        gene="CAPN3", clinvar="Pathogenic", impact="HIGH",
        phenotype_match_score=0.2,
    )
    tissue = mock_tissue_assessment("primary")
    gnomad = mock_gnomad_info("rare", 0.0001)
    domain = mock_domain_info()

    tier, reason, actions = classify_variant_tier(
        v, domain, tissue, gnomad, None, None, {}, GPAConfig()
    )
    print(f"Tier={tier}, reason={reason}")

    if tier == 2:
        ok("Tier 2 for ClinVar Pathogenic + HIGH + phenotype mismatch (score=0.2)")
    else:
        fail(f"Expected Tier 2, got Tier {tier}")

    # Check upgrade condition
    has_upgrade = any("升级为 Tier 1" in uc for uc in v.upgrade_conditions)
    if has_upgrade:
        ok("Upgrade condition present")
    else:
        warn("Missing upgrade condition")

    # Check evidence chain
    ev = [e for e in v.evidence_chain if e.source == "ClinVar" and "phenotype mismatch" in e.rule]
    if ev and ev[0].weight == 0.30:
        ok("Evidence chain weight=0.30 for phenotype mismatch")
    else:
        warn(f"Evidence chain: {ev}")

    return tier == 2


def test_3_clinvar_pathogenic_no_phenotype():
    """Scenario 3: ClinVar Pathogenic + no phenotype_match_score → Tier 1 (old logic compat)"""
    print("\n--- Test 3: ClinVar Pathogenic + no phenotype_match_score → Tier 1 ---")
    v = make_variant(
        gene="CAPN3", clinvar="Pathogenic", impact="HIGH",
        phenotype_match_score=None,
    )
    tissue = mock_tissue_assessment("primary")
    gnomad = mock_gnomad_info("rare", 0.0001)
    domain = mock_domain_info()

    tier, reason, actions = classify_variant_tier(
        v, domain, tissue, gnomad, None, None, {}, GPAConfig()
    )
    print(f"Tier={tier}, reason={reason}")

    if tier == 1:
        ok("Tier 1 for ClinVar Pathogenic + HIGH + no phenotype (backward compatible)")
    else:
        fail(f"Expected Tier 1, got Tier {tier}")
    return tier == 1


def test_4_rare_disease_gene_common_polymorphism():
    """Scenario 4: 罕见病基因 (CAPN3) gnomAD AF=0.05 → Tier 2 (not Tier 3)"""
    print("\n--- Test 4: Rare disease gene + common polymorphism → Tier 2 ---")
    genes = _load_rare_disease_genes()
    ok(f"Loaded {len(genes)} rare disease genes")

    # Pick a known rare disease gene
    test_gene = "CAPN3" if "CAPN3" in genes else list(genes)[0]
    # Use LOW impact + synonymous to avoid triggering Priority 2a (missense)
    v = make_variant(
        gene=test_gene, clinvar="VUS", impact="LOW", consequence="synonymous",
        hgvsp="p.Arg123=", hgvsc="c.367C>T",
    )
    tissue = mock_tissue_assessment("none")  # "none" to avoid tissue-relevant triggers
    gnomad = mock_gnomad_info("common_polymorphism", 0.05)
    domain = {"domain": "TEST", "domain_integrity": "tolerated"}

    tier, reason, actions = classify_variant_tier(
        v, domain, tissue, gnomad, None, None, {}, GPAConfig()
    )
    print(f"Tier={tier}, reason={reason}")

    if tier == 2:
        ok(f"Tier 2 for rare disease gene {test_gene} with common polymorphism")
    else:
        fail(f"Expected Tier 2, got Tier {tier}")

    # Check QC flag
    if "COMMON_POLYMORPHISM_BUT_RARE_DISEASE_GENE" in v.qc_flags:
        ok("QC flag present")
    else:
        warn("Missing QC flag")

    return tier == 2


def test_5_non_rare_disease_gene_common_polymorphism():
    """Scenario 5: 非罕见病基因 gnomAD AF=0.05 → Tier 3"""
    print("\n--- Test 5: Non-rare disease gene + common polymorphism → Tier 3 ---")
    v = make_variant(
        gene="NOT_RARE_GENE_12345", clinvar="VUS", impact="LOW", consequence="synonymous",
        hgvsp="p.Arg123=", hgvsc="c.367C>T",
    )
    tissue = mock_tissue_assessment("none")
    gnomad = mock_gnomad_info("common_polymorphism", 0.05)
    domain = {"domain": "TEST", "domain_integrity": "tolerated"}

    tier, reason, actions = classify_variant_tier(
        v, domain, tissue, gnomad, None, None, {}, GPAConfig()
    )
    print(f"Tier={tier}, reason={reason}")

    if tier == 3:
        ok("Tier 3 for non-rare disease gene with common polymorphism")
    else:
        fail(f"Expected Tier 3, got Tier {tier}")
    return tier == 3


def test_6_regression_old_tests():
    """Scenario 6: Regression — old tests not broken"""
    print("\n--- Test 6: Regression checks ---")
    # Check _is_rare_disease_gene works
    assert _is_rare_disease_gene("CAPN3")
    ok("CAPN3 is a rare disease gene")
    assert not _is_rare_disease_gene("NOT_A_GENE")
    ok("NOT_A_GENE is not a rare disease gene")

    # Check basic tier classification still works
    v = make_variant(gene="VWF", clinvar="Pathogenic", impact="HIGH")
    tissue = mock_tissue_assessment("primary")
    gnomad = mock_gnomad_info("rare", 0.0001)
    domain = mock_domain_info()
    tier, reason, actions = classify_variant_tier(
        v, domain, tissue, gnomad, None, None, {}, GPAConfig()
    )
    if tier == 1:
        ok("Basic ClinVar Pathogenic + HIGH → Tier 1 still works")
    else:
        fail(f"Regression: expected Tier 1, got {tier}")
    return tier == 1


async def main():
    print("=" * 60)
    print("GPA v0.7 Phase 3 Tier Logic Refinement Test Suite")
    print("=" * 60)

    results = []
    results.append(("Test 1: ClinVar Pathogenic + phenotype=0.8 → Tier 1", test_1_clinvar_pathogenic_high_phenotype_match()))
    results.append(("Test 2: ClinVar Pathogenic + phenotype=0.2 → Tier 2", test_2_clinvar_pathogenic_low_phenotype_match()))
    results.append(("Test 3: ClinVar Pathogenic + no phenotype → Tier 1", test_3_clinvar_pathogenic_no_phenotype()))
    results.append(("Test 4: Rare disease gene + common AF → Tier 2", test_4_rare_disease_gene_common_polymorphism()))
    results.append(("Test 5: Non-rare disease gene + common AF → Tier 3", test_5_non_rare_disease_gene_common_polymorphism()))
    results.append(("Test 6: Regression checks", test_6_regression_old_tests()))

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
