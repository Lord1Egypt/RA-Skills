#!/usr/bin/env python3
"""Journal abbreviation lookup tool with multi-source cascade.

Sources (in priority order):
1. JabRef CSV cache (local, ~25K journals, instant)
2. AbbrevISO API (forward only, algorithmic ISO 4)
3. NLM Catalog / Entrez (bidirectional, biomedical journals)

Run `jabbrv --help` for usage and `jabbrv schema` for the full machine-readable
command contract. Stdout is stable JSON when not attached to a TTY; humans on a
terminal get a table/indented view instead.
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import re
import sys
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

CLI_VERSION = "1.0.2"
SCHEMA_VERSION = "1.0.0"

CACHE_DIR = Path(__file__).parent / "cache"

# JabRef CSV files on GitHub (CC0 licensed)
JABREF_BASE = "https://raw.githubusercontent.com/JabRef/abbrv.jabref.org/main/journals"
JABREF_FILES = [
    # ISO 4 (dotted) sources first — these take priority
    "journal_abbreviations_general.csv",
    "journal_abbreviations_lifescience.csv",
    "journal_abbreviations_acs.csv",
    "journal_abbreviations_ams.csv",
    "journal_abbreviations_astronomy.csv",
    "journal_abbreviations_dainst.csv",
    "journal_abbreviations_geology_physics.csv",
    "journal_abbreviations_geology_physics_variations.csv",
    "journal_abbreviations_ieee.csv",
    "journal_abbreviations_ieee_strings.csv",
    "journal_abbreviations_mathematics.csv",
    "journal_abbreviations_mechanical.csv",
    "journal_abbreviations_meteorology.csv",
    "journal_abbreviations_sociology.csv",
    "journal_abbreviations_ubc.csv",
    # MEDLINE (no dots) sources last — used as fallback
    "journal_abbreviations_entrez.csv",
    "journal_abbreviations_medicus.csv",
]

# Exit codes (documented, stable, distinct per failure class)
EXIT_OK = 0
EXIT_RUNTIME = 1      # upstream error, I/O error, unexpected exception
EXIT_VALIDATION = 2   # bad argv, missing input file, invalid flag combination
EXIT_NOT_FOUND = 3    # the looked-up journal does not exist in any source

# Per-process cache telemetry — surfaced in envelope.meta so agents can detect
# silent cache degradation without a separate command
_cache_stats: dict[str, Any] = {
    "files_loaded": 0,
    "files_missing": [],
    "files_failed": [],
    "fetched_this_run": 0,
}

# Rate limiting
_last_abbreviso_time = 0.0
_last_nlm_time = 0.0
_ABBREVISO_GAP = 1.0
_NLM_GAP = 0.35  # ~3 req/sec


# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------

def _fetch(url: str, timeout: int = 15) -> str:
    req = Request(url, headers={"User-Agent": f"jabbrv/{CLI_VERSION} (journal-abbrev-skill)"})
    with urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8")


def _fetch_json(url: str, timeout: int = 15) -> Any:
    return json.loads(_fetch(url, timeout))


# ---------------------------------------------------------------------------
# Cache
# ---------------------------------------------------------------------------

def ensure_cache(verbose: bool = True) -> None:
    """Download any JabRef CSV files not present on disk. Idempotent.

    Resets `files_failed` and `fetched_this_run` before running so telemetry
    reflects this invocation only.
    """
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    _cache_stats["files_failed"] = []
    _cache_stats["fetched_this_run"] = 0
    for fname in JABREF_FILES:
        fpath = CACHE_DIR / fname
        if fpath.exists():
            continue
        url = f"{JABREF_BASE}/{fname}"
        if verbose:
            print(f"  Downloading {fname}...", file=sys.stderr)
        try:
            data = _fetch(url, timeout=30)
            fpath.write_text(data, encoding="utf-8")
            _cache_stats["fetched_this_run"] += 1
        except (HTTPError, URLError, TimeoutError) as e:
            _cache_stats["files_failed"].append({"file": fname, "error": str(e)})
            if verbose:
                print(f"  Warning: failed to download {fname}: {e}", file=sys.stderr)


def load_cache() -> tuple[dict, dict]:
    """Parse all present JabRef CSVs into lookup dicts. Does NOT fetch."""
    full_to_abbrev: dict = {}
    abbrev_to_full: dict = {}

    loaded = 0
    missing: list[str] = []
    for fname in JABREF_FILES:
        fpath = CACHE_DIR / fname
        if not fpath.exists():
            missing.append(fname)
            continue
        loaded += 1
        text = fpath.read_text(encoding="utf-8", errors="replace")
        # JabRef CSVs use comma delimiter with quoted fields
        reader = csv.reader(io.StringIO(text))
        for row in reader:
            if len(row) < 2 or row[0].startswith("#"):
                continue
            full = row[0].strip()
            abbrev = row[1].strip()
            if not full or not abbrev:
                continue
            nf = _normalize(full)
            na = _normalize(abbrev)
            if nf not in full_to_abbrev:
                full_to_abbrev[nf] = (full, abbrev)
            if na not in abbrev_to_full:
                abbrev_to_full[na] = (abbrev, full)

    _cache_stats["files_loaded"] = loaded
    _cache_stats["files_missing"] = missing
    return full_to_abbrev, abbrev_to_full


def _normalize(s: str) -> str:
    """Normalize for case-insensitive matching."""
    s = s.lower().strip()
    s = re.sub(r"^the\s+", "", s)
    s = s.replace("&", "and")
    s = re.sub(r"\s+", " ", s)
    return s


_cache: tuple[dict, dict] | None = None


def _get_cache() -> tuple[dict, dict]:
    global _cache
    if _cache is None:
        ensure_cache()
        _cache = load_cache()
    return _cache


# ---------------------------------------------------------------------------
# Local lookup
# ---------------------------------------------------------------------------

def lookup_local(query: str) -> dict | None:
    full_to_abbrev, abbrev_to_full = _get_cache()
    nq = _normalize(query)

    if nq in full_to_abbrev:
        full, abbrev = full_to_abbrev[nq]
        return {
            "query": query, "full": full, "abbreviation": abbrev,
            "direction": "abbreviate", "source": "JabRef",
        }

    if nq in abbrev_to_full:
        abbrev, full = abbrev_to_full[nq]
        return {
            "query": query, "full": full, "abbreviation": abbrev,
            "direction": "expand", "source": "JabRef",
        }

    return None


def fuzzy_search(query: str) -> list[dict]:
    """Return ALL matching results, sorted by relevance. Caller slices for pagination."""
    full_to_abbrev, abbrev_to_full = _get_cache()
    nq = _normalize(query)
    terms = nq.split()
    results: list[dict] = []
    seen_full: set[str] = set()

    def _matches(text: str) -> bool:
        return all(t in text for t in terms)

    for nf, (full, abbrev) in full_to_abbrev.items():
        if _matches(nf) and full not in seen_full:
            seen_full.add(full)
            results.append({"full": full, "abbreviation": abbrev, "source": "JabRef"})

    for na, (abbrev, full) in abbrev_to_full.items():
        if _matches(na) and full not in seen_full:
            seen_full.add(full)
            results.append({"full": full, "abbreviation": abbrev, "source": "JabRef"})

    # Exact prefix matches first, then by length
    results.sort(key=lambda r: (not _normalize(r["full"]).startswith(nq), len(r["full"])))
    return results


# ---------------------------------------------------------------------------
# Upstream APIs
# ---------------------------------------------------------------------------

def lookup_abbreviso(name: str) -> dict | None:
    """Look up abbreviation via AbbrevISO (forward only)."""
    global _last_abbreviso_time
    elapsed = time.time() - _last_abbreviso_time
    if elapsed < _ABBREVISO_GAP:
        time.sleep(_ABBREVISO_GAP - elapsed)

    encoded = quote(name, safe="")
    url = f"https://abbreviso.toolforge.org/a/{encoded}"
    try:
        _last_abbreviso_time = time.time()
        result = _fetch(url).strip()
        if result and result != name:
            return {
                "query": name, "full": name, "abbreviation": result,
                "direction": "abbreviate", "source": "AbbrevISO", "standard": "ISO 4",
            }
    except (HTTPError, URLError, TimeoutError) as e:
        print(f"  AbbrevISO error: {e}", file=sys.stderr)
    return None


def lookup_nlm(query: str, direction: str = "abbreviate") -> dict | None:
    """Look up via NLM Catalog. direction: 'abbreviate' or 'expand'."""
    global _last_nlm_time
    elapsed = time.time() - _last_nlm_time
    if elapsed < _NLM_GAP:
        time.sleep(_NLM_GAP - elapsed)

    base = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

    if direction == "expand":
        term = f'"{query}"[ta]'
    else:
        term = f'"{query}"[All Fields]'

    search_url = f"{base}/esearch.fcgi?db=nlmcatalog&term={quote(term)}&retmax=3&retmode=json"
    try:
        _last_nlm_time = time.time()
        data = _fetch_json(search_url)
        ids = data.get("esearchresult", {}).get("idlist", [])
        if not ids:
            return None

        elapsed = time.time() - _last_nlm_time
        if elapsed < _NLM_GAP:
            time.sleep(_NLM_GAP - elapsed)
        _last_nlm_time = time.time()

        fetch_url = f"{base}/efetch.fcgi?db=nlmcatalog&id={ids[0]}&retmode=xml"
        xml_text = _fetch(fetch_url)
        root = ET.fromstring(xml_text)

        title_el = root.find(".//TitleMain/Title")
        abbrev_el = root.find(".//MedlineTA")

        if title_el is not None and abbrev_el is not None:
            full = title_el.text.strip().rstrip(".")
            abbrev = abbrev_el.text.strip()
            return {
                "query": query, "full": full, "abbreviation": abbrev,
                "direction": direction, "source": "NLM Catalog", "standard": "MEDLINE",
            }
    except (HTTPError, URLError, TimeoutError, ET.ParseError) as e:
        print(f"  NLM error: {e}", file=sys.stderr)
    return None


# ---------------------------------------------------------------------------
# Cascade
# ---------------------------------------------------------------------------

def abbreviate(name: str) -> dict | None:
    """Full name -> abbreviation. Cascade: local -> AbbrevISO -> NLM."""
    result = lookup_local(name)
    if result and result["direction"] == "abbreviate":
        return result

    result = lookup_abbreviso(name)
    if result:
        return result

    result = lookup_nlm(name, direction="abbreviate")
    if result:
        return result

    return None


def expand(abbrev_: str) -> dict | None:
    """Abbreviation -> full name. Cascade: local -> NLM."""
    result = lookup_local(abbrev_)
    if result:
        return result

    result = lookup_nlm(abbrev_, direction="expand")
    if result:
        return result

    return None


def auto_lookup(query: str) -> dict | None:
    """Auto-detect direction and look up."""
    words = query.split()
    has_periods = "." in query
    avg_word_len = sum(len(w.rstrip(".")) for w in words) / max(len(words), 1)

    if has_periods or (len(words) > 1 and avg_word_len < 4):
        # Likely abbreviation -> try expand first
        result = expand(query)
        if result:
            return result
        return abbreviate(query)
    else:
        # Likely full name -> try abbreviate first
        result = abbreviate(query)
        if result:
            return result
        return expand(query)


# ---------------------------------------------------------------------------
# BibTeX processing
# ---------------------------------------------------------------------------

def process_bib(
    filepath: str,
    direction: str = "abbreviate",
    output: str | None = None,
    dry_run: bool = False,
) -> dict:
    """Process a .bib file, returning a structured result (may not write)."""
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"file not found: {filepath}")

    text = path.read_text(encoding="utf-8", errors="replace")
    pattern = re.compile(r"(journal\s*=\s*\{)([^}]+)(\})", re.IGNORECASE)
    changes: list[dict] = []

    def replacer(m):
        prefix, name, suffix = m.group(1), m.group(2).strip(), m.group(3)
        if direction == "abbreviate":
            result = abbreviate(name)
        else:
            result = expand(name)

        if result:
            new_name = result["abbreviation"] if direction == "abbreviate" else result["full"]
            if new_name != name:
                changes.append({"old": name, "new": new_name, "source": result["source"]})
                return f"{prefix}{new_name}{suffix}"
        return m.group(0)

    new_text = pattern.sub(replacer, text)

    if output:
        out_path = Path(output)
    else:
        stem_suffix = "_abbrev" if direction == "abbreviate" else "_full"
        out_path = path.with_stem(path.stem + stem_suffix)

    written = False
    if not dry_run:
        out_path.write_text(new_text, encoding="utf-8")
        written = True

    return {
        "input": str(path),
        "output": str(out_path),
        "written": written,
        "dry_run": dry_run,
        "direction": direction,
        "changes_count": len(changes),
        "changes": changes,
    }


def batch_lookup(filepath: str) -> dict:
    """Process a text file with one journal name per line. Returns partial-success shape."""
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"file not found: {filepath}")

    lines = path.read_text(encoding="utf-8").strip().splitlines()
    succeeded: list[dict] = []
    failed: list[dict] = []
    for line in lines:
        name = line.strip()
        if not name or name.startswith("#"):
            continue
        result = auto_lookup(name)
        if result:
            succeeded.append(result)
        else:
            failed.append({
                "query": name,
                "error": {
                    "code": "not_found",
                    "message": f"No match for '{name}'",
                    "retryable": False,
                },
            })
    return {"succeeded": succeeded, "failed": failed}


def batch_stream(filepath: str):
    """Yield one NDJSON event per line, plus a final summary event."""
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"file not found: {filepath}")

    lines = path.read_text(encoding="utf-8").strip().splitlines()
    total = 0
    ok_n = 0
    fail_n = 0
    for line in lines:
        name = line.strip()
        if not name or name.startswith("#"):
            continue
        total += 1
        result = auto_lookup(name)
        if result:
            ok_n += 1
            yield {"ok": True, "data": result}
        else:
            fail_n += 1
            yield {
                "ok": False,
                "query": name,
                "error": {
                    "code": "not_found",
                    "message": f"No match for '{name}'",
                    "retryable": False,
                },
            }
    yield {
        "ok": True,
        "summary": {"total": total, "succeeded": ok_n, "failed": fail_n},
    }


# ---------------------------------------------------------------------------
# Schema — single source of truth for commands, params, and introspection
# ---------------------------------------------------------------------------

SCHEMA: dict[str, Any] = {
    "schema_version": SCHEMA_VERSION,
    "cli_version": CLI_VERSION,
    "global_flags": [
        {
            "name": "--format",
            "type": "string",
            "choices": ["json", "table", "human", "auto"],
            "default": "auto",
            "description": "Output format. 'auto' picks json when stdout is not a TTY, else human/table.",
        },
        {
            "name": "--json",
            "type": "bool",
            "description": "Alias for --format json (back-compat).",
        },
    ],
    "exit_codes": {
        "0": "success (including partial success)",
        "1": "runtime / upstream error",
        "2": "validation / bad input",
        "3": "not found",
    },
    "envelope": {
        "success": '{"ok": true, "data": ..., "meta": {...}}',
        "partial": '{"ok": "partial", "data": {"succeeded": [...], "failed": [...]}, "meta": {...}}',
        "error": '{"ok": false, "error": {"code": "...", "message": "...", "retryable": bool}, "meta": {...}}',
    },
    "commands": {
        "lookup": {
            "summary": "Auto-detect direction and look up a journal",
            "since": "1.0.0",
            "params": [
                {"name": "query", "positional": True, "nargs": "+", "type": "string",
                 "required": True, "description": "Journal name or abbreviation (may contain spaces)"},
            ],
        },
        "abbrev": {
            "summary": "Abbreviate a full journal name",
            "since": "1.0.0",
            "params": [
                {"name": "query", "positional": True, "nargs": "+", "type": "string",
                 "required": True, "description": "Full journal name"},
            ],
        },
        "expand": {
            "summary": "Expand a journal abbreviation",
            "since": "1.0.0",
            "params": [
                {"name": "query", "positional": True, "nargs": "+", "type": "string",
                 "required": True, "description": "Journal abbreviation"},
            ],
        },
        "search": {
            "summary": "Fuzzy-search the local cache",
            "since": "1.0.0",
            "params": [
                {"name": "query", "positional": True, "nargs": "+", "type": "string",
                 "required": True, "description": "Search terms (all terms must appear)"},
                {"name": "--limit", "type": "integer", "default": 15,
                 "description": "Maximum results to return (default 15)"},
                {"name": "--offset", "type": "integer", "default": 0,
                 "description": "Skip this many results (for pagination)"},
            ],
        },
        "bib": {
            "summary": "Rewrite journal names in a BibTeX file",
            "since": "1.0.0",
            "params": [
                {"name": "path", "positional": True, "type": "string", "required": True,
                 "description": "Path to .bib file"},
                {"name": "--expand", "type": "bool", "default": False,
                 "description": "Expand abbreviations (default: abbreviate)"},
                {"name": "--output", "type": "string", "default": None,
                 "description": "Explicit output path (default: <stem>_abbrev.bib / <stem>_full.bib)"},
                {"name": "--dry-run", "type": "bool", "default": False,
                 "description": "Preview changes without writing the output file"},
            ],
        },
        "batch": {
            "summary": "Look up a text file of journal names (one per line)",
            "since": "1.0.0",
            "params": [
                {"name": "path", "positional": True, "type": "string", "required": True,
                 "description": "Path to text file, one journal name per line"},
                {"name": "--stream", "type": "bool", "default": False,
                 "description": "Emit NDJSON — one result per line, final summary line"},
            ],
        },
        "cache": {
            "summary": "Inspect or refresh the local cache",
            "since": "1.0.0",
            "params": [
                {"name": "action", "positional": True, "type": "string", "required": True,
                 "choices": ["status", "update", "rebuild"],
                 "description": "status: inspect cache; update: download missing files; rebuild: delete + redownload"},
            ],
        },
        "schema": {
            "summary": "Print the command schema (JSON)",
            "since": "1.0.0",
            "params": [
                {"name": "target", "positional": True, "type": "string",
                 "required": False, "default": None,
                 "description": "Optional command name; omit to list all commands"},
            ],
        },
    },
}


# ---------------------------------------------------------------------------
# Envelope helpers
# ---------------------------------------------------------------------------

def _meta(**extra) -> dict:
    m: dict = {
        "schema_version": SCHEMA_VERSION,
        "cli_version": CLI_VERSION,
    }
    if (
        _cache_stats["files_loaded"]
        or _cache_stats["files_failed"]
        or _cache_stats["fetched_this_run"]
        or _cache_stats["files_missing"]
    ):
        m["cache"] = {
            "files_loaded": _cache_stats["files_loaded"],
            "files_missing": _cache_stats["files_missing"],
            "files_failed": _cache_stats["files_failed"],
            "fetched_this_run": _cache_stats["fetched_this_run"],
        }
    m.update(extra)
    return m


def envelope_ok(data: Any, **extra) -> dict:
    """Build a success envelope. Extra kwargs (meta, page, ...) merge at top level."""
    env: dict = {"ok": True, "data": data}
    env.update(extra)
    env["meta"] = _meta(**env.get("meta", {}))
    return env


def envelope_error(code: str, message: str, retryable: bool = False, **fields) -> dict:
    err = {"code": code, "message": message, "retryable": retryable}
    err.update(fields)
    return {"ok": False, "error": err, "meta": _meta()}


def envelope_partial(succeeded: list, failed: list, **extra) -> dict:
    env: dict = {
        "ok": "partial" if failed else True,
        "data": {"succeeded": succeeded, "failed": failed},
    }
    env.update(extra)
    env["meta"] = _meta(**env.get("meta", {}))
    return env


def exit_code_for(env: dict) -> int:
    if env["ok"] in (True, "partial"):
        return EXIT_OK
    err = env.get("error") or {}
    code = err.get("code", "")
    if code == "not_found":
        return EXIT_NOT_FOUND
    if code in ("validation_error", "file_not_found", "invalid_argument", "file_exists"):
        return EXIT_VALIDATION
    return EXIT_RUNTIME


# ---------------------------------------------------------------------------
# Output formatting
# ---------------------------------------------------------------------------

def _json_dump(obj: Any) -> str:
    return json.dumps(obj, indent=2, ensure_ascii=False)


def _format_human_result(data: dict) -> str:
    lines = [
        f"  Full name:    {data.get('full', 'N/A')}",
        f"  Abbreviation: {data.get('abbreviation', 'N/A')}",
        f"  Source:       {data.get('source', 'N/A')}",
    ]
    if "standard" in data:
        lines.append(f"  Standard:     {data['standard']}")
    return "\n".join(lines)


def _format_table(rows: list[dict]) -> str:
    if not rows:
        return "No results."
    headers = ["Full Name", "Abbreviation", "Source"]
    body = [(r.get("full", ""), r.get("abbreviation", ""), r.get("source", "")) for r in rows]
    widths = [max(len(h), max((len(r[i]) for r in body), default=0)) for i, h in enumerate(headers)]
    sep = "+" + "+".join("-" * (w + 2) for w in widths) + "+"
    hdr = "|" + "|".join(f" {h:<{widths[i]}} " for i, h in enumerate(headers)) + "|"
    lines = [sep, hdr, sep]
    for row in body:
        lines.append("|" + "|".join(f" {row[i]:<{widths[i]}} " for i in range(3)) + "|")
    lines.append(sep)
    return "\n".join(lines)


def resolve_format(args: argparse.Namespace) -> str:
    """Determine output format.

    Rules:
      - explicit --json wins (back-compat)
      - explicit --format <x> wins next
      - otherwise: json when stdout is not a TTY, else 'human' (which _emit_
        will route to table/indent depending on command)
    """
    if getattr(args, "json", False):
        return "json"
    fmt = getattr(args, "format", "auto")
    if fmt and fmt != "auto":
        return fmt
    if not sys.stdout.isatty():
        return "json"
    return "human"


def emit(env: dict, fmt: str, command: str) -> None:
    """Emit the envelope. JSON mode: one envelope on stdout. Human mode: formatted data on
    stdout for success, prose on stderr for errors."""
    if fmt == "json":
        print(_json_dump(env))
        return

    # -------- Human / table mode --------
    if env["ok"] is False:
        err = env["error"]
        print(f"Error [{err['code']}]: {err['message']}", file=sys.stderr)
        return

    if env["ok"] == "partial":
        succeeded = env["data"]["succeeded"]
        failed = env["data"]["failed"]
        if succeeded:
            print(_format_table(succeeded))
        print(f"\n{len(failed)} failed:", file=sys.stderr)
        for f in failed:
            print(f"  - {f['query']}: {f['error']['message']}", file=sys.stderr)
        return

    data = env["data"]

    if command in ("lookup", "abbrev", "expand"):
        print(_format_human_result(data))
        return

    if command == "search":
        print(_format_table(data))
        page = env.get("page") or {}
        if page.get("has_more"):
            print(
                f"\n[showing {page['returned']} of {page['total']}] — pass "
                f"--offset {page['next_offset']} for more",
                file=sys.stderr,
            )
        return

    if command == "bib":
        if data.get("dry_run"):
            print(f"[dry-run] Would write: {data['output']}")
        else:
            print(f"Input:   {data['input']}")
            print(f"Output:  {data['output']}")
        print(f"Changes: {data['changes_count']}")
        for c in data.get("changes", []):
            print(f"  {c['old']}  ->  {c['new']}  ({c['source']})")
        return

    if command == "batch":
        print(_format_table(data.get("succeeded", [])))
        return

    if command == "cache":
        if isinstance(data, dict):
            for k, v in data.items():
                if isinstance(v, (list, dict)):
                    print(f"  {k}: {json.dumps(v, ensure_ascii=False)}")
                else:
                    print(f"  {k}: {v}")
        else:
            print(str(data))
        return

    if command == "schema":
        print(_json_dump(data))
        return

    # Fallback
    print(_json_dump(data))


# ---------------------------------------------------------------------------
# Command handlers
# ---------------------------------------------------------------------------

def handle_lookup(args) -> dict:
    query = " ".join(args.query)
    t0 = time.time()
    result = auto_lookup(query)
    latency = int((time.time() - t0) * 1000)
    if result is None:
        return envelope_error(
            "not_found",
            f"No journal found for '{query}'",
            retryable=False,
            query=query,
        )
    return envelope_ok(result, meta={"latency_ms": latency})


def handle_abbrev(args) -> dict:
    query = " ".join(args.query)
    t0 = time.time()
    result = abbreviate(query)
    latency = int((time.time() - t0) * 1000)
    if result is None:
        return envelope_error(
            "not_found",
            f"No abbreviation found for '{query}'",
            retryable=False,
            query=query,
        )
    return envelope_ok(result, meta={"latency_ms": latency})


def handle_expand(args) -> dict:
    query = " ".join(args.query)
    t0 = time.time()
    result = expand(query)
    latency = int((time.time() - t0) * 1000)
    if result is None:
        return envelope_error(
            "not_found",
            f"No expansion found for '{query}'",
            retryable=False,
            query=query,
        )
    return envelope_ok(result, meta={"latency_ms": latency})


def handle_search(args) -> dict:
    query = " ".join(args.query)
    if args.limit < 0 or args.offset < 0:
        return envelope_error(
            "validation_error",
            "--limit and --offset must be non-negative",
            retryable=False,
        )
    t0 = time.time()
    all_results = fuzzy_search(query)
    latency = int((time.time() - t0) * 1000)
    total = len(all_results)
    start = args.offset
    end = start + args.limit
    page_items = all_results[start:end]
    return envelope_ok(
        page_items,
        meta={"latency_ms": latency},
        page={
            "offset": start,
            "limit": args.limit,
            "returned": len(page_items),
            "total": total,
            "has_more": end < total,
            "next_offset": end if end < total else None,
        },
    )


def handle_bib(args) -> dict:
    direction = "expand" if args.expand else "abbreviate"
    try:
        result = process_bib(
            args.path,
            direction=direction,
            output=args.output,
            dry_run=args.dry_run,
        )
    except FileNotFoundError as e:
        return envelope_error("file_not_found", str(e), retryable=False, path=args.path)
    except Exception as e:
        return envelope_error("runtime_error", f"process_bib failed: {e}", retryable=False)
    return envelope_ok(result)


def handle_batch(args) -> dict:
    # `--stream` is handled separately in main() before this dispatch
    try:
        result = batch_lookup(args.path)
    except FileNotFoundError as e:
        return envelope_error("file_not_found", str(e), retryable=False, path=args.path)
    return envelope_partial(result["succeeded"], result["failed"])


def handle_cache(args) -> dict:
    global _cache
    action = args.action

    if action == "status":
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        present = [f for f in JABREF_FILES if (CACHE_DIR / f).exists()]
        missing = [f for f in JABREF_FILES if not (CACHE_DIR / f).exists()]
        last_updated = None
        total_journals = None
        if present:
            mtimes = [(CACHE_DIR / f).stat().st_mtime for f in present]
            last_updated = (
                datetime.fromtimestamp(max(mtimes), tz=timezone.utc)
                .isoformat()
                .replace("+00:00", "Z")
            )
            try:
                fta, _ = load_cache()  # parse only, no network
                total_journals = len(fta)
            except Exception:
                total_journals = None
        return envelope_ok({
            "cache_dir": str(CACHE_DIR),
            "files_total": len(JABREF_FILES),
            "files_present": len(present),
            "files_missing": missing,
            "total_journals": total_journals,
            "last_updated": last_updated,
        })

    if action == "update":
        _cache = None
        ensure_cache()
        fta, ata = load_cache()
        _cache = (fta, ata)
        return envelope_ok({
            "action": "update",
            "fetched_this_run": _cache_stats["fetched_this_run"],
            "files_failed": _cache_stats["files_failed"],
            "files_missing": _cache_stats["files_missing"],
            "total_journals": len(fta),
        })

    if action == "rebuild":
        if CACHE_DIR.exists():
            for f in CACHE_DIR.iterdir():
                if f.suffix == ".csv":
                    f.unlink()
        _cache = None
        ensure_cache()
        fta, ata = load_cache()
        _cache = (fta, ata)
        return envelope_ok({
            "action": "rebuild",
            "fetched_this_run": _cache_stats["fetched_this_run"],
            "files_failed": _cache_stats["files_failed"],
            "files_missing": _cache_stats["files_missing"],
            "total_journals": len(fta),
        })

    return envelope_error(
        "validation_error",
        f"unknown cache action: {action}",
        retryable=False,
    )


def handle_schema(args) -> dict:
    target = args.target
    if target is None:
        return envelope_ok(SCHEMA)
    cmd = SCHEMA["commands"].get(target)
    if cmd is None:
        return envelope_error(
            "not_found",
            f"No such command: {target}",
            retryable=False,
            known_commands=sorted(SCHEMA["commands"].keys()),
        )
    return envelope_ok({"command": target, **cmd})


HANDLERS = {
    "lookup": handle_lookup,
    "abbrev": handle_abbrev,
    "expand": handle_expand,
    "search": handle_search,
    "bib": handle_bib,
    "batch": handle_batch,
    "cache": handle_cache,
    "schema": handle_schema,
}


# ---------------------------------------------------------------------------
# Argparse wiring (driven from SCHEMA)
# ---------------------------------------------------------------------------

def _add_param(sp: argparse.ArgumentParser, param: dict) -> None:
    name = param["name"]
    desc = param.get("description", "")

    if param.get("positional"):
        kwargs: dict = {"help": desc}
        if "nargs" in param:
            kwargs["nargs"] = param["nargs"]
        elif not param.get("required", True):
            kwargs["nargs"] = "?"
            kwargs["default"] = param.get("default")
        if "choices" in param:
            kwargs["choices"] = param["choices"]
        sp.add_argument(name, **kwargs)
        return

    kwargs = {"help": desc}
    ptype = param.get("type", "string")
    if ptype == "bool":
        kwargs["action"] = "store_true"
    elif ptype == "integer":
        kwargs["type"] = int
        kwargs["default"] = param.get("default")
    else:
        kwargs["default"] = param.get("default")
    if "choices" in param:
        kwargs["choices"] = param["choices"]
    sp.add_argument(name, **kwargs)


def _make_common_parser() -> argparse.ArgumentParser:
    """Parent parser for options that may appear on either side of the subcommand."""
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument(
        "--format",
        choices=["json", "table", "human", "auto"],
        default=argparse.SUPPRESS,
        help="Output format (default: auto — json when stdout is not a TTY, else human/table)",
    )
    common.add_argument(
        "--json",
        action="store_true",
        default=argparse.SUPPRESS,
        help="Alias for --format json (back-compat)",
    )
    return common


def build_parser() -> argparse.ArgumentParser:
    common = _make_common_parser()

    p = argparse.ArgumentParser(
        prog="jabbrv",
        parents=[common],
        description=(
            "Journal abbreviation lookup with a JabRef -> AbbrevISO -> NLM cascade.\n"
            "Serves humans (table/indent output) and AI agents (stable JSON envelope on stdout)."
        ),
        epilog=(
            "Output: stdout is JSON when not a TTY, table/indent when interactive.\n"
            "Exit codes: 0 success (incl. partial), 1 runtime, 2 validation, 3 not found.\n"
            f"CLI {CLI_VERSION}. Run 'jabbrv schema' for the full machine-readable contract.\n"
            "--format/--json may appear before or after the subcommand."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("--version", action="version", version=f"jabbrv {CLI_VERSION}")

    sub = p.add_subparsers(dest="command", metavar="<command>")

    for cmd_name, cmd_spec in SCHEMA["commands"].items():
        sp = sub.add_parser(
            cmd_name,
            parents=[common],
            help=cmd_spec["summary"],
            description=cmd_spec["summary"],
        )
        for param in cmd_spec["params"]:
            _add_param(sp, param)

    # Deprecated alias: update-cache -> cache rebuild
    sub.add_parser("update-cache", parents=[common], help="[deprecated] use 'cache rebuild'")

    return p


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    # Backfill defaults for common options (they use SUPPRESS so either
    # `jabbrv --format human lookup X` or `jabbrv lookup X --format human` works)
    if not hasattr(args, "format"):
        args.format = "auto"
    if not hasattr(args, "json"):
        args.json = False

    if not args.command:
        parser.print_help(sys.stderr)
        return EXIT_VALIDATION

    # Back-compat: `update-cache` -> `cache rebuild`
    if args.command == "update-cache":
        print(
            "warning: 'update-cache' is deprecated; use 'cache rebuild' instead.",
            file=sys.stderr,
        )
        args.command = "cache"
        args.action = "rebuild"

    fmt = resolve_format(args)

    # Streaming path for `batch --stream` — bypass envelope aggregation
    if args.command == "batch" and getattr(args, "stream", False):
        try:
            for event in batch_stream(args.path):
                sys.stdout.write(json.dumps(event, ensure_ascii=False) + "\n")
                sys.stdout.flush()
        except FileNotFoundError as e:
            env = envelope_error("file_not_found", str(e), retryable=False, path=args.path)
            emit(env, fmt, "batch")
            return EXIT_VALIDATION
        return EXIT_OK

    handler = HANDLERS.get(args.command)
    if handler is None:
        env = envelope_error(
            "validation_error",
            f"unknown command: {args.command}",
            retryable=False,
        )
        emit(env, fmt, args.command)
        return EXIT_VALIDATION

    try:
        env = handler(args)
    except Exception as e:  # last-resort structured error
        env = envelope_error(
            "runtime_error",
            f"unexpected error: {e}",
            retryable=True,
        )

    emit(env, fmt, args.command)
    return exit_code_for(env)


if __name__ == "__main__":
    sys.exit(main())
