"""Deterministic runtime capability preflight.

Host tools are deliberately not discovered here.  An agent must pass the
capabilities it actually has (``search``, ``browse``, and ``vision``) so a
report cannot accidentally claim access to a host integration.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from collections.abc import Callable, Iterable
from pathlib import Path

if __package__ in (None, ""):
    # ``python scripts/preflight.py`` puts ``scripts/`` rather than the
    # repository root on sys.path.  Add the root only for this direct CLI
    # invocation; module execution already has the correct import path.
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.contracts import CapabilityReport, CapabilityTier


HOST_CAPABILITIES = ("search", "browse", "vision")
OPTIONAL_MODULES = ("docx", "openpyxl", "pdfplumber")
MINIMUM_PYTHON = (3, 10)


def _default_module_probe(module_name: str) -> bool:
    """Return whether *module_name* has an import spec.

    ``find_spec`` intentionally checks availability without importing or
    executing the optional package.  Exceptions are handled by
    ``detect_capabilities`` so the report can identify the affected module
    and exception type without exposing the exception message.
    """

    return importlib.util.find_spec(module_name) is not None


def _python_version() -> tuple[str, bool]:
    """Return a stable version string and whether this runtime is supported."""

    version_info = sys.version_info
    major = int(version_info[0])
    minor = int(version_info[1])
    micro = int(version_info[2]) if len(version_info) > 2 else 0
    return f"{major}.{minor}.{micro}", (major, minor) >= MINIMUM_PYTHON


def _degradation_messages(
    missing: Iterable[str],
    *,
    offline: bool,
    unsupported_python: bool,
    probe_failures: Iterable[tuple[str, str]],
) -> tuple[str, ...]:
    missing_names = tuple(sorted(set(missing)))
    messages = [f"missing capability: {name}" for name in missing_names]
    if offline:
        missing_network = tuple(
            name for name in ("search", "browse") if name in missing_names
        )
        if missing_network:
            messages.append(
                "offline mode: missing network capabilities: "
                + ", ".join(missing_network)
            )
    if unsupported_python:
        messages.append("python<3.10: runtime is below the supported minimum")
    messages.extend(
        f"module probe failed: {module} ({exception_type})"
        for module, exception_type in sorted(probe_failures)
    )
    return tuple(messages)


def detect_capabilities(
    host_capabilities: set[str],
    module_probe: Callable[[str], bool] | None = None,
) -> CapabilityReport:
    """Detect optional parsers and select a full, standard, or offline tier.

    ``host_capabilities`` is an explicit declaration from the calling agent;
    this function never tries to infer network or vision access.  ``module_probe``
    is injectable so tests and hosts can provide a deterministic import check.
    """

    probe = _default_module_probe if module_probe is None else module_probe
    # Ignore unknown declarations rather than allowing them to affect tier
    # selection.  Sorting all serialized collections keeps output identical
    # across platforms and set iteration orders.
    declared = {name for name in host_capabilities if name in HOST_CAPABILITIES}
    host = tuple(sorted(declared))

    available_module_names = []
    missing_module_names = []
    probe_failures = []
    for name in OPTIONAL_MODULES:
        try:
            available = bool(probe(name))
        except Exception as exc:
            # A broken finder/package must degrade only that module.  Do not
            # catch BaseException: KeyboardInterrupt and SystemExit remain
            # process-control signals rather than capability results.
            available = False
            probe_failures.append((name, type(exc).__name__))
        if available:
            available_module_names.append(name)
        else:
            missing_module_names.append(name)
    available_modules = tuple(sorted(available_module_names))
    missing_modules = tuple(sorted(missing_module_names))
    missing_host = tuple(sorted(set(HOST_CAPABILITIES) - declared))
    missing = tuple(sorted((*missing_host, *missing_modules)))
    python_version, supported_python = _python_version()
    if not supported_python:
        missing = tuple(sorted((*missing, "python>=3.10")))

    has_network = {"search", "browse"}.issubset(declared)
    has_parsers = not missing_modules
    has_vision = "vision" in declared
    if has_network and has_vision and has_parsers and supported_python:
        tier = CapabilityTier.FULL
    elif "browse" in declared and supported_python:
        # A page reader can verify known official URLs without a search API.
        # Search-only snippets still cannot replace opened source evidence.
        tier = CapabilityTier.STANDARD
    else:
        tier = CapabilityTier.OFFLINE

    degradations = _degradation_messages(
        missing,
        offline=tier is CapabilityTier.OFFLINE,
        unsupported_python=not supported_python,
        probe_failures=probe_failures,
    )
    return CapabilityReport(
        tier=tier,
        host_capabilities=host,
        available_capabilities=host,
        missing_capabilities=missing,
        degradations=degradations,
        python_version=python_version,
        optional_modules=available_modules,
    )


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--host-capability",
        action="append",
        default=[],
        metavar="NAME",
        help="explicit host capability (repeat for search, browse, or vision)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    report = detect_capabilities(set(args.host_capability))
    print(json.dumps(report.to_dict(), ensure_ascii=False, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
