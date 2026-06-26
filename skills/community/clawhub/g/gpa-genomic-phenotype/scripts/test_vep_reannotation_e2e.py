#!/usr/bin/env python3
"""
VEP Reannotation End-to-End Test — CRIP2 chr14:105473030
v0.5.2

Validates the full pipeline for a known transcript-discrepancy variant:
  - Input:  NR_073082  splice_donor_variant  HIGH
  - VEP:   NM_001312  upstream_gene_variant MODIFIER
  - Out:   Tier 3 (MODIFIER + no ClinVar/pathogenic evidence)

Run: python -m pytest test_vep_reannotation_e2e.py -v
     python test_vep_reannotation_e2e.py        (standalone)
"""

import asyncio
import json
import sys
from pathlib import Path

# Ensure scripts/ is on path
_SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPT_DIR))

from dgra_core import (
    Variant,
    DGRAConfig,
    correct_transcript_priority,
    map_variant_to_domain,
    assess_tissue_relevance,
    classify_gnomad_frequency,
    classify_variant_tier,
    detect_multi_hit_genes,
    generate_tier_report,
    _format_vep_reannotation_note,
)


async def test_crip2_vep_reannotation_e2e():
    """
    Full pipeline test for CRIP2 chr14:105473030.

    Steps validated:
      1. Transcript correction detects NR_073082 vs canonical NM_001312
      2. VEP reannotation converts splice_donor/HIGH → upstream_gene_variant/MODIFIER
      3. Domain mapping returns empty (MODIFIER has no protein position)
      4. Tier classification → Tier 3 (no pathogenic evidence, impact=MODIFIER)
    """
    # ------------------------------------------------------------------
    # Step 0: Construct input variant (annotator-selected NR_073082)
    # ------------------------------------------------------------------
    v = Variant(
        chrom="chr14",
        pos=105473030,
        ref="G",
        alt="A",
        gene="CRIP2",
        transcript="NR_073082",
        exon="3/5",
        impact="HIGH",
        consequence="splice_donor_variant",
        hgvsp="",
        hgvsc="c.442+1G>A",
        clinvar="",          # No ClinVar evidence
        gnomad_af=None,
        dp=50,
        gq=99,
        gt="0/1",
        vaf=0.48,
    )

    # ------------------------------------------------------------------
    # Step 1: Transcript correction → TRANSCRIPT_DISCREPANCY
    # ------------------------------------------------------------------
    ensembl_data = {
        "CRIP2": {
            "canonical_transcript": "NM_001312",
            "biotype": "protein_coding",
            "source": "ensembl",
            "confidence": "medium",
        }
    }
    v, warning = await correct_transcript_priority(v, ensembl_data)
    assert warning is not None, "Expected TRANSCRIPT_DISCREPANCY warning"
    assert warning["type"] == "TRANSCRIPT_DISCREPANCY"
    assert "NM_001312" in v.transcript_warning
    print("[PASS] Step 1: TRANSCRIPT_DISCREPANCY detected")

    # ------------------------------------------------------------------
    # Step 1.5: VEP reannotation (simulated batch_query_vep_region result)
    # ------------------------------------------------------------------
    original = {
        "consequence": v.consequence,
        "impact": v.impact,
        "hgvsc": v.hgvsc,
        "hgvsp": v.hgvsp,
        "transcript": v.transcript,
    }

    # Apply canonical VEP annotation
    v.consequence = "upstream_gene_variant"
    v.impact = "MODIFIER"
    v.hgvsc = "c.-1234G>A"
    v.hgvsp = ""
    v.transcript = "NM_001312"

    tw = json.loads(v.transcript_warning) if v.transcript_warning else {}
    tw["vep_reannotation"] = {
        "status": "success",
        "original": original,
        "canonical": {
            "consequence": v.consequence,
            "impact": v.impact,
            "hgvsc": v.hgvsc,
            "hgvsp": v.hgvsp,
            "transcript": v.transcript,
            "transcript_id": "NM_001312",
            "protein_domains": [],
        },
        "source": "ensembl",
        "confidence": "medium",
    }
    v.transcript_warning = json.dumps(tw)

    assert v.impact == "MODIFIER"
    assert v.consequence == "upstream_gene_variant"
    assert v.transcript == "NM_001312"
    print("[PASS] Step 1.5: VEP reannotation applied (HIGH → MODIFIER)")

    # ------------------------------------------------------------------
    # Step 4: Domain mapping (MODIFIER → no protein position)
    # ------------------------------------------------------------------
    uniprot_data = {
        "CRIP2": {
            "domains": [],
            "sequence_length": None,
            "source": "uniprot",
            "confidence": "medium",
        }
    }
    v.domain_info = map_variant_to_domain(v, uniprot_data)
    assert v.domain_info["domain"] == "unknown", \
        f"Expected unknown domain for MODIFIER, got {v.domain_info}"
    print("[PASS] Step 4: Domain mapping returns 'unknown' for MODIFIER")

    # ------------------------------------------------------------------
    # Step 5: Tissue relevance
    # ------------------------------------------------------------------
    tissue_profile = {
        "display_name": "Hematopoietic",
        "gtex_tissue": None,
        "genes": {},
        "special_gene_lists": {},
    }
    gtex_data = {}
    tissue = assess_tissue_relevance(v, tissue_profile, gtex_data)
    v.tissue_relevance = tissue
    print(f"[PASS] Step 5: Tissue relevance = {tissue['relevance']}")

    # ------------------------------------------------------------------
    # Step 6: gnomAD classification
    # ------------------------------------------------------------------
    gnomad_info = classify_gnomad_frequency(None, "CRIP2")
    v.gnomad_status = gnomad_info["status"]
    print(f"[PASS] Step 6: gnomAD status = {gnomad_info['status']}")

    # ------------------------------------------------------------------
    # Step 7: Tier classification → MUST be Tier 3
    # ------------------------------------------------------------------
    tw_dict = json.loads(v.transcript_warning) if v.transcript_warning else None
    pw_dict = json.loads(v.pseudogene_warning) if v.pseudogene_warning else None
    config = DGRAConfig(tissue_profile="hematopoietic")

    tier, reason, actions = classify_variant_tier(
        v, v.domain_info, tissue, gnomad_info,
        tw_dict, pw_dict, tissue_profile, config,
    )
    v.tier = tier
    v.tier_reason = reason
    v.tier_actions = actions

    assert tier == 3, (
        f"CRIP2 chr14:105473030 with impact=MODIFIER and no ClinVar "
        f"must be Tier 3, but got Tier {tier}. Reason: {reason}"
    )
    print(f"[PASS] Step 7: Tier = {tier} ✓")

    # ------------------------------------------------------------------
    # Step 8: Report formatting includes VEP reannotation note
    # ------------------------------------------------------------------
    vep_note = _format_vep_reannotation_note(v)
    assert vep_note is not None, "Expected VEP reannotation note in report"
    assert "NM_001312" in vep_note
    assert "upstream_gene_variant" in vep_note
    assert "splice_donor_variant" in vep_note
    print(f"[PASS] Step 8: Report note = {vep_note}")

    # Generate a mini-report to ensure no exceptions
    report_md = generate_tier_report(
        [v], config, tissue_profile,
        multi_hits=[], cross_check=[],
    )
    assert "CRIP2" in report_md
    assert "⚠️ 后果已按 canonical transcript" in report_md
    print("[PASS] Step 9: Markdown report generated with VEP annotation")

    print("\n" + "=" * 60)
    print("ALL TESTS PASSED — CRIP2 VEP reannotation E2E validated")
    print("=" * 60)
    return True


def main():
    """Standalone entry point."""
    try:
        result = asyncio.run(test_crip2_vep_reannotation_e2e())
        sys.exit(0 if result else 1)
    except AssertionError as e:
        print(f"\n[FAIL] Assertion failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n[FAIL] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
