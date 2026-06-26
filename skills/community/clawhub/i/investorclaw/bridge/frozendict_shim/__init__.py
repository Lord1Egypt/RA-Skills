# SPDX-License-Identifier: Apache-2.0
"""Minimal Apache-2.0 frozendict shim.

Drop-in replacement for the LGPL-3.0 frozendict package. Provides just
enough surface for the consumers in our dependency tree (primarily
yfinance, which does `from frozendict import frozendict` for hash-stable
dict cache keys).

Not a full reimplementation: a dict subclass with mutation methods
raising TypeError plus __hash__ over sorted items. Sufficient for any
caller that uses frozendict as an immutable, hashable mapping.

This shim is installed into site-packages by the runtime Dockerfile
after uninstalling the original LGPL frozendict package, so that
`from frozendict import frozendict` continues to resolve.
"""
from typing import Any

__version__ = "0.0.0-shim"


class frozendict(dict):
    """Hashable, immutable dict. Subclass of dict for max compatibility."""

    __slots__ = ("_hash",)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        object.__setattr__(self, "_hash", None)

    def _readonly(self, *args: Any, **kwargs: Any) -> None:
        raise TypeError(f"{type(self).__name__} is immutable")

    __setitem__ = _readonly
    __delitem__ = _readonly
    pop = _readonly                  # type: ignore[assignment]
    popitem = _readonly              # type: ignore[assignment]
    clear = _readonly                # type: ignore[assignment]
    update = _readonly               # type: ignore[assignment]
    setdefault = _readonly           # type: ignore[assignment]

    def __hash__(self) -> int:       # type: ignore[override]
        if self._hash is None:
            object.__setattr__(self, "_hash", hash(frozenset(self.items())))
        return self._hash  # type: ignore[return-value]

    def copy(self) -> "frozendict":
        return frozendict(self)

    def __repr__(self) -> str:
        return f"frozendict({dict.__repr__(self)})"


# Some consumers import `FrozenOrderedDict` — alias to plain frozendict.
FrozenOrderedDict = frozendict
