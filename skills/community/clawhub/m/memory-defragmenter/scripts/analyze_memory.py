#!/usr/bin/env python3
"""
Analyze memory files for defragmentation opportunities.
Usage: python3 analyze_memory.py [--path <path>]
"""

import json
import sys
import argparse
from datetime import datetime, timedelta
from pathlib import Path

def analyze_file(filepath, max_age_days=30):
    """Analyze a single memory file."""
    try:
        content = filepath.read_text()
        lines = content.split("\n")
        
        # Count entries
        entry_count = 0
        stale_entries = []
        duplicates = []
        seen_lines = set()
        
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if not stripped or stripped.startswith("#") or stripped.startswith("<!--"):
                continue
            
            entry_count += 1
            
            # Check for duplicates
            if stripped in seen_lines:
                duplicates.append((i, stripped[:60]))
            seen_lines.add(stripped)
            
            # Check for stale markers (dates older than threshold)
            if "updated:" in stripped.lower() or "last:" in stripped.lower():
                # Try to extract date
                for word in stripped.split():
                    if word.count("-") == 2 and len(word) == 10:
                        try:
                            date = datetime.strptime(word, "%Y-%m-%d")
                            age = (datetime.now() - date).days
                            if age > max_age_days:
                                stale_entries.append((i, stripped[:60], age))
                        except:
                            pass
        
        # Calculate size
        size_kb = len(content) / 1024
        
        return {
            "path": str(filepath),
            "lines": len(lines),
            "entries": entry_count,
            "size_kb": round(size_kb, 2),
            "stale": len(stale_entries),
            "stale_entries": stale_entries[:5],
            "duplicates": len(duplicates),
            "duplicate_samples": duplicates[:3],
            "over_limit": len(lines) > 200
        }
    except Exception as e:
        return {
            "path": str(filepath),
            "error": str(e)
        }

def analyze_memory_path(base_path):
    """Analyze all memory files under a path."""
    results = {
        "hot": [],
        "warm": [],
        "cold": [],
        "total_size_kb": 0,
        "total_files": 0,
        "total_entries": 0,
        "total_stale": 0,
        "total_duplicates": 0
    }
    
    # HOT tier
    hot_files = [
        Path(base_path) / "memory.md",
        Path(base_path) / "self-improving" / "memory.md",
        Path(base_path) / "proactivity" / "memory.md",
    ]
    for f in hot_files:
        if f.exists():
            result = analyze_file(f)
            result["tier"] = "HOT"
            results["hot"].append(result)
    
    # WARM tier - domains and projects
    for subdir in ["domains", "projects"]:
        dir_path = Path(base_path) / "self-improving" / subdir
        if dir_path.exists():
            for f in dir_path.glob("*.md"):
                result = analyze_file(f)
                result["tier"] = "WARM"
                results["warm"].append(result)
    
    # WARM - other memory
    memory_dir = Path(base_path) / "memory"
    if memory_dir.exists():
        for f in memory_dir.glob("*.md"):
            if "heartbeat" not in f.name:
                result = analyze_file(f)
                result["tier"] = "WARM"
                results["warm"].append(result)
    
    # COLD tier
    archive_dir = Path(base_path) / "self-improving" / "archive"
    if archive_dir.exists():
        for f in archive_dir.glob("*.md"):
            result = analyze_file(f)
            result["tier"] = "COLD"
            results["cold"].append(result)
    
    # Aggregate stats
    for tier in ["hot", "warm", "cold"]:
        for r in results[tier]:
            if "error" not in r:
                results["total_size_kb"] += r["size_kb"]
                results["total_files"] += 1
                results["total_entries"] += r["entries"]
                results["total_stale"] += r["stale"]
                results["total_duplicates"] += r["duplicates"]
    
    return results

def print_report(results):
    """Print analysis report."""
    print("\n" + "=" * 60)
    print("MEMORY DEFRAGMENTATION ANALYSIS")
    print("=" * 60)
    print(f"\n📊 Overall Statistics")
    print(f"   Files analyzed: {results['total_files']}")
    print(f"   Total entries: {results['total_entries']}")
    print(f"   Total size: {results['total_size_kb']:.2f} KB")
    print(f"   Stale entries: {results['total_stale']}")
    print(f"   Duplicate entries: {results['total_duplicates']}")
    
    for tier, files in [("HOT", results["hot"]), ("WARM", results["warm"]), ("COLD", results["cold"])]:
        if files:
            print(f"\n{tier} Tier ({len(files)} files)")
            print("-" * 40)
            for r in files:
                if "error" in r:
                    print(f"   ❌ {Path(r['path']).name}: {r['error']}")
                else:
                    flags = []
                    if r["stale"] > 0:
                        flags.append(f"{r['stale']} stale")
                    if r["duplicates"] > 0:
                        flags.append(f"{r['duplicates']} dup")
                    if r["over_limit"]:
                        flags.append("OVER LIMIT")
                    flag_str = f" [{', '.join(flags)}]" if flags else ""
                    print(f"   ✅ {Path(r['path']).name}: {r['entries']} entries, {r['lines']} lines{flag_str}")
    
    # Recommendations
    print("\n" + "=" * 60)
    print("RECOMMENDATIONS")
    print("=" * 60)
    
    if results["total_stale"] > 0:
        print(f"\n⚠️  Found {results['total_stale']} stale entries (30+ days old)")
        print("   Run: python3 scripts/defragment.py --plan")
    
    if results["total_duplicates"] > 0:
        print(f"\n⚠️  Found {results['total_duplicates']} duplicate entries")
        print("   Run: python3 scripts/defragment.py --plan")
    
    over_limit = sum(1 for tier in ["hot", "warm", "cold"] for r in results[tier] if r.get("over_limit"))
    if over_limit > 0:
        print(f"\n⚠️  {over_limit} files exceed 200 line limit")
        print("   Consider compacting or archiving content")
    
    if results["total_stale"] == 0 and results["total_duplicates"] == 0 and over_limit == 0:
        print("\n✅ Memory is clean! No defragmentation needed.")
    
    print()

def main():
    parser = argparse.ArgumentParser(description="Analyze memory for defragmentation")
    parser.add_argument("--path", default="~", help="Base path for memory files")
    args = parser.parse_args()
    
    base_path = Path(args.path).expanduser()
    
    print(f"🔍 Analyzing memory files under: {base_path}")
    
    results = analyze_memory_path(base_path)
    print_report(results)
    
    return results

if __name__ == "__main__":
    main()
