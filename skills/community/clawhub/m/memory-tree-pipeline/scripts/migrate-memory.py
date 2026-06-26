#!/usr/bin/env python3
"""
Memory Tree Migration

Migrates flat memory files (memory/YYYY-MM-DD.md and MEMORY.md)
into the three-scope tree structure (source/, topic/, global/).

- Creates backup before any changes
- Splits daily files into source entries
- Extracts global knowledge from MEMORY.md
- Preserves all original data — nothing is deleted
- Idempotent: running twice produces the same result

Usage:
    python3 migrate-memory.py [--dry-run] [--no-backup]

--dry-run:   Show what would be migrated without writing
--no-backup: Skip backup creation (not recommended)
"""

import json
import os
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

# ── Configuration ──────────────────────────────────────────────────────────────

WORKSPACE = Path(os.environ.get("MEMORY_WORKSPACE", os.path.expanduser("~/.openclaw/workspace")))
MEMORY_ROOT = Path(os.environ.get("MEMORY_ROOT", str(WORKSPACE / "memory")))
MEMORY_MD = Path(os.environ.get("MEMORY_MD", str(WORKSPACE / "MEMORY.md")))
SOURCE_DIR = MEMORY_ROOT / "source"
TOPIC_DIR = MEMORY_ROOT / "topic"
GLOBAL_DIR = MEMORY_ROOT / "global"
META_DIR = MEMORY_ROOT / "_meta"
BACKUP_DIR = MEMORY_ROOT / "_backup_flat"

TOKEN_RATIO = 4  # chars per token estimate


# ── MEMORY.md Section Mapping ──────────────────────────────────────────────────

# Maps MEMORY.md section headers to global/ files
MEMORY_MD_SECTIONS = {
    "IDENTITY": {
        "file": "IDENTITY.md",
        "headers": [
            "Agent Identity — Core Roles",
            "Symbiosis Doctrine",
            "Inspiration DNA",
            "The Suit Philosophy",
            "Boot Protocol",
            "Offspring Doctrine",
            "King Symbiotic",
            "The Uncrowning Law",
            "Carnage Division",
            "Evolution Doctrine",
            "Productization Directive",
            "TELOS Discipline",
            "Autonomous Executive Mode",
        ],
    },
    "DOCTRINE": {
        "file": "DOCTRINE.md",
        "headers": [
            "Security Rules",
            "Venom Mode — Activation Protocol",
            "Venom Mode Rules",
            "Security Incident",
            "Wallet Vault",
            "Model Routing Strategy",
            "Security Audit",
            "Hard rules",
            "Authorized Hacker Mode",
            "Destructive Action Rule",
        ],
    },
    "PREFERENCES": {
        "file": "PREFERENCES.md",
        "headers": [
            "Voice Configuration",
            "Model Routing",
            "Eric",
            "preferences",
            "routing strategy",
            "language",
            "bilingual",
        ],
    },
    "SECURITY": {
        "file": "SECURITY.md",
        "headers": [
            "Security Rules",
            "Security Audit",
            "Wallet Vault",
            "Security Incident",
            "Security fixes applied",
            "hacker mode",
            "destructive action",
        ],
    },
    "ARCHITECTURE": {
        "file": "ARCHITECTURE.md",
        "headers": [
            "API Layer",
            "Compatibility Layer",
            "Service Stack",
            "API Gateway",
            "Homepage Dashboard",
            "Remote Control",
            "Command Center",
            "Integration Registry",
            "Phase",
            "Department",
            "Team Structure",
            "Department Evolution",
            "Department Memory",
            "Department Toolkits",
            "Department Dispatch",
            "GUPP",
            "Scheduled Autonomy",
            "Department Workspaces",
            "Registry",
        ],
    },
    "PRODUCTS": {
        "file": "PRODUCTS.md",
        "headers": [
            "SuperClaw",
            "Avatar Runtime",
            "Conversational Presence",
            "Wake Detection",
            "NanoClaw OS",
            "Phase 8",
            "Phase 9",
            "Phase 10",
            "Phase 11",
            "Phase 12",
            "Phase 13",
            "Phase 14",
            "Cinematic Visual Identity",
            "Beta Build",
        ],
    },
}


