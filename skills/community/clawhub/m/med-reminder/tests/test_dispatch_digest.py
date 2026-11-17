"""
Digest tests against the tick engine (issue #1 §3.7 — the digest is a
stage keyed by local date: once/day, skipped if more than 4h late).
"""
import datetime as dtmod
from datetime import timedelta

import event_store
from occurrence import at_local, at_utc
from tests.conftest import local_dt, make_med, make_tick_env, TZ, utc

import pytest

TUE = dtmod.date(2026, 4, 21)


@pytest.fixture
def env(tmp_path, monkeypatch):
    return make_tick_env(tmp_path, monkeypatch)


def digest_msgs(env):
    return [m for m in env.sent() if "Meds for" in m]


def test_digest_sent_at_first_tick_after_digest_time(env):
    env.write(meds=[make_med(med_id="med-001", frequency="once_daily",
                             times=["08:00"])],
              digest_time="07:30")
    env.run(local_dt(7, 0))
    env.run(local_dt(7, 32))
    msgs = digest_msgs(env)
    assert len(msgs) == 1
    assert "Metformin 500mg | 8:00am" in msgs[0]


def test_digest_once_per_local_date(env):
    env.write(meds=[make_med(med_id="med-001", frequency="once_daily",
                             times=["08:00"])],
              digest_time="07:30")
    env.run(local_dt(7, 0))
    env.run(local_dt(7, 32))
    env.run(local_dt(9, 0))
    env.run(local_dt(11, 0))
    assert len(digest_msgs(env)) == 1


def test_digest_skipped_when_more_than_4h_late(env):
    env.write(meds=[make_med(med_id="med-001", frequency="once_daily",
                             times=["20:00"])],
              digest_time="08:00")
    env.run(local_dt(7, 0))
    env.run(local_dt(12, 30))               # 4.5h after digest_time
    assert digest_msgs(env) == []


def test_digest_lists_active_meds_and_excludes_paused(env):
    met = make_med(med_id="med-001", name="Metformin", frequency="once_daily",
                   times=["08:00"])
    lis = make_med(med_id="med-002", name="Lisinopril", paused=True,
                   frequency="once_daily", times=["21:00"])
    env.write(meds=[met, lis], digest_time="07:30")
    env.run(local_dt(7, 0))
    env.run(local_dt(7, 32))
    msg = digest_msgs(env)[0]
    assert "Metformin" in msg and "Lisinopril" not in msg


def test_as_needed_med_shown_in_digest(env):
    env.write(meds=[make_med(med_id="med-001", name="Ibuprofen",
                             frequency="as_needed")],
              digest_time="07:30")
    env.run(local_dt(7, 0))
    env.run(local_dt(7, 32))
    msg = digest_msgs(env)[0]
    assert "Ibuprofen" in msg and "as needed" in msg


def test_digest_lists_weekly_day(env):
    env.write(meds=[make_med(med_id="med-001", frequency="weekly",
                             times=["09:00"], day_of_week="mon")],
              digest_time="07:30")
    monday = dtmod.timedelta(days=-1)              # Mon Apr 20 — its day
    env.run(local_dt(7, 0) + monday)
    env.run(local_dt(7, 32) + monday)
    assert "Mon 9:00am" in digest_msgs(env)[0]


def test_digest_adherence_from_history_store(env):
    # 3 taken + 1 missed in the last 7 days; one taken-overrides-missed pair
    med = make_med(med_id="med-001", frequency="once_daily", times=["08:00"])
    env.write(meds=[med], digest_time="07:30")
    evs = []
    for days_ago in (1, 2, 6):
        day = TUE - dtmod.timedelta(days=days_ago)
        occ = at_local(day, "08:00", TZ, 0)
        evs.append(event_store.new_event(
            "med-001", "taken", local_dt(8, 10) - dtmod.timedelta(days=days_ago),
            occurrence=occ, taken_at_utc=utc(local_dt(8, 10) - dtmod.timedelta(days=days_ago)).isoformat()))
    day3 = TUE - dtmod.timedelta(days=3)
    occ3 = at_local(day3, "08:00", TZ, 0)
    evs.append(event_store.new_event("med-001", "missed", local_dt(9, 30) - dtmod.timedelta(days=3), occurrence=occ3))
    evs.append(event_store.new_event("med-001", "taken", local_dt(10, 0) - dtmod.timedelta(days=3),
                                     occurrence=occ3))     # late taken overrides
    evs.append(event_store.new_event("med-001", "missed", local_dt(9, 30) - dtmod.timedelta(days=5),
                                     occurrence=at_local(TUE - dtmod.timedelta(days=5), "08:00", TZ, 0)))
    env.seed(evs)
    env.run(local_dt(7, 0))
    env.run(local_dt(7, 32))
    msg = digest_msgs(env)[0]
    # taken late counts as taken: 4 taken of 5 (the 5-days-ago miss is
    # outside the 7-day window anchored at the 07:32 digest… 5 days is
    # inside; 6-days-ago taken is inside too)
    assert "Last 7 days: 4/5 doses taken" in msg


