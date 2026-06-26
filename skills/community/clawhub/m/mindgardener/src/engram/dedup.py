"""
Entity Deduplication — Merges duplicate entity files.

Problem: LLMs extract "steipete" and "Peter Steinberger" as separate entities,
but they're the same person. We need to detect and merge these.

Approach:
1. Rule-based: known aliases in config (steipete = Peter Steinberger)
2. Graph-based: if two entities share many triplet connections, flag as potential dupes
3. Content-based: if two entity files have high overlap in timeline events
"""

from __future__ import annotations

import json
import os
import re
import shutil
from pathlib import Path
from datetime import datetime


# Known alias patterns — common ways LLMs split the same entity
ALIAS_PATTERNS = [
    # GitHub handles vs real names
    (r'^@?(\w+)$', 'handle'),
    # PR #1234 vs PR-1234
    (r'^PR\s*#?(\d+)$', 'pr'),
    # Company Name vs company-name
    (r'^[\w\s]+$', 'name'),
]


def sanitize_filename(name: str) -> str:
    return re.sub(r'[^\w\s-]', '', name).strip().replace(' ', '-')


def find_duplicates(entities_dir: Path, graph_file: Path | None = None,
                    aliases: dict[str, str] | None = None) -> list[tuple[str, str, str]]:
    """
    Find potential duplicate entity files.
    
    Returns list of (file_a, file_b, reason) tuples.
    """
    duplicates = []
    
    entity_files = list(entities_dir.glob("*.md"))
    names = {f.stem.replace('-', ' ').lower(): f for f in entity_files}
    
    # 1. Check configured aliases
    if aliases:
        for canonical, alias_list in aliases.items():
            if isinstance(alias_list, str):
                alias_list = [alias_list]
            for alias in alias_list:
                canonical_lower = canonical.lower()
                alias_lower = alias.lower()
                if canonical_lower in names and alias_lower in names:
                    duplicates.append((
                        str(names[canonical_lower]),
                        str(names[alias_lower]),
                        f"configured alias: {alias} → {canonical}"
                    ))

    # 2. Substring matching (steipete ⊂ Peter Steinberger page content)
    for name_a, file_a in names.items():
        content_a = file_a.read_text().lower()
        for name_b, file_b in names.items():
            if name_a >= name_b:  # avoid self-compare and double-count
                continue
            content_b = file_b.read_text().lower()
            
            # Check if one name appears in the other's content
            if name_a in content_b and name_b in content_a:
                duplicates.append((str(file_a), str(file_b), f"mutual references"))
            
    # 3. Graph-based: shared triplet neighbors
    if graph_file and graph_file.exists():
        neighbors: dict[str, set] = {}
        for line in graph_file.read_text().strip().split('\n'):
            if not line:
                continue
            try:
                t = json.loads(line)
                s, o = t.get("subject", "").lower(), t.get("object", "").lower()
                neighbors.setdefault(s, set()).add(o)
                neighbors.setdefault(o, set()).add(s)
            except:
                pass
        
        # Find entities with high neighbor overlap
        entity_names = list(names.keys())
        for i, name_a in enumerate(entity_names):
            for name_b in entity_names[i+1:]:
                na = neighbors.get(name_a, set())
                nb = neighbors.get(name_b, set())
                if na and nb:
                    overlap = len(na & nb)
                    union = len(na | nb)
                    if union > 0 and overlap / union > 0.5:
                        duplicates.append((
                            str(names[name_a]), str(names[name_b]),
                            f"high graph overlap ({overlap}/{union} shared neighbors)"
                        ))
    
    return duplicates


def merge_entity_files(primary_path: Path, secondary_path: Path, 
                       delete_secondary: bool = False) -> str:
    """
    Merge secondary entity file into primary.
    
    - Facts from secondary are added to primary (if not duplicates)
    - Timeline entries from secondary are appended
    - Relations from secondary are added
    - Secondary file is optionally deleted
    """
    primary = primary_path.read_text()
    secondary = secondary_path.read_text()
    
    changes = []
    
    # Extract facts from secondary
    sec_facts = []
    in_facts = False
    for line in secondary.split('\n'):
        if line.startswith('## Facts'):
            in_facts = True
            continue
        if line.startswith('## ') and in_facts:
            in_facts = False
            continue
        if in_facts and line.strip().startswith('- '):
            fact = line.strip()[2:]
            if fact not in primary:
                sec_facts.append(fact)
    
    # Add new facts to primary
    if sec_facts:
        if '## Facts' in primary:
            # Find end of facts section
            lines = primary.split('\n')
            for i, line in enumerate(lines):
                if line.startswith('## Facts'):
                    insert_at = i + 1
                    while insert_at < len(lines) and not lines[insert_at].startswith('## '):
                        insert_at += 1
                    for fact in sec_facts:
                        lines.insert(insert_at, f"- {fact}")
                        insert_at += 1
                    primary = '\n'.join(lines)
                    break
        else:
            # Add facts section before timeline
            facts_block = "## Facts\n" + '\n'.join(f"- {f}" for f in sec_facts) + "\n\n"
            primary = primary.replace("## Timeline", facts_block + "## Timeline")
        changes.append(f"Added {len(sec_facts)} facts from {secondary_path.stem}")
    
    # Extract and append timeline entries from secondary
    sec_timeline_entries = re.findall(
        r'(### \[\[\d{4}-\d{2}-\d{2}\]\].*?)(?=### \[\[|\Z)', 
        secondary, re.DOTALL
    )
    for entry in sec_timeline_entries:
        date_match = re.search(r'### \[\[(\d{4}-\d{2}-\d{2})\]\]', entry)
        if date_match and date_match.group(0) not in primary:
            primary = primary.rstrip() + '\n' + entry.strip() + '\n'
            changes.append(f"Added timeline entry {date_match.group(1)}")
    
    # Add alias note
    alias_note = f"\n**Also known as:** {secondary_path.stem.replace('-', ' ')}"
    if alias_note.strip() not in primary:
        # Add after the Type line
        primary = re.sub(
            r'(\*\*Type:\*\*.*)', 
            r'\1' + alias_note,
            primary,
            count=1
        )
    
    # Write merged file
    primary_path.write_text(primary)
    
    if delete_secondary:
        secondary_path.unlink()
        changes.append(f"Deleted {secondary_path.name}")
    
    return "; ".join(changes) if changes else "No changes needed"


def run_dedup(entities_dir: Path, graph_file: Path | None = None,
              aliases: dict[str, str] | None = None,
              auto_merge: bool = False) -> list[str]:
    """
    Find and optionally merge duplicate entities.
    
    Returns list of actions taken.
    """
    actions = []
    
    dupes = find_duplicates(entities_dir, graph_file, aliases)
    
    if not dupes:
        actions.append("No duplicates found")
        return actions
    
    for file_a, file_b, reason in dupes:
        path_a = Path(file_a)
        path_b = Path(file_b)
        
        if auto_merge:
            # Merge secondary into primary (larger file wins)
            if path_a.stat().st_size >= path_b.stat().st_size:
                result = merge_entity_files(path_a, path_b, delete_secondary=True)
                actions.append(f"Merged {path_b.name} → {path_a.name} ({reason}): {result}")
            else:
                result = merge_entity_files(path_b, path_a, delete_secondary=True)
                actions.append(f"Merged {path_a.name} → {path_b.name} ({reason}): {result}")
        else:
            actions.append(f"⚠️ Potential duplicate: {path_a.stem} ↔ {path_b.stem} ({reason})")
    
    return actions
