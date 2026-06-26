#!/usr/bin/env python3
"""
DGRA Pseudogene Synchronization — v0.6 P0

GENCODE-driven pseudogene database builder.

Design principles:
- Non-blocking: network failures fall back to existing JSON
- TTL caching: default 30 days (GENCODE release cycle is 3-6 months)
- Offline mode: skip download, use last cached JSON
- Audit logging: every sync writes a log file
"""

import json
import asyncio
import gzip
import os
import re
import shutil
import tempfile
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any

# =============================================================================
# Streaming download helpers
# =============================================================================

def _download_gtf_streaming(url: str, output_path: Path, chunk_size: int = 8192) -> Path:
    """
    Stream-download GTF.gz with progress logging and resume support.
    Uses small chunks to reduce memory pressure.
    """
    import urllib.request

    # Check for partial download (resume)
    existing_size = 0
    headers = {}
    if output_path.exists():
        existing_size = output_path.stat().st_size
        if existing_size > 0:
            headers['Range'] = f'bytes={existing_size}-'
            print(f"[DGRA] Resuming download from {existing_size / 1024 / 1024:.1f} MB")

    req = urllib.request.Request(url, headers=headers)
    downloaded = existing_size
    last_mb = existing_size // (10 * 1024 * 1024)
    mode = 'ab' if existing_size > 0 else 'wb'

    with urllib.request.urlopen(req) as response:
        # Handle 206 Partial Content (resume) or 200 OK (new)
        if response.status not in (200, 206):
            raise RuntimeError(f"HTTP {response.status}: download failed")

        total_size = int(response.headers.get("Content-Length", 0)) + existing_size
        with open(output_path, mode) as f:
            while True:
                chunk = response.read(chunk_size)
                if not chunk:
                    break
                f.write(chunk)
                downloaded += len(chunk)
                mb = downloaded // (10 * 1024 * 1024)
                if mb > last_mb:
                    last_mb = mb
                    total_mb = total_size / (1024 * 1024) if total_size else 0
                    print(f"[DGRA] Downloaded {downloaded / 1024 / 1024:.1f} MB / {total_mb:.1f} MB")

    return output_path


# =============================================================================
# Constants
# =============================================================================

GENCODE_GTF_URL = (
    "http://ftp.ebi.ac.uk/pub/databases/gencode/"
    "Gencode_human/release_48/gencode.v48.annotation.gtf.gz"
)
GENCODE_RELEASE = "48"
PSEUDOGENE_TTL_DAYS = 30


# =============================================================================
# GTF Parsing helpers
# =============================================================================

def _parse_gtf_attributes(attr_str: str) -> Dict[str, str]:
    """Parse GTF attribute column (key \"value\"; key \"value\"; ...)."""
    attrs = {}
    parts = attr_str.strip().split(";")
    for part in parts:
        part = part.strip()
        if not part:
            continue
        if " " in part:
            key, _, value = part.partition(" ")
            value = value.strip().strip('"')
            attrs[key] = value
    return attrs


def _infer_parent_gene(pseudogene_name: str, gene_type: str) -> Optional[str]:
    """
    Heuristic inference of parent gene for processed pseudogenes.

    Naming conventions observed in GENCODE:
      - GUSBP1, GUSBP2  → GUSB
      - CICP27          → CIC
      - PDZD2P1         → PDZD2
      - HNRNPCL1        → HNRNPC (this one is tricky)
      - SURF6P1         → SURF6

    Strategy (ordered):
      1. Strip trailing 'P' + digits:  XXXP123 → XXX
      2. Strip trailing 'P' only:      XXXP    → XXX
      3. For 'unprocessed_pseudogene', no reliable parent inference

    Returns None if no confident parent can be inferred.
    """
    if "unprocessed" in gene_type:
        return None

    # Pattern 1: strip trailing P + digits (e.g., GUSBP1 → GUSB, CICP27 → CIC)
    m = re.match(r'^([A-Z0-9]+?)P\d+$', pseudogene_name)
    if m:
        return m.group(1)

    # Pattern 2: strip trailing P only
    m = re.match(r'^([A-Z0-9]+)P$', pseudogene_name)
    if m:
        return m.group(1)

    return None


# =============================================================================
# Core sync function
# =============================================================================

