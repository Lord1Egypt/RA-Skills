"""Entity alias resolution — merge duplicate entities.

Handles cases like "steipete" and "Peter Steinberger" being the same person.
Aliases are stored in a simple YAML/JSON file alongside entities.
"""

import json
import re
from pathlib import Path
from typing import Optional

from .filelock import safe_write


def load_aliases(entities_dir: Path) -> dict[str, str]:
    """Load alias mappings from entities/.aliases.json.
    
    Format: {"alias": "canonical_name"}
    Example: {"steipete": "Peter Steinberger", "PR #18444": "OpenClaw PR #18444"}
    """
    alias_file = entities_dir / ".aliases.json"
    if alias_file.exists():
        return json.loads(alias_file.read_text())
    return {}


def save_aliases(entities_dir: Path, aliases: dict[str, str]):
    """Save alias mappings."""
    alias_file = entities_dir / ".aliases.json"
    safe_write(alias_file, json.dumps(aliases, indent=2) + "\n")


def resolve_name(name: str, aliases: dict[str, str]) -> str:
    """Resolve an entity name through aliases."""
    return aliases.get(name, name)


def merge_entities(entities_dir: Path, source: str, target: str):
    """Merge source entity into target entity.
    
    - Appends source timeline entries to target
    - Updates .aliases.json
    - Removes source file
    """
    source_file = entities_dir / f"{_sanitize(source)}.md"
    target_file = entities_dir / f"{_sanitize(target)}.md"
    
    if not source_file.exists():
        print(f"Source entity not found: {source}")
        return
    
    source_content = source_file.read_text()
    
    if target_file.exists():
        target_content = target_file.read_text()
        
        # Extract timeline entries from source
        timeline_match = re.search(r'## Timeline\n(.*?)(?=\n## |\Z)', source_content, re.DOTALL)
        if timeline_match:
            source_timeline = timeline_match.group(1).strip()
            
            # Extract facts from source
            facts_match = re.search(r'## Facts\n(.*?)(?=\n## |\Z)', source_content, re.DOTALL)
            source_facts = facts_match.group(1).strip() if facts_match else ""
            
            # Append facts that don't exist
            if source_facts:
                for line in source_facts.split("\n"):
                    line = line.strip()
                    if line and line not in target_content:
                        # Find facts section in target
                        if "## Facts" in target_content:
                            target_content = target_content.replace(
                                "## Facts\n",
                                f"## Facts\n{line}\n",
                                1
                            )
            
            # Append timeline entries that don't exist
            for entry in re.split(r'(?=### \[\[)', source_timeline):
                entry = entry.strip()
                if entry and entry not in target_content:
                    # Add before Relations section or at end
                    if "## Relations" in target_content:
                        target_content = target_content.replace(
                            "## Relations",
                            f"{entry}\n\n## Relations"
                        )
                    else:
                        target_content = target_content.rstrip() + f"\n\n{entry}\n"
        
        # Add alias note
        if f"Also known as: {source}" not in target_content:
            target_content = target_content.replace(
                f"\n## Timeline",
                f"\n**Also known as:** {source}\n\n## Timeline"
            )
        
        safe_write(target_file, target_content)
    else:
        # Just rename the file and update header
        source_content = source_content.replace(f"# {source}", f"# {target}\n**Also known as:** {source}")
        safe_write(target_file, source_content)
    
    # Remove source file
    source_file.unlink()
    
    # Update aliases
    aliases = load_aliases(entities_dir)
    aliases[source] = target
    save_aliases(entities_dir, aliases)
    
    print(f"Merged '{source}' → '{target}'")


def detect_duplicates(entities_dir: Path) -> list[tuple[str, str, float]]:
    """Detect potential duplicate entities.
    
    Returns: list of (entity_a, entity_b, confidence) tuples.
    """
    files = list(entities_dir.glob("*.md"))
    names = [f.stem.replace("-", " ") for f in files]
    
    duplicates = []
    
    for i, name_a in enumerate(names):
        for j, name_b in enumerate(names):
            if j <= i:
                continue
            
            # Check if one name contains the other
            a_lower = name_a.lower()
            b_lower = name_b.lower()
            
            if a_lower in b_lower or b_lower in a_lower:
                duplicates.append((name_a, name_b, 0.8))
                continue
            
            # Check if they share significant words
            words_a = set(a_lower.split()) - {"the", "a", "an", "of", "at", "in", "on"}
            words_b = set(b_lower.split()) - {"the", "a", "an", "of", "at", "in", "on"}
            
            if words_a and words_b:
                overlap = len(words_a & words_b) / min(len(words_a), len(words_b))
                if overlap >= 0.5:
                    duplicates.append((name_a, name_b, overlap))
    
    return sorted(duplicates, key=lambda x: -x[2])


def _sanitize(name: str) -> str:
    """Convert name to filename."""
    return re.sub(r'[^\w\s-]', '', name).strip().replace(' ', '-')
