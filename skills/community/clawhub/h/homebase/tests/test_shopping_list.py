"""
test_shopping_list.py — Unit tests for shopping_list.py

Covers:
  - ShoppingList.add(): new item, duplicate increments quantity, store update
  - ShoppingList.remove(): exact match, partial match, missing item
  - ShoppingList._load() / _save(): file locking, atomic write
  - ShoppingList.format_for_whatsapp(): grouped by store, store filter
  - detect_store(): keyword matching for costco/indian/target/general
"""
import fcntl
import json
import os
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

for mod in ("google", "google.oauth2", "google.oauth2.credentials",
            "google.auth", "google.auth.transport", "google.auth.transport.requests",
            "googleapiclient", "googleapiclient.discovery"):
    sys.modules.setdefault(mod, MagicMock() if "MagicMock" in dir() else __import__("unittest.mock", fromlist=["MagicMock"]).MagicMock())

from unittest.mock import MagicMock

with patch("core.keychain_secrets.load_google_secrets", return_value=None), \
     patch("core.config_loader._load_config") as _mc:
    from conftest import MINIMAL_CONFIG
    from core.config_loader import Config
    _mc.return_value = Config(MINIMAL_CONFIG)
    from features.shopping.shopping_list import ShoppingList, detect_store, STORE_LABELS


# ─── detect_store ─────────────────────────────────────────────────────────────

class TestDetectStore:
    def test_detects_costco(self):
        assert detect_store("from costco") == "costco"

    def test_detects_indian_store(self):
        assert detect_store("from Spencer's indian store") == "indian"
        assert detect_store("ninas grocery") == "indian"

    def test_detects_target(self):
        assert detect_store("at target") == "target"
        assert detect_store("walmart") == "target"

    def test_defaults_to_general(self):
        assert detect_store("random item") == "general"

    def test_case_insensitive(self):
        assert detect_store("COSTCO") == "costco"
        assert detect_store("Target") == "target"


# ─── ShoppingList.add ─────────────────────────────────────────────────────────

class TestShoppingListAdd:
    def test_adds_new_item(self, tmp_path):
        sl = ShoppingList(str(tmp_path))
        item = sl.add("Milk", 2, "costco")
        assert item["name"] == "Milk"
        assert item["quantity"] == 2
        assert item["store"] == "costco"

    def test_increments_quantity_on_duplicate(self, tmp_path):
        sl = ShoppingList(str(tmp_path))
        sl.add("Eggs", 1)
        sl.add("Eggs", 2)
        assert sl.items["eggs"]["quantity"] == 3

    def test_updates_store_on_duplicate_if_not_general(self, tmp_path):
        sl = ShoppingList(str(tmp_path))
        sl.add("Ghee", 1, "general")
        sl.add("Ghee", 1, "indian")  # more specific store
        assert sl.items["ghee"]["store"] == "indian"

    def test_does_not_update_store_to_general_if_already_set(self, tmp_path):
        sl = ShoppingList(str(tmp_path))
        sl.add("Paneer", 1, "indian")
        sl.add("Paneer", 1, "general")  # should not downgrade
        assert sl.items["paneer"]["store"] == "indian"

    def test_ignores_empty_item_name(self, tmp_path):
        sl = ShoppingList(str(tmp_path))
        result = sl.add("   ", 1)
        assert result == {}
        assert sl.is_empty()

    def test_title_cases_item_name(self, tmp_path):
        sl = ShoppingList(str(tmp_path))
        sl.add("olive oil", 1)
        assert sl.items["olive oil"]["name"] == "Olive Oil"

    def test_persists_to_file(self, tmp_path):
        sl = ShoppingList(str(tmp_path))
        sl.add("Bread", 1, "target")
        sl2 = ShoppingList(str(tmp_path))
        assert "bread" in sl2.items


# ─── ShoppingList.remove ──────────────────────────────────────────────────────

