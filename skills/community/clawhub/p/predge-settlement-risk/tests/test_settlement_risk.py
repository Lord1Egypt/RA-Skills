"""Offline tests on real recorded records (examples/), plus live checks with PREDGE_LIVE=1.

    python -m pytest tests -q                # offline
    PREDGE_LIVE=1 python -m pytest tests -q  # also hits api.predge.io
"""
import json
import os
import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import settlement_risk_check as S  # noqa: E402

EX = {p.stem: json.loads(p.read_text()) for p in (ROOT / "examples").glob("*.json")}
BANNED = re.compile(r"flipped|edited rules|payout", re.I)
LIVE = os.environ.get("PREDGE_LIVE") == "1"


def test_disputed_twice_is_skipped():
    r = EX["disputed-twice-uma-vote"]
    assert r["sent_to_uma_vote"] is True and r["dispute_count"] == 2 and r["open_dispute"] is True
    d = S.settlement_risk_gate(r)
    assert (d.allowed, d.reason, d.size_factor) == (False, "contested_resolution", 0.0)
    assert "88.5 h" in r["recommendation"]


def test_clean_market_is_allowed_full_size():
    r = EX["clean-open-market"]
    assert r["dispute_count"] == 0 and r["risk_level"] == "ok"
    d = S.settlement_risk_gate(r)
    assert (d.allowed, d.size_factor) == (True, 1.0)


def test_proposal_window_is_trimmed():
    d = S.settlement_risk_gate(EX["proposal-in-challenge-window"])
    assert (d.allowed, d.reason, d.size_factor) == (True, "watch", 0.5)


def test_resolved_is_skipped_unless_asked():
    r = EX["resolved-after-two-disputes"]
    assert S.settlement_risk_gate(r).allowed is False
    assert S.settlement_risk_gate(r, block_resolved=False).allowed is True


def test_caution_can_be_trimmed_instead():
    d = S.settlement_risk_gate(EX["disputed-twice-uma-vote"], block_on_caution=False, watch_size_factor=0.25)
    assert (d.allowed, d.size_factor) == (True, 0.25)


def test_fails_closed_without_record():
    d = S.settlement_risk_gate(None)
    assert d.allowed is False and d.reason == "state_unavailable"


def test_signatures_pin_the_published_key():
    for r in EX.values():
        assert r["attestation"]["public_key"] == S.PREDGE_ATTESTATION_KEY
        ok = S.verify_attestation(r)
        assert ok in (True, None)  # None only when no ed25519 library is installed
        tampered = json.loads(json.dumps(r))
        tampered["attestation"]["canonical"] = tampered["attestation"]["canonical"].replace('"caution"', '"ok"').replace('"ok"', '"caution"', 1)
        if ok is True and tampered["attestation"]["canonical"] != r["attestation"]["canonical"]:
            assert S.verify_attestation(tampered) is False


def test_no_banned_wording():
    for r in EX.values():
        assert not BANNED.search(r["recommendation"])
        assert not BANNED.search(json.dumps(r["context"]))


@pytest.mark.skipif(not LIVE, reason="set PREDGE_LIVE=1 to hit api.predge.io")
@pytest.mark.parametrize("market", ["4424722", "will-luiz-incio-lula-da-silva-win-the-2026-brazilian-presidential-election", "555793"])
def test_live(market):
    record, decision = S.check(market)
    assert record is not None and record["risk_level"] in ("ok", "watch", "caution", "resolved")
    assert record["attestation"]["public_key"] == S.PREDGE_ATTESTATION_KEY
    assert S.verify_attestation(record) in (True, None)


@pytest.mark.skipif(not LIVE, reason="set PREDGE_LIVE=1 to hit api.predge.io")
def test_live_bad_input_fails_closed():
    record, decision = S.check("not a market")
    assert record is None and decision.allowed is False
