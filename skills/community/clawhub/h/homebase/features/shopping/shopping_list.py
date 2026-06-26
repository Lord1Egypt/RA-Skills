#!/usr/bin/env python3
"""
Shopping List Manager
Simple store-aware shopping list. Stores are config-driven via
`config.stores` (any number of named buckets).
"""

import fcntl
import json
import os
import tempfile
from datetime import datetime
from typing import Dict, List, Optional


# ─── Store Detection ─────────────────────────────────────────────────────────

STORE_KEYWORDS = {
    "costco":  ["costco", "cost co"],
    "indian":  ["indian", "spencer", "ninas", "nina's", "desi", "patel", "apna bazar",
                "india", "indian store", "indian grocery", "subzi", "bazaar"],
    "target":  ["target", "walmart", "wal-mart", "walgreens", "cvs", "safeway",
                "kroger", "vons", "ralphs"],
}

STORE_LABELS = {
    "costco": "Costco",
    "indian": "Indian Store",
    "target": "Target / Walmart",
    "general": "General"
}

COSTCO_ENTRANCE  = ["apple", "banana", "fruit", "veggie", "vegetable", "berry",
                    "bread", "bak", "produce", "orange", "grape", "lettuce",
                    "spinach", "carrot", "tomato", "onion", "avocado"]
COSTCO_BACK      = ["milk", "egg", "cheese", "meat", "chicken", "beef", "pork",
                    "butter", "yogurt", "cream", "ghee", "paneer", "curd"]


def detect_store(message: str) -> str:
    """Detect which store from natural language."""
    msg = message.lower()
    for store, keywords in STORE_KEYWORDS.items():
        if any(kw in msg for kw in keywords):
            return store
    return "general"


def extract_item_and_store(message: str) -> tuple:
    import re
    msg = message.lower()

    # Detect store first
    store = detect_store(msg)

    # Remove "from X store", "at X store", "from X"
    msg = re.sub(r'\b(?:from|at)\s+\w+\s+(?:store|grocery|market)\b', '', msg)
    msg = re.sub(r'\b(?:from|at)\s+(?:' + '|'.join(
        kw for keywords in STORE_KEYWORDS.values() for kw in keywords
    ) + r')\b', '', msg)

    # Remove standalone store words
    for keywords in STORE_KEYWORDS.values():
        for kw in keywords:
            msg = re.sub(r'\b' + re.escape(kw) + r'\b', '', msg)

    # Remove "store", "grocery" standalone
    msg = re.sub(r'\b(?:store|grocery|market)\b', '', msg)

    # Remove action words
    msg = re.sub(r'^(?:add|get|need|pick up|grab)\s+', '', msg.strip())
    msg = re.sub(r'\s+', ' ', msg).strip()

    return msg.strip(), store


# ─── Shopping List Manager ───────────────────────────────────────────────────

