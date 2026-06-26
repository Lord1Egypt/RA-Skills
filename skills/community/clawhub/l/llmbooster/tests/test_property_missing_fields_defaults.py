"""Property-based test: Missing config fields 用 default 值填充.

Feature: llm-booster-skill, Property 8: Missing config fields 用 default 值填充
Validates: Requirements 3.3
"""

from __future__ import annotations

import json
import os
import sys
import tempfile

from hypothesis import given, settings, strategies as st

# Ensure the skill package is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from config_loader import ConfigLoader
from models import BoosterConfig

# ---------------------------------------------------------------------------
# Defaults (must match ConfigLoader.DEFAULT_CONFIG)
# ---------------------------------------------------------------------------

DEFAULTS = {
    "enabled": True,
    "thinkingDepth": 4,
    "maxRetries": 3,
}

ALL_FIELDS = list(DEFAULTS.keys())

# ---------------------------------------------------------------------------
# Strategies
# ---------------------------------------------------------------------------

# Strategy: random subset of field names to *include* in the config file.
# The complement (omitted fields) should be filled with defaults.
fields_subset = st.lists(
    st.sampled_from(ALL_FIELDS),
    unique=True,
    min_size=0,
    max_size=len(ALL_FIELDS),
)

# Valid values for each field (used when a field IS present)
valid_enabled = st.booleans()
valid_thinking_depth = st.integers(min_value=1, max_value=4)
valid_max_retries = st.integers(min_value=1, max_value=10)


# ---------------------------------------------------------------------------
# Property 8: Missing config fields 用 default 值填充
# ---------------------------------------------------------------------------


class TestMissingFieldsDefaultsProperty:
    """**Validates: Requirements 3.3**"""

    @settings(max_examples=100)
    @given(
        included_fields=fields_subset,
        enabled_val=valid_enabled,
        depth_val=valid_thinking_depth,
        retries_val=valid_max_retries,
    )
    def test_missing_fields_filled_with_defaults(
        self,
        included_fields: list[str],
        enabled_val: bool,
        depth_val: int,
        retries_val: int,
    ) -> None:
        """For any subset of config fields omitted from the file, the loader
        fills missing fields with their default values and the resulting
        BoosterConfig passes validation."""

        # Build a partial config containing only the included fields
        field_values = {
            "enabled": enabled_val,
            "thinkingDepth": depth_val,
            "maxRetries": retries_val,
        }
        partial_config = {k: field_values[k] for k in included_fields}

        # Write to a temp file
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as tmp:
            json.dump(partial_config, tmp)
            tmp_path = tmp.name

        try:
            loader = ConfigLoader()
            config = loader.load(tmp_path)

            # The result must be a BoosterConfig
            assert isinstance(config, BoosterConfig)

            # Included fields should keep their provided values
            for field_name in included_fields:
                actual = getattr(config, field_name)
                assert actual == field_values[field_name], (
                    f"Included field '{field_name}' should be {field_values[field_name]!r}"
                    f", got {actual!r}"
                )

            # Omitted fields should have their default values
            omitted = set(ALL_FIELDS) - set(included_fields)
            for field_name in omitted:
                actual = getattr(config, field_name)
                assert actual == DEFAULTS[field_name], (
                    f"Missing field '{field_name}' should default to"
                    f" {DEFAULTS[field_name]!r}, got {actual!r}"
                )

            # The resulting config must pass validation for every field
            for field_name in ALL_FIELDS:
                result = loader.validate_field(field_name, getattr(config, field_name))
                assert result.valid, (
                    f"Field '{field_name}' with value {getattr(config, field_name)!r}"
                    f" should pass validation but got: {result.error_message}"
                )
        finally:
            os.unlink(tmp_path)