def test_digest_adherence_ignores_undone_doses(env):
    # yesterday: taken then undone, then logged missed (generation 1);
    # 2 days ago: skipped then undone, then taken — the undone events must
    # not count, so 1 taken of 2
    med = make_med(med_id="med-001", frequency="once_daily", times=["08:00"])
    env.write(meds=[med], digest_time="07:30")
    d1 = dtmod.timedelta(days=1)
    d2 = dtmod.timedelta(days=2)
    occ1 = at_local(TUE - d1, "08:00", TZ, 0)
    occ2 = at_local(TUE - d2, "08:00", TZ, 0)
    taken1 = event_store.new_event("med-001", "taken", local_dt(8, 10) - d1,
                                   occurrence=occ1, generation=0)
    skipped2 = event_store.new_event("med-001", "skipped", local_dt(8, 10) - d2,
                                     occurrence=occ2, generation=0)
    env.seed([
        taken1,
        event_store.new_event("med-001", "undone", local_dt(8, 20) - d1,
                              occurrence=occ1, generation=0, ref=taken1["id"]),
        event_store.new_event("med-001", "missed", local_dt(20, 0) - d1,
                              occurrence=occ1, generation=1),
        skipped2,
        event_store.new_event("med-001", "undone", local_dt(8, 20) - d2,
                              occurrence=occ2, generation=0, ref=skipped2["id"]),
        event_store.new_event("med-001", "taken", local_dt(9, 0) - d2,
                              occurrence=occ2, generation=1),
    ])
    env.run(local_dt(7, 0))
    env.run(local_dt(7, 32))
    msg = digest_msgs(env)[0]
    assert "Last 7 days: 1/2 doses taken" in msg
    assert "skipped" not in msg


def test_digest_adherence_omitted_without_events(env):
    env.write(meds=[make_med(med_id="med-001", frequency="once_daily",
                             times=["08:00"])],
              digest_time="07:30")
    env.run(local_dt(7, 0))
    env.run(local_dt(7, 32))
    assert "Last 7 days" not in digest_msgs(env)[0]


def test_globally_paused_skips_digest(env):
    env.write(meds=[make_med(med_id="med-001", frequency="once_daily",
                             times=["08:00"])],
              digest_time="07:30", paused=True)
    env.run(local_dt(7, 0))
    env.run(local_dt(7, 32))
    assert digest_msgs(env) == []
    assert env.sent() == []


def test_empty_meds_no_digest(env):
    env.write(meds=[], digest_time="07:30")
    env.run(local_dt(7, 0))
    env.run(local_dt(7, 32))
    assert env.sent() == []


# ── weekly meds only on their days ────────────────────────────────────────────

def weekly_and_daily():
    return [make_med(med_id="med-001", name="MOTS-c", frequency="weekly",
                     times=["08:00"], day_of_week=["tue", "sat"]),
            make_med(med_id="med-002", name="Ipamorelin", frequency="weekly",
                     times=["19:00"], day_of_week=["mon", "tue", "wed", "thu", "fri"]),
            make_med(med_id="med-003", name="T", frequency="once_daily", times=["08:00"])]


def digest_on(env, day_offset):
    d = dtmod.timedelta(days=day_offset)
    env.run(local_dt(7, 0) + d)
    env.run(local_dt(7, 32) + d)
    return digest_msgs(env)[-1]


def test_digest_skips_weekly_meds_on_their_off_days(env):
    env.write(meds=weekly_and_daily(), digest_time="07:30")
    friday = digest_on(env, 3)                       # Fri Apr 24
    assert "MOTS-c" not in friday
    assert "1. Ipamorelin" in friday and "2. T " in friday


def test_digest_lists_weekly_meds_on_their_days(env):
    env.write(meds=weekly_and_daily(), digest_time="07:30")
    tuesday = digest_on(env, 0)                      # Tue Apr 21
    assert "1. MOTS-c" in tuesday and "2. Ipamorelin" in tuesday and "3. T " in tuesday
    saturday = digest_on(env, 4)                     # Sat Apr 25
    assert "1. MOTS-c" in saturday and "Ipamorelin" not in saturday


def test_position_order_matches_the_listed_meds(env):
    env.write(meds=weekly_and_daily(), digest_time="07:30")
    digest_on(env, 3)
    assert env.state()["global"]["last_digest_order"] == ["med-002", "med-003"]


def test_off_day_med_keeps_its_supplies_line(env):
    meds = weekly_and_daily()
    meds[0]["inventory_unit"] = "vial"
    meds[0]["doses_per_unit"] = 10
    env.write(meds=meds, digest_time="07:30")
    env.seed([event_store.new_event("med-001", "restocked",
                                    local_dt(6, 0) + dtmod.timedelta(days=3), qty=2)])
    friday = digest_on(env, 3)
    assert "Supplies:\nMOTS-c: ~2 vials left" in friday
    assert "1. MOTS-c" not in friday
