"""
Predge settlement-risk check for Simmer / Polymarket markets.

Vendor-authored: Predge (https://predge.io) runs the API this skill reads.
The data is UMA's own on-chain state on Polygon; Predge reads it, labels it
and signs the result. Judge accordingly.

This is a template, observe-only gate. It places no orders, real-money or paper.
It answers one question before a strategy enters a Polymarket market: is the
market's resolution contested on chain right now?

    GET https://api.predge.io/v1/settlement-risk/<market>
        <market> = Polymarket condition id (0x + 64 hex), numeric market id or slug

The response says, from UMA's Optimistic Oracle and Polymarket's UMA CTF
adapter on Polygon:
  - whether a dispute is open, and whether the market was disputed twice
    (the outcome then goes to a UMA token-holder vote);
  - the current proposal and when its challenge window ends;
  - each dispute's time, tx and disputed proposal;
  - the latest bulletin-board update (clarification, early-resolution or
    schedule notice) and when it was posted;
  - the on-chain resolution, when there is one;
  - risk_level (ok / watch / caution / resolved) and a one-line recommendation;
  - an ed25519 attestation by Predge's published key.

Pattern (same as simmer-sdk examples/regime_gate_skill.py):
  1. Resolve the market to a Polymarket condition id (a Simmer market id is
     resolved with SimmerClient when SIMMER_API_KEY is set).
  2. Fetch the settlement-risk record.
  3. Run settlement_risk_gate(...). If not allowed, skip. Never fall through.
  4. If allowed, size with your own p_win, scaled by decision.size_factor.

Usage:
    python settlement_risk_check.py --demo                       # offline fixtures, no network
    python settlement_risk_check.py 4424722 601819               # live check, no keys needed
    python settlement_risk_check.py --simmer-market <uuid>       # needs SIMMER_API_KEY
    python settlement_risk_check.py 4424722 --json               # raw record
"""

from __future__ import annotations

import argparse
import json
import os
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Mapping, Optional, Sequence

DEFAULT_BASE_URL = "https://api.predge.io"
# Predge's published attestation key (kid 13fa3d18a369e6c7), listed at
# https://api.predge.io/.well-known/predge-keys.json. Pinned so a response cannot
# vouch for itself with a key it carries.
PREDGE_ATTESTATION_KEY = "13fa3d18a369e6c71bf941563ba47822b30182273d5106a0e8fb61c5016352d9"
SKILL_SLUG = "predge-settlement-risk"
HERE = Path(__file__).resolve().parent


def load_config() -> dict:
    try:
        return json.loads((HERE / "config.json").read_text())
    except (OSError, ValueError):
        return {}


# --------------------------------------------------------------------------- #
# Fetch
# --------------------------------------------------------------------------- #
def _ssl_context() -> ssl.SSLContext:
    """System trust store, or certifi's when installed (python.org builds on macOS ship without one)."""
    try:
        import certifi

        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return ssl.create_default_context()


class SettlementRiskError(RuntimeError):
    """The settlement-risk record could not be read."""


def fetch_settlement_risk(market: str, *, base_url: Optional[str] = None, timeout: float = 20.0) -> dict:
    """Return the settlement-risk record for one Polymarket market (raises SettlementRiskError)."""
    base = (base_url or os.environ.get("PREDGE_API_BASE") or DEFAULT_BASE_URL).rstrip("/")
    url = f"{base}/v1/settlement-risk/{urllib.parse.quote(market.strip(), safe='')}"
    req = urllib.request.Request(url, headers={"accept": "application/json", "user-agent": f"simmer-skill/{SKILL_SLUG}"})
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=_ssl_context()) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        try:
            body = json.loads(e.read().decode("utf-8"))
        except Exception:
            body = {}
        raise SettlementRiskError(f"HTTP {e.code}: {body.get('error', '')} {body.get('message', '')}".strip()) from e
    except (urllib.error.URLError, TimeoutError, ValueError) as e:
        raise SettlementRiskError(f"network error: {e}") from e


