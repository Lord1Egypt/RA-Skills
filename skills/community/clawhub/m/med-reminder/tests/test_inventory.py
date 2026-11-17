"""
PR 8b (#10): derived inventory — restocked/counted events minus effective
taken doses, days of supply, the reorder flag, and the restock command.
"""
import datetime as dtmod

import pytest

import event_store
import inventory as inv
import safe_write as sw
from clock import FakeClock
from occurrence import at_local
from reply import (handle_confirm, handle_restock,
                   handle_status, handle_undo)
from tests.conftest import TZ, local_dt, make_med, make_state, make_tick_env, utc

TUE = dtmod.date(2026, 4, 21)


@pytest.fixture
def env(tmp_path, monkeypatch):
    return make_tick_env(tmp_path, monkeypatch)


def tablets(**kw):
    med = make_med(dose="2", unit="tablet", times=kw.pop("times", ["08:00", "20:00"]),
                   frequency="twice_daily", **kw)
    med["inventory_unit"] = "tablet"
    return med


def ev(kind, h, m=0, med_id="med-001", day=0, **fields):
    return event_store.new_event(med_id, kind, utc(local_dt(h, m) + dtmod.timedelta(days=day)),
                                 **fields)


def taken(h, m=0, day=0, dose_taken=None, med_id="med-001"):
    t = utc(local_dt(h, m) + dtmod.timedelta(days=day))
    return event_store.new_event(med_id, "taken", t, taken_at_utc=t.isoformat(),
                                 dose_taken=dose_taken)


NOW = utc(local_dt(23, 0))


# ── amounts ───────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("text,expected", [
    ("10units", (10.0, "units")), ("10 units", (10.0, "units")),
    ("250mcg", (250.0, "mcg")), ("0.25 mg", (0.25, "mg")), ("2", (2.0, None)),
    ("1 tablet", (1.0, "tablet")), ("3 tabs", (3.0, "tablet")),
    ("half", None), ("", None), ("0", None), ("-1mg", None),
])
def test_parse_amount(text, expected):
    assert inv.parse_amount(text) == expected


@pytest.mark.parametrize("med,taken,scale", [
    ({"dose": "15", "unit": "units"}, "10 units", 10 / 15),
    ({"dose": "250", "unit": "mcg"}, "0.125mg", 0.5),
    ({"dose": "2", "unit": "tablet"}, "1", 0.5),
    ({"dose": "2", "unit": "tablet"}, None, 1.0),
    ({"dose": "2", "unit": "tablet"}, "a bit", 1.0),     # not comparable → full
    ({"dose": "500", "unit": "mg"}, "1 tablet", 1.0),
])
def test_taken_scale(med, taken, scale):
    assert inv.taken_scale(med, taken) == pytest.approx(scale)


# ── what a dose consumes ──────────────────────────────────────────────────────

def test_per_dose_same_unit():
    assert inv.per_dose(tablets(), []) == 2


def test_per_dose_explicit_wins():
    med = tablets(); med["doses_per_unit"] = 30
    assert inv.per_dose(med, []) == pytest.approx(1 / 30)


def test_per_dose_syringe_units_in_ml():
    # issue #10's example: T at 15 units daily from a 20 mL vial ≈ 133 doses
    med = make_med(dose="15", unit="units"); med["inventory_unit"] = "mL"
    assert inv.per_dose(med, []) == pytest.approx(0.15)
    med["syringe"] = "U-50"
    assert inv.per_dose(med, []) == pytest.approx(0.3)


def test_per_dose_from_vial_mix():
    med = make_med(dose="250", unit="mcg"); med["inventory_unit"] = "vial"
    assert inv.per_dose(med, []) is None                  # no mix logged yet
    mix = ev("reconstituted", 7, vial_mg=10, diluent_ml=2)
    assert inv.per_dose(med, [mix]) == pytest.approx(0.025)   # 40 doses / vial


def test_untracked_med_has_no_line():
    assert inv.status_line(make_med(), [ev("restocked", 7, qty=5)], NOW) is None


