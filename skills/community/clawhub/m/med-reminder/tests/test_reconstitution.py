"""
PR 8a — reconstitution calculator (#10): the unit math, the `reconstituted`
event, `reply.py reconstitute`, and the units line in reminders, nudges and
the confirm echo.
"""
import json
from datetime import timedelta

import pytest

import event_store
import reconstitution as rc
import safe_write as sw
from clock import FakeClock
from reply import handle_confirm, handle_reconstitute
from tests.conftest import local_dt, make_med, make_state, make_tick_env, utc


def peptide(**kw):
    kw.setdefault("name", "Wolverine")
    kw.setdefault("med_type", "injection")
    kw.setdefault("dose", "250")
    kw.setdefault("unit", "mcg")
    return make_med(**kw)


# ── Math (issue #10 correction 1 + 2) ─────────────────────────────────────────

def test_u100_worked_example():
    d = rc.compute(250, vial_mg=5, diluent_ml=2)
    assert d.conc_mg_per_ml == 2.5
    assert d.volume_ml == pytest.approx(0.1)
    assert d.exact_units == 10 and d.units == 10
    assert d.doses_per_vial == pytest.approx(20)
    assert d.warnings == ()
    assert rc.units_phrase(d) == "10 units"


def test_u50_is_half_the_units_of_u100():
    d = rc.compute(250, vial_mg=5, diluent_ml=2, syringe="U-50")
    assert d.units == 5 and d.volume_ml == pytest.approx(0.1)


def test_mg_dose_converts_to_mcg():
    assert rc.dose_mcg({"dose": "0.25", "unit": "mg"}) == 250
    assert rc.dose_mcg({"dose": "250", "unit": "MCG"}) == 250
    assert rc.dose_mcg({"dose": "250", "unit": "µg"}) == 250


@pytest.mark.parametrize("med", [
    {"dose": "15", "unit": "units"},
    {"dose": "1", "unit": "tablet"},
    {"dose": "abc", "unit": "mcg"},
    {"dose": "0", "unit": "mcg"},
    {"dose": "-5", "unit": "mg"},
    {"dose": "nan", "unit": "mg"},
])
def test_non_mass_or_bad_dose_has_no_mcg(med):
    assert rc.dose_mcg(med) is None


def test_rounding_over_5_percent_warns_and_shows_exact():
    d = rc.compute(320, vial_mg=10, diluent_ml=2)        # 6.4 units
    assert d.units == 6
    assert rc.units_phrase(d) == "6 units (exact 6.4)"
    assert any("off the exact 6.4" in w for w in d.warnings)


def test_small_rounding_shows_exact_without_warning():
    d = rc.compute(2030, vial_mg=10, diluent_ml=2)       # 40.6 units
    assert d.units == 41
    assert rc.units_phrase(d) == "41 units (exact 40.6)"
    assert d.warnings == ()


def test_half_unit_rounds_up():
    assert rc.compute(250, vial_mg=10, diluent_ml=3).units == 8   # 7.5


def test_volume_over_half_syringe_warns():
    d = rc.compute(3000, vial_mg=5, diluent_ml=1)        # 0.6 mL
    assert any("more than half a 1 mL syringe" in w for w in d.warnings)


def test_below_one_unit_warns():
    d = rc.compute(10, vial_mg=10, diluent_ml=1)          # 0.1 units
    assert d.units == 0
    assert any("too small to measure" in w for w in d.warnings)


def test_mg_mcg_transposition_shows_in_doses_per_vial():
    # vial entered as 5000 "mg" when it was 5000 mcg: the sanity number explodes
    assert rc.compute(250, vial_mg=5000, diluent_ml=2).doses_per_vial == pytest.approx(20000)


# ── current_mix (event-based, latest wins) ────────────────────────────────────

def _mix(med_id, ts, vial, dil):
    return event_store.new_event(med_id, "reconstituted", ts,
                                 vial_mg=vial, diluent_ml=dil)


