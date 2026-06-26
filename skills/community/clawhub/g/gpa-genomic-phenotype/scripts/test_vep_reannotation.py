#!/usr/bin/env python3
"""
Test: VEP batch response parsing for DGRA TRANSCRIPT_DISCREPANCY fix (Scheme B).

Verifies that DGRAAPIClient._parse_vep_batch_response correctly extracts
canonical transcript data (consequence, impact, HGVSc, HGVSp, protein domains)
from Ensembl VEP JSON responses.
"""

import json
import sys
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from dgra_api import DGRAAPIClient


def _make_mock_vep_response() -> list:
    """Return a realistic Ensembl VEP JSON response for 2 variants."""
    return [
        {
            "input": "17 41234451 . A G . . .",
            "seq_region_name": "17",
            "start": 41234451,
            "allele_string": "A/G",
            "most_severe_consequence": "missense_variant",
            "transcript_consequences": [
                {
                    "transcript_id": "ENST00000357654",
                    "gene_symbol": "BRCA1",
                    "gene_id": "ENSG00000012048",
                    "canonical": 1,
                    "biotype": "protein_coding",
                    "consequence_terms": ["missense_variant", "splice_region_variant"],
                    "impact": "MODERATE",
                    "hgvsc": "c.100A>G",
                    "hgvsp": "p.Thr34Ala",
                    "protein_domains": [
                        "Interpro:IPR001356:Zinc finger, PHD-type",
                        "Pfam:PF00628:PHD"
                    ],
                    "mane_select": "NM_007294.3"
                },
                {
                    "transcript_id": "ENST00000471181",
                    "gene_symbol": "BRCA1",
                    "gene_id": "ENSG00000012048",
                    "biotype": "protein_coding",
                    "consequence_terms": ["intron_variant"],
                    "impact": "LOW",
                    "protein_domains": []
                }
            ]
        },
        {
            "input": "1 123456 . C T . . .",
            "seq_region_name": "1",
            "start": 123456,
            "allele_string": "C/T",
            "most_severe_consequence": "stop_gained",
            "transcript_consequences": [
                {
                    "transcript_id": "ENST00000380152",
                    "gene_symbol": "GENE1",
                    "gene_id": "ENSG00000123456",
                    "canonical": 1,
                    "biotype": "protein_coding",
                    "consequence_terms": ["stop_gained", "nonsense_mediating_decay"],
                    "impact": "HIGH",
                    "hgvsc": "c.500C>T",
                    "hgvsp": "p.Arg167Ter",
                    "protein_domains": [
                        {"name": "Kinase domain", "start": 100, "end": 300, "db": "Pfam"}
                    ]
                }
            ]
        },
        {
            "input": "1 999999 . G A . . .",
            "seq_region_name": "1",
            "start": 999999,
            "allele_string": "G/A",
            "transcript_consequences": []
        }
    ]


