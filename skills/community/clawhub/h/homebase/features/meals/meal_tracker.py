#!/usr/bin/env python3
"""
Kids Meal Tracker

Reads structured meal config (kids[].meals) and per-installation learned
catalog (household/learned_catalog.json), exposes a deterministic resolver
that returns concrete menu options per kid per slot. The OpenClaw agent
picks from these options — it never interprets rule text — so even small
local models can produce a valid plan reliably.

The resolver is the single source of truth for "what can a kid eat at
slot X?" — both the daily suggestion (one slot, one day) and the weekly
planner (7 days × 2 kids × 3 slots) call into the same primitives.
"""

import json
import os
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

from utils import write_json_atomic


# ─── Constraint application ──────────────────────────────────────────────────

def _apply_constraints(slot_options: List[str],
                        constraints: List[str],
                        breakfast_choice: Optional[str]) -> List[str]:
    """
    Apply named constraints to filter slot options.

    Currently recognized constraint names:
      - "no_eggs_at_lunch_if_eggs_at_breakfast": if breakfast_choice contains
        "egg" (case-insensitive), drop options whose string contains "egg".

    Unknown constraints are silently ignored — adding new constraint names
    in config.json must be paired with adding handling here.
    """
    out = list(slot_options)
    if not constraints:
        return out
    if "no_eggs_at_lunch_if_eggs_at_breakfast" in constraints:
        if breakfast_choice and "egg" in breakfast_choice.lower():
            out = [o for o in out if "egg" not in o.lower()]
    return out


def _materialize_options(slot_data: dict) -> List[str]:
    """
    Convert a meal slot's structured config into a flat list of menu items.

    Two shapes are supported:
      - {"options": [...]}                                  → returns options
      - {"fixed_dish": "X", "rotate_grains": ["a", "b"]}    → returns
        ["X (a)", "X (b)"]
      - {"fixed_dish": "X", "rotate_grains": ["a", "b"], "options": [...]}
                                                            → returns the
        rotated dishes followed by the extra options

    Returns an empty list if neither shape is present.
    """
    items: List[str] = []
    fixed = slot_data.get("fixed_dish")
    grains = slot_data.get("rotate_grains") or []
    if fixed and grains:
        items.extend(f"{fixed} ({g})" for g in grains)
    items.extend(slot_data.get("options") or [])
    return items


# ─── MealTracker ─────────────────────────────────────────────────────────────

