#!/usr/bin/env python3
"""
DGRA Annotation Adapters — v0.5 P0-2
Normalize variant dicts from VEP / ANNOVAR / SnpEff into dgra internal format.

Each adapter receives a raw row dict (key=column name, value=cell content)
and returns a normalized dict with keys matching dgra_core REQUIRED_COLS.

用法:
    from dgra_adapters import auto_detect_adapter, VEPAdapter, ANNOVARAdapter, SnpEffAdapter
    adapter = auto_detect_adapter(["Chr", "Start", "End", "Ref", "Alt", "Gene.refGene"])
    norm = adapter.adapt(raw_row)
"""

import re
from typing import List, Dict, Any, Optional

# =============================================================================
# DGRA canonical column set (must match dgra_core.py REQUIRED_COLS)
# =============================================================================

DGRA_COLS = [
    "CHROM", "POS", "REF", "ALT", "GENE", "Feature", "EXON",
    "IMPACT", "Consequence", "HGVSp", "HGVSc", "CLIN_SIG",
    "GT", "DP", "GQ", "VAF", "gnomAD_AF",
]

# =============================================================================
# Base Adapter
# =============================================================================

class AnnotationAdapter:
    """Base class for annotation format adapters."""

    def adapt(self, row: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize a raw annotation row to dgra canonical format."""
        raise NotImplementedError

    @classmethod
    def supports_headers(cls, headers: List[str]) -> bool:
        """Return True if these column headers indicate this format."""
        raise NotImplementedError


# =============================================================================
# VEP Adapter
# =============================================================================

class VEPAdapter(AnnotationAdapter):
    """
    VEP (Variant Effect Predictor) output adapter.

    VEP columns are already close to dgra canonical. Main tasks:
      - Strip '#Uploaded_variation' to get CHROM/POS or map Existing_variation
      - Normalize CLIN_SIG delimiters (VEP uses '&' e.g. "Pathogenic&Likely_pathogenic")
      - Ensure HGVSp uses 'p.' prefix
    """

    # Direct pass-through mapping (VEP name → dgra name)
    VEP_TO_DGRA = {
        "#CHROM": "CHROM", "CHROM": "CHROM", "chr": "CHROM",
        "POS": "POS", "Position": "POS", "START": "POS",
        "REF": "REF", "Allele": "ALT", "ALT": "ALT",
        "SYMBOL": "GENE", "Gene": "GENE", "GENE": "GENE",
        "Feature": "Feature", "Transcript": "Feature",
        "EXON": "EXON",
        "IMPACT": "IMPACT",
        "Consequence": "Consequence",
        "HGVSp": "HGVSp", "HGVSp_Short": "HGVSp",
        "HGVSc": "HGVSc", "HGVSc_Short": "HGVSc",
        "CLIN_SIG": "CLIN_SIG",
        "GT": "GT", "gts": "GT",
        "DP": "DP", "AvgDepth": "DP",
        "GQ": "GQ", "Quality": "GQ",
        "VAF": "VAF", "AF": "VAF",
        "gnomAD_AF": "gnomAD_AF", "gnomADe_AF": "gnomAD_AF",
    }

    @classmethod
    def supports_headers(cls, headers: List[str]) -> bool:
        score = 0
        hset = {h.strip().lstrip("#") for h in headers}
        for vep_col in ("Consequence", "IMPACT", "HGVSp", "HGVSc", "CLIN_SIG", "SYMBOL", "Feature"):
            if vep_col in hset:
                score += 1
        return score >= 3

    def adapt(self, row: Dict[str, Any]) -> Dict[str, Any]:
        out: Dict[str, Any] = {}
        # Direct mapping
        for k, v in row.items():
            clean_k = k.strip().lstrip("#")
            dgra_name = self.VEP_TO_DGRA.get(clean_k, clean_k)
            out[dgra_name] = str(v) if v is not None else ""

        # Handle #Uploaded_variation → CHROM/POS if missing
        if not out.get("CHROM") and "#Uploaded_variation" in row:
            uv = str(row["#Uploaded_variation"])
            chrom_pos = self._parse_uploaded_variation(uv)
            if chrom_pos:
                out["CHROM"], out["POS"] = chrom_pos

        # Normalize CLIN_SIG delimiters
        if out.get("CLIN_SIG"):
            cs = out["CLIN_SIG"]
            cs = cs.replace("_", " ").replace("&", "/")
            out["CLIN_SIG"] = cs

        # Ensure HGVSp has p. prefix
        if out.get("HGVSp") and not out["HGVSp"].startswith("p."):
            out["HGVSp"] = "p." + out["HGVSp"]

        # Fill missing dgra columns with empty string (core.py → UNKNOWN)
        for col in DGRA_COLS:
            if col not in out:
                out[col] = ""
        return out

    @staticmethod
    def _parse_uploaded_variation(uv: str) -> Optional[tuple]:
        """Parse '1_12345_A/G' or '1-12345-A-G' or rsID."""
        # 1_12345_A/G
        m = re.match(r"^([0-9XYM]+)[_\-]([0-9]+)[_\-]([ACGT]+)[/_]([ACGT]+)$", uv, re.I)
        if m:
            return m.group(1), m.group(2)
        # rsID — can't extract coordinate
        if uv.startswith("rs"):
            return None
        return None


# =============================================================================
# ANNOVAR Adapter
# =============================================================================

class ANNOVARAdapter(AnnotationAdapter):
    """
    ANNOVAR output adapter.

    ANNOVAR columns differ significantly from VEP. Key mappings:
      - Chr → CHROM, Start → POS, End → (ignored), Ref → REF, Alt → ALT
      - Gene.refGene → GENE
      - AAChange.refGene → parse HGVSc + HGVSp
      - ExonicFunc.refGene → Consequence
      - Func.refGene → broader function category

    AAChange.refGene format:
      "NM_001:exon5:c.123A>G:p.Arg41Cys"
      Multiple transcripts separated by ','.
    """

    # Header → dgra mapping
    ANNOVAR_TO_DGRA = {
        "Chr": "CHROM", "CHROM": "CHROM",
        "Start": "POS", "POS": "POS",
        "End": "_end",
        "Ref": "REF", "REF": "REF",
        "Alt": "ALT", "ALT": "ALT",
        "Gene.refGene": "GENE", "Gene": "GENE",
        "GeneDetail.refGene": "_gene_detail",
        "ExonicFunc.refGene": "_exonic_func",
        "Func.refGene": "_func",
        "AAChange.refGene": "_aachange",
    }

    # ExonicFunc → Consequence mapping
    EXONIC_FUNC_MAP = {
        "frameshift substitution": "frameshift_variant",
        "frameshift deletion": "frameshift_variant",
        "frameshift insertion": "frameshift_variant",
        "nonframeshift substitution": "inframe_variant",
        "nonframeshift deletion": "inframe_deletion",
        "nonframeshift insertion": "inframe_insertion",
        "nonsynonymous snv": "missense_variant",
        "synonymous snv": "synonymous_variant",
        "stopgain": "stop_gained",
        "stoploss": "stop_lost",
        "unknown": "",
    }

    @classmethod
    def supports_headers(cls, headers: List[str]) -> bool:
        score = 0
        hset = {h.strip() for h in headers}
        annovar_markers = ("Chr", "Start", "End", "Ref", "Alt",
                           "Gene.refGene", "AAChange.refGene",
                           "ExonicFunc.refGene", "Func.refGene")
        for m in annovar_markers:
            if m in hset:
                score += 1
        return score >= 3

    def adapt(self, row: Dict[str, Any]) -> Dict[str, Any]:
        out: Dict[str, Any] = {}

        # Direct column mapping
        for k, v in row.items():
            clean_k = k.strip()
            dgra_name = self.ANNOVAR_TO_DGRA.get(clean_k, clean_k)
            out[dgra_name] = str(v) if v is not None else ""

        # Parse AAChange.refGene → HGVSc + HGVSp
        aa_raw = out.pop("_aachange", "")
        if aa_raw:
            hgvsc, hgvsp = self._parse_aachange(aa_raw)
            out["HGVSc"] = hgvsc
            out["HGVSp"] = hgvsp

        # ExonicFunc → Consequence
        exonic_func = out.pop("_exonic_func", "")
        if exonic_func:
            # v0.8.0 P2: Support Chinese exonic function terms
            consequence = self.EXONIC_FUNC_MAP.get(exonic_func.lower())
            if not consequence:
                consequence = self.CN_EXONIC_FUNC_MAP.get(exonic_func.strip())
            if not consequence:
                consequence = exonic_func
            out["Consequence"] = consequence

        # Func.refGene → broad consequence fallback
        func = out.pop("_func", "")
        if func and not out.get("Consequence"):
            func_map = {
                "exonic": "coding_sequence_variant",
                "splicing": "splice_region_variant",
                "ncRNA_exonic": "non_coding_transcript_exon_variant",
                "UTR3": "3_prime_UTR_variant",
                "UTR5": "5_prime_UTR_variant",
                "intronic": "intron_variant",
                "upstream": "upstream_gene_variant",
                "downstream": "downstream_gene_variant",
                "intergenic": "intergenic_variant",
            }
            out["Consequence"] = func_map.get(func, func)

        # IMPACT inference from consequence
        if not out.get("IMPACT") and out.get("Consequence"):
            out["IMPACT"] = self._infer_impact(out["Consequence"])

        # Fill missing dgra columns
        for col in DGRA_COLS:
            if col not in out:
                out[col] = ""
        return out

    @staticmethod
    def _parse_aachange(aa_raw: str) -> tuple:
        """
        Parse AAChange.refGene.
        Format: "NM_001:exon5:c.123A>G:p.Arg41Cys" or multiple separated by ','.
        Returns (hgvsc, hgvsp) from first transcript.
        """
        if not aa_raw or aa_raw == ".":
            return "", ""
        # Take first transcript
        first = aa_raw.split(",")[0].strip()
        parts = first.split(":")
        hgvsc = ""
        hgvsp = ""
        for p in parts:
            p = p.strip()
            if p.startswith("c."):
                hgvsc = p
            elif p.startswith("p."):
                hgvsp = p
        return hgvsc, hgvsp

    @staticmethod
    def _infer_impact(consequence: str) -> str:
        """Infer IMPACT from Consequence string (best-effort).
        v0.7.1: Delegates to gpa_i18n for unified Chinese/English support."""
        from gpa_i18n import infer_impact_from_consequence
        return infer_impact_from_consequence(consequence)

    # v0.8.0 P2: Add Chinese terms to EXONIC_FUNC_MAP for direct lookup
    CN_EXONIC_FUNC_MAP = {
        "移码变异": "frameshift_variant",
        "错义变异": "missense_variant",
        "非移码缺失": "inframe_deletion",
        "非移码插入": "inframe_insertion",
        "无义变异": "stop_gained",
        "终止密码子获得": "stop_gained",
        "剪接位点变异": "splice_variant",
        "剪接受体位点变异": "splice_acceptor_variant",
        "剪接供体位点变异": "splice_donor_variant",
        "剪接区域变异": "splice_region_variant",
        "同义变异": "synonymous_variant",
        "未知": "unknown",
    }


# =============================================================================
# SnpEff Adapter
# =============================================================================

class SnpEffAdapter(AnnotationAdapter):
    """
    SnpEff output adapter.

    SnpEff typically outputs ANN field in VCF INFO or TSV columns:
      ANN = "missense_variant|MODERATE|exon|GENE|transcript|...|c.123A>G|p.Arg41Cys|..."
    Multiple effects are separated by ','.

    For TSV output, SnpEff may have columns like:
      "ANN[0].GENE", "ANN[0].EFFECT", "ANN[0].IMPACT", "ANN[0].HGVS_C", "ANN[0].HGVS_P"
    We pick ANN[0] (first effect, usually most severe by SnpEff's own ranking).
    """

    SnpEff_ANN_ORDER = [
        "transcript_ablation", "splice_acceptor_variant", "splice_donor_variant",
        "stop_gained", "frameshift_variant", "stop_lost", "start_lost",
        "transcript_amplification", "inframe_insertion", "inframe_deletion",
        "missense_variant", "protein_altering_variant", "splice_region_variant",
        "incomplete_terminal_codon_variant", "stop_retained_variant",
        "synonymous_variant", "coding_sequence_variant", "mature_miRNA_variant",
        "5_prime_UTR_variant", "3_prime_UTR_variant", "non_coding_transcript_exon_variant",
        "intron_variant", "NMD_transcript_variant", "non_coding_transcript_variant",
        "upstream_gene_variant", "downstream_gene_variant", "TFBS_ablation",
        "TFBS_amplification", "TF_binding_site_variant", "regulatory_region_ablation",
        "regulatory_region_amplification", "feature_elongation", "regulatory_region_variant",
        "feature_truncation", "intergenic_variant",
    ]

    @classmethod
    def supports_headers(cls, headers: List[str]) -> bool:
        score = 0
        hset = {h.strip() for h in headers}
        for m in ("ANN[0].EFFECT", "ANN[0].IMPACT", "ANN[0].GENE", "ANN[0].HGVS_C", "ANN[0].HGVS_P"):
            if m in hset:
                score += 1
        # Also detect raw ANN column in VCF-derived TSV
        if "ANN" in hset:
            score += 1
        return score >= 2

    def adapt(self, row: Dict[str, Any]) -> Dict[str, Any]:
        out: Dict[str, Any] = {}

        # Try structured ANN[0] columns first
        gene = row.get("ANN[0].GENE", "") or row.get("Gene_Name", "")
        impact = row.get("ANN[0].IMPACT", "") or row.get("Putative_impact", "")
        consequence = row.get("ANN[0].EFFECT", "") or row.get("Effect", "")
        hgvsc = row.get("ANN[0].HGVS_C", "") or row.get("HGVS.c", "")
        hgvsp = row.get("ANN[0].HGVS_P", "") or row.get("HGVS.p", "")
        transcript = row.get("ANN[0].FEATUREID", "") or row.get("Transcript_ID", "")
        exon = row.get("ANN[0].RANK", "") or ""

        # Fallback: raw ANN field
        if not any((gene, impact, consequence)) and "ANN" in row:
            ann = str(row["ANN"])
            gene, transcript, exon, impact, consequence, hgvsc, hgvsp = self._parse_ann(ann)

        # Basic coordinate columns
        out["CHROM"] = str(row.get("CHROM", row.get("#CHROM", row.get("Chrom", ""))))
        out["POS"] = str(row.get("POS", row.get("Position", row.get("Start", ""))))
        out["REF"] = str(row.get("REF", row.get("Ref", "")))
        out["ALT"] = str(row.get("ALT", row.get("Alt", "")))
        out["GENE"] = str(gene) if gene else ""
        out["Feature"] = str(transcript) if transcript else ""
        out["EXON"] = str(exon) if exon else ""
        out["IMPACT"] = str(impact) if impact else ""
        out["Consequence"] = str(consequence) if consequence else ""
        out["HGVSc"] = str(hgvsc) if hgvsc else ""
        out["HGVSp"] = str(hgvsp) if hgvsp else ""
        out["CLIN_SIG"] = str(row.get("CLIN_SIG", ""))
        out["GT"] = str(row.get("GT", ""))
        out["DP"] = str(row.get("DP", ""))
        out["GQ"] = str(row.get("GQ", ""))
        out["VAF"] = str(row.get("VAF", ""))
        out["gnomAD_AF"] = str(row.get("gnomAD_AF", ""))

        # Fill missing
        for col in DGRA_COLS:
            if col not in out:
                out[col] = ""
        return out

    def _parse_ann(self, ann_raw: str) -> tuple:
        """
        Parse SnpEff ANN field.
        SnpEff ANN can have two formats:
          A) allele|effect|impact|gene|... (older/pre-VCF format)
          B) effect|impact|gene|...         (VCF INFO/ANN, allele implicit from ALT)
        We detect by checking if parts[1] is a known impact word.
        """
        if not ann_raw:
            return "", "", "", "", "", "", ""
        first_effect = ann_raw.split(",")[0]
        parts = first_effect.split("|")
        if len(parts) < 2:
            return "", "", "", "", "", "", ""

        known_impacts = {"HIGH", "MODERATE", "LOW", "MODIFIER"}
        if parts[1] in known_impacts:
            # Format B: effect|impact|gene|gene_id|feature_type|feature_id|biotype|rank|hgvs_c|hgvs_p|...
            gene = parts[2] if len(parts) > 2 else ""
            transcript = parts[5] if len(parts) > 5 else ""
            exon = parts[7] if len(parts) > 7 else ""
            impact = parts[1]
            consequence = parts[0]
            hgvsc = parts[8] if len(parts) > 8 else ""
            hgvsp = parts[9] if len(parts) > 9 else ""
        else:
            # Format A: allele|effect|impact|gene|gene_id|feature_type|feature_id|biotype|rank|hgvs_c|hgvs_p|...
            gene = parts[3] if len(parts) > 3 else ""
            transcript = parts[6] if len(parts) > 6 else ""
            exon = parts[8] if len(parts) > 8 else ""
            impact = parts[2] if len(parts) > 2 else ""
            consequence = parts[1] if len(parts) > 1 else ""
            hgvsc = parts[9] if len(parts) > 9 else ""
            hgvsp = parts[10] if len(parts) > 10 else ""
        return gene, transcript, exon, impact, consequence, hgvsc, hgvsp


# =============================================================================
# Auto-detection
# =============================================================================

def auto_detect_adapter(headers: List[str]) -> AnnotationAdapter:
    """Detect annotation format from column headers and return appropriate adapter."""
    if ANNOVARAdapter.supports_headers(headers):
        return ANNOVARAdapter()
    if SnpEffAdapter.supports_headers(headers):
        return SnpEffAdapter()
    if VEPAdapter.supports_headers(headers):
        return VEPAdapter()
    # Default: VEP (pass-through, best-effort)
    return VEPAdapter()


def adapt_rows(rows: List[Dict[str, Any]], adapter: Optional[AnnotationAdapter] = None) -> List[Dict[str, Any]]:
    """Apply adapter to all rows. If adapter is None, auto-detect from first row keys."""
    if not rows:
        return []
    if adapter is None:
        headers = list(rows[0].keys())
        adapter = auto_detect_adapter(headers)
    return [adapter.adapt(row) for row in rows]
