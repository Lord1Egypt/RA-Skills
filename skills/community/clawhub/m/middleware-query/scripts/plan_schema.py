#!/usr/bin/env python3
import json
from pathlib import Path
from typing import List, Tuple

SCHEMA_PATH = Path(__file__).resolve().parent.parent / "references" / "plan-schema.json"


def load_schema() -> dict:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def validate_with_schema(plan: dict) -> Tuple[bool, List[str]]:
    """Validate with jsonschema if installed; fallback to light checks."""
    errors: list[str] = []
    try:
        import jsonschema  # type: ignore

        schema = load_schema()
        validator = jsonschema.Draft202012Validator(schema)
        for err in validator.iter_errors(plan):
            path = ".".join([str(p) for p in err.absolute_path])
            errors.append(f"{path or '$'}: {err.message}")
        return (len(errors) == 0, errors)
    except Exception:
        # fallback minimal validation
        for k in ["datasource", "profile", "action"]:
            if k not in plan:
                errors.append(f"missing required field: {k}")
        if plan.get("datasource") == "mysql" and "sql" not in plan:
            errors.append("mysql requires sql")
        if plan.get("datasource") == "mongo" and "collection" not in plan:
            errors.append("mongo requires collection")
        return (len(errors) == 0, errors)
