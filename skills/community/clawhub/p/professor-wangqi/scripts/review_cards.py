"""
Review Cards - Statistics and review workflow for knowledge cards

Features:
1. Calculate confidence statistics across all cards
2. List cards that need review (low confidence fields)
3. Show detailed card information for review
4. Batch review operations

Usage:
    python review_cards.py --stats
    python review_cards.py --needs-review --threshold 0.5
    python review_cards.py --show WQ-SCI-001
    python review_cards.py --list-overrides
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from collections import defaultdict

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# Try to import card_merger for override info
try:
    from card_merger import CardMerger
    HAS_MERGER = True
except ImportError:
    HAS_MERGER = False


# Confidence thresholds
NEEDS_REVIEW_THRESHOLD = 0.50  # Fields below this need review
HIGH_CONFIDENCE_THRESHOLD = 0.75  # Fields above this are high confidence

# Fields to check for confidence
CONFIDENCE_FIELDS = [
    "title", "authors", "year", "journal", "doi", "keywords",
    "abstract", "conclusions"
]


def load_cards(cards_dir: str) -> List[Dict]:
    """Load all cards from directory."""
    cards = []
    cards_path = Path(cards_dir)
    
    for card_file in cards_path.rglob("*.json"):
        try:
            with open(card_file, "r", encoding="utf-8") as f:
                card = json.load(f)
                card["_source_path"] = str(card_file)
                cards.append(card)
        except Exception as e:
            print(f"Warning: Failed to load {card_file}: {e}")
    
    return cards


def calculate_statistics(cards: List[Dict]) -> Dict:
    """
    Calculate confidence statistics across all cards.
    
    Returns:
        {
            "total_cards": int,
            "by_field": {field: {"avg_confidence": float, "low_count": int, "high_count": int}},
            "needs_review_count": int,
            "reviewed_count": int
        }
    """
    stats = {
        "total_cards": len(cards),
        "by_field": {},
        "needs_review_count": 0,
        "reviewed_count": 0,
        "by_source_type": defaultdict(int)
    }
    
    # Initialize field stats
    for field in CONFIDENCE_FIELDS:
        stats["by_field"][field] = {
            "count": 0,
            "total_confidence": 0.0,
            "low_count": 0,
            "medium_count": 0,
            "high_count": 0,
            "missing_count": 0,
            "sources": defaultdict(int)
        }
    
    for card in cards:
        # Track source type
        source_type = card.get("source_type", "unknown")
        stats["by_source_type"][source_type] += 1
        
        # Check if card has override
        merge_info = card.get("_merge_info", {})
        if merge_info.get("has_override"):
            stats["reviewed_count"] += 1
        
        # Check confidence data (support both _field_meta and legacy _confidence)
        confidence_data = card.get("_field_meta", card.get("_confidence", {}))
        
        card_needs_review = False
        
        for field in CONFIDENCE_FIELDS:
            field_conf = confidence_data.get(field, {})
            confidence = field_conf.get("confidence", 0.0)
            source = field_conf.get("source", "none")
            # Value is in the top-level card field, not in _field_meta
            value = card.get(field)
            
            field_stats = stats["by_field"][field]
            field_stats["count"] += 1
            field_stats["sources"][source] += 1
            
            # Check if field is missing
            if value is None or value == "" or value == []:
                field_stats["missing_count"] += 1
                card_needs_review = True
                continue
            
            field_stats["total_confidence"] += confidence
            
            # Categorize confidence
            if confidence >= HIGH_CONFIDENCE_THRESHOLD:
                field_stats["high_count"] += 1
            elif confidence >= NEEDS_REVIEW_THRESHOLD:
                field_stats["medium_count"] += 1
            else:
                field_stats["low_count"] += 1
                card_needs_review = True
        
        if card_needs_review:
            stats["needs_review_count"] += 1
    
    # Calculate averages
    for field in CONFIDENCE_FIELDS:
        field_stats = stats["by_field"][field]
        if field_stats["count"] > 0:
            field_stats["avg_confidence"] = field_stats["total_confidence"] / field_stats["count"]
        else:
            field_stats["avg_confidence"] = 0.0
    
    return stats


def list_needs_review(cards: List[Dict], threshold: float = NEEDS_REVIEW_THRESHOLD) -> List[Dict]:
    """
    List cards that need review based on confidence threshold.
    
    Returns:
        List of {
            "card_id": str,
            "title": str,
            "low_confidence_fields": list,
            "missing_fields": list,
            "source_type": str
        }
    """
    needs_review = []
    
    for card in cards:
        card_id = card.get("card_id", "unknown")
        confidence_data = card.get("_field_meta", card.get("_confidence", {}))
        
        low_conf_fields = []
        missing_fields = []
        
        for field in CONFIDENCE_FIELDS:
            field_conf = confidence_data.get(field, {})
            confidence = field_conf.get("confidence", 0.0)
            # Value is in the top-level card field, not in _field_meta
            value = card.get(field)
            
            # Check missing
            if value is None or value == "" or value == []:
                missing_fields.append(field)
            elif confidence < threshold:
                low_conf_fields.append({
                    "field": field,
                    "confidence": confidence,
                    "source": field_conf.get("source", "unknown")
                })
        
        if low_conf_fields or missing_fields:
            needs_review.append({
                "card_id": card_id,
                "title": card.get("title", "")[:60] + ("..." if len(card.get("title", "")) > 60 else ""),
                "low_confidence_fields": low_conf_fields,
                "missing_fields": missing_fields,
                "source_type": card.get("source_type", "unknown"),
                "source_file": card.get("source_file", "")
            })
    
    # Sort by number of issues
    needs_review.sort(key=lambda x: len(x["low_confidence_fields"]) + len(x["missing_fields"]), reverse=True)
    
    return needs_review


def show_card_detail(card_id: str, cards_dir: str, overrides_dir: str = None) -> Optional[Dict]:
    """
    Show detailed information for a specific card.
    
    Returns:
        Card detail dict or None if not found
    """
    cards = load_cards(cards_dir)
    
    # Find the card
    card = None
    for c in cards:
        if c.get("card_id") == card_id:
            card = c
            break
    
    if not card:
        return None
    
    # Get override status
    override_status = None
    if HAS_MERGER and overrides_dir:
        merger = CardMerger(overrides_dir=overrides_dir)
        override_status = merger.get_override_status(card_id)
    
    detail = {
        "card_id": card_id,
        "source_type": card.get("source_type"),
        "source_file": card.get("source_file"),
        "created_at": card.get("created_at"),
        "override_status": override_status,
        "fields": {}
    }
    
    confidence_data = card.get("_field_meta", card.get("_confidence", {}))
    
    for field in CONFIDENCE_FIELDS:
        field_conf = confidence_data.get(field, {})
        value = card.get(field)
        override_value = None
        
        # Check if this field is overridden
        if override_status and field in override_status.get("fields", []):
            override_value = value  # The merged value is the override
        
        detail["fields"][field] = {
            "value": value,
            "confidence": field_conf.get("confidence", 0.0),
            "source": field_conf.get("source", "auto"),
            "candidates": field_conf.get("candidates", []),
            "is_overridden": field in (override_status.get("fields", []) if override_status else [])
        }
    
    # Add additional fields
    detail["fields"]["related_constitutions"] = {
        "value": card.get("related_constitutions", []),
        "confidence": 0.5,  # Rule-based
        "source": "heuristic"
    }
    detail["fields"]["related_diseases"] = {
        "value": card.get("related_diseases", []),
        "confidence": 0.5,
        "source": "heuristic"
    }
    detail["fields"]["knowledge_points"] = {
        "value": f"{len(card.get('knowledge_points', []))} points",
        "confidence": 0.7 if card.get("knowledge_points") else 0.0,
        "source": "rule" if not card.get("_confidence", {}).get("abstract", {}).get("source") == "llm" else "llm"
    }
    
    return detail


def print_statistics(stats: Dict):
    """Print statistics in a formatted way."""
    print("\n" + "=" * 70)
    print("KNOWLEDGE CARD STATISTICS")
    print("=" * 70)
    
    print(f"\nTotal Cards: {stats['total_cards']}")
    print(f"By Source Type:")
    for source_type, count in stats["by_source_type"].items():
        print(f"  - {source_type}: {count}")
    
    print(f"\nCards Needing Review: {stats['needs_review_count']}")
    print(f"Cards with Overrides: {stats.get('cards_with_overrides', stats.get('reviewed_count', 0))}")
    
    print("\n" + "-" * 70)
    print("FIELD CONFIDENCE BREAKDOWN")
    print("-" * 70)
    
    print(f"\n{'Field':<15} {'Avg Conf':>10} {'High':>6} {'Medium':>8} {'Low':>6} {'Missing':>8}")
    print("-" * 70)
    
    for field, field_stats in stats["by_field"].items():
        avg = field_stats.get("avg_confidence", 0.0)
        high = field_stats.get("high_count", 0)
        medium = field_stats.get("medium_count", 0)
        low = field_stats.get("low_count", 0)
        missing = field_stats.get("missing_count", 0)
        
        # Color indicator
        if avg >= HIGH_CONFIDENCE_THRESHOLD:
            indicator = "[OK]"
        elif avg >= NEEDS_REVIEW_THRESHOLD:
            indicator = "[~]"
        else:
            indicator = "[!]"
        
        print(f"{field:<15} {avg:>10.2f} {high:>6} {medium:>8} {low:>6} {missing:>8}  {indicator}")
    
    print("\nLegend: [OK] High confidence, [~] Medium, [!] Low")
    print("=" * 70)


def print_needs_review(cards_needing_review: List[Dict], limit: int = 20):
    """Print cards needing review in a formatted way."""
    print("\n" + "=" * 70)
    print(f"CARDS NEEDING REVIEW ({len(cards_needing_review)} total)")
    print("=" * 70)
    
    for i, card in enumerate(cards_needing_review[:limit], 1):
        print(f"\n[{i}] {card['card_id']} ({card['source_type']})")
        print(f"    Title: {card['title']}")
        
        if card['missing_fields']:
            print(f"    Missing: {', '.join(card['missing_fields'])}")
        
        if card['low_confidence_fields']:
            print("    Low Confidence Fields:")
            for field in card['low_confidence_fields']:
                print(f"      - {field['field']}: {field['confidence']:.2f} ({field['source']})")
    
    if len(cards_needing_review) > limit:
        print(f"\n... and {len(cards_needing_review) - limit} more cards")
    
    print("\n" + "=" * 70)


def print_card_detail(detail: Dict):
    """Print card detail in a formatted way."""
    print("\n" + "=" * 70)
    print(f"CARD DETAIL: {detail['card_id']}")
    print("=" * 70)
    
    print(f"\nSource Type: {detail['source_type']}")
    print(f"Source File: {detail['source_file']}")
    print(f"Created: {detail['created_at']}")
    
    if detail.get("override_status"):
        os = detail["override_status"]
        print(f"\nOverride Status: {'Yes' if os['has_override'] else 'No'}")
        if os['has_override']:
            print(f"  Overridden Fields: {', '.join(os['overridden_fields'])}")
            print(f"  Reviewed: {os['reviewed_at']}")
            if os['reviewer_notes']:
                print(f"  Notes: {os['reviewer_notes']}")
    
    print("\n" + "-" * 70)
    print("FIELD VALUES")
    print("-" * 70)
    
    for field, field_data in detail["fields"].items():
        value = field_data.get("value")
        confidence = field_data.get("confidence", 0.0)
        source = field_data.get("source", "auto")
        is_overridden = field_data.get("is_overridden", False)
        
        # Format value
        if isinstance(value, list):
            if len(value) == 0:
                value_str = "(empty)"
            elif len(value) <= 3:
                value_str = ", ".join(str(v) for v in value)
            else:
                value_str = f"{len(value)} items: {', '.join(str(v) for v in value[:3])}..."
        elif value is None or value == "":
            value_str = "(empty)"
        elif isinstance(value, str) and len(value) > 100:
            value_str = value[:100] + "..."
        else:
            value_str = str(value)
        
        # Confidence indicator
        if confidence >= HIGH_CONFIDENCE_THRESHOLD:
            conf_indicator = "[OK]"
        elif confidence >= NEEDS_REVIEW_THRESHOLD:
            conf_indicator = "[~]"
        else:
            conf_indicator = "[!]"
        
        # Override indicator
        override_str = " [OVERRIDE]" if is_overridden else ""
        
        print(f"\n{field}:{override_str}")
        print(f"  Value: {value_str}")
        print(f"  Confidence: {confidence:.2f} {conf_indicator} | Source: {source}")
        
        # Show candidates if available
        candidates = field_data.get("candidates", [])
        if candidates:
            print("  Candidates:")
            for j, cand in enumerate(candidates[:3], 1):
                cand_value = cand.get("value", "")
                cand_conf = cand.get("confidence", 0.0)
                if isinstance(cand_value, list):
                    cand_value = ", ".join(str(v) for v in cand_value)
                print(f"    {j}. {cand_value[:50]}... (conf: {cand_conf:.2f})")
    
    print("\n" + "=" * 70)


def main():
    from runtime_paths import DEFAULT_CARDS_DIR, DEFAULT_OVERRIDES_DIR
    
    parser = argparse.ArgumentParser(description="Review knowledge cards")
    parser.add_argument("--cards", default=DEFAULT_CARDS_DIR, help="Cards directory")
    parser.add_argument("--overrides", default=DEFAULT_OVERRIDES_DIR, help="Overrides directory")
    parser.add_argument("--stats", action="store_true", help="Show statistics")
    parser.add_argument("--needs-review", action="store_true", help="List cards needing review")
    parser.add_argument("--threshold", type=float, default=NEEDS_REVIEW_THRESHOLD, help="Confidence threshold")
    parser.add_argument("--show", metavar="CARD_ID", help="Show detail for specific card")
    parser.add_argument("--list-overrides", action="store_true", help="List all overrides")
    parser.add_argument("--limit", type=int, default=20, help="Limit number of results")
    
    args = parser.parse_args()
    
    # Default to stats if no action specified
    if not any([args.stats, args.needs_review, args.show, args.list_overrides]):
        args.stats = True
    
    # Load cards
    cards = load_cards(args.cards)
    
    if args.stats:
        # Use merger to get override info
        if HAS_MERGER:
            merger = CardMerger(overrides_dir=args.overrides, cards_dir=args.cards)
            merged_cards, merge_stats = merger.merge_directory()
            # Add merge info to cards for statistics
            for card in merged_cards:
                card["_merge_info"] = merger.get_merge_info(card.get("card_id"))
            stats = calculate_statistics(merged_cards)
            stats["cards_with_overrides"] = merge_stats.get("cards_with_overrides", 0)
        else:
            stats = calculate_statistics(cards)
            stats["cards_with_overrides"] = 0
        print_statistics(stats)
    
    if args.needs_review:
        needs_review_list = list_needs_review(cards, args.threshold)
        print_needs_review(needs_review_list, args.limit)
    
    if args.show:
        detail = show_card_detail(args.show, args.cards, args.overrides)
        if detail:
            print_card_detail(detail)
        else:
            print(f"Card not found: {args.show}")
    
    if args.list_overrides:
        if not HAS_MERGER:
            print("Error: card_merger module not available")
            return
        
        merger = CardMerger(overrides_dir=args.overrides)
        overrides = merger.list_overrides()
        
        print(f"\nFound {len(overrides)} override files:\n")
        for o in overrides:
            print(f"  {o['card_id']}:")
            print(f"    Fields: {', '.join(o['fields'])}")
            print(f"    Reviewed: {o['reviewed_at'] or 'N/A'}")
            if o['reviewer_notes']:
                print(f"    Notes: {o['reviewer_notes']}")


if __name__ == "__main__":
    main()
