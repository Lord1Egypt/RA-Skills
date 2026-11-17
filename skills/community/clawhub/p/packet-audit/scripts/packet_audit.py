#!/usr/bin/env python3
"""packet-audit: deterministic submission-packet checker.

Reads a folder of documents, classifies each one against a packet profile,
extracts the fields that must agree across the packet, and reports every
mismatch, missing document, and expired credential with file citations.

Offline by design: no network, no model calls, no subprocess, no third-party
imports. PDFs are read by the bundled stdlib extractor (scripts/pdftext.py);
`pypdf` is used only as a fallback when it already happens to be installed.
A PDF whose text cannot be read is reported with the reason, never guessed at.

Exit codes: 0 clean, 1 warnings, 2 blocking findings, 3 usage/input error.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import html
import json
import os
import re
import sys
import unicodedata
import zipfile
from pathlib import Path

try:  # sibling module when run as a script, package import when imported
    from . import pdftext  # type: ignore
except ImportError:  # pragma: no cover - the script path
    import pdftext  # type: ignore

SCHEMA = "packet-audit/report/1"
TOOL_VERSION = "1.1.1"
SEVERITY_ORDER = {"error": 0, "warning": 1, "info": 2}
TEXT_EXTS = {".txt", ".md", ".csv", ".json", ".log", ".tsv"}
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp", ".gif", ".heic", ".webp"}
SKIP_DIRS = {".git", "__pycache__", ".packet-audit", "node_modules", ".venv", "venv"}


class ProfileError(Exception):
    """A packet profile is structurally invalid."""


class InputError(Exception):
    """The folder or arguments cannot be audited."""


# --------------------------------------------------------------------------
# small utilities
# --------------------------------------------------------------------------

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def clean_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = unicodedata.normalize("NFC", text)
    return "".join(ch for ch in text if ch == "\n" or ch == "\t" or ord(ch) >= 32)


def decode_bytes(data: bytes) -> str:
    for enc in ("utf-8-sig", "utf-16", "cp1252"):
        try:
            return data.decode(enc)
        except (UnicodeDecodeError, UnicodeError):
            continue
    return data.decode("utf-8", errors="replace")


def parse_iso(value: str) -> _dt.date | None:
    try:
        return _dt.date.fromisoformat(value)
    except ValueError:
        return None


def today_iso() -> str:
    return _dt.date.today().isoformat()


# --------------------------------------------------------------------------
# extraction
# --------------------------------------------------------------------------

def docx_pages(path: Path) -> list[str]:
    """Extract paragraph text from a .docx using only the standard library."""
    with zipfile.ZipFile(path) as zf:
        names = [n for n in zf.namelist() if n == "word/document.xml"]
        if not names:
            raise ValueError("docx has no word/document.xml")
        raw = zf.read("word/document.xml").decode("utf-8", errors="replace")
    raw = re.sub(r"<w:(tab|br)\s*/>", "\t", raw)
    raw = re.sub(r"</w:p>", "\n", raw)
    raw = re.sub(r"<[^>]+>", "", raw)
    return [clean_text(html.unescape(raw))]


def pdf_pages(path: Path) -> list[str]:
    """Extract per-page text: bundled stdlib reader first, pypdf only as a fallback.

    Doing this without a third-party import matters for an audit: a PDF that reads or does
    not read depending on what happens to be installed is an audit that checks different
    things on different machines.
    """
    reasons: list[str] = []
    try:
        return [clean_text(page) for page in pdftext.extract_pages(path)]
    except Exception as exc:  # noqa: BLE001 - fall through to pypdf, keep the reason
        reasons.append(str(exc))
    try:
        from pypdf import PdfReader  # type: ignore
    except Exception:  # noqa: BLE001 - any import failure means "not available"
        raise RuntimeError(reasons[0] + "; pypdf not installed either") from None
    try:
        reader = PdfReader(str(path))
        pages = []
        for page in reader.pages:
            try:
                pages.append(clean_text(page.extract_text() or ""))
            except Exception:  # noqa: BLE001 - one bad page must not abort the audit
                pages.append("")
        if not any(p.strip() for p in pages):
            raise RuntimeError("pdf has no extractable text layer (scan or image-only)")
        return pages
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(f"{reasons[0]}; pypdf: {exc}") from None


def extract(path: Path, ext: str) -> tuple[list[str] | None, str]:
    """Return (pages, method). pages is None when the file could not be read."""
    sidecar = path.with_name(path.name + ".txt")
    if sidecar.is_file() and ext not in TEXT_EXTS:
        try:
            return [clean_text(sidecar.read_text(encoding="utf-8", errors="replace"))], "sidecar"
        except OSError:
            pass
    try:
        if ext in TEXT_EXTS:
            return [clean_text(decode_bytes(path.read_bytes()))], "text"
        if ext == ".docx":
            return docx_pages(path), "docx"
        if ext == ".pdf":
            return pdf_pages(path), "pdf"
    except (RuntimeError, ValueError, OSError, zipfile.BadZipFile) as exc:
        return None, str(exc)
    if ext in IMAGE_EXTS:
        return None, "image: needs OCR, which this skill does not perform"
    return None, "unsupported file type"


# --------------------------------------------------------------------------
# profile handling
# --------------------------------------------------------------------------

PROFILE_KEYS = {"id", "title", "review_note", "classify", "fields", "document_fields",
                "required", "validity", "consistency"}
NORMALIZERS = {"name", "address", "date", "money", "text"}


def load_profile(path: Path) -> dict:
    if not path.is_file():
        raise InputError(f"profile not found: {path}")
    try:
        profile = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ProfileError(f"{path.name}: invalid JSON ({exc})") from exc
    validate_profile(profile, path.name)
    profile["_path"] = str(path)
    profile["_digest"] = sha256_file(path)
    return profile


def validate_profile(profile: dict, label: str = "<profile>") -> None:
    if not isinstance(profile, dict):
        raise ProfileError(f"{label}: profile must be a JSON object")
    missing = PROFILE_KEYS - set(profile)
    if missing:
        raise ProfileError(f"{label}: missing keys: {', '.join(sorted(missing))}")
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{1,60}", str(profile["id"])):
        raise ProfileError(f"{label}: id must be lowercase words separated by hyphens")
    if not isinstance(profile["classify"], list) or not profile["classify"]:
        raise ProfileError(f"{label}: classify must be a non-empty list")
    for rule in profile["classify"]:
        if "type" not in rule:
            raise ProfileError(f"{label}: every classify rule needs a type")
    for name, spec in profile["fields"].items():
        if spec.get("normalizer") not in NORMALIZERS:
            raise ProfileError(f"{label}: field {name} has unknown normalizer")
        if not spec.get("patterns"):
            raise ProfileError(f"{label}: field {name} has no patterns")
        for pattern in spec["patterns"]:
            try:
                re.compile(pattern["regex"])
            except re.error as exc:
                raise ProfileError(f"{label}: field {name} bad regex ({exc})") from exc
    known_types = {r["type"] for r in profile["classify"]}
    for dtype, fields in profile["document_fields"].items():
        if dtype not in known_types:
            raise ProfileError(f"{label}: document_fields names unknown type {dtype}")
        for field in fields:
            if field not in profile["fields"]:
                raise ProfileError(f"{label}: document_fields references unknown field {field}")
    required_types = [item["type"] for item in profile["required"]]
    for dtype in required_types:
        if dtype not in known_types:
            raise ProfileError(f"{label}: required names unknown type {dtype}")
    for item in profile["consistency"]:
        if item["field"] not in profile["fields"]:
            raise ProfileError(f"{label}: consistency references unknown field {item['field']}")
        if item.get("severity", "error") not in SEVERITY_ORDER:
            raise ProfileError(f"{label}: consistency has unknown severity")
    for item in profile["validity"]:
        if item["doc_type"] not in required_types:
            raise ProfileError(f"{label}: validity names a doc_type that is not required")
        if item["field"] not in profile["fields"]:
            raise ProfileError(f"{label}: validity references unknown field {item['field']}")


# --------------------------------------------------------------------------
# classification
# --------------------------------------------------------------------------

def rule_matches(rule: dict, rel: str, ext: str, text: str | None) -> bool:
    exts = rule.get("ext")
    if exts and ext not in exts:
        return False
    name_patterns = rule.get("filename") or []
    content_patterns = rule.get("content") or []
    if not name_patterns and not content_patterns:
        return bool(exts)
    name_hit = any(re.search(p, rel, re.I) for p in name_patterns)
    content_hit = False
    if content_patterns and text:
        content_hit = any(re.search(p, text, re.I) for p in content_patterns)
    if name_patterns and content_patterns:
        return name_hit and content_hit
    return name_hit or content_hit


def classify(rel: str, ext: str, text: str | None, profile: dict) -> str:
    for rule in profile["classify"]:
        if rule_matches(rule, rel, ext, text):
            return rule["type"]
    return "unknown"


# --------------------------------------------------------------------------
# field extraction and normalisation
# --------------------------------------------------------------------------

def normalise_space(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip())


TITLE_WORDS = {"mr", "mrs", "ms", "miss", "dr", "prof", "sir", "madam"}


def normalise_name(value: str) -> str:
    text = unicodedata.normalize("NFKD", value)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = re.sub(r"[^A-Za-z ]+", " ", text).casefold()
    tokens = [t for t in text.split() if t and t not in TITLE_WORDS]
    return " ".join(sorted(tokens))


def name_tokens(value: str) -> set[str]:
    return {t for t in normalise_name(value).split() if t}


def normalise_address(value: str) -> str:
    text = unicodedata.normalize("NFKD", value)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = re.sub(r"[^A-Za-z0-9 ]+", " ", text).casefold()
    synonyms = {"street": "st", "avenue": "ave", "road": "rd", "apartment": "apt",
                "suite": "ste", "drive": "dr", "boulevard": "blvd", "lane": "ln"}
    tokens = [synonyms.get(t, t) for t in text.split() if t]
    return " ".join(tokens)


def address_number(value: str) -> str | None:
    for token in normalise_address(value).split():
        if re.fullmatch(r"\d+[a-z]?", token):
            return token
    return None


def address_postcode(value: str) -> str | None:
    match = re.search(r"\b(\d{5}(?:-\d{4})?)\b", value)
    if match:
        return match.group(1)
    match = re.search(r"\b([A-Z]{1,2}\d[A-Z\d]?\s*\d[A-Z]{2})\b", value.upper())
    return match.group(1) if match else None


def normalise_money(value: str) -> float | None:
    text = re.sub(r"[^0-9,.\-]", "", value)
    if not text:
        return None
    if text.count(",") and text.count("."):
        text = text.replace(",", "")
    elif text.count(",") and not text.count("."):
        parts = text.split(",")
        text = text.replace(",", ".") if len(parts[-1]) == 2 else text.replace(",", "")
    try:
        return round(float(text), 2)
    except ValueError:
        return None


def normalise_date(value: str, order: str) -> str | None:
    text = value.strip().replace(".", "/").replace("-", "/")
    parts = [p for p in text.split("/") if p]
    if len(parts) < 3:
        return None
    try:
        nums = [int(p) for p in parts[:3]]
    except ValueError:
        return None
    first, second, third = nums
    if len(parts[0]) == 4 or first > 31:
        year, month, day = first, second, third
    else:
        year = third if third > 99 else 2000 + third
        if order == "dmy":
            day, month = first, second
        else:
            month, day = first, second
        if month > 12 and day <= 12:
            day, month = month, day
    try:
        return _dt.date(year, month, day).isoformat()
    except ValueError:
        return None


def line_of(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def extract_fields(pages: list[str], field_specs: list[str], profile: dict,
                   is_pdf: bool) -> list[dict]:
    found: list[dict] = []
    for field in field_specs:
        spec = profile["fields"][field]
        hit = None
        for page_index, page in enumerate(pages):
            for pattern in spec["patterns"]:
                match = re.search(pattern["regex"], page, re.I | re.M)
                if not match:
                    continue
                group = pattern.get("group", 1)
                try:
                    raw = match.group(group)
                except (IndexError, TypeError):
                    raw = match.group(0)
                if raw is None or not raw.strip():
                    continue
                hit = {
                    "field": field,
                    "value": normalise_space(raw),
                    "locator": f"p{page_index + 1}" if is_pdf else f"line {line_of(page, match.start())}",
                }
                break
            if hit:
                break
        if hit:
            found.append(hit)
    return found


def normalise_value(field: str, value: str, profile: dict) -> object:
    spec = profile["fields"].get(field, {})
    kind = spec.get("normalizer", "text")
    order = profile.get("date_order", "mdy")
    if kind == "name":
        return normalise_name(value)
    if kind == "address":
        return normalise_address(value)
    if kind == "date":
        return normalise_date(value, order)
    if kind == "money":
        return normalise_money(value)
    return normalise_space(value).casefold()


# --------------------------------------------------------------------------
# comparison
# --------------------------------------------------------------------------

def compare_values(field: str, kind: str, left: dict, right: dict) -> tuple[str, str]:
    """Return (outcome, detail) where outcome is ok | variant | conflict."""
    a_raw, b_raw = left["value"], right["value"]
    a, b = left["normalised"], right["normalised"]
    if kind == "name":
        ta, tb = name_tokens(a_raw), name_tokens(b_raw)
        if ta == tb:
            return "ok", ""
        overlap = len(ta & tb) / max(1, len(ta | tb))
        if overlap >= 0.6:
            return "variant", f"same person, different spelling (token overlap {overlap:.0%})"
        return "conflict", f"different names (token overlap {overlap:.0%})"
    if kind == "address":
        num_a, num_b = address_number(a_raw), address_number(b_raw)
        if num_a and num_b and num_a != num_b:
            return "conflict", f"street number {num_a} vs {num_b}"
        pc_a, pc_b = address_postcode(a_raw), address_postcode(b_raw)
        if pc_a and pc_b and pc_a != pc_b:
            return "conflict", f"postal code {pc_a} vs {pc_b}"
        ta, tb = set(str(a).split()), set(str(b).split())
        overlap = len(ta & tb) / max(1, len(ta | tb))
        if ta == tb:
            return "ok", ""
        if overlap >= 0.6:
            return "variant", f"same address, different wording (token overlap {overlap:.0%})"
        return "conflict", f"addresses differ (token overlap {overlap:.0%})"
    if kind == "date":
        if a is None or b is None:
            return "conflict", "a date could not be parsed"
        return ("ok", "") if a == b else ("conflict", f"{a} vs {b}")
    if kind == "money":
        if a is None or b is None:
            return "conflict", "an amount could not be parsed"
        tolerance = float(profile_money_tolerance)
        return ("ok", "") if abs(a - b) <= tolerance else ("conflict", f"{a:,.2f} vs {b:,.2f}")
    if a == b:
        return "ok", ""
    return "variant", "text differs"


profile_money_tolerance = 0.0


# --------------------------------------------------------------------------
# the audit
# --------------------------------------------------------------------------

def finding(code: str, severity: str, title: str, detail: str, docs: list[str] | None = None,
             field: str | None = None, values: list[dict] | None = None) -> dict:
    return {"code": code, "severity": severity, "title": title, "detail": detail,
            "docs": docs or [], "field": field, "values": values or []}


def collect_files(folder: Path) -> list[Path]:
    files = []
    for root, dirs, names in os.walk(folder):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS and not d.startswith("."))
        for name in sorted(names):
            if name.startswith("."):
                continue
            files.append(Path(root) / name)
    return sorted(files, key=lambda p: str(p.relative_to(folder)).lower())


def audit(folder: Path, profile: dict, decision_date: _dt.date, generated_at: str) -> dict:
    global profile_money_tolerance
    profile_money_tolerance = float(profile.get("money_tolerance", 0.0))

    files = collect_files(folder)
    if not files:
        raise InputError(f"no files found under {folder}")

    inventory: list[dict] = []
    texts: dict[str, list[str]] = {}
    for path in files:
        rel = path.relative_to(folder).as_posix()
        ext = path.suffix.lower()
        digest = sha256_file(path)
        pages, method = extract(path, ext)
        entry = {
            "path": rel, "bytes": path.stat().st_size, "sha256": digest, "ext": ext,
            "readable": pages is not None, "extraction": method,
            "doc_type": "unknown", "fields": [],
        }
        if pages is not None:
            texts[rel] = pages
            entry["doc_type"] = classify(rel, ext, "\n".join(pages), profile)
        else:
            entry["doc_type"] = classify(rel, ext, None, profile)
        if entry["doc_type"] in profile["document_fields"]:
            entry["fields"] = [
                {"field": f["field"], "value": f["value"], "locator": f["locator"],
                 "normalised": normalise_value(f["field"], f["value"], profile)}
                for f in extract_fields(pages or [], profile["document_fields"][entry["doc_type"]],
                                        profile, ext == ".pdf")
            ]
        inventory.append(entry)

    findings: list[dict] = []
    by_type: dict[str, list[dict]] = {}
    for entry in inventory:
        by_type.setdefault(entry["doc_type"], []).append(entry)

    # 1. required documents
    for item in profile["required"]:
        candidates = [item["type"]] + list(item.get("alternates") or [])
        present = [t for t in candidates if by_type.get(t)]
        if not present:
            findings.append(finding(
                "PA-E01", "error", "Required document missing",
                f"No file in the packet matched {item['label']} "
                f"(expected type: {' / '.join(candidates)}).",
                docs=[]))
            continue

    # 2. unreadable / unclassified
    for entry in inventory:
        if not entry["readable"]:
            findings.append(finding(
                "PA-R01", "warning", "Document could not be read",
                f"{entry['path']}: {entry['extraction']}. The audit cannot cite or check this file.",
                docs=[entry["path"]]))
        elif entry["doc_type"] == "unknown":
            findings.append(finding(
                "PA-U01", "info", "File not classified",
                f"{entry['path']} did not match any document type in this profile; "
                "it is listed but not checked.",
                docs=[entry["path"]]))

    # 3. duplicate files
    seen: dict[str, str] = {}
    for entry in inventory:
        if entry["sha256"] in seen:
            findings.append(finding(
                "PA-D01", "info", "Duplicate file",
                f"{entry['path']} is byte-identical to {seen[entry['sha256']]}.",
                docs=[entry["path"], seen[entry["sha256"]]]))
        else:
            seen[entry["sha256"]] = entry["path"]

    # 4. required fields per document type
    for dtype, fields in profile["document_fields"].items():
        for entry in by_type.get(dtype, []):
            if not entry["readable"]:
                continue
            present = {f["field"] for f in entry["fields"]}
            for field in fields:
                if field not in present:
                    findings.append(finding(
                        "PA-F01", "warning", "Required field not found",
                        f"{entry['path']} ({dtype}) does not show {profile['fields'][field].get('label', field)}.",
                        docs=[entry["path"]], field=field))

    # 5. validity windows
    for rule in profile["validity"]:
        minimum = decision_date + _dt.timedelta(days=int(rule.get("min_days_after_decision", 0)))
        for entry in by_type.get(rule["doc_type"], []):
            values = [f for f in entry["fields"] if f["field"] == rule["field"]]
            if not values:
                continue
            iso = values[0]["normalised"]
            if not iso:
                findings.append(finding(
                    "PA-X02", "warning", "Expiry date could not be parsed",
                    f"{entry['path']}: '{values[0]['value']}' is not a date this audit understands.",
                    docs=[entry["path"]], field=rule["field"]))
                continue
            if _dt.date.fromisoformat(str(iso)) < minimum:
                findings.append(finding(
                    "PA-X01", rule.get("severity", "error"), "Document expires too soon",
                    f"{entry['path']} expires {iso}; the packet needs it valid until at least "
                    f"{minimum.isoformat()} ({rule.get('reason', 'validity window')}).",
                    docs=[entry["path"]], field=rule["field"],
                    values=[{"doc": entry["path"], "value": str(iso),
                             "locator": values[0]["locator"]}]))

    # 6. cross-document consistency
    for rule in profile["consistency"]:
        field = rule["field"]
        kind = profile["fields"][field].get("normalizer", "text")
        occurrences = []
        checked_digests: set[str] = set()
        for entry in inventory:
            if entry["sha256"] in checked_digests:
                continue
            for value in entry["fields"]:
                if value["field"] == field:
                    occurrences.append({"doc": entry["path"], "doc_type": entry["doc_type"],
                                        "value": value["value"], "normalised": value["normalised"],
                                        "locator": value["locator"]})
            checked_digests.add(entry["sha256"])
        if len(occurrences) < 2:
            continue
        primary_type = rule.get("primary")
        reference = occurrences[0]
        if primary_type:
            matches = [o for o in occurrences if o["doc_type"] == primary_type]
            if matches:
                reference = matches[0]
            elif primary_type in {e["doc_type"] for e in inventory}:
                findings.append(finding(
                    "PA-C03", "warning", "Authoritative document shows no value",
                    f"{profile['fields'][field].get('label', field)} has no value from the "
                    f"{primary_type} that is in the packet, so agreement is checked against the "
                    "first document that carries it.",
                    docs=[o["doc"] for o in occurrences[:4]], field=field))
        for occ in occurrences:
            if occ is reference:
                continue
            outcome, detail = compare_values(field, kind, reference, occ)
            if outcome == "ok":
                continue
            severity = "warning" if (outcome == "variant" or rule.get("severity") == "warning") else "error"
            findings.append(finding(
                "PA-C02" if outcome == "variant" else "PA-C01", severity,
                "Values disagree across documents" if outcome == "conflict" else "Values differ in wording",
                f"{profile['fields'][field].get('label', field)}: {detail}.",
                docs=[reference["doc"], occ["doc"]], field=field,
                values=[{"doc": reference["doc"], "value": reference["value"],
                         "locator": reference["locator"]},
                        {"doc": occ["doc"], "value": occ["value"], "locator": occ["locator"]}]))

    findings.sort(key=lambda f: (SEVERITY_ORDER[f["severity"]], f["code"], f["docs"][:1]))

    counts = {"error": 0, "warning": 0, "info": 0}
    for item in findings:
        counts[item["severity"]] += 1
    if counts["error"]:
        verdict = "NOT READY"
    elif counts["warning"]:
        verdict = "READY WITH WARNINGS"
    else:
        verdict = "READY"

    return {
        "schema": SCHEMA,
        "tool_version": TOOL_VERSION,
        "generated_at": generated_at,
        "decision_date": decision_date.isoformat(),
        "folder": str(folder),
        "profile": {"id": profile["id"], "title": profile["title"],
                    "path": profile.get("_path"), "sha256": profile.get("_digest"),
                    "review_note": profile.get("review_note", "")},
        "counts": counts,
        "verdict": verdict,
        "documents": inventory,
        "findings": findings,
    }


# --------------------------------------------------------------------------
# rendering
# --------------------------------------------------------------------------

def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def render_markdown(report: dict) -> str:
    p = report["profile"]
    lines = [
        "# Packet audit",
        "",
        f"- **Verdict:** {report['verdict']}",
        f"- **Blocking findings:** {report['counts']['error']}  |  "
        f"**Warnings:** {report['counts']['warning']}  |  **Notes:** {report['counts']['info']}",
        f"- **Profile:** {p['title']} (`{p['id']}`)",
        f"- **Decision date:** {report['decision_date']}",
        f"- **Folder:** `{report['folder']}`",
        f"- **Profile digest:** `{(p['sha256'] or '')[:16]}`",
        f"- **Generated:** {report['generated_at']} by packet-audit {report['tool_version']}",
        "",
        "This report checks that the documents agree with each other and cover the "
        "profile's requirements. It is not legal advice and does not decide eligibility.",
        "",
        "## Findings",
        "",
    ]
    if not report["findings"]:
        lines.append("No findings. Every required document was present, readable, and consistent.")
    else:
        lines += ["| # | Severity | Code | Finding | Where |", "|---|---|---|---|---|"]
        for index, item in enumerate(report["findings"], 1):
            where = ", ".join(f"`{d}`" for d in item["docs"]) or "-"
            lines.append(f"| {index} | {item['severity']} | {item['code']} | "
                         f"{md_escape(item['title'])}: {md_escape(item['detail'])} | {where} |")
    lines += ["", "## Documents", "",
              "| File | Type | Read | Fields found | SHA-256 |", "|---|---|---|---|---|"]
    for doc in report["documents"]:
        fields = ", ".join(f"{f['field']}={f['value']}" for f in doc["fields"]) or "-"
        lines.append(f"| `{doc['path']}` | {doc['doc_type']} | "
                     f"{'yes' if doc['readable'] else 'no'} | {md_escape(fields)} | "
                     f"`{doc['sha256'][:16]}` |")
    lines += ["", "## Next actions", ""]
    actions = []
    for item in report["findings"]:
        if item["severity"] == "info":
            continue
        actions.append(f"- **{item['code']}** {item['title']}: {item['detail']}")
    lines += actions or ["Nothing to fix before submitting."]
    lines += ["", "## Limits", "",
              "Text is extracted from .txt/.md/.csv, .docx and .pdf with the standard library; "
              "PDFs fall back to `pypdf` only when it is already installed, and a sibling "
              "`<name>.pdf.txt` text dump is used when present. Encrypted and image-only "
              "PDFs, scans and photos are reported with the reason, never guessed at. "
              "Always confirm the authority's own checklist before submitting.", ""]
    return "\n".join(lines)


def render_manifest(report: dict) -> dict:
    return {
        "schema": "packet-audit/manifest/1",
        "generated_at": report["generated_at"],
        "folder": report["folder"],
        "profile": report["profile"]["id"],
        "files": [{"path": d["path"], "bytes": d["bytes"], "sha256": d["sha256"],
                   "doc_type": d["doc_type"], "readable": d["readable"]}
                  for d in report["documents"]],
    }


# --------------------------------------------------------------------------
# cli
# --------------------------------------------------------------------------

def profile_dir() -> Path:
    return Path(__file__).resolve().parent.parent / "profiles"


def list_profiles() -> list[dict]:
    rows = []
    for path in sorted(profile_dir().glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            rows.append({"id": data.get("id", path.stem), "title": data.get("title", ""),
                         "file": path.name})
        except (OSError, json.JSONDecodeError):
            rows.append({"id": path.stem, "title": "<invalid profile>", "file": path.name})
    return rows


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="packet_audit.py",
        description="Check a submission packet for missing, expired, and inconsistent documents.")
    parser.add_argument("--folder", help="folder holding the documents to audit")
    parser.add_argument("--profile", help="profile id (e.g. rental-us) or path to a profile JSON")
    parser.add_argument("--decision-date", default=today_iso(),
                        help="date the authority decides or the packet is submitted (YYYY-MM-DD)")
    parser.add_argument("--out", help="output folder (default: <folder>/.packet-audit)")
    parser.add_argument("--now", help="override the report timestamp (ISO 8601, for reproducible runs)")
    parser.add_argument("--json", action="store_true", help="print the JSON report to stdout")
    parser.add_argument("--list-profiles", action="store_true", help="list bundled profiles and exit")
    args = parser.parse_args(argv)

    if args.list_profiles:
        for row in list_profiles():
            print(f"{row['id']:28} {row['title']}  ({row['file']})")
        return 0

    try:
        if not args.folder or not args.profile:
            raise InputError("--folder and --profile are required (or use --list-profiles)")
        folder = Path(args.folder).expanduser().resolve()
        if not folder.is_dir():
            raise InputError(f"not a folder: {folder}")
        decision = parse_iso(args.decision_date)
        if decision is None:
            raise InputError(f"--decision-date must be YYYY-MM-DD, got {args.decision_date!r}")
        candidate = Path(args.profile)
        if candidate.suffix.lower() == ".json" and candidate.is_file():
            profile = load_profile(candidate)
        else:
            profile = load_profile(profile_dir() / f"{args.profile}.json")

        generated = args.now or _dt.datetime.now().replace(microsecond=0).isoformat()
        report = audit(folder, profile, decision, generated)

        out_dir = Path(args.out).expanduser() if args.out else folder / ".packet-audit"
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "packet-report.md").write_text(render_markdown(report), encoding="utf-8")
        (out_dir / "packet-report.json").write_text(json.dumps(report, indent=2) + "\n",
                                                    encoding="utf-8")
        (out_dir / "packet-manifest.json").write_text(
            json.dumps(render_manifest(report), indent=2) + "\n", encoding="utf-8")
    except (InputError, ProfileError) as exc:
        print(f"packet-audit: {exc}", file=sys.stderr)
        return 3

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"verdict: {report['verdict']}")
        print(f"errors: {report['counts']['error']}  warnings: {report['counts']['warning']}  "
              f"notes: {report['counts']['info']}")
        for item in report["findings"]:
            print(f"  [{item['severity']:7}] {item['code']}  {item['title']}: {item['detail']}")
        print(f"report: {out_dir / 'packet-report.md'}")

    if report["counts"]["error"]:
        return 2
    if report["counts"]["warning"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
