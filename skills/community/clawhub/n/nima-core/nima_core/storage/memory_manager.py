#!/usr/bin/env python3
"""
Memory Manager
==============
Auto-prune old data, enforce memory limits, archive old memories.

Features:
- Configurable memory limits
- Auto-archive old checkpoints
- Prune low-importance memories
- Storage statistics

Author: Lilu
Date: Feb 3, 2026
"""

import os
import json
import logging
import shutil
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict
from dataclasses import dataclass

logger = logging.getLogger(__name__)

from nima_core.config import OPENCLAW_WORKSPACE
WORKSPACE_DIR = OPENCLAW_WORKSPACE
NIMA_CORE_DIR = WORKSPACE_DIR / "nima-core"
MEMORY_DIR = NIMA_CORE_DIR / "storage" / "data"
ARCHIVE_DIR = MEMORY_DIR / "archive"


@dataclass
class MemoryLimits:
    """Configuration for memory limits."""
    # Checkpoint limits
    max_checkpoints: int = 20  # Keep last N checkpoints
    checkpoint_age_days: int = 30  # Archive checkpoints older than this
    
    # Experience limits
    max_experiences: int = 1000  # Max in experience stream
    experience_age_days: int = 7  # Archive experiences older than this
    
    # Pattern/insight limits
    max_patterns: int = 100
    max_insights: int = 200
    
    # Storage limits
    max_storage_mb: int = 100  # Max total storage
    
    # Dream log limits
    max_dream_sessions: int = 50


