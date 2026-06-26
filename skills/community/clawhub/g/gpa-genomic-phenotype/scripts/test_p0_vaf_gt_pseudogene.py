#!/usr/bin/env python3
"""
P0 Tests — VAF-GT Consistency + Pseudogene Database (v0.5.3)

Run: python3 test_p0_vaf_gt_pseudogene.py
"""

import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPT_DIR))

from dgra_core import (
    Variant, DGRAConfig,
    _run_qc_checks,
    detect_pseudogene_artifact,
    _load_pseudogene_database,
    classify_variant_tier,
)


def test_vaf_gt_mismatch_heterozygous_low():
    """GT=0/1, VAF=0.13 (<0.20) → VAF_GT_MISMATCH"""
    v = Variant(chrom="chr1", pos=100, ref="A", alt="G", gene="TEST", transcript="NM_001", exon="E1/5", impact="HIGH", consequence="missense", hgvsp="p.Arg1Cys", hgvsc="c.1A>G", clinvar="VUS", gt="0/1", vaf=0.13, dp=50)
    qc = _run_qc_checks([v])
    assert "VAF_GT_MISMATCH" in v.qc_flags, f"Expected VAF_GT_MISMATCH for GT=0/1 VAF=0.13, got {v.qc_flags}"
    print("[PASS] Heterozygous low VAF → VAF_GT_MISMATCH")


def test_vaf_gt_mismatch_heterozygous_high():
    """GT=0/1, VAF=0.85 (>0.80) → VAF_GT_MISMATCH"""
    v = Variant(chrom="chr1", pos=101, ref="A", alt="G", gene="TEST", transcript="NM_001", exon="E1/5", impact="HIGH", consequence="missense", hgvsp="p.Arg1Cys", hgvsc="c.1A>G", clinvar="VUS", gt="0/1", vaf=0.85, dp=50)
    qc = _run_qc_checks([v])
    assert "VAF_GT_MISMATCH" in v.qc_flags, f"Expected VAF_GT_MISMATCH for GT=0/1 VAF=0.85, got {v.qc_flags}"
    print("[PASS] Heterozygous high VAF → VAF_GT_MISMATCH")


def test_vaf_gt_mismatch_homozygous():
    """GT=1/1, VAF=0.60 (<0.70) → VAF_GT_MISMATCH"""
    v = Variant(chrom="chr1", pos=102, ref="A", alt="G", gene="TEST", transcript="NM_001", exon="E1/5", impact="HIGH", consequence="missense", hgvsp="p.Arg1Cys", hgvsc="c.1A>G", clinvar="VUS", gt="1/1", vaf=0.60, dp=50)
    qc = _run_qc_checks([v])
    assert "VAF_GT_MISMATCH" in v.qc_flags, f"Expected VAF_GT_MISMATCH for GT=1/1 VAF=0.60, got {v.qc_flags}"
    print("[PASS] Homozygous low VAF → VAF_GT_MISMATCH")


def test_vaf_gt_mismatch_wildtype():
    """GT=0/0, VAF=0.15 (>0.10) → VAF_GT_MISMATCH"""
    v = Variant(chrom="chr1", pos=103, ref="A", alt="G", gene="TEST", transcript="NM_001", exon="E1/5", impact="HIGH", consequence="missense", hgvsp="p.Arg1Cys", hgvsc="c.1A>G", clinvar="VUS", gt="0/0", vaf=0.15, dp=50)
    qc = _run_qc_checks([v])
    assert "VAF_GT_MISMATCH" in v.qc_flags, f"Expected VAF_GT_MISMATCH for GT=0/0 VAF=0.15, got {v.qc_flags}"
    print("[PASS] Wildtype with VAF → VAF_GT_MISMATCH")


