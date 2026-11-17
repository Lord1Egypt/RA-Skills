"""Generic settle predicate. Site-agnostic signals only."""
from __future__ import annotations

from typing import Any

WHY_OVERRIDE = None
PROBE_JS = r"""(() => {
  const now = Date.now();
  if (!window.__jw) { window.__jw = {lastMut: now, textLen: 0};
    new MutationObserver(() => { window.__jw.lastMut = Date.now(); }).observe(document.body, {subtree:true, childList:true, characterData:true}); }
  const textLen = document.body ? document.body.innerText.length : 0;
  window.__jw.textLen = textLen;
  return JSON.stringify({text_len: textLen, quiet_ms: Date.now() - window.__jw.lastMut, extra: {}});
})()"""

def is_stable(samples: list[tuple[int, int]]) -> bool:
    """[(value, age_ms)] newest first: same value AND oldest sample ≥500ms older than newest."""
    if len(samples) < 2: return False
    vals = [v for v, _ in samples]
    return len(set(vals)) == 1 and (samples[0][1] - samples[-1][1]) >= 500

def settled(baseline_len: int, samples: list[tuple[int, int]], quiet_ms: int) -> bool:
    newest_len = samples[0][0] if samples else baseline_len
    grew = newest_len > baseline_len
    quiet = samples and samples[0][1] >= quiet_ms
    return bool(grew and quiet and is_stable(samples))

def predicate() -> dict[str, Any]:
    """The site-agnostic default Predicate dict (spec §6 generic-by-default)."""
    return {"name": "generic", "probe_js": PROBE_JS, "cap_ms": 2000, "poll_ms": 100,
            "settled": settled, "why_override": WHY_OVERRIDE}
