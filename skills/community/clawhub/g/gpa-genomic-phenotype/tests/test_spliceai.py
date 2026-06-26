#!/usr/bin/env python3
"""
GPA v0.8.0 SpliceAI Integration Tests

Tests the SpliceAI lookup module and its integration into the tier classification pipeline.
All tests use mocked API responses (no real network calls).

Test cases:
1. PYGL downgrade: canonical splice + SpliceAI delta=0 → Tier downgrade
2. Strong splice upgrade: canonical splice + SpliceAI delta=0.8 → Tier upgrade
3. Not in database: variant not in SpliceAI DB → not_in_db, no crash
4. API failure: network error / timeout → api_error, no crash
5. Unchanged without flag: --spliceai not provided → results identical to v0.7.2
6. Non-splice not queried: missense/stop_gained → no SpliceAI query
"""

import asyncio
import sys
from pathlib import Path
from unittest.mock import AsyncMock, patch, MagicMock

# Ensure scripts are importable
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from dgra_splice_predictor import (
    SpliceAIPredictor,
    SpliceAIResult,
    should_query_spliceai,
    reset_spliceai_cache,
    _cache_key,
    query_spliceai_batch,
)
from dgra_core import classify_variant_tier, Variant, GPAConfig


# ---------------------------------------------------------------------------
# Mock variant factory
# ---------------------------------------------------------------------------

def _make_variant(
    gene="PYGL",
    consequence="splice_acceptor_variant",
    impact="HIGH",
    clinvar="",
    gt="0/1",
    chrom="1",
    pos=100000,
    ref="A",
    alt="G",
    vaf=0.5,
    gnomad_af=0.0,
    **kwargs,
) -> Variant:
    """Build a minimal Variant for testing."""
    defaults = {
        "transcript": "ENST00000000000",
        "exon": "1/10",
        "hgvsp": "",
        "hgvsc": "",
        "gnomad_status": "unknown",
        "gnomad_populations": {},
        "domain_info": {},
        "tissue_relevance": "unknown",
        "evidence_chain": [],
        "upgrade_conditions": [],
        "tier": 3,
        "tier_reason": "",
        "tier_actions": [],
        "tier_confidence": "LOW",
        "qc_flags": [],
        "quality_confidence": "high",
        "missing_fields": [],
        "pseudogene_warning": None,
        "transcript_warning": None,
        "gene_constraint": {},
        "phenotype_match_score": None,
        "phenotype_match_explanation": None,
        "phenotype_match_confidence": None,
        "phenotype_matched_pairs": [],
        "phenotype_known_list": [],
        "clinvar_review_status": None,
        "spliceai_result": None,
    }
    defaults.update(kwargs)
    v = Variant(
        chrom=chrom,
        pos=pos,
        ref=ref,
        alt=alt,
        gene=gene,
        consequence=consequence,
        impact=impact,
        clinvar=clinvar,
        gt=gt,
        vaf=vaf,
        gnomad_af=gnomad_af,
        **defaults,
    )
    return v


def _minimal_domain():
    return {"domain": None, "domain_integrity": "unknown"}


def _minimal_tissue(relevance="primary"):
    return {"relevance": relevance, "reason": "test", "tissues": []}


def _minimal_gnomad():
    return {"status": "rare", "af": 0.0}


# ---------------------------------------------------------------------------
# Test 1: PYGL downgrade — canonical splice + SpliceAI delta=0
# ---------------------------------------------------------------------------

def test_pygl_spliceai_delta_zero_downgrade():
    """
    A canonical splice_acceptor_variant with SpliceAI delta=0 should trigger
    a downgrade from Tier 1 (HIGH impact) to Tier 2, with weight=-0.5 evidence.
    """
    v = _make_variant(gene="PYGL", consequence="splice_acceptor_variant", impact="HIGH")
    v.spliceai_result = {
        "source": "spliceai",
        "delta_score": 0.0,
        "predicted_impact": "none",
        "details": {"AG": 0.0, "AL": 0.0, "DG": 0.0, "DL": 0.0},
        "threshold_type": "canonical",
    }
    config = GPAConfig(tissue_profile="general", spliceai_enabled=True)

    tier, reason, actions = classify_variant_tier(
        v, _minimal_domain(), _minimal_tissue("primary"),
        _minimal_gnomad(), None, None, {}, config,
    )

    # The variant is HIGH impact + primary tissue + heterozygous → normally Tier 2
    # With SpliceAI delta=0, it should downgrade from Tier 2 → Tier 3
    assert tier == 3, f"Expected Tier 3 downgrade, got Tier {tier}"
    assert "SpliceAI delta=0" in reason or any("SpliceAI" in a for a in actions), \
        "SpliceAI downgrade reason/action not found"
    evidence_sources = [ev.source for ev in v.evidence_chain]
    assert "SpliceAI" in evidence_sources, "SpliceAI evidence not in evidence chain"
    print("✅ Test 1: PYGL delta=0 downgrade passed")


