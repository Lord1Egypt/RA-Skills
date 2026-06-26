"""
Quick-fix commands for correcting entity metadata without opening files.

Users will inevitably need to fix LLM mistakes:
- Wrong entity type ("Greptile" classified as person instead of tool)
- Wrong name (canonical name needs changing)
- Add/remove facts
"""

from __future__ import annotations

import re
import shutil
from pathlib import Path

from .filelock import safe_write


def fix_type(entities_dir: Path, entity_name: str, new_type: str) -> str:
    """Change an entity's type."""
    from .core import sanitize_filename
    
    filename = sanitize_filename(entity_name)
    filepath = entities_dir / f"{filename}.md"
    
    if not filepath.exists():
        # Fuzzy search
        matches = [f for f in entities_dir.glob("*.md") 
                   if entity_name.lower() in f.stem.lower()]
        if matches:
            filepath = matches[0]
        else:
            return f"Entity '{entity_name}' not found"
    
    content = filepath.read_text()
    old = re.search(r'\*\*Type:\*\*\s*\w+', content)
    if old:
        content = content.replace(old.group(), f"**Type:** {new_type}")
        safe_write(filepath, content)
        return f"Updated {filepath.stem}: type → {new_type}"
    else:
        return f"No type field found in {filepath.stem}"


def fix_name(entities_dir: Path, old_name: str, new_name: str) -> str:
    """Rename an entity (file + content)."""
    from .core import sanitize_filename
    
    old_filename = sanitize_filename(old_name)
    new_filename = sanitize_filename(new_name)
    old_path = entities_dir / f"{old_filename}.md"
    new_path = entities_dir / f"{new_filename}.md"
    
    if not old_path.exists():
        return f"Entity '{old_name}' not found"
    
    if new_path.exists():
        return f"Entity '{new_name}' already exists — use `garden merge` instead"
    
    content = old_path.read_text()
    content = content.replace(f"# {old_name}", f"# {new_name}", 1)
    safe_write(new_path, content)
    old_path.unlink()
    
    return f"Renamed: {old_name} → {new_name}"


def add_fact(entities_dir: Path, entity_name: str, fact: str) -> str:
    """Add a fact to an entity."""
    from .core import sanitize_filename
    
    filename = sanitize_filename(entity_name)
    filepath = entities_dir / f"{filename}.md"
    
    if not filepath.exists():
        matches = [f for f in entities_dir.glob("*.md") 
                   if entity_name.lower() in f.stem.lower()]
        if matches:
            filepath = matches[0]
        else:
            return f"Entity '{entity_name}' not found"
    
    content = filepath.read_text()
    
    if fact in content:
        return f"Fact already exists in {filepath.stem}"
    
    if "## Facts" in content:
        content = content.replace("## Facts\n", f"## Facts\n- {fact}\n", 1)
    else:
        # Add Facts section before Timeline
        if "## Timeline" in content:
            content = content.replace("## Timeline", f"## Facts\n- {fact}\n\n## Timeline")
        else:
            content += f"\n## Facts\n- {fact}\n"
    
    safe_write(filepath, content)
    return f"Added fact to {filepath.stem}: {fact}"


def remove_fact(entities_dir: Path, entity_name: str, fact_substring: str) -> str:
    """Remove a fact containing the given substring."""
    from .core import sanitize_filename
    
    filename = sanitize_filename(entity_name)
    filepath = entities_dir / f"{filename}.md"
    
    if not filepath.exists():
        return f"Entity '{entity_name}' not found"
    
    lines = filepath.read_text().split('\n')
    removed = False
    new_lines = []
    
    for line in lines:
        if line.strip().startswith('- ') and fact_substring.lower() in line.lower():
            removed = True
            continue
        new_lines.append(line)
    
    if removed:
        safe_write(filepath, '\n'.join(new_lines))
        return f"Removed fact containing '{fact_substring}' from {filepath.stem}"
    else:
        return f"No fact matching '{fact_substring}' found in {filepath.stem}"
