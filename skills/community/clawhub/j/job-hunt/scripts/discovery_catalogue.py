#!/usr/bin/env python3
"""Read the adapter catalogue in references/discovery-sources.md.

One parser, used by the gate and by the tests that police the document. A
second hand-rolled copy of this regex would let the two disagree silently,
which is the failure the catalogue exists to prevent.

The field this module exists for is `listing_commands`: the commands whose
output is a **job posting**. It is not the same question as "does this adapter
have a search command". `nowcoder` has one, and it returns 面经 — threads about
interviews that already happened. A row built from one of those asserts a
vacancy exists, and no provenance check can tell the difference, because every
anchor holds: the id is really in the capture and the text was really copied.
"""
from __future__ import annotations

import functools
import pathlib
import re

import yaml

CATALOGUE = (pathlib.Path(__file__).resolve().parent.parent
             / "references" / "discovery-sources.md")

_BLOCK = re.compile(r"```yaml\n(.*?)\n```", re.S)


class CatalogueUnreadable(Exception):
    """The catalogue is missing or malformed; callers fail closed."""


@functools.lru_cache(maxsize=None)
def adapters(path: str | None = None) -> dict:
    """Every adapter entry, keyed by site."""
    source = pathlib.Path(path) if path else CATALOGUE
    try:
        text = source.read_text(encoding="utf-8")
    except OSError as exc:
        raise CatalogueUnreadable(f"cannot read {source}: {exc}") from exc
    match = _BLOCK.search(text)
    if not match:
        raise CatalogueUnreadable(f"{source} has no fenced yaml block")
    try:
        block = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        raise CatalogueUnreadable(f"{source} yaml block is malformed: {exc}") from exc
    if not isinstance(block, dict) or not isinstance(block.get("adapters"), dict):
        raise CatalogueUnreadable(f"{source} yaml block has no `adapters` mapping")
    return block["adapters"]


def _entry(site, path):
    """Look a site up the way a hand-written `source_site` spells it.

    Probed 2026-09-20: keys here are lowercase, so `"NOWCODER"` missed and fell
    through the branch that deliberately lets UNCATALOGUED browser-route boards
    pass — one capital letter turned the refusal off. Match on a folded,
    stripped key instead; the catalogue is small and the keys are distinct, so
    nothing collides.
    """
    if not isinstance(site, str):
        return None
    wanted = site.strip().casefold()
    if not wanted:
        return None
    for name, entry in adapters(path).items():
        if str(name).strip().casefold() == wanted and isinstance(entry, dict):
            return entry
    return None


def listing_commands(site: str, path: str | None = None) -> tuple[str, ...]:
    """Commands of `site` whose output is a job posting.

    An empty tuple means the site publishes none — not that it is useless, and
    not that it cannot be read. `()` is also what an UNKNOWN site returns, so
    callers must tell the two apart with `is_catalogued` before refusing a row:
    modes/discover.md routes European rounds to Indeed's country sites and to
    market-native boards through the browser, and none of those is an adapter
    in here. An allow-list keyed on this catalogue would refuse them.
    """
    entry = _entry(site, path)
    if entry is None:
        return ()
    commands = entry.get("listing_commands")
    if not isinstance(commands, list):
        return ()
    return tuple(str(command) for command in commands)


def is_catalogued(site: str, path: str | None = None) -> bool:
    return _entry(site, path) is not None