class ShoppingList:
    def __init__(self, base_path: str = "."):
        self.data_path = os.path.join(base_path, "household")
        os.makedirs(self.data_path, exist_ok=True)
        self.list_file = os.path.join(self.data_path, "shopping_list.json")
        self.items = self._load()

    def _load(self) -> Dict:
        if os.path.exists(self.list_file):
            with open(self.list_file, 'r') as f:
                fcntl.flock(f, fcntl.LOCK_SH)
                try:
                    return json.load(f)
                finally:
                    fcntl.flock(f, fcntl.LOCK_UN)
        return {}

    def _save(self):
        """Atomic write with exclusive lock — prevents corruption under concurrent access."""
        dir_path = os.path.dirname(self.list_file)
        with tempfile.NamedTemporaryFile('w', dir=dir_path, delete=False, suffix='.tmp') as tmp:
            json.dump(self.items, tmp, indent=2)
            tmp_path = tmp.name
        with open(tmp_path, 'a') as lock_f:
            fcntl.flock(lock_f, fcntl.LOCK_EX)
            try:
                os.replace(tmp_path, self.list_file)
            finally:
                fcntl.flock(lock_f, fcntl.LOCK_UN)

    # ─── Add / Remove ────────────────────────────────────────────────────────

    def add(self, name: str, quantity: float = 1,
            store: str = "general", source: str = "manual") -> Dict:
        """Add item to shopping list."""
        key = name.lower().strip()
        if not key:
            return {}

        if key in self.items:
            self.items[key]["quantity"] += quantity
            self.items[key]["updated_at"] = datetime.now().isoformat()
            # Update store if specified
            if store != "general":
                self.items[key]["store"] = store
        else:
            self.items[key] = {
                "name":       name.title(),
                "quantity":   quantity,
                "store":      store,
                "source":     source,
                "added_at":   datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
        self._save()
        return self.items[key]

    def remove(self, name: str) -> bool:
        """Remove item when bought."""
        key = name.lower().strip()
        # Try exact match first
        if key in self.items:
            del self.items[key]
            self._save()
            return True
        # Try partial match
        for k in list(self.items.keys()):
            if key in k or k in key:
                del self.items[k]
                self._save()
                return True
        return False

    def clear(self):
        self.items = {}
        self._save()

    def clear_store(self, store: str):
        """Clear all items for a specific store (after shopping trip)."""
        self.items = {k: v for k, v in self.items.items()
                     if v.get("store") != store}
        self._save()

    # ─── Query ───────────────────────────────────────────────────────────────

    def get_all(self) -> List[Dict]:
        return sorted(self.items.values(), key=lambda x: x["name"])

    def get_by_store(self, store: str) -> List[Dict]:
        return [v for v in self.items.values() if v.get("store") == store]

    def is_empty(self) -> bool:
        return len(self.items) == 0

    # ─── Format for WhatsApp ─────────────────────────────────────────────────

    def format_for_whatsapp(self, store_filter: str = None) -> str:
        """Format shopping list grouped by store."""
        if self.is_empty():
            return "✅ Shopping list is empty — nothing to grab!"

        # Filter by store if specified
        if store_filter:
            items = self.get_by_store(store_filter)
            if not items:
                return f"✅ Nothing on the list for {STORE_LABELS.get(store_filter, store_filter)}!"
            lines = [f"🛒 *{STORE_LABELS.get(store_filter, store_filter)} List*\n"]
            for item in sorted(items, key=lambda x: x["name"]):
                qty = item["quantity"]
                qty_str = f"×{int(qty) if qty == int(qty) else qty}"
                lines.append(f"  • {item['name']} {qty_str}")
            return "\n".join(lines)

        # Group by store
        grouped: Dict[str, List] = {}
        for item in self.get_all():
            store = item.get("store", "general")
            grouped.setdefault(store, []).append(item)

        total = len(self.items)
        lines = [f"🛒 *Shopping List* ({total} item{'s' if total != 1 else ''})\n"]

        store_order = ["costco", "indian", "target", "general"]
        for store in store_order:
            if store not in grouped:
                continue
            lines.append(f"*{STORE_LABELS[store]}*")
            for item in grouped[store]:
                qty = item["quantity"]
                qty_str = f"×{int(qty) if qty == int(qty) else qty}"
                lines.append(f"  • {item['name']} {qty_str}")
            lines.append("")

        return "\n".join(lines).strip()

    def format_costco(self) -> str:
        """Format Costco items by Technology Drive store layout."""
        costco_items = self.get_by_store("costco")
        general_items = self.get_by_store("general")
        all_items = costco_items + general_items

        if not all_items:
            return "✅ Nothing on the Costco list!"

        entrance, middle, back = [], [], []

        for item in sorted(all_items, key=lambda x: x["name"]):
            name_lower = item["name"].lower()
            qty = item["quantity"]
            qty_str = f"×{int(qty) if qty == int(qty) else qty}"
            label = f"{item['name']} {qty_str}"

            if any(kw in name_lower for kw in COSTCO_BACK):
                back.append(label)
            elif any(kw in name_lower for kw in COSTCO_ENTRANCE):
                entrance.append(label)
            else:
                middle.append(label)

        lines = ["🛒 *Costco — Technology Drive*\n"]
        if entrance:
            lines.append("📍 *Entrance / Right (Produce & Bakery)*")
            for i in entrance:
                lines.append(f"  • {i}")
            lines.append("")
        if middle:
            lines.append("📍 *Middle Aisles (Pantry & Snacks)*")
            for i in middle:
                lines.append(f"  • {i}")
            lines.append("")
        if back:
            lines.append("📍 *Back Wall (Dairy & Meats)*")
            for i in back:
                lines.append(f"  • {i}")

        return "\n".join(lines)


if __name__ == "__main__":
    import sys
    sl = ShoppingList(os.path.join(os.path.dirname(os.path.abspath(__file__)), ""))

    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "list":
            print(sl.format_for_whatsapp())
        elif cmd == "costco":
            print(sl.format_costco())
        elif cmd == "add" and len(sys.argv) > 2:
            item, store = extract_item_and_store(" ".join(sys.argv[2:]))
            sl.add(item, 1, store)
            print(f"Added {item} → {STORE_LABELS.get(store, store)}")
        elif cmd == "remove" and len(sys.argv) > 2:
            sl.remove(sys.argv[2])
            print(f"Removed {sys.argv[2]}")
        elif cmd == "clear":
            sl.clear()
            print("Cleared")
        elif cmd == "store" and len(sys.argv) > 2:
            print(sl.format_for_whatsapp(sys.argv[2]))
    else:
        print("Usage: shopping_list.py [list|costco|add <item> [from store]|remove <item>|clear|store <name>]")
