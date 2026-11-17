#!/usr/bin/env python3
"""Read-only four-state probe for the Perplexity console ``_JS_INFO`` snapshot.

Dumps the ``_JS_INFO`` state under the four composer states used to verify
the completion-determination predicate:

  1_before_submit_with_draft   after fill, draft present, NOT submitted
  2_during_generation          within ~3s of a real submit (generating)
  3_after_done_empty_composer  after the NEW answer's 已研究 pill appears
                               (``studied >= base + 1``) and the prose
                               settles — NOT ``_gate_complete`` (its
                               early-exit bug samples mid-stream)
  4_after_done_with_draft      reload (heal DOM/state desync), then fill
                               again after completion (draft present);
                               a still-not-committed fill is flagged
                               ``state4_fill_failed`` instead of raising

v2 snapshot extras (every state): ``buttons_raw`` is an UNFILTERED dump of
``button,[role="button"]`` (bare icon buttons included — the stop control
is conditionally rendered and often unlabeled) and ``submit_parent_html``
is the submit button's ``parentElement.outerHTML`` (trimmed to 1500 chars).

Snapshots are written to
``<console_home()>/evidence/probe_submit_states-<epoch>.json``
(default ``~/.perplexity-console/evidence/``) and each state is echoed to
stdout as one compact JSON line.

WARNING — 未获用户 GO 不得运行 (DO NOT RUN WITHOUT EXPLICIT USER GO):

  State 2 performs ONE real submission against perplexity.ai — an external
  side effect (a real question is sent to your Perplexity account). The
  script pauses before that submit and requires an interactive Enter at an
  explicit confirmation prompt. States 1/3/4 are read-only page reads plus
  composer fill. Do not run this script until the user has given GO.

Usage::

    python3 scripts/probe_submit_states.py --help
    python3 scripts/probe_submit_states.py --query "用一句话回答：1+1 等于几？"
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# src-layout fallback: allow running from the repo without `pip install -e .`
_SRC = Path(__file__).resolve().parent.parent / "src"
if _SRC.is_dir() and str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from perplexity_toolkit.config import get_config  # noqa: E402
from perplexity_toolkit.console import (  # noqa: E402
    POLL_INTERVAL,
    SELFCHECK_QUERY,
    SUBMIT_TIMEOUT,
    ConsoleError,
    _JS_CLICK_SUBMIT,  # noqa: F401 — imported for signature-parity checks
    _ensure_console_tab,
    _gate_fill,
    _gate_submit,
    _info,
    _js,
    _make_driver,
    _reload_console_tab,  # v2 state-4 desync healing
    console_home,
    load_state,
)

STATE_KEYS = (
    "1_before_submit_with_draft",
    "2_during_generation",
    "3_after_done_empty_composer",
    "4_after_done_with_draft",
)


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ── v2: unfiltered button dump + submit-button context ────────────────
# The stop control is conditionally rendered in the generating state and
# may carry no aria-label; filtering empty labels would hide it, so this
# dump NEVER filters.
_JS_BUTTONS = r"""(() => {
  const out = [];
  document.querySelectorAll('button,[role="button"]').forEach((n) => {
    const r = n.getBoundingClientRect();
    const cs = window.getComputedStyle(n);
    out.push({
      tag: String(n.tagName || '').toLowerCase(),
      aria: n.getAttribute('aria-label') || '',
      title: n.getAttribute('title') || '',
      text: String(n.innerText || n.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 16),
      visible: Boolean(r.width && r.height && cs.visibility !== 'hidden'),
      cls: String(n.className || '').slice(0, 40),
    });
  });
  return JSON.stringify(out);
})()"""

_JS_SUBMIT_PARENT = r"""(() => {
  const btn = document.querySelector('button[aria-label="提交"]');
  const composer = document.querySelector('[contenteditable]');
  const src = (btn && btn.parentElement) || (composer && composer.parentElement);
  return JSON.stringify(String((src && src.outerHTML) || '').slice(0, 1500));
})()"""


def _dump_buttons(driver) -> list:
    """Every ``button``/``[role="button"]`` node — no filtering at all."""
    try:
        raw = _js(driver, _JS_BUTTONS, [])
    except Exception as exc:  # noqa: BLE001 — dump must never break a snapshot
        return [{"_error": f"{type(exc).__name__}: {exc}"}]
    if not isinstance(raw, list):
        return [{"_error": "non-list buttons result", "_raw": repr(raw)}]
    return raw


def _submit_parent_html(driver) -> str:
    """outerHTML of the submit button's parent (composer area as fallback)."""
    try:
        html = _js(driver, _JS_SUBMIT_PARENT, "")
    except Exception as exc:  # noqa: BLE001
        return f"<!-- dump failed: {type(exc).__name__}: {exc} -->"
    return html if isinstance(html, str) else json.dumps(html, ensure_ascii=False)