def test_current_mix_latest_at_or_before():
    a = _mix("med-001", utc(local_dt(8)), 5, 2)
    b = _mix("med-001", utc(local_dt(12)), 10, 2)
    other = _mix("med-002", utc(local_dt(13)), 1, 1)
    evs = [a, b, other]
    assert rc.current_mix(evs, "med-001")["vial_mg"] == 10
    assert rc.current_mix(evs, "med-001", at=utc(local_dt(9)))["vial_mg"] == 5
    assert rc.current_mix(evs, "med-001", at=utc(local_dt(7))) is None


def test_med_draw_uses_med_syringe():
    med = peptide(); med["syringe"] = "U-50"
    d = rc.med_draw(med, [_mix("med-001", utc(local_dt(8)), 5, 2)])
    assert d.units == 5 and d.syringe == "U-50"


@pytest.mark.parametrize("bad", [
    {"vial_mg": 0, "diluent_ml": 2},
    {"vial_mg": 5, "diluent_ml": 0},
    {"vial_mg": "x", "diluent_ml": 2},
    {"diluent_ml": 2},
])
def test_malformed_mix_falls_back_to_plain_dose(bad):
    ev = {"id": "x", "ts_utc": "2026-04-21T14:00:00+00:00", "med_id": "med-001",
          "event": "reconstituted", **bad}
    assert rc.med_draw(peptide(), [ev]) is None


def test_malformed_mix_never_blocks_the_reminder(env):
    env.write(meds=[peptide(times=["08:00"])])
    env.run(local_dt(7))
    env.seed([{"id": "bad-mix", "ts_utc": utc(local_dt(7, 30)).isoformat(),
               "med_id": "med-001", "event": "reconstituted",
               "vial_mg": 0, "diluent_ml": 2}])
    env.run(local_dt(8, 1))
    assert env.sent() == ["Reminder: Wolverine 250mcg"]


def test_new_event_carries_mix_fields():
    e = _mix("med-001", utc(local_dt(8)), 5, 2)
    assert e["event"] == "reconstituted"
    assert e["vial_mg"] == 5 and e["diluent_ml"] == 2


# ── Validation: syringe field ─────────────────────────────────────────────────

def test_syringe_validates():
    med = peptide(); med["syringe"] = "U-50"
    sw.validate(make_state(meds=[med]))
    med["syringe"] = "U-40"
    with pytest.raises((ValueError, SystemExit)):
        sw.validate(make_state(meds=[med]))


# ── reply.py reconstitute ─────────────────────────────────────────────────────

@pytest.fixture
def env(tmp_path, monkeypatch):
    return make_tick_env(tmp_path, monkeypatch)


def test_reconstitute_logs_event_and_prints_sanity(env, capsys):
    env.write(meds=[peptide()])
    handle_reconstitute("med-001", 5, 2, dry_run=False, clock=FakeClock(local_dt(7)))
    out = capsys.readouterr().out
    assert "5 mg in 2 mL = 2.5 mg/mL" in out
    assert "250mcg = 10 units on your U-100" in out
    assert "about 20 doses" in out
    ev = env.events("reconstituted")
    assert len(ev) == 1 and ev[0]["vial_mg"] == 5 and ev[0]["diluent_ml"] == 2


def test_reconstitute_prints_warnings(env, capsys):
    env.write(meds=[peptide(dose="320")])
    handle_reconstitute("med-001", 10, 2, dry_run=False, clock=FakeClock(local_dt(7)))
    assert "off the exact 6.4" in capsys.readouterr().out


def test_reconstitute_dry_run_writes_nothing(env, capsys):
    env.write(meds=[peptide()])
    handle_reconstitute("med-001", 5, 2, dry_run=True, clock=FakeClock(local_dt(7)))
    assert "[DRY RUN]" in capsys.readouterr().out
    assert env.events("reconstituted") == []