async def sync_gencode_pseudogenes(
    references_dir: Optional[Path] = None,
    force: bool = False,
    ttl_days: int = PSEUDOGENE_TTL_DAYS,
) -> Path:
    """
    Download and parse GENCODE v48 pseudogene annotations.

    Writes references/gencode_pseudogenes.json with:
      - pseudogenes: list of all pseudogene records
      - parent_pseudogene_pairs: mapping of inferred parent → pseudogenes

    Args:
        references_dir: Directory for output JSON (default: ../../references)
        force: Force re-download even if TTL not expired
        ttl_days: Time-to-live for cached JSON

    Returns:
        Path to generated gencode_pseudogenes.json

    Non-blocking: network failures fall back to existing JSON if present.
    """
    if references_dir is None:
        references_dir = Path(__file__).parent.parent / "references"

    references_dir.mkdir(parents=True, exist_ok=True)
    output_path = references_dir / "gencode_pseudogenes.json"
    log_dir = references_dir.parent / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    def _log(event_type: str, msg: str) -> None:
        ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        log_file = log_dir / f"gencode_pseudogene_sync_{datetime.utcnow().strftime('%Y-%m-%d')}.log"
        try:
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(f"[{ts}] [{event_type}] {msg}\n")
        except Exception:
            pass

    # v0.6 A-layer: check build state for resume
    try:
        from dgra_build_state import is_step_complete
        if is_step_complete("pseudogene_sync") and output_path.exists():
            _log("STATE_RESUME", "pseudogene_sync already complete, skipping")
            return output_path
    except Exception:
        pass  # Best-effort, don't fail on state read errors

    # Check TTL
    if not force and output_path.exists():
        mtime = datetime.fromtimestamp(output_path.stat().st_mtime)
        age_days = (datetime.utcnow() - mtime).total_seconds() / 86400
        if age_days < ttl_days:
            _log("SKIP", f"gencode_pseudogenes.json up to date (age={age_days:.1f}d < TTL={ttl_days}d)")
            return output_path
        else:
            _log("TTL_EXPIRED", f"age={age_days:.1f}d >= TTL={ttl_days}d, re-syncing")

    # Download GTF with streaming + resume support
    temp_dir = Path(tempfile.mkdtemp(prefix="dgra_gencode_"))
    gtf_gz_path = temp_dir / "gencode.v48.annotation.gtf.gz"

    _log("DOWNLOAD_START", f"URL={GENCODE_GTF_URL}, output={gtf_gz_path}")
    try:
        _download_gtf_streaming(GENCODE_GTF_URL, gtf_gz_path)
        _log("DOWNLOAD_OK", f"path={gtf_gz_path}, size={gtf_gz_path.stat().st_size}")
    except Exception as e:
        _log("DOWNLOAD_FAILED", str(e))
        # Fallback to existing JSON
        if output_path.exists():
            _log("FALLBACK", f"Using existing {output_path}")
            return output_path
        raise RuntimeError(f"GENCODE download failed and no fallback exists: {e}")

    # Parse GTF
    pseudogenes = []
    parent_map: Dict[str, List[str]] = {}
    line_count = 0

    try:
        with gzip.open(gtf_gz_path, "rt", encoding="utf-8") as f:
            for line in f:
                line_count += 1
                if line.startswith("#"):
                    continue
                parts = line.strip().split("\t")
                if len(parts) < 9:
                    continue
                if parts[2] != "gene":
                    continue

                attrs = _parse_gtf_attributes(parts[8])
                gene_type = attrs.get("gene_type", "")

                if "pseudogene" not in gene_type:
                    continue

                gene_name = attrs.get("gene_name", "")
                raw_gene_id = attrs.get("gene_id", "")
                gene_id = raw_gene_id.split(".")[0] if raw_gene_id else raw_gene_id
                chrom = parts[0]
                start = int(parts[3])
                end = int(parts[4])
                strand = parts[6]

                parent_gene = _infer_parent_gene(gene_name, gene_type)

                pg = {
                    "gene_name": gene_name,
                    "gene_id": gene_id,
                    "chr": chrom,
                    "start": start,
                    "end": end,
                    "strand": strand,
                    "type": gene_type,
                    "parent_gene": parent_gene,
                }
                pseudogenes.append(pg)

                if parent_gene and gene_name:
                    if parent_gene not in parent_map:
                        parent_map[parent_gene] = []
                    if gene_name not in parent_map[parent_gene]:
                        parent_map[parent_gene].append(gene_name)

        _log("PARSE_OK", f"lines={line_count}, pseudogenes={len(pseudogenes)}, parent_pairs={len(parent_map)}")
    except Exception as e:
        _log("PARSE_FAILED", str(e))
        # Fallback to existing JSON
        if output_path.exists():
            _log("FALLBACK", f"Using existing {output_path}")
            return output_path
        raise
    finally:
        # Cleanup temp
        shutil.rmtree(temp_dir, ignore_errors=True)

    # Build and write output
    output = {
        "version": GENCODE_RELEASE,
        "release": f"GENCODE v{GENCODE_RELEASE}",
        "source_url": GENCODE_GTF_URL,
        "generated_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "ttl_days": ttl_days,
        "total_pseudogenes": len(pseudogenes),
        "pseudogenes": pseudogenes,
        "parent_pseudogene_pairs": parent_map,
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    _log("WRITE_OK", f"path={output_path}, total={len(pseudogenes)}")
    print(f"[DGRA] GENCODE pseudogene sync complete: {len(pseudogenes)} pseudogenes, {len(parent_map)} parent genes")

    # v0.6 A-layer: persist build state
    try:
        from dgra_build_state import save_state
        save_state("pseudogene_sync", {
            "status": "complete",
            "genes_synced": len(pseudogenes),
            "parent_pairs": len(parent_map),
            "file": str(output_path),
            "release": GENCODE_RELEASE,
        })
    except Exception:
        pass  # Build state is best-effort

    return output_path


def sync_gencode_pseudogenes_sync(
    references_dir: Optional[Path] = None,
    force: bool = False,
    ttl_days: int = PSEUDOGENE_TTL_DAYS,
) -> Path:
    """Synchronous wrapper for sync_gencode_pseudogenes()."""
    return asyncio.run(sync_gencode_pseudogenes(references_dir, force, ttl_days))


# =============================================================================
# Query / Lookup API
# =============================================================================

_GENCODE_PSEUDOGENE_DB: Optional[Dict] = None

def load_gencode_pseudogenes(references_dir: Optional[Path] = None) -> Dict:
    """
    Load gencode_pseudogenes.json into memory.
    Returns dict with 'pseudogenes' list and 'parent_pseudogene_pairs' mapping.
    Falls back to empty dict if file missing.
    """
    global _GENCODE_PSEUDOGENE_DB
    if _GENCODE_PSEUDOGENE_DB is not None:
        return _GENCODE_PSEUDOGENE_DB

    if references_dir is None:
        references_dir = Path(__file__).parent.parent / "references"

    path = references_dir / "gencode_pseudogenes.json"
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        _GENCODE_PSEUDOGENE_DB = data
        pairs = data.get("parent_pseudogene_pairs", {})
        print(f"[DGRA] Loaded GENCODE pseudogenes: {len(data.get('pseudogenes', []))} entries, {len(pairs)} parent-pseudogene mappings")
        return _GENCODE_PSEUDOGENE_DB
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"[DGRA] INFO: gencode_pseudogenes.json not found ({e}). GENCODE pseudogene detection unavailable.")
        _GENCODE_PSEUDOGENE_DB = {}
        return _GENCODE_PSEUDOGENE_DB


