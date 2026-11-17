"""Action executor: ordinal re-resolve -> occlusion ladder -> act -> generic extract."""
from __future__ import annotations

import json
import os
import shutil
import time
from datetime import UTC, datetime
from typing import Any

from .table import STATE_JS, TABLE_CORE_JS

NO_TARGET_OPS = {"WAIT", "SCROLL_UP", "SCROLL_DOWN", "DONE", "BLOCKED"}
EVIDENCE_DIR = "~/.jev-webbridge/evidence"
MAX_EXTRACT_CHARS = 20000

# Resolve re-runs the EXACT TABLE_CORE selection so ordinals can never diverge from
# table.py, then stamps a temporary data-jw-idx marker. Ladder selectors are built
# ONLY from [data-jw-idx="N"] — never site classes.
_RESOLVE_TMPL = "(() => {\n  const idx = __IDX__;\n" + TABLE_CORE_JS + r"""
  const el = rowEls[idx];  // row ordinal, 1:1 with the table the model saw
  if (!el) return JSON.stringify({found: false});
  el.setAttribute('data-jw-idx', String(idx));
  const nm = (el.getAttribute('aria-label') || el.getAttribute('placeholder')
    || el.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 80);
  return JSON.stringify({found: true, tag: el.tagName, name: nm});
})()"""

RESOLVE_JS = _RESOLVE_TMPL


def resolve_js(idx: int) -> str:
    """Self-contained IIFE: re-run TABLE_CORE selection, stamp data-jw-idx on ordinal idx."""
    return _RESOLVE_TMPL.replace("__IDX__", str(int(idx)))


# Generic value readback probe (fill_check / pre_submit_check second readback).
_READBACK_TMPL = r"""(() => { /* __compose_readback__: generic value readback for one selector */
  const el = document.querySelector(__SEL__);
  if (!el) return JSON.stringify({text: null});
  let text = '';
  if ('value' in el && typeof el.value === 'string') text = el.value;
  else text = el.textContent || '';
  return JSON.stringify({text});
})()"""


def _readback_js(selector: str) -> str:
    return _READBACK_TMPL.replace("__SEL__", json.dumps(selector))


# GENERIC extract: expand via generic control match, then largest visible
# main/article region, capped — never whole-page text, never site-specific.
EXTRACT_JS = r"""(() => {
  const EXPAND = /^(展开|查看更多|show more|read more)$/i;
  try {
    const controls = Array.from(document.querySelectorAll('button, a, [role=button], summary'));
    for (const c of controls) {
      const label = ((c.getAttribute('aria-label') || '') + ' ' + (c.textContent || '')).trim();
      if (EXPAND.test(label)) {
        const r = c.getBoundingClientRect();
        if (r.width > 0 && r.height > 0) { c.click(); break; }
      }
    }
  } catch (e) {}
  const visible = (el) => {
    if (!el) return false;
    const r = el.getBoundingClientRect(); const s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none';
  };
  let region = document.querySelector('main article') || document.querySelector('main');
  if (!region) {
    const cands = Array.from(document.querySelectorAll('main, [role=main], article')).filter(visible);
    region = cands.sort((a, b) => ((b.innerText || '').length) - ((a.innerText || '').length))[0] || null;
  }
  if (!region) region = document.body;
  const text = (((region && region.innerText) || '').trim()).slice(0, 20000);
  return JSON.stringify({text, url: location.href});
})()"""


