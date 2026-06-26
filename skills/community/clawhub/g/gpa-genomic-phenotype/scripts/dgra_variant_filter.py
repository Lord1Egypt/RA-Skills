#!/usr/bin/env python3
"""
dgra_variant_filter.py — Variant Pre-filtering Module (v0.7.1)

Clinical-oriented smart filtering to reduce noise before tier classification.
Reduces ~40K raw variants to ~500 clinically relevant candidates.

Usage:
    from dgra_variant_filter import filter_variants, FILTER_PRESETS
    filtered, stats = filter_variants(variants, preset="clinical", tissue_relevant_genes=genes)
"""

import sys
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional, Set

# Add script dir to path for gpa_i18n import
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from gpa_i18n import normalize_consequence

# =============================================================================
# Filter Presets
# =============================================================================

FILTER_PRESETS = {
    "strict": {
        "impacts": {"HIGH", "MODERATE"},
        "include_low_splice": False,
        "include_synonymous_tissue": False,
        "include_clinvar_conflicting": False,
    },
    "clinical": {
        "impacts": {"HIGH", "MODERATE"},
        "include_low_splice": True,
        "include_synonymous_tissue": True,
        "include_clinvar_conflicting": True,
    },
    "broad": {
        "impacts": {"HIGH", "MODERATE", "LOW"},
        "include_low_splice": True,
        "include_synonymous_tissue": True,
        "include_clinvar_conflicting": True,
    },
}

# Splice-related consequence keywords (LOW impact but clinically relevant)
SPLICE_LOW_KEYWORDS = {
    "splice_region_variant",
    "splice_polypyrimidine_tract_variant",
    "splice_donor_5th_base_variant",
    "splice_acceptor_variant",  # usually HIGH but included for safety
    "splice_donor_variant",     # usually HIGH
}


def _get_impact(variant: Dict[str, Any]) -> str:
    """Extract IMPACT from variant dict, normalize to uppercase."""
    impact = variant.get("IMPACT", "").strip().upper()
    return impact


def _get_consequence_terms(variant: Dict[str, Any]) -> Set[str]:
    """Extract and normalize consequence terms from variant dict."""
    cons = variant.get("Consequence", "").strip()
    if not cons:
        return set()
    terms = normalize_consequence(cons)
    return set(t.lower() for t in terms)


def _has_splice_consequence(terms: Set[str]) -> bool:
    """Check if any consequence term is splice-related."""
    return bool(terms & SPLICE_LOW_KEYWORDS)


def _is_synonymous_in_tissue_gene(variant: Dict[str, Any], tissue_genes: Optional[Set[str]]) -> bool:
    """Check if variant is synonymous AND in a tissue-relevant gene."""
    if not tissue_genes:
        return False
    terms = _get_consequence_terms(variant)
    if "synonymous_variant" not in terms:
        return False
    gene = variant.get("GENE", "").strip()
    return gene in tissue_genes


def _is_clinvar_conflicting(variant: Dict[str, Any]) -> bool:
    """Check if variant has ClinVar conflicting interpretation."""
    clinvar = variant.get("CLIN_SIG", "").strip()
    if not clinvar:
        return False
    clinvar_lower = clinvar.lower()
    if "conflicting" in clinvar_lower:
        return True
    # Same logic as _clinvar_is_conflicting in dgra_core.py
    pathogenic_keywords = ["pathogenic", "致病", "likely_pathogenic", "可能致病"]
    benign_or_vus_keywords = ["benign", "良性", "likely_benign", "可能良性", "vus", "意义不明", "uncertain"]
    has_pathogenic = any(kw in clinvar_lower for kw in pathogenic_keywords)
    has_benign_or_vus = any(kw in clinvar_lower for kw in benign_or_vus_keywords)
    if has_pathogenic and has_benign_or_vus:
        return True
    return False


# =============================================================================
# Main Filter Function
# =============================================================================