def estimate_tokens(text: str) -> int:
    return max(1, len(text) // TOKEN_RATIO)


def split_memory_md(content: str) -> dict[str, str]:
    """
    Split MEMORY.md content into global knowledge categories.
    Returns dict of {category_name: content}.
    """
    # Split by ## headers
    sections = re.split(r"\n(?=## )", content)

    categorized = {name: [] for name in MEMORY_MD_SECTIONS}
    categorized["UNCATEGORIZED"] = []

    for section in sections:
        if not section.strip():
            continue

        # Get the header line
        header_match = re.match(r"##\s*(.+)", section.strip())
        header = header_match.group(1) if header_match else ""
        header_lower = header.lower()
        section_text = section.strip()

        # Find which category this section belongs to
        assigned = False
        for cat_name, cat_config in MEMORY_MD_SECTIONS.items():
            for cat_header in cat_config["headers"]:
                if cat_header.lower() in header_lower or header_lower.startswith(cat_header.lower()):
                    categorized[cat_name].append(section_text)
                    assigned = True
                    break
            if assigned:
                break

        if not assigned:
            # Try content-based matching for small sections
            for cat_name, cat_config in MEMORY_MD_SECTIONS.items():
                for cat_header in cat_config["headers"]:
                    if cat_header.lower() in section_text.lower()[:200]:
                        categorized[cat_name].append(section_text)
                        assigned = True
                        break
                if assigned:
                    break

        if not assigned:
            categorized["UNCATEGORIZED"].append(section_text)

    # Build final content for each category
    result = {}
    for cat_name, sections_list in categorized.items():
        if sections_list:
            result[cat_name] = "\n\n".join(sections_list)

    return result


def create_global_file(category: str, content: str) -> str:
    """Create formatted global knowledge file content."""
    header = f"# {category.title()} — Global Knowledge\n\n"
    header += f"_Migrated from MEMORY.md on {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}_\n\n"

    return header + content


def split_daily_file(content: str, filename: str) -> list[dict]:
    """
    Split a daily file into topic-based source entries.
    Each entry becomes a separate source file.
    """
    date_match = re.match(r"(\d{4}-\d{2}-\d{2})", filename)
    date = date_match.group(1) if date_match else "unknown"

    # Split by ## headers
    sections = re.split(r"\n(?=## )", content)

    entries = []
    for i, section in enumerate(sections):
        if not section.strip():
            continue

        # Extract heading for filename
        header_match = re.match(r"##\s*(.+)", section.strip())
        if header_match:
            heading = header_match.group(1).strip()
            # Clean heading for filename
            slug = re.sub(r"[^a-z0-9]+", "-", heading.lower()).strip("-")
            slug = slug[:50]  # Truncate long names
        else:
            slug = f"section-{i}"

        entry_filename = f"{date}-{slug}.md"
        entries.append({
            "filename": entry_filename,
            "date": date,
            "heading": header_match.group(1) if header_match else f"Section {i}",
            "content": section.strip(),
            "original_file": filename,
        })

    return entries


def migrate_memory_md(dry_run: bool = False) -> dict:
    """Migrate MEMORY.md into global/ files."""
    if not MEMORY_MD.exists():
        print(f"MEMORY.md not found at {MEMORY_MD}")
        return {"error": "MEMORY.md not found"}

    content = MEMORY_MD.read_text(encoding="utf-8", errors="replace")
    print(f"MEMORY.md: {estimate_tokens(content)} tokens, {len(content)} chars")

    categories = split_memory_md(content)
    results = {}

    for cat_name, cat_content in categories.items():
        if cat_name == "UNCATEGORIZED":
            # Append uncategorized content to DOCTRINE as catch-all
            if cat_content:
                doctrine_file = GLOBAL_DIR / "DOCTRINE.md"
                existing = doctrine_file.read_text(encoding="utf-8", errors="replace") if doctrine_file.exists() else ""
                global_content = create_global_file("DOCTRINE", existing + "\n\n## Uncategorized\n\n" + cat_content if existing else create_global_file("DOCTRINE", cat_content))
                if not dry_run:
                    doctrine_file.parent.mkdir(parents=True, exist_ok=True)
                    doctrine_file.write_text(global_content, encoding="utf-8")
                results["DOCTRINE"] = {
                    "tokens": estimate_tokens(global_content),
                    "sections": "uncategorized + existing",
                }
            continue

        cat_config = MEMORY_MD_SECTIONS[cat_name]
        global_file = GLOBAL_DIR / cat_config["file"]
        global_content = create_global_file(cat_name, cat_content)

        if not dry_run:
            global_file.parent.mkdir(parents=True, exist_ok=True)
            global_file.write_text(global_content, encoding="utf-8")

        results[cat_name] = {
            "file": str(cat_config["file"]),
            "tokens": estimate_tokens(global_content),
            "chars": len(global_content),
        }
        print(f"  Global: {cat_config['file']} — {estimate_tokens(global_content)} tokens")

    return results


def migrate_daily_files(dry_run: bool = False) -> dict:
    """Migrate daily memory files into source/ entries."""
    daily_files = sorted(MEMORY_ROOT.glob("2*.md"))
    # Exclude files already in subdirectories
    daily_files = [f for f in daily_files if f.parent == MEMORY_ROOT]

    print(f"Found {len(daily_files)} daily memory files")

    results = {"files": 0, "entries": 0, "topics": set()}

    for daily_file in daily_files:
        content = daily_file.read_text(encoding="utf-8", errors="replace")
        filename = daily_file.name

        entries = split_daily_file(content, filename)

        for entry in entries:
            source_path = SOURCE_DIR / entry["filename"]

            # Add provenance frontmatter
            provenance = f"""---
source: {filename}
date: {entry['date']}
heading: {entry['heading']}
migrated: {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}
---

"""
            source_content = provenance + entry["content"]

            if not dry_run:
                source_path.parent.mkdir(parents=True, exist_ok=True)
                # Don't overwrite if file already exists (idempotent)
                if not source_path.exists():
                    source_path.write_text(source_content, encoding="utf-8")

            results["entries"] += 1

        results["files"] += 1
        print(f"  Migrated: {filename} → {len(entries)} entries")

    results["topics"] = list(results["topics"])
    return results


def create_backup(dry_run: bool = False) -> bool:
    """Create backup of existing flat memory structure."""
    if dry_run:
        print(f"[DRY RUN] Would create backup at {BACKUP_DIR}")
        return True

    if BACKUP_DIR.exists():
        print(f"Backup already exists at {BACKUP_DIR}")
        return True

    print(f"Creating backup at {BACKUP_DIR}...")
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    # Backup daily files
    for f in MEMORY_ROOT.glob("2*.md"):
        if f.parent == MEMORY_ROOT:
            shutil.copy2(f, BACKUP_DIR / f.name)

    # Backup other key files
    for name in ["backup.log", "d-drive-inventory.md", "heartbeat-state.json"]:
        src = MEMORY_ROOT / name
        if src.exists():
            shutil.copy2(src, BACKUP_DIR / name)

    # Backup MEMORY.md
    if MEMORY_MD.exists():
        shutil.copy2(MEMORY_MD, BACKUP_DIR / "MEMORY.md")

    # Backup .dreams directory
    dreams_dir = MEMORY_ROOT / ".dreams"
    if dreams_dir.exists():
        shutil.copytree(dreams_dir, BACKUP_DIR / ".dreams", dirs_exist_ok=True)

    print(f"Backup complete: {BACKUP_DIR}")
    return True


def init_meta(dry_run: bool = False):
    """Initialize _meta/index.json with migration info."""
    index = {
        "version": 1,
        "migrated_at": datetime.now(timezone.utc).isoformat(),
        "migration_source": "flat_files",
        "sources": {},
        "source_to_topic": {},
        "topics": {},
        "global": {},
        "last_seal": None,
    }

    # Count source files
    for source_file in SOURCE_DIR.glob("*.md"):
        rel = str(source_file.relative_to(MEMORY_ROOT))
        content = source_file.read_text(encoding="utf-8", errors="replace")
        index["sources"][rel] = {
            "sealed": False,
            "hash": "",
            "tokens": estimate_tokens(content),
            "migrated_from": "daily_file",
        }

    if not dry_run:
        META_DIR.mkdir(parents=True, exist_ok=True)
        index_file = META_DIR / "index.json"
        if not index_file.exists():
            import hashlib
            with open(index_file, "w") as f:
                json.dump(index, f, indent=2, ensure_ascii=False)
            print(f"Created index: {index_file}")

    return index


# ── Main ────────────────────────────────────────────────────────────────────────

def main():
    dry_run = "--dry-run" in sys.argv
    no_backup = "--no-backup" in sys.argv

    print("=" * 60)
    print("Memory Tree Migration")
    print("=" * 60)

    if dry_run:
        print("\n[DRY RUN] No files will be written.\n")

    # Step 1: Create backup
    if not no_backup:
        print("\n--- Step 1: Creating Backup ---")
        create_backup(dry_run)

    # Step 2: Ensure directory structure
    print("\n--- Step 2: Creating Directory Structure ---")
    for d in [SOURCE_DIR, TOPIC_DIR, GLOBAL_DIR, META_DIR]:
        if not dry_run:
            d.mkdir(parents=True, exist_ok=True)
        print(f"  {'Would create' if dry_run else 'Ensured'}: {d.relative_to(WORKSPACE)}")

    # Step 3: Migrate MEMORY.md → global/
    print("\n--- Step 3: Migrating MEMORY.md → global/ ---")
    md_results = migrate_memory_md(dry_run)

    # Step 4: Migrate daily files → source/
    print("\n--- Step 4: Migrating Daily Files → source/ ---")
    daily_results = migrate_daily_files(dry_run)

    # Step 5: Initialize _meta/
    print("\n--- Step 5: Initializing _meta/ ---")
    init_meta(dry_run)

    # Summary
    print("\n" + "=" * 60)
    print("Migration Summary")
    print("=" * 60)
    print(f"MEMORY.md → global/ : {len(md_results)} categories")
    print(f"Daily files → source/ : {daily_results['files']} files → {daily_results['entries']} entries")
    if not dry_run:
        print(f"\nOriginal files preserved. Backup at: {BACKUP_DIR}")
        print(f"Run seal-worker.py to generate topic summaries and update global knowledge.")
    else:
        print("\n[DRY RUN] No files were written. Run without --dry-run to perform migration.")


if __name__ == "__main__":
    main()
