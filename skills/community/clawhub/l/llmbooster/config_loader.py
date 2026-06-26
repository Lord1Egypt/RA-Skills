"""Config Loader & Validator for LLMBooster skill."""

from __future__ import annotations

import json
from typing import Any

from models import BoosterConfig, ValidationResult


class ConfigLoader:
    """Responsible for reading and validating config file.
    Missing fields are filled with default values, invalid values are rejected and fallback to default.
    """

    DEFAULT_CONFIG = {
        "enabled": True,
        "thinkingDepth": 4,
        "maxRetries": 3,
    }

    VALIDATION_RULES = {
        "enabled": {"type": bool},
        "thinkingDepth": {"type": int, "min": 1, "max": 4},
        "maxRetries": {"type": int, "min": 1, "max": 10},
    }

    def load(self, config_path: str) -> BoosterConfig:
        """Read config file, validate each field, return BoosterConfig."""
        errors: list[str] = []

        # Try to read and parse the file
        try:
            with open(config_path, "r") as f:
                raw = json.load(f)
        except FileNotFoundError:
            return BoosterConfig(**self.DEFAULT_CONFIG)
        except (json.JSONDecodeError, ValueError):
            config = BoosterConfig(**self.DEFAULT_CONFIG)
            config._errors = ["JSON parse error: config file is not valid JSON"]
            return config

        if not isinstance(raw, dict):
            config = BoosterConfig(**self.DEFAULT_CONFIG)
            config._errors = ["JSON parse error: config file root is not an object"]
            return config

        # Build config with validation
        result = {}
        for field_name, default_value in self.DEFAULT_CONFIG.items():
            if field_name not in raw:
                # Missing field → use default
                result[field_name] = default_value
            else:
                validation = self.validate_field(field_name, raw[field_name])
                if validation.valid:
                    result[field_name] = raw[field_name]
                else:
                    result[field_name] = default_value
                    errors.append(validation.error_message)

        config = BoosterConfig(**result)
        if errors:
            config._errors = errors
        return config

    def validate_field(self, field_name: str, value: Any) -> ValidationResult:
        """Validate single field against rules. Return success or error message."""
        if field_name not in self.VALIDATION_RULES:
            return ValidationResult(
                valid=False,
                field_name=field_name,
                error_message=f"Unknown field: {field_name}",
            )

        rules = self.VALIDATION_RULES[field_name]
        expected_type = rules["type"]

        # For int fields, reject booleans (since bool is subclass of int in Python)
        if expected_type is int:
            if isinstance(value, bool) or not isinstance(value, int):
                range_info = f"{rules['min']}-{rules['max']}"
                return ValidationResult(
                    valid=False,
                    field_name=field_name,
                    error_message=f"{field_name} must be an integer in range {range_info}",
                )
            if value < rules["min"] or value > rules["max"]:
                range_info = f"{rules['min']}-{rules['max']}"
                return ValidationResult(
                    valid=False,
                    field_name=field_name,
                    error_message=f"{field_name} must be in range {range_info}",
                )
        elif expected_type is bool:
            if not isinstance(value, bool):
                return ValidationResult(
                    valid=False,
                    field_name=field_name,
                    error_message=f"{field_name} must be a boolean",
                )

        return ValidationResult(valid=True, field_name=field_name, error_message=None)
