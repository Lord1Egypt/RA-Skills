"""
test_snack_collision.py — save_snack_schedule refuses a column that is a copy
of the column already stored for the same dates.

Written after 2026-09-08, when September's morning snacks were overwritten with
September's afternoon snacks and the family was told both meals were the same
item every day for a month.

The sequence, from the session transcript:

  16:41:21  view_image(<morning photo>)   → save type="morning"    correct
  16:44:58  view_image(<afternoon photo>) → all three image models down
  16:48:38  view_image(<afternoon photo>) → save type="afternoon"  correct
  16:49:45  view_image(<AFTERNOON photo>, "extract the MORNING schedule")
            → the model returned the afternoon items under a heading reading
              "September 2026 Morning Snack Schedule"
  16:50:07  save type="morning" with those items → clobbered 16:41:21

Only the second image was still in the agent's recent context; the morning
photo sat in a different `openclaw-staged-*` directory that never got listed.
Nothing in the vision result marks which file it came from, so a wrong path is
indistinguishable from a right one at the call site — the write is the last
place this can be caught.

The duplicate was printed in the tool's own success message twice, and waved
off both times, including when the owner asked directly. So this guard fails
the write; it does not warn.
"""

import json
import sys
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent.parent))

import tools


# The real September 2026 afternoon calendar, as extracted at 16:48:38.
AFTERNOON = {
    1:  "1/2 cup snap peas; 1 clementine",
    2:  "1 Hawaiian roll; 1 cheese stick",
    3:  "1 granola bar; 1/2 cup blueberries",
    4:  "1/2 cup Chex; 1/2 cup milk; 1/2 cup raisins",
    8:  "1 bag granola bites; 1/2 banana",
    9:  "Popcorn or pretzels; 1/2 cup blueberries",
    10: "1/2 cup Wheat Thins; 1 Babybel cheese",
    11: "1/2 cup veggie straws; Mandarins",
}

# The real September 2026 morning calendar, as extracted at 16:40:34 — a
# different photo, different items, same dates.
MORNING = {
    1:  "1/2 slice raisin bread; 1 tsp cream cheese",
    2:  "1 graham cracker; 1/2 banana",
    3:  "1/2 cup Pirate Booty; 1/2 cup strawberries",
    4:  "1 slice wheat bread; 1 pat butter; 1/2 cup applesauce",
    8:  "1/4 cup Triscuits; 1/2 cup strawberries",
    9:  "1/2 English muffin; Wow butter",
    10: "1/2c Kix cereal; 1/2c milk; Peaches",
    11: "1/2 pita bread; Hummus; raisins",
}


def _days(column, values):
    return [{"day": d, column: text} for d, text in sorted(values.items())]


def _save(tmp_path, column, values, **kw):
    with patch.object(tools, "SKILL_DIR", str(tmp_path)):
        return tools.save_snack_schedule(
            month=9, year=2026, type=column, days=_days(column, values), **kw)


def _stored(tmp_path):
    return json.loads(
        (tmp_path / "household" / "snack_schedule.json").read_text())


# ── The incident ─────────────────────────────────────────────────────────────

def test_afternoon_items_resaved_as_morning_are_refused(tmp_path):
    """The 16:50:07 call. Fails without the guard: it used to return success."""
    _save(tmp_path, "morning", MORNING)
    _save(tmp_path, "afternoon", AFTERNOON)

    result = _save(tmp_path, "morning", AFTERNOON)

    assert result.startswith("❌")
    assert "same photo read twice" in result
    assert "MORNING calendar" in result


def test_refused_write_leaves_the_good_morning_column_intact(tmp_path):
    """The damage was a silent overwrite, so refusing must also be a no-op."""
    _save(tmp_path, "morning", MORNING)
    _save(tmp_path, "afternoon", AFTERNOON)

    _save(tmp_path, "morning", AFTERNOON)

    stored = _stored(tmp_path)
    assert stored["2026-09-08"]["morning"] == \
        "1/4 cup Triscuits; 1/2 cup strawberries"
    assert stored["2026-09-08"]["afternoon"] == "1 bag granola bites; 1/2 banana"


def test_guard_ignores_case_and_spacing(tmp_path):
    """The two extractions were not byte-identical.

    The same model re-reading the same photo produced "Club Crackers" once and
    "Club crackers" the other time, so an equality check on the raw strings
    would have let the write through.
    """
    _save(tmp_path, "afternoon", AFTERNOON)
    noisy = {d: v.upper().replace("; ", ";  ") for d, v in AFTERNOON.items()}

    assert _save(tmp_path, "morning", noisy).startswith("❌")


# ── What must still go through ───────────────────────────────────────────────

def test_first_save_of_a_month_is_allowed(tmp_path):
    """Nothing to collide with — the other column is empty."""
    assert _save(tmp_path, "morning", MORNING).startswith("✅")


def test_the_real_second_photo_is_allowed(tmp_path):
    """16:48:38, the call that was correct. The guard must not block it."""
    _save(tmp_path, "morning", MORNING)

    result = _save(tmp_path, "afternoon", AFTERNOON)

    assert result.startswith("✅")
    assert _stored(tmp_path)["2026-09-09"]["afternoon"].startswith("Popcorn")


def test_resaving_the_same_column_is_allowed(tmp_path):
    """A corrective re-read compares against the OTHER column, not itself."""
    _save(tmp_path, "morning", MORNING)
    _save(tmp_path, "afternoon", AFTERNOON)

    assert _save(tmp_path, "morning", MORNING).startswith("✅")


def test_two_genuinely_shared_days_pass_with_a_warning(tmp_path):
    """A school can repeat one item; it cannot repeat the whole month."""
    _save(tmp_path, "afternoon", AFTERNOON)
    mostly_different = dict(MORNING)
    mostly_different[1] = AFTERNOON[1]
    mostly_different[2] = AFTERNOON[2]

    result = _save(tmp_path, "morning", mostly_different)

    assert result.startswith("✅")
    assert "2 day(s) have identical" in result


def test_closed_days_do_not_count_as_collisions(tmp_path):
    """"No School - Labor Day" legitimately reads the same in both columns."""
    with patch.object(tools, "SKILL_DIR", str(tmp_path)):
        tools.save_snack_schedule(
            month=9, year=2026, type="afternoon",
            days=[{"day": 7, "afternoon": "No School - Labor Day",
                   "school_closed": True}])
        result = tools.save_snack_schedule(
            month=9, year=2026, type="morning",
            days=[{"day": 7, "morning": "No School - Labor Day",
                   "school_closed": True}])

    assert result.startswith("✅")


def test_force_overrides_the_guard(tmp_path):
    _save(tmp_path, "afternoon", AFTERNOON)

    result = _save(tmp_path, "morning", AFTERNOON, force=True)

    assert result.startswith("✅")
    assert _stored(tmp_path)["2026-09-08"]["morning"] == AFTERNOON[8]


# ── The latent bug on the same line ──────────────────────────────────────────

def test_an_unrecognised_type_is_rejected_not_treated_as_afternoon(tmp_path):
    """`if type == "morning": ... else: afternoon` made every typo an afternoon
    write — "Morning", "am", "pm", a mis-guessed kwarg. The free-tier model
    guessed this tool's signature wrong three times in the same session."""
    with patch.object(tools, "SKILL_DIR", str(tmp_path)):
        result = tools.save_snack_schedule(
            month=9, year=2026, type="Morning",
            days=[{"day": 8, "morning": "1/4 cup Triscuits"}])

    assert result.startswith("❌")
    assert not (tmp_path / "household" / "snack_schedule.json").exists()