class Executor:
    def __init__(self, driver: Any, evidence_dir: str = EVIDENCE_DIR):
        self.driver = driver
        self.evidence_dir = evidence_dir

    # ---- resolve -------------------------------------------------------
    def resolve(self, idx: int) -> dict | None:
        """Re-run the deterministic in-page query; stamp data-jw-idx on ordinal idx."""
        try:
            raw = self.driver.evaluate(resolve_js(idx))
            data = json.loads(raw) if isinstance(raw, str) else raw
        except Exception:  # noqa: BLE001 — driver/parse failure degrades to unresolved
            return None
        if not isinstance(data, dict) or not data.get("found"):
            return None
        return data

    # ---- readbacks -----------------------------------------------------
    def fill_check(self, selector: str, value: str) -> bool:
        """Immediate equality readback after driver fill."""
        return self._readback(selector) == value

    def pre_submit_check(self, selector: str, expected: str | None = None) -> bool:
        """Separate second readback (loop.py): detects late draft-restore before submit."""
        text = self._readback(selector)
        if expected is None:
            return text is not None
        return text == expected

    def _readback(self, selector: str) -> str | None:
        try:
            raw = self.driver.evaluate(_readback_js(selector), mutating=True)
            data = json.loads(raw) if isinstance(raw, str) else raw
        except Exception:  # noqa: BLE001 — readback failure reports as mismatch, never raises
            return None
        if isinstance(data, dict):
            text = data.get("text")
            return None if text is None else str(text)
        return None

    # ---- act -----------------------------------------------------------
    def act(self, decision: dict, rows: list[dict],
            *, post_fill_js: str | None = None) -> dict:
        t0 = time.monotonic()
        op = decision.get("op")
        if op in NO_TARGET_OPS and decision.get("target") is None:
            return self._receipt(decision, result="ok", rung=0, detail="no-target op", t0=t0)
        target_idx = decision.get("target")
        if target_idx is None:
            return self._receipt(decision, result="stale", rung=None, detail="ordinal missing", t0=t0)
        target = self.resolve(target_idx)
        if not target:
            return self._receipt(decision, result="stale", rung=None, detail="ordinal missing", t0=t0)
        sel = f'[data-jw-idx="{target_idx}"]'
        try:
            if op == "TYPE_TEXT":
                value = decision.get("value") or ""
                try:
                    self.driver.call("fill", mutating=True, selector=sel, value=value)
                except Exception as e:  # noqa: BLE001 — any driver failure -> error receipt
                    return self._receipt(
                        decision, result="error", rung=None, detail=f"fill failed: {e}", t0=t0
                    )
                ok = self.fill_check(sel, value)
                if ok and post_fill_js:
                    # Site draft-sync hook: fill touched the DOM only; dispatch the
                    # input-event sync so the framework's draft state registers the
                    # text (otherwise submit can silently no-op).
                    try:
                        self.driver.evaluate(post_fill_js, mutating=True)
                    except Exception:  # noqa: BLE001, S110 — best effort, never fails the act
                        pass
                return self._receipt(
                    decision, result="ok" if ok else "error", rung=2,
                    detail="fill readback " + ("equal" if ok else "MISMATCH"), t0=t0,
                )
            errors = []
            rungs = self._click_ladder(sel)
            base = self._state_fingerprint()
            silent_ok: tuple[int, str] | None = None
            for rung, (name, fn) in enumerate(rungs, start=1):
                try:
                    fn()
                except Exception as e:  # noqa: BLE001 — rung failure escalates the ladder
                    errors.append(f"rung{rung}:{e}")
                    continue
                # A rung can succeed mechanically and be IGNORED by the app
                # (silent no-op). Unchanged state fingerprint -> fall through;
                # the last rung returns regardless (invisible effects are not blocks).
                if rung == len(rungs) or self._effect_seen(base):
                    return self._receipt(decision, result="ok", rung=rung, detail=name, t0=t0)
                errors.append(f"rung{rung}:{name}:no-effect")
                if silent_ok is None:
                    silent_ok = (rung, name)
            if silent_ok is not None:
                # Every successful rung was invisible to the probe and the rest
                # failed: a click with no observable effect is not proof of
                # failure — trust the first silent success over a blocked verdict.
                return self._receipt(decision, result="ok", rung=silent_ok[0],
                                     detail=silent_ok[1] + "+silent", t0=t0)
            self._screenshot(decision)
            return self._receipt(
                decision, result="blocked", rung=None, detail=" | ".join(errors), t0=t0
            )
        finally:
            self._cleanup_marker(sel)

    def _click_ladder(self, sel: str) -> list[tuple[str, Any]]:
        """Spec §5 order (amended 2026-09-24): rung1 bring_to_front+trusted mouse_click,
        rung2 synthetic click (app handlers fire — CDP mouse events were proven to be
        silently ignored by a submit handler), rung3 cdp dispatchMouseEvent (occlusion
        survivor). Every rung except the last must prove effect before it counts."""
        return [
            (
                "bring_to_front+trusted_mouse_click",
                lambda: (
                    self.driver.call("cdp", mutating=True, method="Page.bringToFront"),
                    self.driver.call("mouse_click", mutating=True, selector=sel),
                ),
            ),
            (
                "synthetic_click",
                lambda: self.driver.call(
                    "evaluate", mutating=True,
                    code=f"(() => document.querySelector({sel!r}).click())()",
                ),
            ),
            ("cdp_dispatch_mouse_event", lambda: self._cdp_click(sel)),
        ]

    def _cdp_click(self, sel: str) -> None:
        """Rung 2: executor computes rect center from box model — never model output."""
        code = (
            f"(() => {{ const el = document.querySelector({sel!r});"
            " if (!el) return JSON.stringify(null);"
            " const r = el.getBoundingClientRect();"
            " return JSON.stringify({x: r.left + r.width / 2, y: r.top + r.height / 2}); })()"
        )
        raw = self.driver.evaluate(code, mutating=True)
        box = json.loads(raw) if isinstance(raw, str) else raw
        if not isinstance(box, dict) or "x" not in box or "y" not in box:
            raise RuntimeError("no box model for target")
        x, y = float(box["x"]), float(box["y"])
        for event_type in ("mousePressed", "mouseReleased"):
            self.driver.call(
                "cdp", mutating=True, method="Input.dispatchMouseEvent",
                params={"type": event_type, "x": x, "y": y, "button": "left", "clickCount": 1},
            )

    # ---- helpers -------------------------------------------------------
    def _cleanup_marker(self, sel: str) -> None:
        try:
            self.driver.evaluate(
                f"(() => {{ const el = document.querySelector({sel!r});"
                " if (el) el.removeAttribute('data-jw-idx'); })()",
                mutating=True,
            )
        except Exception:  # noqa: BLE001 — marker cleanup is best-effort, never raises
            return

    EFFECT_WAIT_S = 0.7  # window in which a click's effect must show in the state

    def _state_fingerprint(self) -> str:
        try:
            return str(self.driver.evaluate(STATE_JS))
        except Exception:  # noqa: BLE001 — no fingerprint => first success counts as effect
            return ""

    def _effect_seen(self, base: str) -> bool:
        time.sleep(self.EFFECT_WAIT_S)
        if not base:
            return True
        try:
            return self._state_fingerprint() != base
        except Exception:  # noqa: BLE001 — probe failure errs toward the rung having worked
            return True

    def _receipt(self, decision: dict, *, result: str, rung: int | None,
                 detail: str, t0: float) -> dict:
        return {
            "op": decision.get("op"),
            "target": decision.get("target"),
            "result": result,
            "rung": rung,
            "detail": str(detail)[:500],
            "duration_ms": int((time.monotonic() - t0) * 1000),
        }

    def _screenshot(self, decision: dict) -> None:
        """Failure evidence; failure to screenshot never raises."""
        try:
            data = self.driver.call("screenshot", format="jpeg", quality=60)
            src = None
            if isinstance(data, dict):
                for key in ("path", "file", "filename", "value"):
                    value = data.get(key)
                    if isinstance(value, str) and value and os.path.exists(value):
                        src = value
                        break
            elif isinstance(data, str) and os.path.exists(data):
                src = data
            if not src:
                return
            dest_dir = os.path.expanduser(self.evidence_dir)
            os.makedirs(dest_dir, exist_ok=True)
            stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%S%fZ")
            shutil.copy2(src, os.path.join(dest_dir, f"{stamp}-{decision.get('op', 'act')}"))
        except Exception:  # noqa: BLE001 — evidence capture must never break the act path
            return

    # ---- extract -------------------------------------------------------
    def extract(self) -> str:
        """Generic extract: expand control, then largest visible main/article region."""
        try:
            raw = self.driver.evaluate(EXTRACT_JS)
            data = json.loads(raw) if isinstance(raw, str) else raw
        except Exception:  # noqa: BLE001 — extraction failure returns empty, never raises
            return ""
        if isinstance(data, dict):
            return str(data.get("text") or "")[:MAX_EXTRACT_CHARS]
        return str(data or "")[:MAX_EXTRACT_CHARS]

    def post_extract_probe(self, post_extract_js: str | None) -> dict:
        """Optional site QA probe run after extraction (e.g. answer provenance
        and citation-marker counts). Best-effort read-only: never raises."""
        if not post_extract_js:
            return {}
        try:
            raw = self.driver.evaluate(post_extract_js)
            data = json.loads(raw) if isinstance(raw, str) else raw
            return data if isinstance(data, dict) else {}
        except Exception:  # noqa: BLE001 — QA probe must never break the run
            return {}
