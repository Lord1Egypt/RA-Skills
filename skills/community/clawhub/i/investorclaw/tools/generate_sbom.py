# SPDX-License-Identifier: Apache-2.0
"""Generate an SPDX 2.3 SBOM for the ic-engine container.

Reads:
  /tmp/ic-engine-bom-raw.json   — importlib.metadata dump from container
  /tmp/ic-engine-sizes.txt      — `du -sm` per site-packages dir

Writes:
  ic-engine-4.0-cpu.spdx.json   — SPDX 2.3 JSON SBOM
  ic-engine-4.0-cpu.bom.md      — human-readable trim audit table

The SBOM follows SPDX 2.3 (https://spdx.github.io/spdx-spec/v2.3/).
"""
from __future__ import annotations

import datetime
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

# ── inputs ──────────────────────────────────────────────────────────
RAW_BOM = Path("/tmp/ic-engine-bom-raw.json")
SIZES = Path("/tmp/ic-engine-sizes.txt")

# ── outputs ─────────────────────────────────────────────────────────
OUT_DIR = Path(__file__).resolve().parent.parent / "sbom"
OUT_DIR.mkdir(exist_ok=True)
SPDX_OUT = OUT_DIR / "ic-engine-4.0-cpu.spdx.json"
MD_OUT = OUT_DIR / "ic-engine-4.0-cpu.bom.md"

# Image identity
IMAGE_NAME = "mnemos-os/ic-engine"
IMAGE_TAG = "4.0-cpu"
IMAGE_DIGEST = "sha256:0510c3016f03fe35d7c59b8433a6494253de1892cce2be2029a0e5974b9d1e03"
IMAGE_SIZE_GB = 2.27

# ── load ────────────────────────────────────────────────────────────


def load_pkgs() -> list[dict[str, Any]]:
    return json.loads(RAW_BOM.read_text())


def load_sizes() -> dict[str, int]:
    """Map package-name (lowercased, normalized) -> size in MB."""
    out: dict[str, int] = {}
    for line in SIZES.read_text().splitlines():
        if not line.strip():
            continue
        size_str, path = line.split(maxsplit=1)
        try:
            size = int(size_str)
        except ValueError:
            continue
        # path is like .../site-packages/numpy or .../numpy-2.4.1.dist-info
        name = Path(path).name
        # Strip dist-info suffix
        name = re.sub(r"-[0-9].*\.dist-info$", "", name)
        # Normalize: lowercase, replace _ with -
        key = name.lower().replace("_", "-")
        # Sum sizes for namespace + dist-info
        out[key] = out.get(key, 0) + size
    return out


# ── license normalization ───────────────────────────────────────────
# Map common free-form license strings to SPDX identifiers.
LICENSE_MAP = {
    "apache 2.0": "Apache-2.0",
    "apache-2.0": "Apache-2.0",
    "apache 2": "Apache-2.0",
    "apache license 2.0": "Apache-2.0",
    "apache license, version 2.0": "Apache-2.0",
    "apache software license": "Apache-2.0",
    "mit": "MIT",
    "mit license": "MIT",
    "mit-cmu": "MIT-CMU",
    "bsd": "BSD-3-Clause",
    "bsd-2-clause": "BSD-2-Clause",
    "bsd-3-clause": "BSD-3-Clause",
    "bsd 3-clause": "BSD-3-Clause",
    "bsd license": "BSD-3-Clause",
    "lgpl": "LGPL-3.0-or-later",
    "lgplv3": "LGPL-3.0-only",
    "gpl": "GPL-3.0-or-later",
    "gplv3": "GPL-3.0-only",
    "gplv2": "GPL-2.0-only",
    "psf": "Python-2.0",
    "python software foundation license": "Python-2.0",
    "python-2.0": "Python-2.0",
    "isc": "ISC",
    "mpl": "MPL-2.0",
    "mpl-2.0": "MPL-2.0",
    "unlicense": "Unlicense",
    "0bsd": "0BSD",
    "zlib": "Zlib",
    "cc0": "CC0-1.0",
    "cc-by-4.0": "CC-BY-4.0",
}


def normalize_license(pkg: dict[str, Any]) -> str:
    """Pick the best SPDX license identifier from the metadata fields.

    Order: License-Expression (if SPDX-formatted) > Classifier > License.
    Returns 'NOASSERTION' if nothing usable.
    """
    expr = (pkg.get("license_expression") or "").strip()
    if expr:
        # PEP 639 license expressions are already SPDX-formatted
        return expr

    classifiers = pkg.get("classifiers", [])
    for c in classifiers:
        # e.g. "License :: OSI Approved :: Apache Software License"
        m = re.match(r"License :: (?:OSI Approved :: )?(.+)", c)
        if not m:
            continue
        name = m.group(1).strip().lower()
        spdx = LICENSE_MAP.get(name)
        if spdx:
            return spdx
        # Try secondary lookups
        for k, v in LICENSE_MAP.items():
            if k in name:
                return v

    raw = (pkg.get("license") or "").strip()
    if raw:
        # Sometimes license field is the full text — first line is the hint
        first_line = raw.splitlines()[0].strip().lower()
        spdx = LICENSE_MAP.get(first_line)
        if spdx:
            return spdx
        for k, v in LICENSE_MAP.items():
            if k in first_line:
                return v

    return "NOASSERTION"


