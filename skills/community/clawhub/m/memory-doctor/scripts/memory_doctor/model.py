"""The normalized in-memory unit shared by all format adapters.

Both the auto-memory format (frontmatter + [[links]] + MEMORY.md) and, later, mneme
(cells/spine/lifecycle) parse down to a list of MemUnit. The rest of the tool
(report, lint) only ever sees MemUnit, never the raw format.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class MemUnit:
    id: str                       # auto-memory slug | mneme cell id
    gist: str                     # frontmatter description | mneme gist
    body: str                     # markdown body | cell body
    path: str                     # source file on disk
    type: str = "unknown"         # user|feedback|project|reference|unknown
    state: str = "live"           # live|stale|superseded|retired|proposed (auto-memory: live)
    conf: str = "med"             # high|med|low (auto-memory: default med)
    links: list[str] = field(default_factory=list)  # outbound target ids ([[links]] / link targets)
    rel_links: list = field(default_factory=list)    # mneme: list of (relation, target_id)
    topic: str = ""               # mneme topic-path; "" for auto-memory
    mtime: float = 0.0            # freshness epoch: mneme uses `seen` date, auto-memory file mtime
    raw_frontmatter: dict = field(default_factory=dict)

    @property
    def size_chars(self) -> int:
        return len(self.body)


@dataclass
class IndexEntry:
    """One line of the MEMORY.md / spine index."""
    id: str
    hook: str
    target: str                   # file the entry points at (may not exist)


@dataclass
class MemoryStore:
    """A parsed memory directory: units + the index that is supposed to mirror them."""
    root: str
    fmt: str                      # adapter name, e.g. "auto-memory"
    units: list[MemUnit] = field(default_factory=list)
    index: list[IndexEntry] = field(default_factory=list)
    index_path: Optional[str] = None
    has_index: bool = True        # auto-memory: persisted MEMORY.md (drifts). mneme: spine is derived

    def unit_by_id(self, uid: str) -> Optional[MemUnit]:
        for u in self.units:
            if u.id == uid:
                return u
        return None