def test_vaf_gt_normal():
    """GT=0/1, VAF=0.50 → no flag"""
    v = Variant(chrom="chr1", pos=104, ref="A", alt="G", gene="TEST", transcript="NM_001", exon="E1/5", impact="HIGH", consequence="missense", hgvsp="p.Arg1Cys", hgvsc="c.1A>G", clinvar="VUS", gt="0/1", vaf=0.50, dp=50)
    qc = _run_qc_checks([v])
    assert "VAF_GT_MISMATCH" not in v.qc_flags, f"Unexpected VAF_GT_MISMATCH for GT=0/1 VAF=0.50, got {v.qc_flags}"
    print("[PASS] Normal heterozygous VAF → no flag")


def test_pseudogene_database_loaded():
    """JSON database loads correctly"""
    db = _load_pseudogene_database()
    assert "VWF" in db, "VWF not in pseudogene database"
    assert "GUSB" in db, "GUSB not in pseudogene database"
    assert db["VWF"]["detection_strategy"] == "vaf_mismatch"
    assert db["GUSB"]["detection_strategy"] == "sequence_homology"
    print(f"[PASS] Pseudogene database loaded: {len(db)} genes")


def test_pseudogene_interference_vwf():
    """VWF VAF=0.15 < interference threshold 0.20 → PSEUDOGENE_INTERFERENCE"""
    v = Variant(chrom="chr12", pos=6126538, ref="G", alt="A", gene="VWF", transcript="NM_000552", exon="E23/52", impact="HIGH", consequence="nonsense", hgvsp="p.Gln1311Ter", hgvsc="c.3931C>T", clinvar="Pathogenic", gt="0/1", vaf=0.15, dp=50)
    pg = detect_pseudogene_artifact(v)
    assert pg is not None, "Expected pseudogene warning for VWF VAF=0.15"
    assert pg["type"] == "PSEUDOGENE_INTERFERENCE", f"Expected PSEUDOGENE_INTERFERENCE, got {pg['type']}"
    assert "VWFP1" in pg["pseudogenes"]
    print("[PASS] VWF VAF=0.15 → PSEUDOGENE_INTERFERENCE")


def test_pseudogene_suspected_vwf():
    """VWF VAF=0.23 < suspected 0.25 but > interference 0.20 → PSEUDOGENE_SUSPECTED"""
    v = Variant(chrom="chr12", pos=6126538, ref="G", alt="A", gene="VWF", transcript="NM_000552", exon="E23/52", impact="HIGH", consequence="nonsense", hgvsp="p.Gln1311Ter", hgvsc="c.3931C>T", clinvar="Pathogenic", gt="0/1", vaf=0.23, dp=50)
    pg = detect_pseudogene_artifact(v)
    assert pg is not None, "Expected pseudogene warning for VWF VAF=0.23"
    assert pg["type"] == "PSEUDOGENE_SUSPECTED", f"Expected PSEUDOGENE_SUSPECTED, got {pg['type']}"
    print("[PASS] VWF VAF=0.23 → PSEUDOGENE_SUSPECTED")


def test_pseudogene_normal_vwf():
    """VWF VAF=0.48 → no pseudogene warning"""
    v = Variant(chrom="chr12", pos=6126538, ref="G", alt="A", gene="VWF", transcript="NM_000552", exon="E23/52", impact="HIGH", consequence="nonsense", hgvsp="p.Gln1311Ter", hgvsc="c.3931C>T", clinvar="Pathogenic", gt="0/1", vaf=0.48, dp=50)
    pg = detect_pseudogene_artifact(v)
    assert pg is None, f"Unexpected pseudogene warning for VWF VAF=0.48: {pg}"
    print("[PASS] VWF VAF=0.48 → no pseudogene warning")