# ── trim-candidate scoring ──────────────────────────────────────────
# Packages with high size and low utility for ic-engine's deterministic
# portfolio path. These are the audit candidates for the engine maintainer.

TRIM_CANDIDATES = {
    # ML / NLP — dragged in by clio's vision/schema-mapping; only used when
    # parsing unfamiliar PDF formats that fall through camelot+pdfplumber.
    # Could be made lazy or replaced with regex parsers for known broker formats.
    "torch": "ML — used only by clio vision-extract; lazy-load or replace with regex parsers",
    "transformers": "NLP — clio schema-mapping models; consider rule-based mapper for top brokers",
    "sentence-transformers": "Embeddings — does ic-engine actually compute embeddings? Confirm usage.",
    "tokenizers": "Transitive of transformers; goes if transformers goes",
    "huggingface-hub": "Transitive of transformers; goes if transformers goes",
    "safetensors": "Transitive of transformers; goes if transformers goes",
    "regex": "Transitive of transformers; goes if transformers goes",
    "tiktoken": "OpenAI tokenizer — used by litellm? Check call sites",
    # Vision / OCR — used by clio for table extraction from PDFs
    "opencv-python-headless": "Used by clio table-extract from PDFs; could move behind feature flag",
    # Math / optimization — cvxpy stack is for portfolio optimization
    "cvxpy": "Portfolio optimization — keep, this is core",
    "ecos": "cvxpy solver — keep",
    "scs": "cvxpy solver — keep",
    "clarabel": "cvxpy solver — keep",
    "osqp": "cvxpy solver — keep",
    # PDF parsing — used by clio
    "pymupdf": "PDF text extraction — used by clio; likely needed",
    "pdfplumber": "PDF table extraction — used by clio; likely needed",
    "camelot-py": "PDF table extraction — used by clio; likely needed",
    "tabula-py": "PDF table extraction (Java backend) — used by clio; consider dropping if camelot/pdfplumber suffice",
    "pdfminer-six": "Transitive of pdfplumber",
    "pypdf2": "PDF — legacy; check if still imported",
    # LLM gateways — used only for narrative synthesis (rendering/stonkmode.py)
    "litellm": "LLM gateway — only used in rendering/stonkmode.py for narrative; could split into separate `narrative` extra",
    # Polars/pyarrow — likely keep
    "polars": "Fast dataframe — keep, ic-engine uses it",
    "pyarrow": "Transitive of polars and parquet I/O — keep",
}


def trim_label(name: str, size_mb: int) -> str:
    """Return trim-audit annotation for a package, or empty string."""
    return TRIM_CANDIDATES.get(name.lower(), "")


# ── SPDX 2.3 generation ─────────────────────────────────────────────


def package_purl(name: str, version: str) -> str:
    """Build a Package URL (purl) for a Python package."""
    return f"pkg:pypi/{name.lower()}@{version}"


def package_spdxid(name: str) -> str:
    """SPDX ids must match [A-Za-z0-9.\\-]+; normalize aggressively."""
    safe = re.sub(r"[^A-Za-z0-9.\-]", "-", name)
    return f"SPDXRef-Package-{safe}"


