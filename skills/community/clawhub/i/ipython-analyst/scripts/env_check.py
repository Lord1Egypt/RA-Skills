"""
env_check.py — Verify installed packages and extract imports from scripts.

Bug fix vs v6:
- `verify_environment` now passes correct import names. v6 lowercased package
  names so `'PIL'` became `'pil'` (not a valid module) and `'cv2'` stayed as
  `'cv2'` only by luck. v7 uses an explicit name map so Pillow is checked as
  `'PIL'`, opencv as `'cv2'`, sklearn as `'sklearn'`, etc.
- `_check_package` no longer mangles the name; it imports what it's given.
"""
from __future__ import annotations

import ast
import importlib
from dataclasses import dataclass
from typing import Optional


# Map "package name" (PyPI distribution) → "import name" (what you `import`).
# Most packages match (numpy → numpy), but some diverge significantly.
PACKAGE_TO_IMPORT = {
    "pillow": "PIL",
    "opencv-python": "cv2",
    "opencv-contrib-python": "cv2",
    "scikit-learn": "sklearn",
    "pyyaml": "yaml",
    "beautifulsoup4": "bs4",
    "python-dateutil": "dateutil",
    "python-dotenv": "dotenv",
    "pydantic": "pydantic",
    "protobuf": "google.protobuf",
}


@dataclass
class RequirementStatus:
    name: str
    installed: bool
    version: Optional[str]
    required_version: Optional[str]
    status: str  # 'ok', 'missing', 'version_mismatch', 'unknown'


def check_requirements(
    script_path: Optional[str] = None,
    requirements: Optional[dict[str, str]] = None,
    verbose: bool = False,
) -> dict:
    """Check whether required packages are installed with correct versions.

    Args:
        script_path: Path to a Python script to scan for imports (optional).
        requirements: Dict of {package_name: version_spec} (optional).
        verbose: Print per-package status.

    Returns dict with 'status', 'missing', 'mismatches', 'details'.
    """
    if script_path and requirements is None:
        requirements = _extract_imports(script_path)

    if requirements is None:
        return {"status": "no_requirements", "details": []}

    results = []
    for package, version_spec in requirements.items():
        status = _check_package(package, version_spec)
        results.append(status)
        if verbose:
            version_info = f" (need {version_spec})" if version_spec else ""
            print(f"{package}: {status.status}{version_info}")

    missing = [r for r in results if r.status == "missing"]
    mismatches = [r for r in results if r.status == "version_mismatch"]

    return {
        "status": "ok" if not missing and not mismatches else "issues",
        "missing": [r.name for r in missing],
        "mismatches": [
            {"name": r.name, "installed": r.version, "required": r.required_version}
            for r in mismatches
        ],
        "details": results,
    }


def _extract_imports(script_path: str) -> dict[str, str]:
    """Extract top-level package names from a Python script's imports.

    Returns {import_name: None} — values are None because we don't track
    version requirements from source alone. Use the explicit name map so
    `import PIL` is reported as 'PIL' (matching what verify_environment expects).
    """
    with open(script_path, encoding="utf-8") as f:
        source = f.read()

    tree = ast.parse(source)
    imports: dict[str, None] = {}

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                base_name = alias.name.split(".")[0]
                imports[base_name] = None
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                base_name = node.module.split(".")[0]
                imports[base_name] = None

    return imports


def _check_package(package: str, version_spec: Optional[str] = None) -> RequirementStatus:
    """Check if a single package is importable, optionally with version check.

    `package` should be the import name (e.g., 'PIL' for Pillow, 'cv2' for
    opencv-python, 'sklearn' for scikit-learn). For PyPI distribution names,
    map them first via PACKAGE_TO_IMPORT.
    """
    import_name = PACKAGE_TO_IMPORT.get(package.lower(), package)

    try:
        mod = importlib.import_module(import_name)
        version = getattr(mod, "__version__", None)

        status = "ok"
        if version_spec and version:
            status = _check_version(version, version_spec)

        return RequirementStatus(package, True, version, version_spec, status)

    except ImportError:
        return RequirementStatus(package, False, None, version_spec, "missing")


def _check_version(installed: str, spec: str) -> str:
    """Check installed version against a spec like '>=1.0', '==2.5', '<=3.0'."""
    try:
        from packaging.version import Version
        installed_v = Version(installed)

        for op, prefix in [(">=", ">="), ("==", "=="), ("<=", "<="), (">", ">"), ("<", "<")]:
            if spec.startswith(op):
                required = spec[len(op):].strip()
                required_v = Version(required)
                if op == ">=" and not installed_v >= required_v: return "version_mismatch"
                if op == "==" and not installed_v == required_v: return "version_mismatch"
                if op == "<=" and not installed_v <= required_v: return "version_mismatch"
                if op == ">"  and not installed_v >  required_v: return "version_mismatch"
                if op == "<"  and not installed_v <  required_v: return "version_mismatch"
                return "ok"
        return "ok"  # Unknown spec format, assume ok
    except ImportError:
        # packaging not available — fall back to string compare
        for op in [">=", "==", "<="]:
            if spec.startswith(op):
                required = spec[len(op):].strip()
                if op == ">=" and not installed >= required: return "version_mismatch"
                if op == "==" and not installed == required: return "version_mismatch"
                if op == "<=" and not installed <= required: return "version_mismatch"
        return "ok"


def verify_environment(packages: Optional[list[str]] = None, verbose: bool = False) -> dict:
    """Verify that common data science packages are available.

    Args:
        packages: List of import names to check. Defaults to common set.
        verbose: Print per-package status.

    Returns dict with verification results.
    """
    if packages is None:
        # Use import names (not PyPI distribution names) so _check_package
        # can directly import them.
        packages = [
            "pandas", "numpy", "matplotlib", "seaborn",
            "scipy", "sklearn", "torch", "networkx",
            "PIL", "cv2", "tqdm", "dask",
        ]

    return check_requirements(
        requirements={p: None for p in packages}, verbose=verbose
    )


__all__ = ["check_requirements", "verify_environment", "RequirementStatus"]