def filter_variants(
    variants: List[Dict[str, Any]],
    preset: str = "clinical",
    tissue_relevant_genes: Optional[Set[str]] = None,
) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """
    Filter variant list based on clinical relevance preset.

    Args:
        variants: List of variant dicts (raw, from parser/adapter)
        preset: One of "strict", "clinical", "broad"
        tissue_relevant_genes: Set of gene symbols considered relevant to tissue.
                               Used for synonymous_variant retention.

    Returns:
        (filtered_variants, stats_dict)
        stats_dict contains counts for reporting.
    """
    if preset not in FILTER_PRESETS:
        raise ValueError(f"Unknown preset '{preset}'. Valid: {list(FILTER_PRESETS.keys())}")

    config = FILTER_PRESETS[preset]
    allowed_impacts = config["impacts"]
    include_low_splice = config["include_low_splice"]
    include_synonymous_tissue = config["include_synonymous_tissue"]
    include_clinvar_conflicting = config["include_clinvar_conflicting"]

    filtered = []
    stats = {
        "input_count": len(variants),
        "output_count": 0,
        "by_impact": {"HIGH": 0, "MODERATE": 0, "LOW": 0, "MODIFIER": 0, "UNKNOWN": 0},
        "splice_retained": 0,
        "synonymous_tissue_retained": 0,
        "clinvar_conflicting_retained": 0,
        "excluded": 0,
        "excluded_by_impact": 0,
        "excluded_other": 0,
    }

    tissue_genes = tissue_relevant_genes or set()

    for v in variants:
        impact = _get_impact(v)
        terms = _get_consequence_terms(v)
        is_conflicting = _is_clinvar_conflicting(v)

        # Track input impact distribution
        impact_key = impact if impact in stats["by_impact"] else "UNKNOWN"
        stats["by_impact"][impact_key] += 1

        # Decision logic
        keep = False
        reason = ""

        if impact in allowed_impacts:
            keep = True
            reason = f"impact_{impact.lower()}"
        elif include_low_splice and _has_splice_consequence(terms):
            keep = True
            reason = "splice_region"
            stats["splice_retained"] += 1
        elif include_synonymous_tissue and _is_synonymous_in_tissue_gene(v, tissue_genes):
            keep = True
            reason = "synonymous_tissue"
            stats["synonymous_tissue_retained"] += 1
        elif include_clinvar_conflicting and is_conflicting:
            keep = True
            reason = "clinvar_conflict"
            stats["clinvar_conflicting_retained"] += 1

        if keep:
            # Add filtering metadata to variant for downstream reporting
            v["_filter_reason"] = reason
            v["_filter_preset"] = preset
            filtered.append(v)
        else:
            stats["excluded"] += 1
            if impact and impact not in allowed_impacts:
                stats["excluded_by_impact"] += 1
            else:
                stats["excluded_other"] += 1

    stats["output_count"] = len(filtered)
    return filtered, stats


def get_tissue_relevant_genes(tissue_profile: str, tissue_context_path: Optional[Path] = None) -> Set[str]:
    """
    Extract tissue-relevant gene symbols from tissue_context.json.
    Collects all genes from special_gene_lists in the specified profile.
    """
    if tissue_context_path is None:
        tissue_context_path = Path(__file__).resolve().parent.parent / "references" / "tissue_context.json"

    try:
        import json
        with open(tissue_context_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return set()

    profile = data.get("profiles", {}).get(tissue_profile)
    if not profile:
        return set()

    gene_lists = profile.get("special_gene_lists", {})
    genes = set()
    for gene_list in gene_lists.values():
        if isinstance(gene_list, list):
            genes.update(g.upper() for g in gene_list if isinstance(g, str))
    return genes


# =============================================================================
# CLI / Standalone test
# =============================================================================

if __name__ == "__main__":
    # Quick self-test
    test_variants = [
        {"CHROM": "1", "POS": "100", "REF": "A", "ALT": "G", "GENE": "BRCA1", "IMPACT": "HIGH", "Consequence": "stop_gained", "CLIN_SIG": ""},
        {"CHROM": "1", "POS": "200", "REF": "C", "ALT": "T", "GENE": "TP53", "IMPACT": "MODERATE", "Consequence": "missense_variant", "CLIN_SIG": ""},
        {"CHROM": "1", "POS": "300", "REF": "G", "ALT": "A", "GENE": "BRCA2", "IMPACT": "LOW", "Consequence": "synonymous_variant", "CLIN_SIG": ""},
        {"CHROM": "1", "POS": "400", "REF": "T", "ALT": "C", "GENE": "TTN", "IMPACT": "LOW", "Consequence": "splice_region_variant", "CLIN_SIG": ""},
        {"CHROM": "1", "POS": "500", "REF": "A", "ALT": "G", "GENE": "BRCA1", "IMPACT": "LOW", "Consequence": "synonymous_variant", "CLIN_SIG": ""},
        {"CHROM": "1", "POS": "600", "REF": "C", "ALT": "T", "GENE": "VWF", "IMPACT": "LOW", "Consequence": "synonymous_variant", "CLIN_SIG": "良性, 致病"},
        {"CHROM": "1", "POS": "700", "REF": "G", "ALT": "A", "GENE": "XYZ", "IMPACT": "MODIFIER", "Consequence": "intergenic_variant", "CLIN_SIG": ""},
    ]

    tissue_genes = {"BRCA1", "TP53", "BRCA2", "VWF"}

    for preset in ["strict", "clinical", "broad"]:
        filtered, stats = filter_variants(test_variants, preset=preset, tissue_relevant_genes=tissue_genes)
        print(f"\n=== {preset} ===")
        print(f"  Input: {stats['input_count']} → Output: {stats['output_count']} (excluded: {stats['excluded']})")
        print(f"  HIGH: {stats['by_impact']['HIGH']} | MODERATE: {stats['by_impact']['MODERATE']} | LOW: {stats['by_impact']['LOW']} | MODIFIER: {stats['by_impact']['MODIFIER']}")
        print(f"  splice_retained: {stats['splice_retained']} | synonymous_tissue: {stats['synonymous_tissue_retained']} | clinvar_conflict: {stats['clinvar_conflicting_retained']}")
        print(f"  Kept genes: {[v['GENE'] for v in filtered]}")