def get_pseudogenes_for_gene(gene: str, references_dir: Optional[Path] = None) -> List[str]:
    """
    Return list of known GENCODE pseudogenes for a given functional gene.

    Args:
        gene: Functional gene symbol (e.g., "VWF")

    Returns:
        List of pseudogene names (deduplicated)
    """
    db = load_gencode_pseudogenes(references_dir)
    pairs = db.get("parent_pseudogene_pairs", {})
    return list(dict.fromkeys(pairs.get(gene, [])))


def is_gencode_pseudogene(gene_symbol: str, references_dir: Optional[Path] = None) -> bool:
    """
    Check if a gene symbol is annotated as a pseudogene in GENCODE.

    Args:
        gene_symbol: Gene symbol to check

    Returns:
        True if the symbol appears in GENCODE pseudogene list
    """
    db = load_gencode_pseudogenes(references_dir)
    for pg in db.get("pseudogenes", []):
        if pg.get("gene_name") == gene_symbol:
            return True
    return False


# =============================================================================
# __main__ test entry point
# =============================================================================

if __name__ == "__main__":
    # Quick sanity test when run standalone
    print("Testing GENCODE pseudogene sync...")
    path = sync_gencode_pseudogenes_sync(force=True)
    print(f"Output: {path}")

    import json
    with open(path) as f:
        data = json.load(f)
    print(f"Total pseudogenes: {data['total_pseudogenes']}")
    print(f"Parent pairs: {len(data['parent_pseudogene_pairs'])}")

    # Check some known genes
    pairs = data["parent_pseudogene_pairs"]
    for g in ["VWF", "GUSB", "CIC", "PMS2", "GBA"]:
        if g in pairs:
            print(f"  {g}: {pairs[g]}")

    print("Done.")
