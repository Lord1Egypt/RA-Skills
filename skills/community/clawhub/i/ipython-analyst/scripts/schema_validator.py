"""
schema_validator.py — Validate data against declarative schema definitions.

Bug fix vs v6:
- `_validate_field` removed the redundant ternary
  `field.type if not isinstance(field.type, tuple) else field.type`
  (both branches returned the same thing). isinstance() handles tuples
  natively, so just `isinstance(value, field.type)` does the right thing
  for both single types and `(int, float)` tuples.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Optional, Union


@dataclass
class SchemaField:
    """Declarative field spec for SchemaValidator.

    `type` accepts a single type, a tuple of types (any match passes),
    or None (skip type check). Use `min_value`/`max_value` for numerics,
    `pattern` for strings (regex), `enum` for closed-set validation.
    """
    type: Union[type, tuple[type, ...], None] = None
    required: bool = True
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    pattern: Optional[str] = None
    enum: Optional[list[Any]] = None
    description: Optional[str] = None  # for human-readable error messages


class SchemaValidator:
    """Validate nested data against a schema of SchemaField / dict entries.

    Schema can mix SchemaField (leaf validation) and dict (recurse into
    nested object). Errors are categorized as 'error' (hard fail) or
    'warning' (advisory). `validate()` returns {'valid': bool, 'errors': [...]}.
    """

    def __init__(self, schema: dict[str, Any], strict: bool = False):
        self.schema = schema
        self.strict = strict  # if True, unknown keys are errors
        self.errors: list[dict] = []

    def validate(self, data: dict) -> dict[str, Any]:
        self.errors = []
        self._validate(data, self.schema, "")
        hard_errors = [e for e in self.errors if e["severity"] == "error"]
        return {"valid": len(hard_errors) == 0, "errors": self.errors}

    def _validate(self, data: dict, schema: dict, path: str) -> None:
        # Check for unknown keys in strict mode
        if self.strict and isinstance(data, dict):
            for key in data:
                if key not in schema:
                    current_path = f"{path}.{key}" if path else key
                    self.errors.append({
                        "path": current_path,
                        "message": f"Unknown key (strict mode)",
                        "severity": "error",
                    })

        for key, field in schema.items():
            current_path = f"{path}.{key}" if path else key
            if key not in data:
                if isinstance(field, SchemaField) and field.required:
                    self.errors.append({
                        "path": current_path,
                        "message": "Required field missing",
                        "severity": "error",
                    })
                continue

            value = data[key]
            if isinstance(field, SchemaField):
                self._validate_field(value, field, current_path)
            elif isinstance(field, dict):
                if not isinstance(value, dict):
                    self.errors.append({
                        "path": current_path,
                        "message": f"Expected object, got {type(value).__name__}",
                        "severity": "error",
                    })
                else:
                    self._validate(value, field, current_path)

    def _validate_field(self, value: Any, field: SchemaField, path: str) -> None:
        # Type check — isinstance handles tuple of types natively
        if field.type is not None and not isinstance(value, field.type):
            type_name = (
                " | ".join(t.__name__ for t in field.type)
                if isinstance(field.type, tuple)
                else field.type.__name__
            )
            self.errors.append({
                "path": path,
                "message": f"Expected {type_name}, got {type(value).__name__}",
                "severity": "error",
            })

        # Numeric range
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            if field.min_value is not None and value < field.min_value:
                self.errors.append({
                    "path": path,
                    "message": f"Below minimum {field.min_value}",
                    "severity": "warning",
                })
            if field.max_value is not None and value > field.max_value:
                self.errors.append({
                    "path": path,
                    "message": f"Above maximum {field.max_value}",
                    "severity": "warning",
                })

        # String pattern
        if field.pattern is not None and isinstance(value, str):
            if not re.match(field.pattern, value):
                self.errors.append({
                    "path": path,
                    "message": f"Pattern mismatch (expected {field.pattern!r})",
                    "severity": "warning",
                })

        # Enum
        if field.enum is not None and value not in field.enum:
            self.errors.append({
                "path": path,
                "message": f"Not in enum {field.enum}",
                "severity": "error" if self.strict else "warning",
            })


def validate_schema(data: dict, schema: dict, strict: bool = False) -> dict[str, Any]:
    """One-shot schema validation. Returns {valid: bool, errors: [...]}."""
    return SchemaValidator(schema, strict=strict).validate(data)


__all__ = ["SchemaValidator", "SchemaField", "validate_schema"]