# ── on hand ───────────────────────────────────────────────────────────────────

def test_restock_minus_taken():
    events = [ev("restocked", 7, qty=60), taken(8, 5), taken(20, 5)]
    assert inv.on_hand(tablets(), events, NOW) == 56


def test_doses_before_tracking_started_dont_count():
    events = [taken(8, 5), ev("restocked", 9, qty=60), taken(20, 5)]
    assert inv.on_hand(tablets(), events, NOW) == 58


def test_undone_dose_restores_stock():
    t = taken(8, 5)
    undo = ev("undone", 8, 30, ref=t["id"])
    events = [ev("restocked", 7, qty=60), t, undo]
    assert inv.on_hand(tablets(), events, NOW) == 60


def test_partial_dose_consumes_its_share():
    events = [ev("restocked", 7, qty=60), taken(8, 5, dose_taken="1 tablet")]
    assert inv.on_hand(tablets(), events, NOW) == 59


def test_skipped_and_missed_consume_nothing():
    occ = at_local(TUE, "08:00", TZ)
    events = [ev("restocked", 7, qty=60),
              event_store.new_event("med-001", "skipped", utc(local_dt(8, 5)), occurrence=occ),
              event_store.new_event("med-001", "missed", utc(local_dt(21)),
                                    occurrence=at_local(TUE, "20:00", TZ))]
    assert inv.on_hand(tablets(), events, NOW) == 60


def test_count_resets_the_baseline():
    events = [ev("restocked", 6, qty=60), taken(8, 5),
              ev("counted", 12, qty=40),                   # a recount: 40 on hand
              ev("restocked", 13, qty=10), taken(20, 5)]
    assert inv.on_hand(tablets(), events, NOW) == 48


def test_remix_changes_consumption_from_then_on():
    med = make_med(dose="250", unit="mcg", times=["08:00", "20:00"],
                   frequency="twice_daily")
    med["inventory_unit"] = "vial"
    events = [ev("reconstituted", 7, vial_mg=10, diluent_ml=2),
              ev("restocked", 7, qty=2),
              taken(8, 5),                                 # 1/40 vial
              ev("reconstituted", 12, vial_mg=5, diluent_ml=2),
              taken(20, 5)]                                # 1/20 vial
    assert inv.on_hand(med, events, NOW) == pytest.approx(2 - 0.025 - 0.05)


# ── days of supply, reorder ───────────────────────────────────────────────────

def test_days_left_and_line():
    events = [ev("restocked", 7, qty=60)]
    med = tablets()                                        # 4 tablets / day
    assert inv.days_left(med, events, NOW) == pytest.approx(15)
    assert inv.status_line(med, events, NOW) == "~60 tablets left (~15 days)"


def test_reorder_flag_below_threshold():
    med = tablets(); med["reorder_when_below_days"] = 20
    line = inv.status_line(med, [ev("restocked", 7, qty=60)], NOW)
    assert line.endswith("— reorder")


def test_weekly_and_interval_rates():
    assert inv.doses_per_day(make_med(frequency="weekly", times=["08:00"],
                                      day_of_week=["tue", "sat"])) == pytest.approx(2 / 7)
    assert inv.doses_per_day(make_med(frequency="interval", interval_hours=6)) == 4
    assert inv.doses_per_day(make_med(frequency="as_needed")) is None


def test_out_of_stock():
    events = [ev("restocked", 7, qty=2), taken(8, 5)]
    assert inv.status_line(tablets(), events, NOW) == "out of tablets — restock"


def test_cant_cost_a_dose_asks_for_doses_per_unit():
    med = make_med(dose="500", unit="mg"); med["inventory_unit"] = "bottle"
    assert "set doses_per_unit" in inv.status_line(med, [ev("restocked", 7, qty=1)], NOW)


