#!/usr/bin/env python3
"""
memos_dreaming_audit.py — Weekly MEMORY.md Quality Audit

Scans MEMORY.md for:
1. Duplicate entries (similar title/summary from repeated promotions)
2. Outdated entries (old dates, superseded content)
3. Noise entries (technical one-offs that don't deserve long-term retention)
4. Structural issues (orphaned sections, broken formatting)

Outputs: AUDIT.md with findings + recommended actions
Run with --apply to auto-clean (creates backup first).
"""

import re
import shutil
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Optional

# ─── Config ──────────────────────────────────────────────────────────────────

MEMORY_FILE = Path.home() / ".openclaw/workspace/MEMORY.md"
BACKUP_DIR  = Path.home() / ".openclaw/workspace/.memos-dreaming/audits"
AUDIT_FILE  = Path.home() / ".openclaw/workspace/AUDIT.md"

MIN_TITLE_LEN = 6    # Chinese chars are information-dense; titles shorter than 6 CJK chars are likely noise
MAX_AGE_DAYS  = 90  # entries older than this need review
DEDUP_SIMILARITY = 0.75  # 0-1, title similarity threshold for dedup

# ─── Helpers ─────────────────────────────────────────────────────────────────

def get_now():
    return datetime.now()

def ensure_dir(p: Path):
    p.parent.mkdir(parents=True, exist_ok=True)

def ts_to_date(ts: int) -> str:
    return datetime.fromtimestamp(ts / 1000). strftime("%Y-%m-%d")

def simple_similarity(a: str, b: str) -> float:
    """Crude similarity: Jaccard of bigram sets."""
    a_words = set(a.lower().split())
    b_words = set(b.lower().split())
    if not a_words or not b_words:
        return 0.0
    intersection = len(a_words & b_words)
    union = len(a_words | b_words)
    return intersection / union if union else 0.0

# ─── Parsers ─────────────────────────────────────────────────────────────────

def parse_entries(content: str) -> list[dict]:
    """Extract individual bullet entries from MEMORY.md."""
    entries = []
    # Match lines starting with - or ## that look like entries
    lines = content.split("\n")
    current_section = "General"
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        # Section headers
        section_match = re.match(r"^##?\s+(.+)", line)
        if section_match:
            current_section = section_match.group(1).strip()
        # Bullet entries
        elif line.startswith("- **"):
            # Extract title between **...**
            title_match = re.search(r"^\- \*\*([^\*]+)\*\*", line)
            if title_match:
                title = title_match.group(1).strip()
                # Get continuation lines (indented or next bullet)
                body_lines = []
                j = i + 1
                while j < len(lines) and (lines[j].startswith("  ") or lines[j].strip().startswith("- ")):
                    if lines[j].strip().startswith("- **"):
                        break
                    body_lines.append(lines[j].strip())
                    j += 1
                body = " ".join(body_lines).strip()
                
                # Extract date from title (e.g., "(skill, 2026-04-18)")
                date_match = re.search(r"\((\d{4}-\d{2}-\d{2})\)", line)
                entry_date = date_match.group(1) if date_match else None
                
                # Calculate entry hash for dedup
                entry_hash = hashlib.sha256(title.encode()).hexdigest()[:12]
                
                entries.append({
                    "title": title,
                    "body": body,
                    "section": current_section,
                    "date": entry_date,
                    "line_start": i,
                    "hash": entry_hash,
                    "raw": line,
                })
        i += 1
    return entries

def parse_sections(content: str) -> dict[str, list[str]]:
    """Group lines by section headers."""
    sections = {}
    current = "Top"
    lines = []
    for line in content.split("\n"):
        m = re.match(r"^##?\s+(.+)", line)
        if m:
            if current:
                sections[current] = lines
            current = m.group(1).strip()
            lines = []
        else:
            lines.append(line)
    sections[current] = lines
    return sections

# ─── Auditors ────────────────────────────────────────────────────────────────

def audit_duplicates(entries: list[dict]) -> list[dict]:
    """Find entries with highly similar titles."""
    findings = []
    n = len(entries)
    checked = set()
    for i in range(n):
        for j in range(i + 1, n):
            a, b = entries[i], entries[j]
            key = tuple(sorted([a["hash"], b["hash"]]))
            if key in checked:
                continue
            checked.add(key)
            sim = simple_similarity(a["title"], b["title"])
            if sim >= DEDUP_SIMILARITY:
                findings.append({
                    "type": "duplicate",
                    "severity": "medium",
                    "entry_a": a,
                    "entry_b": b,
                    "similarity": sim,
                })
    return findings

