"""Two-source World Cup group-winner discovery.

Why two sources? The active Simmer venue only holds markets that have ALREADY been imported. The
2026 group-winner markets live upstream on Polymarket and are not imported yet, so a skill that
only reads ``client.get_markets()`` is structurally blind to them. We therefore read BOTH:

  1. the active venue (``get_markets``) — tradeable today; and
  2. the importable upstream pool (``list_importable_markets``) — candidates, report-only until
     Simmer imports + prices them.

Rule (per campaign spec): a complete, mutually-exclusive group set is exactly 4 group-WINNER legs
for the SAME letter, confirmed from market TEXT. Anything else is alerted, never arbed.

Server contract notes (SDK 0.17.25, verified live 2026-06-12):
  * ``get_markets`` signature is (status, import_source, limit, include) — there is NO search
    kwarg; fetch wide and regex-filter locally.
  * ``list_importable_markets`` 422s on limit > 100 and silently floors min_volume to 1000, so we
    clamp limit to 1..100.
"""

import re
import unicodedata

# --- Letter extraction --------------------------------------------------------------------------
# A group-WINNER market is phrased as "win(s) Group X", "finish(es) first in [World Cup] Group X",
# "Group X winner", or "top Group X". Letters are A–L (2026 = 12 groups of 4).
_WINNER_RE = re.compile(
    r"(?:wins?|finish(?:es)?\s+first|tops?)\s+"
    r"(?:in\s+)?(?:the\s+)?(?:world\s+cup\s+)?group\s+([A-L])\b",
    re.IGNORECASE,
)
_WINNER_SUFFIX_RE = re.compile(r"\bgroup\s+([A-L])\s+winner\b", re.IGNORECASE)
# Wording from the NON-exclusive market family — if present, the title is not a clean winner leg.
_NON_WINNER_RE = re.compile(
    r"advanc|qualif|knockout|reach|runner.?up|second.?place", re.IGNORECASE
)

COMPLETE_SET_SIZE = 4   # 2026 format: 4 teams per group
IMPORTABLE_QUERIES = ["World Cup", "World Cup Group", "FIFA", "finish first"]
ACTIVE_LIMIT_LADDER = [5000, 1000, 500, 200, 50]


def _norm(text):
    return unicodedata.normalize("NFKD", text or "")


def extract_group_letter(question):
    """Return the group letter 'A'..'L' for a group-WINNER market, else None.

    Matches winner wording ("win/finish first/top Group X", "Group X winner"); rejects the
    non-exclusive family (advance / qualify / knockout / reach / runner-up / second-place)."""
    q = _norm(question)
    if not q or _NON_WINNER_RE.search(q):
        return None
    for rx in (_WINNER_RE, _WINNER_SUFFIX_RE):
        m = rx.search(q)
        if m:
            return m.group(1).upper()
    return None


# --- Market-shape helpers (markets arrive as dicts OR objects) ----------------------------------
def _get(m, *names):
    for n in names:
        if isinstance(m, dict):
            if m.get(n) is not None:
                return m[n]
        else:
            v = getattr(m, n, None)
            if v is not None:
                return v
    return None


def _id_of(m):
    return _get(m, "id", "market_id", "condition_id")


def _question_of(m):
    return _get(m, "question", "title", "name") or ""


def _status_of(m):
    return _get(m, "status") or "active"


def _qkey(question):
    return re.sub(r"\s+", " ", _norm(question).strip().lower())


def _normalize(m, source):
    return {
        "source": source,
        "id": _id_of(m),
        "question": _question_of(m),
        "status": _status_of(m),
        "yes_price": _get(m, "yes_price", "current_probability", "best_ask", "price"),
        "polymarket_token_id": _get(m, "polymarket_token_id", "token_id", "clob_token_id"),
        "polymarket_condition_id": _get(m, "polymarket_condition_id", "condition_id"),
        "raw": m,
    }


# --- Source 1: active venue ---------------------------------------------------------------------
def fetch_active_markets(client, limit=5000):
    """Fetch the active venue wide (no search kwarg — the SDK has none). Degrade through smaller
    limits on error so a server cap on huge fetches doesn't blank the run."""
    ladder = [limit] + [n for n in ACTIVE_LIMIT_LADDER if n < limit]
    for n in ladder:
        try:
            return list(client.get_markets(limit=n) or [])
        except Exception as exc:                          # noqa: BLE001 — degrade, don't die
            print(f"  ! get_markets(limit={n}) failed: {exc}")
    return []


# --- Source 2: importable upstream pool ---------------------------------------------------------
def fetch_importable_worldcup(client, queries=None, limit=50, min_volume=0):
    """Fetch upstream World-Cup markets that exist but aren't imported yet. limit is clamped to
    1..100 (server 422s above 100). One failing query (422/timeout) is logged and skipped."""
    queries = IMPORTABLE_QUERIES if queries is None else queries
    limit = max(1, min(int(limit), 100))
    by_key = {}
    for q in queries:
        try:
            results = client.list_importable_markets(q=q, limit=limit, min_volume=min_volume) or []
        except Exception as exc:                          # noqa: BLE001 — one bad query isn't fatal
            print(f"  ! importable query '{q}' failed: {exc}")
            continue
        for m in results:
            key = _id_of(m) or _qkey(_question_of(m))
            if key is not None and key not in by_key:
                by_key[key] = m
    return list(by_key.values())


