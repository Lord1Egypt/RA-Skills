#!/usr/bin/env python3
"""
GPA Core Engine - Genomic Phenotype Association
v0.4 - 2026-05-19

API-first pipeline with cache layer. Replaces hardcoded gene dictionaries
with live queries to Ensembl, UniProt, GTEx, and gnomAD.

Phase 2 changes:
- MANE_SELECT / PROTEIN_DOMAINS / tissue gene lists → API queries
- run_dgra_pipeline is now async, with batch concurrent API calls
- --offline mode skips APIs, uses cache + local overrides only
"""

import json
import sys
import csv
import re
import os
import asyncio
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Tuple, Any
import argparse
import aiohttp

# v0.8.0: SpliceAI requires aiohttp for async HTTP queries
try:
    import aiohttp
except ImportError:
    aiohttp = None

# v0.5 P2-3: YAML config support
from dgra_config import DGRAGlobalConfig as GPAGlobalConfig, DGRAFileConfig as GPAFileConfig, DEFAULT_CONFIG_PATH
from dgra_cache import DGRACache
from dgra_api import DGRAAPIClient
from dgra_splice_predictor import SpliceAIPredictor, should_query_spliceai

# =============================================================================
# Offline Archive Persistence (v0.4)
# =============================================================================

OFFLINE_ARCHIVE_DIR = Path(__file__).parent.parent / "references" / "offline_data"

def _save_offline_archive(gene: str, ensembl_data: dict, uniprot_data: dict,
                          gtex_data: dict, tissue_profile: str,
                          gnomad_constraint_data: dict = None):
    """Persist API results for future offline use.
    v0.5 P1-4: Now also saves gnomAD gene constraint data."""
    OFFLINE_ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    archive = {
        "gene": gene,
        "tissue_profile": tissue_profile,
        "saved_at": datetime.utcnow().isoformat() + "Z",
        "ensembl": ensembl_data.get(gene, {}),
        "uniprot": uniprot_data.get(gene, {}),
        "gtex": gtex_data.get(gene, {}),
    }
    if gnomad_constraint_data is not None:
        archive["gnomad_constraint"] = gnomad_constraint_data.get(gene, {})
    path = OFFLINE_ARCHIVE_DIR / f"{gene}.json"
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(archive, f, indent=2, ensure_ascii=False, default=str)

def _load_offline_archive(gene: str) -> Optional[Dict]:
    """Load previously saved API results for offline mode.
    v0.5 P1-4: Returns gnomad_constraint field if present."""
    path = OFFLINE_ARCHIVE_DIR / f"{gene}.json"
    if not path.exists():
        return None
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return None

# =============================================================================
# Data Structures
# =============================================================================

# v0.5 P0-7: Sentinel for missing/unknown field values. Used instead of injecting
# false defaults like IMPACT="MODERATE" or VAF=0.5, which systematically
# underestimate risk.
_UNKNOWN = "UNKNOWN"

# v0.4.5: Common cancer gene lists for somatic mode
_COMMON_TS_GENES = {
    "TP53", "RB1", "CDKN2A", "CDKN2B", "PTEN", "NF1", "NF2", "APC", "BRCA1", "BRCA2",
    "ATM", "CHEK2", "MLH1", "MSH2", "MSH6", "PMS2", "VHL", "WT1", "TSC1", "TSC2",
    "PHF6", "BCOR", "BCORL1", "ASXL1", "RUNX1", "CEBPA", "GATA2", "ETV6", "DDX41",
    "SAMD9", "SAMD9L", "TP53BP1", "BRCC3", "RAD51", "RAD51C", "RAD51D", "PALB2",
    "BARD1", "NBN", "ATM", "CHEK2",
}

_KNOWN_AML_DRIVERS = {
    "FLT3", "NPM1", "IDH1", "IDH2", "DNMT3A", "TET2", "ASXL1", "RUNX1", "CEBPA",
    "TP53", "KIT", "NRAS", "KRAS", "PTPN11", "CBL", "JAK2", "JAK3", "SH2B3",
    "BCOR", "BCORL1", "PHF6", "GATA2", "ETV6", "DDX41", "SAMD9", "SAMD9L",
    "KDM6A", "KDM5C", "KMT2A", "KMT2D", "EZH2", "STAG2", "RAD21", "SMC1A",
    "SMC3", "ZRSR2", "SRSF2", "SF3B1", "U2AF1", "U2AF2",
}

# v0.5.1 OPT-P2-2: Gene family redundancy - reduce multi-hit false positives
# Genes with functional paralogs/isoforms that can compensate for LOF
_GENE_FAMILY_REDUNDANCY = {
    # Mitochondrial ADP/ATP translocases - 4 paralogs with overlapping function
    "SLC25A5": {
        "paralogs": ["SLC25A4", "SLC25A6", "SLC25A31"],  # ANT1, ANT3, ANT4
        "compensation_level": "partial",  # Not complete, but significant
        "reason": "ANT family has 4 paralogs; SLC25A5 (ANT2) loss partially compensated",
    },
    # CYP family - extensive redundancy for drug metabolism
    "CYP2D6": {
        "paralogs": ["CYP2C19", "CYP3A4", "CYP1A2", "CYP2C9"],
        "compensation_level": "partial",
        "reason": "CYP450 family redundancy; other isoforms handle most substrates",
    },
    # SLC drug transporters
    "SLC22A1": {
        "paralogs": ["SLC22A2", "SLC22A3"],  # OCT2, OCT3
        "compensation_level": "partial",
        "reason": "OCT family redundancy for cation transport",
    },
    # HLA class I - extensive polymorphism is normal, null alleles common
    "HLA-A": {"paralogs": [], "compensation_level": "complete", "reason": "HLA null alleles are normal polymorphism"},
    "HLA-B": {"paralogs": [], "compensation_level": "complete", "reason": "HLA null alleles are normal polymorphism"},
    "HLA-C": {"paralogs": [], "compensation_level": "complete", "reason": "HLA null alleles are normal polymorphism"},
}

@dataclass
class Evidence:
    """Structured evidence entry for variant tier classification.
    v0.5 P1-9: Replaces free-text tier_reason with traceable evidence chain.
    """
    source: str           # "ClinVar", "gnomAD", "GTEx", "ACMG", "GeneConstraint", "NMD", "DomainMapping", "Somatic", "SpecialList", "MultiHit", "Phase", "FastTrack"
    rule: str             # Human-readable rule/condition, e.g. "PM2: gnomAD_AF=0.0001 < 0.001"
    weight: float = 1.0   # Contribution weight to final tier (default 1.0)
    confidence: str = "high"  # "high" | "moderate" | "low"
    raw_data: Optional[Dict] = None  # Key API response fields for audit


@dataclass
class Variant:
    chrom: str
    pos: int
    ref: str
    alt: str
    gene: str
    transcript: str
    exon: str  # e.g., "E5/15"
    impact: str  # HIGH, MODERATE, LOW
    consequence: str  # frameshift, missense, splice_donor, etc.
    hgvsp: str  # protein change, e.g., "p.Thr111SerfsTer22"
    hgvsc: str  # cDNA change
    clinvar: str  # Pathogenic, Benign, etc.
    gnomad_af: Optional[float] = None
    gnomad_populations: Optional[Dict[str, Dict]] = None  # v0.5 P1-1: per-pop AFs
    dp: int = 0
    gq: float = 0.0
    gt: str = ""  # 0/1, 1/1, etc.
    vaf: Optional[float] = None

    # v0.4.5: Somatic annotation fields
    classification: str = ""  # OncoKB: Oncogenic, Likely Oncogenic, VUS, etc.
    is_tsg: bool = False
    is_oncogene: bool = False

    # Computed fields
    tier: Optional[int] = None
    tier_reason: str = ""
    tier_actions: List[str] = field(default_factory=list)
    domain_info: Optional[Dict] = None
    transcript_warning: Optional[str] = None
    pseudogene_warning: Optional[str] = None
    gnomad_status: Optional[str] = None
    tissue_relevance: Optional[Dict] = None

    # v0.5 P0-7: Quality confidence when key fields are missing.
    quality_confidence: str = "high"  # "high" | "medium" | "low" | "unknown"
    missing_fields: List[str] = field(default_factory=list)

    # v0.5 P1-2: Original gene symbol before HGNC normalization
    gene_original: str = ""

    # v0.5 P1-9: Structured evidence chain for traceable tier classification
    evidence_chain: List[Evidence] = field(default_factory=list)

    # v0.5 P1-13: Quality control flags for input validation
    qc_flags: List[str] = field(default_factory=list)

    # v0.5 P1-11: Upgrade conditions - forward-looking evidence gap descriptions
    upgrade_conditions: List[str] = field(default_factory=list)

    # v0.5 P1-4: Gene constraint metrics (pLI, LOEUF, lof_z, mis_z)
    gene_constraint: Optional[Dict] = None

    # v0.5 P1-10: Tier confidence classification
    tier_confidence: str = "LOW"  # "HIGH" | "MEDIUM" | "LOW"

    # v0.7: Phenotype association fields
    phenotype_match_score: Optional[float] = None
    phenotype_match_explanation: str = ""
    phenotype_match_confidence: str = ""
    phenotype_matched_pairs: List = field(default_factory=list)
    phenotype_known_list: List[str] = field(default_factory=list)

    # v0.7.2: ClinVar review status (CLNREVSTAT)
    clinvar_review_status: Optional[str] = None
    # v0.8.0: SpliceAI lookup result (pre-computed in pipeline)
    spliceai_result: Optional[Dict[str, Any]] = None

@dataclass
class GPAConfig:
    """User-facing config (kept simple). Maps to GPAGlobalConfig internally.
    v0.4-fix: tissue_profile has NO default - must be specified by user.
    """
    min_dp: int = 20
    min_gq: float = 90.0
    common_af_threshold: float = 0.01
    low_af_threshold: float = 0.001
    vaf_deviation_threshold: float = 0.20
    tissue_profile: Optional[str] = None  # NO default - caller must specify
    target_population: Optional[str] = None  # v0.5 P1-1: EAS, AMR, AFR, NFE, SAS, etc.
    offline_mode: bool = False
    somatic_mode: bool = False  # v0.4.5: tumor/somatic driver analysis mode
    multi_organ_profiles: Optional[List[str]] = None  # v0.5 P1-7: multi-organ assessment
    gene_sync_enabled: bool = True  # v0.5 P1-8: auto-sync special_gene_lists
    filter_stats: Optional[Dict[str, Any]] = None  # v0.7.1: variant pre-filtering statistics
    filter_preset: Optional[str] = None  # v0.7.1: filter preset name used
    gene_sync_ttl_days: int = 7  # v0.5 P1-8: sync cache TTL
    force_sync: bool = False  # v0.5 P1-8: force sync gene lists (bypass cache)
    evidence_detail: str = "brief"  # v0.5 P1-9: "brief" | "full" - evidence chain detail level in report
    database_version: Optional[str] = None  # v0.5 P1-15: freeze analysis DB version for reproducibility
    # v0.8.0: SpliceAI splice-prediction integration (default OFF - must be explicitly enabled)
    spliceai_enabled: bool = False
    spliceai_concurrency: int = 5

    def to_global(self) -> GPAGlobalConfig:
        gc = GPAGlobalConfig()
        gc.tissue_profile = self.tissue_profile or ""
        gc.target_population = self.target_population or ""
        gc.offline_mode = self.offline_mode
        gc.somatic_mode = self.somatic_mode
        gc.gene_sync_enabled = self.gene_sync_enabled
        gc.gene_sync_ttl_days = self.gene_sync_ttl_days
        gc.min_dp = self.min_dp
        gc.min_gq = self.min_gq
        gc.common_af_threshold = self.common_af_threshold
        gc.low_af_threshold = self.low_af_threshold
        gc.vaf_deviation_threshold = self.vaf_deviation_threshold
        return gc

    def get_tissue_profile(self, force_sync: bool = False) -> Dict:
        """Load tissue profile from references/tissue_context.json.
        v0.5 P1-8: Merged with external sync + user extensions for special_gene_lists.

        Priority of special_gene_lists:
          1. Hardcoded CORE (safety-critical, immutable)
          2. User add/remove extensions (user_gene_lists.json)
          3. Auto-synced from Orphanet / OMIM
          4. Static JSON from tissue_context.json

        Raises if tissue_profile is not set.
        Args:
            force_sync: Force a fresh sync even if cache is not expired.
        """
        if not self.tissue_profile:
            raise ValueError(
                "tissue_profile is required. Available profiles: general, hematopoietic, cardiovascular, "
                "hepatic, renal, neurological. Specify via --tissue or config.tissue_profile."
            )
        ref_path = Path(__file__).parent.parent / "references" / "tissue_context.json"
        with open(ref_path, 'r') as f:
            data = json.load(f)
        profiles = data.get("profiles", {})
        if self.tissue_profile not in profiles:
            available = ", ".join(profiles.keys())
            raise ValueError(f"Unknown tissue profile '{self.tissue_profile}'. Available: {available}")

        profile = dict(profiles[self.tissue_profile])

        # v0.5 P1-8: Merge special_gene_lists with sync + user extensions
        try:
            from dgra_gene_sync import get_merged_gene_lists_sync
            merged_lists = get_merged_gene_lists_sync(
                tissue_profile=self.tissue_profile,
                offline_mode=self.offline_mode,
                sync_enabled=self.gene_sync_enabled,
                ttl_days=self.gene_sync_ttl_days,
                force_sync=force_sync,
            )
            if merged_lists:
                profile["special_gene_lists"] = merged_lists
        except Exception as e:
            # Non-blocking: if merge fails, keep static lists
            print(f"[GPA] Gene list sync warning: {e} - using static lists")

        return profile

# =============================================================================
# Module A: Transcript Priority Correction  (v0.4: Ensembl API)
# =============================================================================

async def correct_transcript_priority(variant: Variant,
                                       ensembl_data: Dict[str, Dict]) -> Tuple[Variant, Optional[Dict]]:
    """
    Check if annotator selected non-canonical isoform.
    Uses Ensembl API canonical transcript; falls back to input VCF transcript.

    Args:
        variant: Variant object
        ensembl_data: Pre-fetched Ensembl gene data {gene: {canonical_transcript, ...}}

    Returns: (corrected_variant, warning_dict or None)
    """
    gene = variant.gene
    selected_tx = variant.transcript.split()[0] if variant.transcript else ""

    # Get canonical from Ensembl API
    ens = ensembl_data.get(gene, {})
    canonical = ens.get("canonical_transcript", "")

    if not canonical:
        # No API data: fall back to trusting annotator's choice
        return variant, None

    # If already canonical
    if selected_tx.startswith(canonical):
        return variant, None

    # Annotator selected non-canonical isoform
    warning = {
        "type": "TRANSCRIPT_DISCREPANCY",
        "gene": gene,
        "annotator_selected": selected_tx,
        "canonical": canonical,
        "message": f"Annotator selected {selected_tx}, but Ensembl canonical {canonical} should be used.",
        "recommendation": "Re-assess impact using canonical transcript.",
        "source": ens.get("source", "unknown"),
        "confidence": ens.get("confidence", "medium"),
    }

    variant.transcript_warning = json.dumps(warning)
    return variant, warning

# =============================================================================
# Module B: Pseudogene Interference Detection  (unchanged in v0.4)
# =============================================================================

# Load pseudogene database from JSON (v0.5.3)
_PSEUDOGENE_DB_PATH = Path(__file__).resolve().parent.parent / "references" / "pseudogene_database.json"
_PSEUDOGENE_CONFIG = {}

def _load_pseudogene_database():
    """Load pseudogene database from JSON. Falls back to empty if missing."""
    global _PSEUDOGENE_CONFIG
    if _PSEUDOGENE_CONFIG:
        return _PSEUDOGENE_CONFIG
    try:
        with open(_PSEUDOGENE_DB_PATH, "r") as f:
            db = json.load(f)
        _PSEUDOGENE_CONFIG = db.get("genes", {})
        print(f"[GPA] Loaded pseudogene database: {len(_PSEUDOGENE_CONFIG)} genes")
        return _PSEUDOGENE_CONFIG
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"[GPA] WARNING: pseudogene_database.json not found or invalid ({e}). Using empty config.")
        _PSEUDOGENE_CONFIG = {}
        return _PSEUDOGENE_CONFIG


# Legacy hardcoded config - kept as fallback if JSON missing
_PSEUDOGENE_CONFIG_LEGACY = {
    "SETBP1": {"pseudogene": "VWFP1", "vaf_expected": 0.5, "vaf_min": 0.30, "notes": "VWFP1 on chr1 shares homology"},
    "VWF": {"pseudogene": "VWFP1", "vaf_expected": 0.5, "vaf_min": 0.25, "notes": "VWFP1 exon 23-34 homology"},
    "GBA": {"pseudogene": "GBAP1", "vaf_expected": 0.5, "vaf_min": 0.20, "notes": "GBAP1 on chr1"},
    "PMS2": {"pseudogene": "PMS2CL", "vaf_expected": 0.5, "vaf_min": 0.25, "notes": "PMS2CL on chr7"},
}


# =============================================================================
# v0.6: Lightweight Pseudogene Lookup (manual curation + Ensembl REST)
# =============================================================================

_PSEUDOGENE_LOOKUP_PATH = Path(__file__).resolve().parent.parent / "references" / "pseudogene_lookup.json"
_PSEUDOGENE_LOOKUP: Optional[Dict] = None


def _load_pseudogene_lookup() -> Dict:
    """
    Load lightweight pseudogene lookup from JSON.
    Returns dict keyed by functional gene symbol.
    Falls back to empty dict if file missing.
    """
    global _PSEUDOGENE_LOOKUP
    if _PSEUDOGENE_LOOKUP is not None:
        return _PSEUDOGENE_LOOKUP

    try:
        with open(_PSEUDOGENE_LOOKUP_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        _PSEUDOGENE_LOOKUP = data.get("pairs", {})
        print(f"[GPA] Loaded pseudogene lookup: {len(_PSEUDOGENE_LOOKUP)} genes")
        return _PSEUDOGENE_LOOKUP
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"[GPA] INFO: pseudogene_lookup.json not found ({e}). Using empty lookup.")
        _PSEUDOGENE_LOOKUP = {}
        return _PSEUDOGENE_LOOKUP


def get_pseudogenes_for_gene(gene: str, offline_mode: bool = True) -> List[str]:
    """
    Return list of known pseudogenes for a given functional gene.

    Resolution order:
      1. Local pseudogene_lookup.json (manual curation)
      2. Legacy pseudogene_database.json
      3. (Future) Ensembl REST API - not yet implemented

    Args:
        gene: Functional gene symbol (e.g., "VWF")
        offline_mode: If True, skip API calls (default for reliability)

    Returns:
        List of pseudogene names (deduplicated). Empty if none known.
    """
    pseudogenes: List[str] = []

    # 1. v0.6 lookup
    lookup = _load_pseudogene_lookup()
    entry = lookup.get(gene)
    if entry:
        pseudogenes.extend(entry.get("pseudogenes", []))

    # 2. Legacy database (v0.5.3)
    legacy = _load_pseudogene_database()
    legacy_cfg = legacy.get(gene) or _PSEUDOGENE_CONFIG_LEGACY.get(gene)
    if legacy_cfg:
        legacy_pgs = legacy_cfg.get("pseudogenes", [])
        if isinstance(legacy_pgs, str):
            legacy_pgs = [legacy_pgs]
        pseudogenes.extend(legacy_pgs)

    # 3. (Future) Ensembl REST query when offline_mode=False

    # Deduplicate while preserving order
    seen = set()
    result = []
    for pg in pseudogenes:
        if pg and pg not in seen:
            seen.add(pg)
            result.append(pg)

    return result


def _calculate_pseudogene_score(
    observed_vaf: float,
    genotype: str,
    pseudogenes: List[str],
    gene: str,
) -> Dict:
    """
    Calculate pseudogene interference score (0.0-1.0).

    Scoring rules:
      - Homozygous (1/1): score=0 (no pseudogene interference expected)
      - Heterozygous (0/1) with VAF ~0.50: score=0
      - Heterozygous with VAF <0.30: score=0.8+ (strong interference)
      - Heterozygous with VAF 0.30-0.40: score=0.4-0.7 (suspected)
      - Heterozygous with VAF >0.65: score=0.3 (possible read bias)

    Returns dict with score, level, and recommendation.
    """
    if genotype in ["1/1", "1|1"]:
        return {
            "score": 0.0,
            "level": "none",
            "reason": "Homozygous variant - pseudogene interference unlikely",
            "recommendation": None,
        }

    if genotype not in ["0/1", "0|1"]:
        return {
            "score": 0.0,
            "level": "unknown_genotype",
            "reason": f"Genotype {genotype} not evaluable",
            "recommendation": None,
        }

    # Heterozygous scoring
    if observed_vaf < 0.20:
        return {
            "score": 0.9,
            "level": "strong_interference",
            "reason": f"VAF={observed_vaf:.2f} far below expected 0.50",
            "recommendation": "Strong evidence of pseudogene interference. Sanger validation or long-read sequencing strongly recommended.",
        }
    elif observed_vaf < 0.30:
        return {
            "score": 0.75,
            "level": "interference",
            "reason": f"VAF={observed_vaf:.2f} significantly below expected 0.50",
            "recommendation": "Probable pseudogene interference. Consider Sanger validation.",
        }
    elif observed_vaf < 0.40:
        return {
            "score": 0.55,
            "level": "suspected",
            "reason": f"VAF={observed_vaf:.2f} below expected 0.50",
            "recommendation": "Possible pseudogene interference. Caution advised.",
        }
    elif observed_vaf > 0.65:
        return {
            "score": 0.30,
            "level": "bias_suspected",
            "reason": f"VAF={observed_vaf:.2f} above expected 0.50",
            "recommendation": "Possible read bias or allele-specific expression. Review alignment.",
        }
    else:
        return {
            "score": 0.0,
            "level": "none",
            "reason": f"VAF={observed_vaf:.2f} within expected heterozygous range",
            "recommendation": None,
        }


def detect_pseudogene_artifact(variant: Variant) -> Optional[Dict]:
    """
    Detect pseudogene interference using v0.6 lookup system.

    v0.6: Unified detection using pseudogene_lookup.json + legacy DB.
    - Checks if gene has known pseudogenes
    - Evaluates VAF against expected heterozygous ratio
    - Returns structured score instead of binary flag

    Does NOT modify tier directly. Only provides evidence for confidence adjustment.
    """
    gene = variant.gene
    pseudogenes = get_pseudogenes_for_gene(gene)
    if not pseudogenes:
        return None

    observed_vaf = variant.vaf
    genotype = variant.gt

    if observed_vaf is None or genotype is None:
        return None

    score_info = _calculate_pseudogene_score(observed_vaf, genotype, pseudogenes, gene)

    # Build evidence dict
    if score_info["score"] >= 0.75:
        artifact_type = "PSEUDOGENE_INTERFERENCE"
    elif score_info["score"] >= 0.40:
        artifact_type = "PSEUDOGENE_SUSPECTED"
    else:
        return None  # No meaningful interference detected

    # Fetch lookup entry for metadata
    lookup = _load_pseudogene_lookup()
    entry = lookup.get(gene, {})
    strategy = entry.get("detection_strategy", "vaf_mismatch")
    confidence = entry.get("confidence", "medium")
    notes = entry.get("notes", "")

    return {
        "type": artifact_type,
        "gene": gene,
        "pseudogenes": pseudogenes,
        "strategy": strategy,
        "score": score_info["score"],
        "level": score_info["level"],
        "observed_vaf": observed_vaf,
        "expected_vaf": 0.5,
        "notes": notes,
        "recommendation": score_info["recommendation"],
        "confidence": confidence,
    }

# =============================================================================
# Module C: gnomAD Frequency Handler
# =============================================================================

def classify_gnomad_frequency(af: Optional[float], gene: str,
                               af_by_population: Optional[Dict[str, Dict]] = None,
                               target_population: Optional[str] = None) -> Dict:
    """
    Classify gnomAD allele frequency with zero-frequency handling.
    v0.5 P1-1: Population subgroup frequencies (EAS, AMR, AFR, NFE, SAS, etc.)

    If target_population is specified and available in af_by_population,
    uses that population's AF for classification instead of overall AF.
    """
    # Genes with germline warnings (clonal hematopoiesis filtering)
    GERMLINE_WARNING_GENES = {"ASXL1", "DNMT3A", "TET2", "TP53", "PPM1D", "JAK2", "CBL", "IDH1", "IDH2"}

    # Determine effective AF for classification
    effective_af = af
    pop_note = ""

    if target_population and af_by_population and target_population in af_by_population:
        pop_data = af_by_population[target_population]
        pop_af = pop_data.get("af")
        if pop_af is not None:
            effective_af = pop_af
            pop_note = f" Using {target_population} AF={pop_af:.6f} (overall AF={af})."

    # If overall AF is available but target population is missing, note it
    if target_population and (not af_by_population or target_population not in (af_by_population or {})):
        if af is not None:
            pop_note = f" {target_population} data unavailable; using overall AF={af}."
        else:
            pop_note = f" {target_population} data unavailable."

    if effective_af is None:
        result = {
            "af": "NOT_CAPTURED",
            "status": "gnomAD database does not capture this locus",
            "interpretation": "Population frequency data unavailable. Cannot judge benign based on gnomAD." + pop_note,
            "action": "Continue with other modules (domain, ClinVar, zygosity).",
            "risk_adjustment": "Do NOT downgrade risk due to gnomAD absence."
        }
        if af_by_population:
            result["af_populations"] = af_by_population
        return result

    if gene in GERMLINE_WARNING_GENES:
        result = {
            "af": effective_af,
            "status": "GERMLINE_WARNING",
            "interpretation": f"{gene} is filtered in gnomAD germline due to clonal hematopoiesis." + pop_note,
            "action": "Use alternative databases (ExAC pre-filtered, ClinVar, LOVD).",
            "risk_adjustment": "Evaluate independently of gnomAD."
        }
        if af_by_population:
            result["af_populations"] = af_by_population
        return result

    if effective_af > 0.01:
        result = {
            "af": effective_af,
            "status": "common_polymorphism",
            "interpretation": "High population frequency (>1%), likely benign." + pop_note,
            "action": "Require strong evidence to upgrade risk.",
            "risk_adjustment": "Default Tier 3 unless other evidence is strong."
        }
    elif effective_af > 0.001:
        result = {
            "af": effective_af,
            "status": "low_frequency",
            "interpretation": "Moderate frequency (0.1-1%), needs functional assessment." + pop_note,
            "action": "Include in comprehensive evaluation."
        }
    else:
        result = {
            "af": effective_af if effective_af else "extremely_rare",
            "status": "rare_variant",
            "interpretation": "Very rare in population (<0.1%), likely under negative selection." + pop_note,
            "action": "Focus attention, requires literature search.",
            "risk_adjustment": "Do NOT downgrade risk by default."
        }

    if af_by_population:
        result["af_populations"] = af_by_population
    return result

# =============================================================================
# Module C.5: HGNC Gene Symbol Normalization (v0.5 P1-2)
# =============================================================================