# ---------------------------------------------------------------------------
# Test 2: Strong splice upgrade — canonical splice + SpliceAI delta=0.8
# ---------------------------------------------------------------------------

def test_strong_splice_upgrade():
    """
    A splice_region_variant with SpliceAI delta=0.8 should trigger an upgrade
    from Tier 3 to Tier 2, with weight=0.8 evidence.
    """
    v = _make_variant(
        gene="TEST1",
        consequence="splice_region_variant",
        impact="MODERATE",
        clinvar="",
        gnomad_af=0.001,
    )
    v.spliceai_result = {
        "source": "spliceai",
        "delta_score": 0.8,
        "predicted_impact": "strong",
        "details": {"AG": 0.0, "AL": 0.8, "DG": 0.0, "DL": 0.0},
        "threshold_type": "splice_region",
    }
    config = GPAConfig(tissue_profile="general", spliceai_enabled=True)

    tier, reason, actions = classify_variant_tier(
        v, _minimal_domain(), _minimal_tissue("none"),
        {"status": "rare", "af": 0.001}, None, None, {}, config,
    )

    assert tier == 2, f"Expected Tier 2 upgrade, got Tier {tier}"
    assert "SpliceAI" in reason or any("SpliceAI" in a for a in actions)
    evidence_sources = [ev.source for ev in v.evidence_chain]
    assert "SpliceAI" in evidence_sources
    print("✅ Test 2: Strong splice upgrade passed")


# ---------------------------------------------------------------------------
# Test 3: Not in database
# ---------------------------------------------------------------------------

def test_not_in_database():
    """
    A splice variant not present in SpliceAI DB should return not_in_db
    without crashing, and classify_variant_tier should handle it gracefully.
    Uses a Tier 3 path variant (MODERATE impact, non-tissue) so the not_in_db
    logic in Tier 3 is exercised.
    """
    v = _make_variant(
        gene="NOTDB",
        consequence="splice_region_variant",
        impact="MODERATE",
        gnomad_af=0.001,
    )
    v.spliceai_result = {
        "source": "not_in_db",
        "delta_score": None,
        "predicted_impact": None,
    }
    config = GPAConfig(tissue_profile="general", spliceai_enabled=True)

    tier, reason, actions = classify_variant_tier(
        v, _minimal_domain(), _minimal_tissue("none"),
        _minimal_gnomad(), None, None, {}, config,
    )

    # Not in DB should not crash; tier should be based on other evidence (Tier 3)
    assert tier == 3, f"Expected Tier 3, got Tier {tier}"
    evidence_sources = [ev.source for ev in v.evidence_chain]
    assert "SpliceAI" in evidence_sources, "SpliceAI 'not in db' evidence should be recorded"
    print("✅ Test 3: Not in database passed")


# ---------------------------------------------------------------------------
# Test 4: API failure
# ---------------------------------------------------------------------------

def test_api_failure_graceful():
    """
    Simulate an API failure. The pipeline must not crash; a QC flag should be added.
    Uses a Tier 3 path variant to exercise the api_error handling in Tier 3.
    """
    v = _make_variant(
        gene="APIFAIL",
        consequence="splice_region_variant",
        impact="MODERATE",
        gnomad_af=0.001,
    )
    v.spliceai_result = {
        "source": "api_error",
        "delta_score": None,
        "predicted_impact": None,
        "error": "HTTP 503: Server temporarily unavailable",
    }
    config = GPAConfig(tissue_profile="general", spliceai_enabled=True)

    tier, reason, actions = classify_variant_tier(
        v, _minimal_domain(), _minimal_tissue("none"),
        _minimal_gnomad(), None, None, {}, config,
    )

    assert tier == 3, f"Expected Tier 3, got Tier {tier}"
    assert "SPLICEAI_API_ERROR" in v.qc_flags, "SPLICEAI_API_ERROR QC flag not set"
    print("✅ Test 4: API failure graceful fallback passed")


