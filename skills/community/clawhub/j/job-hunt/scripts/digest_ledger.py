"""The weekly digest's ledger of roles already sent (<profile>/digest-seen.yaml).

A role is the same role when any URL matches, or when the normalised company and
title match and the location matches (a remote or multi-location posting matches
any location). Matching is exact after normalisation: a near-identical title is a
new role, because a wrong merge hides a role the user would want to see.
"""
from __future__ import annotations

import datetime
import os
import re
import tempfile
import unicodedata

import journal
import paths

KEEP_DAYS = 180
_SUFFIXES = (("b", "v"), ("bv",), ("n", "v"), ("nv",), ("gmbh",), ("ltd",), ("limited",),
             ("inc",), ("llc",), ("plc",), ("ag",), ("sa",), ("s", "a"), ("co",), ("corp",))
_TITLE_WORDS = {"sr": "senior", "jr": "junior"}
_ANY_PLACE = re.compile(r"remote|multiple|various|anywhere|thuiswerk|远程|[;|/]|\bor\b", re.I)


def _words(text) -> list:
    folded = unicodedata.normalize("NFKC", str(text or "")).casefold()
    return "".join(ch if ch.isalnum() else " " for ch in folded).split()


def norm_company(name) -> str:
    words = _words(name)
    changed = True
    while changed:
        changed = False
        for suffix in _SUFFIXES:
            n = len(suffix)
            if len(words) > n and tuple(words[-n:]) == suffix:
                words, changed = words[:-n], True
    return " ".join(words)


def norm_title(title) -> str:
    return " ".join(_TITLE_WORDS.get(w, w) for w in _words(title))


def norm_location(location) -> str:
    """"*" for remote or multi-location postings; otherwise the first place named."""
    text = str(location or "")
    if _ANY_PLACE.search(text):
        return "*"
    return " ".join(_words(text.split(",")[0]))


def _identity(row: dict) -> tuple:
    return norm_company(row.get("company")), norm_title(row.get("title"))


def is_seen(row: dict, ledger: dict) -> bool:
    url = str(row.get("url") or "").strip()
    company, title = _identity(row)
    place = norm_location(row.get("location"))
    for role in ledger.get("roles") or []:
        if url and url in (role.get("urls") or []):
            return True
        if company and title and role.get("company") == company and role.get("title") == title:
            places = role.get("locations") or []
            if place == "*" or "*" in places or place in places:
                return True
    return False


def filter_new(rows: list, ledger: dict) -> list:
    """Rows not yet sent, in order; a role repeated within the batch is kept once."""
    out, batch = [], {"roles": []}
    for row in rows:
        if is_seen(row, ledger) or is_seen(row, batch):
            continue
        out.append(row)
        batch = record_sent(batch, [row], datetime.date.today())
    return out


def record_sent(ledger: dict, rows: list, today: datetime.date) -> dict:
    roles = [dict(r) for r in ledger.get("roles") or []]
    for row in rows:
        url = str(row.get("url") or "").strip()
        company, title = _identity(row)
        place = norm_location(row.get("location"))
        match = None
        for role in roles:
            if (url and url in role["urls"]) or (company and title and role["company"] == company
                                                 and role["title"] == title):
                match = role
                break
        if match is None:
            match = {"company": company, "title": title, "locations": [], "urls": [],
                     "first_sent": today.isoformat()}
            roles.append(match)
        if url and url not in match["urls"]:
            match["urls"].append(url)
        if place not in match["locations"]:
            match["locations"].append(place)
        match["last_seen"] = today.isoformat()
    return {"roles": roles}


def prune(ledger: dict, today: datetime.date, days: int = KEEP_DAYS) -> dict:
    keep = []
    for role in ledger.get("roles") or []:
        try:
            first = datetime.date.fromisoformat(str(role.get("first_sent")))
        except ValueError:
            keep.append(role)  # an unreadable date is kept: dropping it would resend the role
            continue
        if (today - first).days <= days:
            keep.append(role)
    return {"roles": keep}


def load_ledger(name: str) -> dict:
    path = paths.digest_seen(name)
    if not path.exists():
        return {"roles": []}
    data = journal.load_yaml(path)
    roles = data.get("roles", [])
    if not isinstance(roles, list):
        raise journal.YamlUnreadable(path, "`roles` must be a list")
    return {"roles": roles}


def save_ledger(name: str, ledger: dict) -> None:
    import yaml
    path = paths.digest_seen(name)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=".digest-seen-", suffix=".yaml")
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        yaml.safe_dump({"roles": ledger.get("roles") or []}, fh, allow_unicode=True, sort_keys=False)
    os.replace(tmp, path)