def test_pseudogene_gusb_sequence_homology():
    """GUSB VAF=0.20 (outside 35-65%) → PSEUDOGENE_SUSPECTED via sequence_homology"""
    v = Variant(chrom="chr7", pos=100, ref="A", alt="G", gene="GUSB", transcript="NM_000181", exon="E1/12", impact="MODERATE", consequence="missense", hgvsp="p.Arg1Cys", hgvsc="c.1A>G", clinvar="VUS", gt="0/1", vaf=0.20, dp=50)
    pg = detect_pseudogene_artifact(v)
    assert pg is not None, "Expected pseudogene warning for GUSB VAF=0.20"
    assert pg["type"] == "PSEUDOGENE_SUSPECTED"
    assert "GUSBP1" in pg["pseudogenes"] or "GUSBP2" in pg["pseudogenes"]
    print("[PASS] GUSB VAF=0.20 → PSEUDOGENE_SUSPECTED (sequence_homology)")


def test_tier_confidence_downgrade_vaf_gt_mismatch():
    """VAF_GT_MISMATCH forces tier_confidence to LOW"""
    v = Variant(chrom="chr1", pos=100, ref="A", alt="G", gene="VWF", transcript="NM_000552", exon="E23/52", impact="HIGH", consequence="nonsense", hgvsp="p.Gln1311Ter", hgvsc="c.3931C>T", clinvar="Pathogenic", gt="0/1", vaf=0.15, dp=50)
    v.qc_flags = ["VAF_GT_MISMATCH"]
    
    domain_info = {"domain": "unknown"}
    tissue = {"relevance": "none", "fast_track": False}
    gnomad_info = {"status": "not_captured"}
    
    tier, reason, actions = classify_variant_tier(
        v, domain_info, tissue, gnomad_info,
        None, None, {"display_name": "test"}, DGRAConfig()
    )
    assert v.tier_confidence == "LOW", f"Expected LOW confidence with VAF_GT_MISMATCH, got {v.tier_confidence}"
    print("[PASS] VAF_GT_MISMATCH → tier_confidence=LOW")


def test_tier_confidence_downgrade_pseudogene_interference():
    """PSEUDOGENE_INTERFERENCE forces tier_confidence to LOW"""
    v = Variant(chrom="chr1", pos=100, ref="A", alt="G", gene="VWF", transcript="NM_000552", exon="E23/52", impact="HIGH", consequence="nonsense", hgvsp="p.Gln1311Ter", hgvsc="c.3931C>T", clinvar="Pathogenic", gt="0/1", vaf=0.15, dp=50)
    pw = {
        "type": "PSEUDOGENE_INTERFERENCE",
        "gene": "VWF",
        "pseudogenes": ["VWFP1"],
        "observed_vaf": 0.15,
    }
    
    domain_info = {"domain": "unknown"}
    tissue = {"relevance": "none", "fast_track": False}
    gnomad_info = {"status": "not_captured"}
    
    tier, reason, actions = classify_variant_tier(
        v, domain_info, tissue, gnomad_info,
        None, pw, {"display_name": "test"}, DGRAConfig()
    )
    assert v.tier_confidence == "LOW", f"Expected LOW confidence with PSEUDOGENE_INTERFERENCE, got {v.tier_confidence}"
    print("[PASS] PSEUDOGENE_INTERFERENCE → tier_confidence=LOW")


def main():
    tests = [
        test_vaf_gt_mismatch_heterozygous_low,
        test_vaf_gt_mismatch_heterozygous_high,
        test_vaf_gt_mismatch_homozygous,
        test_vaf_gt_mismatch_wildtype,
        test_vaf_gt_normal,
        test_pseudogene_database_loaded,
        test_pseudogene_interference_vwf,
        test_pseudogene_suspected_vwf,
        test_pseudogene_normal_vwf,
        test_pseudogene_gusb_sequence_homology,
        test_tier_confidence_downgrade_vaf_gt_mismatch,
        test_tier_confidence_downgrade_pseudogene_interference,
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
    print(f"P0 TESTS: {passed} passed, {failed} failed")
    print(f"{'='*60}")
    return failed == 0


if __name__ == "__main__":
    import sys
    sys.exit(0 if main() else 1)
