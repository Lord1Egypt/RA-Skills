"""Site settle predicates: GENERIC default + thin last-resort overrides (spec §6)."""
from __future__ import annotations

from typing import Any

from jev_webbridge.predicates import generic as _generic
from jev_webbridge.predicates import github as _github
from jev_webbridge.predicates import perplexity as _perplexity

_GENERIC = _generic.predicate()
_OVERRIDES: dict[str, dict[str, Any]] = {
    "perplexity": _perplexity.predicate(),
    "github": _github.predicate(),
}


def get_predicate(site: str) -> dict[str, Any]:
    """Resolve the settle predicate for a site; unknown sites get the generic default."""
    return _OVERRIDES.get(site, _GENERIC)
