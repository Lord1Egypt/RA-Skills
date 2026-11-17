"""GitHub override: ZERO logic — the generic predicate with only cap_ms lowered."""
from jev_webbridge.predicates.generic import predicate as _generic_predicate

WHY_OVERRIDE = None


def predicate() -> dict:
    return {**_generic_predicate(), "cap_ms": 500}