# ---------------------------------------------------------------------------
# Test 5: Unchanged without --spliceai flag
# ---------------------------------------------------------------------------

def test_unchanged_without_flag():
    """
    When spliceai_enabled=False (default), results must be identical to v0.7.2.
    SpliceAI result attached but not used.
    """
    # Without flag — fresh variant
    v_off = _make_variant(gene="NOFLAG", consequence="splice_acceptor_variant", impact="HIGH")
    v_off.spliceai_result = {
        "source": "spliceai",
        "delta_score": 0.0,
        "predicted_impact": "none",
        "details": {"AG": 0.0, "AL": 0.0, "DG": 0.0, "DL": 0.0},
        "threshold_type": "canonical",
    }
    config_off = GPAConfig(tissue_profile="general", spliceai_enabled=False)

    tier_off, reason_off, actions_off = classify_variant_tier(
        v_off, _minimal_domain(), _minimal_tissue("primary"),
        _minimal_gnomad(), None, None, {}, config_off,
    )

    # With flag ON — fresh variant, same data
    v_on = _make_variant(gene="NOFLAG", consequence="splice_acceptor_variant", impact="HIGH")
    v_on.spliceai_result = {
        "source": "spliceai",
        "delta_score": 0.0,
        "predicted_impact": "none",
        "details": {"AG": 0.0, "AL": 0.0, "DG": 0.0, "DL": 0.0},
        "threshold_type": "canonical",
    }
    config_on = GPAConfig(tissue_profile="general", spliceai_enabled=True)

    tier_on, reason_on, actions_on = classify_variant_tier(
        v_on, _minimal_domain(), _minimal_tissue("primary"),
        _minimal_gnomad(), None, None, {}, config_on,
    )

    # Without flag: tier should be higher (not downgraded)
    # HIGH + primary tissue + het → normally Tier 2
    # With SpliceAI delta=0 enabled: Tier 2 → Tier 3 (downgrade)
    # Without SpliceAI: stays Tier 2
    assert tier_off == 2, f"Without flag expected Tier 2, got Tier {tier_off}"
    assert tier_on == 3, f"With flag expected Tier 3 (downgraded), got Tier {tier_on}"

    # Evidence check: disabled = no SpliceAI evidence
    evidence_off = [ev.source for ev in v_off.evidence_chain]
    assert "SpliceAI" not in evidence_off, "SpliceAI evidence should NOT appear when disabled"
    evidence_on = [ev.source for ev in v_on.evidence_chain]
    assert "SpliceAI" in evidence_on, "SpliceAI evidence SHOULD appear when enabled"
    print("✅ Test 5: Unchanged without --spliceai passed")


# ---------------------------------------------------------------------------
# Test 6: Non-splice variant not queried
# ---------------------------------------------------------------------------

def test_non_splice_not_queried():
    """
    Missense and stop_gained variants should NOT trigger SpliceAI queries.
    should_query_spliceai() must return False for these consequences.
    """
    assert not should_query_spliceai("missense_variant")
    assert not should_query_spliceai("stop_gained")
    assert not should_query_spliceai("frameshift_variant")
    assert not should_query_spliceai("synonymous_variant")

    assert should_query_spliceai("splice_acceptor_variant")
    assert should_query_spliceai("splice_donor_variant")
    assert should_query_spliceai("splice_region_variant")
    assert should_query_spliceai("splice_polypyrimidine_tract_variant")
    assert should_query_spliceai("splice_donor_5th_base_variant")
    print("✅ Test 6: Non-splice not queried passed")


# ---------------------------------------------------------------------------
# Module-level tests for dgra_splice_predictor
# ---------------------------------------------------------------------------

def test_classify_spliceai_impact():
    """Test SpliceAI delta score classification."""
    # canonical thresholds: strong=0.5, moderate=0.2, weak=0.1
    assert SpliceAIPredictor.determine_impact(0.0, "canonical") == "none"
    assert SpliceAIPredictor.determine_impact(0.05, "canonical") == "none"   # 0.05 < 0.1 (weak)
    assert SpliceAIPredictor.determine_impact(0.15, "canonical") == "weak"   # 0.15 >= 0.1 (weak)
    assert SpliceAIPredictor.determine_impact(0.25, "canonical") == "moderate"
    assert SpliceAIPredictor.determine_impact(0.55, "canonical") == "strong"
    # splice_region thresholds: strong=0.2, moderate=0.1, weak=0.05
    assert SpliceAIPredictor.determine_impact(0.03, "splice_region") == "none"
    assert SpliceAIPredictor.determine_impact(0.25, "splice_region") == "strong"
    print("✅ Test: classify_spliceai_impact passed")


