#!/usr/bin/env python3
"""
vault-write.py — Write updates back to Obsidian vault files safely.

Usage:
    python vault-write.py <vault-path> --file <filename> --action <action> [options]

Actions:
    add-task     --title "Task title" [--priority important] [--owner Dave]
    mark-done    --task-id <id>
    append-section --section "Section Title" --content "New content"

Examples:
    python vault-write.py /path/to/vault --file open-questions.md --action add-task --title "Review PR" --priority important
    python vault-write.py /path/to/vault --file open-questions.md --action mark-done --task-id 3
"""

import sys
import os
import json
import re
from pathlib import Path
from datetime import datetime

# Cross-platform file locking
try:
    import fcntl  # Unix/Linux
    HAS_FCNTL = True
except ImportError:
    HAS_FCNTL = False
    try:
        import msvcrt  # Windows
        HAS_MSVCRT = True
    except ImportError:
        HAS_MSVCRT = False

# Error codes
ERR_VAULT_NOT_FOUND = 1
ERR_FILE_NOT_FOUND = 2
ERR_CONFLICT = 3
ERR_WRITE_FAILED = 4


def load_vault(vault_path: str) -> Path:
    """Validate and return vault path."""
    path = Path(vault_path)
    if not path.exists() or not path.is_dir():
        print(f"ERROR: Vault path not found: {vault_path}", file=sys.stderr)
        sys.exit(ERR_VAULT_NOT_FOUND)
    return path


def log_audit(vault: Path, agent: str, file: str, action: str, status: str = "success"):
    """Write entry to audit log."""
    audit_file = vault / ".vault-audit.log"
    try:
        with open(audit_file, 'a', encoding='utf-8') as f:
            f.write(f"{datetime.now().isoformat()} | {agent} | {file} | {action} | {status}\n")
    except Exception:
        pass  # Audit logging is best-effort