def audit_outdated(entries: list[dict]) -> list[dict]:
    """Find entries older than MAX_AGE_DAYS without update."""
    findings = []
    now = get_now()
    for e in entries:
        if not e.get("date"):
            continue
        try:
            entry_date = datetime.strptime(e["date"], "%Y-%m-%d")
            age_days = (now - entry_date).days
            if age_days > MAX_AGE_DAYS:
                findings.append({
                    "type": "outdated",
                    "severity": "low",
                    "entry": e,
                    "age_days": age_days,
                })
        except ValueError:
            pass
    return findings

def audit_noise(entries: list[dict]) -> list[dict]:
    """Find entries that look like noise (too short, one-off technical notes)."""
    findings = []
    noise_patterns = [
        r"^[\d\.]+$",  # just a version number
        r"^today's.*",  # one-off daily notes
        r"^temp.*", r"^tmp.*",  # temporary
        r"^test.*", r"^debug.*",
    ]
    for e in entries:
        title = e["title"]
        # Too short
        if len(title) < MIN_TITLE_LEN:
            findings.append({
                "type": "noise_short",
                "severity": "high",
                "entry": e,
                "reason": f"Title too short ({len(title)} chars)",
            })
            continue
        # Matches noise patterns
        for pat in noise_patterns:
            if re.match(pat, title, re.IGNORECASE):
                findings.append({
                    "type": "noise_pattern",
                    "severity": "medium",
                    "entry": e,
                    "reason": f"Matches noise pattern: {pat}",
                })
                break
        # Technical one-offs that shouldn't be in long-term memory
        if any(k in title.lower() for k in ["css selector", "field name", "query param", "api endpoint"]):
            findings.append({
                "type": "noise_technical",
                "severity": "medium",
                "entry": e,
                "reason": "One-off technical detail not useful long-term",
            })
    return findings

def audit_orphans(entries: list[dict]) -> list[dict]:
    """Find orphaned bullet points (not under any section)."""
    findings = []
    for e in entries:
        if e.get("section") == "Top" or not e.get("section"):
            findings.append({
                "type": "orphan",
                "severity": "low",
                "entry": e,
            })
    return findings

# ─── Report Generator ────────────────────────────────────────────────────────

def generate_report(
    duplicates: list[dict],
    outdated: list[dict],
    noise: list[dict],
    orphans: list[dict],
    total_entries: int,
) -> str:
    now_str = get_now().strftime("%Y-%m-%d %H:%M %Z%z")
    lines = [
        f"# AUDIT.md — MEMORY.md Quality Audit",
        f"Generated: {now_str}",
        "",
        f"## Summary",
        f"",
        f"- Total entries scanned: {total_entries}",
        f"- Duplicates found: {len(duplicates)}",
        f"- Outdated entries: {len(outdated)}",
        f"- Noise entries: {len(noise)}",
        f"- Orphan entries: {len(orphans)}",
        f"",
    ]

    if not any([duplicates, outdated, noise, orphans]):
        lines.append("✅ **MEMORY.md is clean.** No issues found.")
        return "\n".join(lines)

    # Duplicates
    if duplicates:
        lines.append("## 🔴 Duplicates (Medium — Review for Merge)")
        lines.append("")
        for d in duplicates:
            a, b = d["entry_a"], d["entry_b"]
            lines.append(f"- **[{a['title']}]({a['section']})** ≈ **[{b['title']}]({b['section']})**")
            lines.append(f"  - Similarity: {d['similarity']:.0%} | Section A: {a['section']} | Section B: {b['section']}")
            lines.append(f"  - A date: {a.get('date','N/A')} | B date: {b.get('date','N/A')}")
            lines.append("")
        lines.append("**Recommendation:** Keep newer entry, merge older into it or delete.\n")

    # Outdated
    if outdated:
        lines.append("## 🟡 Outdated Entries (Low Priority)")
        lines.append("")
        for o in outdated:
            e = o["entry"]
            lines.append(f"- **{e['title']}** ({e.get('date','N/A')}) — {o['age_days']} days old")
            lines.append(f"  - Section: {e['section']}")
            lines.append("")
        lines.append("**Recommendation:** Review if still relevant. Consider archiving or deleting.\n")

    # Noise
    if noise:
        lines.append("## 🔴 Noise Entries (High Priority — Delete)")
        lines.append("")
        for n in noise:
            e = n["entry"]
            lines.append(f"- **[{e['title']}]({e['section']})** — {n['reason']}")
            lines.append(f"  - Body: {e.get('body','(empty)')[:100]}")
            lines.append("")
        lines.append("**Recommendation:** Delete these. They pollute MEMORY.md without adding value.\n")

    # Orphans
    if orphans:
        lines.append("## 🟡 Orphan Entries (Low Priority)")
        lines.append("")
        for o in orphans:
            e = o["entry"]
            lines.append(f"- [{e['title']}]({e['section']}) — no section header")
        lines.append("")
        lines.append("**Recommendation:** Move under appropriate section header.\n")

    # Action summary
    total_issues = len(set(e["entry"]["hash"] for f in [duplicates, noise]
                           for e in f)) + len(outdated) + len(orphans)
    lines.append("## ✅ Recommended Actions")
    lines.append("")
    if noise:
        lines.append(f"- 🔴 DELETE {len(noise)} noise entries (high priority)")
    if duplicates:
        lines.append(f"- 🟡 MERGE/DELETE {len(duplicates)} duplicate pairs")
    if outdated:
        lines.append(f"- 🟡 REVIEW {len(outdated)} outdated entries")
    if orphans:
        lines.append(f"- 🟡 FIX {len(orphans)} orphan entries")
    if not any([noise, duplicates, outdated, orphans]):
        lines.append("- No immediate action required.")

    return "\n".join(lines)

