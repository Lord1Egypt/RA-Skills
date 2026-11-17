"""Classify renderer failures caused by a restricted host process.

An installed renderer can be healthy while an agent sandbox blocks an OS service
it initializes. That is operationally different from a missing binary: retrying
the same narrow render through an approved host route is the repair, whereas a
reinstall is unnecessary and can hide the actual cause.
"""
from __future__ import annotations

import pathlib


HOST_EXECUTION_REQUIRED = "HOST_EXECUTION_REQUIRED"


def tectonic_needs_host_execution(engine, log: str) -> bool:
    """Whether Tectonic hit the macOS SystemConfiguration sandbox panic.

    Tectonic's reqwest runtime initializes the system proxy configuration even
    for cached builds. On macOS, a restricted subprocess can deny that API and
    trigger this three-part panic signature. Restricting the classification to
    Tectonic prevents an unrelated LaTeX failure from receiving the wrong fix.
    """
    if pathlib.Path(str(engine)).stem != "tectonic":
        return False
    text = str(log or "").casefold()
    return all(marker in text for marker in (
        "reqwest", "system-configuration", "attempted to create a null object"))