def test_reconstitute_refuses_non_mass_dose(env, capsys):
    env.write(meds=[make_med(dose="15", unit="units")])
    with pytest.raises(SystemExit):
        handle_reconstitute("med-001", 5, 2, dry_run=False, clock=FakeClock(local_dt(7)))
    assert "mcg or mg" in capsys.readouterr().out
    assert env.events("reconstituted") == []


@pytest.mark.parametrize("vial,dil", [(0, 2), (5, 0), (-1, 2), (float("nan"), 2)])
def test_reconstitute_refuses_bad_amounts(env, vial, dil):
    env.write(meds=[peptide()])
    with pytest.raises(SystemExit):
        handle_reconstitute("med-001", vial, dil, dry_run=False, clock=FakeClock(local_dt(7)))
    assert env.events("reconstituted") == []


def test_reconstitute_refuses_dose_bigger_than_vial(env, capsys):
    env.write(meds=[peptide(dose="6", unit="mg")])
    with pytest.raises(SystemExit):
        handle_reconstitute("med-001", 5, 2, dry_run=False, clock=FakeClock(local_dt(7)))
    assert "more than the whole vial" in capsys.readouterr().out


# ── Units in reminder, nudge, confirm echo ────────────────────────────────────

def test_reminder_and_nudge_carry_units(env):
    env.write(meds=[peptide(times=["08:00"])])
    handle_reconstitute("med-001", 5, 2, dry_run=False, clock=FakeClock(local_dt(7)))
    env.run(local_dt(8, 1))
    env.run(local_dt(8, 31))
    sent = env.sent()
    assert any(m.startswith("Reminder: Wolverine 250mcg = 10 units on your U-100")
               for m in sent)
    assert any(m.startswith("Late:") and "250mcg = 10 units on your U-100" in m
               for m in sent)


def test_reminder_without_mix_is_unchanged(env):
    env.write(meds=[peptide(times=["08:00"])])
    env.run(local_dt(7))          # first tick sets the watermark
    env.run(local_dt(8, 1))
    assert env.sent() == ["Reminder: Wolverine 250mcg"]


def test_remix_changes_units(env):
    env.write(meds=[peptide(times=["08:00"])])
    handle_reconstitute("med-001", 5, 2, dry_run=False, clock=FakeClock(local_dt(6)))
    handle_reconstitute("med-001", 10, 2, dry_run=False, clock=FakeClock(local_dt(7)))
    env.run(local_dt(8, 1))
    assert "= 5 units on your U-100" in env.sent()[0]


def test_confirm_echo_shows_units(env, capsys):
    env.write(meds=[peptide(times=["08:00"])])
    handle_reconstitute("med-001", 5, 2, dry_run=False, clock=FakeClock(local_dt(7)))
    capsys.readouterr()
    handle_confirm("med-001", None, dry_run=False, clock=FakeClock(local_dt(8, 5)))
    assert "Wolverine 250mcg (10 units)." in capsys.readouterr().out


def test_confirm_echo_with_different_dose_has_no_units(env, capsys):
    env.write(meds=[peptide(times=["08:00"])])
    handle_reconstitute("med-001", 5, 2, dry_run=False, clock=FakeClock(local_dt(7)))
    capsys.readouterr()
    handle_confirm("med-001", "200mcg", dry_run=False, clock=FakeClock(local_dt(8, 5)))
    assert "units" not in capsys.readouterr().out


def test_reconstituted_event_does_not_disturb_tick(env):
    """A mix event has no occurrence — outcome/attribution/send index ignore it."""
    env.write(meds=[peptide(times=["08:00"])])
    handle_reconstitute("med-001", 5, 2, dry_run=False, clock=FakeClock(local_dt(8, 2)))
    env.run(local_dt(8, 3))
    handle_confirm("med-001", None, dry_run=False, clock=FakeClock(local_dt(8, 5)))
    env.run(local_dt(10, 0))
    assert env.events("missed") == []
