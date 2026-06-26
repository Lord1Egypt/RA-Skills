"""Read-only health detection over a MemoryStore.

Everything here is deterministic and LLM-free (v0.1). Semantic problems that genuinely
need a model (true dedup merge, contradiction reconcile) are *flagged* as candidates,
never resolved — resolution is v0.2.
"""

from __future__ import annotations

import re
import time
from dataclasses import dataclass, field

from .model import MemoryStore, MemUnit

OVERSIZE_CHARS = 1800
DUP_JACCARD = 0.50
# freshness half-life (days) by type: references/prefs age slowly, projects fast
HALFLIFE_DAYS = {"reference": 180, "user": 180, "feedback": 90, "project": 30, "unknown": 60}
STALE_DAYS = 30
# mneme lifecycle states that are history, excluded from "active" health
HISTORY_STATES = {"superseded", "retired", "proposed"}
REL_INVERSE = {"supersedes": "superseded-by", "superseded-by": "supersedes"}

_ASCII_WORD = re.compile(r"[a-z0-9_]{3,}")
_CJK = re.compile(r"[一-鿿]")


def _tokens(text: str) -> set:
    """Stdlib-only tokens that work for mixed CN/EN: ascii words (len>=3) plus CJK
    character bigrams. Good enough to surface lexical near-duplicates without jieba."""
    t = text.lower()
    toks = set(_ASCII_WORD.findall(t))
    cjk = _CJK.findall(t)
    toks.update(cjk[i] + cjk[i + 1] for i in range(len(cjk) - 1))
    return toks


def _jaccard(a: set, b: set) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


@dataclass
class HealthReport:
    store: MemoryStore
    total_units: int = 0
    total_bytes: int = 0
    missing_from_index: list = field(default_factory=list)   # unit ids absent from index
    dangling_index: list = field(default_factory=list)       # index entries -> no file
    dead_links: list = field(default_factory=list)           # (unit_id, broken_target)
    orphans: list = field(default_factory=list)              # unit ids, no inbound + unindexed
    stale: list = field(default_factory=list)                # (unit_id, age_days)
    oversized: list = field(default_factory=list)            # (unit_id, chars)
    dup_candidates: list = field(default_factory=list)       # (id_a, id_b, score)
    freshness: int = 0
    history: list = field(default_factory=list)              # mneme: superseded/retired/proposed ids
    asymmetric_links: list = field(default_factory=list)     # mneme: "A supersedes B but B lacks back-link"

    @property
    def fixable_index_issues(self) -> int:
        return len(self.missing_from_index) + len(self.dangling_index)


def analyze(store: MemoryStore) -> HealthReport:
    rep = HealthReport(store=store)
    all_units = store.units
    # "active" health excludes mneme history cells (superseded/retired/proposed); for
    # auto-memory every unit defaults to state=live, so active == all there.
    rep.history = [u.id for u in all_units if u.state in HISTORY_STATES]
    units = [u for u in all_units if u.state not in HISTORY_STATES]
    rep.total_units = len(units)
    rep.total_bytes = sum(len(u.body.encode("utf-8")) for u in units)

    ids = {u.id for u in all_units}            # link targets may point at history cells
    active_ids = {u.id for u in units}

    # index drift / index-based orphans only apply when the index is a persisted file
    # that can drift (auto-memory). mneme's spine is derived → skip.
    indexed_ids = {e.id for e in store.index}
    if store.has_index:
        import os
        files = {os.path.basename(u.path) for u in all_units}
        rep.missing_from_index = sorted(active_ids - indexed_ids)
        rep.dangling_index = [e.id for e in store.index
                              if e.target not in files and e.id not in ids]

    # inbound link map + dead-link + (mneme) supersede symmetry, over all units
    inbound = {u.id: 0 for u in units}
    by_id = {u.id: u for u in all_units}
    for u in all_units:
        for target in u.links:
            if target in inbound and target != u.id:
                inbound[target] += 1
            if target not in ids:
                rep.dead_links.append((u.id, target))
        for rel, tgt in u.rel_links:
            inv = REL_INVERSE.get(rel)
            if inv and tgt in by_id and not any(
                r == inv and t == u.id for r, t in by_id[tgt].rel_links
            ):
                rep.asymmetric_links.append(f"{u.id} {rel} {tgt}, but {tgt} lacks {inv}")

    now = time.time()
    for u in units:
        if store.has_index and inbound.get(u.id, 0) == 0 and u.id not in indexed_ids:
            rep.orphans.append(u.id)
        age_days = (now - u.mtime) / 86400 if u.mtime else 0
        if age_days > STALE_DAYS:
            rep.stale.append((u.id, round(age_days)))
        if u.size_chars > OVERSIZE_CHARS:
            rep.oversized.append((u.id, u.size_chars))

    # lexical duplicate candidates over active units (flag only)
    toksets = {u.id: _tokens(u.gist + " " + u.body) for u in units}
    for i in range(len(units)):
        for j in range(i + 1, len(units)):
            a, b = units[i], units[j]
            s = _jaccard(toksets[a.id], toksets[b.id])
            if s >= DUP_JACCARD:
                rep.dup_candidates.append((a.id, b.id, round(s, 2)))

    # freshness = mean per-unit exponential decay, by type half-life (active units)
    if units:
        total = 0.0
        for u in units:
            age_days = (now - u.mtime) / 86400 if u.mtime else 0
            hl = HALFLIFE_DAYS.get(u.type, HALFLIFE_DAYS["unknown"])
            total += 0.5 ** (age_days / hl)
        rep.freshness = round(total / len(units) * 100)
    return rep