# ─── Auto-Clean ──────────────────────────────────────────────────────────────

def auto_clean(content: str, noise: list[dict], orphans: list[dict]) -> tuple[str, int]:
    """
    Auto-remove high-confidence noise entries.
    - noise type 'noise_short' and 'noise_pattern' with high severity
    Returns (cleaned_content, removed_count).
    """
    lines = content.split("\n")
    remove_indices = set()
    for n in noise:
        if n["severity"] == "high":
            remove_indices.add(n["entry"]["line_start"])
    for o in orphans:
        remove_indices.add(o["entry"]["line_start"])

    # Also remove consecutive indented lines after removed bullets
    to_remove = set()
    for idx in sorted(remove_indices, reverse=True):
        if idx < len(lines):
            to_remove.add(idx)
            # Remove following indented lines
            j = idx + 1
            while j < len(lines) and (lines[j].startswith("  ") or lines[j].strip() == ""):
                to_remove.add(j)
                j += 1

    cleaned_lines = [l for i, l in enumerate(lines) if i not in to_remove]
    return "\n".join(cleaned_lines), len(to_remove)

# ─── Main ─────────────────────────────────────────────────────────────────────

def main(apply: bool = False):
    print(f"[memos-dreaming-audit] Starting at {get_now().strftime('%Y-%m-%d %H:%M')}")

    if not MEMORY_FILE.exists():
        print(f"  [ERROR] {MEMORY_FILE} not found.")
        return

    content = MEMORY_FILE.read_text()
    entries = parse_entries(content)
    print(f"  Parsed {len(entries)} entries from MEMORY.md")

    # Run audits
    duplicates = audit_duplicates(entries)
    outdated   = audit_outdated(entries)
    noise      = audit_noise(entries)
    orphans    = audit_orphans(entries)

    print(f"  Duplicates: {len(duplicates)} | Outdated: {len(outdated)} | Noise: {len(noise)} | Orphans: {len(orphans)}")

    # Generate report
    report = generate_report(duplicates, outdated, noise, orphans, len(entries))
    ensure_dir(AUDIT_FILE)
    AUDIT_FILE.write_text(report)
    print(f"  Audit report: {AUDIT_FILE}")

    if apply:
        # Backup first
        ensure_dir(BACKUP_DIR)
        backup_path = BACKUP_DIR / f"MEMORY-{get_now().strftime('%Y-%m-%d-%H%M%S')}.md"
        shutil.copy2(MEMORY_FILE, backup_path)
        print(f"  Backup: {backup_path}")

        # Auto-clean high-confidence noise
        cleaned, removed = auto_clean(content, noise, orphans)
        if removed > 0:
            MEMORY_FILE.write_text(cleaned)
            print(f"  ✅ Auto-removed {removed} noise lines from MEMORY.md")
        else:
            print("  No high-confidence noise to auto-remove.")
    else:
        print("  Run with --apply to auto-clean noise entries.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="MEMORY.md Quality Audit")
    parser.add_argument("--apply", action="store_true", help="Auto-clean noise entries (backup first)")
    args = parser.parse_args()
    main(apply=args.apply)
