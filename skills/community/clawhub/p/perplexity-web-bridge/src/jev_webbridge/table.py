"""Dynamic indexed element table. GENERIC ONLY — no site selectors, no prepared strings."""
from __future__ import annotations

import json
from typing import Any

KNOWN_OPS = {"CLICK", "TYPE_TEXT", "SELECT", "SCROLL_UP", "SCROLL_DOWN"}
REQUIRED = ("idx", "role", "ops")

# Shared selection logic: selector list + visibility filter + OPS mapping + row building.
# TABLE_JS, OBSERVE_JS and (Task 4) executor resolve all embed this exact string, so
# ordinals can never diverge from the executor's resolver.
TABLE_CORE_JS = r"""  const VIS = (el) => { const r = el.getBoundingClientRect(); const s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none'; };
  const OPS = (el) => {
    const role = (el.getAttribute('role') || el.tagName.toLowerCase());
    const t = role.toLowerCase();
    if (el.tagName === 'BUTTON' || el.tagName === 'A' || ['button','link','menuitem','tab','checkbox','radio'].includes(t))
      return ['CLICK'];
    // Fillable == what the extension accepts (native input/textarea/CE).
    // role=textbox alone is a custom widget the extension refuses -> CLICK only.
    if (el.isContentEditable || el.tagName === 'INPUT' || el.tagName === 'TEXTAREA')
      return ['CLICK','TYPE_TEXT'];
    if (el.tagName === 'SELECT' || ['combobox','listbox','select'].includes(t))
      return ['CLICK','TYPE_TEXT','SELECT'];
    if (t.includes('scroll')) return ['SCROLL_UP','SCROLL_DOWN'];
    return ['CLICK'];
  };
  const sel = ['button','a[href]','input','textarea','select','[contenteditable="true"]',
    '[role=button]','[role=link]','[role=textbox]','[role=combobox]','[role=menuitem]',
    '[role=tab]','[role=checkbox]','[role=radio]'].join(',');
  // Drop stamps from any previous observe/resolve first: re-renders reuse nodes
  // and a stale data-jw-idx would silently point fill/click at the wrong element.
  document.querySelectorAll('[data-jw-idx]').forEach(x => x.removeAttribute('data-jw-idx'));
  const els = Array.from(document.querySelectorAll(sel))
    .filter(el => VIS(el) && !el.disabled)
    .filter(el => !(el.closest('[aria-hidden="true"]')));
  const rows = [];
  const rowEls = [];   // row ordinal <-> element, 1:1 (resolve() must use THIS,
                       // not els[], because empty rows are skipped below)
  els.forEach((el, i) => {
    const ops = OPS(el);
    let name = (el.getAttribute('aria-label') || el.getAttribute('placeholder')
      || el.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 80);
    if (!name && el.id) {
      const lb = document.querySelector('label[for="' + el.id.replace(/"/g, '') + '"]');
      if (lb) name = (lb.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 80);
    }
    let value = null;
    if ('value' in el && typeof el.value === 'string') value = el.value.slice(0, 80);
    else if (el.isContentEditable) value = (el.textContent || '').slice(0, 80);
    const typeable = ops.includes('TYPE_TEXT');
    if (!name && !value && !typeable) return;
    if (!name) name = '(unnamed ' + (el.getAttribute('role') || el.tagName.toLowerCase()) + ')';
    el.setAttribute('data-jw-idx', String(rows.length));  // included rows only
    rowEls.push(el);
    rows.push({idx: rows.length, role: (el.getAttribute('role') || el.tagName.toLowerCase()),
               name, value, ops});
  });"""

TABLE_JS = "(() => {\n" + TABLE_CORE_JS + "\n  return JSON.stringify({rows, url: location.href});\n})()"

STATE_JS = r"""(() => JSON.stringify({url: location.href, title: document.title,
  text_len: (document.body ? document.body.innerText.length : 0)}))()"""

OBSERVE_JS = "(() => {\n" + TABLE_CORE_JS + """
  const state = {url: location.href, title: document.title,
    text_len: (document.body ? document.body.innerText.length : 0)};
  return JSON.stringify({table: {rows, url: location.href}, state});
})()"""


def parse_table(raw: str | dict) -> list[dict[str, Any]]:
    try:
        data = json.loads(raw) if isinstance(raw, str) else raw
        rows = data["rows"]
    except (json.JSONDecodeError, KeyError, TypeError) as e:
        raise ValueError(f"malformed table payload: {e}") from e
    out = []
    for i, r in enumerate(rows):
        if any(k not in r for k in REQUIRED) or r.get("idx") != i:
            raise ValueError(f"row {i} malformed or idx not dense-ordinal: {r}")
        if not isinstance(r["ops"], list) or not r["ops"]:
            raise ValueError(f"row {i} has no ops")
        out.append(r)
    return out


def observe(raw: str) -> tuple[list[dict], dict]:
    """Parse OBSERVE_JS output -> (rows, state)."""
    try:
        data = json.loads(raw)
        return parse_table(data["table"]), data["state"]
    except (json.JSONDecodeError, KeyError) as e:
        raise ValueError(f"malformed observe payload: {e}") from e


def observe_js() -> str:
    """Single IIFE evaluating to JSON {"table": {"rows", "url"}, "state": {...}}."""
    return OBSERVE_JS