# ── validation ────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("field,value", [
    ("inventory_unit", ""), ("inventory_unit", 3),
    ("doses_per_unit", 0), ("doses_per_unit", "30"), ("doses_per_unit", True),
    ("reorder_when_below_days", 0), ("reorder_when_below_days", 2.5),
])
def test_bad_inventory_fields_rejected(field, value):
    med = tablets(); med[field] = value
    with pytest.raises(ValueError):
        sw.validate(make_state(meds=[med]))


def test_good_inventory_fields_validate():
    med = tablets(); med["doses_per_unit"] = 30; med["reorder_when_below_days"] = 14
    sw.validate(make_state(meds=[med]))


# ── reply restock / status / digest ───────────────────────────────────────────

def test_restock_command_and_echo(env, capsys):
    env.write(meds=[tablets()])
    handle_restock("med-001", 60, None, dry_run=False, clock=FakeClock(local_dt(7)))
    out = capsys.readouterr().out
    assert "Added 60 tablet for Metformin. Now ~60 tablets left (~15 days)." in out
    assert env.events("restocked")[0]["qty"] == 60


def test_set_records_a_count(env, capsys):
    env.write(meds=[tablets()])
    handle_restock("med-001", None, 12, dry_run=False, clock=FakeClock(local_dt(7)))
    assert env.events("counted")[0]["qty"] == 12
    assert "Recorded 12 tablet on hand" in capsys.readouterr().out


@pytest.mark.parametrize("qty,set_qty", [(None, None), (5, 5), (0, None), (-1, None),
                                         (None, -1), (float("nan"), None)])
def test_restock_rejects_bad_arguments(env, qty, set_qty):
    env.write(meds=[tablets()])
    with pytest.raises(SystemExit):
        handle_restock("med-001", qty, set_qty, dry_run=False, clock=FakeClock(local_dt(7)))
    assert env.events("restocked") == [] and env.events("counted") == []


def test_restock_needs_an_inventory_unit(env, capsys):
    env.write(meds=[make_med()])
    with pytest.raises(SystemExit):
        handle_restock("med-001", 5, None, dry_run=False, clock=FakeClock(local_dt(7)))
    assert "inventory_unit" in capsys.readouterr().out


def test_confirm_and_undo_flow_through(env):
    env.write(meds=[tablets()])
    handle_restock("med-001", 10, None, dry_run=False, clock=FakeClock(local_dt(7)))
    handle_confirm("med-001", None, dry_run=False, clock=FakeClock(local_dt(8, 5)))
    med = env.state()["meds"][0]
    assert inv.on_hand(med, env.events(), utc(local_dt(8, 10))) == 8
    handle_undo("med-001", dry_run=False, clock=FakeClock(local_dt(8, 10)))
    assert inv.on_hand(med, env.events(), utc(local_dt(8, 20))) == 10


def test_status_shows_supplies(env, capsys, monkeypatch):
    env.write(meds=[tablets()])
    handle_restock("med-001", 60, None, dry_run=False, clock=FakeClock(local_dt(7)))
    monkeypatch.setenv("MEDS_TEST", "1")
    monkeypatch.setenv("MEDS_FAKE_NOW", "2026-04-21T07:30:00-07:00")
    capsys.readouterr()
    handle_status()
    assert "| ~60 tablets left (~15 days)" in capsys.readouterr().out


def test_digest_lists_supplies(env):
    med = tablets(); med["reorder_when_below_days"] = 20
    env.write(meds=[med], digest_time="07:30")
    env.run(local_dt(7, 0))
    handle_restock("med-001", 60, None, dry_run=False, clock=FakeClock(local_dt(7, 10)))
    env.run(local_dt(7, 35))
    digest = [m for m in env.sent() if m.startswith("Meds for")][0]
    assert "Supplies:\nMetformin: ~60 tablets left (~15 days) — reorder" in digest


def test_digest_has_no_supplies_section_without_tracking(env):
    env.write(meds=[make_med()], digest_time="07:30")
    env.run(local_dt(7, 0))
    env.run(local_dt(7, 35))
    assert "Supplies" not in [m for m in env.sent() if m.startswith("Meds for")][0]