def normalize_gene_symbols(
    variants: List[Variant],
    hgnc_results: Dict[str, Dict[str, Any]],
    offline_mode: bool = False,
) -> List[str]:
    """
    Normalize gene symbols using HGNC API results.

    Mutates Variant objects in-place:
    - Sets gene_original to the original symbol
    - Updates gene to the approved HGNC symbol
    - Sets transcript_warning for outdated/withdrawn/unknown symbols

    Returns list of WARNING strings for the report.

    Args:
        variants: Variant objects to normalize
        hgnc_results: Dict mapping original symbol -> HGNC query result
        offline_mode: If True, skip validation for known symbols; warn on unknown
    """
    warnings = []

    for v in variants:
        original = v.gene
        v.gene_original = original

        hgnc = hgnc_results.get(original, {})
        status = hgnc.get("status", "query_failed")
        approved = hgnc.get("approved_symbol", original)

        if status == "approved":
            # Symbol is valid, may need case correction
            if original != approved:
                v.gene = approved
                warnings.append(
                    f"HGNC: Gene symbol corrected \"{original}\" → \"{approved}\" (approved)"
                )
            # else: exact match, no change needed

        elif status in ("previous", "alias"):
            # Outdated symbol - auto-replace with approved
            v.gene = approved
            prev_syms = ", ".join(hgnc.get("previous_symbols", [])) or "N/A"
            alias_syms = ", ".join(hgnc.get("alias_symbols", [])) or "N/A"
            warnings.append(
                f"HGNC WARNING: Outdated symbol \"{original}\" → \"{approved}\" "
                f"(status={status}, previous={prev_syms}, alias={alias_syms})"
            )
            # Set transcript_warning for visibility
            tw = json.loads(v.transcript_warning) if v.transcript_warning else {}
            tw["hgnc_warning"] = {
                "original": original,
                "approved": approved,
                "status": status,
                "action": "Symbol auto-corrected. Verify variant coordinates match approved symbol.",
            }
            v.transcript_warning = json.dumps(tw)

        elif status == "withdrawn":
            # Symbol withdrawn - cannot map, keep original, mark warning
            warnings.append(
                f"HGNC WARNING: Symbol \"{original}\" is WITHDRAWN. "
                f"Approved symbol: \"{approved}\". Cannot auto-correct - manual review required."
            )
            tw = json.loads(v.transcript_warning) if v.transcript_warning else {}
            tw["hgnc_warning"] = {
                "original": original,
                "approved": approved,
                "status": "withdrawn",
                "action": "Symbol withdrawn. Manual mapping required. Verify coordinates independently.",
            }
            v.transcript_warning = json.dumps(tw)

        elif status in ("not_found", "query_failed"):
            # Unknown symbol - keep original, mark warning
            if offline_mode:
                # In offline mode, we can't validate. Only warn if symbol looks suspicious.
                # Known symbols from our common lists are accepted without warning.
                known_symbols = {
                    "VWF", "F8", "F9", "F7", "F10", "F11", "F12", "F13A1", "F13B",
                    "PROC", "PROS1", "SERPINC1", "SERPIND1", "PLG", "THBD",
                    "BRCA1", "BRCA2", "TP53", "PTEN", "APC", "MLH1", "MSH2", "MSH6", "PMS2",
                    "ATM", "CHEK2", "PALB2", "CDH1", "STK11",
                    "RUNX1", "CEBPA", "GATA2", "ETV6", "DDX41", "SAMD9", "SAMD9L",
                    "ASXL1", "BCOR", "BCORL1", "PHF6", "IDH1", "IDH2", "DNMT3A", "TET2",
                    "FLT3", "NPM1", "NRAS", "KRAS", "KIT",
                    "CYP2D6", "CYP2C19", "CYP3A4", "CYP3A5", "ABCB1", "TPMT", "DPYD", "UGT1A1",
                    "SCN5A", "KCNQ1", "KCNH2", "RYR2", "DSP", "PKP2", "LMNA", "TTN",
                }
                if original not in known_symbols:
                    warnings.append(
                        f"HGNC WARNING: Symbol \"{original}\" could not be validated (offline mode). "
                        f"Not in known gene lists - may be outdated or misspelled."
                    )
                    tw = json.loads(v.transcript_warning) if v.transcript_warning else {}
                    tw["hgnc_warning"] = {
                        "original": original,
                        "status": "unvalidated_offline",
                        "action": "Offline mode: symbol not in known lists. Manual verification recommended.",
                    }
                    v.transcript_warning = json.dumps(tw)
                # else: known symbol, silently accept in offline mode
            else:
                # Online mode: API returned not_found - definitely warn
                warnings.append(
                    f"HGNC WARNING: Symbol \"{original}\" not found in HGNC database. "
                    f"May be misspelled, outdated, or non-standard. Keeping original symbol."
                )
                tw = json.loads(v.transcript_warning) if v.transcript_warning else {}
                tw["hgnc_warning"] = {
                    "original": original,
                    "status": status,
                    "action": "Symbol not found in HGNC. Verify spelling or check if gene has been renamed.",
                }
                v.transcript_warning = json.dumps(tw)

    return warnings


# =============================================================================
# Module D: Protein Domain Mapping
# =============================================================================

# =============================================================================
# Module D: Protein Domain Mapping  (v0.4: UniProt API)
# =============================================================================

# v0.3 hardcoded PROTEIN_DOMAINS dict removed - now fetched from UniProt API
# Protein domains are loaded via dgra_api.query_uniprot_by_gene() and passed
# as uniprot_data dict to this function.

def parse_protein_position(hgvsp: str) -> Optional[int]:
    """Extract amino acid position from p. string. Handles NP_ prefix."""
    hgvsp = str(hgvsp) if hgvsp is not None else ""
    if not hgvsp or hgvsp == "" or hgvsp == "nan":
        return None
    # Strip NP_ prefix if present: NP_000543.3:p.Val1565Leu -> p.Val1565Leu
    if ':p.' in hgvsp:
        hgvsp = hgvsp.split(':p.', 1)[1]
        hgvsp = 'p.' + hgvsp
    # Match p.XXX123 or p.Ala123 or p.123
    match = re.search(r'p\.[A-Za-z]+(\d+)', hgvsp)
    if match:
        return int(match.group(1))
    match = re.search(r'p\.(\d+)', hgvsp)
    if match:
        return int(match.group(1))
    return None

def map_variant_to_domain(variant: Variant, uniprot_data: Dict[str, Dict]) -> Dict:
    """
    Map variant to protein functional domain using UniProt API data.

    Args:
        variant: Variant object
        uniprot_data: Pre-fetched UniProt data {gene: {domains: [...], sequence_length: N}}

    Returns:
        Domain mapping dict with damage assessment.
    """
    gene = variant.gene
    up = uniprot_data.get(gene, {})
    domains = up.get("domains", [])
    seq_length = up.get("sequence_length")
    aa_pos = parse_protein_position(variant.hgvsp)

    # No API data available
    if not domains:
        if seq_length and aa_pos and aa_pos > seq_length:
            return {
                "domain": "unknown",
                "note": f"Parsed aa{aa_pos} exceeds UniProt sequence length ({seq_length}). "
                        "Possible transcript mismatch.",
                "gene": gene,
                "hgvsp": variant.hgvsp,
                "source": up.get("source", "failed"),
                "confidence": up.get("confidence", "low"),
                "interpro_id": None,
                "interpro_url": None,
            }

        return {
            "domain": "unknown",
            "note": "No UniProt domain annotation available for this gene.",
            "gene": gene,
            "hgvsp": variant.hgvsp,
            "source": up.get("source", "failed"),
            "confidence": up.get("confidence", "low"),
            "interpro_id": None,
            "interpro_url": None,
        }

    if not aa_pos:
        return {
            "domain": "unknown",
            "note": "Could not parse protein position from hgvsp",
            "gene": gene,
            "hgvsp": variant.hgvsp,
            "source": up.get("source", "unknown"),
            "interpro_id": None,
            "interpro_url": None,
        }

    # Search for domain overlap
    for d in domains:
        start = d.get("start")
        end = d.get("end")
        if start is None or end is None:
            continue

        if start <= aa_pos <= end:
            # Determine damage type
            if "frameshift" in variant.consequence or "nonsense" in variant.consequence:
                relative_pos = (aa_pos - start) / (end - start + 1)
                if relative_pos < 0.3:
                    damage = "N-terminal destruction, domain completely lost"
                    integrity = "completely_destroyed"
                elif relative_pos < 0.7:
                    damage = "Mid-domain truncation"
                    integrity = "partially_destroyed"
                else:
                    damage = "C-terminal truncation, partial domain retention"
                    integrity = "partially_retained"
            elif "splice" in variant.consequence:
                damage = "Splice site disruption, may cause exon skipping"
                integrity = "splicing_disrupted"
            else:
                damage = "Point mutation, assess specific amino acid change"
                integrity = "point_mutation"

            return {
                "domain": d.get("name", "unnamed"),
                "domain_range": f"aa{start}-{end}",
                "position_in_domain": f"aa{aa_pos}",
                "relative_position": round(relative_pos if "relative_pos" in locals() else (aa_pos - start) / (end - start + 1), 2),
                "function": d.get("type", "unknown"),
                "damage_type": damage,
                "domain_integrity": integrity,
                "gene": gene,
                "source": up.get("source", "unknown"),
                "confidence": up.get("confidence", "medium"),
                "interpro_id": (up.get("interpro_ids") or [None])[0],
                "interpro_url": f"https://www.ebi.ac.uk/interpro/entry/InterPro/{(up.get('interpro_ids') or [None])[0]}/" if (up.get("interpro_ids") or [None])[0] else None,
            }

    # Position outside all annotated domains
    return {
        "domain": "inter-domain / unannotated",
        "position": f"aa{aa_pos}",
        "note": "Position outside known functional domains",
        "gene": gene,
        "source": up.get("source", "unknown"),
        "confidence": up.get("confidence", "medium"),
        "interpro_id": (up.get("interpro_ids") or [None])[0],
        "interpro_url": f"https://www.ebi.ac.uk/interpro/entry/InterPro/{(up.get('interpro_ids') or [None])[0]}/" if (up.get("interpro_ids") or [None])[0] else None,
    }

# =============================================================================
# Module D.5: Gene Constraint Evaluation (v0.5 P1-4: pLI/LOEUF)
# =============================================================================

def evaluate_gene_constraint(variant: Variant) -> Dict[str, Any]:
    """
    Evaluate gnomAD gene constraint for variant tier modulation.

    Only applies to LOF variants (frameshift, nonsense, splice, start_lost, stop_gained).
    Non-LOF variants get constraint info for report but no tier upgrade.

    Returns:
    {
        "constraint_level": "strong" | "moderate" | "tolerant" | "unknown",
        "pLI": 0.99,
        "loeuf": 0.12,
        "lof_z": 5.2,
        "mis_z": 3.1,
        "is_lof": True,
        "tier_adjustment": 1,  # -1, 0, or +1 (only +1 for strong LOF constraint)
        "reason": "LOF-intolerant gene (pLI=0.99, LOEUF=0.12)",
    }
    """
    gc = variant.gene_constraint
    if not gc or gc.get("status") in ("NO_CONSTRAINT_DATA", "QUERY_FAILED"):
        return {
            "constraint_level": "unknown",
            "pLI": None,
            "loeuf": None,
            "lof_z": None,
            "mis_z": None,
            "is_lof": False,
            "tier_adjustment": 0,
            "reason": "No constraint data available",
        }

    pLI = gc.get("pLI")
    loeuf = gc.get("loeuf")
    lof_z = gc.get("lof_z")
    mis_z = gc.get("mis_z")

    # Determine if variant is LOF
    lof_consequences = {
        "frameshift", "nonsense", "stop_gained", "start_lost",
        "splice_donor", "splice_acceptor", "splice_site",
    }
    is_lof = any(lof_term in variant.consequence.lower() for lof_term in lof_consequences)

    # Determine constraint level
    constraint_level = "unknown"
    tier_adjustment = 0
    reason = ""

    if pLI is not None and loeuf is not None:
        if pLI >= 0.9 or loeuf <= 0.35:
            constraint_level = "strong"
            if is_lof:
                tier_adjustment = 1
                reason = f"LOF-intolerant gene (pLI={pLI:.2f}, LOEUF={loeuf:.2f}) - heterozygous LOF likely pathogenic"
            else:
                reason = f"LOF-intolerant gene (pLI={pLI:.2f}, LOEUF={loeuf:.2f}) - but variant is non-LOF, no tier upgrade"
        elif (pLI >= 0.5 and pLI < 0.9) or (loeuf >= 0.35 and loeuf <= 0.8):
            constraint_level = "moderate"
            reason = f"Moderate LOF constraint (pLI={pLI:.2f}, LOEUF={loeuf:.2f})"
        elif pLI < 0.5 and loeuf > 0.8:
            constraint_level = "tolerant"
            reason = f"LOF-tolerant gene (pLI={pLI:.2f}, LOEUF={loeuf:.2f}) - background LOF tolerated"
    elif pLI is not None:
        # Only pLI available
        if pLI >= 0.9:
            constraint_level = "strong"
            if is_lof:
                tier_adjustment = 1
                reason = f"LOF-intolerant gene (pLI={pLI:.2f}) - heterozygous LOF likely pathogenic"
            else:
                reason = f"LOF-intolerant gene (pLI={pLI:.2f}) - but variant is non-LOF"
        elif pLI >= 0.5:
            constraint_level = "moderate"
            reason = f"Moderate LOF constraint (pLI={pLI:.2f})"
        else:
            constraint_level = "tolerant"
            reason = f"LOF-tolerant gene (pLI={pLI:.2f})"
    elif loeuf is not None:
        # Only LOEUF available
        if loeuf <= 0.35:
            constraint_level = "strong"
            if is_lof:
                tier_adjustment = 1
                reason = f"LOF-intolerant gene (LOEUF={loeuf:.2f}) - heterozygous LOF likely pathogenic"
            else:
                reason = f"LOF-intolerant gene (LOEUF={loeuf:.2f}) - but variant is non-LOF"
        elif loeuf <= 0.8:
            constraint_level = "moderate"
            reason = f"Moderate LOF constraint (LOEUF={loeuf:.2f})"
        else:
            constraint_level = "tolerant"
            reason = f"LOF-tolerant gene (LOEUF={loeuf:.2f})"
    else:
        reason = "Constraint metrics incomplete"

    return {
        "constraint_level": constraint_level,
        "pLI": pLI,
        "loeuf": loeuf,
        "lof_z": lof_z,
        "mis_z": mis_z,
        "is_lof": is_lof,
        "tier_adjustment": tier_adjustment,
        "reason": reason,
    }


# =============================================================================
# Module D.6: NMD Prediction (v0.5 P1-5: PVS1 refinement)
# =============================================================================

def predict_nmd(variant: Variant, ensembl_data: Optional[Dict] = None) -> Dict[str, Any]:
    """
    Predict nonsense-mediated decay (NMD) sensitivity based on truncation position.

    ClinGen PVS1 guidance:
    - Internal exons (up to penultimate exon, excluding last 50-55bp) → NMD sensitive → PVS1 applies
    - Last 50-55bp of penultimate exon → possible NMD escape → PVS1 downgraded to PM/PP
    - Last exon → NMD escape → PVS1 does NOT apply
    - UTR regions → NMD does NOT apply

    Returns:
    {
        "status": "sensitive" | "escape" | "possible_escape" | "not_applicable" | "unknown",
        "reason": "Truncation in internal exon → classic NMD",
        "confidence": "high" | "moderate" | "low",
        "pvs1_applicable": True/False,
        "pvs1_strength": "strong" | "moderate" | "weak" | "not_applicable",
    }
    """
    consequence = str(variant.consequence or "").lower()

    # Check if variant is a truncating variant (LOF)
    lof_terms = {"frameshift", "nonsense", "stop_gained", "start_lost"}
    is_truncating = any(term in consequence for term in lof_terms)

    # Splice variants are not handled by simple exon position rules
    if "splice" in consequence:
        return {
            "status": "unknown",
            "reason": "Splice variant - NMD prediction requires transcript-level analysis",
            "confidence": "low",
            "pvs1_applicable": True,  # Conservative: assume PVS1 applies for splice
            "pvs1_strength": "strong",
        }

    if not is_truncating:
        return {
            "status": "not_applicable",
            "reason": "Not a truncating variant - NMD prediction not applicable",
            "confidence": "high",
            "pvs1_applicable": False,
            "pvs1_strength": "not_applicable",
        }

    # Parse exon field (e.g., "2/15" or "15/15")
    exon_str = str(variant.exon or "").strip()
    if not exon_str or exon_str == _UNKNOWN:
        # No exon info - conservative assumption: NMD sensitive
        return {
            "status": "unknown",
            "reason": "NMD status unknown, assuming sensitive (conservative)",
            "confidence": "low",
            "pvs1_applicable": True,
            "pvs1_strength": "strong",
        }

    # Parse exon position
    try:
        if "/" in exon_str:
            current_exon, total_exons = exon_str.split("/", 1)
            current = int(current_exon.strip())
            total = int(total_exons.strip())
        elif " of " in exon_str.lower():
            # Format: "2 of 15"
            parts = exon_str.lower().split(" of ")
            current = int(parts[0].strip())
            total = int(parts[1].strip())
        else:
            # Single number - can't determine position
            return {
                "status": "unknown",
                "reason": f"Cannot determine exon position from '{exon_str}' - assuming sensitive",
                "confidence": "low",
                "pvs1_applicable": True,
                "pvs1_strength": "strong",
            }
    except (ValueError, IndexError):
        return {
            "status": "unknown",
            "reason": f"Cannot parse exon '{exon_str}' - assuming sensitive",
            "confidence": "low",
            "pvs1_applicable": True,
            "pvs1_strength": "strong",
        }

    if total <= 0:
        return {
            "status": "unknown",
            "reason": "Invalid total exon count - assuming sensitive",
            "confidence": "low",
            "pvs1_applicable": True,
            "pvs1_strength": "strong",
        }

    # Determine NMD status based on exon position
    if current == total:
        # Last exon - NMD escape
        return {
            "status": "escape",
            "reason": f"Truncation in last exon ({current}/{total}) - NMD escape",
            "confidence": "high",
            "pvs1_applicable": False,
            "pvs1_strength": "not_applicable",
        }
    elif current == total - 1:
        # Penultimate exon - possible escape if within last 50-55bp of CDS
        # Without exact CDS position, we use a conservative estimate:
        # If we have transcript length info from Ensembl, we could be more precise
        return {
            "status": "possible_escape",
            "reason": f"Truncation in penultimate exon ({current}/{total}) - possible NMD escape if within last 50-55bp",
            "confidence": "moderate",
            "pvs1_applicable": False,  # Conservative: don't apply PVS1 if uncertain
            "pvs1_strength": "moderate",  # Downgraded to PM/PP level
        }
    else:
        # Internal exon - classic NMD
        return {
            "status": "sensitive",
            "reason": f"Truncation in internal exon ({current}/{total}) - classic NMD",
            "confidence": "high",
            "pvs1_applicable": True,
            "pvs1_strength": "strong",
        }


# =============================================================================
# Module D.7: Missense Stratification (v0.5 P1-5)
# =============================================================================

def evaluate_missense_tier(variant: Variant, domain_info: Optional[Dict],
                           gene_constraint: Optional[Dict]) -> Dict[str, Any]:
    """
    Stratify missense variants by domain impact and conservation.

    Returns a score (0-1) and tier recommendation for missense variants.

    Scoring:
    - Domain-critical: completely_destroyed + mis_z > 3.09 → score=0.9
    - Likely damaging: partially_destroyed + mis_z 2-3.09 → score=0.6
    - Tolerated: tolerated/inter-domain + mis_z < 2 → score=0.1
    - Unknown: no domain info → score=0.3 (conservative)

    Returns:
    {
        "score": 0.9,
        "tier_recommendation": 2,  # or 3
        "category": "domain_critical" | "likely_damaging" | "tolerated" | "unknown",
        "reason": "Missense in critical domain residue (mis_z=4.2)",
    }
    """
    consequence = str(variant.consequence or "").lower()

    # Only applies to missense variants
    if "missense" not in consequence:
        return {
            "score": 0.0,
            "tier_recommendation": None,
            "category": "not_missense",
            "reason": "Not a missense variant",
        }

    # Get mis_z score
    mis_z = None
    if gene_constraint and gene_constraint.get("mis_z") is not None:
        mis_z = float(gene_constraint["mis_z"])

    # Get domain integrity
    domain_integrity = None
    if domain_info:
        domain_integrity = domain_info.get("domain_integrity")

    # Stratify
    if domain_integrity == "completely_destroyed":
        if mis_z is not None and mis_z > 3.09:
            return {
                "score": 0.9,
                "tier_recommendation": 2,
                "category": "domain_critical",
                "reason": f"Missense in critical domain residue (mis_z={mis_z:.2f}) - high pathogenic potential",
            }
        else:
            return {
                "score": 0.7,
                "tier_recommendation": 2,
                "category": "likely_damaging",
                "reason": f"Missense destroys domain structure (mis_z={mis_z:.2f if mis_z else 'N/A'})",
            }
    elif domain_integrity == "partially_destroyed":
        if mis_z is not None and mis_z >= 2.0:
            return {
                "score": 0.6,
                "tier_recommendation": 2,
                "category": "likely_damaging",
                "reason": f"Missense in conserved domain (mis_z={mis_z:.2f}) - likely damaging",
            }
        else:
            mis_z_fmt = f"{mis_z:.2f}" if mis_z is not None else "N/A"
            return {
                "score": 0.4,
                "tier_recommendation": 2,
                "category": "possibly_damaging",
                "reason": f"Missense partially disrupts domain (mis_z={mis_z_fmt})",
            }
    elif domain_integrity == "tolerated":
        if mis_z is not None and mis_z < 2.0:
            return {
                "score": 0.1,
                "tier_recommendation": 3,
                "category": "tolerated",
                "reason": f"Missense in non-critical region (mis_z={mis_z:.2f}) - likely tolerated",
            }
        else:
            return {
                "score": 0.3,
                "tier_recommendation": 2,
                "category": "uncertain",
                "reason": f"Missense tolerated by structure but in conserved region (mis_z={mis_z:.2f})",
            }
    else:
        # No domain info or unknown
        if mis_z is not None and mis_z > 3.09:
            return {
                "score": 0.5,
                "tier_recommendation": 2,
                "category": "conservation_concern",
                "reason": f"Missense in highly constrained gene (mis_z={mis_z:.2f}) - domain info unavailable",
            }
        else:
            return {
                "score": 0.3,
                "tier_recommendation": 2,
                "category": "unknown",
                "reason": "Missense with unknown domain impact - conservative Tier 2",
            }


# =============================================================================
# Module E: Tissue Relevance Assessment  (v0.4: GTEx API + fallback)
# =============================================================================

def aggregate_gtex_expression(results: List[Dict[str, Any]],
                               strategy: str = "max") -> Dict[str, Any]:
    """
    Aggregate multi-tissue GTEx expression results.

    v0.5 P1-6: Multi-tissue GTEx aggregation. Takes a list of per-tissue
    GTEx results and returns a single aggregated result dict compatible
    with the single-tissue format.

    Args:
        results: List of GTEx result dicts (from query_gtex_expression_multi)
        strategy: Aggregation strategy - "max" (default, conservative),
                  "mean", or "median"

    Returns:
        Aggregated result dict with:
        - median_tpm: aggregated TPM value
        - max_tpm: maximum TPM across tissues
        - mean_tpm: mean TPM across tissues
        - expressing_tissues: count of tissues with TPM >= 1.0
        - primary_tissues: list of tissues with TPM >= 10.0
        - all_tissues: list of (tissue, tpm) tuples
        - source: "gtex_multi"
    """
    if not results:
        return {
            "median_tpm": None,
            "max_tpm": None,
            "mean_tpm": None,
            "expressing_tissues": 0,
            "primary_tissues": [],
            "all_tissues": [],
            "source": "gtex_multi",
            "unit": "TPM",
        }

    # Extract valid TPM values
    valid = []
    all_tissues = []
    for r in results:
        tpm = r.get("median_tpm")
        tissue = r.get("tissue", "unknown")
        if tpm is not None and tpm >= 0:
            valid.append(tpm)
            all_tissues.append((tissue, tpm))

    if not valid:
        return {
            "median_tpm": None,
            "max_tpm": None,
            "mean_tpm": None,
            "expressing_tissues": 0,
            "primary_tissues": [],
            "all_tissues": all_tissues,
            "source": "gtex_multi",
            "unit": "TPM",
        }

    max_tpm = max(valid)
    mean_tpm = sum(valid) / len(valid)

    # Determine aggregated TPM based on strategy
    if strategy == "max":
        aggregated_tpm = max_tpm
    elif strategy == "mean":
        aggregated_tpm = mean_tpm
    elif strategy == "median":
        sorted_tpms = sorted(valid)
        mid = len(sorted_tpms) // 2
        aggregated_tpm = sorted_tpms[mid] if len(sorted_tpms) % 2 == 1 else (sorted_tpms[mid - 1] + sorted_tpms[mid]) / 2
    else:
        aggregated_tpm = max_tpm

    expressing_tissues = sum(1 for t in valid if t >= 1.0)
    primary_tissues = [tissue for tissue, tpm in all_tissues if tpm >= 10.0]

    return {
        "median_tpm": aggregated_tpm,  # Named "median_tpm" for backward compatibility
        "max_tpm": max_tpm,
        "mean_tpm": mean_tpm,
        "expressing_tissues": expressing_tissues,
        "primary_tissues": primary_tissues,
        "all_tissues": all_tissues,
        "source": "gtex_multi",
        "unit": "TPM",
    }


