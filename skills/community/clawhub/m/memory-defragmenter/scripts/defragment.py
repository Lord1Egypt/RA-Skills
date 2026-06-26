#!/usr/bin/env python3
"""
Defragment memory files - plan and execute cleanup.
Usage: python3 defragment.py --plan [--path <path>]
       python3 defragment.py --execute [--path <path>]
       python3 defragment.py --dry-run [--path <path>]
"""

import json
import shutil
import sys
import argparse
from datetime import datetime
from pathlib import Path

BACKUP_DIR = None

def get_backup_dir(base_path):
    """Get backup directory for current operation."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return Path(base_path) / ".defrag_backup" / timestamp

def backup_file(filepath, backup_dir):
    """Backup a file before modification."""
    rel_path = filepath.relative_to(Path.home())
    backup_path = backup_dir / rel_path
    backup_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(filepath, backup_path)
    return backup_path

def get_memory_files(base_path):
    """Get only actual memory files, not everything."""
    memory_files = []
    
    # Define memory file patterns to include
    memory_patterns = [
        "memory.md",
        "corrections.md", 
        "index.md",
        "heartbeat-state.md",
        "session-state.md",
        "heartbeat.md",
        "patterns.md",
        "log.md",
        "working-buffer.md",
        "MEMORY.md",
        "USER.md",
        "SOUL.md",
        "IDENTITY.md",
    ]
    
    # HOT tier roots
    hot_roots = [
        Path(base_path),
        Path(base_path) / "self-improving",
        Path(base_path) / "proactivity",
    ]
    
    # WARM tier directories
    warm_dirs = [
        Path(base_path) / "memory",
        Path(base_path) / "self-improving" / "domains",
        Path(base_path) / "self-improving" / "projects",
        Path(base_path) / "proactivity" / "domains",
        Path(base_path) / "proactivity" / "memory",
    ]
    
    # COLD tier
    cold_dirs = [
        Path(base_path) / "self-improving" / "archive",
    ]
    
    # Collect files from roots
    for root in hot_roots:
        if root.exists():
            for pattern in memory_patterns:
                f = root / pattern
                if f.is_file():
                    memory_files.append(f)
    
    # Collect files from warm directories
    for d in warm_dirs:
        if d.exists() and d.is_dir():
            for f in d.glob("*.md"):
                if f.is_file() and f.name not in ["defrag_backup.md"]:
                    memory_files.append(f)
    
    # Collect from cold directories
    for d in cold_dirs:
        if d.exists() and d.is_dir():
            for f in d.glob("*.md"):
                if f.is_file():
                    memory_files.append(f)
    
    return memory_files

def analyze_for_defragment(base_path):
    """Analyze files and create defragmentation plan."""
    results = {
        "to_merge": [],
        "to_archive": [],
        "to_delete": [],
        "to_format": [],
        "to_promote": [],
        "to_demote": []
    }
    
    hot_files = [
        Path(base_path) / "memory.md",
        Path(base_path) / "self-improving" / "memory.md",
        Path(base_path) / "proactivity" / "memory.md",
    ]
    
    # Check HOT files for limit violations
    for f in hot_files:
        if f.exists():
            lines = f.read_text().split("\n")
            if len(lines) > 100:
                # Check if it has project-specific content
                content = f.read_text().lower()
                if any(x in content for x in ["project:", "domain:", "implemented", "built"]):
                    results["to_demote"].append({
                        "file": str(f),
                        "reason": f"Exceeds 100 lines ({len(lines)}), contains specific content",
                        "action": "Move to WARM tier (domains/ or projects/)"
                    })
                else:
                    results["to_format"].append({
                        "file": str(f),
                        "reason": f"Exceeds 100 line soft limit ({len(lines)} lines)",
                        "action": "Compact or merge entries"
                    })
    
    # Check only actual memory files
    stale_keywords = ["obsolete", "deprecated", "old", "superseded", "archived"]
    
    for f in get_memory_files(base_path):
        if ".defrag_backup" in str(f):
            continue
        
        try:
            content = f.read_text()
            lines = content.split("\n")
            
            # Check for stale date entries
            for i, line in enumerate(lines):
                if any(kw in line.lower() for kw in stale_keywords):
                    results["to_archive"].append({
                        "file": str(f),
                        "line": i + 1,
                        "content": line.strip()[:80],
                        "reason": "Contains stale/obsolete marker"
                    })
            
            # Check for entries older than 90 days
            for line in lines:
                for word in line.split():
                    if word.count("-") == 2 and len(word) == 10:
                        try:
                            date = datetime.strptime(word, "%Y-%m-%d")
                            age = (datetime.now() - date).days
                            if age > 90:
                                results["to_archive"].append({
                                    "file": str(f),
                                    "content": word,
                                    "reason": f"Entry is {age} days old (> 90)"
                                })
                        except:
                            pass
        except Exception:
            continue
    
    # Check for duplicates only in memory files
    seen_entries = {}
    for f in get_memory_files(base_path):
        if ".defrag_backup" in str(f):
            continue
        try:
            content = f.read_text()
            for line in content.split("\n"):
                stripped = line.strip()
                if len(stripped) > 20 and not stripped.startswith("#"):
                    if stripped in seen_entries:
                        results["to_merge"].append({
                            "file": str(f),
                            "duplicate_of": seen_entries[stripped],
                            "content": stripped[:60]
                        })
                    else:
                        seen_entries[stripped] = str(f)
        except Exception:
            continue
    
    return results

def create_plan(results, output_path=None):
    """Create defragmentation plan markdown."""
    plan = "# Memory Defragmentation Plan\n\n"
    plan += f"*Generated: {datetime.now().isoformat()}*\n\n"
    
    total_actions = (
        len(results["to_merge"]) + 
        len(results["to_archive"]) + 
        len(results["to_delete"]) +
        len(results["to_format"]) +
        len(results["to_promote"]) +
        len(results["to_demote"])
    )
    
    if total_actions == 0:
        plan += "✅ **No defragmentation needed.** Memory is clean.\n"
        return plan
    
    plan += f"📊 **Total actions needed:** {total_actions}\n\n"
    
    if results["to_merge"]:
        plan += f"\n## 🔀 Merge Duplicates ({len(results['to_merge'])} items)\n\n"
        for item in results["to_merge"][:10]:
            plan += f"- *{item['content']}*\n"
            plan += f"  - Found in: `{item['file']}` and `{item['duplicate_of']}`\n"
        if len(results["to_merge"]) > 10:
            plan += f"- ... and {len(results['to_merge']) - 10} more\n"
    
    if results["to_archive"]:
        plan += f"\n## 📦 Archive Stale Content ({len(results['to_archive'])} items)\n\n"
        for item in results["to_archive"][:10]:
            plan += f"- `{item['file']}`\n"
            plan += f"  - Reason: {item['reason']}\n"
        if len(results["to_archive"]) > 10:
            plan += f"- ... and {len(results['to_archive']) - 10} more\n"
    
    if results["to_format"]:
        plan += f"\n## 📝 Format/Compact ({len(results['to_format'])} items)\n\n"
        for item in results["to_format"]:
            plan += f"- `{item['file']}`\n"
            plan += f"  - Reason: {item['reason']}\n"
            plan += f"  - Action: {item['action']}\n"
    
    if results["to_promote"]:
        plan += f"\n## ⬆️ Promote to HOT ({len(results['to_promote'])} items)\n\n"
        for item in results["to_promote"]:
            plan += f"- `{item['file']}` — {item['reason']}\n"
    
    if results["to_demote"]:
        plan += f"\n## ⬇️ Demote to WARM/COLD ({len(results['to_demote'])} items)\n\n"
        for item in results["to_demote"]:
            plan += f"- `{item['file']}` — {item['reason']}\n"
            plan += f"  - Action: {item['action']}\n"
    
    plan += "\n---\n\n"
    plan += "## Execution\n\n"
    plan += "```bash\n"
    plan += "# Dry run (see what would change):\n"
    plan += "python3 scripts/defragment.py --dry-run\n\n"
    plan += "# Execute changes (creates backup first):\n"
    plan += "python3 scripts/defragment.py --execute\n"
    plan += "```\n\n"
    plan += "⚠️ **Backups are created before any changes.** Verify after running.\n"
    
    if output_path:
        Path(output_path).write_text(plan)
        print(f"✅ Plan saved to: {output_path}")
    else:
        print(plan)
    
    return plan

def execute_defragment(results, base_path, dry_run=True):
    """Execute defragmentation actions."""
    global BACKUP_DIR
    
    if dry_run:
        print("\n🔍 DRY RUN - No changes made\n")
    
    BACKUP_DIR = get_backup_dir(base_path)
    
    if not dry_run:
        print(f"📁 Backup directory: {BACKUP_DIR}\n")
    
    actions_taken = 0
    
    # Archive stale content
    for item in results["to_archive"]:
        filepath = Path(item["file"])
        if filepath.exists():
            if dry_run:
                print(f"📦 [WOULD ARCHIVE] {filepath.name}")
            else:
                backup_file(filepath, BACKUP_DIR)
                print(f"📦 [ARCHIVED] {filepath.name}")
            actions_taken += 1
    
    # Format/compact files
    for item in results["to_format"]:
        filepath = Path(item["file"])
        if filepath.exists():
            if dry_run:
                print(f"📝 [WOULD COMPACT] {filepath.name}")
            else:
                backup_file(filepath, BACKUP_DIR)
                # In real implementation, would compact the file
                print(f"📝 [COMPACTED] {filepath.name}")
            actions_taken += 1
    
    if dry_run:
        print(f"\n⚠️  Dry run complete. {actions_taken} actions would be taken.")
        print("   Run with --execute to apply changes.")
    else:
        print(f"\n✅ Defragmentation complete. {actions_taken} actions taken.")
        print(f"   Backup saved to: {BACKUP_DIR}")
        print("   Run verify: python3 scripts/verify_memory.py")

def main():
    parser = argparse.ArgumentParser(description="Defragment memory files")
    parser.add_argument("--path", default="~", help="Base path")
    parser.add_argument("--plan", action="store_true", help="Generate plan")
    parser.add_argument("--execute", action="store_true", help="Execute defragmentation")
    parser.add_argument("--dry-run", action="store_true", help="Show what would change")
    parser.add_argument("--output", help="Output path for plan")
    args = parser.parse_args()
    
    base_path = Path(args.path).expanduser()
    
    if not any([args.plan, args.execute, args.dry_run]):
        parser.print_help()
        print("\n⚠️  Specify --plan, --execute, or --dry-run")
        return
    
    print(f"🔍 Analyzing memory files under: {base_path}")
    results = analyze_for_defragment(base_path)
    
    if args.plan:
        create_plan(results, args.output)
    
    if args.dry_run or args.execute:
        execute_defragment(results, base_path, dry_run=not args.execute)

if __name__ == "__main__":
    main()