class TestShoppingListRemove:
    def test_removes_existing_item(self, tmp_path):
        sl = ShoppingList(str(tmp_path))
        sl.add("Butter", 1)
        result = sl.remove("Butter")
        assert result is True
        assert "butter" not in sl.items

    def test_removes_by_partial_match(self, tmp_path):
        sl = ShoppingList(str(tmp_path))
        sl.add("Organic Milk", 1)
        result = sl.remove("milk")
        assert result is True

    def test_returns_false_for_missing_item(self, tmp_path):
        sl = ShoppingList(str(tmp_path))
        result = sl.remove("nonexistent item")
        assert result is False

    def test_persists_removal_to_file(self, tmp_path):
        sl = ShoppingList(str(tmp_path))
        sl.add("Yogurt", 1)
        sl.remove("Yogurt")
        sl2 = ShoppingList(str(tmp_path))
        assert "yogurt" not in sl2.items

    def test_case_insensitive_remove(self, tmp_path):
        sl = ShoppingList(str(tmp_path))
        sl.add("Avocado", 2)
        result = sl.remove("AVOCADO")
        assert result is True


# ─── ShoppingList._load / _save ──────────────────────────────────────────────

class TestShoppingListPersistence:
    def test_empty_list_when_no_file(self, tmp_path):
        sl = ShoppingList(str(tmp_path))
        assert sl.items == {}

    def test_atomic_write_no_tmp_leftovers(self, tmp_path):
        sl = ShoppingList(str(tmp_path))
        sl.add("Cheese", 1)
        tmp_files = list(Path(tmp_path / "household").glob("*.tmp"))
        assert tmp_files == []

    def test_round_trip_preserves_all_fields(self, tmp_path):
        sl = ShoppingList(str(tmp_path))
        sl.add("Spinach", 3, "costco", source="whatsapp")
        sl2 = ShoppingList(str(tmp_path))
        item = sl2.items["spinach"]
        assert item["quantity"] == 3
        assert item["store"] == "costco"
        assert item["source"] == "whatsapp"


# ─── format_for_whatsapp ──────────────────────────────────────────────────────

class TestFormatForWhatsapp:
    def test_empty_list_message(self, tmp_path):
        sl = ShoppingList(str(tmp_path))
        result = sl.format_for_whatsapp()
        assert "empty" in result.lower() or "nothing" in result.lower()

    def test_grouped_by_store(self, tmp_path):
        sl = ShoppingList(str(tmp_path))
        sl.add("Milk", 2, "costco")
        sl.add("Ghee", 1, "indian")
        result = sl.format_for_whatsapp()
        assert "Costco" in result
        assert "Indian Store" in result
        assert "Milk" in result
        assert "Ghee" in result

    def test_store_filter(self, tmp_path):
        sl = ShoppingList(str(tmp_path))
        sl.add("Paneer", 1, "indian")
        sl.add("Towels", 1, "target")
        result = sl.format_for_whatsapp(store_filter="indian")
        assert "Paneer" in result
        assert "Towels" not in result

    def test_store_filter_empty_message(self, tmp_path):
        sl = ShoppingList(str(tmp_path))
        sl.add("Milk", 1, "costco")
        result = sl.format_for_whatsapp(store_filter="indian")
        assert "Nothing" in result or "empty" in result.lower()

    def test_integer_quantity_displayed_without_decimal(self, tmp_path):
        sl = ShoppingList(str(tmp_path))
        sl.add("Eggs", 2, "costco")
        result = sl.format_for_whatsapp()
        assert "×2" in result

    def test_total_count_in_header(self, tmp_path):
        sl = ShoppingList(str(tmp_path))
        sl.add("Item A", 1, "general")
        sl.add("Item B", 1, "general")
        result = sl.format_for_whatsapp()
        assert "2 items" in result or "2 item" in result


# ─── clear / clear_store ──────────────────────────────────────────────────────

class TestClearOperations:
    def test_clear_removes_all_items(self, tmp_path):
        sl = ShoppingList(str(tmp_path))
        sl.add("A", 1); sl.add("B", 1); sl.add("C", 1)
        sl.clear()
        assert sl.is_empty()

    def test_clear_store_removes_only_that_store(self, tmp_path):
        sl = ShoppingList(str(tmp_path))
        sl.add("Milk", 1, "costco")
        sl.add("Ghee", 1, "indian")
        sl.clear_store("costco")
        assert "milk" not in sl.items
        assert "ghee" in sl.items