def assess_tissue_relevance(variant: Variant, tissue_profile: Dict,
                            gtex_data: Dict[str, Dict]) -> Dict:
    """
    Assess if gene is relevant to target tissue/organ context.

    Priority:
    1. GTEx API expression data (if available) - auto-classify by TPM thresholds
    2. Local tissue_context.json profile (fallback for API failures)
    3. Unknown if neither available - conservative, do NOT fast-track

    Args:
        variant: Variant object
        tissue_profile: Loaded tissue profile (tier_rules + special_gene_lists)
        gtex_data: Pre-fetched GTEx data {gene: {median_tpm, ...}}
    """
    gene = variant.gene
    profile_name = tissue_profile.get("display_name", "target tissue")

    # --- Priority 1: GTEx API data ---
    gtex = gtex_data.get(gene, {})
    tpm = gtex.get("median_tpm")

    # v0.5 P1-6: Check if this is multi-tissue aggregated data
    is_multi_tissue = gtex.get("source") == "gtex_multi"
    all_tissues = gtex.get("all_tissues", [])
    max_tpm = gtex.get("max_tpm")
    mean_tpm = gtex.get("mean_tpm")
    primary_tissues = gtex.get("primary_tissues", [])
    expressing_tissues = gtex.get("expressing_tissues", 0)

    # v0.5 P0-6: General profile - skip GTEx tissue-specific fast-track.
    # When gtex_tissue is null, expression-based fast-track is disabled;
    # assessment relies on special gene lists and ClinVar/gnomAD instead.
    if tpm is not None and tissue_profile.get("gtex_tissue") is not None:
        # v0.5 P1-6: Multi-tissue rationale
        if is_multi_tissue and all_tissues:
            tissue_count = len(all_tissues)
            if tpm >= 10.0:
                relevance = "primary"
                rationale = f"High {profile_name} expression (max TPM={max_tpm:.1f} across {tissue_count} tissues) per GTEx."
            elif tpm >= 1.0:
                relevance = "secondary"
                rationale = f"Moderate {profile_name} expression (max TPM={max_tpm:.1f} across {tissue_count} tissues) per GTEx."
            elif tpm > 0:
                relevance = "none"
                rationale = f"Low {profile_name} expression (max TPM={max_tpm:.2f} across {tissue_count} tissues) per GTEx."
            else:
                relevance = "none"
                rationale = f"No detectable {profile_name} expression across {tissue_count} tissues per GTEx."
        else:
            # Single tissue (backward compatible)
            if tpm >= 10.0:
                relevance = "primary"
                rationale = f"High {profile_name} expression (TPM={tpm:.1f}) per GTEx."
            elif tpm >= 1.0:
                relevance = "secondary"
                rationale = f"Moderate {profile_name} expression (TPM={tpm:.1f}) per GTEx."
            elif tpm > 0:
                relevance = "none"
                rationale = f"Low {profile_name} expression (TPM={tpm:.2f}) per GTEx."
            else:
                relevance = "none"
                rationale = f"No detectable {profile_name} expression per GTEx."

        # Fast track for none + benign
        if relevance == "none":
            if variant.clinvar and "Pathogenic" in variant.clinvar:
                return {
                    "tier_suggestion": 2,
                    "relevance": relevance,
                    "reason": f"{gene} is not {profile_name}-relevant (GTEx TPM={tpm:.2f}) but ClinVar pathogenic.",
                    "clinical_note": "Inform patient, record in medical history.",
                    "fast_track": False,
                    "rationale": rationale,
                    "gtex_tpm": tpm,
                    "source": gtex.get("source", "gtex"),
                }

            return {
                "tier_suggestion": 3,
                "relevance": relevance,
                "reason": f"{gene} has no {profile_name} relevance (GTEx TPM={tpm:.2f}).",
                "clinical_note": f"No impact on {profile_name} function or safety.",
                "fast_track": True,
                "rationale": rationale,
                "gtex_tpm": tpm,
                "source": gtex.get("source", "gtex"),
            }

        # Primary or secondary: standard pipeline
        # v0.5 P1-6: Enhanced clinical note for multi-tissue
        if is_multi_tissue and all_tissues:
            tissue_detail = "; ".join([f"{t}:{v:.1f}" for t, v in all_tissues])
            clinical_note = f"{gene} is {relevance}-relevant to {profile_name} (max TPM={max_tpm:.1f} across {len(all_tissues)} tissues: {tissue_detail})."
        else:
            clinical_note = f"{gene} is {relevance}-relevant to {profile_name} (GTEx TPM={tpm:.1f})."

        return {
            "tier_suggestion": "assess_via_standard_pipeline",
            "relevance": relevance,
            "gtex_tpm": tpm,
            "rationale": rationale,
            "fast_track": False,
            "clinical_note": clinical_note,
            "source": gtex.get("source", "gtex"),
        }

    # --- Priority 1b: GTEx data available but tissue is null (general profile) ---
    if tpm is not None and tissue_profile.get("gtex_tissue") is None:
        # For general profile, use max TPM across all queried tissues as a proxy
        # for "expressed somewhere important". Still don't fast-track based on
        # expression alone; rely on special lists.
        if tpm >= 10.0:
            relevance = "primary"
            rationale = f"High expression (TPM={tpm:.1f}) in at least one tissue. Relevant to general health."
        elif tpm >= 1.0:
            relevance = "secondary"
            rationale = f"Moderate expression (TPM={tpm:.1f}) in at least one tissue."
        else:
            relevance = "none"
            rationale = f"Low expression (TPM={tpm:.2f}) - not prominently expressed."
        return {
            "tier_suggestion": "assess_via_standard_pipeline",
            "relevance": relevance,
            "gtex_tpm": tpm,
            "rationale": rationale,
            "fast_track": False,
            "clinical_note": f"{gene} general relevance: {relevance} (TPM={tpm:.1f}). No tissue-specific fast-track.",
            "source": gtex.get("source", "gtex"),
        }

    # --- Priority 2: Local tissue_context.json fallback ---
    genes_local = tissue_profile.get("genes", {})
    relevance_info = genes_local.get(gene)

    if relevance_info:
        relevance = relevance_info.get("relevance", "unknown")
        gtex_rpkm_local = relevance_info.get("gtex_rpkm", None)
        rationale = relevance_info.get("rationale", "")

        if relevance == "none":
            if variant.clinvar and "Pathogenic" in variant.clinvar:
                return {
                    "tier_suggestion": 2,
                    "relevance": relevance,
                    "reason": f"{gene} is not {profile_name}-relevant but ClinVar pathogenic.",
                    "clinical_note": "Inform patient, record in medical history.",
                    "fast_track": False,
                    "rationale": rationale,
                    "gtex_rpkm": gtex_rpkm_local,
                    "source": "local_fallback",
                }

            return {
                "tier_suggestion": 3,
                "relevance": relevance,
                "reason": f"{gene} has no {profile_name} relevance.",
                "clinical_note": f"No impact on {profile_name} function or safety.",
                "fast_track": True,
                "rationale": rationale,
                "gtex_rpkm": gtex_rpkm_local,
                "source": "local_fallback",
            }

        return {
            "tier_suggestion": "assess_via_standard_pipeline",
            "relevance": relevance,
            "gtex_rpkm": gtex_rpkm_local,
            "rationale": rationale,
            "fast_track": False,
            "clinical_note": f"{gene} is {relevance}-relevant to {profile_name}.",
            "source": "local_fallback",
        }

    # --- Priority 3: Special gene lists (irreplaceable clinical rules) ---
    special_lists = tissue_profile.get("special_gene_lists", {})
    _SPECIAL_LIST_RELEVANCE = {
        # general + hematopoietic (overlapping keys share same values)
        "cancer_predisposition": "primary",
        "cardiac_safety": "primary",
        "coagulation": "primary",
        "fa_dna_repair": "primary",
        "drug_metabolism": "secondary",
        "kir_cluster": "secondary",
        "immunodeficiency": "primary",
        # cardiovascular
        "cardiomyopathy": "primary",
        "ion_channel": "primary",
        "aortopathy": "primary",
        "arrhythmia": "primary",
        # hepatic
        "bilirubin_metabolism": "secondary",
        "cyp450": "secondary",
        "cholestatic": "primary",
        "hemochromatosis": "primary",
        # renal
        "renal_ciliopathy": "primary",
        "tubulopathy": "primary",
        "nephrotic": "primary",
        "congenital_abnormalities": "primary",
        # neurological
        "neurodegeneration": "primary",
        "leukodystrophy": "primary",
        "epilepsy": "primary",
        "movement_disorder": "primary",
    }
    for list_name, genes_in_list in special_lists.items():
        if gene in genes_in_list:
            relevance = _SPECIAL_LIST_RELEVANCE.get(list_name, "secondary")
            rationale = f"{gene} is in '{list_name}' special list for {profile_name}."

            return {
                "tier_suggestion": "assess_via_standard_pipeline",
                "relevance": relevance,
                "rationale": rationale,
                "fast_track": False,
                "action": "Proceed with standard domain + ClinVar + gnomAD assessment.",
                "clinical_note": f"{gene} is {relevance}-relevant to {profile_name} ({list_name} list).",
                "gtex_rpkm": None,
                "source": f"special_list:{list_name}",
            }

    # --- Priority 4: Completely unknown ---
    return {
        "tier_suggestion": "assess_via_standard_pipeline",
        "relevance": "unknown",
        "rationale": f"{gene} not in GTEx or local tissue profile '{profile_name}'.",
        "fast_track": False,
        "action": "Proceed with standard domain + ClinVar + gnomAD assessment. Do NOT fast-track.",
        "clinical_note": "Gene relevance unknown - conservative assessment.",
        "gtex_rpkm": None,
        "source": "unknown",
    }

# =============================================================================
# Module F: Three-Tier Risk Classification
# =============================================================================

TIER1_ACTION_GENES = {
    "VWF": {"reason": "Coagulation disorder - vWD risk in patient", "condition": "ClinVar_Pathogenic"},
}

# v0.5.1 OPT-P0-2: X-linked gene female heterozygous risk adjustment
def _x_linked_female_adjustment(tier: int, chrom: str, gt: str,
                                gene_constraint: Optional[Dict] = None) -> Tuple[int, str]:
    """
    Adjust tier for X-linked genes in female heterozygous carriers.

    Biological basis:
    - Female XX: random X-inactivation (lyonization) ~50% cells express wild-type X
    - If gene is haplosufficient (pLI < 0.5 or LOEUF > 0.35): 50% wild-type sufficient
    - If gene is haploinsufficient (pLI > 0.9): maintain tier

    Returns: (adjusted_tier, reason)
    """
    if chrom not in ('X', 'chrX'):
        return tier, ""
    if gt not in ('0/1', '0|1'):
        return tier, ""

    pLI = 0.0
    loeuf = 1.0
    if gene_constraint:
        pLI = gene_constraint.get("pLI", 0.0) or 0.0
        loeuf = gene_constraint.get("loeuf", 1.0) or 1.0

    is_haplosufficient = (pLI < 0.5) or (loeuf > 0.35)
    is_haploinsufficient = (pLI > 0.9) and (loeuf < 0.35)

    if is_haplosufficient and tier == 1:
        return 2, (f"X-linked female het + haplosufficient "
                   f"(pLI={pLI:.2f}, LOEUF={loeuf:.2f}) - "
                   f"50% wild-type via X-inactivation sufficient")
    elif is_haplosufficient and tier == 2:
        return 3, (f"X-linked female het + haplosufficient - no concern")
    elif is_haploinsufficient:
        return tier, (f"X-linked female het but haploinsufficient "
                      f"(pLI={pLI:.2f}, LOEUF={loeuf:.2f}) - maintaining tier {tier}")
    return tier, ""


# v0.7 Phase 3: Rare disease gene list (from gene_phenotype_map.json)
_RARE_DISEASE_GENES: Optional[set] = None

def _load_rare_disease_genes() -> set:
    """Load rare disease gene list from gene_phenotype_map.json.
    Genes with OMIM/ClinVar phenotypes are considered rare disease-related.
    """
    global _RARE_DISEASE_GENES
    if _RARE_DISEASE_GENES is not None:
        return _RARE_DISEASE_GENES

    map_path = Path(__file__).parent.parent / "references" / "gene_phenotype_map.json"
    try:
        with open(map_path, 'r') as f:
            data = json.load(f)
        _RARE_DISEASE_GENES = set(data.keys())
        return _RARE_DISEASE_GENES
    except Exception:
        _RARE_DISEASE_GENES = set()
        return _RARE_DISEASE_GENES


def _is_rare_disease_gene(gene: str) -> bool:
    """Check if gene is in the rare disease gene list."""
    return gene in _load_rare_disease_genes()