def resolve_simmer_market(simmer_market_id: str) -> str:
    """Simmer market id -> Polymarket condition id, via SimmerClient (needs SIMMER_API_KEY)."""
    key = os.environ.get("SIMMER_API_KEY")
    if not key:
        raise SettlementRiskError("SIMMER_API_KEY is needed to resolve a Simmer market id")
    from simmer_sdk import SimmerClient  # lazy: the check itself needs no SDK

    client = SimmerClient(api_key=key, venue="polymarket")
    market = client.get_market_by_id(simmer_market_id)
    cid = getattr(market, "polymarket_condition_id", None) if market else None
    if not cid:
        raise SettlementRiskError(f"Simmer market {simmer_market_id} has no Polymarket condition id")
    return cid


# --------------------------------------------------------------------------- #
# Signature (optional, needs `cryptography` or `pynacl`)
# --------------------------------------------------------------------------- #
def verify_attestation(record: Mapping[str, Any], pinned_key: str = PREDGE_ATTESTATION_KEY) -> Optional[bool]:
    """True/False if checkable, None if no ed25519 library is installed or the record is unsigned."""
    att = record.get("attestation") or {}
    canonical, sig, pub = att.get("canonical"), att.get("signature"), att.get("public_key")
    if not (canonical and sig and pub):
        return None
    if pub.lower() != pinned_key.lower():
        return False
    try:
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

        try:
            Ed25519PublicKey.from_public_bytes(bytes.fromhex(pub)).verify(bytes.fromhex(sig), canonical.encode("utf-8"))
            return True
        except Exception:
            return False
    except ImportError:
        pass
    try:
        from nacl.signing import VerifyKey

        try:
            VerifyKey(bytes.fromhex(pub)).verify(canonical.encode("utf-8"), bytes.fromhex(sig))
            return True
        except Exception:
            return False
    except ImportError:
        return None


# --------------------------------------------------------------------------- #
# Gate
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class SettlementGateDecision:
    """allowed=False means skip this entry. size_factor scales your own sizing."""

    allowed: bool
    size_factor: float
    reason: str
    risk_level: Optional[str]
    recommendation: str
    dispute_count: int
    sent_to_uma_vote: bool
    market_id: Optional[str]
    checked_at: Optional[str]


def settlement_risk_gate(
    record: Optional[Mapping[str, Any]],
    *,
    block_on_caution: bool = True,
    watch_size_factor: float = 0.5,
    block_resolved: bool = True,
) -> SettlementGateDecision:
    """Decide whether the settlement state permits an entry.

    Fails closed: a missing record is a skip. Order:
        no record                      -> skip  "state_unavailable"
        resolved on chain              -> skip  "already_resolved" (unless block_resolved=False)
        caution (disputed / paused)    -> skip  "contested_resolution" (or trim if block_on_caution=False)
        watch (proposal / bulletin)    -> allow at watch_size_factor, "watch"
        ok                             -> allow at 1.0, "ok"
    """
    if not record:
        return SettlementGateDecision(False, 0.0, "state_unavailable", None, "no settlement-risk record", 0, False, None, None)
    level = record.get("risk_level")
    common = dict(
        risk_level=level,
        recommendation=str(record.get("recommendation", "")),
        dispute_count=int(record.get("dispute_count") or 0),
        sent_to_uma_vote=bool(record.get("sent_to_uma_vote")),
        market_id=(record.get("market") or {}).get("market_id"),
        checked_at=record.get("checked_at"),
    )
    if level == "resolved":
        return SettlementGateDecision(not block_resolved, 0.0 if block_resolved else 1.0, "already_resolved", **common)
    if level == "caution":
        if block_on_caution:
            return SettlementGateDecision(False, 0.0, "contested_resolution", **common)
        return SettlementGateDecision(True, watch_size_factor, "contested_resolution_trimmed", **common)
    if level == "watch":
        return SettlementGateDecision(True, watch_size_factor, "watch", **common)
    if level == "ok":
        return SettlementGateDecision(True, 1.0, "ok", **common)
    return SettlementGateDecision(False, 0.0, "unknown_risk_level", **common)


