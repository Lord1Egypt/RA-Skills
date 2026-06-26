#!/usr/bin/env python3
"""
gpa_i18n.py — GPA Internationalization / Normalization Module (v0.7.1)

Centralized bilingual (Chinese/English) consequence normalization.
Used by adapters, filters, and downstream analysis modules.
"""

from typing import List

# =============================================================================
# Consequence Term Mapping: Chinese VEP/SnpEff/ANNOVAR → English SO terms
# =============================================================================

CONSEQUENCE_MAP = {
    # High impact
    "移码变异": "frameshift_variant",
    "获得终止密码子": "stop_gained",
    "失去终止密码子": "stop_lost",
    "起始密码子缺失": "start_lost",
    "剪接受体位点变异": "splice_acceptor_variant",
    "剪接供体位点变异": "splice_donor_variant",
    "剪接位点变异": "splice_variant",
    "转录本缺失": "transcript_ablation",
    "转录本扩增": "transcript_amplification",
    # Moderate impact
    "错义变异": "missense_variant",
    "框内插入": "inframe_insertion",
    "框内缺失": "inframe_deletion",
    "蛋白质改变变异": "protein_altering_variant",
    "剪接区域变异": "splice_region_variant",
    "剪接区变异": "splice_region_variant",
    "剪接多聚嘧啶束变异": "splice_polypyrimidine_tract_variant",
    "剪接供体第5碱基变异": "splice_donor_5th_base_variant",
    "起始密码子保留变异": "start_retained_variant",
    "终止密码子保留变异": "stop_retained_variant",
    "不完全末端密码子变异": "incomplete_terminal_codon_variant",
    # Low impact
    "同义变异": "synonymous_variant",
    "5'UTR变异": "5_prime_UTR_variant",
    "3'UTR变异": "3_prime_UTR_variant",
    "内含子变异": "intron_variant",
    "上游基因变异": "upstream_gene_variant",
    "下游基因变异": "downstream_gene_variant",
    "非编码转录本外显子变异": "non_coding_transcript_exon_variant",
    "编码序列变异": "coding_sequence_variant",
    "成熟miRNA变异": "mature_miRNA_variant",
    "NMD转录本变异": "NMD_transcript_variant",
    "非编码转录本变异": "non_coding_transcript_variant",
    # Modifier
    "基因间变异": "intergenic_variant",
    "调控区域变异": "regulatory_region_variant",
    "TFBS缺失": "TFBS_ablation",
    "TFBS扩增": "TFBS_amplification",
    "TF结合位点变异": "TF_binding_site_variant",
    "调控区域缺失": "regulatory_region_ablation",
    "调控区域扩增": "regulatory_region_amplification",
    "特征延伸": "feature_elongation",
    "特征截短": "feature_truncation",
}


# =============================================================================
# Normalization Functions
# =============================================================================

def normalize_consequence(cons_str: str) -> List[str]:
    """
    Normalize a mixed Chinese/English consequence string into English SO terms.

    Input:  "错义变异,剪接区域变异"  or  "missense_variant,splice_region_variant"
    Output: ["missense_variant", "splice_region_variant"]
    """
    if not cons_str or cons_str.strip() in ("", ".", "UNKNOWN", "N/A"):
        return []

    # Split by common delimiters (VEP uses ',', some tools use '&' or ';')
    raw_terms = [t.strip() for t in cons_str.replace("&", ",").replace(";", ",").split(",")]

    normalized = []
    for t in raw_terms:
        if not t:
            continue
        # Direct Chinese → English mapping
        if t in CONSEQUENCE_MAP:
            normalized.append(CONSEQUENCE_MAP[t])
        else:
            # Already English or unknown — pass through as-is
            normalized.append(t)
    return normalized


def infer_impact_from_consequence(cons_str: str) -> str:
    """
    Unified IMPACT inference from consequence string.
    Supports both Chinese and English input.

    Returns: "HIGH" | "MODERATE" | "LOW" | "MODIFIER" | "" (unknown)
    """
    if not cons_str or cons_str.strip() in ("", ".", "UNKNOWN", "N/A"):
        return ""  # core.py maps empty → UNKNOWN → conservative HIGH

    # Normalize to English SO terms first
    terms = normalize_consequence(cons_str)
    if not terms:
        return ""

    # Combine all terms into a single lowercase string for matching
    cons_combined = ",".join(terms).lower()

    # HIGH impact consequences
    high_keywords = {
        "stop_gained", "stop_lost", "frameshift_variant", "splice_acceptor_variant",
        "splice_donor_variant", "start_lost", "transcript_ablation", "transcript_amplification",
        "splice_variant",
    }
    # MODERATE impact consequences
    moderate_keywords = {
        "missense_variant", "inframe_deletion", "inframe_insertion",
        "protein_altering_variant", "splice_region_variant",
        "splice_polypyrimidine_tract_variant", "splice_donor_5th_base_variant",
        "incomplete_terminal_codon_variant", "stop_retained_variant", "start_retained_variant",
    }
    # LOW impact consequences
    low_keywords = {
        "synonymous_variant", "5_prime_utr_variant", "3_prime_utr_variant",
        "intron_variant", "upstream_gene_variant", "downstream_gene_variant",
        "non_coding_transcript_exon_variant", "coding_sequence_variant",
        "mature_mirna_variant", "nmd_transcript_variant", "non_coding_transcript_variant",
    }

    if any(h in cons_combined for h in high_keywords):
        return "HIGH"
    if any(m in cons_combined for m in moderate_keywords):
        return "MODERATE"
    if any(l in cons_combined for l in low_keywords):
        return "LOW"

    # Everything else → MODIFIER (or pass through as unknown for conservative handling)
    return "MODIFIER"


# =============================================================================
# ClinVar text normalization (for downstream matching)
# =============================================================================

def normalize_clinvar(clinvar_str: str) -> str:
    """
    Normalize ClinVar text: standardize delimiters, strip extra whitespace.
    Does NOT change semantic meaning — purely formatting.
    """
    if not clinvar_str:
        return ""
    # Replace & with / (VEP style)
    normalized = clinvar_str.replace("_", " ").replace("&", "/")
    return normalized.strip()