def classify_variant_tier(variant: Variant, domain_info: Dict, tissue_assessment: Dict,
                          gnomad_info: Dict, transcript_warning: Optional[Dict],
                          pseudogene_warning: Optional[Dict], tissue_profile: Dict,
                          config: Optional[GPAConfig] = None) -> Tuple[int, str, List[str]]:
    """
    Three-tier classification with dynamic tissue context.
    v0.4.5: Added somatic_mode support for tumor driver analysis.
    Returns: (tier, reason, actions)
    """
    gene = variant.gene
    actions = []
    # v0.5 P1-9: Initialize evidence chain for structured traceability
    # If variant already has evidence (e.g., from previous analysis or testing), preserve it
    evidence_chain = list(variant.evidence_chain)
    def _add_evidence(source, rule, weight=1.0, confidence="high", raw_data=None):
        evidence_chain.append(Evidence(source=source, rule=rule, weight=weight, confidence=confidence, raw_data=raw_data))

    def _is_unknown(val):
        return val == _UNKNOWN or val == "" or val is None

    def _clinvar_is_conflicting(clinvar):
        """Detect ClinVar conflicting interpretations.
        v0.7.1: Conflicting = pathogenic AND benign/VUS keywords present simultaneously.
        Standard composite ratings like 'Pathogenic/Likely_pathogenic' are NOT conflicting.
        """
        if _is_unknown(clinvar):
            return False
        clinvar_lower = clinvar.lower()
        if "conflicting" in clinvar_lower:
            return True
        pathogenic_keywords = ["pathogenic", "致病", "likely_pathogenic", "可能致病"]
        benign_or_vus_keywords = ["benign", "良性", "likely_benign", "可能良性", "vus", "意义不明", "uncertain"]
        has_pathogenic = any(kw in clinvar_lower for kw in pathogenic_keywords)
        has_benign_or_vus = any(kw in clinvar_lower for kw in benign_or_vus_keywords)
        if has_pathogenic and has_benign_or_vus:
            return True
        if "/" in clinvar and clinvar.count("/") == 1:
            return False
        return False

    def _clinvar_pathogenic(clinvar):
        """ClinVar pathogenic check - UNKNOWN does NOT trigger this.
        v0.5.2: Support both English 'Pathogenic' and Chinese '致病'.
        v0.7.1: Conflicting interpretations return False."""
        if _clinvar_is_conflicting(clinvar):
            return False
        if _is_unknown(clinvar):
            return False
        clinvar_lower = clinvar.lower()
        return ("pathogenic" in clinvar_lower or
                "致病" in clinvar or
                "likely_pathogenic" in clinvar_lower or
                "可能致病" in clinvar)

    def _clinvar_benign(clinvar):
        """ClinVar benign check - UNKNOWN does NOT trigger this.
        v0.5.2: Support both English 'Benign' and Chinese '良性'.
        v0.7.1: Conflicting interpretations return False."""
        if _clinvar_is_conflicting(clinvar):
            return False
        if _is_unknown(clinvar):
            return False
        clinvar_lower = clinvar.lower()
        return (("benign" in clinvar_lower or "良性" in clinvar)
                and "conflicting" not in clinvar_lower)

    def _parse_clinvar_confidence(clnrevstat):
        """v0.7.2: Map ClinVar CLNREVSTAT review status to confidence weight (0.30~0.95).

        ClinVar review status is text, not numeric stars:
            - practice_guideline → 0.95 (★★★★)
            - reviewed_by_expert_panel → 0.80 (★★★☆)
            - multiple_submitters_no_conflict → 0.55 (★★☆☆)
            - single_submitter → 0.40 (★☆☆☆)
            - no_assertion / no_criteria / conflicting / missing → 0.30
        """
        if not clnrevstat:
            return 0.30
        cs = clnrevstat.lower()
        if "practice_guideline" in cs:
            return 0.95
        if "reviewed_by_expert_panel" in cs:
            return 0.80
        if "multiple_submitters" in cs and "noconflict" in cs.replace("_", ""):
            return 0.55
        if "noconflicts" in cs.replace("_", ""):
            return 0.50
        if "single_submitter" in cs:
            return 0.40
        if "conflicting" in cs:
            return 0.30
        if "no_assertion" in cs or "no_criteria" in cs:
            return 0.30
        return 0.30

    # v0.7.2: Pre-compute ClinVar confidence once for this variant
    clinvar_conf = _parse_clinvar_confidence(variant.clinvar_review_status)
    if _clinvar_is_conflicting(variant.clinvar):
        if "CLINVAR_CONFLICTING" not in variant.qc_flags:
            variant.qc_flags.append("CLINVAR_CONFLICTING")
        _add_evidence(
            source="ClinVar",
            rule=f"Conflicting ClinVar interpretation: '{variant.clinvar}' - NOT used for tier upgrade",
            weight=0.0,
            confidence="low",
            raw_data={"clinvar": variant.clinvar},
        )
    if pseudogene_warning:
        pg_score = pseudogene_warning.get("score", 0)
        pg_level = pseudogene_warning.get("level", "unknown")
        pg_conf = "low" if pg_score >= 0.75 else ("moderate" if pg_score >= 0.40 else "high")
        _add_evidence(
            source="PseudogeneDetection",
            rule=f"Pseudogene_{pg_level}_score={pg_score:.2f}",
            weight=0.0,  # Does not affect tier directly
            confidence=pg_conf,
            raw_data=pseudogene_warning,
        )

    def _confidence_from_data():
        """Determine confidence based on data quality."""
        if variant.missing_fields:
            return "low" if len(variant.missing_fields) >= 3 else "moderate"
        if getattr(config, 'offline_mode', False):
            return "low"
        return "high"

    def _calculate_tier_confidence(chain):
        """v0.5 P1-10: Calculate tier confidence based on evidence chain.

        HIGH: >=3 independent high-confidence sources, no conflict.
        MEDIUM: 2 independent sources, or mixed quality, or minor conflict.
        LOW: <=1 source, or conflicting evidence, or many UNKNOWN fields.
        """
        if not chain:
            return "LOW"

        # Count unique high-confidence sources
        unique_sources = set()
        high_conf_count = 0
        has_conflict = False

        for ev in chain:
            if ev.confidence in ("high", "HIGH"):
                unique_sources.add(ev.source)
                high_conf_count += 1

        # Check for conflicting evidence
        clinvar_path = any("ClinVar" in ev.source and "Pathogenic" in ev.rule for ev in chain)
        gnomad_common = any(("gnomAD" in ev.source or "Frequency" in ev.source) and "common" in ev.rule.lower() for ev in chain)
        clinvar_benign = any("ClinVar" in ev.source and "Benign" in ev.rule for ev in chain)

        if (clinvar_path and gnomad_common) or (clinvar_path and clinvar_benign):
            has_conflict = True

        # Check for many UNKNOWN fields
        many_unknown = len(variant.missing_fields) >= 3 if variant.missing_fields else False

        if has_conflict or many_unknown:
            return "LOW"

        # v0.6: Pseudogene interference scoring - does NOT change tier, only confidence
        if pseudogene_warning:
            pg_score = pseudogene_warning.get("score", 0)
            if pg_score >= 0.75:
                return "LOW"  # Strong interference: confidence drops
            elif pg_score >= 0.40:
                return "MEDIUM"  # Suspected interference: confidence downgraded
            elif pg_score > 0:
                return "MEDIUM"  # Minor bias: slight downgrade
            # v0.5.3 legacy fallback (backward compatibility with old-format warnings)
            elif pseudogene_warning.get("type") == "PSEUDOGENE_INTERFERENCE":
                return "LOW"

        # v0.5.3: QC flags force LOW confidence
        if "VAF_GT_MISMATCH" in variant.qc_flags:
            return "LOW"

        if len(unique_sources) >= 3 and high_conf_count >= 3:
            return "HIGH"
        elif len(unique_sources) >= 2:
            return "MEDIUM"
        else:
            return "LOW"

    def _generate_upgrade_conditions(variant, tier, tissue_assessment, gnomad_info):
        """v0.5 P1-11: Generate forward-looking upgrade conditions based on evidence gaps.

        Tier 2 → Tier 1: What would make this variant actionable?
        Tier 3 → Tier 2: What would make this variant worth monitoring?
        Tier 1: No upgrade conditions (already highest tier).
        """
        conditions = []
        gene = variant.gene
        clinvar = variant.clinvar
        impact = variant.impact
        consequence = variant.consequence
        gnomad_status = gnomad_info.get("status", "")
        gnomad_af = gnomad_info.get("af")
        if gnomad_af is not None:
            try:
                gnomad_af = float(gnomad_af)
            except (ValueError, TypeError):
                gnomad_af = None

        if tier == 2:
            # Tier 2 → Tier 1 upgrade paths
            # Condition 1: ClinVar upgrade
            if clinvar and "Pathogenic" not in clinvar and "pathogenic" not in clinvar.lower():
                conditions.append(f"若 ClinVar 收录为 Pathogenic/Likely_pathogenic 则升级为 Tier 1")

            # Condition 2: Functional evidence
            if impact not in ("HIGH", ""):
                conditions.append(f"若功能实验证实 {consequence} 有害(如蛋白稳定性下降)则升级为 Tier 1")

            # Condition 3: Zygosity upgrade
            if variant.gt == "0/1":
                conditions.append(f"若后续验证为纯合变异 (1/1) 且基因对 {tissue_assessment.get('relevance', 'target')} 组织关键则升级为 Tier 1")

            # Condition 4: gnomAD AF near threshold
            if gnomad_af and gnomad_af > 0.001:
                conditions.append(f"若东亚人群 AF < 0.001% 或该位点在患者中富集则升级为 Tier 1")

            # Condition 5: Domain info upgrade
            if not variant.domain_info:
                conditions.append(f"若位于关键功能域或保守残基(如 ATP结合位点)则升级为 Tier 1")

        elif tier == 3:
            # Tier 3 → Tier 2 upgrade paths
            # Condition 1: de novo validation
            conditions.append(f"若后续家系验证为 de novo(非遗传)或患者表型与该基因高度匹配则升级为 Tier 2")

            # Condition 2: ClinVar upgrade from benign
            if clinvar and ("Benign" in clinvar or "benign" in clinvar.lower()):
                conditions.append(f"若 ClinVar 重新评级为 VUS 或以上,或新功能证据出现则升级为 Tier 2")

            # Condition 3: Common polymorphism but in special domain
            if gnomad_status == "common_polymorphism":
                conditions.append(f"若功能域分析显示该位点位于关键结构域或影响剪接则升级为 Tier 2")

            # Condition 4: Missing tissue relevance
            if tissue_assessment.get("relevance") == "none":
                conditions.append(f"若 GTEx 或其他数据显示该基因在 {tissue_assessment.get('relevance', 'target')} 组织中高表达则升级为 Tier 2")

            # Condition 5: Domain info gap
            if not variant.domain_info:
                conditions.append(f"若后续实验证实该变异影响蛋白功能或相互作用则升级为 Tier 2")

        return conditions

    profile_name = tissue_profile.get("display_name", "target tissue")
    tier_rules = tissue_profile.get("tier_rules", {})
    special_lists = tissue_profile.get("special_gene_lists", {})

    # v0.5 P0-7: Helpers for conservative UNKNOWN handling
    def _impact_high(impact):
        """Impact HIGH check - UNKNOWN is treated as HIGH (conservative, no downgrade).
        v0.5.2: TRANSCRIPT_DISCREPANCY with non-coding annotator transcript (NR_/XM_/XR_)
        but canonical protein-coding (ENST/ENSG) → downgrade HIGH to prevent false Tier 1.
        """
        if _is_unknown(impact):
            return True  # Missing impact data → assume worst case

        # v0.5.2: Transcript discrepancy check
        if (transcript_warning and
            transcript_warning.get("type") == "TRANSCRIPT_DISCREPANCY"):
            annotator_tx = transcript_warning.get("annotator_selected", "")
            canonical_tx = transcript_warning.get("canonical", "")
            is_annotator_noncoding = annotator_tx.startswith(("NR_", "XM_", "XR_"))
            is_canonical_protein = canonical_tx.startswith(("ENST", "ENSG"))
            if (is_annotator_noncoding and is_canonical_protein and
                impact == "HIGH"):
                actions.append(f"WARNING: Annotator used non-coding transcript {annotator_tx} "
                              f"but canonical {canonical_tx} is protein-coding. "
                              f"HIGH impact downgraded to MODERATE for tier classification.")
                _add_evidence("TranscriptWarning",
                    f"Non-coding annotator tx {annotator_tx} vs canonical {canonical_tx} → impact downgraded",
                    weight=0.5, confidence="medium",
                    raw_data={"annotator_tx": annotator_tx, "canonical_tx": canonical_tx})
                return False  # Treat as non-HIGH for tier classification

        return impact == "HIGH"

    # Report missing fields in actions
    if variant.missing_fields:
        actions.append(f"Missing fields: {', '.join(variant.missing_fields)} - conservative assessment applied")

    # Priority 0: Fast track for non-relevant tissue genes
    if tissue_assessment.get("fast_track") and tissue_assessment.get("tier_suggestion") == 3:
        if not _clinvar_pathogenic(variant.clinvar):
            _add_evidence("TissueContext", f"FastTrack: GTEx≈0 + non-pathogenic → Tier 3 for {profile_name}", weight=0.3, confidence=_confidence_from_data(), raw_data={"relevance": tissue_assessment.get("relevance"), "gtex_tpm": tissue_assessment.get("gtex_tpm")})
            variant.evidence_chain = evidence_chain
            upgrade_conditions = _generate_upgrade_conditions(variant, 3, tissue_assessment, gnomad_info)
            variant.upgrade_conditions = upgrade_conditions
            variant.tier_confidence = _calculate_tier_confidence(evidence_chain)
            upgrade_conditions = _generate_upgrade_conditions(variant, 3, tissue_assessment, gnomad_info)

            return 3, tissue_assessment["reason"], actions

    # v0.4.5: Somatic mode overrides for tumor driver analysis
    # In somatic mode, tier classification prioritizes driver mutation evidence
    # over germline carrier-state logic
    if hasattr(variant, 'vaf') and variant.vaf is not None and variant.vaf > 0.5:
        # Likely germline polymorphism contamination in somatic sample
        actions.append("VAF > 0.5 suggests germline contamination - verify if intended somatic analysis")
        variant.evidence_chain = evidence_chain
        upgrade_conditions = _generate_upgrade_conditions(variant, 3, tissue_assessment, gnomad_info)
        variant.upgrade_conditions = upgrade_conditions
        variant.tier_confidence = _calculate_tier_confidence(evidence_chain)
        upgrade_conditions = _generate_upgrade_conditions(variant, 3, tissue_assessment, gnomad_info)

        return 3, f"VAF={variant.vaf:.3f} > 0.5 - likely germline polymorphism, not somatic driver", actions

    # Somatic mode Tier 1: Core driver mutations
    if getattr(config, 'somatic_mode', False):
        # 1a. TSG loss-of-function in tissue-relevant gene = Tier 1 (core driver)
        if tissue_assessment.get("relevance") in ["primary", "secondary"] and _impact_high(variant.impact):
            # Check if gene is known TSG (from OncoKB annotation or common TSG list)
            is_tsg = getattr(variant, 'is_tsg', False) or gene in _COMMON_TS_GENES
            if is_tsg:
                reason = f"Somatic TSG loss-of-function: {variant.consequence} in {gene}"
                if domain_info and domain_info.get("domain_integrity") in ["completely_destroyed", "partially_destroyed"]:
                    reason += f", {domain_info['domain']} domain disrupted"
                actions.append("Confirm somatic origin (VAF < 0.5, tumor-normal pair)")
                actions.append("Assess as core leukemic driver - target for MRD monitoring")
                variant.evidence_chain = evidence_chain
                upgrade_conditions = []  # Tier 1: no upgrade
                variant.upgrade_conditions = upgrade_conditions
                variant.tier_confidence = _calculate_tier_confidence(evidence_chain)
                upgrade_conditions = []  # Tier 1: no upgrade possible

                return 1, reason, actions

        # 1b. Oncogene hotspot / functional domain mutation = Tier 1
        is_oncogene = getattr(variant, 'is_oncogene', False)
        oncokb_class = getattr(variant, 'classification', '')
        if is_oncogene or oncokb_class in ("Oncogenic", "Likely Oncogenic"):
            if tissue_assessment.get("relevance") in ["primary", "secondary"]:
                reason = f"Somatic oncogene driver: {gene} {variant.hgvsp or variant.hgvsc}"
                if oncokb_class:
                    reason += f" (OncoKB: {oncokb_class})"
                actions.append("Confirm somatic origin")
                actions.append("Assess as core leukemic driver - potential therapeutic target")
                variant.evidence_chain = evidence_chain
                upgrade_conditions = []  # Tier 1: no upgrade
                variant.upgrade_conditions = upgrade_conditions
                variant.tier_confidence = _calculate_tier_confidence(evidence_chain)
                upgrade_conditions = []  # Tier 1: no upgrade possible

                return 1, reason, actions

        # 1c. Known AML driver genes with HIGH impact = Tier 1
        if gene in _KNOWN_AML_DRIVERS and _impact_high(variant.impact):
            actions.append("Known AML driver gene with truncating mutation")
            actions.append("Assess for therapeutic targeting or MRD monitoring")
            variant.evidence_chain = evidence_chain
            upgrade_conditions = []  # Tier 1: no upgrade
            variant.upgrade_conditions = upgrade_conditions
            variant.tier_confidence = _calculate_tier_confidence(evidence_chain)
            upgrade_conditions = []  # Tier 1: no upgrade possible

            return 1, f"Known AML driver {gene} with {variant.consequence} - core somatic driver", actions

    # Priority 1: Tier 1 checks (germline disease risk logic)
    # 1a. Known high-risk special gene lists with pathogenic variant
    for list_name, gene_list in special_lists.items():
        if gene in gene_list:
            if "coagulation" in list_name.lower() and _clinvar_pathogenic(variant.clinvar):
                # v0.7.2: weight scaled by ClinVar review status confidence
                _add_evidence("ClinVar", f"Pathogenic in coagulation gene {gene} → Tier 1 (review_status={variant.clinvar_review_status}, conf={clinvar_conf:.2f})", weight=1.0*clinvar_conf, confidence="high" if clinvar_conf >= 0.8 else "medium" if clinvar_conf >= 0.5 else "low", raw_data={"clinvar": variant.clinvar, "gene_list": list_name, "review_status": variant.clinvar_review_status, "clinvar_conf": clinvar_conf})
                actions.append("Assess bleeding history and coagulation function")
                actions.append("Consider peripheral blood stem cell over bone marrow if applicable")
                variant.evidence_chain = evidence_chain
                upgrade_conditions = []  # Tier 1: no upgrade
                variant.upgrade_conditions = upgrade_conditions
                variant.tier_confidence = _calculate_tier_confidence(evidence_chain)
                upgrade_conditions = []  # Tier 1: no upgrade possible

                return 1, f"{gene} pathogenic variant in coagulation gene - bleeding risk", actions
            if "fa_dna_repair" in list_name.lower() and _clinvar_pathogenic(variant.clinvar):
                actions.append("Assess if patient has Fanconi anemia phenotype")
                actions.append("Biallelic: high personal health risk; heterozygous: carrier status")
                variant.evidence_chain = evidence_chain
                upgrade_conditions = []  # Tier 1: no upgrade
                variant.upgrade_conditions = upgrade_conditions
                variant.tier_confidence = _calculate_tier_confidence(evidence_chain)
                upgrade_conditions = []  # Tier 1: no upgrade possible

                return 1, f"{gene} pathogenic variant in FA pathway - marrow failure risk", actions

    # 1b. Homozygous truncating in primary tissue gene
    if variant.gt in ["1/1", "1|1"] and _impact_high(variant.impact):
        if tissue_assessment.get("relevance") == "primary":
            _add_evidence("Zygosity", f"Homozygous LOF in primary tissue gene {gene} → Tier 1", weight=1.0, confidence="high", raw_data={"gt": variant.gt, "impact": variant.impact, "relevance": "primary"})
            actions.append("Confirm homozygosity via secondary method")
            actions.append("Assess if phenotype is consistent with expected tissue function")
            variant.evidence_chain = evidence_chain
            upgrade_conditions = []  # Tier 1: no upgrade
            variant.upgrade_conditions = upgrade_conditions
            variant.tier_confidence = _calculate_tier_confidence(evidence_chain)
            upgrade_conditions = []  # Tier 1: no upgrade possible

            return 1, f"Homozygous truncating variant in primary tissue gene {gene}", actions

    # Priority 1c: ClinVar Pathogenic + HIGH impact + primary/secondary tissue
    # v0.5.2 FIX: Heterozygous pathogenic truncating variants in tissue-relevant genes
    # were incorrectly falling to Tier 2. ClinVar Pathogenic + HIGH + relevant tissue
    # should be Tier 1 regardless of zygosity (heterozygous pathogenic = actionable).
    # v0.7 Phase 3: If phenotype_match_score is provided and < 0.6 → Tier 2 (phenotype mismatch)
    if _clinvar_pathogenic(variant.clinvar) and _impact_high(variant.impact):
        if tissue_assessment.get("relevance") in ["primary", "secondary"]:
            # v0.7 Phase 3: Check phenotype match score
            pms = getattr(variant, 'phenotype_match_score', None)
            if pms is not None and pms < 0.6:
                # Phenotype mismatch → Tier 2 (not Tier 3)
                _add_evidence("ClinVar", f"Pathogenic + HIGH + tissue-relevant but phenotype mismatch (score={pms:.2f}) → Tier 2 (review_status={variant.clinvar_review_status}, conf={clinvar_conf:.2f})", weight=0.30*clinvar_conf, confidence="medium" if clinvar_conf >= 0.5 else "low", raw_data={"clinvar": variant.clinvar, "impact": variant.impact, "phenotype_match_score": pms, "review_status": variant.clinvar_review_status, "clinvar_conf": clinvar_conf})
                actions.append("Confirm variant via secondary method")
                actions.append("Assess phenotypic severity and clinical relevance")
                variant.evidence_chain = evidence_chain
                upgrade_conditions = _generate_upgrade_conditions(variant, 2, tissue_assessment, gnomad_info)
                upgrade_conditions.append(f"若表型验证与 {gene} 已知疾病匹配,可升级为 Tier 1")
                variant.upgrade_conditions = upgrade_conditions
                variant.tier_confidence = _calculate_tier_confidence(evidence_chain)
                return 2, f"ClinVar pathogenic {variant.consequence} in tissue-relevant gene {gene} - phenotype mismatch (score={pms:.2f})", actions
            # Phenotype match or no phenotype provided → Tier 1 (original logic)
            _add_evidence("ClinVar", f"Pathogenic + HIGH + tissue-relevant → Tier 1 for {gene} (review_status={variant.clinvar_review_status}, conf={clinvar_conf:.2f})", weight=1.0*clinvar_conf, confidence="high" if clinvar_conf >= 0.8 else "medium" if clinvar_conf >= 0.5 else "low", raw_data={"clinvar": variant.clinvar, "impact": variant.impact, "relevance": tissue_assessment.get("relevance"), "review_status": variant.clinvar_review_status, "clinvar_conf": clinvar_conf})
            actions.append("Confirm variant via secondary method")
            actions.append("Assess phenotypic severity and clinical relevance")
            variant.evidence_chain = evidence_chain
            upgrade_conditions = []
            variant.upgrade_conditions = upgrade_conditions
            variant.tier_confidence = _calculate_tier_confidence(evidence_chain)
            return 1, f"ClinVar pathogenic {variant.consequence} in tissue-relevant gene {gene}", actions

    # v0.5 P1-4 + P1-5: Gene constraint tier adjustment with NMD refinement
    # Only applies to LOF variants in strongly constrained genes
    # Placed BEFORE Priority 2 so that NMD-sensitive LOF-intolerant variants
    # go directly to Tier 1, while NMD-escape variants fall through to Priority 2/3
    constraint_eval = evaluate_gene_constraint(variant)
    if constraint_eval.get("tier_adjustment") == 1:
        # P1-5: Check NMD prediction before applying PVS1
        nmd = variant.nmd_prediction or predict_nmd(variant)
        nmd_status = nmd.get("status", "unknown")

        if nmd_status == "escape":
            # Last exon - NMD escape, PVS1 does NOT apply
            # Do NOT upgrade to Tier 1, continue to Priority 2/3
            pass  # Fall through to Priority 2
        elif nmd_status == "possible_escape":
            # Penultimate exon - possible escape, PVS1 downgraded to PM/PP
            if variant.gt in ["0/1", "0|1"] and _impact_high(variant.impact):
                if tissue_assessment.get("relevance") in ["primary", "secondary"]:
                    reason = f"Heterozygous {variant.consequence} in LOF-intolerant gene {gene}"
                    reason += f" ({constraint_eval['reason']})"
                    reason += " - PVS1_Strong→PM: possible NMD escape in penultimate exon"
                    actions.append(f"Gene constraint: pLI={constraint_eval['pLI']:.2f}, LOEUF={constraint_eval['loeuf']:.2f}")
                    actions.append("Possible NMD escape - PVS1 downgraded to moderate evidence")
                    actions.append("Haploinsufficiency possible but uncertain - consider functional validation")
                    variant.evidence_chain = evidence_chain
                    upgrade_conditions = _generate_upgrade_conditions(variant, 2, tissue_assessment, gnomad_info)
                    variant.upgrade_conditions = upgrade_conditions
                    variant.tier_confidence = _calculate_tier_confidence(evidence_chain)
                    upgrade_conditions = _generate_upgrade_conditions(variant, 2, tissue_assessment, gnomad_info)

                    return 2, reason, actions  # Tier 2, not Tier 1
                else:
                    reason = f"ClinVar pathogenic variant in LOF-intolerant gene {gene}"
                    reason += f" ({constraint_eval['reason']})"
                    reason += " - possible NMD escape, PVS1_Strong→PM"
                    actions.append(f"Gene constraint: pLI={constraint_eval['pLI']:.2f}, LOEUF={constraint_eval['loeuf']:.2f}")
                    actions.append("Possible NMD escape - functional assessment needed")
                    variant.evidence_chain = evidence_chain
                    upgrade_conditions = _generate_upgrade_conditions(variant, 2, tissue_assessment, gnomad_info)
                    variant.upgrade_conditions = upgrade_conditions
                    variant.tier_confidence = _calculate_tier_confidence(evidence_chain)
                    upgrade_conditions = _generate_upgrade_conditions(variant, 2, tissue_assessment, gnomad_info)

                    return 2, reason, actions
        elif nmd_status == "unknown":
            # NMD uncertain - conservative: apply PVS1 but annotate uncertainty
            if variant.gt in ["0/1", "0|1"] and _impact_high(variant.impact):
                if tissue_assessment.get("relevance") in ["primary", "secondary"]:
                    reason = f"Heterozygous {variant.consequence} in LOF-intolerant gene {gene}"
                    reason += f" ({constraint_eval['reason']})"
                    reason += f" - NMD status unknown ({nmd.get('reason', 'assuming sensitive')}), PVS1 applied conservatively"
                    actions.append(f"Gene constraint: pLI={constraint_eval['pLI']:.2f}, LOEUF={constraint_eval['loeuf']:.2f}")
                    actions.append("NMD prediction uncertain - assumed sensitive, functional validation recommended")
                    variant.evidence_chain = evidence_chain
                    upgrade_conditions = []  # Tier 1: no upgrade
                    variant.upgrade_conditions = upgrade_conditions
                    variant.tier_confidence = _calculate_tier_confidence(evidence_chain)
                    upgrade_conditions = []  # Tier 1: no upgrade possible

                    return 1, reason, actions
                else:
                    reason = f"ClinVar pathogenic variant in LOF-intolerant gene {gene}"
                    reason += f" ({constraint_eval['reason']})"
                    reason += " - NMD uncertain, assumed sensitive"
                    actions.append(f"Gene constraint: pLI={constraint_eval['pLI']:.2f}, LOEUF={constraint_eval['loeuf']:.2f}")
                    actions.append("Non-tissue-relevant but LOF-intolerant - patient's own health risk")
                    variant.evidence_chain = evidence_chain
                    upgrade_conditions = _generate_upgrade_conditions(variant, 2, tissue_assessment, gnomad_info)
                    variant.upgrade_conditions = upgrade_conditions
                    variant.tier_confidence = _calculate_tier_confidence(evidence_chain)
                    upgrade_conditions = _generate_upgrade_conditions(variant, 2, tissue_assessment, gnomad_info)

                    return 2, reason, actions
        else:
            # NMD sensitive - classic PVS1 applies
            if variant.gt in ["0/1", "0|1"] and _impact_high(variant.impact):
                if tissue_assessment.get("relevance") in ["primary", "secondary"]:
                    _add_evidence("GeneConstraint", f"LOF-intolerant + NMD-sensitive → Tier 1 (PVS1) for {gene}", weight=0.8, confidence="high", raw_data={"pLI": constraint_eval.get('pLI'), "loeuf": constraint_eval.get('loeuf'), "nmd_status": "sensitive"})
                    reason = f"Heterozygous {variant.consequence} in LOF-intolerant gene {gene}"
                    reason += f" ({constraint_eval['reason']})"
                    reason += " — NMD sensitive, PVS1 fully applicable"
                    actions.append(f"Gene constraint: pLI={constraint_eval['pLI']:.2f}, LOEUF={constraint_eval['loeuf']:.2f}")
                    actions.append("Haploinsufficiency likely — consider functional validation")
                    variant.evidence_chain = evidence_chain
                    upgrade_conditions = []  # Tier 1: no upgrade
                    variant.upgrade_conditions = upgrade_conditions
                    variant.tier_confidence = _calculate_tier_confidence(evidence_chain)
                    upgrade_conditions = []  # Tier 1: no upgrade possible

                    # v0.8.0: SpliceAI downgrade check for HIGH-impact variants ascribed to canonical splice
                    # If SpliceAI delta=0, VEP's HIGH impact call is likely an overcall → downgrade to Tier 2.
                    if getattr(config, 'spliceai_enabled', False) and variant.spliceai_result:
                        sa = variant.spliceai_result
                        if sa.get("source") == "spliceai" and sa.get("delta_score") == 0.0:
                            _add_evidence("SpliceAI", f"SpliceAI delta=0 — no splice change predicted for {variant.consequence}, downgrading from Tier 1", weight=-0.5, confidence="high", raw_data={"delta_score": 0.0, "predicted_impact": "none", "details": sa.get("details")})
                            actions.append("SpliceAI predicts no splice disruption — VEP HIGH may be overcalled; consider RNA-seq validation")
                            variant.evidence_chain = evidence_chain
                            upgrade_conditions = _generate_upgrade_conditions(variant, 2, tissue_assessment, gnomad_info)
                            variant.upgrade_conditions = upgrade_conditions
                            variant.tier_confidence = _calculate_tier_confidence(evidence_chain)
                            return 2, f"SpliceAI delta=0 — no splice change for {gene} {variant.consequence}, downgraded from Tier 1", actions

                    return 1, reason, actions
                else:
                    reason = f"ClinVar pathogenic variant in LOF-intolerant gene {gene}"
                    reason += f" ({constraint_eval['reason']})"
                    reason += " - NMD sensitive, patient's own health risk"
                    actions.append(f"Gene constraint: pLI={constraint_eval['pLI']:.2f}, LOEUF={constraint_eval['loeuf']:.2f}")
                    actions.append("Non-tissue-relevant but LOF-intolerant - assess phenotypic impact")
                    variant.evidence_chain = evidence_chain
                    upgrade_conditions = _generate_upgrade_conditions(variant, 2, tissue_assessment, gnomad_info)
                    variant.upgrade_conditions = upgrade_conditions
                    variant.tier_confidence = _calculate_tier_confidence(evidence_chain)
                    upgrade_conditions = _generate_upgrade_conditions(variant, 2, tissue_assessment, gnomad_info)

                    return 2, reason, actions

    # Priority 2: Tier 2 checks
    # 2a. Primary tissue gene, heterozygous, function affected
    if tissue_assessment.get("relevance") in ["primary", "secondary"] and variant.gt in ["0/1", "0|1"]:
        if _impact_high(variant.impact):
            _add_evidence("TissueRelevance", f"Heterozygous LOF in tissue-relevant {gene} → Tier 2", weight=0.6, confidence=_confidence_from_data(), raw_data={"relevance": tissue_assessment.get("relevance"), "gt": variant.gt, "impact": variant.impact, "domain": domain_info.get("domain") if domain_info else None})
            reason = f"Heterozygous {variant.consequence} in tissue-relevant gene {gene}"
            if domain_info and domain_info.get("domain_integrity") in ["completely_destroyed", "partially_destroyed"]:
                reason += f", {domain_info['domain']} domain disrupted"
            actions.append("Inform patient of carrier status")
            actions.append("Monitor post-intervention recovery/function")
            variant.evidence_chain = evidence_chain
            upgrade_conditions = _generate_upgrade_conditions(variant, 2, tissue_assessment, gnomad_info)
            variant.upgrade_conditions = upgrade_conditions
            variant.tier_confidence = _calculate_tier_confidence(evidence_chain)
            upgrade_conditions = _generate_upgrade_conditions(variant, 2, tissue_assessment, gnomad_info)

            # v0.8.0: SpliceAI downgrade check for HIGH-impact variants ascribed to canonical splice in Tier 2
            if getattr(config, 'spliceai_enabled', False) and variant.spliceai_result:
                sa = variant.spliceai_result
                if sa.get("source") == "spliceai" and sa.get("delta_score") == 0.0:
                    _add_evidence("SpliceAI", f"SpliceAI delta=0 — no splice change predicted for {variant.consequence}, downgrading from Tier 2", weight=-0.5, confidence="high", raw_data={"delta_score": 0.0, "predicted_impact": "none", "details": sa.get("details")})
                    actions.append("SpliceAI predicts no splice disruption — VEP HIGH may be overcalled; consider RNA-seq validation")
                    variant.evidence_chain = evidence_chain
                    upgrade_conditions = _generate_upgrade_conditions(variant, 3, tissue_assessment, gnomad_info)
                    variant.upgrade_conditions = upgrade_conditions
                    variant.tier_confidence = _calculate_tier_confidence(evidence_chain)
                    return 3, f"SpliceAI delta=0 — no splice change for {gene} {variant.consequence}, downgraded from Tier 2", actions

            return 2, reason, actions

        # v0.5 P1-5: Missense stratification (impact is MODERATE, not HIGH)
        if "missense" in variant.consequence.lower():
            missense_eval = evaluate_missense_tier(variant, domain_info, variant.gene_constraint)
            if missense_eval.get("tier_recommendation") == 2:
                reason = f"Heterozygous missense in tissue-relevant gene {gene}"
                reason += f" - {missense_eval['reason']}"
                actions.append("Inform patient of carrier status")
                actions.append("Monitor post-intervention recovery/function")
                variant.evidence_chain = evidence_chain
                upgrade_conditions = _generate_upgrade_conditions(variant, 2, tissue_assessment, gnomad_info)
                variant.upgrade_conditions = upgrade_conditions
                variant.tier_confidence = _calculate_tier_confidence(evidence_chain)
                upgrade_conditions = _generate_upgrade_conditions(variant, 2, tissue_assessment, gnomad_info)

                return 2, reason, actions
            elif missense_eval.get("tier_recommendation") == 3:
                # Missense is tolerated - continue to Priority 3
                pass  # Fall through to Tier 3 logic

    # 2b. Non-primary but ClinVar pathogenic
    if _clinvar_pathogenic(variant.clinvar) and tissue_assessment.get("relevance") == "none":
        # v0.7.2: weight scaled by ClinVar review status confidence
        _add_evidence("ClinVar", f"Pathogenic but non-tissue-relevant {gene} → Tier 2 (review_status={variant.clinvar_review_status}, conf={clinvar_conf:.2f})", weight=0.7*clinvar_conf, confidence="high" if clinvar_conf >= 0.8 else "medium" if clinvar_conf >= 0.5 else "low", raw_data={"clinvar": variant.clinvar, "relevance": "none", "review_status": variant.clinvar_review_status, "clinvar_conf": clinvar_conf})
        actions.append("Inform patient of genetic finding")
        actions.append("Refer for relevant specialist evaluation if indicated")
        variant.evidence_chain = evidence_chain
        upgrade_conditions = _generate_upgrade_conditions(variant, 2, tissue_assessment, gnomad_info)
        variant.upgrade_conditions = upgrade_conditions
        variant.tier_confidence = _calculate_tier_confidence(evidence_chain)
        upgrade_conditions = _generate_upgrade_conditions(variant, 2, tissue_assessment, gnomad_info)

        return 2, f"ClinVar pathogenic variant in {gene} - patient's own health may be affected", actions

    # 2c. Drug metabolism genes (if applicable to this tissue context)
    drug_genes = special_lists.get("drug_metabolism", [])
    if gene in drug_genes:
        actions.append(f"Monitor post-intervention drug levels if relevant medications used")
        variant.evidence_chain = evidence_chain
        upgrade_conditions = _generate_upgrade_conditions(variant, 2, tissue_assessment, gnomad_info)
        variant.upgrade_conditions = upgrade_conditions
        variant.tier_confidence = _calculate_tier_confidence(evidence_chain)
        upgrade_conditions = _generate_upgrade_conditions(variant, 2, tissue_assessment, gnomad_info)

        return 2, f"Drug metabolism variant may affect pharmacokinetics", actions

    # Priority 3: Tier 3 - everything else
    reason_parts = []
    if gnomad_info.get("status") == "common_polymorphism":
        # v0.7 Phase 3: Rare disease genes with AF>1% - do NOT auto Tier 3
        if _is_rare_disease_gene(gene) and not _clinvar_benign(variant.clinvar):
            _add_evidence("Frequency", f"AF>1% but rare disease gene {gene} → Tier 2 (not auto Tier 3)", weight=0.2, confidence="medium", raw_data={"gnomad_status": gnomad_info.get("status"), "af": gnomad_info.get("af"), "gene": gene, "rare_disease": True})
            variant.qc_flags.append("COMMON_POLYMORPHISM_BUT_RARE_DISEASE_GENE")
            actions.append(f"Rare disease gene {gene} with common polymorphism - monitor for phenotype correlation")
            variant.evidence_chain = evidence_chain
            upgrade_conditions = _generate_upgrade_conditions(variant, 2, tissue_assessment, gnomad_info)
            variant.upgrade_conditions = upgrade_conditions
            variant.tier_confidence = _calculate_tier_confidence(evidence_chain)
            return 2, f"Common polymorphism in rare disease gene {gene}", actions
        reason_parts.append(f"Common polymorphism (AF={gnomad_info.get('af')})")
    if _clinvar_benign(variant.clinvar):
        reason_parts.append("ClinVar benign")
        # v0.7.2: Add separate ClinVar benign evidence with negative weight scaled by review status
        _add_evidence("ClinVar", f"ClinVar Benign (review_status={variant.clinvar_review_status}, conf={clinvar_conf:.2f})", weight=-0.5*clinvar_conf, confidence="high" if clinvar_conf >= 0.8 else "medium" if clinvar_conf >= 0.5 else "low", raw_data={"clinvar": variant.clinvar, "review_status": variant.clinvar_review_status, "clinvar_conf": clinvar_conf})
    if tissue_assessment.get("relevance") == "none":
        reason_parts.append("No tissue relevance")

    reason = "; ".join(reason_parts) if reason_parts else "Low risk based on combined assessment"
    _add_evidence("Frequency", f"Common polymorphism / benign / no tissue relevance → Tier 3", weight=0.2, confidence="high", raw_data={"gnomad_status": gnomad_info.get("status"), "clinvar": variant.clinvar, "relevance": tissue_assessment.get("relevance")})

    # v0.8.0: SpliceAI evidence for Tier 3 splice variants (default OFF)
    # If SpliceAI is enabled and pre-computed result exists, evaluate upgrade/downgrade.
    if getattr(config, 'spliceai_enabled', False) and variant.spliceai_result:
        sa = variant.spliceai_result
        source = getattr(sa, 'source', 'unknown')
        if source == "spliceai":
            delta = getattr(sa, 'delta_score', None)
            if delta is not None:
                impact = getattr(sa, 'predicted_impact', 'none')
                if impact == "strong" and delta >= 0.5:
                    # Strong splice prediction for a Tier 3 variant → upgrade to Tier 2
                    _add_evidence("SpliceAI", f"SpliceAI strong (delta={delta:.2f}) for {variant.consequence} -> upgrade to Tier 2", weight=0.8, confidence="high", raw_data={"delta_score": delta, "predicted_impact": impact, "details": getattr(sa, 'raw_response', None)})
                    actions.append("SpliceAI predicts strong splice disruption - confirm via RNA-seq or functional assay")
                    variant.evidence_chain = evidence_chain
                    upgrade_conditions = _generate_upgrade_conditions(variant, 2, tissue_assessment, gnomad_info)
                    variant.upgrade_conditions = upgrade_conditions
                    variant.tier_confidence = _calculate_tier_confidence(evidence_chain)
                    return 2, f"SpliceAI strong splice prediction (delta={delta:.2f}) for {gene} {variant.consequence} - upgraded from Tier 3", actions
                elif impact == "moderate" and delta >= 0.2:
                    _add_evidence("SpliceAI", f"SpliceAI moderate (delta={delta:.2f}) for {variant.consequence}", weight=0.4, confidence="medium", raw_data={"delta_score": delta, "predicted_impact": impact, "details": getattr(sa, 'raw_response', None)})
                elif impact in ("weak", "none") and delta == 0.0:
                    # No predicted splice change - supports VEP overcall, keep Tier 3
                    _add_evidence("SpliceAI", f"SpliceAI delta=0 - no splice change predicted for {variant.consequence}", weight=-0.5, confidence="high", raw_data={"delta_score": delta, "predicted_impact": impact, "details": getattr(sa, 'raw_response', None)})
        elif source == "api_error":
            variant.qc_flags.append("SPLICEAI_API_ERROR")
        elif source == "not_in_db":
            _add_evidence("SpliceAI", "Not in SpliceAI database - no splice prediction available", weight=0.0, confidence="low", raw_data={"source": "not_in_db"})

    # v0.5 P1-11: Generate upgrade conditions before final tier assignment
    upgrade_conditions = _generate_upgrade_conditions(variant, tier=3, tissue_assessment=tissue_assessment, gnomad_info=gnomad_info)
    variant.upgrade_conditions = upgrade_conditions

    variant.evidence_chain = evidence_chain
    upgrade_conditions = _generate_upgrade_conditions(variant, 3, tissue_assessment, gnomad_info)
    variant.upgrade_conditions = upgrade_conditions
    variant.tier_confidence = _calculate_tier_confidence(evidence_chain)
    return 3, reason, []

# v0.5.1 OPT-P1-3: C-terminal truncation severity assessment
def _is_minimal_c_terminal_truncation(hgvsp: Optional[str]) -> bool:
    """
    Assess if a HIGH-impact variant involves minimal C-terminal truncation.
    Such truncations (<5% of protein from C-terminus) are often benign
    due to NMD escape or non-critical tail domains.

    Returns True if the variant appears to be a minimal C-terminal truncation.
    """
    if not hgvsp:
        return False
    hgvsp_str = str(hgvsp)
    import re
    # Match nonsense: p.Glu293Ter
    ter_match = re.search(r'p\.[A-Za-z]+(\d+)Ter', hgvsp_str)
    if ter_match:
        stop_pos = int(ter_match.group(1))
        # Conservative heuristic: stop position >=280 aa is likely near C-terminus
        # for most proteins (median ~400 aa). Combined with ClinVar benign in caller.
        if stop_pos >= 280:
            return True
    # Match frameshift: p.Ile249LeufsTer3
    fs_match = re.search(r'p\.[A-Za-z]+(\d+)[A-Za-z]*fsTer(\d+)', hgvsp_str)
    if fs_match:
        original_pos = int(fs_match.group(1))
        fs_stop_count = int(fs_match.group(2))
        # If frameshift occurs late in protein AND early termination
        # e.g., position >=250 with fsTer within 10 aa -> minimal impact
        if original_pos >= 250 and fs_stop_count <= 10:
            return True
    return False


# =============================================================================
# Multi-hit Gene Detection (v0.5.1 OPT: ClinVar benign + synonymous exclusion)
# =============================================================================