def check(market: str, **gate_kwargs: Any) -> tuple[Optional[dict], SettlementGateDecision]:
    """Fetch and gate in one call. Network failure -> skip (fail closed)."""
    try:
        record = fetch_settlement_risk(market)
    except SettlementRiskError as e:
        return None, SettlementGateDecision(False, 0.0, "state_unavailable", None, str(e), 0, False, None, None)
    return record, settlement_risk_gate(record, **gate_kwargs)


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def summarize(record: Mapping[str, Any], decision: SettlementGateDecision) -> str:
    m = record.get("market") or {}
    lines = [
        f"{m.get('question') or m.get('slug')} (market {m.get('market_id')})",
        f"  risk_level: {record.get('risk_level')}  ->  gate: {'ALLOW' if decision.allowed else 'SKIP'} ({decision.reason}, size x{decision.size_factor})",
        f"  {record.get('recommendation')}",
        f"  UMA state: {record.get('uma_state')}, disputes: {record.get('dispute_count')}, "
        f"open dispute: {record.get('open_dispute')}, sent to UMA vote: {record.get('sent_to_uma_vote')}",
    ]
    cp = record.get("current_proposal")
    if cp:
        lines.append(f"  proposal: {cp['proposed_outcome']} at {cp['proposed_at']}, challenge window ends {cp['challenge_window_ends']}")
    for d in record.get("disputes") or []:
        lines.append(f"  dispute: {d['disputed_at']} (disputed proposal: {d['disputed_proposal']}) tx {d['tx']}")
    bb = (record.get("bulletin_board") or {}).get("latest")
    if bb:
        lines.append(f"  latest bulletin-board update: {bb['kind']} at {bb['posted_at']} ({bb['poster']})")
    res = record.get("onchain_resolution")
    if res:
        lines.append(f"  on-chain resolution: {res['outcome']}")
    ok = verify_attestation(record)
    lines.append(f"  signature: {'verified (Predge key 13fa3d18)' if ok else 'NOT verified' if ok is False else 'not checked (pip install cryptography to verify)'}")
    lines.append(f"  checked at {record.get('checked_at')}")
    return "\n".join(lines)


def main(argv: Optional[Sequence[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="Predge settlement-risk check (observe-only, places no orders)")
    ap.add_argument("markets", nargs="*", help="Polymarket condition id, numeric market id or slug")
    ap.add_argument("--simmer-market", action="append", default=[], help="Simmer market id (needs SIMMER_API_KEY)")
    ap.add_argument("--demo", action="store_true", help="run on the bundled example records, no network")
    ap.add_argument("--json", action="store_true", help="print raw records")
    args = ap.parse_args(argv)
    cfg = load_config()
    gate_kwargs = {k: cfg[k] for k in ("block_on_caution", "watch_size_factor", "block_resolved") if k in cfg}

    if args.demo:
        for f in sorted((HERE / "examples").glob("*.json")):
            record = json.loads(f.read_text())
            print(summarize(record, settlement_risk_gate(record, **gate_kwargs)), "\n")
        return 0

    targets = list(args.markets)
    for sm in args.simmer_market:
        try:
            targets.append(resolve_simmer_market(sm))
        except SettlementRiskError as e:
            print(f"{sm}: SKIP (state_unavailable): {e}")
    if not targets:
        ap.print_help()
        return 2
    for t in targets:
        try:
            record = fetch_settlement_risk(t)
        except SettlementRiskError as e:
            print(f"{t}: SKIP (state_unavailable): {e}\n")
            continue
        if args.json:
            print(json.dumps(record, indent=1))
        else:
            print(summarize(record, settlement_risk_gate(record, **gate_kwargs)), "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
