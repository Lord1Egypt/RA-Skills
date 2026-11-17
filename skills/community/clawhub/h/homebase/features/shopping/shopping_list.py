#!/usr/bin/env python3
"""
Shopping List Manager
Simple store-aware shopping list. Items carry a store bucket chosen by the
caller; STORE_LABELS below is how each bucket is displayed.
"""

import fcntl
import json
import os
from datetime import datetime
from typing import Dict, List

from utils import write_json_atomic, locked_file


# ─── Store buckets ───────────────────────────────────────────────────────────
#
# Display labels only. The keyword-matching store *detector* that used to live
# here (detect_store / extract_item_and_store) parsed free text like "milk from
# costco" — a job the agent does now, since tools.add_to_grocery_list takes an
# explicit `store`. It had no production caller and hardcoded the family's
# store list against a docstring claiming the stores were config-driven.

STORE_LABELS = {
    "costco": "Costco",
    "indian": "Indian Store",
    "target": "Target / Walmart",
    "general": "General"
}


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
        write_json_atomic(self.list_file, self.items)

    # ─── Add / Remove ────────────────────────────────────────────────────────
    #
    # Each mutating method holds locked_file() across the full reload →
    # mutate → save cycle (not just the save), so two near-simultaneous
    # calls from separate processes can't silently drop each other's change.

    def add(self, name: str, quantity: float = 1,
            store: str = "general", source: str = "manual") -> Dict:
        """Add item to shopping list."""
        key = name.lower().strip()
        if not key:
            return {}

        with locked_file(self.list_file):
            self.items = self._load()
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
        with locked_file(self.list_file):
            self.items = self._load()
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
        with locked_file(self.list_file):
            self.items = {}
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

        # Derived from STORE_LABELS, plus anything grouped that it does not
        # know about. Hardcoding the four keys here meant a bucket present in
        # STORE_LABELS but missing from this list had its items counted in the
        # `total` header above and then never printed — a silent drop in the
        # one output the family actually reads.
        store_order = list(STORE_LABELS) + [
            k for k in grouped if k not in STORE_LABELS]
        for store in store_order:
            if store not in grouped:
                continue
            lines.append(f"*{STORE_LABELS.get(store, store.title())}*")
            for item in grouped[store]:
                qty = item["quantity"]
                qty_str = f"×{int(qty) if qty == int(qty) else qty}"
                lines.append(f"  • {item['name']} {qty_str}")
            lines.append("")

        return "\n".join(lines).strip()


if __name__ == "__main__":
    import sys
    from core.config_loader import SKILL_DIR

    # SKILL_DIR, not this module's directory. Passing the latter made the CLI
    # read and write features/shopping/household/shopping_list.json — a phantom
    # list, separate from the real one every tool uses.
    sl = ShoppingList(SKILL_DIR)

    if len(sys.argv) > 1 and sys.argv[1] == "list":
        print(sl.format_for_whatsapp())
    elif len(sys.argv) > 2 and sys.argv[1] == "store":
        print(sl.format_for_whatsapp(sys.argv[2]))
    else:
        print("Usage: shopping_list.py [list|store <name>]")
        print("Writes go through tools.py — see references/agent.md.")