def _snapshot(driver) -> dict:
    """One _JS_INFO snapshot; ``.get()`` tolerates fields (e.g. stop_button)
    that a parallel change may not have added yet."""
    info = _info(driver)
    if not isinstance(info, dict):
        info = {"_error": "non-dict _JS_INFO result", "_raw": repr(info)}
    return {
        "ts": _now_iso(),
        "buttons_raw": _dump_buttons(driver),
        "submit_parent_html": _submit_parent_html(driver),
        "submit_button": info.get("submit_button"),
        "stop_button": info.get("stop_button"),   # may be absent (old _JS_INFO)
        "generating": info.get("generating"),
        "studied": info.get("studied"),
        "lastProseLen": info.get("lastProseLen"),
        "proseCount": info.get("proseCount"),
        "bubbles": info.get("bubbles"),
        "composer": info.get("composer") or "",
        "composer_len": len(info.get("composer") or ""),
        "url": info.get("url"),
        "info": info,  # full raw _JS_INFO payload
    }


def _wait_state3(driver, base_studied: int, *, wait_budget: float,
                 poll: float, sleep) -> bool:
    """v2 state-3 trigger — returns True on timeout.

    Phase A: poll ``_info`` until ``studied >= base_studied + 1`` (the new
    answer's 已研究 pill; one pill per answer, counter +1 on completion).
    Phase B: after the pill, wait 5s AND require ``lastProseLen`` equal on
    two consecutive samples (stable >= 2) before the snapshot.

    ``_gate_complete`` is deliberately NOT used: its early-exit bug
    returned true at 9 chars of prose, sampling mid-stream.
    Total wait is capped by ``wait_budget`` (--wait-budget).
    """
    deadline = time.monotonic() + max(wait_budget, 0.0)

    # Phase A — new answer's studied pill appears (+1 over baseline)
    while True:
        info = _info(driver)
        if int(info.get("studied") or 0) >= int(base_studied) + 1:
            break
        if time.monotonic() >= deadline:
            return True
        sleep(max(poll, 0.01))

    # Phase B — pill seen: wait 5s, then wait for prose stability
    sleep(5.0)
    stable = 0
    last_len: int | None = None
    while True:
        info = _info(driver)
        length = int(info.get("lastProseLen") or 0)
        if last_len is not None and length == last_len and length > 0:
            stable += 1
        else:
            stable = 0
        last_len = length
        if stable >= 2:      # 连续两次相等
            return False
        if time.monotonic() >= deadline:
            return True
        sleep(max(poll, 0.01))


def _emit(key: str, snap: dict) -> None:
    """One compact JSON line per state on stdout."""
    print(json.dumps({"state": key, "snapshot": snap},
                     ensure_ascii=False, separators=(",", ":")),
          flush=True)