def _variant_has_pathogenic_evidence(v: Variant, gtex_data: Optional[Dict] = None) -> bool:
    """
    Check if a variant has evidence suggesting pathogenicity.
    v0.5 P0-7: UNKNOWN fields treated conservatively - UNKNOWN impact is treated as HIGH,
    UNKNOWN clinvar does not trigger benign exclusion.

    Criteria (OR):
      1. Affects protein domain (has specific domain mapping, not unknown/inter-domain)
         AND gene is expressed in target tissue (GTEx TPM >= 1.0)
      2. ClinVar pathogenic/likely pathogenic or HIGH impact or rare gnomAD (<0.001)
      3. Splice site change (consequence contains 'splice')
    """
    # === OPT-P1-4: Synonymous (LOW) variants NEVER have pathogenic evidence ===
    if v.impact == "LOW":
        cons = str(v.consequence or "").lower()
        if "synonymous" in cons or "同义" in cons:
            return False

    # === OPT-P0-1: ClinVar benign exclusion for LOW/MODERATE impact ===
    clinvar_lower = str(v.clinvar or "").lower()
    is_benign_cv = (("benign" in clinvar_lower and "conflicting" not in clinvar_lower)
                    or "likely_benign" in clinvar_lower)
    if is_benign_cv and v.impact in ("LOW", "MODERATE"):
        return False

    # === OPT-P1-3: Minimal C-terminal truncation + ClinVar benign -> not pathogenic ===
    if v.impact == "HIGH" and is_benign_cv:
        if _is_minimal_c_terminal_truncation(v.hgvsp):
            return False

    # Quick check: splice site changes are always considered
    consequence_lower = str(v.consequence or "").lower()
    if "splice" in consequence_lower:
        return True

    # Check tissue expression for domain relevance
    tissue_tpm = None
    if gtex_data and v.gene in gtex_data:
        tissue_tpm = gtex_data[v.gene].get("median_tpm")

    # 1. Domain impact - only counts if gene is expressed in target tissue
    di = v.domain_info
    if di:
        domain = di.get("domain", "")
        if domain and domain not in ("unknown", "N/A", "inter-domain / unannotated"):
            if tissue_tpm is not None and tissue_tpm < 1.0:
                pass  # Low expression: domain not relevant for this tissue
            else:
                return True

    # 2. Pathogenic evidence
    if v.clinvar and v.clinvar != _UNKNOWN and "pathogenic" in clinvar_lower and "conflicting" not in clinvar_lower:
        return True
    # HIGH impact - but C-terminal truncation + ClinVar benign already filtered above
    if v.impact == "HIGH" or v.impact == _UNKNOWN:
        return True
    if v.gnomad_af is not None and v.gnomad_af < 0.001:
        return True

    # 3. Splice site changes - always considered
    if "splice" in consequence_lower:
        return True

    return False


# =============================================================================
# Phase Analysis (v0.4.5)
# =============================================================================

@dataclass
class PhaseResult:
    phase_status: str       # cis / trans / cis_both / ambiguous / unphased / cis_likely / trans_likely
    confidence: str         # high / medium / low / none
    method: str             # gatk_phased_gt / short_reads_overlap / paired_end / reads_direct / trio_segregation / ld_inference / infeasible_short_reads
    evidence: str           # 详细证据描述
    max_gap_bp: int = 0
    min_gap_bp: int = 0
    n_variants: int = 0


def _parse_gt_field(gt_str: str) -> Dict:
    """解析 VCF GT 字段,返回 {is_phased, allele_0, allele_1}"""
    gt_str = str(gt_str) if gt_str is not None else ""
    if not gt_str or gt_str in ('.', './.', '.|.', 'nan'):
        return {"is_phased": False, "allele_0": -1, "allele_1": -1}

    if '|' in gt_str:
        parts = gt_str.split('|')
        return {"is_phased": True, "allele_0": int(parts[0]), "allele_1": int(parts[1])}
    elif '/' in gt_str:
        parts = gt_str.split('/')
        return {"is_phased": False, "allele_0": int(parts[0]), "allele_1": int(parts[1])}
    else:
        # Single allele (haploid)
        val = int(gt_str)
        return {"is_phased": False, "allele_0": val, "allele_1": val}


def _level1_gatk_phase(variants: List[Variant]) -> Optional[PhaseResult]:
    """Level 1: 基于 GATK phased GT 判断相位"""
    parsed = [_parse_gt_field(v.gt) for v in variants]

    # 检查是否全部 phased
    all_phased = all(p["is_phased"] for p in parsed)
    if not all_phased:
        return None

    hap0_alleles = [p["allele_0"] for p in parsed]
    hap1_alleles = [p["allele_1"] for p in parsed]

    # 情况 1: 所有变异都是 1|1 → 两条单倍型都携带
    if set(hap0_alleles) == {1} and set(hap1_alleles) == {1}:
        return PhaseResult(
            phase_status="cis_both",
            confidence="high",
            method="gatk_phased_gt",
            evidence=f"所有 {len(variants)} 个变异 GT=1|1,GATK local assembly 确认两条单倍型均携带"
        )

    # 情况 2: Hap0 全为 ALT, Hap1 全为 REF → cis(杂合)
    if set(hap0_alleles) == {1} and set(hap1_alleles) == {0}:
        return PhaseResult(
            phase_status="cis",
            confidence="high",
            method="gatk_phased_gt",
            evidence="所有 ALT 等位基因位于同一单倍型 (Hap0),REF 位于另一单倍型"
        )

    # 情况 3: Hap0 全为 REF, Hap1 全为 ALT → cis(对称)
    if set(hap0_alleles) == {0} and set(hap1_alleles) == {1}:
        return PhaseResult(
            phase_status="cis",
            confidence="high",
            method="gatk_phased_gt",
            evidence="所有 ALT 等位基因位于同一单倍型 (Hap1),REF 位于另一单倍型"
        )

    # 情况 4: Hap0 上同时存在 REF 和 ALT → trans
    if 0 in hap0_alleles and 1 in hap0_alleles:
        return PhaseResult(
            phase_status="trans",
            confidence="high",
            method="gatk_phased_gt",
            evidence=f"单倍型 Hap0 上同时存在 REF 和 ALT ({hap0_alleles}),确认 trans 关系"
        )

    # 情况 5: Hap1 上同时存在 REF 和 ALT → trans
    if 0 in hap1_alleles and 1 in hap1_alleles:
        return PhaseResult(
            phase_status="trans",
            confidence="high",
            method="gatk_phased_gt",
            evidence=f"单倍型 Hap1 上同时存在 REF 和 ALT ({hap1_alleles}),确认 trans 关系"
        )

    # 其他情况(如包含缺失 -1)
    return None


def _level2_distance_assessment(variants: List[Variant]) -> Dict:
    """Level 2: 基于变异间距判断相位可行性"""
    positions = sorted([v.pos for v in variants])
    gaps = [positions[i+1] - positions[i] for i in range(len(positions) - 1)]
    max_gap = max(gaps) if gaps else 0
    min_gap = min(gaps) if gaps else 0

    if max_gap < 50:
        return {
            "feasible": True,
            "confidence": "high",
            "method": "short_reads_overlap",
            "evidence": f"间距 {min_gap}-{max_gap}bp,同一 150bp read 必然覆盖所有变异"
        }
    elif max_gap < 150:
        return {
            "feasible": True,
            "confidence": "high",
            "method": "short_reads_overlap_or_paired_end",
            "evidence": f"间距 {min_gap}-{max_gap}bp,同一 read (靠近 3' 端) 或 pair-end 覆盖"
        }
    elif max_gap < 500:
        return {
            "feasible": True,
            "confidence": "medium",
            "method": "paired_end_only",
            "evidence": f"间距 {min_gap}-{max_gap}bp,依赖 pair-end insert size (通常 300-500bp)"
        }
    else:
        return {
            "feasible": False,
            "confidence": "none",
            "method": "infeasible_short_reads",
            "evidence": f"最大间距 {max_gap}bp 超出 short-read 相位范围"
        }


def determine_phase(variants: List[Variant]) -> PhaseResult:
    """
    主函数:分层决策判断 multi-hit 变异的相位关系

    优先级:
    1. GATK phased GT(最可靠)
    2. 间距可行性判断(短 reads 范围评估)
    3. 标记为需进一步验证(trio / 长读长)
    """
    positions = sorted([v.pos for v in variants])
    max_gap = max(positions[i+1] - positions[i] for i in range(len(positions) - 1)) if len(positions) > 1 else 0
    min_gap = min(positions[i+1] - positions[i] for i in range(len(positions) - 1)) if len(positions) > 1 else 0

    # Level 1: GATK Phased GT
    result = _level1_gatk_phase(variants)
    if result:
        result.max_gap_bp = max_gap
        result.min_gap_bp = min_gap
        result.n_variants = len(variants)
        return result

    # Level 2: 间距可行性判断
    distance = _level2_distance_assessment(variants)

    if not distance["feasible"]:
        # 短 reads 不可行
        return PhaseResult(
            phase_status="unphased",
            confidence="none",
            method=distance["method"],
            evidence=f"{distance['evidence']}。建议: trio 测序 或 PacBio/Nanopore 长读长",
            max_gap_bp=max_gap,
            min_gap_bp=min_gap,
            n_variants=len(variants)
        )

    # 间距可行但未 phased
    # 根据间距范围给出 cis 可能性评估
    if distance["method"] == "short_reads_overlap":
        # <50bp: 同一 read 必然覆盖 → 高置信度 cis(如果都是杂合)
        # 但如果是 0/1 (unphased),我们无法确认是 cis 还是 trans
        # 只能标记为"技术上可行,需 reads 分析确认"
        return PhaseResult(
            phase_status="cis_likely" if all(_parse_gt_field(v.gt)["allele_0"] == _parse_gt_field(v.gt)["allele_1"] for v in variants) else "ambiguous",
            confidence="high",
            method=distance["method"],
            evidence=f"{distance['evidence']}。GATK 未输出 phased GT,但物理距离保证 reads 重叠。建议 IGV 验证 reads 直接比对",
            max_gap_bp=max_gap,
            min_gap_bp=min_gap,
            n_variants=len(variants)
        )
    elif distance["method"] == "short_reads_overlap_or_paired_end":
        return PhaseResult(
            phase_status="ambiguous",
            confidence="medium",
            method=distance["method"],
            evidence=f"{distance['evidence']}。短 reads 可能 phase,需 reads 分析或 trio 确认",
            max_gap_bp=max_gap,
            min_gap_bp=min_gap,
            n_variants=len(variants)
        )
    else:  # paired_end_only
        return PhaseResult(
            phase_status="ambiguous",
            confidence="low",
            method=distance["method"],
            evidence=f"{distance['evidence']}。pair-end phase 可靠性低,建议 trio 或长读长",
            max_gap_bp=max_gap,
            min_gap_bp=min_gap,
            n_variants=len(variants)
        )


# =============================================================================
# Multi-hit Gene Detection (v0.4.5: with phase analysis)
# =============================================================================

def detect_multi_hit_genes(variants: List[Variant], gtex_data: Optional[Dict] = None) -> List[Dict]:
    """
    Detect genes with multiple pathogenic variants that may require phase analysis.

    v0.4.5 新增:自动相位分析,基于 GATK GT 格式和变异间距判断 cis/trans

    Only counts variants with evidence of pathogenicity:
      - Domain impact, or
      - ClinVar pathogenic / HIGH impact / rare gnomAD, or
      - Splice site change

    Normal polymorphisms (benign / common / no domain impact) are excluded.
    """
    # Group variants by gene
    gene_variants = {}
    for v in variants:
        gene_variants.setdefault(v.gene, []).append(v)

    multi_hits = []
    for gene, var_list in gene_variants.items():
        # Count only variants with pathogenic evidence
        pathogenic_vars = [v for v in var_list if _variant_has_pathogenic_evidence(v, gtex_data)]

        if len(pathogenic_vars) >= 2:
            # v0.4.5: 相位分析
            phase_result = determine_phase(pathogenic_vars)

            # Collect details for each pathogenic variant
            var_details = []
            for v in pathogenic_vars:
                detail = {
                    "hgvsp": v.hgvsp,
                    "hgvsc": v.hgvsc,
                    "chrom": v.chrom,
                    "pos": v.pos,
                    "impact": v.impact,
                    "clinvar": v.clinvar,
                    "gnomad_af": v.gnomad_af,
                    "consequence": v.consequence,
                }
                if v.domain_info:
                    detail["domain"] = v.domain_info.get("domain")
                    detail["domain_range"] = v.domain_info.get("domain_range")
                var_details.append(detail)

            # v0.4.5: 相位状态临床解读
            phase_clinical = {
                "cis": "两个变异位于同一单倍型 → 另一单倍型正常 → 保留 50% 功能",
                "trans": "两个变异位于不同单倍型 → 复合杂合 → 功能可能完全丧失",
                "cis_both": "两条单倍型均携带变异 → 纯合/复合 → 功能严重受损",
                "ambiguous": "相位关系不确定 → 需进一步验证",
                "unphased": "超出短 reads 相位范围 → 需 trio 或长读长",
                "cis_likely": "高概率 cis,但未 100% 确认 → 建议验证",
                "trans_likely": "高概率 trans,但未 100% 确认 → 建议验证"
            }

            multi_hits.append({
                "gene": gene,
                "variant_count": len(var_list),           # total variants in gene
                "pathogenic_count": len(pathogenic_vars),  # variants with evidence
                "warning": "MULTI_HIT_GENE",
                "pathogenic_variants": var_details,
                "phase_result": {
                    "status": phase_result.phase_status,
                    "confidence": phase_result.confidence,
                    "method": phase_result.method,
                    "evidence": phase_result.evidence,
                    "max_gap_bp": phase_result.max_gap_bp,
                    "min_gap_bp": phase_result.min_gap_bp,
                    "n_variants": phase_result.n_variants
                },
                "phase_clinical_significance": phase_clinical.get(phase_result.phase_status, "未知"),
                "phases": {
                    "cis": "Both variants on same allele → other allele normal → heterozygous function retained",
                    "trans": "Variants on different alleles → compound heterozygous → function may be severely impaired"
                },
                "required_evidence": [
                    "Trio/family segregation analysis",
                    "Long-read sequencing (PacBio/Nanopore)",
                    "Allele-specific expression analysis"
                ],
                "action": "Priority P1: Must confirm phase before final assessment",
                "impact": "If trans: may elevate to Tier 1 regardless of individual variant assessment"
            })

    return multi_hits

# =============================================================================
# Version & Provenance (v0.5 P1-15)
# =============================================================================