class MemoryManager:
    """
    Manage memory storage limits and archival.
    
    Usage:
        manager = MemoryManager()
        manager.analyze()  # Get storage stats
        manager.prune()    # Auto-prune based on limits
        manager.archive()  # Archive old data
    """
    
    def __init__(self, limits: MemoryLimits = None):
        """Initialize memory manager."""
        self.limits = limits or MemoryLimits()
        
        # Ensure archive directory exists
        ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    
    def analyze(self) -> Dict:
        """
        Analyze current memory storage.
        
        Returns:
            Storage statistics
        """
        stats = {
            "timestamp": datetime.now().isoformat(),
            "total_size_mb": 0,
            "checkpoints": {},
            "experiences": {},
            "dreams": {},
            "patterns": {},
            "relationships": {},
            "warnings": [],
        }
        
        # Checkpoint analysis
        sessions_dir = MEMORY_DIR / "persistence" / "sessions"
        if sessions_dir.exists():
            checkpoints = list(sessions_dir.glob("*.pt"))
            total_size = sum(f.stat().st_size for f in checkpoints)
            
            stats["checkpoints"] = {
                "count": len(checkpoints),
                "size_mb": total_size / (1024 * 1024),
                "limit": self.limits.max_checkpoints,
                "over_limit": len(checkpoints) > self.limits.max_checkpoints,
            }
            stats["total_size_mb"] += stats["checkpoints"]["size_mb"]
            
            if stats["checkpoints"]["over_limit"]:
                stats["warnings"].append(
                    f"Checkpoints ({len(checkpoints)}) exceed limit ({self.limits.max_checkpoints})"
                )
        
        # Experience stream analysis
        exp_file = MEMORY_DIR / "stories" / "experience_stream.json"
        if exp_file.exists():
            try:
                with open(exp_file) as f:
                    experiences = json.load(f)
                
                stats["experiences"] = {
                    "count": len(experiences),
                    "size_mb": exp_file.stat().st_size / (1024 * 1024),
                    "limit": self.limits.max_experiences,
                    "over_limit": len(experiences) > self.limits.max_experiences,
                }
                stats["total_size_mb"] += stats["experiences"]["size_mb"]
                
                if stats["experiences"]["over_limit"]:
                    stats["warnings"].append(
                        f"Experiences ({len(experiences)}) exceed limit ({self.limits.max_experiences})"
                    )
            except (json.JSONDecodeError, FileNotFoundError, KeyError) as exc:
                logger.warning("MemoryManager.analyze error: %s", exc)
        
        # Dreams analysis
        dreams_dir = MEMORY_DIR / "dreams"
        if dreams_dir.exists():
            dream_files = list(dreams_dir.glob("*.json"))
            total_size = sum(f.stat().st_size for f in dream_files)
            
            stats["dreams"] = {
                "files": len(dream_files),
                "size_mb": total_size / (1024 * 1024),
            }
            stats["total_size_mb"] += stats["dreams"]["size_mb"]
        
        # Relationships analysis
        rel_file = MEMORY_DIR / "relationships.json"
        if rel_file.exists():
            stats["relationships"] = {
                "size_mb": rel_file.stat().st_size / (1024 * 1024),
            }
            stats["total_size_mb"] += stats["relationships"]["size_mb"]
        
        # Check total storage limit
        if stats["total_size_mb"] > self.limits.max_storage_mb:
            stats["warnings"].append(
                f"Total storage ({stats['total_size_mb']:.2f} MB) exceeds limit ({self.limits.max_storage_mb} MB)"
            )
        
        return stats
    
    def prune_checkpoints(self, dry_run: bool = False) -> Dict:
        """
        Prune old checkpoints.
        
        Args:
            dry_run: If True, only report what would be pruned
            
        Returns:
            Pruning results
        """
        sessions_dir = MEMORY_DIR / "persistence" / "sessions"
        if not sessions_dir.exists():
            return {"pruned": 0, "archived": 0}
        
        checkpoints = sorted(sessions_dir.glob("*.pt"), key=lambda f: f.stat().st_mtime)
        
        # Keep latest.pt always
        checkpoints = [c for c in checkpoints if c.name != "latest.pt"]
        
        to_prune = []
        to_archive = []
        
        # Check age
        cutoff = datetime.now() - timedelta(days=self.limits.checkpoint_age_days)
        for cp in checkpoints:
            mtime = datetime.fromtimestamp(cp.stat().st_mtime)
            if mtime < cutoff:
                to_archive.append(cp)
        
        # Check count (keep most recent)
        remaining = [c for c in checkpoints if c not in to_archive]
        if len(remaining) > self.limits.max_checkpoints:
            excess = len(remaining) - self.limits.max_checkpoints
            to_prune = remaining[:excess]  # Oldest first
        
        result = {
            "to_archive": [str(p) for p in to_archive],
            "to_prune": [str(p) for p in to_prune],
            "dry_run": dry_run,
        }
        
        if not dry_run:
            # Archive old checkpoints
            for cp in to_archive:
                archive_path = ARCHIVE_DIR / "checkpoints"
                archive_path.mkdir(parents=True, exist_ok=True)
                shutil.move(str(cp), str(archive_path / cp.name))
            
            # Delete excess checkpoints
            for cp in to_prune:
                cp.unlink()
            
            result["archived"] = len(to_archive)
            result["pruned"] = len(to_prune)
        
        return result
    
    def prune_experiences(self, dry_run: bool = False) -> Dict:
        """
        Prune old experiences from stream.
        
        Args:
            dry_run: If True, only report
            
        Returns:
            Pruning results
        """
        exp_file = MEMORY_DIR / "stories" / "experience_stream.json"
        if not exp_file.exists():
            return {"pruned": 0}
        
        try:
            with open(exp_file) as f:
                experiences = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            return {"error": f"Failed to load experiences: {e}"}
        
        original_count = len(experiences)
        
        # Prune by age
        cutoff = datetime.now() - timedelta(days=self.limits.experience_age_days)
        cutoff_iso = cutoff.isoformat()
        
        # Keep recent experiences
        recent = [e for e in experiences if e.get("timestamp", "") > cutoff_iso]
        recent_ids = {id(e) for e in recent}  # O(1) lookup set
        
        # Also keep important ones regardless of age
        important = [e for e in experiences 
                    if e.get("importance", 0) > 0.8 and id(e) not in recent_ids]
        
        # Combine and limit
        kept = recent + important
        if len(kept) > self.limits.max_experiences:
            # Sort by importance, keep top N
            kept = sorted(kept, key=lambda e: e.get("importance", 0), reverse=True)
            kept = kept[:self.limits.max_experiences]
        
        result = {
            "original": original_count,
            "kept": len(kept),
            "pruned": original_count - len(kept),
            "dry_run": dry_run,
        }
        
        if not dry_run and len(kept) < original_count:
            # Archive old experiences
            archive_path = ARCHIVE_DIR / "experiences"
            archive_path.mkdir(parents=True, exist_ok=True)
            
            archived = [e for e in experiences if e not in kept]
            archive_file = archive_path / f"experiences_{datetime.now().strftime('%Y%m%d')}.json"
            
            with open(archive_file, 'w') as f:
                json.dump(archived, f)
            
            # Save pruned stream
            with open(exp_file, 'w') as f:
                json.dump(kept, f, indent=2)
            
            result["archived_to"] = str(archive_file)
        
        return result
    
    def prune(self, dry_run: bool = False) -> Dict:
        """
        Run all pruning operations.
        
        Args:
            dry_run: If True, only report
            
        Returns:
            Combined results
        """
        results = {
            "timestamp": datetime.now().isoformat(),
            "dry_run": dry_run,
            "checkpoints": self.prune_checkpoints(dry_run),
            "experiences": self.prune_experiences(dry_run),
        }
        
        return results
    
    def get_archive_stats(self) -> Dict:
        """Get archive statistics."""
        if not ARCHIVE_DIR.exists():
            return {"exists": False}
        
        stats = {
            "exists": True,
            "total_size_mb": 0,
            "contents": {},
        }
        
        for subdir in ARCHIVE_DIR.iterdir():
            if subdir.is_dir():
                files = list(subdir.glob("*"))
                size = sum(f.stat().st_size for f in files if f.is_file())
                stats["contents"][subdir.name] = {
                    "files": len(files),
                    "size_mb": size / (1024 * 1024),
                }
                stats["total_size_mb"] += size / (1024 * 1024)
        
        return stats


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="NIMA Core Memory Manager")
    parser.add_argument("action", choices=["analyze", "prune", "archive-stats"],
                        help="Action to perform")
    parser.add_argument("--dry-run", action="store_true", help="Don't actually prune")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    args = parser.parse_args()
    
    manager = MemoryManager()
    
    if args.action == "analyze":
        result = manager.analyze()
        
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print("📊 MEMORY ANALYSIS")
            print("=" * 50)
            print(f"Total Storage: {result['total_size_mb']:.2f} MB")
            print(f"\nCheckpoints: {result.get('checkpoints', {}).get('count', '?')}")
            print(f"Experiences: {result.get('experiences', {}).get('count', '?')}")
            
            if result["warnings"]:
                print("\n⚠️  Warnings:")
                for w in result["warnings"]:
                    print(f"   • {w}")
    
    elif args.action == "prune":
        result = manager.prune(dry_run=args.dry_run)
        
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print("🧹 MEMORY PRUNING" + (" (DRY RUN)" if args.dry_run else ""))
            print("=" * 50)
            
            cp = result["checkpoints"]
            print(f"Checkpoints: archived={cp.get('archived', len(cp.get('to_archive', [])))}, "
                  f"pruned={cp.get('pruned', len(cp.get('to_prune', [])))}")
            
            exp = result["experiences"]
            print(f"Experiences: {exp.get('original', '?')} → {exp.get('kept', '?')} "
                  f"(pruned {exp.get('pruned', '?')})")
    
    elif args.action == "archive-stats":
        result = manager.get_archive_stats()
        
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print("📦 ARCHIVE STATISTICS")
            print("=" * 50)
            print(f"Total Size: {result.get('total_size_mb', 0):.2f} MB")
            for name, info in result.get("contents", {}).items():
                print(f"  {name}: {info['files']} files, {info['size_mb']:.2f} MB")


if __name__ == "__main__":
    main()