def render_card(rep: HealthReport) -> str:
    kb = rep.total_bytes / 1024
    lines = [
        f"🧠 Memory Health   ({rep.total_units} units, {kb:.1f} KB · format: {rep.store.fmt})",
    ]

    def row(label, count, detail="", flag=""):
        bar = f"{label+':':<18}{count}"
        if detail:
            bar = f"{bar:<28}{detail}"
        if flag:
            bar = f"{bar}  {flag}"
        return "├─ " + bar

    if rep.store.has_index:
        idx_issues = rep.fixable_index_issues
        lines.append(row("Index drift", idx_issues,
                         f"{len(rep.missing_from_index)} missing / {len(rep.dangling_index)} dangling",
                         "▲ fixable" if idx_issues else "✓"))
    else:
        lines.append(row("Spine", "derived", "no persisted index", "✓"))
        lines.append(row("History", len(rep.history), "superseded/retired/proposed", ""))
        lines.append(row("Link symmetry", len(rep.asymmetric_links),
                         "supersede back-links", "⚠" if rep.asymmetric_links else "✓"))
    lines.append(row("Duplicate cand.", len(rep.dup_candidates),
                     "lexical", "▲ review (v0.2 merge)" if rep.dup_candidates else "✓"))
    lines.append(row("Conflicts", "—", "needs LLM", "→ v0.2"))
    lines.append(row("Dead links", len(rep.dead_links),
                     "", "⚠" if rep.dead_links else "✓"))
    if rep.store.has_index:
        lines.append(row("Orphans", len(rep.orphans),
                         "no inbound + unindexed", "▲" if rep.orphans else "✓"))
    lines.append(row("Stale (>30d)", len(rep.stale),
                     "", "" if not rep.stale else "▲"))
    lines.append(row("Oversized", len(rep.oversized),
                     f">{OVERSIZE_CHARS} chars", "▲ compact (v0.2)" if rep.oversized else "✓"))
    # last row uses └─
    lines.append(f"└─ {'Freshness:':<18}{rep.freshness} / 100")

    # detail appendix
    def detail_block(title, items):
        if not items:
            return []
        return [f"\n{title}:"] + [f"  • {x}" for x in items]

    out = ["\n".join(lines)]
    out += detail_block("Index — missing entries", rep.missing_from_index)
    out += detail_block("Index — dangling entries", rep.dangling_index)
    out += detail_block("Dead links", [f"{a} → {b}" for a, b in rep.dead_links])
    out += detail_block("Asymmetric supersede links", rep.asymmetric_links)
    out += detail_block("Orphans", rep.orphans)
    out += detail_block("Duplicate candidates",
                        [f"{a} ~ {b}  ({s})" for a, b, s in rep.dup_candidates])
    out += detail_block("Oversized", [f"{i}  ({c} chars)" for i, c in rep.oversized])
    out += detail_block("Stale", [f"{i}  ({d}d)" for i, d in rep.stale])
    return "\n".join(p for p in out if p)
