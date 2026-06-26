#!/usr/bin/env python3
"""
vault-read.py — Read and parse Obsidian vault files into structured JSON.

Usage:
    python vault-read.py <vault-path> [--file <filename>] [--format json|markdown]

Examples:
    python vault-read.py /path/to/vault --file open-questions.md --format json
    python vault-read.py /path/to/vault  # list all files with metadata
"""

import sys
import os
import json
import re
from pathlib import Path

try:
    import frontmatter
except ImportError:
    frontmatter = None


# Error codes
ERR_VAULT_NOT_FOUND = 1
ERR_FILE_NOT_FOUND = 2
ERR_PARSE_FAILED = 3


def load_vault(vault_path: str) -> Path:
    """Validate and return vault path."""
    path = Path(vault_path)
    if not path.exists() or not path.is_dir():
        print(f"ERROR: Vault path not found: {vault_path}", file=sys.stderr)
        sys.exit(ERR_VAULT_NOT_FOUND)
    return path


def discover_files(vault: Path) -> list:
    """Discover all markdown files in vault with frontmatter metadata."""
    files = []
    for md_file in vault.rglob("*.md"):
        meta = {}
        if frontmatter:
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    post = frontmatter.load(f)
                    meta = post.metadata
            except Exception:
                pass
        files.append({
            "path": str(md_file.relative_to(vault)),
            "name": md_file.name,
            "type": meta.get("type", guess_type(md_file.name)),
            "status": meta.get("status", "active"),
            "size": md_file.stat().st_size
        })
    return files


def guess_type(filename: str) -> str:
    """Guess file type from filename."""
    fname = filename.lower()
    if "open-question" in fname or "todo" in fname:
        return "open-questions"
    if "team" in fname:
        return "team"
    if "milestone" in fname:
        return "milestones"
    if "business-plan" in fname:
        return "business-plan"
    if "architecture" in fname:
        return "architecture"
    return "generic"


def parse_tasks(content: str) -> list:
    """Parse checkbox items from markdown into task objects."""
    tasks = []
    current_priority = "important"
    
    lines = content.split('\n')
    for i, line in enumerate(lines):
        # Detect priority from section headers
        if '🔴' in line or 'critical' in line.lower():
            current_priority = "critical"
        elif '🟡' in line or 'important' in line.lower():
            current_priority = "important"
        elif '🟢' in line or 'nice' in line.lower():
            current_priority = "nice"
        
        # Parse checkbox items
        match = re.match(r'\s*-\s*\[([ x])\]\s*(.*)', line)
        if match:
            checked = match.group(1).lower() == 'x'
            text = match.group(2).strip()
            
            # Extract bold title
            title_match = re.match(r'\*\*(.*?)\*\*\s*[—\-–]?\s*(.*)', text)
            if title_match:
                title = title_match.group(1)
                description = title_match.group(2).strip()
            else:
                parts = re.split(r'\s*[—\-–]\s*', text, maxsplit=1)
                title = parts[0].strip()
                description = parts[1].strip() if len(parts) > 1 else ""
            
            # Extract owner
            owner = None
            owner_match = re.search(r'Owner:\s*(\w+)', text, re.IGNORECASE)
            if owner_match:
                owner = owner_match.group(1)
            
            tasks.append({
                "id": len(tasks) + 1,
                "title": title,
                "description": description,
                "status": "done" if checked else "todo",
                "priority": current_priority,
                "owner": owner,
                "line": i + 1
            })
    
    return tasks


def parse_team(content: str) -> list:
    """Parse team members from markdown."""
    members = []
    current = None
    
    for line in content.split('\n'):
        # Match ### Name — Role
        header_match = re.match(r'###\s+(.+?)\s*[—\-–]\s*(.+)', line)
        if header_match:
            if current:
                members.append(current)
            current = {
                "name": header_match.group(1).strip(),
                "role": header_match.group(2).strip(),
                "responsibilities": [],
                "telegram_bot": None
            }
        elif current and line.strip().startswith('- '):
            current["responsibilities"].append(line.strip()[2:])
        
        # Extract telegram bot
        tg_match = re.search(r'Telegram:\s*@(\w+)', line)
        if tg_match and current:
            current["telegram_bot"] = "@" + tg_match.group(1)
    
    if current:
        members.append(current)
    
    return members


def read_file(vault: Path, filename: str, fmt: str = "json") -> dict:
    """Read and parse a specific vault file."""
    # Try direct path first
    filepath = vault / filename
    if not filepath.exists():
        # Try discovery by type
        files = discover_files(vault)
        target_type = guess_type(filename)
        matches = [f for f in files if f["type"] == target_type]
        if matches:
            filepath = vault / matches[0]["path"]
        else:
            print(f"ERROR: File not found: {filename}", file=sys.stderr)
            sys.exit(ERR_FILE_NOT_FOUND)
    
    # Read content
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            if frontmatter:
                post = frontmatter.load(f)
                content = post.content
                metadata = post.metadata
            else:
                content = f.read()
                metadata = {}
    except Exception as e:
        print(f"ERROR: Failed to read {filepath}: {e}", file=sys.stderr)
        sys.exit(ERR_PARSE_FAILED)
    
    # Parse based on file type
    file_type = metadata.get("type", guess_type(filepath.name))
    
    result = {
        "file": str(filepath.relative_to(vault)),
        "type": file_type,
        "metadata": metadata
    }
    
    if fmt == "markdown":
        result["content"] = content
    elif file_type == "open-questions":
        result["tasks"] = parse_tasks(content)
    elif file_type == "team":
        result["members"] = parse_team(content)
    else:
        # Generic: extract sections
        sections = []
        for line in content.split('\n'):
            if line.startswith('## '):
                sections.append(line[3:].strip())
        result["sections"] = sections
        result["content"] = content[:2000]  # Truncated preview
    
    return result


def main():
    # Determine vault path: positional arg > env var
    if len(sys.argv) >= 2 and not sys.argv[1].startswith("--"):
        vault_path = sys.argv[1]
        arg_start = 2
    else:
        vault_path = os.environ.get("OBSIDIAN_VAULT_PATH")
        arg_start = 1
        if not vault_path:
            print("Usage: vault-read.py [vault-path] [--file <filename>] [--format json|markdown]")
            print("Or set OBSIDIAN_VAULT_PATH environment variable")
            sys.exit(1)
    vault = load_vault(vault_path)
    
    # Parse arguments
    filename = None
    fmt = "json"
    
    i = arg_start
    while i < len(sys.argv):
        if sys.argv[i] == "--file" and i + 1 < len(sys.argv):
            filename = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--format" and i + 1 < len(sys.argv):
            fmt = sys.argv[i + 1]
            i += 2
        else:
            i += 1
    
    if filename:
        result = read_file(vault, filename, fmt)
    else:
        # List all files
        result = {
            "vault": str(vault),
            "files": discover_files(vault)
        }
    
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