def _write_evidence(states: dict, epoch: int) -> Path:
    out_dir = console_home() / "evidence"
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"probe_submit_states-{epoch}.json"
    path.write_text(
        json.dumps(states, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="probe_submit_states.py",
        description=(
            "Read-only four-state probe of _JS_INFO in the Perplexity console. "
            "State 2 performs ONE real submission (external side effect) behind "
            "an interactive confirmation."
        ),
        epilog=(
            "未获用户 GO 不得运行 (DO NOT RUN WITHOUT EXPLICIT USER GO): state 2 "
            "sends a real question to perplexity.ai; the script blocks on an "
            "Enter-to-continue prompt immediately before that submit. "
            "States 1/3/4 only read the page and fill the composer."
        ),
    )
    parser.add_argument("--query", default=SELFCHECK_QUERY,
                        help="probe query used for fill/submit (default: %(default)s)")
    parser.add_argument("--wait-budget", type=float, default=600.0,
                        help="state-3 pill+settle budget in seconds "
                             "(default: %(default)s)")
    parser.add_argument("--poll", type=float, default=POLL_INTERVAL,
                        help="poll interval in seconds (default: %(default)s)")
    parser.add_argument("--submit-timeout", type=float, default=SUBMIT_TIMEOUT,
                        help="submit ownership timeout in seconds (default: %(default)s)")
    args = parser.parse_args(argv)

    cfg = get_config()
    state = load_state()
    driver = _make_driver(cfg, state)
    _ensure_console_tab(driver, state, cfg=cfg, sleep=time.sleep)

    epoch = int(time.time())
    states: dict[str, dict] = {}
    rc = 0
    try:
        # Baselines captured pre-fill: state 3 waits for studied >= base+1
        # (the new answer's 已研究 pill). The probe bypasses the pending
        # ledger on purpose (no state.json writes).
        pre = _info(driver)

        # ── State 1: draft in composer, nothing submitted ──────────────
        _gate_fill(driver, args.query, sleep=time.sleep)
        snap1 = _snapshot(driver)
        states["1_before_submit_with_draft"] = snap1
        _emit("1_before_submit_with_draft", snap1)

        # ── GO gate: state 2 requires a REAL submission ────────────────
        print("== 即将执行唯一一次真实 submit（外部副作用：真实提问已发送到 Perplexity）。"
              "未获用户 GO 请现在 Ctrl-C 退出。 ==", flush=True)
        input("已获用户 GO，按回车继续（state 2 将提交）… ")

        # ── State 2: within ~3s of submit, while generating ────────────
        t0 = time.monotonic()
        _gate_submit(driver, args.query, int(pre.get("bubbles") or 0),
                     timeout=args.submit_timeout, poll=args.poll,
                     sleep=time.sleep)
        time.sleep(max(0.0, 3.0 - (time.monotonic() - t0)))
        snap2 = _snapshot(driver)
        states["2_during_generation"] = snap2
        _emit("2_during_generation", snap2)

        # ── State 3: 已研究药丸 (studied +1) 出现后稳定再快照 ───────────
        state3_timeout = _wait_state3(
            driver, int(pre.get("studied") or 0),
            wait_budget=args.wait_budget, poll=args.poll, sleep=time.sleep)
        snap3 = _snapshot(driver)
        if state3_timeout:
            snap3["state3_timeout"] = True  # snapshot taken at budget expiry
        states["3_after_done_empty_composer"] = snap3
        _emit("3_after_done_empty_composer", snap3)

        # ── State 4: reload 愈合 DOM/state desync 后再 fill ──────────────
        try:
            _reload_console_tab(cfg, state, sleep=time.sleep, driver=driver)
        except Exception as exc:  # noqa: BLE001 — reload is best-effort healing
            print(json.dumps({"state4_reload_error": f"{type(exc).__name__}: {exc}"},
                             ensure_ascii=False, separators=(",", ":")),
                  file=sys.stderr, flush=True)
        state4_fill_failed = False
        try:
            filled = _gate_fill(driver, args.query, sleep=time.sleep)
            if not (isinstance(filled, dict) and filled.get("ok")):
                state4_fill_failed = True
        except ConsoleError as exc:
            # fill.not-committed after reload: snapshot anyway, do NOT abort
            state4_fill_failed = True
            print(json.dumps({"state4_fill_error": {"code": exc.code,
                                                    "message": exc.message}},
                             ensure_ascii=False, separators=(",", ":")),
                  file=sys.stderr, flush=True)
        except Exception as exc:  # noqa: BLE001 — never interrupt the probe here
            state4_fill_failed = True
            print(json.dumps({"state4_fill_error": f"{type(exc).__name__}: {exc}"},
                             ensure_ascii=False, separators=(",", ":")),
                  file=sys.stderr, flush=True)
        snap4 = _snapshot(driver)
        if state4_fill_failed:
            snap4["state4_fill_failed"] = True
        states["4_after_done_with_draft"] = snap4
        _emit("4_after_done_with_draft", snap4)

    except ConsoleError as exc:
        print(json.dumps({"error": "ConsoleError", "gate": exc.gate,
                          "code": exc.code, "message": exc.message,
                          "evidence": exc.evidence},
                         ensure_ascii=False, separators=(",", ":")),
              file=sys.stderr, flush=True)
        rc = 1
    except KeyboardInterrupt:
        print("\naborted by user (Ctrl-C); partial evidence will be written",
              file=sys.stderr, flush=True)
        rc = 130
    finally:
        # Evidence is written even for partial runs (any state captured so far).
        try:
            path = _write_evidence(states, epoch)
            print(json.dumps({"evidence": str(path),
                              "states_captured": sorted(states),
                              "expected": list(STATE_KEYS)},
                             ensure_ascii=False, separators=(",", ":")),
                  flush=True)
        except OSError as exc:
            print(json.dumps({"evidence_error": str(exc)},
                             ensure_ascii=False, separators=(",", ":")),
                  file=sys.stderr, flush=True)
            if rc == 0:
                rc = 1
    return rc


if __name__ == "__main__":
    sys.exit(main())
