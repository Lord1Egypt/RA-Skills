"""
Card Merger - Handle manual overrides and merge with auto-extracted values

Features:
1. Load/save manual overrides from data/overrides/
2. Merge auto-extracted values with manual overrides
3. Confidence-based field selection
4. Directory-level merge operations

Override file format (JSON):
{
    "card_id": "WQ-SCI-001",
    "overrides": {
        "title": {"value": "Manual Title", "source": "manual"},
        "authors": {"value": ["Author 1", "Author 2"], "source": "manual"}
    },
    "reviewed_at": "2026-04-25T10:00:00",
    "reviewer_notes": "Fixed author extraction errors"
}

Usage:
    from card_merger import CardMerger
    
    merger = CardMerger(overrides_dir="data/overrides/")
    
    # Load a card with overrides applied
    merged_card = merger.merge_card(auto_card)
    
    # Save an override
    merger.save_override("WQ-SCI-001", {"title": "Corrected Title"})
"""

import os
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field


@dataclass
class FieldOverride:
    """Represents a manual override for a single field."""
    value: Any
    source: str = "manual"
    overridden_at: str = field(default_factory=lambda: datetime.now().isoformat())
    notes: str = ""


class CardMerger:
    """
    Merge auto-extracted card values with manual overrides.
    
    Design decisions:
    - Override location: data/overrides/
    - Manual overrides always take precedence (confidence = 1.0)
    - Merged values don't include confidence metadata in index
    """
    
    # Fields that support overrides
    OVERRIDABLE_FIELDS = [
        "title", "authors", "year", "journal", "doi", "keywords",
        "abstract", "conclusions", "related_constitutions", "related_diseases"
    ]
    
    # Fields that are lists
    LIST_FIELDS = ["authors", "keywords", "related_constitutions", "related_diseases"]
    
    def __init__(self, overrides_dir: str = None, cards_dir: str = None):
        """
        Initialize the merger.
        
        Args:
            overrides_dir: Directory for override files (default: data/overrides/)
            cards_dir: Directory for auto-extracted cards (default: data/cards/)
        """
        self.overrides_dir = Path(overrides_dir) if overrides_dir else Path("data/overrides")
        self.cards_dir = Path(cards_dir) if cards_dir else Path("data/cards")
        
        # Ensure directories exist
        self.overrides_dir.mkdir(parents=True, exist_ok=True)
    
    def load_override(self, card_id: str) -> Optional[Dict]:
        """
        Load override file for a card.
        
        Args:
            card_id: Card ID (e.g., "WQ-SCI-001")
        
        Returns:
            Override dict or None if not found
        """
        override_path = self.overrides_dir / f"{card_id}.json"
        
        if not override_path.exists():
            return None
        
        try:
            with open(override_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Failed to load override for {card_id}: {e}")
            return None
    
    def save_override(self, card_id: str, overrides: Dict[str, Any], notes: str = "") -> bool:
        """
        Save manual overrides for a card.
        
        Args:
            card_id: Card ID
            overrides: Dict of field -> value
            notes: Reviewer notes
        
        Returns:
            True if saved successfully
        """
        override_path = self.overrides_dir / f"{card_id}.json"
        
        # Load existing override or create new
        existing = self.load_override(card_id) or {
            "card_id": card_id,
            "overrides": {},
            "history": []
        }
        
        # Update overrides
        for field_name, value in overrides.items():
            if field_name not in self.OVERRIDABLE_FIELDS:
                print(f"Warning: Field '{field_name}' is not overridable, skipping")
                continue
            
            # Store old value in history if exists
            if field_name in existing["overrides"]:
                existing["history"].append({
                    "field": field_name,
                    "old_value": existing["overrides"][field_name]["value"],
                    "new_value": value,
                    "changed_at": datetime.now().isoformat()
                })
            
            existing["overrides"][field_name] = {
                "value": value,
                "source": "manual",
                "overridden_at": datetime.now().isoformat(),
                "notes": notes
            }
        
        existing["reviewed_at"] = datetime.now().isoformat()
        if notes:
            existing["reviewer_notes"] = notes
        
        try:
            with open(override_path, "w", encoding="utf-8") as f:
                json.dump(existing, f, ensure_ascii=False, indent=2)
            print(f"Saved override for {card_id}")
            return True
        except Exception as e:
            print(f"Error saving override for {card_id}: {e}")
            return False
    
    def delete_override(self, card_id: str, field_name: str = None) -> bool:
        """
        Delete override for a card or specific field.
        
        Args:
            card_id: Card ID
            field_name: Specific field to delete, or None to delete all
        
        Returns:
            True if deleted successfully
        """
        override_path = self.overrides_dir / f"{card_id}.json"
        
        if not override_path.exists():
            return False
        
        if field_name is None:
            # Delete entire override file
            try:
                override_path.unlink()
                print(f"Deleted override file for {card_id}")
                return True
            except Exception as e:
                print(f"Error deleting override file: {e}")
                return False
        
        # Delete specific field
        override = self.load_override(card_id)
        if not override:
            return False
        
        if field_name in override.get("overrides", {}):
            del override["overrides"][field_name]
            
            if not override["overrides"]:
                # No more overrides, delete file
                override_path.unlink()
                print(f"Deleted override file for {card_id} (no overrides remaining)")
            else:
                # Save updated override
                with open(override_path, "w", encoding="utf-8") as f:
                    json.dump(override, f, ensure_ascii=False, indent=2)
                print(f"Deleted override for {card_id}.{field_name}")
            return True
        
        return False
    
    def merge_card(self, auto_card: Dict, override: Dict = None) -> Dict:
        """
        Merge auto-extracted card with manual overrides.
        
        Args:
            auto_card: Auto-extracted card
            override: Override dict (loaded from file), or None to auto-load
        
        Returns:
            Merged card (deep copy, original not modified)
        """
        import copy
        from datetime import datetime
        
        card_id = auto_card.get("card_id", "unknown")
        
        # Load override if not provided
        if override is None:
            override = self.load_override(card_id)
        
        # Create a DEEP copy of the auto card (to avoid modifying nested structures)
        merged = copy.deepcopy(auto_card)
        
        # Track merge info
        merge_info = {
            "has_override": override is not None,
            "overridden_fields": []
        }
        
        if override and "overrides" in override:
            overridden_fields = []
            
            for field_name, field_override in override["overrides"].items():
                if field_name in self.OVERRIDABLE_FIELDS:
                    # Update top-level field value
                    merged[field_name] = field_override["value"]
                    merge_info["overridden_fields"].append(field_name)
                    overridden_fields.append(field_name)
                    
                    # Update _field_meta for this field
                    if "_field_meta" in merged and field_name in merged["_field_meta"]:
                        merged["_field_meta"][field_name]["confidence"] = 1.0
                        merged["_field_meta"][field_name]["source"] = "manual"
                        merged["_field_meta"][field_name]["level"] = "high"  # Use "high" for consistency
                        merged["_field_meta"][field_name]["reasoning"] = "Manually corrected"
                    
                    # Also support legacy _confidence field
                    if "_confidence" in merged and field_name in merged["_confidence"]:
                        merged["_confidence"][field_name]["confidence"] = 1.0
                        merged["_confidence"][field_name]["source"] = "manual"
            
            # Update _review structure if overrides were applied
            if overridden_fields:
                if "_review" not in merged:
                    merged["_review"] = {}
                
                merged["_review"]["status"] = "manually_fixed"
                merged["_review"]["manual_reviewed_at"] = override.get("reviewed_at", datetime.now().isoformat())
                merged["_review"]["reviewer_notes"] = override.get("reviewer_notes", "")
                
                # Add overridden fields to the fields list if not already present
                existing_fields = set(merged["_review"].get("fields", []))
                merged["_review"]["fields"] = list(existing_fields.union(set(overridden_fields)))
                
                # Ensure priority is set (inherit from existing or default to P1)
                if "priority" not in merged["_review"]:
                    merged["_review"]["priority"] = 1  # P1: high priority for manual review
        
        # Store merge info (for debugging, not for index)
        merged["_merge_info"] = merge_info
        
        return merged
    
    def merge_directory(self, cards_subdir: str = None) -> Tuple[List[Dict], Dict]:
        """
        Merge all cards in a directory with their overrides.
        
        Args:
            cards_subdir: Subdirectory under cards/ (e.g., "papers", "experiences")
                         If None, processes all subdirectories
        
        Returns:
            Tuple of (merged_cards, stats)
        """
        merged_cards = []
        stats = {
            "total_cards": 0,
            "cards_with_overrides": 0,
            "total_overrides": 0,
            "fields_overridden": {}
        }
        
        if cards_subdir:
            subdirs = [self.cards_dir / cards_subdir]
        else:
            subdirs = [d for d in self.cards_dir.iterdir() if d.is_dir()]
        
        for subdir in subdirs:
            if not subdir.exists():
                continue
            
            for card_file in subdir.glob("*.json"):
                try:
                    with open(card_file, "r", encoding="utf-8") as f:
                        auto_card = json.load(f)
                    
                    card_id = auto_card.get("card_id", card_file.stem)
                    override = self.load_override(card_id)
                    
                    merged = self.merge_card(auto_card, override)
                    merged_cards.append(merged)
                    
                    stats["total_cards"] += 1
                    
                    if override:
                        stats["cards_with_overrides"] += 1
                        override_count = len(override.get("overrides", {}))
                        stats["total_overrides"] += override_count
                        
                        for field_name in override.get("overrides", {}).keys():
                            stats["fields_overridden"][field_name] = \
                                stats["fields_overridden"].get(field_name, 0) + 1
                
                except Exception as e:
                    print(f"Warning: Failed to process {card_file}: {e}")
        
        return merged_cards, stats
    
    def get_merge_info(self, card_id: str) -> Dict:
        """
        Get merge info for a card (for statistics).
        
        Returns:
            {"has_override": bool, "overridden_fields": list}
        """
        override = self.load_override(card_id)
        if not override:
            return {"has_override": False, "overridden_fields": []}
        
        return {
            "has_override": True,
            "overridden_fields": list(override.get("overrides", {}).keys())
        }
    
    def get_override_status(self, card_id: str) -> Dict:
        """
        Get the override status for a card.
        
        Returns:
            {
                "has_override": bool,
                "overridden_fields": list,
                "reviewed_at": str or None,
                "reviewer_notes": str or None
            }
        """
        override = self.load_override(card_id)
        
        if not override:
            return {
                "has_override": False,
                "fields": [],  # Changed from overridden_fields for consistency
                "overridden_fields": [],  # Keep for backward compatibility
                "reviewed_at": None,
                "reviewer_notes": None
            }
        
        fields_list = list(override.get("overrides", {}).keys())
        return {
            "has_override": True,
            "fields": fields_list,  # Primary key for consumers
            "overridden_fields": fields_list,  # Keep for backward compatibility
            "reviewed_at": override.get("reviewed_at"),
            "reviewer_notes": override.get("reviewer_notes")
        }
    
    def list_overrides(self) -> List[Dict]:
        """
        List all override files with their status.
        
        Returns:
            List of {"card_id": str, "fields": list, "reviewed_at": str}
        """
        overrides = []
        
        for override_file in self.overrides_dir.glob("*.json"):
            try:
                with open(override_file, "r", encoding="utf-8") as f:
                    override = json.load(f)
                
                overrides.append({
                    "card_id": override.get("card_id", override_file.stem),
                    "fields": list(override.get("overrides", {}).keys()),
                    "reviewed_at": override.get("reviewed_at"),
                    "reviewer_notes": override.get("reviewer_notes", "")
                })
            except Exception as e:
                print(f"Warning: Failed to read {override_file}: {e}")
        
        return overrides


def load_cards_with_overrides(cards_dir: str, overrides_dir: str = None) -> List[Dict]:
    """
    Convenience function to load all cards with overrides applied.
    
    Args:
        cards_dir: Directory containing auto-extracted cards
        overrides_dir: Directory containing override files
    
    Returns:
        List of merged cards
    """
    merger = CardMerger(overrides_dir=overrides_dir, cards_dir=cards_dir)
    merged_cards, _ = merger.merge_directory()
    return merged_cards


if __name__ == "__main__":
    import argparse
    from runtime_paths import DEFAULT_CARDS_DIR, DEFAULT_OVERRIDES_DIR
    
    parser = argparse.ArgumentParser(description="Card merger for manual overrides")
    parser.add_argument("--cards", default=DEFAULT_CARDS_DIR, help="Cards directory")
    parser.add_argument("--overrides", default=DEFAULT_OVERRIDES_DIR, help="Overrides directory")
    parser.add_argument("--list", action="store_true", help="List all overrides")
    parser.add_argument("--stats", action="store_true", help="Show merge statistics")
    
    args = parser.parse_args()
    
    merger = CardMerger(overrides_dir=args.overrides, cards_dir=args.cards)
    
    if args.list:
        overrides = merger.list_overrides()
        print(f"\nFound {len(overrides)} override files:\n")
        for o in overrides:
            print(f"  {o['card_id']}: {', '.join(o['fields'])} (reviewed: {o['reviewed_at'] or 'N/A'})")
    
    if args.stats:
        cards, stats = merger.merge_directory()
        print(f"\nMerge Statistics:")
        print(f"  Total cards: {stats['total_cards']}")
        print(f"  Cards with overrides: {stats['cards_with_overrides']}")
        print(f"  Total override fields: {stats['total_overrides']}")
        print(f"  Fields overridden:")
        for field, count in stats['fields_overridden'].items():
            print(f"    {field}: {count}")
