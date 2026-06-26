#!/usr/bin/env python3
"""
Verify memory integrity after defragmentation.
Usage: python3 verify_memory.py [--path <path>]
"""

import sys
import argparse
from datetime import datetime
from pathlib import Path

def get_memory_files(base_path):
    """Get only actual memory files, not everything."""
    memory_files = []
    
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
            for f in root.glob("*.md"):
                if f.is_file() and f.name not in ["defrag_backup.md"]:
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

def verify_file(filepath):
    """Verify a single memory file."""
    issues = []
    warnings = []
    
    try:
        content = filepath.read_text()
        lines = content.split("\n")
        
        # Check size - HOT files should be lean
        if len(lines) > 200:
            issues.append(f"Exceeds 200 line limit ({len(lines)} lines)")
        
        # Check for nearly empty files
        if len(content.strip()) < 10:
            issues.append("File is nearly empty")
        
        return {
            "path": str(filepath),
            "valid": len(issues) == 0,
            "issues": issues,
            "warnings": warnings,
            "lines": len(lines),
            "size_kb": round(len(content) / 1024, 2)
        }
    except Exception as e:
        return {
            "path": str(filepath),
            "valid": False,
            "issues": [f"Error reading file: {e}"],
            "warnings": [],
            "lines": 0,
            "size_kb": 0
        }

def verify_memory_path(base_path):
    """Verify all memory files under a path."""
    results = {
        "verified": [],
        "issues": [],
        "warnings": [],
        "total_files": 0,
        "valid_files": 0
    }
    
    memory_files = get_memory_files(base_path)
    
    for filepath in memory_files:
        result = verify_file(filepath)
        results["total_files"] += 1
        
        if result["valid"]:
            results["valid_files"] += 1
            results["verified"].append(result)
        else:
            results["issues"].append(result)
        
        results["warnings"].extend([
            {"file": str(filepath), "warning": w} 
            for w in result["warnings"]
        ])
    
    return results

def print_report(results):
    """Print verification report."""
    print("\n" + "=" * 60)
    print("MEMORY VERIFICATION REPORT")
    print("=" * 60)
    
    print(f"\n📊 Summary")
    print(f"   Files verified: {results['total_files']}")
    print(f"   Valid files: {results['valid_files']}")
    print(f"   Files with issues: {len(results['issues'])}")
    print(f"   Warnings: {len(results['warnings'])}")
    
    if results["issues"]:
        print(f"\n❌ ISSUES FOUND ({len(results['issues'])})")
        print("-" * 40)
        for issue in results["issues"]:
            print(f"   ❌ {Path(issue['path']).name}: {issue['lines']} lines")
            for i in issue["issues"]:
                print(f"      - {i}")
    
    if results["warnings"]:
        print(f"\n⚠️  WARNINGS ({len(results['warnings'])})")
        print("-" * 40)
        for warn in results["warnings"][:10]:
            print(f"   ⚠️  {Path(warn['file']).name}: {warn['warning']}")
        if len(results["warnings"]) > 10:
            print(f"   ... and {len(results['warnings']) - 10} more warnings")
    
    if results["valid_files"] == results["total_files"] and not results["warnings"]:
        print("\n✅ ALL FILES VALID - Memory integrity verified!")
    elif results["valid_files"] == results["total_files"]:
        print("\n✅ All files valid (with warnings)")
    
    print()
    
    return results["valid_files"] == results["total_files"]

def main():
    parser = argparse.ArgumentParser(description="Verify memory integrity")
    parser.add_argument("--path", default="~", help="Base path for memory files")
    args = parser.parse_args()
    
    base_path = Path(args.path).expanduser()
    
    print(f"🔍 Verifying memory files under: {base_path}")
    
    results = verify_memory_path(base_path)
    is_valid = print_report(results)
    
    return 0 if is_valid else 1

if __name__ == "__main__":
    sys.exit(main())
