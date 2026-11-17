#!/usr/bin/env python3
"""
Migration script to add _field_meta and _review structures to existing cards.

This script backfills confidence metadata for cards that were extracted before
the confidence system was implemented.

Usage:
    python migrate_confidence.py --dry-run  # Preview changes
    python migrate_confidence.py            # Apply changes
    python migrate_confidence.py --backup   # Apply with backup
"""

import os
import sys
import json
import argparse
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# Add project path
sys.path.insert(0, str(Path(__file__).parent))

from runtime_paths import DEFAULT_CARDS_DIR, load_runtime_env

# Import confidence system
try:
    from extract_knowledge_cards import ConfidenceCalculator, generate_review_structure
    HAS_CONFIDENCE = True
except ImportError:
    HAS_CONFIDENCE = False
    print("Error: ConfidenceCalculator not available. Run from professor-wangqi/scripts/")
    sys.exit(1)

load_runtime_env()


def calculate_field_confidence(value, field_name: str) -> Dict:
    """
    Calculate confidence for a field value.
    
    For migrated cards, we use conservative estimates based on value presence.
    """
    calc = ConfidenceCalculator()
    
    # Check if value is present
    has_value = value is not None and value != "" and value != []
    
    if not has_value:
        return {
            "confidence": 0.0,
            "source": "none",
            "level": "none",
            "reasoning": "Field not populated in original extraction"
        }
    
    # For migrated cards, use medium confidence (conservative)
    # They were extracted before the confidence system, so we can't be certain
    confidence = 0.70  # Medium confidence for existing data
    
    # Adjust based on field type
    if field_name in ["doi", "year"]:
        # These are usually accurate if present
        confidence = 0.85
    elif field_name in ["title", "authors"]:
        # Usually good quality
        confidence = 0.80
    elif field_name in ["abstract", "conclusions"]:
        # May be truncated or incomplete
        confidence = 0.70
    elif field_name == "keywords":
        # Often empty or incomplete
        confidence = 0.65 if value else 0.0
    
    # Determine level
    if confidence >= 0.85:
        level = "high"
    elif confidence >= 0.70:
        level = "medium"
    elif confidence >= 0.50:
        level = "low"
    else:
        level = "none"
    
    return {
        "confidence": confidence,
        "source": "migrated",  # Indicates this was backfilled
        "level": level,
        "reasoning": "Confidence estimated during migration from legacy cards"
    }


def migrate_card(card: Dict) -> Dict:
    """
    Add _field_meta and _review to a card if missing.
    
    Returns:
        Migrated card (copy)
    """
    import copy
    migrated = copy.deepcopy(card)
    
    # Skip if already has _field_meta
    if "_field_meta" in migrated and "_review" in migrated:
        return migrated
    
    # Calculate confidence for each field
    field_meta = {}
    
    # Standard fields
    for field in ["title", "authors", "year", "journal", "doi", "keywords", "abstract", "conclusions"]:
        value = card.get(field)
        field_meta[field] = calculate_field_confidence(value, field)
    
    # Add _field_meta
    migrated["_field_meta"] = field_meta
    
    # Generate _review structure
    migrated["_review"] = generate_review_structure(field_meta)
    
    # Mark as migrated
    migrated["_review"]["migrated_at"] = datetime.now().isoformat()
    migrated["_review"]["reviewer_notes"] = "Confidence data backfilled by migration script"
    
    return migrated


def migrate_directory(cards_dir: str, dry_run: bool = False, backup: bool = False) -> Dict:
    """
    Migrate all cards in a directory.
    
    Args:
        cards_dir: Directory containing card subdirectories (papers/, experiences/)
        dry_run: If True, don't write changes
        backup: If True, create backup before modifying
    
    Returns:
        Statistics dict
    """
    stats = {
        "total_cards": 0,
        "migrated_cards": 0,
        "skipped_cards": 0,
        "errors": []
    }
    
    cards_path = Path(cards_dir)
    
    if not cards_path.exists():
        print(f"Error: Cards directory not found: {cards_dir}")
        return stats
    
    # Process subdirectories
    for subdir in ["papers", "experiences"]:
        subdir_path = cards_path / subdir
        if not subdir_path.exists():
            continue
        
        for card_file in subdir_path.glob("*.json"):
            stats["total_cards"] += 1
            
            try:
                # Load card
                with open(card_file, "r", encoding="utf-8") as f:
                    card = json.load(f)
                
                # Check if already has confidence data
                if "_field_meta" in card and "_review" in card:
                    stats["skipped_cards"] += 1
                    continue
                
                # Migrate
                migrated = migrate_card(card)
                
                if dry_run:
                    print(f"[DRY RUN] Would migrate: {card_file.name}")
                    print(f"  _field_meta: {list(migrated['_field_meta'].keys())}")
                    print(f"  _review.status: {migrated['_review']['status']}")
                else:
                    # Backup if requested
                    if backup:
                        backup_path = card_file.with_suffix(".json.bak")
                        shutil.copy2(card_file, backup_path)
                    
                    # Write migrated card
                    with open(card_file, "w", encoding="utf-8") as f:
                        json.dump(migrated, f, ensure_ascii=False, indent=2)
                    
                    print(f"Migrated: {card_file.name}")
                
                stats["migrated_cards"] += 1
                
            except Exception as e:
                error_msg = f"Error processing {card_file}: {e}"
                print(error_msg)
                stats["errors"].append(error_msg)
    
    return stats


def main():
    parser = argparse.ArgumentParser(description="Migrate existing cards to add confidence metadata")
    parser.add_argument("--cards", default=DEFAULT_CARDS_DIR, help="Cards directory")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without writing")
    parser.add_argument("--backup", action="store_true", help="Create backup before modifying")
    
    args = parser.parse_args()
    
    print(f"Migrating cards from: {args.cards}")
    print(f"Dry run: {args.dry_run}")
    print(f"Backup: {args.backup}")
    print()
    
    stats = migrate_directory(args.cards, dry_run=args.dry_run, backup=args.backup)
    
    print()
    print("=" * 60)
    print("MIGRATION SUMMARY")
    print("=" * 60)
    print(f"Total cards: {stats['total_cards']}")
    print(f"Migrated: {stats['migrated_cards']}")
    print(f"Skipped (already has confidence): {stats['skipped_cards']}")
    print(f"Errors: {len(stats['errors'])}")
    
    if stats['errors']:
        print()
        print("Errors:")
        for err in stats['errors']:
            print(f"  - {err}")
    
    if args.dry_run:
        print()
        print("This was a dry run. Run without --dry-run to apply changes.")


if __name__ == "__main__":
    main()
