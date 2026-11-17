"""
Show Card - Display detailed card information with auto/override/merged values

This is a simplified CLI-focused script for showing card details.
For full review functionality, use review_cards.py.

Usage:
    python show_card.py WQ-SCI-001
    python show_card.py WQ-SCI-001 --json
    python show_card.py WQ-SCI-001 --edit  # Interactive override editing
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# Try to import card_merger
try:
    from card_merger import CardMerger
    HAS_MERGER = True
except ImportError:
    HAS_MERGER = False


# Fields to display
DISPLAY_FIELDS = [
    ("card_id", "Card ID"),
    ("source_type", "Source Type"),
    ("source_file", "Source File"),
    ("title", "Title"),
    ("authors", "Authors"),
    ("year", "Year"),
    ("journal", "Journal"),
    ("doi", "DOI"),
    ("keywords", "Keywords"),
    ("language", "Language"),
    ("abstract", "Abstract"),
    ("conclusions", "Conclusions"),
    ("related_constitutions", "Related Constitutions"),
    ("related_diseases", "Related Diseases"),
    ("knowledge_points", "Knowledge Points"),
    ("created_at", "Created"),
]

# Confidence fields
CONFIDENCE_FIELDS = ["title", "authors", "year", "journal", "doi", "keywords", "abstract", "conclusions"]


def find_card(card_id: str, cards_dir: str) -> Optional[Dict]:
    """Find a card by ID in the cards directory."""
    cards_path = Path(cards_dir)
    
    for card_file in cards_path.rglob("*.json"):
        try:
            with open(card_file, "r", encoding="utf-8") as f:
                card = json.load(f)
                if card.get("card_id") == card_id:
                    card["_source_path"] = str(card_file)
                    return card
        except Exception:
            continue
    
    return None


def format_value(value: Any, max_length: int = 100) -> str:
    """Format a value for display."""
    if value is None:
        return "(not set)"
    
    if isinstance(value, list):
        if len(value) == 0:
            return "(empty list)"
        elif len(value) <= 5:
            return ", ".join(str(v) for v in value)
        else:
            return f"{len(value)} items: " + ", ".join(str(v) for v in value[:5]) + "..."
    
    if isinstance(value, dict):
        result = json.dumps(value, ensure_ascii=False, indent=2)
        return (result[:max_length] + "...") if len(result) > max_length else result
    
    if isinstance(value, str):
        if len(value) == 0:
            return "(empty string)"
        elif len(value) <= max_length:
            return value
        else:
            return value[:max_length] + "..."
    
    return str(value)


def get_confidence_indicator(confidence: float) -> str:
    """Get a visual indicator for confidence level."""
    if confidence >= 0.75:
        return "[HIGH]"
    elif confidence >= 0.50:
        return "[MED]"
    elif confidence > 0:
        return "[LOW]"
    return "[NONE]"


def show_card(card_id: str, cards_dir: str, overrides_dir: str = None, 
              show_json: bool = False, show_candidates: bool = False) -> int:
    """
    Display card information.
    
    Returns:
        0 on success, 1 if not found
    """
    # Find the card
    card = find_card(card_id, cards_dir)
    
    if not card:
        print(f"Error: Card '{card_id}' not found in {cards_dir}")
        return 1
    
    # Get override info
    override = None
    merged_card = card
    if HAS_MERGER and overrides_dir:
        merger = CardMerger(overrides_dir=overrides_dir, cards_dir=cards_dir)
        override = merger.load_override(card_id)
        merged_card = merger.merge_card(card, override)
    
    # JSON output
    if show_json:
        output = {
            "auto": card,
            "merged": merged_card,
            "override": override
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return 0
    
    # Formatted output
    print("\n" + "=" * 80)
    print(f"  CARD: {card_id}")
    print("=" * 80)
    
    confidence_data = card.get("_field_meta", card.get("_confidence", {}))
    override_fields = set(override.get("overrides", {}).keys()) if override else set()
    
    # Display each field
    for field_key, field_label in DISPLAY_FIELDS:
        auto_value = card.get(field_key)
        merged_value = merged_card.get(field_key)
        
        # Skip internal fields
        if field_key.startswith("_"):
            continue
        
        # Check if overridden
        is_overridden = field_key in override_fields
        
        # Get confidence info
        field_conf = confidence_data.get(field_key, {})
        confidence = field_conf.get("confidence", 0.0)
        source = field_conf.get("source", "auto")
        
        # Print field header
        header = f"\n{field_label}"
        if is_overridden:
            header += " [OVERRIDE]"
        if field_key in CONFIDENCE_FIELDS:
            header += f" ({get_confidence_indicator(confidence)}, {source})"
        print(header)
        print("-" * len(header.strip()))
        
        # Print values
        if is_overridden:
            print(f"  Auto:    {format_value(auto_value)}")
            print(f"  Manual:  {format_value(merged_value)}")
        else:
            print(f"  {format_value(merged_value)}")
        
        # Show candidates if requested
        if show_candidates and field_key in CONFIDENCE_FIELDS:
            candidates = field_conf.get("candidates", [])
            if candidates:
                print("  Candidates:")
                for i, cand in enumerate(candidates, 1):
                    cand_val = format_value(cand.get("value"), max_length=60)
                    cand_conf = cand.get("confidence", 0.0)
                    print(f"    {i}. {cand_val} (conf: {cand_conf:.2f})")
    
    # Show override info
    if override:
        print("\n" + "-" * 80)
        print("OVERRIDE INFORMATION")
        print("-" * 80)
        print(f"  Reviewed at: {override.get('reviewed_at', 'N/A')}")
        if override.get("reviewer_notes"):
            print(f"  Notes: {override['reviewer_notes']}")
        if override.get("history"):
            print("  History:")
            for h in override["history"][-5:]:  # Last 5 changes
                print(f"    - {h['field']}: changed at {h['changed_at']}")
    
    # Show knowledge points summary
    kp_count = len(card.get("knowledge_points", []))
    if kp_count > 0:
        print(f"\nKnowledge Points: {kp_count}")
        for i, kp in enumerate(card.get("knowledge_points", [])[:3], 1):
            content = kp.get("content", "")[:80]
            print(f"  {i}. [{kp.get('category', '?')}] {content}...")
    
    print("\n" + "=" * 80)
    
    return 0


def edit_override_interactive(card_id: str, cards_dir: str, overrides_dir: str) -> int:
    """
    Interactive override editing.
    
    Returns:
        0 on success, 1 on error
    """
    if not HAS_MERGER:
        print("Error: card_merger module required for editing")
        return 1
    
    # Find the card
    card = find_card(card_id, cards_dir)
    if not card:
        print(f"Error: Card '{card_id}' not found")
        return 1
    
    print(f"\nEditing overrides for {card_id}")
    print("Current values:")
    print("-" * 40)
    
    for field in ["title", "authors", "year", "journal", "doi"]:
        value = card.get(field)
        print(f"  {field}: {format_value(value, max_length=60)}")
    
    print("\nEnter new values (leave blank to keep current, 'delete' to remove override):")
    print("-" * 40)
    
    overrides = {}
    
    for field in ["title", "authors", "year", "journal", "doi"]:
        current = card.get(field)
        if isinstance(current, list):
            current_str = ", ".join(str(v) for v in current)
        else:
            current_str = str(current) if current else ""
        
        try:
            new_value = input(f"  {field} [{current_str[:50]}]: ").strip()
            
            if new_value.lower() == "delete":
                overrides[field] = None  # Mark for deletion
            elif new_value:
                # Parse value
                if field == "authors":
                    overrides[field] = [a.strip() for a in new_value.split(",")]
                elif field == "year":
                    overrides[field] = int(new_value)
                else:
                    overrides[field] = new_value
        except KeyboardInterrupt:
            print("\nCancelled")
            return 1
        except ValueError as e:
            print(f"  Invalid value for {field}: {e}")
    
    if not overrides:
        print("No changes made")
        return 0
    
    # Get notes
    notes = input("\nReviewer notes (optional): ").strip()
    
    # Save overrides
    merger = CardMerger(overrides_dir=overrides_dir, cards_dir=cards_dir)
    
    # Filter out deletions (handle separately)
    deletions = {k: v for k, v in overrides.items() if v is None}
    updates = {k: v for k, v in overrides.items() if v is not None}
    
    if updates:
        merger.save_override(card_id, updates, notes)
    
    for field in deletions:
        merger.delete_override(card_id, field)
    
    print(f"\nSaved overrides for {card_id}")
    return 0


def main():
    from runtime_paths import DEFAULT_CARDS_DIR, DEFAULT_OVERRIDES_DIR
    
    parser = argparse.ArgumentParser(description="Show knowledge card details")
    parser.add_argument("card_id", help="Card ID to show (e.g., WQ-SCI-001)")
    parser.add_argument("--cards", default=DEFAULT_CARDS_DIR, help="Cards directory")
    parser.add_argument("--overrides", default=DEFAULT_OVERRIDES_DIR, help="Overrides directory")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--candidates", action="store_true", help="Show candidate values")
    parser.add_argument("--edit", action="store_true", help="Interactive override editing")
    
    args = parser.parse_args()
    
    if args.edit:
        return edit_override_interactive(args.card_id, args.cards, args.overrides)
    else:
        return show_card(
            args.card_id, 
            args.cards, 
            args.overrides,
            show_json=args.json,
            show_candidates=args.candidates
        )


if __name__ == "__main__":
    exit_code = main()
    exit(exit_code or 0)
