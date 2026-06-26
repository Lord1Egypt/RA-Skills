"""Tests for mg_schema.meta_defaults — canonical schema constants."""

from mg_schema.meta_defaults import (
    SCHEMA_VERSION,
    PRODUCT_VERSION,
    DEFAULT_DECAY_CONFIG,
    DEFAULT_QUALITY_GATE_STATE,
)


class TestMetaDefaults:
    def test_schema_version_format(self):
        assert isinstance(SCHEMA_VERSION, str)
        # SCHEMA_VERSION is like "0.4.5" (no "v" prefix)
        assert "." in SCHEMA_VERSION

    def test_product_version_format(self):
        assert isinstance(PRODUCT_VERSION, str)
        assert PRODUCT_VERSION.startswith("v")

    def test_decay_config_structure(self):
        assert isinstance(DEFAULT_DECAY_CONFIG, dict)
        assert "alpha" in DEFAULT_DECAY_CONFIG
        assert "beta_cap" in DEFAULT_DECAY_CONFIG
        assert DEFAULT_DECAY_CONFIG["alpha"] > 0

    def test_decay_config_provenance(self):
        prov = DEFAULT_DECAY_CONFIG["provenance"]
        assert "authoritative_base" in prov
        assert "non_authoritative_base" in prov
        assert prov["authoritative_base"] > prov["non_authoritative_base"]

    def test_decay_config_quiet_degradation(self):
        qd = DEFAULT_DECAY_CONFIG["quiet_degradation"]
        assert "min_sample" in qd
        assert "median_discount" in qd
        assert qd["min_sample"] >= 1

    def test_quality_gate_state_defaults(self):
        state = DEFAULT_QUALITY_GATE_STATE
        assert state["state"] == "NORMAL"
        assert state["anomaly_count"] == 0
        assert state["total_writes"] == 0
        assert state["total_failures"] == 0
        assert state["failure_rate"] == 0.0
        assert isinstance(state["history"], list)
        assert isinstance(state["check_history"], list)