def _get_version_info(config: GPAConfig) -> Dict:
    """
    Gather analysis version and provenance metadata.
    v0.5 P1-15: Full version tracking for reproducibility.
    """
    import hashlib
    import subprocess

    version_info = {
        "dgra_version": "0.8.0",
        "analysis_date": datetime.now().isoformat(),
    }

    # Cache version: hash of SQLite cache file
    cache_path = getattr(config, 'cache_db_path', None)
    if cache_path and Path(cache_path).exists():
        try:
            with open(cache_path, 'rb') as f:
                cache_hash = hashlib.sha256(f.read()).hexdigest()[:16]
            version_info["cache_version"] = cache_hash
        except Exception:
            version_info["cache_version"] = "unknown"
    else:
        version_info["cache_version"] = "no_cache"

    # Offline archive: latest file modification time
    if OFFLINE_ARCHIVE_DIR.exists():
        try:
            mtimes = [p.stat().st_mtime for p in OFFLINE_ARCHIVE_DIR.iterdir() if p.is_file()]
            if mtimes:
                latest_mtime = max(mtimes)
                version_info["offline_archive_date"] = datetime.fromtimestamp(latest_mtime).isoformat()
            else:
                version_info["offline_archive_date"] = "empty"
        except Exception:
            version_info["offline_archive_date"] = "unknown"
    else:
        version_info["offline_archive_date"] = "no_archive"

    # Git commit hash of dgra_core.py
    try:
        script_dir = Path(__file__).resolve().parent
        result = subprocess.run(
            ["git", "-C", str(script_dir), "rev-parse", "HEAD"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            version_info["dgra_core_commit"] = result.stdout.strip()[:12]
        else:
            version_info["dgra_core_commit"] = "unknown"
    except Exception:
        version_info["dgra_core_commit"] = "unknown"

    # Database version override (CLI --database-version)
    db_version = getattr(config, 'database_version', None)
    if db_version:
        version_info["database_version"] = db_version

    return version_info

# =============================================================================
# Quality Control Checks (v0.5 P1-13)
# =============================================================================

_REPEATMASKER_DATA = None  # Lazy-loaded cache

def _load_repeatmasker():
    """Load repeatmasker regions from references."""
    global _REPEATMASKER_DATA
    if _REPEATMASKER_DATA is not None:
        return _REPEATMASKER_DATA
    rm_path = Path(__file__).resolve().parent.parent / "references" / "repeatmasker_regions.json"
    if rm_path.exists():
        with open(rm_path, 'r') as f:
            _REPEATMASKER_DATA = json.load(f)
    else:
        _REPEATMASKER_DATA = []
    return _REPEATMASKER_DATA

def _is_in_repeat_region(chrom, pos):
    """Check if position falls within any repeatmasker region."""
    regions = _load_repeatmasker()
    for region in regions:
        if str(region.get("chrom", "")) == str(chrom) and region.get("start", 0) <= pos <= region.get("end", 0):
            return True
    return False

def _run_qc_checks(variants: List[Variant]) -> Dict:
    """
    v0.5 P1-13: Input quality control checks.

    Flags anomalies but does NOT reject analysis - conservative approach.
    Returns QC summary dict for report rendering.
    """
    qc_summary = {
        "total": len(variants),
        "flagged": 0,
        "by_flag": {},
        "flagged_variants": [],
    }

    for v in variants:
        flags = []

        # 1. VAF range check
        if v.vaf is not None and (v.vaf < 0 or v.vaf > 1):
            flags.append("INVALID_VAF")

        # 2. DP depth check
        if v.dp < 10:
            flags.append("LOW_DEPTH")
        elif v.dp >= 10:
            # Check allele support (AD/DP ratio) if AD is available
            # AD not in standard Variant dataclass, skip if unavailable
            pass  # AD field not in core Variant; could be extended later

        # 3. Low complexity / repeat region check
        if _is_in_repeat_region(v.chrom, v.pos):
            flags.append("LOW_COMPLEXITY_REGION")

        # 4. Gene symbol format check (P1-2 HGNC rules)
        gene = v.gene
        if gene:
            # Invalid if starts with digit, too long, or contains illegal chars
            if gene[0].isdigit():
                flags.append("INVALID_GENE_SYMBOL")
            elif len(gene) > 50:
                flags.append("INVALID_GENE_SYMBOL")
            elif not re.match(r'^[A-Za-z][A-Za-z0-9\-]*$', gene):
                flags.append("INVALID_GENE_SYMBOL")

        # v0.5 P1-14: HGNC validation - check transcript_warning for HGNC status
        if v.transcript_warning:
            try:
                tw = json.loads(v.transcript_warning)
                hgnc_warn = tw.get("hgnc_warning", {})
                hgnc_status = hgnc_warn.get("status", "")
                # Withdrawn, not_found, query_failed, or unvalidated_offline = invalid
                if hgnc_status in ("withdrawn", "not_found", "query_failed", "unvalidated_offline"):
                    if "INVALID_GENE_SYMBOL" not in flags:
                        flags.append("INVALID_GENE_SYMBOL")
            except (json.JSONDecodeError, AttributeError):
                pass

        # 5. VAF-GT consistency check (v0.5.3)
        gt_raw = str(v.gt) if v.gt is not None else ""
        if gt_raw in ('.', './.', '.|.', 'nan', 'None', ''):
            gt_raw = ""
        if v.vaf is not None and gt_raw:
            gt = gt_raw.replace("|", "/")
            vaf = v.vaf
            if gt == "0/1":
                if vaf < 0.20 or vaf > 0.80:
                    flags.append("VAF_GT_MISMATCH")
            elif gt == "1/1":
                if vaf < 0.70:
                    flags.append("VAF_GT_MISMATCH")
            elif gt == "0/0":
                if vaf > 0.10:
                    flags.append("VAF_GT_MISMATCH")

        v.qc_flags = flags

        if flags:
            qc_summary["flagged"] += 1
            qc_summary["flagged_variants"].append({
                "gene": v.gene,
                "chrom": v.chrom,
                "pos": v.pos,
                "flags": flags,
            })
            for f in flags:
                qc_summary["by_flag"][f] = qc_summary["by_flag"].get(f, 0) + 1

    return qc_summary

# =============================================================================
# Report Generation
# =============================================================================

def _format_vep_reannotation_note(v: Variant) -> Optional[str]:
    """Format a human-readable VEP reannotation note for report display.

    Returns None if the variant was not VEP-reannotated.
    """
    if not v.transcript_warning:
        return None
    try:
        tw = json.loads(v.transcript_warning)
    except (json.JSONDecodeError, TypeError):
        return None

    vep = tw.get("vep_reannotation")
    if not vep or vep.get("status") != "success":
        return None

    original = vep.get("original", {})
    canonical = vep.get("canonical", {})
    orig_tx = original.get("transcript", "N/A")
    orig_consq = original.get("consequence", "N/A")
    orig_impact = original.get("impact", "N/A")
    new_tx = canonical.get("transcript_id", v.transcript or "N/A")
    new_consq = v.consequence or canonical.get("consequence", "N/A")
    new_impact = v.impact or canonical.get("impact", "N/A")

    note = (
        f"⚠️ 后果已按 canonical transcript ({new_tx}) 重新注释:"
        f"原 {orig_tx} {orig_consq}/{orig_impact} → "
        f"VEP 结果 {new_consq}/{new_impact}"
    )
    return note


def _generate_pseudogene_assessment_section(variants: List[Variant]) -> Optional[str]:
    """
    v0.6: Generate standalone pseudogene interference assessment section.

    Returns Markdown string with:
      - Summary table of all variants with pseudogene warnings
      - Score-based classification (0.0-1.0)
      - Per-gene pseudogene list from lookup
      - Recommendations (Sanger, long-read, etc.)

    Does NOT modify tier - only provides analytical assessment.
    """
    # Collect variants with pseudogene warnings
    pg_variants = []
    for v in variants:
        if v.pseudogene_warning:
            try:
                pw = json.loads(v.pseudogene_warning)
                if pw.get("score", 0) > 0:
                    pg_variants.append((v, pw))
            except (json.JSONDecodeError, TypeError):
                continue

    if not pg_variants:
        return None

    lines = []
    lines.append("## 🧬 假基因干扰评估\n")
    lines.append(f"*基于 v0.6 轻量版假基因数据库({len(_load_pseudogene_lookup())} 个临床相关基因对)*\n")
    lines.append(f"**检测到 {len(pg_variants)} 个变异存在假基因干扰风险**\n\n")

    # Summary table
    lines.append("| 基因 | 位点 | 基因型 | 观察VAF | 预期VAF | 干扰评分 | 等级 | 假基因 | 建议 |\n")
    lines.append("|------|------|--------|---------|---------|----------|------|--------|------|\n")

    # Severity classification
    severity_map = {
        "strong_interference": ("🔴", "高度干扰"),
        "interference": ("🟠", "中度干扰"),
        "suspected": ("🟡", "疑似干扰"),
        "bias_suspected": ("🟡", "疑似偏倚"),
    }

    for v, pw in pg_variants:
        level = pw.get("level", "unknown")
        icon, desc = severity_map.get(level, ("⚪", "未知"))

        pos = f"{v.chrom}:{v.pos}"
        gt = v.gt or "N/A"
        obs_vaf = pw.get("observed_vaf", v.vaf or "N/A")
        exp_vaf = pw.get("expected_vaf", 0.5)
        score = pw.get("score", 0)
        pgs = ", ".join(pw.get("pseudogenes", []))
        rec = pw.get("recommendation", "建议验证")

        # Truncate recommendation for table
        rec_short = rec[:40] + "..." if len(rec) > 40 else rec

        lines.append(f"| {v.gene} | {pos} | {gt} | {obs_vaf} | {exp_vaf} | {score:.2f} | {icon} {desc} | {pgs} | {rec_short} |\n")

    lines.append("\n")

    # Detailed per-variant analysis
    lines.append("### 详细分析\n\n")
    for i, (v, pw) in enumerate(pg_variants, 1):
        level = pw.get("level", "unknown")
        icon, desc = severity_map.get(level, ("⚪", "未知"))

        lines.append(f"**{i}. {v.gene} ({v.chrom}:{v.pos})** {icon} {desc}\n\n")
        lines.append(f"- **变异**: {v.hgvsp or v.hgvsc or 'N/A'}\n")
        lines.append(f"- **基因型**: {v.gt or 'N/A'} | **观察VAF**: {pw.get('observed_vaf', v.vaf)} | **预期VAF**: {pw.get('expected_vaf', 0.5)}\n")
        lines.append(f"- **干扰评分**: {pw.get('score', 0):.2f}/1.0\n")
        lines.append(f"- **检测策略**: {pw.get('strategy', 'vaf_mismatch')}\n")

        pgs = pw.get("pseudogenes", [])
        if pgs:
            lines.append(f"- **相关假基因**: {', '.join(pgs)}\n")
            # Add notes from lookup if available
            lookup = _load_pseudogene_lookup()
            entry = lookup.get(v.gene, {})
            if entry.get("notes"):
                lines.append(f"- **注释**: {entry['notes']}\n")

        lines.append(f"- **建议**: {pw.get('recommendation', '建议验证')}\n")

        # Tier impact note
        lines.append(f"- **分级影响**: 本评估**不直接修改 Tier**,仅下调置信度。当前 Tier {v.tier or 'N/A'},置信度 {v.tier_confidence or 'N/A'}\n")

        lines.append("\n")

    # Overall recommendation
    strong_count = sum(1 for _, pw in pg_variants if pw.get("score", 0) >= 0.75)
    if strong_count > 0:
        lines.append(f"### ⚠️ 重点关注\n\n")
        lines.append(f"检测到 **{strong_count} 个**高度假基因干扰变异(评分≥0.75)。")
        lines.append("强烈建议使用 Sanger 测序或长读长测序验证以下位点:\n\n")
        for v, pw in pg_variants:
            if pw.get("score", 0) >= 0.75:
                lines.append(f"- {v.gene}: {v.chrom}:{v.pos} ({v.hgvsp or v.hgvsc})\n")
        lines.append("\n")

    return "".join(lines)


# =============================================================================
# Phenotype Association Assessment Section (v0.7 Phase 4)
# =============================================================================

def _generate_phenotype_assessment_section(variants: List[Variant]) -> Optional[str]:
    """
    v0.7 Phase 4: Generate standalone phenotype association assessment section.

    Core principle: Only Tier 1/2 variants undergo phenotype association analysis.
    This saves ~95% computation (typically 5-20 variants out of 500).

    Returns Markdown string with:
      - Summary table of all Tier 1/2 variants with phenotype match results
      - Per-variant detailed analysis (score, explanation, matched pairs, known phenotypes)
      - High-score (≥0.75) variants → validation recommendation
      - ClinVar Pathogenic + low match score → explicit mismatch warning
    """
    # Collect Tier 1/2 variants with phenotype data
    pheno_variants = []
    for v in variants:
        if v.tier in (1, 2) and v.phenotype_match_score is not None:
            pheno_variants.append(v)

    if not pheno_variants:
        return None

    lines = []
    lines.append("## 🧬 表型关联评估\n")
    lines.append(f"*仅对 Tier 1/2 变异执行表型关联分析(共 {len(pheno_variants)} 个变异)*\n\n")

    # Summary table
    lines.append("### 汇总表\n\n")
    lines.append("| 基因 | 位点 | 合子型 | VAF | 匹配评分 | 关联等级 | 假基因状态 | 建议 |\n")
    lines.append("|------|------|--------|-----|----------|----------|------------|------|\n")

    for v in pheno_variants:
        pos = f"{v.chrom}:{v.pos}"
        gt = v.gt or "N/A"
        vaf = f"{v.vaf:.3f}" if v.vaf is not None else "N/A"
        score = v.phenotype_match_score

        # Association level
        conf = v.phenotype_match_confidence or "low"
        if score >= 0.75:
            level_icon = "🟢"
            level_text = "高度关联"
        elif score >= 0.40:
            level_icon = "🟡"
            level_text = "中度关联"
        elif score > 0:
            level_icon = "🔴"
            level_text = "低度关联"
        else:
            level_icon = "⚪"
            level_text = "无关联"

        # Pseudogene status
        pg_status = "无"
        if v.pseudogene_warning:
            try:
                pw = json.loads(v.pseudogene_warning)
                if pw.get("score", 0) > 0:
                    pg_level = pw.get("level", "unknown")
                    pg_status = f"{pw.get('score', 0):.2f} ({pg_level})"
            except (json.JSONDecodeError, TypeError):
                pass

        # Recommendation
        if score >= 0.75:
            rec = "✅ 表型高度匹配,建议确认"
        elif score >= 0.40:
            rec = "⚠️ 部分匹配,建议结合临床评估"
        else:
            rec = "⚠️ 表型匹配度低,建议复核"

        lines.append(f"| {v.gene} | {pos} | {gt} | {vaf} | {score:.2f} | {level_icon} {level_text} | {pg_status} | {rec} |\n")

    lines.append("\n")

    # Detailed per-variant analysis
    lines.append("### 逐变异详细分析\n\n")
    for i, v in enumerate(pheno_variants, 1):
        pos = f"{v.chrom}:{v.pos}"
        score = v.phenotype_match_score
        conf = v.phenotype_match_confidence or "low"

        if score >= 0.75:
            level_icon = "🟢"
            level_text = "高度关联"
        elif score >= 0.40:
            level_icon = "🟡"
            level_text = "中度关联"
        elif score > 0:
            level_icon = "🔴"
            level_text = "低度关联"
        else:
            level_icon = "⚪"
            level_text = "无关联"

        lines.append(f"**{i}. {v.gene} ({pos})** {level_icon} {level_text}\n\n")
        lines.append(f"- **变异**: {v.hgvsp or v.hgvsc or 'N/A'}\n")
        lines.append(f"- **表型匹配评分**: {score:.2f}/1.0 (置信度: {conf})\n")

        if v.phenotype_match_explanation:
            lines.append(f"- **匹配解释**: {v.phenotype_match_explanation}\n")

        if v.phenotype_matched_pairs:
            pairs_str = ", ".join([f"'{u}' → '{k}'" for u, k in v.phenotype_matched_pairs[:5]])
            ellipsis = "..." if len(v.phenotype_matched_pairs) > 5 else ""
            lines.append(f"- **匹配对**: {pairs_str}{ellipsis}\n")

        if v.phenotype_known_list:
            known_str = ", ".join(v.phenotype_known_list[:5])
            ellipsis = "..." if len(v.phenotype_known_list) > 5 else ""
            lines.append(f"- **基因已知表型**: {known_str}{ellipsis}\n")

        # ClinVar Pathogenic + low score → explicit warning
        clinvar_is_pathogenic = v.clinvar and any(kw in v.clinvar.lower() for kw in ("pathogenic", "致病"))
        if clinvar_is_pathogenic and score < 0.6:
            lines.append(f"- ⚠️ **ClinVar 致病性提示**: 该变异在 ClinVar 中标注为致病/可能致病,但与输入表型的匹配度较低({score:.2f})。")
            lines.append("建议结合患者具体临床表现进一步验证,不排除该变异与其他未报告表型相关。\n")

        # Tier context
        lines.append(f"- **当前分级**: Tier {v.tier} | 置信度: {v.tier_confidence or 'N/A'}\n")
        lines.append(f"- **分级原因**: {v.tier_reason}\n")

        lines.append("\n")

    # High-score variants validation recommendation
    high_score = [v for v in pheno_variants if v.phenotype_match_score >= 0.75]
    if high_score:
        lines.append("### ⚠️ 高分匹配变异验证建议\n\n")
        lines.append(f"检测到 **{len(high_score)}** 个表型高度匹配变异(评分≥0.75)。")
        lines.append("这些变异与输入的临床表型高度吻合,强烈建议进行验证:\n\n")
        for v in high_score:
            pos = f"{v.chrom}:{v.pos}"
            lines.append(f"- **{v.gene}**: {pos} ({v.hgvsp or v.hgvsc or 'N/A'}) - 评分 {v.phenotype_match_score:.2f}\n")
        lines.append("\n**建议验证方法**:\n")
        lines.append("- Sanger 测序验证\n")
        lines.append("- 长读长测序(如 PacBio / Oxford Nanopore)验证结构变异\n")
        lines.append("- 家系共分离分析(如可获得父母/子女样本)\n")
        lines.append("- 功能实验(如可行)\n\n")

    return "".join(lines)


# =============================================================================
# Report Generation
# =============================================================================

def generate_tier_report(variants: List[Variant], config: GPAConfig,
                        tissue_profile: Dict, multi_hits: List[Dict]) -> str:
    """
    Generate Markdown report with three-tier structure and dynamic tissue context.
    """
    # Sort by tier
    tier1 = [v for v in variants if v.tier == 1]
    tier2 = [v for v in variants if v.tier == 2]
    tier3 = [v for v in variants if v.tier == 3]

    profile_name = tissue_profile.get("display_name", config.tissue_profile)

    report = []
    report.append("# GPA Report - Genomic Phenotype Association v0.7\n")
    report.append(f"**Analysis Context**: {profile_name}\n")
    report.append(f"**Tissue Profile**: `{config.tissue_profile}`\n")
    report.append(f"**Offline Mode**: {'Yes' if config.offline_mode else 'No'}\n")
    report.append(f"**Analysis Date**: {datetime.now().isoformat()}\n")

    # v0.7.1: Variant pre-filtering statistics
    if config.filter_stats:
        fs = config.filter_stats
        report.append(f"**Input Variants**: {fs.get('input_count', '?')} → **Assessed**: {fs.get('output_count', '?')} (excluded: {fs.get('excluded', '?')})\n")
        # Compact impact breakdown
        impact_parts = []
        for imp in ['HIGH', 'MODERATE', 'LOW', 'MODIFIER']:
            cnt = fs.get('by_impact', {}).get(imp, 0)
            if cnt > 0:
                impact_parts.append(f"{imp}: {cnt}")
        if impact_parts:
            report.append(f"**Impact Distribution (input)**: {' | '.join(impact_parts)}\n")
        # Retention details
        retention_parts = []
        if fs.get('splice_retained', 0) > 0:
            retention_parts.append(f"splice retained: {fs['splice_retained']}")
        if fs.get('synonymous_tissue_retained', 0) > 0:
            retention_parts.append(f"synonymous tissue: {fs['synonymous_tissue_retained']}")
        if fs.get('clinvar_conflicting_retained', 0) > 0:
            retention_parts.append(f"ClinVar conflict: {fs['clinvar_conflicting_retained']}")
        if retention_parts:
            report.append(f"**Filter Retention**: {' | '.join(retention_parts)}\n")
        if config.filter_preset:
            report.append(f"**Filter Preset**: `{config.filter_preset}`\n")
    else:
        report.append(f"**Total Variants Assessed**: {len(variants)}\n")

    # v0.5 P1-15: Version and provenance metadata
    version_info = _get_version_info(config)
    report.append(f"**GPA Version**: {version_info.get('dgra_version', '0.5.3')}\n")
    if version_info.get('cache_version'):
        report.append(f"**Cache Version**: {version_info['cache_version']}\n")
    if version_info.get('offline_archive_date') and version_info['offline_archive_date'] not in ('no_archive', 'empty', 'unknown'):
        report.append(f"**Offline Archive Date**: {version_info['offline_archive_date']}\n")
    if version_info.get('dgra_core_commit') and version_info['dgra_core_commit'] != 'unknown':
        report.append(f"**Code Commit**: `{version_info['dgra_core_commit']}`\n")
    if version_info.get('database_version'):
        report.append(f"**Database Version**: {version_info['database_version']}\n")
    report.append("\n")

    report.append(f"**Tier 1 基因**: {len(set(v.gene for v in tier1))} 个 | **Tier 1 突变**: {len(tier1)} 个\n")
    report.append(f"**Tier 2 基因**: {len(set(v.gene for v in tier2))} 个 | **Tier 2 突变**: {len(tier2)} 个\n")
    report.append(f"**Tier 3 基因**: {len(set(v.gene for v in tier3))} 个 | **Tier 3 突变**: {len(tier3)} 个\n\n")

    # v0.5 P1-13: QC summary table
    # Collect QC flags from all variants
    all_qc_flags = []
    for v in variants:
        all_qc_flags.extend(v.qc_flags)

    if all_qc_flags:
        from collections import Counter
        flag_counts = Counter(all_qc_flags)
        report.append("## ⚠️ 输入 QC 异常汇总\n")
        report.append(f"**总异常数**: {len(all_qc_flags)} 条(涉及 {len(set((v.chrom, v.pos) for v in variants if v.qc_flags))} 个变异)\n\n")
        report.append("| QC 标志 | 计数 | 说明 |\n")
        report.append("|---------|------|------|\n")

        flag_descriptions = {
            "INVALID_VAF": "VAF 超出 [0,1] 范围",
            "LOW_DEPTH": "测序深度 < 10x",
            "LOW_COMPLEXITY_REGION": "位于低复杂度/重复区域",
            "INVALID_GENE_SYMBOL": "基因名格式不符合 HGNC 规范",
            "VAF_GT_MISMATCH": "VAF 与基因型不一致(杂合 35-65%,纯合 85-100%,野生型 0-5%)",
        }

        # Show top 5 most frequent flags
        for flag, count in flag_counts.most_common(5):
            desc = flag_descriptions.get(flag, "未知标志")
            report.append(f"| {flag} | {count} | {desc} |\n")

        if len(flag_counts) > 5:
            report.append(f"| ... | ... | 共 {len(flag_counts)} 种异常 |\n")

        # Show first 5 flagged variant details
        flagged = [v for v in variants if v.qc_flags][:5]
        if flagged:
            report.append(f"\n**前 5 条异常变异**:\n")
            report.append("| 位置 | 基因 | 异常标志 |\n")
            report.append("|------|------|----------|\n")
            for v in flagged:
                report.append(f"| {v.chrom}:{v.pos} | {v.gene} | {', '.join(v.qc_flags)} |\n")

        if len([v for v in variants if v.qc_flags]) > 5:
            report.append(f"\n*... 共 {len([v for v in variants if v.qc_flags])} 个变异有异常,详见 JSON 输出*\n")

        report.append("\n")

    # v0.6: Pseudogene interference assessment - independent section
    pseudogene_assessment = _generate_pseudogene_assessment_section(variants)
    if pseudogene_assessment:
        report.append(pseudogene_assessment)
        report.append("\n")

    # Multi-hit warnings
    if multi_hits:
        report.append("## ⚠️ Multi-Hit Gene Warnings\n")
        for mh in multi_hits:
            report.append(f"### {mh['gene']} - {mh['variant_count']} variants detected\n")
            report.append(f"- **Warning**: {mh['warning']}\n")

            # v0.4.5: Phase analysis result
            phase = mh.get('phase_result', {})
            if phase:
                status = phase.get('status', 'unknown')
                confidence = phase.get('confidence', 'unknown')
                method = phase.get('method', 'unknown')
                evidence = phase.get('evidence', 'N/A')
                max_gap = phase.get('max_gap_bp', 'N/A')

                # Phase status emoji
                if status in ('cis', 'cis_both', 'cis_likely'):
                    status_icon = '🟢'  # 相对安全
                elif status == 'trans':
                    status_icon = '🔴'  # 高风险
                elif status == 'ambiguous':
                    status_icon = '🟡'  # 不确定
                elif status == 'unphased':
                    status_icon = '⚪'  # 无法判断
                else:
                    status_icon = '❓'

                report.append(f"\n**相位分析**: {status_icon} **{status.upper()}** (置信度: {confidence})\n")
                report.append(f"- **判定方法**: {method}\n")
                report.append(f"- **间距**: {max_gap}bp\n")
                report.append(f"- **证据**: {evidence}\n")

                # Clinical significance based on phase
                phase_clinical = mh.get('phase_clinical_significance', '')
                if phase_clinical:
                    report.append(f"- **临床意义**: {phase_clinical}\n")

            report.append(f"\n- **Cis hypothesis**: {mh['phases']['cis']}\n")
            report.append(f"- **Trans hypothesis**: {mh['phases']['trans']}\n")
            report.append(f"- **Required evidence**: {', '.join(mh['required_evidence'])}\n")
            report.append(f"- **Action**: {mh['action']}\n\n")

    # v0.7 Phase 4: Phenotype association assessment - independent section
    phenotype_assessment = _generate_phenotype_assessment_section(variants)
    if phenotype_assessment:
        report.append(phenotype_assessment)
        report.append("\n")

    # Tier 1
    if tier1:
        report.append("---\n\n## 🔴 Tier 1: Action Required\n")
        report.append(f"*Variants requiring clinical attention for {profile_name} context*\n\n")

        # v0.5.2: Show gene-level summary first
        tier1_genes = set(v.gene for v in tier1)
        report.append(f"**Tier 1 基因总数**: {len(tier1_genes)} 个\n")
        report.append(f"**Tier 1 突变总数**: {len(tier1)} 个\n\n")

        # List multi-hit genes among Tier 1
        multi_hit_tier1_genes = tier1_genes.intersection(set(mh['gene'] for mh in multi_hits))
        if multi_hit_tier1_genes:
            report.append(f"**其中 Multi-hit 基因** ({len(multi_hit_tier1_genes)} 个): {', '.join(sorted(multi_hit_tier1_genes))}\n")
            report.append(f"*注: Multi-hit 基因因检测到多个变异被标记关注,但各变异保持独立分级*\n\n")

        # Group by gene
        from collections import OrderedDict
        gene_groups = OrderedDict()
        for v in tier1:
            gene_groups.setdefault(v.gene, []).append(v)

        for gene, var_list in gene_groups.items():
            report.append(f"### {gene}")

            # v0.5.2: Gene-level summary with multi-hit indicator
            is_multi_hit = gene in [mh['gene'] for mh in multi_hits]
            if is_multi_hit:
                report.append(f" **[Multi-hit 基因]**")
            report.append(f"\n")

            report.append(f"**基因**: {gene} | **变异数**: {len(var_list)}\n\n")

            # Variant table
            report.append("| # | 染色体位置 | 转录本 | 变异名称 | 功能域 | 合子型 | ClinVar | 基因约束 | 置信度 | 说明 |\n")
            report.append("|---|-----------|--------|---------|--------|--------|---------|----------|--------|------|\n")

            for i, v in enumerate(var_list, 1):
                # Position
                pos = f"{v.chrom}:{v.pos}"

                # Transcript
                tx = v.transcript or "N/A"

                # Variant name
                var_name = v.hgvsp or v.hgvsc or "N/A"

                # Domain
                di = v.domain_info
                if di:
                    domain = f"{di.get('domain', 'N/A')} ({di.get('domain_range', 'N/A')})"
                else:
                    domain = "N/A"

                # Zygosity
                zyg = v.gt or "N/A"

                # ClinVar
                clin = v.clinvar or "N/A"

                # v0.5 P1-4: Gene constraint
                gc_info = ""
                if v.gene_constraint:
                    pLI = v.gene_constraint.get("pLI")
                    loeuf = v.gene_constraint.get("loeuf")
                    parts = []
                    if pLI is not None:
                        parts.append(f"pLI={pLI:.2f}")
                    if loeuf is not None:
                        parts.append(f"LOEUF={loeuf:.2f}")
                    if parts:
                        gc_info = " | ".join(parts)

                # Reason (shortened)
                reason = v.tier_reason[:80] + "..." if len(v.tier_reason) > 80 else v.tier_reason
                reason = reason.replace("|", "/")  # avoid markdown table break

                # v0.5 P1-10: Confidence indicator
                conf = v.tier_confidence or "UNKNOWN"
                conf_icon = "⚠️" if conf == "LOW" else ""

                report.append(f"| {i} | {pos} | {tx} | {var_name} | {domain} | {zyg} | {clin} | {gc_info} | {conf_icon} {conf} | {reason} |\n")

            report.append(f"\n**详细说明**:\n")
            for i, v in enumerate(var_list, 1):
                report.append(f"{i}. **{v.hgvsp or v.hgvsc}** ({v.chrom}:{v.pos}):\n")
                vep_note = _format_vep_reannotation_note(v)
                if vep_note:
                    report.append(f"   - **{vep_note}**\n")
                # v0.5.3: VAF-GT mismatch warning
                if "VAF_GT_MISMATCH" in v.qc_flags:
                    report.append(f"   - ⚠️ **VAF 与基因型不一致**(GT={v.gt}, VAF={v.vaf:.2f}),提示可能存在假基因干扰、CNV 或比对错误\n")
                # v0.5.3: Pseudogene interference warning
                if v.pseudogene_warning:
                    try:
                        pw = json.loads(v.pseudogene_warning)
                        if pw.get("type") == "PSEUDOGENE_INTERFERENCE":
                            report.append(f"   - ⚠️ **假基因干扰**: {pw.get('gene')} 观察 VAF={pw.get('observed_vaf', 'N/A')},远低于预期杂合 0.5,疑似 {', '.join(pw.get('pseudogenes', []))} 假基因读取\n")
                    except (json.JSONDecodeError, TypeError):
                        pass
                report.append(f"   - 影响程度: {v.impact} | 后果: {v.consequence}\n")
                if v.domain_info:
                    di = v.domain_info
                    report.append(f"   - 功能域: {di.get('domain', 'N/A')} {di.get('domain_range', 'N/A')}\n")
                    rp = di.get('relative_position')
                    if isinstance(rp, (int, float)):
                        report.append(f"   - 域内位置: {di.get('position_in_domain', 'N/A')} (相对: {rp:.2f})\n")
                    else:
                        report.append(f"   - 域内位置: {di.get('position_in_domain', 'N/A')} (相对: {rp})\n")
                    report.append(f"   - 损伤评估: {di.get('damage_type', 'N/A')}\n")
                if v.tissue_relevance:
                    tr = v.tissue_relevance
                    report.append(f"   - 组织相关性: {tr.get('relevance', 'N/A')} | GTEx TPM: {tr.get('gtex_tpm', 'N/A')}\n")
                # v0.5 P1-4: Gene constraint
                if v.gene_constraint:
                    gc = v.gene_constraint
                    parts = []
                    if gc.get("pLI") is not None:
                        parts.append(f"pLI={gc['pLI']:.2f}")
                    if gc.get("loeuf") is not None:
                        parts.append(f"LOEUF={gc['loeuf']:.2f}")
                    if gc.get("lof_z") is not None:
                        parts.append(f"lof_z={gc['lof_z']:.2f}")
                    if gc.get("mis_z") is not None:
                        parts.append(f"mis_z={gc['mis_z']:.2f}")
                    if parts:
                        report.append(f"   - 基因约束: {' | '.join(parts)} (来源: {gc.get('source', 'N/A')})\n")
                report.append(f"   - 分级原因: {v.tier_reason}\n")
                # v0.7: Phenotype association
                if v.phenotype_match_score is not None:
                    score = v.phenotype_match_score
                    conf = v.phenotype_match_confidence
                    conf_icon = "🟢" if conf == "high" else "🟡" if conf == "medium" else "🔴"
                    report.append(f"   - **表型关联**: {conf_icon} Score={score:.2f} (置信度: {conf})\n")
                    if v.phenotype_match_explanation:
                        report.append(f"     - 解释: {v.phenotype_match_explanation}\n")
                    if v.phenotype_matched_pairs:
                        pairs_str = ", ".join([f"'{u}'→'{k}'" for u, k in v.phenotype_matched_pairs[:3]])
                        report.append(f"     - 匹配对: {pairs_str}{'...' if len(v.phenotype_matched_pairs) > 3 else ''}\n")
                    if v.phenotype_known_list:
                        known_str = ", ".join(v.phenotype_known_list[:3])
                        report.append(f"     - 基因已知表型: {known_str}{'...' if len(v.phenotype_known_list) > 3 else ''}\n")
                # v0.5 P1-9: Structured evidence chain
                if v.evidence_chain:
                    report.append(f"   - **证据链** ({len(v.evidence_chain)} 条):\n")
                    chain = v.evidence_chain
                    evidence_detail = getattr(config, 'evidence_detail', 'brief')
                    if evidence_detail == 'brief' and len(chain) > 3:
                        chain = chain[:3]
                        report.append(f"     *(brief mode: 显示前 3 条关键证据)*\n")
                    for ev in chain:
                        report.append(f"     - **{ev.source}**: {ev.rule} (权重={ev.weight:.2f}, 置信度={ev.confidence})\n")
                        if evidence_detail == 'full' and ev.raw_data:
                            raw_summary = {k: v for k, v in ev.raw_data.items() if k in ('af', 'tpm', 'pLI', 'loeuf', 'status', 'domain')}
                            if raw_summary:
                                report.append(f"       原始数据: {raw_summary}\n")
                if v.tier_actions:
                    report.append(f"   - 建议措施: {'; '.join(v.tier_actions)}\n")
                # v0.5 P1-11: Upgrade conditions for forward-looking assessment
                if v.upgrade_conditions:
                    report.append(f"   - **升级条件**:\n")
                    for uc in v.upgrade_conditions:
                        report.append(f"     → {uc}\n")
                report.append(f"\n")

    # Tier 2
    if tier2:
        report.append("---\n\n## 🟡 Tier 2: Inform & Monitor\n")
        report.append(f"*Variants of clinical significance for {profile_name} context*\n\n")

        # Group by gene
        from collections import OrderedDict
        gene_groups_t2 = OrderedDict()
        for v in tier2:
            gene_groups_t2.setdefault(v.gene, []).append(v)

        for gene, var_list in gene_groups_t2.items():
            report.append(f"### {gene}\n")
            report.append(f"**基因**: {gene} | **变异数**: {len(var_list)}\n\n")

            # Variant table
            report.append("| # | 染色体位置 | 转录本 | 变异名称 | 功能域 | 合子型 | ClinVar | 基因约束 | 置信度 | 说明 |\n")
            report.append("|---|-----------|--------|---------|--------|--------|---------|----------|--------|------|\n")

            for i, v in enumerate(var_list, 1):
                pos = f"{v.chrom}:{v.pos}"
                tx = v.transcript or "N/A"
                var_name = v.hgvsp or v.hgvsc or "N/A"
                di = v.domain_info
                if di:
                    domain = f"{di.get('domain', 'N/A')} ({di.get('domain_range', 'N/A')})"
                else:
                    domain = "N/A"
                zyg = v.gt or "N/A"
                clin = v.clinvar or "N/A"
                reason = v.tier_reason[:80] + "..." if len(v.tier_reason) > 80 else v.tier_reason
                reason = reason.replace("|", "/")

                # v0.5 P1-4: Gene constraint
                gc_info = ""
                if v.gene_constraint:
                    pLI = v.gene_constraint.get("pLI")
                    loeuf = v.gene_constraint.get("loeuf")
                    parts = []
                    if pLI is not None:
                        parts.append(f"pLI={pLI:.2f}")
                    if loeuf is not None:
                        parts.append(f"LOEUF={loeuf:.2f}")
                    if parts:
                        gc_info = " | ".join(parts)

                # v0.5 P1-10: Confidence indicator
                conf = v.tier_confidence or "UNKNOWN"
                conf_icon = "⚠️" if conf == "LOW" else ""

                report.append(f"| {i} | {pos} | {tx} | {var_name} | {domain} | {zyg} | {clin} | {gc_info} | {conf_icon} {conf} | {reason} |\n")

            report.append(f"\n**详细说明**:\n")
            for i, v in enumerate(var_list, 1):
                report.append(f"{i}. **{v.hgvsp or v.hgvsc}** ({v.chrom}:{v.pos}):\n")
                vep_note = _format_vep_reannotation_note(v)
                if vep_note:
                    report.append(f"   - **{vep_note}**\n")
                # v0.5.3: VAF-GT mismatch warning
                if "VAF_GT_MISMATCH" in v.qc_flags:
                    report.append(f"   - ⚠️ **VAF 与基因型不一致**(GT={v.gt}, VAF={v.vaf:.2f}),提示可能存在假基因干扰、CNV 或比对错误\n")
                # v0.5.3: Pseudogene interference warning
                if v.pseudogene_warning:
                    try:
                        pw = json.loads(v.pseudogene_warning)
                        if pw.get("type") == "PSEUDOGENE_INTERFERENCE":
                            report.append(f"   - ⚠️ **假基因干扰**: {pw.get('gene')} 观察 VAF={pw.get('observed_vaf', 'N/A')},远低于预期杂合 0.5,疑似 {', '.join(pw.get('pseudogenes', []))} 假基因读取\n")
                    except (json.JSONDecodeError, TypeError):
                        pass
                report.append(f"   - 影响程度: {v.impact} | 后果: {v.consequence}\n")
                if v.domain_info:
                    di = v.domain_info
                    report.append(f"   - 功能域: {di.get('domain', 'N/A')} {di.get('domain_range', 'N/A')}\n")
                    rp = di.get('relative_position')
                    if isinstance(rp, (int, float)):
                        report.append(f"   - 域内位置: {di.get('position_in_domain', 'N/A')} (相对: {rp:.2f})\n")
                    else:
                        report.append(f"   - 域内位置: {di.get('position_in_domain', 'N/A')} (相对: {rp})\n")
                    report.append(f"   - 损伤评估: {di.get('damage_type', 'N/A')}\n")
                if v.tissue_relevance:
                    tr = v.tissue_relevance
                    report.append(f"   - 组织相关性: {tr.get('relevance', 'N/A')} | GTEx TPM: {tr.get('gtex_tpm', 'N/A')}\n")
                # v0.5 P1-4: Gene constraint
                if v.gene_constraint:
                    gc = v.gene_constraint
                    parts = []
                    if gc.get("pLI") is not None:
                        parts.append(f"pLI={gc['pLI']:.2f}")
                    if gc.get("loeuf") is not None:
                        parts.append(f"LOEUF={gc['loeuf']:.2f}")
                    if gc.get("lof_z") is not None:
                        parts.append(f"lof_z={gc['lof_z']:.2f}")
                    if gc.get("mis_z") is not None:
                        parts.append(f"mis_z={gc['mis_z']:.2f}")
                    if parts:
                        report.append(f"   - 基因约束: {' | '.join(parts)} (来源: {gc.get('source', 'N/A')})\n")
                report.append(f"   - 分级原因: {v.tier_reason}\n")
                # v0.7: Phenotype association
                if v.phenotype_match_score is not None:
                    score = v.phenotype_match_score
                    conf = v.phenotype_match_confidence
                    conf_icon = "🟢" if conf == "high" else "🟡" if conf == "medium" else "🔴"
                    report.append(f"   - **表型关联**: {conf_icon} Score={score:.2f} (置信度: {conf})\n")
                    if v.phenotype_match_explanation:
                        report.append(f"     - 解释: {v.phenotype_match_explanation}\n")
                    if v.phenotype_matched_pairs:
                        pairs_str = ", ".join([f"'{u}'→'{k}'" for u, k in v.phenotype_matched_pairs[:3]])
                        report.append(f"     - 匹配对: {pairs_str}{'...' if len(v.phenotype_matched_pairs) > 3 else ''}\n")
                    if v.phenotype_known_list:
                        known_str = ", ".join(v.phenotype_known_list[:3])
                        report.append(f"     - 基因已知表型: {known_str}{'...' if len(v.phenotype_known_list) > 3 else ''}\n")
                if v.tier_actions:
                    report.append(f"   - 建议措施: {'; '.join(v.tier_actions)}\n")
                # v0.5 P1-11: Upgrade conditions for forward-looking assessment
                if v.upgrade_conditions:
                    report.append(f"   - **升级条件**:\n")
                    for uc in v.upgrade_conditions:
                        report.append(f"     → {uc}\n")
                report.append(f"\n")

    # Tier 3
    if tier3:
        report.append("---\n\n## 🟢 Tier 3: No Concern\n")
        report.append(f"*Variants with no {profile_name} relevance*\n\n")

        # Group by gene
        gene_groups_t3 = {}
        for v in tier3:
            gene_groups_t3.setdefault(v.gene, []).append(v)

        for gene, var_list in gene_groups_t3.items():
            if len(var_list) <= 3:
                # Short list: inline table
                report.append(f"**{gene}** ({len(var_list)} variants):\n")
                report.append("| 位置 | 变异 | 功能域 | 置信度 | 原因 |\n")
                report.append("|------|------|--------|--------|------|\n")
                for v in var_list:
                    pos = f"{v.chrom}:{v.pos}"
                    var_name = v.hgvsp or v.hgvsc or "N/A"
                    di = v.domain_info
                    domain = f"{di.get('domain', 'N/A')}" if di else "N/A"
                    # v0.5 P1-10: Confidence
                    conf = v.tier_confidence or "UNKNOWN"
                    conf_icon = "⚠️" if conf == "LOW" else ""
                    reason = v.tier_reason[:50] + "..." if len(v.tier_reason) > 50 else v.tier_reason
                    reason = reason.replace("|", "/")
                    # v0.5.2: VEP reannotation note in table
                    vep_note = _format_vep_reannotation_note(v)
                    if vep_note:
                        reason = f"⚠️ VEP reannotated | {reason}"
                    report.append(f"| {pos} | {var_name} | {domain} | {conf_icon} {conf} | {reason} |\n")
                report.append(f"\n")
                # v0.5.2: VEP reannotation detail for Tier 3 short-list
                for v in var_list:
                    vep_note = _format_vep_reannotation_note(v)
                    if vep_note:
                        report.append(f"   *{v.hgvsp or v.hgvsc}*: {vep_note}\n")
                report.append(f"\n")
            else:
                # Many variants: just count
                report.append(f"**{gene}**: {len(var_list)} variants - 详见原始数据\n\n")

            # v0.5 P1-11: Show upgrade conditions for Tier 3 short-list genes
            if len(var_list) <= 3:
                for v in var_list:
                    if v.upgrade_conditions:
                        report.append(f"   *{v.hgvsp or v.hgvsc} 升级条件*: {' / '.join(v.upgrade_conditions[:2])}\n")
                report.append(f"\n")

    # Methodology
    report.append("---\n\n## 方法学附录\n")
    report.append(f"### 分析背景: {profile_name}\n")
    report.append(f"- **GTEx 参考组织**: {tissue_profile.get('gtex_tissue', 'N/A')}\n")
    report.append(f"- **快速排除规则**: {tissue_profile.get('fast_track_rule', 'N/A')}\n\n")
    report.append("### 分析流程\n")
    report.append("1. **转录本校正**: Ensembl REST API → canonical transcript → 本地回退\n")
    report.append("2. **假基因检测**: VAF 偏差分析识别已知假基因对\n")
    report.append("3. **gnomAD 整合**: AF>1% 常见; AF<0.1% 罕见; NOT_CAPTURED 明确标注\n")
    report.append("4. **蛋白功能域映射**: UniProt REST API → DOMAIN/REGION 特征 → 本地回退\n")
    report.append("5. **组织相关性评估**: GTEx API → median TPM → 自动分级 + 本地回退\n")
    report.append("6. **表型关联分析** (v0.7): LLM 语义匹配 → 基因已知表型 vs 用户输入表型 → 仅 Tier 1/2 执行\n")
    report.append("7. **三级分类**: Action (Tier 1) → Inform (Tier 2) → No concern (Tier 3)\n")
    report.append("8. **基因检测历史记录**: 保留变异信息用于后续分析\n")
    report.append("9. **缓存**: 所有 API 响应缓存 30 天 (SQLite); 离线模式仅用缓存\n")

    return "\n".join(report)

# =============================================================================
# JSON Structured Report Generation (v0.5 P1-12)
# =============================================================================

def generate_json_report(variants: List[Variant], config: GPAConfig,
                         tissue_profile: Dict, multi_hits: List[Dict],
                         report_md: str,
                         qc_summary: Optional[Dict] = None) -> Dict:
    """
    Generate structured JSON report for downstream system consumption.
    v0.5 P1-12: Complete structured output alongside Markdown report.
    """
    profile_name = tissue_profile.get("display_name", config.tissue_profile)

    # Meta section - v0.5 P1-15: include full version metadata
    meta = {
        "dgra_version": "0.7.0",
        "analysis_date": datetime.now().isoformat(),
        "input_format": "vcf",
        "tissue_profile": config.tissue_profile,
        "target_population": getattr(config, 'target_population', None),
        "scoring_model": "weighted",
        "evidence_detail": getattr(config, 'evidence_detail', 'brief'),
        "offline_mode": config.offline_mode,
        "somatic_mode": config.somatic_mode,
        "multi_organ_profiles": config.multi_organ_profiles,
    }
    # Merge version/provenance info (P1-15)
    meta.update(_get_version_info(config))

    # Summary section - v0.5.2: gene-level and variant-level counts
    tier1_genes = set(v.gene for v in variants if v.tier == 1)
    tier2_genes = set(v.gene for v in variants if v.tier == 2)
    tier3_genes = set(v.gene for v in variants if v.tier == 3)
    summary = {
        "total_variants": len(variants),
        "tier1_gene_count": len(tier1_genes),
        "tier1_variant_count": len([v for v in variants if v.tier == 1]),
        "tier2_gene_count": len(tier2_genes),
        "tier2_variant_count": len([v for v in variants if v.tier == 2]),
        "tier3_gene_count": len(tier3_genes),
        "tier3_variant_count": len([v for v in variants if v.tier == 3]),
        "multi_hit_genes": [mh["gene"] for mh in multi_hits],
    }

    # Variants array - structured per variant
    variants_json = []
    for v in variants:
        # Build evidence chain JSON
        evidence_chain = []
        for ev in v.evidence_chain:
            evidence_chain.append({
                "source": ev.source,
                "rule": ev.rule,
                "weight": ev.weight,
                "confidence": ev.confidence,
                "raw_data": ev.raw_data,
            })

        # Build gnomAD section
        gnomad_section = {
            "overall_af": v.gnomad_af,
            "popmax_af": None,
            "eas_af": None,
        }
        if v.gnomad_populations:
            for pop_code, pop_data in v.gnomad_populations.items():
                if pop_code == "EAS":
                    gnomad_section["eas_af"] = pop_data.get("af")
                # Track popmax
                pop_af = pop_data.get("af")
                if pop_af is not None:
                    current_max = gnomad_section["popmax_af"] or 0
                    if pop_af > current_max:
                        gnomad_section["popmax_af"] = pop_af

        # Build GTEx section
        gtex_section = {"tissue": None, "tpm_median": None}
        if v.tissue_relevance:
            gtex_section["tissue"] = v.tissue_relevance.get("gtex_tissue")
            gtex_section["tpm_median"] = v.tissue_relevance.get("gtex_tpm")

        # Build NMD prediction
        nmd_section = {"status": "not_applicable"}
        if v.gene_constraint and "nmd_prediction" in v.gene_constraint:
            nmd_section = v.gene_constraint["nmd_prediction"]

        # Build ClinVar section
        clinvar_section = {
            "clinical_significance": v.clinvar if v.clinvar != _UNKNOWN else None,
            "review_status": None,
        }

        variant_json = {
            "gene": v.gene,
            "gene_original": v.gene_original or v.gene,
            "chrom": v.chrom,
            "pos": v.pos,
            "ref": v.ref,
            "alt": v.alt,
            "hgvsc": v.hgvsc or None,
            "hgvsp": v.hgvsp or None,
            "transcript": v.transcript or None,
            "exon": v.exon or None,
            "impact": v.impact if v.impact != _UNKNOWN else None,
            "consequence": v.consequence if v.consequence != _UNKNOWN else None,
            "zygosity": v.gt or None,
            "vaf": v.vaf,
            "dp": v.dp,
            "gq": v.gq,
            "tier": v.tier,
            "tier_confidence": v.tier_confidence,
            "tier_reason": v.tier_reason or None,
            "tier_actions": v.tier_actions,
            "evidence_chain": evidence_chain,
            "upgrade_conditions": v.upgrade_conditions,
            "gene_constraint": v.gene_constraint,
            "clinvar": clinvar_section,
            "gnomAD": gnomad_section,
            "gtex": gtex_section,
            "nmd_prediction": nmd_section,
            "domain_info": v.domain_info,
            "tissue_relevance": v.tissue_relevance,
            "quality_confidence": v.quality_confidence,
            "missing_fields": v.missing_fields,
            "pseudogene_warning": json.loads(v.pseudogene_warning) if v.pseudogene_warning else None,
            "transcript_warning": json.loads(v.transcript_warning) if v.transcript_warning else None,
        }
        variants_json.append(variant_json)

    # v0.7 Phase 4: Phenotype association data for JSON output
    phenotype_data = []
    pheno_variants = [v for v in variants if v.tier in (1, 2) and v.phenotype_match_score is not None]
    for v in pheno_variants:
        phenotype_data.append({
            "gene": v.gene,
            "chrom": v.chrom,
            "pos": v.pos,
            "ref": v.ref,
            "alt": v.alt,
            "hgvsp": v.hgvsp or None,
            "hgvsc": v.hgvsc or None,
            "tier": v.tier,
            "phenotype_match_score": v.phenotype_match_score,
            "phenotype_match_confidence": v.phenotype_match_confidence or None,
            "phenotype_match_explanation": v.phenotype_match_explanation or None,
            "phenotype_matched_pairs": v.phenotype_matched_pairs,
            "phenotype_known_list": v.phenotype_known_list,
        })

    phenotype_association = {
        "total_tier12_with_phenotype": len(pheno_variants),
        "high_match_count": len([v for v in pheno_variants if v.phenotype_match_score >= 0.75]),
        "variants": phenotype_data,
    }

    # Assemble final JSON
    json_report = {
        "meta": meta,
        "summary": summary,
        "variants": variants_json,
        "multi_hit_details": multi_hits,
        "qc_summary": qc_summary,  # v0.5 P1-13: input QC flags
        "phenotype_association": phenotype_association,
        "report_md": report_md,
    }

    return json_report

# =============================================================================
# Main Pipeline  (v0.4: async + batch API queries)
# =============================================================================

async def run_dgra_pipeline(variants_data: List[Dict],
                      user_phenotypes: Optional[str] = None,
                      config: Optional[GPAConfig] = None) -> Dict:
    """
    Main GPA analysis pipeline with dynamic tissue context.
    v0.4: Async, batch API queries with cache.
    v0.7: Optional phenotype association for Tier 1/2 variants.

    Args:
        variants_data: List of variant dicts from VCF annotation
        user_phenotypes: Optional clinical phenotype description (e.g., "肌无力、肌源性损害")
        config: GPA configuration (includes tissue_profile + offline_mode)

    Returns:
        Dict with report and structured results
    """
    if config is None:
        config = GPAConfig()

    # Convert user config to global config
    global_config = config.to_global()

    # Load tissue profile (keeps tier_rules + special_gene_lists)
    tissue_profile = config.get_tissue_profile()
    profile_name = tissue_profile.get("display_name", config.tissue_profile)

    # Parse variants
    variants = []
    for vd in variants_data:
        # P0-7: Conservative missing field handling
        # Detect which critical fields are missing/empty and record them.
        missing = []

        raw_impact = str(vd.get("IMPACT", "")).strip()
        # v0.7.1: Chinese impact mapping
        _IMPACT_CN_MAP = {"高": "HIGH", "中等": "MODERATE", "低": "LOW", "修饰": "MODIFIER"}
        if raw_impact in _IMPACT_CN_MAP:
            raw_impact = _IMPACT_CN_MAP[raw_impact]
        if not raw_impact:
            raw_impact = _UNKNOWN
            missing.append("IMPACT")

        raw_consequence = str(vd.get("Consequence", "")).strip()
        # v0.7.1: Chinese consequence mapping
        _CONSEQUENCE_CN_MAP = {
            "错义变异": "missense_variant",
            "无义变异": "stop_gained",
            "获得终止密码子": "stop_gained",
            "移码变异": "frameshift_variant",
            "框内插入": "inframe_insertion",
            "剪接位点变异": "splice_donor_variant",
            "剪接区域变异": "splice_region_variant",
            "剪接供体区域变异": "splice_donor_variant",
            "剪接供体第5位碱基变异": "splice_donor_variant",
            "剪接多嘧啶束变异": "splice_polypyrimidine_tract_variant",
            "内含子变异": "intron_variant",
            "基因上游变异": "upstream_gene_variant",
            "基因下游变异": "downstream_gene_variant",
            "同义变异": "synonymous_variant",
            "非翻译区变异": "UTR_variant",
            "3'非翻译区变异": "3_prime_UTR_variant",
            "5'非翻译区变异": "5_prime_UTR_variant",
            "非编码转录本外显子变异": "non_coding_transcript_exon_variant",
        }
        if raw_consequence in _CONSEQUENCE_CN_MAP:
            raw_consequence = _CONSEQUENCE_CN_MAP[raw_consequence]
        if not raw_consequence:
            raw_consequence = _UNKNOWN
            missing.append("Consequence")

        raw_clinvar = str(vd.get("CLIN_SIG", "")).strip()
        if not raw_clinvar:
            raw_clinvar = _UNKNOWN
            missing.append("CLIN_SIG")

        # v0.7.2: ClinVar review status (CLNREVSTAT)
        raw_clinvar_review = str(vd.get("CLNREVSTAT", "")).strip()
        if not raw_clinvar_review or raw_clinvar_review == "nan":
            raw_clinvar_review = None

        raw_dp = str(vd.get("DP", "")).strip()
        try:
            dp_val = int(float(raw_dp)) if raw_dp and raw_dp != _UNKNOWN else 0
        except ValueError:
            dp_val = 0
        if not raw_dp:
            missing.append("DP")

        raw_gq = str(vd.get("GQ", "")).strip()
        gq_val = float(raw_gq) if raw_gq and raw_gq != _UNKNOWN else 0.0
        if not raw_gq:
            missing.append("GQ")

        raw_vaf = str(vd.get("VAF", "")).strip()
        vaf_val = float(raw_vaf) if raw_vaf else None
        if not raw_vaf:
            missing.append("VAF")

        raw_gnomad = str(vd.get("gnomAD_AF", "")).strip()
        gnomad_val = float(raw_gnomad) if raw_gnomad and raw_gnomad != "N/A" else None
        if not raw_gnomad:
            missing.append("gnomAD_AF")

        # Determine quality confidence
        quality_confidence = "high"
        if missing:
            n_critical = sum(1 for f in missing if f in ("IMPACT", "Consequence", "VAF", "CLIN_SIG"))
            if n_critical >= 3:
                quality_confidence = "unknown"
            elif n_critical >= 1:
                quality_confidence = "low"
            else:
                quality_confidence = "medium"

        v = Variant(
            chrom=vd.get("CHROM", ""),
            pos=int(vd.get("POS", 0)),
            ref=vd.get("REF", ""),
            alt=vd.get("ALT", ""),
            gene=vd.get("GENE", ""),
            transcript=vd.get("Feature", ""),
            exon=vd.get("EXON", ""),
            impact=raw_impact,
            consequence=raw_consequence,
            hgvsp=vd.get("HGVSp", ""),
            hgvsc=vd.get("HGVSc", ""),
            clinvar=raw_clinvar,
            dp=dp_val,
            gq=gq_val,
            gt=vd.get("GT", ""),
            vaf=vaf_val,
            gnomad_af=gnomad_val,
            # v0.4.5: somatic annotation fields
            classification=vd.get("classification", ""),
            is_tsg=vd.get("is_tsg", "") == "Yes" or vd.get("is_tsg", False) == True,
            is_oncogene=vd.get("is_oncogene", "") == "Yes" or vd.get("is_oncogene", False) == True,
            # v0.7.2: ClinVar review status
            clinvar_review_status=raw_clinvar_review,
            # v0.5 P0-7
            quality_confidence=quality_confidence,
            missing_fields=missing,
        )
        variants.append(v)

    # Collect all unique genes for batch API queries
    unique_genes = list({v.gene for v in variants})
    print(f"[GPA] {len(variants)} variants across {len(unique_genes)} unique genes")
    print(f"[GPA] Tissue profile: {profile_name} | Offline: {config.offline_mode}")

    # ------------------------------------------------------------------
    # Batch API queries (concurrent)
    # ------------------------------------------------------------------
    ensembl_data = {}
    uniprot_data = {}
    gtex_data = {}
    hgnc_data = {}
    gnomad_constraint_data = {}

    if not config.offline_mode and unique_genes:
        cache = DGRACache(global_config.cache_db_path)
        async with DGRAAPIClient(global_config, cache) as client:
            # v0.5 P1-6: Multi-tissue GTEx aggregation
            gtex_tissues = tissue_profile.get("gtex_tissues")
            gtex_single_tissue = tissue_profile.get("gtex_tissue")

            if gtex_tissues and len(gtex_tissues) > 1:
                # Multi-tissue query
                gtex_raw = await client.batch_query_genes(
                    unique_genes, "gtex_multi",
                    tissues=gtex_tissues
                )
                # Aggregate multi-tissue results
                gtex_data = {}
                for gene in unique_genes:
                    multi_result = gtex_raw.get(gene, [])
                    if isinstance(multi_result, list) and multi_result:
                        gtex_data[gene] = aggregate_gtex_expression(multi_result)
                    else:
                        gtex_data[gene] = multi_result if isinstance(multi_result, dict) else {}
                print(f"[GPA] GTEx multi-tissue query: {len(gtex_tissues)} tissues ({', '.join(gtex_tissues)})")
            else:
                # Single tissue query (backward compatible)
                gtex_raw = await client.batch_query_genes(
                    unique_genes, "gtex",
                    tissue=gtex_single_tissue or "Whole Blood"
                )
                gtex_data = {g: gtex_raw.get(g, {}) for g in unique_genes}

            # Batch query other APIs concurrently with GTEx
            ensembl_raw, uniprot_raw, hgnc_raw, gnomad_constraint_raw = await asyncio.gather(
                client.batch_query_genes(unique_genes, "ensembl"),
                client.batch_query_genes(unique_genes, "uniprot"),
                client.batch_query_genes(unique_genes, "hgnc"),
                client.batch_query_genes(unique_genes, "gnomad_constraint"),
            )
            ensembl_data = {g: ensembl_raw.get(g, {}) for g in unique_genes}
            uniprot_data = {g: uniprot_raw.get(g, {}) for g in unique_genes}
            hgnc_data = {g: hgnc_raw.get(g, {}) for g in unique_genes}
            gnomad_constraint_data = {g: gnomad_constraint_raw.get(g, {}) for g in unique_genes}
        # v0.8.0 P6: gnomAD variant frequency batch query for variants missing AF data
        # This fixes the disconnect where query_gnomad_variant() was implemented
        # but never called — all frequency-based tiering was effectively disabled.
        variants_without_af = [v for v in variants if v.gnomad_af is None and v.chrom and v.pos and v.ref and v.alt]
        if variants_without_af:
            print(f"[GPA] gnomAD: querying {len(variants_without_af)} variants without AF data")
            gnomad_sem = asyncio.Semaphore(5)  # Limit concurrent gnomAD requests
            async def _query_one_gnomad(v):
                async with gnomad_sem:
                    try:
                        return await client.query_gnomad_variant(v.chrom, v.pos, v.ref, v.alt)
                    except Exception as e:
                        print(f"[GPA] gnomAD query failed for {v.gene} {v.chrom}:{v.pos}: {e}")
                        return None
            gnomad_results = await asyncio.gather(*[_query_one_gnomad(v) for v in variants_without_af])
            for v, result in zip(variants_without_af, gnomad_results):
                if result and result.get("source") in ("gnomad", "cache"):
                    v.gnomad_af = result.get("af")
                    v.gnomad_populations = result.get("af_populations", {})
                    print(f"[GPA] gnomAD: {v.gene} {v.chrom}:{v.pos} AF={v.gnomad_af}")
                else:
                    v.gnomad_populations = {}
        print(f"[GPA] API batch query complete: Ensembl={len(ensembl_data)}, UniProt={len(uniprot_data)}, GTEx={len(gtex_data)}, HGNC={len(hgnc_data)}, gnomAD_constraint={len(gnomad_constraint_data)}")
        # Persist successful API results for future offline use
        for gene in unique_genes:
            _save_offline_archive(gene, ensembl_data, uniprot_data, gtex_data, config.tissue_profile, gnomad_constraint_data)
        print(f"[GPA] Offline archive saved for {len(unique_genes)} genes to {OFFLINE_ARCHIVE_DIR}")
    else:
        # Offline mode: try to load archived data first, then fall back to local rules
        loaded = 0
        for gene in unique_genes:
            archive = _load_offline_archive(gene)
            if archive:
                ensembl_data[gene] = archive.get("ensembl", {})
                uniprot_data[gene] = archive.get("uniprot", {})
                gtex_data[gene] = archive.get("gtex", {})
                # v0.5 P1-4: Load cached gnomAD constraint if available
                gc = archive.get("gnomad_constraint")
                if gc and gc.get("status") == "CAPTURED":
                    gnomad_constraint_data[gene] = gc
                loaded += 1
        print(f"[GPA] Offline mode: loaded archived data for {loaded}/{len(unique_genes)} genes from {OFFLINE_ARCHIVE_DIR}")
        if loaded == 0:
            print("[GPA] Offline mode: no archive found, using local fallbacks only (conservative)")
        hgnc_data = {}
        # gnomad_constraint_data already populated from archive above
        # No HGNC data in offline mode unless cached

    # ------------------------------------------------------------------
    # Step 0.5: HGNC Gene Symbol Normalization (v0.5 P1-2)
    # ------------------------------------------------------------------
    hgnc_warnings = normalize_gene_symbols(variants, hgnc_data, offline_mode=config.offline_mode)
    if hgnc_warnings:
        print(f"[GPA] HGNC normalization: {len(hgnc_warnings)} warnings")
        for w in hgnc_warnings[:5]:  # Print first 5
            print(f"  - {w}")
        if len(hgnc_warnings) > 5:
            print(f"  ... and {len(hgnc_warnings) - 5} more")

    # Step 0.6: Populate gene constraint data (v0.5 P1-4)
    for v in variants:
        gc = gnomad_constraint_data.get(v.gene, {})
        if gc and gc.get("status") == "CAPTURED":
            v.gene_constraint = {
                "pLI": gc.get("pLI"),
                "loeuf": gc.get("loeuf"),
                "lof_z": gc.get("lof_z"),
                "mis_z": gc.get("mis_z"),
                "oe_lof": gc.get("oe_lof"),
                "source": gc.get("source", "gnomad"),
            }

    # Step 0.7: NMD prediction for truncating variants (v0.5 P1-5)
    nmd_count = 0
    for v in variants:
        lof_terms = {"frameshift", "nonsense", "stop_gained", "start_lost"}
        is_truncating = any(term in v.consequence.lower() for term in lof_terms)
        if is_truncating:
            v.nmd_prediction = predict_nmd(v, ensembl_data.get(v.gene, {}) if ensembl_data else None)
            nmd_count += 1
    if nmd_count > 0:
        print(f"[GPA] NMD prediction computed for {nmd_count} truncating variants")

    # ------------------------------------------------------------------
    # Step 1: Transcript correction (v0.4: Ensembl API)
    # ------------------------------------------------------------------
    for v in variants:
        v, warning = await correct_transcript_priority(v, ensembl_data)
        if warning:
            v.transcript_warning = json.dumps(warning)

    # ------------------------------------------------------------------
    # Step 1.5: VEP canonical reannotation for TRANSCRIPT_DISCREPANCY variants
    # ------------------------------------------------------------------
    # Collect variants where annotator selected non-canonical isoform.
    # Query Ensembl VEP for canonical transcript consequence, impact, and HGVSp.
    # This ensures downstream domain mapping (Step 4) and tier classification
    # use the canonical protein-coding transcript annotation.
    discrepancy_variants = []
    for v in variants:
        if v.transcript_warning:
            try:
                tw = json.loads(v.transcript_warning)
            except (json.JSONDecodeError, TypeError):
                tw = {}
            if tw.get("type") == "TRANSCRIPT_DISCREPANCY":
                discrepancy_variants.append(v)

    if discrepancy_variants and not config.offline_mode:
        print(f"[GPA] VEP reannotation: {len(discrepancy_variants)} variants with TRANSCRIPT_DISCREPANCY")
        vep_inputs = []
        for v in discrepancy_variants:
            vep_inputs.append({
                "chrom": v.chrom,
                "pos": v.pos,
                "ref": v.ref,
                "alt": v.alt,
                "key": f"{v.chrom}:{v.pos}_{v.ref}>{v.alt}",
            })

        cache = DGRACache(global_config.cache_db_path)
        async with DGRAAPIClient(global_config, cache) as client:
            vep_results = await client.batch_query_vep_region(vep_inputs)

        updated_count = 0
        failed_count = 0
        for v in discrepancy_variants:
            key = f"{v.chrom}:{v.pos}_{v.ref}>{v.alt}"
            vep_result = vep_results.get(key, {})

            if vep_result.get("error"):
                failed_count += 1
                try:
                    tw = json.loads(v.transcript_warning) if v.transcript_warning else {}
                except (json.JSONDecodeError, TypeError):
                    tw = {}
                tw["vep_reannotation"] = {
                    "status": "failed",
                    "error": vep_result.get("error"),
                    "fallback": "Using annotator's original annotation",
                }
                tw["vep_reannotation_failed"] = True
                v.transcript_warning = json.dumps(tw)
                # v0.5.2: Fallback confidence downgrade
                v.quality_confidence = "LOW"
                v.tier_confidence = "LOW"
                continue

            # Capture original values for comparison record
            original = {
                "consequence": v.consequence,
                "impact": v.impact,
                "hgvsc": v.hgvsc,
                "hgvsp": v.hgvsp,
                "transcript": v.transcript,
            }

            # Update variant with canonical VEP annotation
            consequence_terms = vep_result.get("consequence_terms", [])
            if consequence_terms:
                # Use first (most severe) consequence term; convert underscores to spaces
                v.consequence = consequence_terms[0].replace("_", " ")
            if vep_result.get("impact"):
                v.impact = vep_result["impact"]
            if vep_result.get("hgvsc"):
                v.hgvsc = vep_result["hgvsc"]
            if vep_result.get("hgvsp"):
                v.hgvsp = vep_result["hgvsp"]
            if vep_result.get("transcript_id"):
                v.transcript = vep_result["transcript_id"]

            # Update transcript_warning with reannotation record
            try:
                tw = json.loads(v.transcript_warning) if v.transcript_warning else {}
            except (json.JSONDecodeError, TypeError):
                tw = {}
            tw["vep_reannotation"] = {
                "status": "success",
                "original": original,
                "canonical": {
                    "consequence": v.consequence,
                    "impact": v.impact,
                    "hgvsc": v.hgvsc,
                    "hgvsp": v.hgvsp,
                    "transcript": v.transcript,
                    "transcript_id": vep_result.get("transcript_id"),
                    "protein_domains": vep_result.get("protein_domains", []),
                },
                "source": vep_result.get("source", "ensembl"),
                "confidence": vep_result.get("confidence", "medium"),
            }
            v.transcript_warning = json.dumps(tw)
            updated_count += 1

        print(f"[GPA] VEP reannotation complete: {updated_count} updated, {failed_count} failed")

    elif discrepancy_variants and config.offline_mode:
        print(f"[GPA] VEP reannotation skipped: offline mode ({len(discrepancy_variants)} discrepancies)")
        for v in discrepancy_variants:
            try:
                tw = json.loads(v.transcript_warning) if v.transcript_warning else {}
            except (json.JSONDecodeError, TypeError):
                tw = {}
            tw["vep_reannotation"] = {
                "status": "skipped",
                "reason": "offline_mode",
                "fallback": "Using annotator's original annotation",
            }
            tw["vep_reannotation_failed"] = True
            v.transcript_warning = json.dumps(tw)
            # v0.5.2: Offline fallback confidence downgrade
            v.quality_confidence = "LOW"
            v.tier_confidence = "LOW"

    # Step 2: Pseudogene detection (unchanged)
    for v in variants:
        pg_warning = detect_pseudogene_artifact(v)
        if pg_warning:
            v.pseudogene_warning = json.dumps(pg_warning)

    # Step 3: gnomAD classification (v0.5 P1-1: population subgroup AFs)
    for v in variants:
        gnomad_info = classify_gnomad_frequency(
            v.gnomad_af, v.gene,
            af_by_population=v.gnomad_populations,
            target_population=getattr(config, 'target_population', None)
        )
        v.gnomad_status = gnomad_info["status"]

    # Step 4: Protein domain mapping (v0.4: UniProt API)
    for v in variants:
        v.domain_info = map_variant_to_domain(v, uniprot_data)

    # Step 5: Tissue relevance assessment (v0.4: GTEx API + local fallback)
    tissue_assessments = {}
    for v in variants:
        tissue = assess_tissue_relevance(v, tissue_profile, gtex_data)
        tissue_assessments[v.gene] = tissue
        v.tissue_relevance = tissue

    # Step 6: Multi-hit detection (unchanged)
    multi_hits = detect_multi_hit_genes(variants, gtex_data)

    # v0.5 P1-13: Input QC checks - after parsing, before tier classification
    qc_summary = _run_qc_checks(variants)
    if qc_summary["flagged"] > 0:
        print(f"[GPA] QC: {qc_summary['flagged']}/{qc_summary['total']} variants flagged: {qc_summary['by_flag']}")

    # Step 6.5: Phenotype association analysis (v0.7 Phase 3, pre-tier)
    # Run BEFORE tier classification so phenotype_match_score is available for tier logic.
    if user_phenotypes:
        from gpa_phenotype_match import PhenotypeMatcher
        matcher = PhenotypeMatcher()
        gene_symbols = [v.gene for v in variants]
        match_results = await matcher.match_batch(gene_symbols, user_phenotypes)
        for v, mr in zip(variants, match_results):
            v.phenotype_match_score = mr.get("score")
            v.phenotype_match_explanation = mr.get("explanation", "")
            v.phenotype_match_confidence = mr.get("confidence", "")
            v.phenotype_matched_pairs = mr.get("matched_pairs", [])
            v.phenotype_known_list = mr.get("known_phenotypes", [])

    # v0.8.0: Step 6.75 - SpliceAI splice-prediction (pre-tier, default OFF)
    # Only runs when config.spliceai_enabled == True.
    # Results stored in variant.spliceai_result for classify_variant_tier to consume.
    if getattr(config, 'spliceai_enabled', False):
        from dgra_splice_predictor import (
            query_spliceai_batch, should_query_spliceai, reset_spliceai_cache
        )
        reset_spliceai_cache()
        spliceai_sem = asyncio.Semaphore(getattr(config, 'spliceai_concurrency', 5))
        # Build list of variants that need SpliceAI
        spliceai_candidates = [v for v in variants if should_query_spliceai(v.consequence)]
        if spliceai_candidates:
            print(f"[GPA] SpliceAI: querying {len(spliceai_candidates)} splice variants (concurrency={getattr(config, 'spliceai_concurrency', 5)})")
            timeout_obj = aiohttp.ClientTimeout(total=120)
            async with aiohttp.ClientSession(timeout=timeout_obj) as spliceai_session:
                spliceai_results = await query_spliceai_batch(
                    spliceai_candidates, spliceai_session, spliceai_sem
                )
            # Attach results back to variants
            for v in variants:
                from dgra_splice_predictor import _cache_key as _splice_key
                key = _splice_key(v.chrom, v.pos, v.ref, v.alt)
                if key in spliceai_results:
                    v.spliceai_result = spliceai_results[key]
                elif should_query_spliceai(v.consequence):
                    # Should have been queried but not in results → mark as not_in_db
                    v.spliceai_result = {"source": "not_in_db", "delta_score": None, "predicted_impact": None}
            print(f"[GPA] SpliceAI: batch complete")

    # Step 7: Three-tier classification (with tissue context)
    for v in variants:
        tissue = tissue_assessments[v.gene]
        gnomad_info = classify_gnomad_frequency(
            v.gnomad_af, v.gene,
            af_by_population=v.gnomad_populations,
            target_population=getattr(config, 'target_population', None)
        )
        tw = json.loads(v.transcript_warning) if v.transcript_warning else None
        pw = json.loads(v.pseudogene_warning) if v.pseudogene_warning else None

        tier, reason, actions = classify_variant_tier(
            v, v.domain_info, tissue, gnomad_info, tw, pw, tissue_profile, config
        )
        v.tier = tier
        v.tier_reason = reason
        v.tier_actions = actions

    # Handle multi-hit elevation
    # v0.5.2 CHANGE: Do NOT elevate individual variants due to multi-hit status.
    # Multi-hit genes are flagged in the report for attention, but each variant
    # keeps its independently-assessed tier. Only variants with their own
    # pathogenic evidence (HIGH impact, ClinVar pathogenic, etc.) remain Tier 1.
    # This prevents false-positive inflation where benign/low-impact variants
    # in a multi-hit gene are incorrectly upgraded.
    _HLA_GENES = {
        "HLA-A", "HLA-B", "HLA-C", "HLA-DRB1", "HLA-DQA1", "HLA-DQB1",
        "HLA-DPA1", "HLA-DPB1", "HLA-E", "HLA-F", "HLA-G", "HLA-H",
        "HLA-J", "HLA-K", "HLA-L", "HLA-N", "HLA-P", "HLA-S",
        "HLA-DMA", "HLA-DMB", "HLA-DOA", "HLA-DOB",
        "MICA", "MICB", "TAP1", "TAP2",
    }
    multi_hit_genes = {mh["gene"] for mh in multi_hits}
    # Filter out HLA genes: natural polymorphism, not pathogenic multi-hit
    hla_multi_hits = {g for g in multi_hit_genes if g in _HLA_GENES}
    multi_hit_genes -= hla_multi_hits  # Exclude from reporting

    # v0.5.2: Multi-hit genes are tracked but their variants are NOT elevated.
    # The multi_hit_genes set is used for reporting only.
    # The hla_multi_hits set can be used for reporting if needed

    # v0.5.1 OPT-P0-2: X-linked female heterozygous adjustment after all tier assignments
    # Female XX patients with X-linked genes: random X-inactivation may provide mosaic protection
    # If gene is haplosufficient, tier 1 -> tier 2, tier 2 -> tier 3
    for v in variants:
        adj_tier, adj_reason = _x_linked_female_adjustment(
            v.tier, v.chrom, v.gt, v.gene_constraint
        )
        if adj_reason:
            v.tier = adj_tier
            v.tier_reason += f" | {adj_reason}"

    # v0.5.1 OPT-P2-2: Gene family redundancy - reduce multi-hit false positives
    for v in variants:
        if v.gene in _GENE_FAMILY_REDUNDANCY and v.tier == 1:
            redundancy = _GENE_FAMILY_REDUNDANCY[v.gene]
            if redundancy.get("compensation_level") == "complete":
                v.tier = 2
                v.tier_reason += f" | REDUCED: {redundancy['reason']} - complete paralog compensation"
            elif redundancy.get("compensation_level") == "partial":
                # Keep tier but add annotation
                v.tier_reason += f" | NOTE: {redundancy['reason']} - partial compensation may mitigate risk"

    # Step 8: Generate report (with tissue context)
    report_md = generate_tier_report(variants, config, tissue_profile, multi_hits)

    # v0.5 P1-12: Generate structured JSON report
    json_report = generate_json_report(variants, config, tissue_profile, multi_hits, report_md, qc_summary)

    # Compile structured output
    def _count_valid(data_dict):
        return sum(1 for d in data_dict.values() if d and d.get("source") not in ("failed", None))

    output = {
        "meta": {
            "tissue_profile": config.tissue_profile,
            "profile_display_name": profile_name,
            "analysis_date": datetime.now().isoformat(),
            "total_variants": len(variants),
            "offline_mode": config.offline_mode,
            "api_coverage": {
                "genes_queried": len(unique_genes),
                "ensembl_success": _count_valid(ensembl_data),
                "uniprot_success": _count_valid(uniprot_data),
                "gtex_success": _count_valid(gtex_data),
            }
        },
        "summary": {
            "tier1_gene_count": len(set(v.gene for v in variants if v.tier == 1)),
            "tier1_variant_count": len([v for v in variants if v.tier == 1]),
            "tier2_gene_count": len(set(v.gene for v in variants if v.tier == 2)),
            "tier2_variant_count": len([v for v in variants if v.tier == 2]),
            "tier3_gene_count": len(set(v.gene for v in variants if v.tier == 3)),
            "tier3_variant_count": len([v for v in variants if v.tier == 3]),
            "multi_hit_genes": [mh["gene"] for mh in multi_hits],
        },
        "tier1_variants": [asdict(v) for v in variants if v.tier == 1],
        "tier2_variants": [asdict(v) for v in variants if v.tier == 2],
        "tier3_variants": [asdict(v) for v in variants if v.tier == 3],
        "multi_hit_details": multi_hits,
        "report_markdown": report_md,
        "json_report": json_report,  # v0.5 P1-12: structured JSON for downstream systems
        "qc_summary": qc_summary,  # v0.5 P1-13: input QC flags
    }

    return output

# =============================================================================
# Multi-Organ Assessment  (v0.5 P1-7)
# =============================================================================

async def run_multi_organ_assessment(variants_data: List[Dict],
                                      user_phenotypes: Optional[str] = None,
                                      config: Optional[GPAConfig] = None) -> Dict:
    """
    v0.5 P1-7: Multi-organ joint assessment.

    Runs GPA for each profile in config.multi_organ_profiles, then generates
    a joint risk matrix taking the MAX tier across profiles per variant.

    API queries are performed per-profile (GTEx tissue-specific), but cached
    responses minimize redundant calls.

    Args:
        variants_data: List of variant dicts from VCF annotation
        config: GPA configuration with multi_organ_profiles set

    Returns:
        Dict with per-profile results + joint report
    """
    if config is None:
        config = GPAConfig()

    if not config.multi_organ_profiles or len(config.multi_organ_profiles) == 0:
        raise ValueError("multi_organ_profiles must be set for multi-organ assessment")

    profiles = config.multi_organ_profiles
    print(f"[GPA] Multi-organ assessment: {len(profiles)} profiles - {', '.join(profiles)}")

    # Run each profile independently
    profile_results = {}
    for profile_name in profiles:
        profile_config = GPAConfig(
            tissue_profile=profile_name,
            offline_mode=config.offline_mode,
            somatic_mode=config.somatic_mode,
            target_population=config.target_population,
            min_dp=config.min_dp,
            min_gq=config.min_gq,
            common_af_threshold=config.common_af_threshold,
            low_af_threshold=config.low_af_threshold,
            vaf_deviation_threshold=config.vaf_deviation_threshold,
            force_sync=config.force_sync,
        )
        print(f"\n[GPA] === Running profile: {profile_name} ===")
        result = await run_dgra_pipeline(variants_data, user_phenotypes=user_phenotypes, config=profile_config)
        profile_results[profile_name] = result

    # Build joint risk matrix: max tier across profiles per variant
    variant_tiers_by_profile = {}  # gene_pos -> {profile: tier}
    variant_details = {}  # gene_pos -> variant dict

    for profile_name, result in profile_results.items():
        for tier_field in ["tier1_variants", "tier2_variants", "tier3_variants"]:
            tier_num = int(tier_field.replace("tier", "").replace("_variants", ""))
            for v_dict in result.get(tier_field, []):
                key = (v_dict.get("gene", ""), v_dict.get("chrom", ""), v_dict.get("pos", 0))
                if key not in variant_tiers_by_profile:
                    variant_tiers_by_profile[key] = {}
                    variant_details[key] = v_dict
                variant_tiers_by_profile[key][profile_name] = tier_num

    # Compute max tier per variant
    joint_tiers = {}
    for key, tiers in variant_tiers_by_profile.items():
        max_tier = max(tiers.values())
        joint_tiers[key] = {
            "gene": key[0],
            "chrom": key[1],
            "pos": key[2],
            "max_tier": max_tier,
            "per_profile": tiers,
            "details": variant_details[key],
        }

    # Generate joint report
    joint_report = generate_multi_organ_report(profile_results, joint_tiers, profiles)

    # Summary
    tier1_joint = [k for k, v in joint_tiers.items() if v["max_tier"] == 1]
    tier2_joint = [k for k, v in joint_tiers.items() if v["max_tier"] == 2]
    tier3_joint = [k for k, v in joint_tiers.items() if v["max_tier"] == 3]

    # Cross-profile high-concern variants (Tier 1 in any profile)
    high_concern = []
    for key, info in joint_tiers.items():
        if info["max_tier"] == 1:
            profiles_t1 = [p for p, t in info["per_profile"].items() if t == 1]
            high_concern.append({
                "gene": info["gene"],
                "chrom": info["chrom"],
                "pos": info["pos"],
                "tier_1_in": profiles_t1,
                "all_profiles": info["per_profile"],
            })

    return {
        "meta": {
            "multi_organ": True,
            "profiles": profiles,
            "analysis_date": datetime.now().isoformat(),
            "total_variants": len(variants_data),
        },
        "profile_results": profile_results,
        "joint_summary": {
            "tier1_count": len(tier1_joint),
            "tier2_count": len(tier2_joint),
            "tier3_count": len(tier3_joint),
            "high_concern_variants": high_concern,
        },
        "joint_risk_matrix": joint_tiers,
        "joint_report_markdown": joint_report,
    }


def generate_multi_organ_report(profile_results: Dict[str, Dict],
                                 joint_tiers: Dict,
                                 profiles: List[str]) -> str:
    """
    v0.5 P1-7: Generate a joint multi-organ risk assessment report.

    Includes:
    - Joint summary (Tier 1/2/3 counts across all profiles)
    - Risk matrix table (variant x profile)
    - High-concern variants (Tier 1 in any profile)
    - Per-profile reports (appended)
    """
    report = []

    report.append("# GPA 多器官联合关联分析报告\n")
    report.append(f"**评估器官**: {', '.join(profiles)}\n")
    report.append(f"**分析日期**: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    report.append(f"**联合策略**: 跨器官取最高 Tier(最保守)\n\n")

    # Joint summary
    tier1_count = sum(1 for k, v in joint_tiers.items() if v["max_tier"] == 1)
    tier2_count = sum(1 for k, v in joint_tiers.items() if v["max_tier"] == 2)
    tier3_count = sum(1 for k, v in joint_tiers.items() if v["max_tier"] == 3)

    report.append("## 联合风险摘要\n\n")
    report.append(f"- **Tier 1 (需干预)**: {tier1_count} 个变异\n")
    report.append(f"- **Tier 2 (需知情)**: {tier2_count} 个变异\n")
    report.append(f"- **Tier 3 (无需担忧)**: {tier3_count} 个变异\n\n")

    # Risk matrix
    report.append("## 联合风险矩阵\n\n")
    report.append("| 基因 | 位置 | " + " | ".join(profiles) + " | **最高 Tier** |\n")
    report.append("|------|------|" + "|".join(["------"] * len(profiles)) + "|----------|\n")

    for key, info in sorted(joint_tiers.items(), key=lambda x: (x[1]["gene"], x[1]["pos"])):
        gene = info["gene"]
        pos = f"{info['chrom']}:{info['pos']}"
        tier_cells = []
        for p in profiles:
            t = info["per_profile"].get(p, "-")
            tier_cells.append(str(t))
        max_tier = info["max_tier"]
        report.append(f"| {gene} | {pos} | " + " | ".join(tier_cells) + f" | **{max_tier}** |\n")

    report.append("\n")

    # High-concern variants
    high_concern = [(k, v) for k, v in joint_tiers.items() if v["max_tier"] == 1]
    if high_concern:
        report.append("## 高关注变异(任一器官 Tier 1)\n\n")
        for key, info in high_concern:
            gene = info["gene"]
            pos = f"{info['chrom']}:{info['pos']}"
            t1_profiles = [p for p, t in info["per_profile"].items() if t == 1]
            report.append(f"- **{gene}** ({pos}): Tier 1 于 {', '.join(t1_profiles)}\n")
            # Show all profile tiers
            tier_detail = ", ".join([f"{p}: Tier {t}" for p, t in info["per_profile"].items()])
            report.append(f"  - 全器官评估: {tier_detail}\n")
        report.append("\n")

    # Per-profile reports
    report.append("---\n\n")
    report.append("# 各器官独立评估报告\n\n")
    for profile_name in profiles:
        result = profile_results[profile_name]
        report.append(f"## [{profile_name}] {result['meta']['profile_display_name']}\n\n")
        report.append(result.get("report_markdown", "(无报告)\n"))
        report.append("\n---\n\n")

    return "\n".join(report)

# =============================================================================
# CLI Interface  (v0.4: --offline + asyncio.run)
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="GPA - Genomic Phenotype Association (v0.4 API-first with cache)",
        epilog="Available tissue profiles: hematopoietic (default), cardiovascular, hepatic, renal, neurological. "
               "Define custom profiles in references/tissue_context.json"
    )
    parser.add_argument("--input", "-i", required=True, help="Input CSV/TSV with annotated variants")
    parser.add_argument("--output", "-o", default="dgra_report.md", help="Output report file")
    parser.add_argument("--json", "-j", help="Output JSON file with full structured results (backward compatible)")
    parser.add_argument("--output-json", dest="output_json",
                        help="Output P1-12 structured JSON report for downstream systems (v0.5 P1-12)")
    parser.add_argument("--tissue", "-t", default="general",
                        help="Tissue/organ context profile. "
                             "Controls which genes are considered relevant for tier classification. "
                             "Available: general, hematopoietic, cardiovascular, hepatic, renal, neurological. "
                             "Default: general. Mutually exclusive with --multi-organ.")
    parser.add_argument("--multi-organ", default=None,
                        help="Multi-organ assessment: comma-separated profiles, e.g. 'hematopoietic,cardiovascular'. "
                             "Runs independent assessment for each profile and generates a joint risk matrix. "
                             "Takes max tier across profiles. Mutually exclusive with --tissue. (v0.5 P1-7)")
    parser.add_argument("--offline", action="store_true",
                        help="Offline mode: skip all API calls, use cache + local references only")
    parser.add_argument("--somatic", action="store_true",
                        help="Somatic mode: tumor driver mutation analysis. "
                             "TSG truncating + oncogene hotspots = Tier 1")
    parser.add_argument("--sync-gene-lists", action="store_true",
                        help="Force sync special_gene_lists from external sources (Orphanet, OMIM) before analysis. "
                             "Bypasses cache TTL. (v0.5 P1-8)")
    parser.add_argument("--evidence-detail", choices=["brief", "full"], default="brief",
                        help="Evidence chain detail level in report: brief (top 3) or full (all). (v0.5 P1-9)")
    parser.add_argument("--target-population", "--population",
                        choices=["EAS", "AMR", "AFR", "NFE", "SAS", "ASJ", "FIN", "MID", "OTH"],
                        help="Target population for gnomAD subgroup AF classification (v0.5 P1-1). "
                             "Uses that population's AF instead of overall AF for frequency-based tiering.")
    parser.add_argument("--database-version",
                        help="Freeze analysis to a specific database version for reproducibility "
                             "(e.g., 'gnomAD v4.1'). Recorded in output meta. (v0.5 P1-15)")
    # v0.5 P2-3: YAML config file support
    parser.add_argument("--config", "-c", type=Path, default=None,
                        help="Path to dgra.yaml configuration file. Overrides built-in defaults. "
                             "If not specified, uses references/dgra.yaml if it exists, "
                             "otherwise falls back to built-in defaults. (v0.5 P2-3)")

    # v0.7: Phenotype association
    parser.add_argument("--phenotypes", default=None,
                        help="Clinical phenotype description for phenotype-gene association analysis. "
                             "e.g. 'distal muscle weakness, myopathic damage, slow progression'. "
                             "Only applied to Tier 1/2 variants. Requires LLM API key for best accuracy.")
    parser.add_argument("--filter-preset", default=None, choices=["strict", "clinical", "broad"],
                        help="Filter preset name used for pre-filtering. Displayed in report header. (v0.7.1)")
    parser.add_argument("--filter-stats", default=None,
                        help="JSON string of filter statistics. Displayed in report header. (v0.7.1)")
    parser.add_argument("--llm-model", default="gpt-4o-mini",
                        help="LLM model for phenotype semantic matching. Default: gpt-4o-mini. "
                             "Alternative: gpt-4o, claude-3-haiku.")
    # v0.8.0: SpliceAI splice-prediction integration (default OFF)
    parser.add_argument("--spliceai", action="store_true",
                        help="Enable SpliceAI splice-prediction lookup for splice variants. "
                             "Default OFF — only applies to canonical splice (acceptor/donor) and splice_region. "
                             "(v0.8.0)")
    parser.add_argument("--spliceai-concurrency", type=int, default=5,
                        help="Max concurrent SpliceAI API requests (default: 5). (v0.8.0)")

    args = parser.parse_args()

    # v0.5 P2-3: Load YAML config if provided or default exists
    file_config = None
    config_path = args.config
    if config_path is None and DEFAULT_CONFIG_PATH.exists():
        config_path = DEFAULT_CONFIG_PATH

    if config_path:
        try:
            file_config = GPAFileConfig.from_yaml(config_path)
            print(f"[GPA] Loaded configuration from {config_path}")
        except FileNotFoundError:
            print(f"[GPA] Config file not found: {config_path}, using built-in defaults")
        except Exception as e:
            print(f"[GPA] Warning: Failed to load config {config_path}: {e}")

    # v0.5 P1-7: Validate --multi-organ vs --tissue mutual exclusion
    multi_organ = None
    if args.multi_organ:
        if args.tissue != "general":
            # tissue was explicitly set (not default)
            print("Error: --tissue and --multi-organ are mutually exclusive. Use one or the other.")
            sys.exit(1)
        multi_organ = [p.strip() for p in args.multi_organ.split(",") if p.strip()]
        valid_tissues = {"general", "hematopoietic", "cardiovascular", "hepatic", "renal", "neurological"}
        invalid = [p for p in multi_organ if p not in valid_tissues]
        if invalid:
            print(f"Error: Invalid multi-organ profile(s): {', '.join(invalid)}. Valid: {', '.join(sorted(valid_tissues))}")
            sys.exit(1)
        if len(multi_organ) < 1 or len(multi_organ) > 3:
            print("Error: --multi-organ requires 1-3 profiles.")
            sys.exit(1)
        print(f"Multi-organ assessment: {', '.join(multi_organ)}")

    # Read variants from CSV/TSV
    variants_data = []
    with open(args.input, 'r') as f:
        reader = csv.DictReader(f, delimiter='\t' if args.input.endswith('.tsv') else ',')
        for row in reader:
            variants_data.append(dict(row))

    # v0.7: Set LLM model env var if specified
    if args.llm_model:
        os.environ.setdefault("GPA_LLM_MODEL", args.llm_model)

    # Run async pipeline with tissue context
    filter_stats = None
    if args.filter_stats:
        try:
            filter_stats = json.loads(args.filter_stats)
        except json.JSONDecodeError:
            print(f"[GPA] Warning: Invalid --filter-stats JSON, ignoring")

    config = GPAConfig(
        tissue_profile=args.tissue,
        offline_mode=args.offline,
        somatic_mode=args.somatic,
        target_population=args.target_population,
        multi_organ_profiles=multi_organ,
        force_sync=args.sync_gene_lists,
        evidence_detail=args.evidence_detail,
        database_version=args.database_version,
        filter_stats=filter_stats,
        filter_preset=args.filter_preset,
        # v0.8.0: SpliceAI
        spliceai_enabled=getattr(args, 'spliceai', False),
        spliceai_concurrency=getattr(args, 'spliceai_concurrency', 5),
    )

    # v0.5 P2-3: Apply YAML config overrides to user config
    if file_config:
        file_config.apply_to_user_config(config)

    # v0.5 P2-3: Also build global config with file overrides (for API layer)
    global_config = config.to_global()
    if file_config:
        base_dir = config_path.parent if config_path else Path(__file__).parent.parent
        file_config.apply_to_global(global_config, base_dir)

    # v0.5 P1-7: Multi-organ path
    if multi_organ:
        results = asyncio.run(run_multi_organ_assessment(variants_data, user_phenotypes=args.phenotypes, config=config))

        # Write joint report
        with open(args.output, 'w') as f:
            f.write(results["joint_report_markdown"])

        print(f"GPA Multi-Organ Report Generated: {args.output}")
        print(f"Profiles assessed: {', '.join(multi_organ)}")
        print(f"Joint Summary: Tier 1={results['joint_summary']['tier1_gene_count']} genes / {results['joint_summary']['tier1_variant_count']} variants, "
              f"Tier 2={results['joint_summary']['tier2_gene_count']} genes / {results['joint_summary']['tier2_variant_count']} variants, "
              f"Tier 3={results['joint_summary']['tier3_gene_count']} genes / {results['joint_summary']['tier3_variant_count']} variants")

        if results['joint_summary']['high_concern_variants']:
            genes = [v['gene'] for v in results['joint_summary']['high_concern_variants']]
            print(f"High-concern variants (Tier 1 in any profile): {', '.join(genes)}")

        # Write JSON if requested (backward compatible)
        if args.json:
            with open(args.json, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            print(f"Structured output written to: {args.json}")

        # v0.5 P1-12: Write P1-12 structured JSON report if requested
        if args.output_json:
            with open(args.output_json, 'w') as f:
                json.dump(results.get("json_report", {}), f, indent=2, default=str, ensure_ascii=False)
            print(f"P1-12 JSON report written to: {args.output_json}")

        return

    # Single-organ path (original behavior)
    results = asyncio.run(run_dgra_pipeline(variants_data, user_phenotypes=args.phenotypes, config=config))

    # Write report
    with open(args.output, 'w') as f:
        f.write(results["report_markdown"])

    profile_name = results["meta"]["profile_display_name"]
    print(f"GPA Report Generated: {args.output}")
    print(f"Tissue Context: {profile_name} ({args.tissue})")
    print(f"Summary: Tier 1={results['summary']['tier1_gene_count']} genes / {results['summary']['tier1_variant_count']} variants, "
          f"Tier 2={results['summary']['tier2_gene_count']} genes / {results['summary']['tier2_variant_count']} variants, "
          f"Tier 3={results['summary']['tier3_gene_count']} genes / {results['summary']['tier3_variant_count']} variants")

    if results['summary']['multi_hit_genes']:
        print(f"Multi-hit genes: {', '.join(results['summary']['multi_hit_genes'])}")

    # Write JSON if requested (backward compatible)
    if args.json:
        with open(args.json, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        print(f"Structured output written to: {args.json}")

    # v0.5 P1-12: Write P1-12 structured JSON report if requested
    if args.output_json:
        with open(args.output_json, 'w') as f:
            json.dump(results.get("json_report", {}), f, indent=2, default=str, ensure_ascii=False)
        print(f"P1-12 JSON report written to: {args.output_json}")

if __name__ == "__main__":
    main()