# --- Merge --------------------------------------------------------------------------------------
def discover(client):
    """Merge both sources into a structured discovery result. Importable entries that duplicate an
    active question are dropped (already tradeable)."""
    active_raw = fetch_active_markets(client)
    importable_raw = fetch_importable_worldcup(client)

    groups = {}

    def _bucket(letter):
        return groups.setdefault(letter, {"active": [], "importable": []})

    active_qkeys = set()
    active_legs = 0
    for m in active_raw:
        if _status_of(m) != "active":
            continue
        letter = extract_group_letter(_question_of(m))
        if not letter:
            continue
        entry = _normalize(m, "active")
        _bucket(letter)["active"].append(entry)
        active_qkeys.add(_qkey(entry["question"]))
        active_legs += 1

    importable_candidates = 0
    for m in importable_raw:
        letter = extract_group_letter(_question_of(m))
        if not letter:
            continue
        entry = _normalize(m, "importable")
        if _qkey(entry["question"]) in active_qkeys:
            continue                                      # already on the active venue
        _bucket(letter)["importable"].append(entry)
        importable_candidates += 1

    for g in groups.values():
        n_active = len(g["active"])
        g["complete_active_set"] = n_active == COMPLETE_SET_SIZE
        g["missing_legs"] = max(0, COMPLETE_SET_SIZE - n_active)

    counts = {
        "active_total": len(active_raw),
        "active_group_legs": active_legs,
        "importable_total": len(importable_raw),
        "importable_group_candidates": importable_candidates,
        "groups": len(groups),
        "complete_active_sets": sum(1 for g in groups.values() if g["complete_active_set"]),
    }
    return {"groups": groups, "counts": counts}


def format_report(discovery):
    """Render the four discovery states: active tradeable legs, importable-only candidates,
    complete active 4-leg sets, and incomplete groups."""
    groups = discovery["groups"]
    counts = discovery["counts"]
    lines = [
        f"Discovery: {counts['active_total']} active markets "
        f"({counts['active_group_legs']} group-winner legs) | "
        f"{counts['importable_total']} importable WC markets "
        f"({counts['importable_group_candidates']} group-winner candidates).",
    ]

    active_letters = sorted(l for l, g in groups.items() if g["active"])
    if active_letters:
        lines.append("Active tradeable group legs:")
        for letter in active_letters:
            for e in groups[letter]["active"]:
                p = e["yes_price"]
                px = f"{p:.2f}" if isinstance(p, (int, float)) else "n/a"
                lines.append(f"  [active]     Group {letter}: {e['question']} (yes={px})")
    else:
        lines.append("Active tradeable group legs: none.")

    cand_letters = sorted(l for l, g in groups.items() if g["importable"])
    if cand_letters:
        lines.append("Importable-only candidates (report-only — NOT traded until imported):")
        for letter in cand_letters:
            for e in groups[letter]["importable"]:
                lines.append(f"  [importable] Group {letter}: {e['question']}")

    complete = sorted(l for l, g in groups.items() if g["complete_active_set"])
    lines.append(
        "Complete active 4-leg sets: "
        + (", ".join("Group " + l for l in complete) if complete else "none")
        + "."
    )

    incomplete = sorted(l for l, g in groups.items() if not g["complete_active_set"])
    if incomplete:
        lines.append("Incomplete groups:")
        for letter in incomplete:
            g = groups[letter]
            lines.append(
                f"  Group {letter}: {len(g['active'])}/4 active, missing {g['missing_legs']} "
                f"(importable candidates: {len(g['importable'])})"
            )
    return "\n".join(lines)


# --- Back-compat contracts ----------------------------------------------------------------------
def find_group_sets(client, limit=5000):
    """Active-only {letter: [market objects]}, deduped by id. Unchanged contract for callers that
    only care about tradeable legs."""
    seen = {}
    for m in fetch_active_markets(client, limit=limit):
        if _status_of(m) != "active":
            continue
        letter = extract_group_letter(_question_of(m))
        if letter:
            seen.setdefault(letter, {})[_id_of(m) or _qkey(_question_of(m))] = m
    return {letter: list(d.values()) for letter, d in seen.items()}


def is_confirmed_exclusive(legs):
    """Exactly 4 legs, all winner-family wording, all the SAME letter -> arbable; else alert."""
    if len(legs) != COMPLETE_SET_SIZE:
        return False
    letters = set()
    for m in legs:
        letter = extract_group_letter(_question_of(m))
        if letter is None:
            return False                                  # a non-winner leg breaks the set
        letters.add(letter)
    return len(letters) == 1