class MealTracker:
    """
    Owns three pieces of household state plus a read-through to config:

      household/meal_history.json          — append-only log of what was eaten
      household/learned_catalog.json       — per-installation catalog additions
      household/catalog_pending_review.json — off-catalog meals awaiting owner OK
    """

    HISTORY_FILE_NAME  = "meal_history.json"
    LEARNED_FILE_NAME  = "learned_catalog.json"
    PENDING_FILE_NAME  = "catalog_pending_review.json"

    def __init__(self, base_path: str = "."):
        self.base_path     = base_path
        self.data_path     = os.path.join(base_path, "household")
        os.makedirs(self.data_path, exist_ok=True)
        self.history_file  = os.path.join(self.data_path, self.HISTORY_FILE_NAME)
        self.learned_file  = os.path.join(self.data_path, self.LEARNED_FILE_NAME)
        self.pending_file  = os.path.join(self.data_path, self.PENDING_FILE_NAME)
        self.history       = self._load_json(self.history_file, default={})
        self.learned       = self._load_json(self.learned_file, default={})
        self.config        = self._load_config()

    # ── basic IO ─────────────────────────────────────────────────────────────

    @staticmethod
    def _load_json(path: str, default):
        if not os.path.exists(path):
            return default if default is not None else {}
        try:
            with open(path, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return default if default is not None else {}

    def _load_config(self):
        try:
            from core.config_loader import config
            return config
        except Exception:
            return None

    def _save_history(self):
        write_json_atomic(self.history_file, self.history)

    def _save_learned(self):
        write_json_atomic(self.learned_file, self.learned)

    def _save_pending(self, payload: dict):
        write_json_atomic(self.pending_file, payload)

    # ── history ──────────────────────────────────────────────────────────────

    def log_meal(self, child: str, meal_type: str, food: str,
                 date: Optional[str] = None) -> Tuple[bool, Optional[str]]:
        """
        Log what a child ate. Always appends to history (history is the
        ground truth of what happened, regardless of whether the meal is
        catalog-approved).

        Returns (in_catalog, off_catalog_reason):
          - in_catalog == True   → meal matched a known option
          - in_catalog == False  → meal was added to catalog_pending_review.json
        The caller decides what to do with the off-catalog signal.
        """
        child = child.lower()
        if child not in self.history:
            self.history[child] = []
        entry = {
            "date":      date or datetime.now().strftime("%Y-%m-%d"),
            "meal_type": meal_type,
            "food":      food,
            "logged_at": datetime.now().isoformat(),
        }
        self.history[child].append(entry)
        # Trim to 30 days so the file doesn't grow forever
        cutoff = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        self.history[child] = [
            e for e in self.history[child] if e.get("date", "") >= cutoff
        ]
        self._save_history()

        slot = self._slot_alias(meal_type)
        in_catalog = self._is_in_catalog(child, slot, food)
        if not in_catalog:
            self._record_pending(child, slot, food)
            return False, f"{food!r} is not in {child}'s {slot} catalog"
        return True, None

    def get_recent_meals(self, child: str, meal_type: str,
                         days: int = 5) -> List[str]:
        child = child.lower()
        cutoff = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        return [
            e["food"] for e in self.history.get(child, [])
            if e.get("meal_type") == meal_type and e.get("date", "") >= cutoff
        ]

    def had_eggs_today(self, child: str) -> bool:
        today = datetime.now().strftime("%Y-%m-%d")
        for entry in self.history.get(child.lower(), []):
            if (entry.get("date") == today
                    and entry.get("meal_type") == "breakfast"
                    and "egg" in entry.get("food", "").lower()):
                return True
        return False

    # ── catalog learning ─────────────────────────────────────────────────────

    @staticmethod
    def _slot_alias(meal_type: str) -> str:
        """Normalize meal_type → slot key. 'side'/'sides'/'snack' all map to 'sides'."""
        s = (meal_type or "").lower().strip()
        if s in ("side", "sides", "snack"):
            return "sides"
        return s

    @staticmethod
    def _normalize_meal(s: str) -> str:
        """Case-fold + collapse whitespace for exact-match dedup."""
        return " ".join((s or "").split()).strip().lower()

    def _is_in_catalog(self, child: str, slot: str, food: str) -> bool:
        if not self.config:
            return True  # tests with no config — don't fail logging
        kid = self._kid_obj(child)
        if not kid:
            return True
        approved = self._approved_options_for(kid, slot)
        norm = self._normalize_meal(food)
        return any(self._normalize_meal(o) == norm for o in approved)

    def _record_pending(self, child: str, slot: str, food: str) -> None:
        existing = self._load_json(self.pending_file, default={"pending": []})
        pending  = existing.get("pending", [])
        norm     = self._normalize_meal(food)
        for entry in pending:
            if (entry.get("kid") == child
                    and entry.get("slot") == slot
                    and self._normalize_meal(entry.get("meal", "")) == norm):
                entry["occurrences"] = int(entry.get("occurrences", 1)) + 1
                entry["last_seen"]   = datetime.now().isoformat()
                break
        else:
            pending.append({
                "kid":         child,
                "slot":        slot,
                "meal":        food,
                "first_seen":  datetime.now().isoformat(),
                "last_seen":   datetime.now().isoformat(),
                "occurrences": 1,
            })
        self._save_pending({"pending": pending})

    def _approved_options_for(self, kid, slot: str) -> List[str]:
        """Config options + learned catalog options for one kid + slot."""
        cfg_slot = kid.slot(slot) if hasattr(kid, "slot") else {}
        items    = list(_materialize_options(cfg_slot))
        learned  = (self.learned.get(kid.name.lower(), {}) or {}).get(slot, {}) or {}
        items.extend(learned.get("options") or [])
        # de-dup preserving order
        seen, out = set(), []
        for it in items:
            n = self._normalize_meal(it)
            if n in seen:
                continue
            seen.add(n)
            out.append(it)
        return out

    def _kid_obj(self, name: str):
        if not self.config or not hasattr(self.config, "kids"):
            return None
        for k in self.config.kids:
            if k.name.lower() == name.lower():
                return k
        return None

    # ── public catalog API (used by tools.py) ────────────────────────────────

    def get_pending_reviews(self) -> List[dict]:
        data = self._load_json(self.pending_file, default={"pending": []})
        return list(data.get("pending", []))

    def apply_catalog_decisions(self, decisions: List[dict]) -> dict:
        """
        Apply a structured list of catalog decisions to learned_catalog.json.

        ``decisions`` is a list of objects each shaped like
        ``{"index": <int>, "decision": "accept"|"reject"}``. Indices refer to
        the current pending list (zero-based). The function:
          1. Validates every index exists in the pending list — if any index
             is out of range or duplicated, the entire batch is rejected with
             a structured error (defends against the agent fabricating
             approvals for nonexistent items).
          2. For each accept, adds the meal to ``learned_catalog.json`` under
             the right kid + slot.
          3. Removes processed entries from ``catalog_pending_review.json``
             (both accepts and rejects are removed).

        Returns ``{"ok": True, "added": [...], "rejected": [...]}`` on success
        or ``{"ok": False, "error": "..."}`` on validation failure.
        """
        pending = self.get_pending_reviews()
        if not isinstance(decisions, list):
            return {"ok": False, "error": "decisions must be a list"}

        seen_indices = set()
        for d in decisions:
            if not isinstance(d, dict):
                return {"ok": False, "error": "each decision must be an object"}
            idx = d.get("index")
            decision = d.get("decision")
            if not isinstance(idx, int):
                return {"ok": False, "error": f"missing or non-int index in {d}"}
            if idx < 0 or idx >= len(pending):
                return {"ok": False, "error": f"index {idx} out of range (0..{len(pending)-1})"}
            if idx in seen_indices:
                return {"ok": False, "error": f"duplicate index {idx}"}
            if decision not in ("accept", "reject"):
                return {"ok": False, "error": f"decision must be 'accept' or 'reject', got {decision!r}"}
            seen_indices.add(idx)

        added: List[dict] = []
        rejected: List[dict] = []
        for d in decisions:
            entry = pending[d["index"]]
            if d["decision"] == "accept":
                kid_key = entry["kid"]
                slot    = entry["slot"]
                meal    = entry["meal"]
                self.learned.setdefault(kid_key, {}).setdefault(slot, {"options": []})
                opts = self.learned[kid_key][slot].setdefault("options", [])
                if not any(self._normalize_meal(o) == self._normalize_meal(meal) for o in opts):
                    opts.append(meal)
                added.append(entry)
            else:
                rejected.append(entry)

        # Remove processed entries
        keep_indices = set(range(len(pending))) - seen_indices
        new_pending  = [pending[i] for i in sorted(keep_indices)]
        self._save_learned()
        self._save_pending({"pending": new_pending})
        return {"ok": True, "added": added, "rejected": rejected}

    # ── resolver: per-day, per-kid, per-slot menu pool ───────────────────────

    def get_meal_suggestions(self) -> Dict:
        """
        Return today's per-kid suggestion (one breakfast, one lunch, one side).

        Picks deterministically by avoiding recent repeats. Used by the
        morning briefing's meal section. The agent does not need to interpret
        anything — every value is a concrete menu item from the resolved pool.
        """
        kids = self.config.kids if (self.config and hasattr(self.config, "kids")) else []
        suggestions: Dict[str, dict] = {}
        for kid in kids:
            name      = kid.name.lower()
            had_eggs  = self.had_eggs_today(name)

            breakfast_pool = self._approved_options_for(kid, "breakfast")
            lunch_pool_raw = self._approved_options_for(kid, "lunch")
            sides_pool     = self._approved_options_for(kid, "sides")
            constraints    = list((kid.slot("lunch").get("constraints") or []))

            # Pick breakfast (avoid recent), then apply constraints to lunch
            breakfast = self._pick_avoiding(
                breakfast_pool, self.get_recent_meals(name, "breakfast", days=3)
            )
            effective_breakfast = breakfast if breakfast != "TBD" else None
            lunch_pool = _apply_constraints(lunch_pool_raw, constraints,
                                            effective_breakfast)
            # If we have history of eggs at breakfast today, also enforce
            if had_eggs:
                lunch_pool = _apply_constraints(lunch_pool_raw, constraints,
                                                "Scrambled eggs")
            lunch = self._pick_avoiding(
                lunch_pool, self.get_recent_meals(name, "lunch", days=3)
            )
            side  = random.choice(sides_pool) if sides_pool else "Fruit"

            note = ""
            if had_eggs and "no_eggs_at_lunch_if_eggs_at_breakfast" in constraints:
                note = "Had eggs for breakfast today."

            suggestions[name] = {
                "name":      kid.name,
                "breakfast": breakfast,
                "lunch":     lunch,
                "side":      side,
                "note":      note,
            }
        return suggestions

    def get_weekly_pool(self, days: int = 7) -> Dict:
        """
        Return the menu pool for ``days`` consecutive days, per kid, per slot.

        Shape::

            {
              "monday":   {"amyra": {"breakfast": [...], "lunch": [...], "sides": [...]},
                            "reyansh": {...}},
              "tuesday":  {...},
              ...
            }

        Constraints are NOT pre-applied — the lunch pool contains every option
        regardless of which breakfast might be picked. ``save_meal_plan``'s
        validator enforces constraints at write time. This keeps the agent's
        job simple: pick exactly one item from each list, no reasoning about
        rule interactions.
        """
        DAY_NAMES = ["monday", "tuesday", "wednesday", "thursday",
                     "friday", "saturday", "sunday"]
        days = max(1, min(int(days or 7), len(DAY_NAMES)))
        kids = self.config.kids if (self.config and hasattr(self.config, "kids")) else []
        pool: Dict[str, dict] = {}
        for d in DAY_NAMES[:days]:
            day_pool: Dict[str, dict] = {}
            for kid in kids:
                day_pool[kid.name.lower()] = {
                    "breakfast": self._approved_options_for(kid, "breakfast"),
                    "lunch":     self._approved_options_for(kid, "lunch"),
                    "sides":     self._approved_options_for(kid, "sides"),
                }
            pool[d] = day_pool
        return pool

    def validate_plan(self, plan: dict) -> dict:
        """
        Check that every chosen meal in ``plan`` is in the kid's resolved pool
        for that slot, and that lunch picks honor constraints relative to the
        same day's breakfast pick.

        Returns ``{"ok": True, "corrections": [...]}`` if the plan is valid
        (corrections is empty when nothing was auto-fixed) or
        ``{"ok": False, "errors": [...]}`` if anything is unrecoverable.

        Auto-correction policy: if a chosen lunch item violates the
        no-eggs-after-eggs constraint, swap it for the first valid lunch
        option in the pool and record the swap. If no valid lunch option
        exists at all, surface an error instead.
        """
        if not isinstance(plan, dict):
            return {"ok": False, "errors": ["plan must be an object"]}
        kids = self.config.kids if (self.config and hasattr(self.config, "kids")) else []
        kid_by_key = {k.name.lower(): k for k in kids}

        errors:      List[str] = []
        corrections: List[dict] = []

        for day, day_plan in plan.items():
            if not isinstance(day_plan, dict):
                errors.append(f"{day}: must be an object of kid → meals")
                continue
            for kid_key, meals in day_plan.items():
                if not isinstance(meals, dict):
                    errors.append(f"{day}/{kid_key}: must be an object of slot → meal")
                    continue
                kid = kid_by_key.get(kid_key.lower())
                if not kid:
                    errors.append(f"{day}/{kid_key}: unknown kid")
                    continue

                # Validate breakfast
                breakfast = meals.get("breakfast")
                bf_pool   = self._approved_options_for(kid, "breakfast")
                if breakfast not in bf_pool:
                    errors.append(
                        f"{day}/{kid_key}: breakfast {breakfast!r} not in catalog "
                        f"({len(bf_pool)} options)"
                    )

                # Validate side
                side      = meals.get("side") or meals.get("sides")
                side_pool = self._approved_options_for(kid, "sides")
                if side and side not in side_pool:
                    errors.append(
                        f"{day}/{kid_key}: side {side!r} not in catalog "
                        f"({len(side_pool)} options)"
                    )

                # Validate lunch with constraints (auto-correct if possible)
                lunch        = meals.get("lunch")
                lunch_raw    = self._approved_options_for(kid, "lunch")
                constraints  = list((kid.slot("lunch").get("constraints") or []))
                lunch_pool   = _apply_constraints(lunch_raw, constraints, breakfast)

                if lunch in lunch_pool:
                    pass  # ok
                elif lunch in lunch_raw:
                    # Member of full pool but excluded by constraint — auto-fix
                    if lunch_pool:
                        new_lunch = lunch_pool[0]
                        meals["lunch"] = new_lunch
                        corrections.append({
                            "day":  day,
                            "kid":  kid_key,
                            "slot": "lunch",
                            "from": lunch,
                            "to":   new_lunch,
                            "reason": "constraint:no_eggs_at_lunch_if_eggs_at_breakfast",
                        })
                    else:
                        errors.append(
                            f"{day}/{kid_key}: no valid lunch option after applying "
                            f"constraints to breakfast {breakfast!r}"
                        )
                else:
                    errors.append(
                        f"{day}/{kid_key}: lunch {lunch!r} not in catalog "
                        f"({len(lunch_raw)} options)"
                    )

        if errors:
            return {"ok": False, "errors": errors, "corrections": corrections}
        return {"ok": True, "corrections": corrections}

    # ── helpers ──────────────────────────────────────────────────────────────

    @staticmethod
    def _pick_avoiding(options: List[str], used: List[str]) -> str:
        if not options:
            return "TBD"
        used_norm = {MealTracker._normalize_meal(u) for u in used}
        fresh = [o for o in options if MealTracker._normalize_meal(o) not in used_norm]
        return random.choice(fresh if fresh else options)
