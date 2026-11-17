#!/usr/bin/env python3
"""
School Snack Manager
Stores morning and afternoon snack schedules from school.
Detects school closed days and warns when next month's schedule is missing.
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, Optional

from utils import write_json_atomic


class SnackManager:
    def __init__(self, base_path: str = "."):
        self.data_path = os.path.join(base_path, "household")
        os.makedirs(self.data_path, exist_ok=True)
        self.snack_file = os.path.join(self.data_path, "snack_schedule.json")
        self.schedule = self._load()

    def _load(self) -> Dict:
        if os.path.exists(self.snack_file):
            with open(self.snack_file, 'r') as f:
                return json.load(f)
        return {}

    def _save(self):
        write_json_atomic(self.snack_file, self.schedule)

    def set_snack(self, date_str: str, morning: str = "",
                  afternoon: str = "", school_closed: bool = False):
        existing = self.schedule.get(date_str, {})
        self.schedule[date_str] = {
            "morning":       morning if morning else existing.get("morning", ""),
            "afternoon":     afternoon if afternoon else existing.get("afternoon", ""),
            "school_closed": school_closed or existing.get("school_closed", False),
            "updated_at":    datetime.now().isoformat()
        }
        self._save()

    def get_snack(self, date_str: str = None) -> Optional[Dict]:
        if not date_str:
            date_str = datetime.now().strftime("%Y-%m-%d")
        return self.schedule.get(date_str)

    def get_today_snack(self) -> Optional[Dict]:
        return self.get_snack(datetime.now().strftime("%Y-%m-%d"))

    def is_school_closed(self, date_str: str = None) -> bool:
        if not date_str:
            date_str = datetime.now().strftime("%Y-%m-%d")
        try:
            parsed = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            return False
        if parsed.weekday() >= 5:
            return True
        snack = self.get_snack(date_str)
        if snack and snack.get("school_closed"):
            return True
        return False

    def is_school_closed_today(self) -> bool:
        return self.is_school_closed()

    def is_current_month_loaded(self) -> bool:
        prefix = datetime.now().strftime("%Y-%m-")
        return any(k.startswith(prefix) for k in self.schedule)

    def _first_of_next_month(self) -> datetime:
        """First day of next month, carrying today's time of day.

        `day=1` is load-bearing rather than tidiness. `replace(month=m + 1)`
        on the 31st of a month whose successor is shorter raises ValueError
        ("day is out of range for month") — Jan, Mar, May, Aug and Oct 31,
        five days a year, and every one of them inside the last-week window
        this class exists to watch. Two copies of this arithmetic had the bug
        and a third did not; one helper is why there cannot be a fourth.
        """
        now = datetime.now()
        if now.month == 12:
            return now.replace(year=now.year + 1, month=1, day=1)
        return now.replace(month=now.month + 1, day=1)

    def is_next_month_loaded(self) -> bool:
        prefix = self._first_of_next_month().strftime("%Y-%m-")
        return any(k.startswith(prefix) for k in self.schedule)

    def should_warn_about_missing_schedule(self) -> Optional[str]:
        """The one snack-schedule warning worth sending today, if any.

        The two branches below are mutually exclusive by construction: the
        next-month branch is only reached once the current month is loaded.
        """
        now = datetime.now()
        if now.weekday() >= 5:
            return None
        if not self.is_current_month_loaded():
            month_name = now.strftime("%B")
            return (
                f"📸 *Snack schedule missing for {month_name}*\n"
                f"Please send a photo of the school snack calendar to the group."
            )
        last_day = self._first_of_next_month() - timedelta(days=1)
        # Deliberately independent of whether today has a snack. Whether next
        # month's photo has arrived has nothing to do with today's snack, and
        # the caller gating this on `not snack_text` is what made this branch
        # unreachable on every normal school day of its own window — the only
        # days it is for. Do not reintroduce that guard here or at the call
        # site; the current-month branch above already cannot fire when a
        # snack exists, because that snack's own key is what makes
        # is_current_month_loaded() true.
        if now.day >= last_day.day - 6:
            if not self.is_next_month_loaded():
                next_name = self._first_of_next_month().strftime("%B")
                return (
                    f"📸 *Heads up* — please send the snack schedule photo "
                    f"for {next_name} when it's posted at school."
                )
        return None

    def format_for_briefing(self) -> Optional[str]:
        """Today's snack block, or None when there isn't one.

        Never returns a warning. Warnings travel in the briefing's own
        `snack_warning` field; one returned from here lands in `snack`
        instead, which the briefing prompt pastes verbatim under a "School
        Snacks Today" heading. "Send next month's photo" is not a snack, and
        rendering it as one is how the September 2026 reminder reached the
        family mislabelled.
        """
        if self.is_school_closed_today():
            return None
        snack = self.get_today_snack()
        if not snack:
            return None
        lines = ["🍎 *School Snacks Today*"]
        if snack.get("morning"):
            lines.append(f"  Morning: {snack['morning']}")
        if snack.get("afternoon"):
            lines.append(f"  Afternoon: {snack['afternoon']}")
        if len(lines) == 1:
            return None
        return "\n".join(lines)


if __name__ == "__main__":
    import sys
    # SKILL_DIR, not this module's directory. Passing the latter pointed the
    # CLI at features/school/household/snack_schedule.json — a phantom file.
    # `status` then reported an empty schedule and `clear` reported success
    # while the real schedule sat untouched.
    from core.config_loader import SKILL_DIR
    mgr = SnackManager(SKILL_DIR)
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "today":
            print(mgr.format_for_briefing() or "No snack info today")
        elif cmd == "status":
            print(f"Current month loaded: {mgr.is_current_month_loaded()}")
            print(f"Next month loaded:    {mgr.is_next_month_loaded()}")
            print(f"School closed today:  {mgr.is_school_closed_today()}")
            print(f"Total days stored:    {len(mgr.schedule)}")
            w = mgr.should_warn_about_missing_schedule()
            if w: print(f"\nWarning:\n{w}")
        elif cmd == "set" and len(sys.argv) >= 5:
            mgr.set_snack(sys.argv[2], sys.argv[3], sys.argv[4])
            print(f"Set snacks for {sys.argv[2]}")
        elif cmd == "clear":
            mgr.schedule = {}
            mgr._save()
            print("Cleared all snack data")
    else:
        print("Usage: snack_manager.py [today|status|set <date> <morning> <afternoon>|clear]")