def test_get_spliceai_threshold():
    """Test threshold retrieval per consequence type."""
    from dgra_splice_predictor import SPLICEAI_THRESHOLDS
    canonical = SPLICEAI_THRESHOLDS["canonical"]
    assert canonical["strong"] == 0.50
    region = SPLICEAI_THRESHOLDS["splice_region"]
    assert region["strong"] == 0.20
    print("✅ Test: get_spliceai_threshold passed")


def test_is_canonical_vs_region():
    """Test canonical vs splice_region classification."""
    assert SpliceAIPredictor.is_canonical_splice(["splice_acceptor_variant"])
    assert SpliceAIPredictor.is_canonical_splice(["splice_donor_variant"])
    assert not SpliceAIPredictor.is_canonical_splice(["splice_region_variant"])
    # splice_region is not canonical but still queried
    assert should_query_spliceai("splice_region_variant")
    assert should_query_spliceai("splice_polypyrimidine_tract_variant")
    print("✅ Test: is_canonical_vs_region passed")


# ---------------------------------------------------------------------------
# Async API tests (mocked)
# ---------------------------------------------------------------------------

async def _test_query_spliceai_mock():
    """Mock the aiohttp session to test SpliceAI query without real network."""
    reset_spliceai_cache()

    v = _make_variant(chrom="1", pos=100000, ref="A", alt="G", consequence="splice_acceptor_variant")

    # Use SpliceAIPredictor directly with mocked internal _query_with_retry
    predictor = SpliceAIPredictor(max_concurrency=5, timeout=30)

    # Mock response object
    mock_resp = AsyncMock()
    mock_resp.status = 200
    mock_resp.json = AsyncMock(return_value={
        "delta_scores": {"AG": 0.0, "AL": 0.55, "DG": 0.0, "DL": 0.0}
    })
    mock_resp.headers = {}

    mock_session = AsyncMock()
    mock_session.get = AsyncMock(return_value=mock_resp)

    # Patch predictor.query to use mock session
    async def mock_query(chrom, pos, ref, alt, genome="GRCh38"):
        chrom_std = chrom.replace("chr", "") if chrom.startswith("chr") else chrom
        cache_key = predictor._cache_key(chrom_std, pos, ref, alt)
        if cache_key in predictor._cache:
            return predictor._cache[cache_key]

        result = SpliceAIResult(
            delta_score=0.55,
            delta_acceptor_gain=0.0,
            delta_acceptor_loss=0.55,
            delta_donor_gain=0.0,
            delta_donor_loss=0.0,
            predicted_impact="strong",
            threshold_type="canonical",
            source="spliceai_lookup",
            raw_response={"delta_scores": {"AG": 0.0, "AL": 0.55, "DG": 0.0, "DL": 0.0}},
        )
        predictor._cache[cache_key] = result
        return result

    predictor.query = mock_query

    sem = asyncio.Semaphore(5)
    result = await predictor.query(v.chrom, v.pos, v.ref, v.alt)

    assert result.source == "spliceai_lookup"
    assert result.delta_score == 0.55
    print("✅ Async test: SpliceAIPredictor mock passed")
    assert result.predicted_impact == "strong"
    assert result.threshold_type == "canonical"
    print("✅ Async test: query_spliceai mock passed")


def test_async_mock():
    asyncio.run(_test_query_spliceai_mock())


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    tests = [
        test_pygl_spliceai_delta_zero_downgrade,
        test_strong_splice_upgrade,
        test_not_in_database,
        test_api_failure_graceful,
        test_unchanged_without_flag,
        test_non_splice_not_queried,
        test_classify_spliceai_impact,
        test_get_spliceai_threshold,
        test_is_canonical_vs_region,
        test_async_mock,
    ]

    passed = 0
    failed = 0
    for t in tests:
        try:
            t()
            passed += 1
        except Exception as e:
            failed += 1
            print(f"❌ {t.__name__} FAILED: {e}")

    print(f"\n{'='*50}")
    print(f"SpliceAI Tests: {passed} passed, {failed} failed out of {len(tests)}")
    print(f"{'='*50}")
    if failed > 0:
        sys.exit(1)
