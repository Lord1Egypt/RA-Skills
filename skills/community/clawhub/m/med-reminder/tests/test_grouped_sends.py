"""
#26: meds due at the same minute get ONE reminder (and one nudge per slot)
listing them all, instead of a message per med. Bookkeeping stays per med:
every med keeps its own send_intent / sent / send_failed events, so
confirms, retries, missed-dose closes and delivery notes work unchanged.
"""
import pytest

from clock import FakeClock
from reply import handle_confirm
from tests.conftest import local_dt, make_med, make_tick_env


@pytest.fixture
def env(tmp_path, monkeypatch):
    return make_tick_env(tmp_path, monkeypatch)


def evening_pair(**kw):
    return [make_med(med_id="med-001", name="Wolverine", dose="4", unit="units",
                     times=["19:00"], **kw),
            make_med(med_id="med-002", name="Ipamorelin", dose="200", unit="mcg",
                     times=["19:00"], **kw)]


def test_same_minute_reminders_are_one_message(env):
    env.write(meds=evening_pair())
    env.run(local_dt(18, 55))
    env.run(local_dt(19, 1))
    assert env.sent() == ["Reminder — your 7:00pm meds:\n"
                          "- Wolverine 4units\n"
                          "- Ipamorelin 200mcg"]
    # each med still has its own intent and delivery record
    intents = env.events("send_intent")
    assert sorted(e["med_id"] for e in intents) == ["med-001", "med-002"]
    assert sorted(e["med_id"] for e in env.events("sent")) == ["med-001", "med-002"]


def test_nudges_are_grouped_too(env):
    env.write(meds=evening_pair())
    env.run(local_dt(18, 55))
    env.run(local_dt(19, 1))
    env.run(local_dt(19, 31))
    assert env.sent()[-1] == ("Still to take — your 7:00pm meds:\n"
                              "- Wolverine 4units\n"
                              "- Ipamorelin 200mcg")
    assert len(env.sent()) == 2


def test_confirmed_med_drops_out_of_the_next_nudge(env):
    env.write(meds=evening_pair())
    env.run(local_dt(18, 55))
    env.run(local_dt(19, 1))
    handle_confirm("med-001", None, dry_run=False, clock=FakeClock(local_dt(19, 10)))
    env.run(local_dt(19, 31))
    last = env.sent()[-1]
    assert "Wolverine" not in last
    assert last.startswith("Late: Ipamorelin")      # a lone med keeps its own text
    assert len(env.sent()) == 2


def test_different_minutes_stay_separate(env):
    meds = evening_pair()
    meds[1]["schedule"]["times"] = ["19:15"]
    env.write(meds=meds)
    env.run(local_dt(18, 55))
    env.run(local_dt(19, 20))                        # both reminders due this tick
    assert sorted(m.split(":")[1].split()[0] for m in env.sent()) == ["Ipamorelin", "Wolverine"]
    assert all(m.startswith("Reminder: ") for m in env.sent())


def test_group_lists_food_units_and_warnings(env):
    meds = evening_pair(with_food=True, notes="after dinner")
    env.write(meds=meds)
    env.run(local_dt(18, 55))
    env.run(local_dt(19, 1))
    msg = env.sent()[0]
    assert "- Wolverine 4units — take with food\n  after dinner" in msg
    assert "- Ipamorelin 200mcg — take with food\n  after dinner" in msg


def test_failed_group_is_recorded_for_every_member_and_retried_together(env):
    env.write(meds=evening_pair())
    env.run(local_dt(18, 55))
    env.fail_sends()
    env.run(local_dt(19, 1))
    failed = env.events("send_failed")
    assert sorted(e["med_id"] for e in failed) == ["med-001", "med-002"]
    env.heal_sends()
    env.run(local_dt(19, 7))                         # backoff over: one retry message
    assert len(env.sent()) == 1
    # (FakeClock stamps the failure at its intent's instant, so the retry
    # carries the "(repeat …)" prefix — the grouping is what's under test)
    assert "Reminder — your 7:00pm meds:\n- Wolverine 4units\n- Ipamorelin 200mcg" \
        in env.sent()[0]
    assert sorted(e["med_id"] for e in env.events("sent")) == ["med-001", "med-002"]


def test_both_confirmed_then_no_nudge(env):
    env.write(meds=evening_pair())
    env.run(local_dt(18, 55))
    env.run(local_dt(19, 1))
    from reply import handle_confirm_all
    handle_confirm_all(None, dry_run=False, clock=FakeClock(local_dt(19, 10)))
    env.run(local_dt(19, 31))
    assert len(env.sent()) == 1