def build_spdx(pkgs: list[dict], sizes: dict[str, int]) -> dict:
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    spdx_packages = []
    relationships = []
    root_id = "SPDXRef-Package-ic-engine-image"

    # Root: the container image itself
    spdx_packages.append({
        "SPDXID": root_id,
        "name": f"{IMAGE_NAME}:{IMAGE_TAG}",
        "versionInfo": IMAGE_TAG,
        "downloadLocation": "NOASSERTION",
        "filesAnalyzed": False,
        "licenseConcluded": "Apache-2.0",
        "licenseDeclared": "Apache-2.0",
        "supplier": "Organization: InvestorClaw Contributors",
        "checksums": [
            {"algorithm": "SHA256", "checksumValue": IMAGE_DIGEST.replace("sha256:", "")}
        ],
        "externalRefs": [
            {
                "referenceCategory": "PACKAGE-MANAGER",
                "referenceType": "purl",
                "referenceLocator": f"pkg:oci/{IMAGE_NAME}@{IMAGE_DIGEST}?tag={IMAGE_TAG}",
            }
        ],
        "comment": (
            f"OCI container image. Compressed size: {IMAGE_SIZE_GB} GB. "
            "Wraps ic-engine deterministic portfolio analysis service "
            "behind an MCP-HTTP server."
        ),
    })

    relationships.append({
        "spdxElementId": "SPDXRef-DOCUMENT",
        "relationshipType": "DESCRIBES",
        "relatedSpdxElement": root_id,
    })

    for pkg in sorted(pkgs, key=lambda p: p["name"].lower()):
        name = pkg["name"]
        version = pkg["version"]
        spdx_id = package_spdxid(name)
        purl = package_purl(name, version)
        license_id = normalize_license(pkg)
        size_mb = sizes.get(name.lower().replace("_", "-"), 0)
        trim = trim_label(name, size_mb)

        annotations = []
        if size_mb >= 5:
            annotations.append({
                "annotator": "Tool: generate_sbom.py",
                "annotationDate": now,
                "annotationType": "REVIEW",
                "comment": f"size: {size_mb} MB",
            })
        if trim:
            annotations.append({
                "annotator": "Tool: generate_sbom.py",
                "annotationDate": now,
                "annotationType": "REVIEW",
                "comment": f"trim-audit: {trim}",
            })

        entry = {
            "SPDXID": spdx_id,
            "name": name,
            "versionInfo": version,
            "downloadLocation": pkg.get("home") or "NOASSERTION",
            "filesAnalyzed": False,
            "licenseConcluded": "NOASSERTION",
            "licenseDeclared": license_id,
            "supplier": "NOASSERTION",
            "externalRefs": [
                {
                    "referenceCategory": "PACKAGE-MANAGER",
                    "referenceType": "purl",
                    "referenceLocator": purl,
                }
            ],
        }
        if pkg.get("summary"):
            entry["description"] = pkg["summary"]
        if annotations:
            entry["annotations"] = annotations

        spdx_packages.append(entry)
        relationships.append({
            "spdxElementId": root_id,
            "relationshipType": "CONTAINS",
            "relatedSpdxElement": spdx_id,
        })

    doc = {
        "spdxVersion": "SPDX-2.3",
        "dataLicense": "CC0-1.0",
        "SPDXID": "SPDXRef-DOCUMENT",
        "name": f"ic-engine-{IMAGE_TAG}-sbom",
        "documentNamespace": (
            f"https://github.com/mnemos-os/mnemos-ic-runtime/sbom/"
            f"ic-engine-{IMAGE_TAG}-{hashlib.sha256(IMAGE_DIGEST.encode()).hexdigest()[:12]}"
        ),
        "creationInfo": {
            "created": now,
            "creators": [
                "Tool: generate_sbom.py",
                "Organization: InvestorClaw Contributors",
            ],
            "licenseListVersion": "3.24",
        },
        "packages": spdx_packages,
        "relationships": relationships,
    }
    return doc


# ── markdown audit table ────────────────────────────────────────────


def build_markdown(pkgs: list[dict], sizes: dict[str, int]) -> str:
    lines = []
    lines.append(f"# ic-engine v{IMAGE_TAG} — Bill of Materials & Trim Audit\n")
    lines.append(f"**Image:** `{IMAGE_NAME}:{IMAGE_TAG}` ({IMAGE_SIZE_GB} GB compressed)  ")
    lines.append(f"**Digest:** `{IMAGE_DIGEST}`  ")
    lines.append(f"**Generated:** {datetime.datetime.now(datetime.timezone.utc).isoformat()}  ")
    lines.append(f"**Total Python packages:** {len(pkgs)}\n")

    lines.append("## Trim-audit candidates (by size, descending)\n")
    lines.append("These are the high-cost packages flagged for the ic-engine maintainer to review for actual usage. The recommendations are not prescriptive — the maintainer is the source of truth on whether each package is load-bearing for the deterministic-engine path.\n")

    lines.append("| Package | Version | Size (MB) | License | Trim recommendation |")
    lines.append("|---|---|---:|---|---|")

    audit = []
    for pkg in pkgs:
        name = pkg["name"]
        size = sizes.get(name.lower().replace("_", "-"), 0)
        if size < 10:
            continue
        license_id = normalize_license(pkg)
        trim = trim_label(name, size)
        audit.append((name, pkg["version"], size, license_id, trim))

    for name, ver, size, lic, trim in sorted(audit, key=lambda r: -r[2]):
        lines.append(f"| `{name}` | {ver} | {size} | {lic} | {trim or '—'} |")

    lines.append("\n## Full package inventory\n")
    lines.append("| Package | Version | Size (MB) | License |")
    lines.append("|---|---|---:|---|")
    for pkg in sorted(pkgs, key=lambda p: p["name"].lower()):
        name = pkg["name"]
        size = sizes.get(name.lower().replace("_", "-"), 0)
        license_id = normalize_license(pkg)
        size_str = str(size) if size else "—"
        lines.append(f"| `{name}` | {pkg['version']} | {size_str} | {license_id} |")

    return "\n".join(lines) + "\n"


# ── main ────────────────────────────────────────────────────────────


def main() -> int:
    pkgs = load_pkgs()
    sizes = load_sizes()
    print(f"Loaded {len(pkgs)} packages, {len(sizes)} sized dirs", file=sys.stderr)

    spdx = build_spdx(pkgs, sizes)
    SPDX_OUT.write_text(json.dumps(spdx, indent=2))
    print(f"Wrote {SPDX_OUT} ({SPDX_OUT.stat().st_size:,} bytes)", file=sys.stderr)

    md = build_markdown(pkgs, sizes)
    MD_OUT.write_text(md)
    print(f"Wrote {MD_OUT} ({MD_OUT.stat().st_size:,} bytes)", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