def test_parse_vep_batch_response():
    """Test canonical transcript extraction from VEP batch response."""
    client = DGRAAPIClient.__new__(DGRAAPIClient)
    mock_data = _make_mock_vep_response()
    variants = [
        {"chrom": "17", "pos": 41234451, "ref": "A", "alt": "G"},
        {"chrom": "1", "pos": 123456, "ref": "C", "alt": "T"},
        {"chrom": "1", "pos": 999999, "ref": "G", "alt": "A"},
    ]
    results = client._parse_vep_batch_response(mock_data, variants)

    assert len(results) == 3, f"Expected 3 results, got {len(results)}"

    # Variant 1: BRCA1 missense — canonical=1 selected
    r1 = results[0]
    assert r1["transcript_id"] == "ENST00000357654", f"Expected ENST00000357654, got {r1['transcript_id']}"
    assert r1["impact"] == "MODERATE", f"Expected MODERATE, got {r1['impact']}"
    assert r1["hgvsc"] == "c.100A>G", f"Expected c.100A>G, got {r1['hgvsc']}"
    assert r1["hgvsp"] == "p.Thr34Ala", f"Expected p.Thr34Ala, got {r1['hgvsp']}"
    assert r1["consequence_terms"] == ["missense_variant", "splice_region_variant"]
    assert len(r1["protein_domains"]) == 2
    assert r1["protein_domains"][0]["name"] == "Zinc finger, PHD-type"
    assert r1["protein_domains"][0]["db"] == "Interpro"
    assert r1["protein_domains"][0]["interpro_id"] == "IPR001356"
    assert r1["protein_domains"][1]["name"] == "PHD"
    assert r1["protein_domains"][1]["db"] == "Pfam"
    print("  Variant 1 (BRCA1 missense): PASSED")

    # Variant 2: stop_gained — canonical=1 selected, dict-style protein_domains
    r2 = results[1]
    assert r2["transcript_id"] == "ENST00000380152"
    assert r2["impact"] == "HIGH"
    assert r2["hgvsc"] == "c.500C>T"
    assert r2["hgvsp"] == "p.Arg167Ter"
    assert r2["consequence_terms"] == ["stop_gained", "nonsense_mediating_decay"]
    assert len(r2["protein_domains"]) == 1
    assert r2["protein_domains"][0]["name"] == "Kinase domain"
    assert r2["protein_domains"][0]["db"] == "Pfam"
    assert r2["protein_domains"][0]["start"] == 100
    assert r2["protein_domains"][0]["end"] == 300
    print("  Variant 2 (stop_gained, dict domains): PASSED")

    # Variant 3: no transcript consequences — error entry
    r3 = results[2]
    assert "error" in r3, f"Expected error entry, got {r3}"
    assert r3.get("error") == "No transcript consequences found"
    print("  Variant 3 (no consequences): PASSED")

    print("test_parse_vep_batch_response: ALL PASSED")


def test_mane_select_fallback():
    """Test MANE Select fallback when no canonical=1 flag."""
    client = DGRAAPIClient.__new__(DGRAAPIClient)
    mock_data = [
        {
            "transcript_consequences": [
                {
                    "transcript_id": "ENST00000471181",
                    "biotype": "protein_coding",
                    "consequence_terms": ["intron_variant"],
                    "impact": "LOW",
                },
                {
                    "transcript_id": "ENST00000357654",
                    "biotype": "protein_coding",
                    "consequence_terms": ["missense_variant"],
                    "impact": "MODERATE",
                    "mane_select": "NM_007294.3",
                }
            ]
        }
    ]
    variants = [{"chrom": "17", "pos": 41234451, "ref": "A", "alt": "G"}]
    results = client._parse_vep_batch_response(mock_data, variants)
    assert results[0]["transcript_id"] == "ENST00000357654"
    assert results[0]["impact"] == "MODERATE"
    print("test_mane_select_fallback: PASSED")


def test_protein_coding_fallback():
    """Test protein_coding fallback when no canonical or MANE."""
    client = DGRAAPIClient.__new__(DGRAAPIClient)
    mock_data = [
        {
            "transcript_consequences": [
                {
                    "transcript_id": "ENST00000586383",
                    "biotype": "retained_intron",
                    "consequence_terms": ["intron_variant"],
                    "impact": "LOW",
                },
                {
                    "transcript_id": "ENST00000357654",
                    "biotype": "protein_coding",
                    "consequence_terms": ["missense_variant"],
                    "impact": "MODERATE",
                }
            ]
        }
    ]
    variants = [{"chrom": "17", "pos": 41234451, "ref": "A", "alt": "G"}]
    results = client._parse_vep_batch_response(mock_data, variants)
    assert results[0]["transcript_id"] == "ENST00000357654"
    assert results[0]["impact"] == "MODERATE"
    print("test_protein_coding_fallback: PASSED")


if __name__ == "__main__":
    test_parse_vep_batch_response()
    test_mane_select_fallback()
    test_protein_coding_fallback()
    print("\nAll VEP parsing tests passed.")