def read_file_with_lock(filepath: Path) -> tuple:
    """Read file content. Returns (content, mtime)."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            mtime = filepath.stat().st_mtime
        return content, mtime
    except Exception as e:
        print(f"ERROR: Failed to read {filepath}: {e}", file=sys.stderr)
        sys.exit(ERR_WRITE_FAILED)


def write_file_with_lock(filepath: Path, content: str, expected_mtime: float):
    """Write file with conflict detection."""
    try:
        current_mtime = filepath.stat().st_mtime
        if expected_mtime and abs(current_mtime - expected_mtime) > 0.1:
            print(f"ERROR: Conflict detected - file changed since read", file=sys.stderr)
            sys.exit(ERR_CONFLICT)
        
        # Write to temp file first, then rename (atomic on most filesystems)
        temp_path = filepath.with_suffix('.tmp')
        with open(temp_path, 'w', encoding='utf-8') as f:
            f.write(content)
            f.flush()
            os.fsync(f.fileno())
        temp_path.replace(filepath)
    except SystemExit:
        raise
    except Exception as e:
        print(f"ERROR: Failed to write {filepath}: {e}", file=sys.stderr)
        sys.exit(ERR_WRITE_FAILED)


def find_target_file(vault: Path, filename: str) -> Path:
    """Find target file by name or type metadata."""
    filepath = vault / filename
    if filepath.exists():
        return filepath
    
    # Search subdirectories
    for md_file in vault.rglob("*.md"):
        if md_file.name == filename:
            return md_file
    
    print(f"ERROR: File not found: {filename}", file=sys.stderr)
    sys.exit(ERR_FILE_NOT_FOUND)


def add_task(vault: Path, filepath: Path, title: str, priority: str = "important", owner: str = None):
    """Add a task to an open-questions style file."""
    content, mtime = read_file_with_lock(filepath)
    lines = content.split('\n')
    
    # Find the right section based on priority
    priority_markers = {
        "critical": "🔴",
        "important": "🟡",
        "nice": "🟢"
    }
    marker = priority_markers.get(priority, "🟡")
    
    # Find insertion point (end of matching priority section)
    insert_idx = len(lines)
    in_section = False
    
    for i, line in enumerate(lines):
        if marker in line and ('###' in line or '##' in line):
            in_section = True
        elif in_section and ('###' in line or '##' in line):
            insert_idx = i
            break
    
    # Build task line
    task_line = f"- [ ] **{title}**"
    if owner:
        task_line += f" — Owner: {owner}"
    
    lines.insert(insert_idx, task_line)
    new_content = '\n'.join(lines)
    
    write_file_with_lock(filepath, new_content, mtime)
    
    agent = os.environ.get("AGENT_NAME", "unknown")
    log_audit(vault, agent, filepath.name, f"add-task: {title}")
    
    print(json.dumps({
        "status": "success",
        "action": "add-task",
        "title": title,
        "priority": priority,
        "owner": owner,
        "file": str(filepath.relative_to(vault))
    }, indent=2))


def mark_done(vault: Path, filepath: Path, task_id: int):
    """Mark a task as done by ID."""
    content, mtime = read_file_with_lock(filepath)
    lines = content.split('\n')
    
    task_counter = 0
    for i, line in enumerate(lines):
        match = re.match(r'(\s*-\s*)\[([ x])\](.*)', line)
        if match:
            task_counter += 1
            if task_counter == task_id:
                lines[i] = f"{match.group(1)}[x]{match.group(3)}"
                new_content = '\n'.join(lines)
                write_file_with_lock(filepath, new_content, mtime)
                
                agent = os.environ.get("AGENT_NAME", "unknown")
                log_audit(vault, agent, filepath.name, f"mark-done: task-{task_id}")
                
                print(json.dumps({
                    "status": "success",
                    "action": "mark-done",
                    "task_id": task_id,
                    "file": str(filepath.relative_to(vault))
                }, indent=2))
                return
    
    print(f"ERROR: Task ID {task_id} not found", file=sys.stderr)
    sys.exit(2)


def append_section(vault: Path, filepath: Path, section: str, content_to_add: str):
    """Append content to a named section."""
    content, mtime = read_file_with_lock(filepath)
    lines = content.split('\n')
    
    # Find section header
    insert_idx = len(lines)
    found = False
    
    for i, line in enumerate(lines):
        if line.strip().startswith('##') and section.lower() in line.lower():
            found = True
        elif found and line.strip().startswith('##'):
            insert_idx = i
            break
    
    if not found:
        # Append section at end
        lines.append(f"\n## {section}")
        insert_idx = len(lines)
    
    lines.insert(insert_idx, content_to_add)
    new_content = '\n'.join(lines)
    
    write_file_with_lock(filepath, new_content, mtime)
    
    agent = os.environ.get("AGENT_NAME", "unknown")
    log_audit(vault, agent, filepath.name, f"append-section: {section}")
    
    print(json.dumps({
        "status": "success",
        "action": "append-section",
        "section": section,
        "file": str(filepath.relative_to(vault))
    }, indent=2))


def main():
    # Determine vault path: positional arg > env var
    if len(sys.argv) >= 2 and not sys.argv[1].startswith("--"):
        vault_path = sys.argv[1]
        start_idx = 2
    else:
        vault_path = os.environ.get("OBSIDIAN_VAULT_PATH")
        start_idx = 1
        if not vault_path:
            print("Usage: vault-write.py [vault-path] --file <filename> --action <action> [options]")
            print("Or set OBSIDIAN_VAULT_PATH environment variable")
            sys.exit(1)
    argv = sys.argv
    vault = load_vault(vault_path)
    
    # Parse arguments
    filename = None
    action = None
    title = None
    priority = "important"
    owner = None
    task_id = None
    section = None
    content = None
    
    i = start_idx
    while i < len(argv):
        arg = argv[i]
        if arg == "--file" and i + 1 < len(argv):
            filename = argv[i + 1]
            i += 2
        elif arg == "--action" and i + 1 < len(argv):
            action = argv[i + 1]
            i += 2
        elif arg == "--title" and i + 1 < len(argv):
            title = argv[i + 1]
            i += 2
        elif arg == "--priority" and i + 1 < len(argv):
            priority = argv[i + 1]
            i += 2
        elif arg == "--owner" and i + 1 < len(argv):
            owner = argv[i + 1]
            i += 2
        elif arg == "--task-id" and i + 1 < len(argv):
            task_id = int(argv[i + 1])
            i += 2
        elif arg == "--section" and i + 1 < len(argv):
            section = argv[i + 1]
            i += 2
        elif arg == "--content" and i + 1 < len(argv):
            content = argv[i + 1]
            i += 2
        else:
            i += 1
    
    if not filename or not action:
        print("ERROR: --file and --action are required", file=sys.stderr)
        sys.exit(1)
    
    filepath = find_target_file(vault, filename)
    
    if action == "add-task":
        if not title:
            print("ERROR: --title required for add-task", file=sys.stderr)
            sys.exit(1)
        add_task(vault, filepath, title, priority, owner)
    elif action == "mark-done":
        if task_id is None:
            print("ERROR: --task-id required for mark-done", file=sys.stderr)
            sys.exit(1)
        mark_done(vault, filepath, task_id)
    elif action == "append-section":
        if not section or not content:
            print("ERROR: --section and --content required for append-section", file=sys.stderr)
            sys.exit(1)
        append_section(vault, filepath, section, content)
    else:
        print(f"ERROR: Unknown action: {action}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
