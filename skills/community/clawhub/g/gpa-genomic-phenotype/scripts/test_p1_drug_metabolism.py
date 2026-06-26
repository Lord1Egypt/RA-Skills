#!/usr/bin/env python3
"""
P1 Tests — Drug Metabolism Gene Expansion (v0.5.3)

Run: python3 test_p1_drug_metabolism.py
"""

import sys
from pathlib import Path
import json

_SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPT_DIR))

# Load tissue context
_TISSUE_CONTEXT_PATH = Path(__file__).resolve().parent.parent / "references" / "tissue_context.json"


def load_tissue_context():
    with open(_TISSUE_CONTEXT_PATH, "r") as f:
        return json.load(f)


def test_drug_metabolism_list_length():
    """drug_metabolism list should have 28 genes (18 original + 10 new, deduped)"""
    ctx = load_tissue_context()
    dm = ctx["profiles"]["general"]["special_gene_lists"]["drug_metabolism"]
    assert len(dm) == 28, f"Expected 28 drug metabolism genes, got {len(dm)}"
    print(f"[PASS] drug_metabolism list length = {len(dm)}")


def test_new_cyp_genes_present():
    """New CYP genes should be in the list"""
    ctx = load_tissue_context()
    dm = ctx["profiles"]["general"]["special_gene_lists"]["drug_metabolism"]
    new_genes = ["CYP2C8", "CYP3A7", "CYP4F2", "CYP2A6", "CYP2J2", "CYP2S1", "CYP3A43", "CYP4A11", "CYP4A22", "CYP17A1"]
    for gene in new_genes:
        assert gene in dm, f"Expected {gene} in drug_metabolism list"
    print(f"[PASS] All 10 new CYP genes present")


def test_cyp2d7_excluded():
    """CYP2D7 (pseudogene) should NOT be in the list"""
    ctx = load_tissue_context()
    dm = ctx["profiles"]["general"]["special_gene_lists"]["drug_metabolism"]
    assert "CYP2D7" not in dm, "CYP2D7 (pseudogene) should not be in drug_metabolism list"
    print("[PASS] CYP2D7 correctly excluded")


def test_existing_genes_preserved():
    """Original genes should still be present"""
    ctx = load_tissue_context()
    dm = ctx["profiles"]["general"]["special_gene_lists"]["drug_metabolism"]
    original = ["CYP2D6", "CYP2C19", "CYP3A4", "CYP3A5", "ABCB1", "TPMT", "DPYD", "UGT1A1", "NAT2", "G6PD", "VKORC1"]
    for gene in original:
        assert gene in dm, f"Original gene {gene} missing from list"
    print("[PASS] All original genes preserved")


def test_no_duplicates():
    """No gene should appear twice"""
    ctx = load_tissue_context()
    dm = ctx["profiles"]["general"]["special_gene_lists"]["drug_metabolism"]
    assert len(dm) == len(set(dm)), f"Duplicates found: {[g for g in dm if dm.count(g) > 1]}"
    print("[PASS] No duplicates in drug_metabolism list")


def test_all_cyp_genes():
    """Verify all expected CYP genes are present"""
    ctx = load_tissue_context()
    dm = ctx["profiles"]["general"]["special_gene_lists"]["drug_metabolism"]
    expected_cyp = [
        "CYP1A2", "CYP2A6", "CYP2B6", "CYP2C8", "CYP2C9", "CYP2C19",
        "CYP2D6", "CYP2E1", "CYP2J2", "CYP2S1", "CYP3A4", "CYP3A5",
        "CYP3A7", "CYP3A43", "CYP4A11", "CYP4A22", "CYP4F2", "CYP17A1",
    ]
    for gene in expected_cyp:
        assert gene in dm, f"Expected CYP gene {gene} missing"
    print(f"[PASS] All {len(expected_cyp)} expected CYP genes present")


def main():
    tests = [
        test_drug_metabolism_list_length,
        test_new_cyp_genes_present,
        test_cyp2d7_excluded,
        test_existing_genes_preserved,
        test_no_duplicates,
        test_all_cyp_genes,
    ]
    
    passed = 0
    failed = 0
    for t in tests:
        try:
            t()
            passed += 1
        except AssertionError as e:
            print(f"[FAIL] {t.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"[ERROR] {t.__name__}: {e}")
            failed += 1
    
    print(f"\n{'='*60}")
    print(f"P1 TESTS: {passed} passed, {failed} failed")
    print(f"{'='*60}")
    return failed == 0


if __name__ == "__main__":
    import sys
    sys.exit(0 if main() else 1)
