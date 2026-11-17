"""Resident Perplexity console — one long-lived tab/group with verified steps.

Design (live-mapped against the perplexity.ai web UI, 2026-09-21):

* One WebBridge session ("perplexity-console") owns one tab inside the group
  "Perplexity 控制台". Every console task shares that single tab; a *task*
  maps to one Perplexity thread (conversation) inside it.
* WebBridge session→tab mappings live only in the daemon's memory and are
  lost when the daemon restarts, so the durable console state is this
  module's JSON state file (session, group title, per-task thread URL).
  Attach-or-recreate reads it back: reuse the live tab when present,
  otherwise reopen the saved thread URL in a fresh tab of the same
  session/group. The Perplexity thread itself lives server-side, so the
  persisted URL restores continuity across browser and daemon restarts.
* Every step carries a readback gate. A gate that cannot be verified raises
  ConsoleError with a screenshot path — the console never reports an
  unverified step as success:
    1. fill      — composer text EQUALS the query. ``fill`` is this editor's
                   only reliable mutation path (CDP keys, execCommand and
                   DOM/range edits are reverted by the editor's controlled
                   re-render, and empty/whitespace fill values are silent
                   no-ops). A late async draft-restore can merge extra text
                   into the composer after the fill gate passed, so the
                   equality is re-verified and re-filled immediately before
                   submit (observed live 2026-09-21: merged draft + query
                   produced a polluted submission).
    2. submit    — a new user bubble exists whose text equals the query or
                   begins with it; "contains" alone proved too weak.
    3. complete  — the studied-pill count increased AND the turn-scoped
                   answer text stopped changing
    4. extract   — the latest answer (`div.prose`, turn-scoped) is non-empty
* Turn scoping: the answer is extracted from the LAST ``div.prose`` element,
  never from ``main.innerText`` (which spans the whole thread). The current
  UI can retain text in the composer after submission, so the composer is NOT
  used as the submit signal; user-bubble ownership is authoritative.
"""

from __future__ import annotations

import base64
import datetime
import hashlib
import json
import logging
import mimetypes
import os
import re
import time
from pathlib import Path
from typing import Any, Callable, Optional, Sequence

from . import console_judge
from .config import Config, get_config
from .utils.i18n import get_ui_string

logger = logging.getLogger(__name__)

DEFAULT_SESSION = "perplexity-console"
DEFAULT_GROUP_TITLE = "Perplexity 控制台"
BASE_URL = "https://www.perplexity.ai/"
HREF_MATCH_SLACK = "/search/"

DEFAULT_WAIT = 120.0          # seconds, completion budget
POLL_INTERVAL = 3.0           # seconds between completion samples
SUBMIT_TIMEOUT = 15.0         # seconds to observe the new user turn
FILL_SETTLE = 0.7             # seconds after a fill/CDP insert before readback
SELFCHECK_QUERY = "用一句话回答：1+1 等于几？"

# Circuit breaker for polling/wait loops: N consecutive samples with zero
# substantive progress fail the step early instead of spinning to the
# timeout (lesson: a repeated action that "keeps doing something" only
# because the page wiggled by a sub-pixel must never look like progress).
NO_PROGRESS_LIMIT = 3


SUBMIT_ICON_IDLE = "#pplx-icon-arrow-up"   # live-verified idle action icon (2026-09-23)


def _answer_settled(info: dict, prev_len: int, stable: int, *, new_seen: bool) -> tuple[bool, str]:
    """Completion decision for `_gate_complete` — deterministic signals only.

    Live-verified semantics (2026-09-23 four-state probe):
    - the action button keeps aria-label 提交 while generating (disabled once the
      composer clears) — its STATE cannot discriminate busy/done;
    - its inner `svg use` ICON morphs instead: idle == SUBMIT_ICON_IDLE, any
      other/unreadable-but-present icon == busy (inverted guard, no need to
      know the stop icon's name);
    - the 已研究 pill appears only on Pro-Search turns — advisory at best;
    - the whole-page `generating` regex is pinned true by the model badge
      (『… 正在思考』) — ignored entirely.

    done ⟺ new_seen ∧ length>0 ∧ length==prev_len ∧ stable≥2
            ∧ no visible stop control ∧ action icon idle (or probe blank →
              signal downgraded to "length-only").
    """
    length = int(info.get("lastProseLen") or 0)
    if not new_seen or length <= 0 or length != prev_len or stable < 2:
        return False, ""
    if info.get("stop_button"):
        return False, ""
    icon = info.get("action_icon") or ""
    if icon and icon != SUBMIT_ICON_IDLE:
        return False, ""
    return True, ("icon+stable" if icon == SUBMIT_ICON_IDLE else "length-only")

# ──────────────────────────────────────────────────────────────
# JS snippets (markers are relied on by tests: 'user-bubble', 'cloneNode',
# "a[href]", '提交', 'dispatchEvent', "=== '展开'").
# ──────────────────────────────────────────────────────────────

_JS_INFO_TMPL = r"""(() => {
  const btns = Array.from(document.querySelectorAll('button'));
  const bubbles = Array.from(document.querySelectorAll('[class*="user-bubble"]'))
    .filter(el => !String(el.className || '').includes('opacity-0'));
  const main = document.querySelector('main');
  const prose = main ? Array.from(main.querySelectorAll('div.prose')) : [];
  const ce = document.querySelector('[contenteditable]');
  const area = ce ? (ce.closest('form') || ce.parentElement.parentElement.parentElement.parentElement) : document.body;
  const modelBtns = Array.from(area.querySelectorAll('button')).filter(b => b.getAttribute('aria-haspopup') === 'menu' && (b.getAttribute('aria-label') || '').length > 0 && !/添加文件或工具|草稿/.test(b.getAttribute('aria-label')));
  const modelBtn = modelBtns.length ? modelBtns[modelBtns.length - 1] : null;
  return JSON.stringify({
    url: location.href,
    title: document.title,
    composer: ce ? String(ce.innerText || '') : '',
    model: modelBtn ? (modelBtn.getAttribute('aria-label') || '') : '',
    submit_button: (() => {
      const root = main || document;
      const b = root.querySelector(
        'button[aria-label="提交"],button[aria-label="搜索"],button[aria-label="Submit"]'
      );
      return b ? (b.disabled ? "disabled" : "enabled") : "missing";
    })(),
    action_icon: (() => {
      const root = (typeof main !== 'undefined' && main) || document;
      const b = root.querySelector('button[aria-label="提交"],button[aria-label="搜索"],button[aria-label="Submit"]');
      const use = b ? b.querySelector('svg use') : null;
      return use ? (use.getAttribute('xlink:href') || use.getAttribute('href') || '') : '';
    })(),
    stop_button: [...document.querySelectorAll(
      'button[aria-label*="停止"],button[aria-label*="Stop" i]'
    )].some(b => (b.checkVisibility?.() ?? b.offsetParent !== null)),
    bubbles: bubbles.length,
    lastBubble: bubbles.length ? String(bubbles[bubbles.length - 1].innerText || '').slice(0, 300) : '',
    studied: btns.filter(b => String(b.innerText || '').includes(__STUDIED__)).length,
    generating: /正在|思考中|generating/i.test(document.body.textContent || ''),
    proseCount: prose.length,
    lastProseLen: prose.length ? String(prose[prose.length - 1].innerText || '').length : 0
  });
})()"""

_JS_PROSE = r"""(() => {
  const main = document.querySelector('main');
  if (!main) return JSON.stringify({found: false});
  const prose = Array.from(main.querySelectorAll('div.prose'));
  if (!prose.length) return JSON.stringify({found: false});
  const el = prose[prose.length - 1];
  const clone = el.cloneNode(true);
  clone.querySelectorAll('a[href], button').forEach(n => n.remove());
  return JSON.stringify({
    found: true,
    text: String(clone.innerText || '').trim(),
    raw: String(el.innerText || '').trim()
  });
})()"""

# Scroll the answer's scrollable container to its bottom before extraction.
# Discovery: walk up from the LAST div.prose to the first overflow-y
# auto/scroll ancestor with real overflow (scrollHeight > clientHeight + 4),
# falling back to document.scrollingElement. Live DOM (2026-09-23): the
# container found this way is `div.scrollable-container.overflow-auto`
# (inside <main>, the prose's scrollable ancestor).
_JS_SCROLL = r"""(() => {
  const m = document.querySelector("main");
  const lastProse = [...(m ? m.querySelectorAll("div.prose") : document.querySelectorAll("div.prose"))].pop();
  let container = null;
  for (let n = lastProse; n && n !== document.body; n = n.parentElement) {
    const oy = getComputedStyle(n).overflowY;
    if ((oy === "auto" || oy === "scroll") && n.scrollHeight > n.clientHeight + 4) { container = n; break; }
  }
  if (!container) container = document.scrollingElement || document.documentElement;
  const before = container.scrollTop;
  container.scrollTop = container.scrollHeight;
  window.scrollTo(0, document.body.scrollHeight);
  return { bottom: container.scrollTop + container.clientHeight >= container.scrollHeight - 8,
           height: container.scrollHeight, scrolled: container.scrollTop !== before,
           container: container.tagName + (container.className ? "." + String(container.className).split(" ")[0] : "") };
})()"""

_JS_SOURCES = r"""(() => {
  const main = document.querySelector('main');
  if (!main) return JSON.stringify([]);
  const seen = new Set();
  const out = [];
  for (const a of main.querySelectorAll('a[href]')) {
    const href = a.href || '';
    if (!href.startsWith('http') || href.includes('perplexity.ai')) continue;
    if (seen.has(href)) continue;
    seen.add(href);
    out.push({text: String(a.textContent || '').trim().slice(0, 200), href: href});
  }
  return JSON.stringify(out);
})()"""

_JS_CLICK_SUBMIT = r"""(() => {
  const sels = ['button[aria-label="提交"]', 'button[aria-label="搜索"]', 'button[aria-label="Submit"]'];
  for (const s of sels) {
    const btn = document.querySelector(s);
    if (btn) { btn.click(); return 'clicked:' + s; }
  }
  const btns = Array.from(document.querySelectorAll('button'));
  const t = btns.find(b => { const x = String(b.innerText || '').trim(); return x === '搜索' || x === '提交' || x === 'Submit'; });
  if (t) { t.click(); return 'clicked:text'; }
  return 'no-button';
})()"""

_JS_ENTER_COMBO = r"""(() => {
  const el = document.querySelector('[contenteditable]');
  if (!el) return 'no input';
  el.dispatchEvent(new InputEvent('beforeinput', {inputType: 'insertText', data: '\n', bubbles: true, cancelable: true}));
  el.dispatchEvent(new KeyboardEvent('keydown', {key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true, cancelable: true}));
  el.dispatchEvent(new KeyboardEvent('keyup', {key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true, cancelable: true}));
  return 'enter dispatched';
})()"""

_JS_EXPAND_TMPL = r"""(() => {
  const btns = Array.from(document.querySelectorAll('button'))
    .map(b => [b, String(b.innerText || '').trim()]);
  // Exact label match wins (trim + ===). The legacy includes() rung is a
  // LAST-RESORT fallback: it only fires when NO exact match exists AND the
  // button text is essentially just the label (<=2 chars of icon/punctuation
  // noise, no question mark), so question buttons carrying the label as a
  // substring (e.g. the follow-up 「怎么查看更多细节？」) are never clicked —
  // clicking them would submit a question inside a read-only extraction step.
  const near = (t, lab) => t.includes(lab) && t.length - lab.length <= 2
                           && !/[？?]/.test(t);
  const exact = btns.filter(([b, t]) => t === __EXPAND__ || t === __LEGACY__);
  const loose = exact.length ? []
    : btns.filter(([b, t]) => near(t, __EXPAND__) || near(t, __LEGACY__));
  const pool = exact.length ? exact : loose;
  if (!pool.length) return 'none';
  pool[pool.length - 1][0].click();
  return 'clicked';
})()"""

_JS_MODEL_BTN = r"""(() => {
  const ce = document.querySelector('[contenteditable]');
  const area = ce ? (ce.closest('form') || ce.parentElement.parentElement.parentElement.parentElement) : document.body;
  const cands = Array.from(area.querySelectorAll('button')).filter(b => b.getAttribute('aria-haspopup') === 'menu' && (b.getAttribute('aria-label') || '').length > 0 && !/添加文件或工具|草稿/.test(b.getAttribute('aria-label')));
  const b = cands.length ? cands[cands.length - 1] : null;
  if (!b) return JSON.stringify({found: false});
  const r = b.getBoundingClientRect();
  return JSON.stringify({found: true, label: b.getAttribute('aria-label') || String(b.innerText || '').trim(),
    expanded: b.getAttribute('aria-expanded') === 'true',
    x: Math.round(r.x + r.width / 2), y: Math.round(r.y + r.height / 2)});
})()"""

_JS_VISIBILITY = r"""(() => {
  return JSON.stringify({visible: document.visibilityState === 'visible',
                         visibilityState: document.visibilityState,
                         hidden: !!document.hidden});
})()"""

_JS_MODEL_MENU = r"""(() => {
  const menu = document.querySelector('[role=menu]');
  if (!menu) return JSON.stringify({open: false, rows: []});
  const rows = Array.from(menu.querySelectorAll('[data-radix-collection-item], [role^=menuitem]')).map(r => {
    const b = r.getBoundingClientRect();
    const parts = String(r.innerText || '').split('\n').map(s => s.trim()).filter(Boolean);
    return {name: parts[0] || '', badges: parts.slice(1),
            role: r.getAttribute('role'), checked: r.getAttribute('aria-checked') === 'true',
            submenu: r.getAttribute('role') === 'menuitem',
            x: Math.round(b.x + b.width / 2), y: Math.round(b.y + b.height / 2),
            vis: !!r.offsetParent};
  });
  return JSON.stringify({open: true, rows: rows});
})()"""

_JS_CHIPS_TMPL = r"""(() => {
  const PREFIX = __PREFIX__;
  const labels = Array.from(document.querySelectorAll('button'))
    .map(b => b.getAttribute('aria-label') || '')
    .filter(a => a.indexOf(PREFIX) === 0)
    .map(a => a.slice(PREFIX.length));
  return JSON.stringify({attachments: labels});
})()"""

_JS_INJECT_FILE = r"""(() => {
  const input = document.querySelector('input[type=file]');
  if (!input) return JSON.stringify({ok: false, why: 'no-input'});
  const bin = atob(__B64__);
  const arr = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) arr[i] = bin.charCodeAt(i);
  const dt = new DataTransfer();
  dt.items.add(new File([arr], __NAME__, {type: __MIME__}));
  input.files = dt.files;
  input.dispatchEvent(new Event('change', {bubbles: true}));
  return JSON.stringify({ok: true, count: input.files.length, size: arr.length});
})()"""


# ──────────────────────────────────────────────────────────────
# Element-table fallback probes (second rung of the fail-closed ladder)
#
# The console has two "whole-run stops" (audit 2026-09-28): the answer text
# is `main div.prose` (_JS_INFO/_JS_PROSE/_JS_SCROLL) and submit ownership
# is the `[class*="user-bubble"]` completion anchor (_wait_ownership). These
# probes give both a SECOND rung — `probe → element-table rung →
# probe.fallback-exhausted` — under the external review's ruling:
#
#   D1=A  the fallback target choice is a PURE deterministic heuristic (no
#         LLM); it only ever produces CANDIDATES, and a candidate is adopted
#         only after a semantic readback (and, for actions, an effect check);
#   D2=A  when the fallback also fails: unified error code
#         `probe.fallback-exhausted`, fail-closed, never a half result;
#   D3=B  every fallback trigger appends a runs.jsonl event carrying a
#         sanitized hit-element snapshot summary (role/label/text head with
#         URL query strings and suspected tokens stripped, ≤80 chars); the
#         drift report shows the cumulative count and recent summaries.
#
# WARN (highest constraint): composer state, URL changes and count changes
# can NEVER prove submit ownership on their own. Ownership is only claimed
# with an independent identity binding (this turn's query text present in
# the page/thread — never in the composer) PLUS an effect signal (the
# answer area starts growing or the completion-marker count increases).
#
# All probes below are locale-neutral and read-only (the expand rung's
# click goes through trusted CDP mouse events, not through these probes).
# Each carries a /*PPLX_*_PROBE*/ marker so test doubles can dispatch on
# an unambiguous signature.
# ──────────────────────────────────────────────────────────────

# Minimal element table: atomic read of VISIBLE controls only — index,
# role, aria-label, innerText ≤120 chars, rect, disabled. Read-only: no
# click, no input, no scroll (relied on by tests and the drift selfcheck).
_JS_TABLE = r"""/*PPLX_TABLE_PROBE*/(() => {
  const vis = (el) => { try { return el.checkVisibility ? el.checkVisibility() : el.offsetParent !== null; } catch (e) { return true; } };
  const nodes = document.querySelectorAll('button, a, [role="button"], [role="link"], [role="tab"], [role="menuitem"], [role="menuitemradio"], [role="option"], input, select, textarea, summary, [contenteditable]');
  const out = [];
  let i = 0;
  for (const el of nodes) {
    if (el.tagName.toLowerCase() === 'a' && !el.hasAttribute('href')) continue;
    if (!vis(el)) continue;
    const r = el.getBoundingClientRect();
    if (r.width < 1 || r.height < 1) continue;
    out.push({i: i++, tag: el.tagName.toLowerCase(),
      role: el.getAttribute('role') || '',
      label: el.getAttribute('aria-label') || '',
      text: String(el.innerText || el.value || '').trim().slice(0, 120),
      rect: {x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height)},
      disabled: !!(el.disabled || el.getAttribute('aria-disabled') === 'true')});
    if (out.length >= 200) break;
  }
  return JSON.stringify({items: out, count: out.length});
})()"""

# Content-block candidates for the prose rung: visible block containers with
# their text, container semantics and a chrome hint (nav/aside/footer/header
# /sidebar-ish) computed from tag/role/class ancestry so the deterministic
# scorer in Python can exclude navigation chrome by role/aria/position.
_JS_BLOCKS = r"""/*PPLX_BLOCKS_PROBE*/(() => {
  const vis = (el) => { try { return el.checkVisibility ? el.checkVisibility() : el.offsetParent !== null; } catch (e) { return true; } };
  const hintOf = (el) => {
    for (let n = el; n && n !== document.body; n = n.parentElement) {
      const tag = n.tagName ? n.tagName.toLowerCase() : '';
      const role = n.getAttribute ? (n.getAttribute('role') || '') : '';
      const cls = String((typeof n.className === 'string' ? n.className : '') || '');
      if (tag === 'nav' || role === 'navigation') return 'nav';
      if (tag === 'aside' || role === 'complementary') return 'aside';
      if (tag === 'footer' || role === 'contentinfo') return 'footer';
      if (tag === 'header' || role === 'banner') return 'header';
      if (/sidebar|side-bar|rail|footer|nav-|menu-/.test(cls)) return 'chrome';
    }
    return '';
  };
  const out = [];
  let i = 0;
  for (const el of document.querySelectorAll('main, article, [role="main"], section, div')) {
    if (!vis(el)) continue;
    const t = String(el.innerText || '').trim();
    if (t.length < 80) continue;
    const r = el.getBoundingClientRect();
    out.push({i: i++, tag: el.tagName.toLowerCase(),
      role: el.getAttribute('role') || '',
      label: el.getAttribute('aria-label') || '',
      cls: String(typeof el.className === 'string' ? el.className : '').slice(0, 80),
      hint: hintOf(el), len: t.length, text: t.slice(0, 4000),
      rect: {x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height)}});
    if (out.length >= 40) break;
  }
  return JSON.stringify({blocks: out, count: out.length});
})()"""

# Identity binding for the ownership rung: does THIS turn's query text (the
# exact fill string) appear in the thread/page as text? Normalized-whitespace
# containment. WARN (red line): the composer subtree is NEVER evidence — the
# query sits there before/without a submit — and neither is any ANCESTOR of
# the composer (main/body innerText includes composer text; the historical
# containment check on those is exactly the silent-send-failure false bind).
# Containment runs on skip-excluded text only and `bound:true` requires the
# evidence to land on ONE concrete non-composer element with non-empty text.
_JS_BOUND_TMPL = r"""/*PPLX_BOUND_PROBE*/(() => {
  const q = __QUERY__;
  const norm = (s) => String(s || '').replace(/\s+/g, ' ').trim();
  const nq = norm(q);
  const out = {bound: false, where: '', tag: '', role: '', label: '', text: ''};
  if (!nq) return JSON.stringify(out);
  const all = Array.from(document.querySelectorAll('*'));
  // skip roots: EVERY contenteditable's form/parent — the composer subtree
  // in all its shapes (multiple editors, missing form wrapper, ...)
  const roots = [];
  for (const ce of document.querySelectorAll('[contenteditable]')) {
    let root = ce;
    try { root = ce.closest('form') || ce.parentElement || ce; } catch (e) {}
    if (root && roots.indexOf(root) === -1) roots.push(root);
  }
  const under = (el, root) => { for (let n = el; n; n = n.parentElement) { if (n === root) return true; } return false; };
  // dead = composer subtree member, composer ANCESTOR (its innerText carries
  // composer text too), or non-rendered metadata
  const dead = (el) => {
    const tag = String(el.tagName || '').toLowerCase();
    if (tag === 'script' || tag === 'style' || tag === 'noscript'
        || tag === 'template' || tag === 'head') return true;
    for (const r of roots) { if (under(el, r) || under(r, el)) return true; }
    return false;
  };
  // containment on skip-excluded text only: the innerText of the OUTERMOST
  // live elements — never body/main innerText (both can carry the composer)
  const main = document.querySelector('main');
  const tops = [];
  for (const el of all) {
    if (dead(el)) continue;
    let nested = false;
    for (let p = el.parentElement; p; p = p.parentElement) {
      if (!dead(p)) { nested = true; break; }
    }
    if (!nested) tops.push(el);
  }
  const textOf = (els) => norm(els.map((e) => e.innerText || e.textContent || '').join(' '));
  const mainText = textOf(tops.filter((e) => main && under(e, main)));
  const pageText = textOf(tops);
  if (main && mainText.includes(nq)) out.where = 'thread';
  else if (pageText.includes(nq)) out.where = 'page';
  else return JSON.stringify(out);
  // bound:true ONLY when the text evidence lands on one concrete
  // non-composer element (WARN: never on composer state)
  let best = null, bestLen = Infinity;
  for (const el of all) {
    if (dead(el)) continue;
    const t = norm(el.innerText || el.textContent || '');
    if (!t || !t.includes(nq)) continue;
    if (t.length < bestLen) { best = el; bestLen = t.length; }
  }
  const btext = best ? norm(best.innerText || best.textContent || '') : '';
  if (best && btext) {
    out.bound = true;
    out.tag = String(best.tagName || '').toLowerCase();
    out.role = best.getAttribute('role') || '';
    out.label = best.getAttribute('aria-label') || '';
    out.text = btext.slice(0, 120);
  }
  return JSON.stringify(out);
})()"""

# Pre-action geometry/occlusion re-check (融合项 d, narrow): before a
# click/fill fires on cached coordinates or a selector target, the action
# point is re-verified ONCE more against the live DOM:
#
#   (a) the target rect must be non-degenerate (w/h ≥ 1) and sit inside the
#       viewport — a rect whose centre leaves the viewport is unusable;
#   (b) `document.elementFromPoint(cx, cy)` at the target's CENTRE must hit
#       the target itself or an element inside its subtree; the target being
#       an ANCESTOR of the hit (point lands on a container) also counts.
#       A floating layer/弹窗 covering the target makes elementFromPoint
#       return the LAYER (rel 'other') → unusable.
#
# Input spec (JSON-injected, `__SPEC__`): {"selector": css} | {"selectors":
# [css, …]} (first match wins, mirroring `_JS_CLICK_SUBMIT`) | {"rect":
# {x, y, w, h}} (cached coordinates; the target is re-identified by a
# matching rect near the hit — hit's ancestor-or-self chain or subtree).
# Read-only: no click, no input, no scroll. Returns JSON like the other
# probes: {ok, reason, rel, target, hit}; `reason` is '' on success and one
# of not-found / no-spec / not-visible / degenerate / off-viewport / no-hit /
# occluded otherwise. The /*PPLX_HITTEST_PROBE*/ marker lets test doubles
# dispatch on an unambiguous signature (same convention as the rung-2
# probes); it sits INSIDE the IIFE body — not as the source prefix — so the
# rung-2 bookkeeping (`pplx_probes`, sources starting with `/*PPLX_`) keeps
# meaning "element-table rung probes only": this gate is a different class.
# The spec is injected with ``ensure_ascii=True`` so UI-label
# literals (submit selectors) never appear verbatim in the executed source.
_JS_HITTEST_TMPL = r"""(() => {
  /*PPLX_HITTEST_PROBE*/
  const spec = __SPEC__;
  const out = {ok: false, reason: '', rel: '', target: null, hit: null};
  const desc = (el) => {
    if (!el || !el.tagName) return null;
    return {tag: String(el.tagName).toLowerCase(),
            role: (el.getAttribute && el.getAttribute('role')) || '',
            label: (el.getAttribute && el.getAttribute('aria-label')) || '',
            text: String(el.innerText || el.textContent || '').trim().slice(0, 120)};
  };
  const vis = (el) => {
    try { return el.checkVisibility ? el.checkVisibility() : el.offsetParent !== null; }
    catch (e) { return true; }
  };
  const boxOf = (r) => ({x: Number(r.x) || 0, y: Number(r.y) || 0,
    w: Number(r.width !== undefined ? r.width : r.w) || 0,
    h: Number(r.height !== undefined ? r.height : r.h) || 0});
  const box = (el) => boxOf(el.getBoundingClientRect());
  let target = null, rect = null;
  const sel = String(spec.selector || '');
  const sels = (spec.selectors && spec.selectors.length) ? spec.selectors
             : (sel ? [sel] : []);
  if (sels.length) {
    for (const s of sels) {
      const el = document.querySelector(String(s));
      if (el) { target = el; break; }
    }
    if (!target) { out.reason = 'not-found'; return JSON.stringify(out); }
    rect = box(target);
    out.target = desc(target);
    if (!vis(target)) { out.reason = 'not-visible'; return JSON.stringify(out); }
  } else if (spec.rect) {
    rect = boxOf(spec.rect);
  } else {
    out.reason = 'no-spec'; return JSON.stringify(out); }
  const vw = Number(window.innerWidth) || 0, vh = Number(window.innerHeight) || 0;
  if (!(rect.w >= 1) || !(rect.h >= 1)) {
    out.reason = 'degenerate'; return JSON.stringify(out); }
  if (rect.x + rect.w <= 0 || rect.y + rect.h <= 0 || rect.x >= vw || rect.y >= vh) {
    out.reason = 'off-viewport'; return JSON.stringify(out); }
  const cx = Math.trunc(rect.x) + Math.trunc(rect.w / 2), cy = Math.trunc(rect.y) + Math.trunc(rect.h / 2);
  if (cx < 0 || cy < 0 || cx >= vw || cy >= vh) {
    out.reason = 'off-viewport'; return JSON.stringify(out); }
  const hit = document.elementFromPoint(cx, cy);
  if (!hit) { out.reason = 'no-hit'; return JSON.stringify(out); }
  out.hit = desc(hit);
  const relOf = (el) => (el === hit) ? 'self'
    : (el.contains(hit) ? 'descendant'
    : (hit.contains(el) ? 'ancestor' : 'other'));
  if (target) {
    out.rel = relOf(target);
    if (out.rel === 'other') { out.reason = 'occluded'; return JSON.stringify(out); }
    out.ok = true;
    return JSON.stringify(out);
  }
  // rect mode: the cached target is re-identified by its rect (±2px) among
  // the hit's ancestor-or-self chain and subtree; no match ⇒ the point no
  // longer lands in the candidate's subtree (occluded / moved) ⇒ unusable.
  const tol = 2;
  const same = (a, b) => Math.abs(a.x - b.x) <= tol && Math.abs(a.y - b.y) <= tol
    && Math.abs(a.w - b.w) <= tol && Math.abs(a.h - b.h) <= tol;
  let all = [];
  try { all = Array.from(document.querySelectorAll('*')); } catch (e) { all = []; }
  for (const el of all) {
    if (!el || !el.tagName || typeof el.getBoundingClientRect !== 'function') continue;
    let r = null;
    try { r = box(el); } catch (e) { continue; }
    if (!same(r, rect)) continue;
    out.target = desc(el);
    out.rel = relOf(el);
    if (out.rel !== 'other') { out.ok = true; return JSON.stringify(out); }
  }
  out.reason = 'occluded';
  out.rel = 'other';
  return JSON.stringify(out);
})()"""

# Import-time binding kept for introspection (same convention as `_JS_INFO`).
_JS_HITTEST = _JS_HITTEST_TMPL

# ──────────────────────────────────────────────────────────────
# Locale-aware probe assembly
#
# Three probes embed UI text (studied pill / expand control / attachment-chip
# aria-label prefix); the rest are locale-neutral. Those three are built from
# utils.i18n so an `en` console matches the English UI, and with the default
# locale (zh) the INJECTED LITERALS reproduce the historical source byte for
# byte — the marker strings the tests/FakeDriver dispatch on (=== '展开', 移除 ,
# 已研究) survive verbatim. The probe source AS A WHOLE is not byte-identical
# to the historical constants: `_JS_CHIPS` is only semantically equivalent
# (PREFIX-based slicing instead of the old hard-coded slice(3)) and
# `_JS_EXPAND`'s legacy rung was tightened (exact label match first).
# `_probe(name)` re-resolves the locale on every call; the module
# level `_JS_*` constants are the import-time binding kept for introspection
# and the drift report's static checks.
# ──────────────────────────────────────────────────────────────

def _js_str(value: Any) -> str:
    """Single-quoted JS string literal (keeps the historical `=== '展开'` shape)."""
    return "'" + str(value).replace("\\", "\\\\").replace("'", "\\'") + "'"


def _probe_locale() -> str:
    """Active UI locale for label-bearing probes ('zh' unless configured)."""
    try:
        return get_config().locale or "zh"
    except Exception:  # noqa: BLE001 — a broken config must never break probing
        return "zh"


def _build_info(locale: str) -> str:
    return _JS_INFO_TMPL.replace("__STUDIED__", _js_str(get_ui_string("studied", locale)))


def _build_expand(locale: str) -> str:
    # new-UI label (exact match) + legacy rung 「查看更多」 — exact match
    # first, `includes` only as a last resort when no exact match exists
    # (see _JS_EXPAND_TMPL), mirroring skills/perplexity-web-automation/SKILL.md.
    return (_JS_EXPAND_TMPL
            .replace("__EXPAND__", _js_str(get_ui_string("expand", locale)))
            .replace("__LEGACY__", _js_str(get_ui_string("show_more", locale))))


def _build_chips(locale: str) -> str:
    return _JS_CHIPS_TMPL.replace("__PREFIX__", _js_str(get_ui_string("remove_prefix", locale)))


_PROBE_BUILDERS: dict = {"info": _build_info, "expand": _build_expand, "chips": _build_chips}
_PROBE_CACHE: dict = {}


def _probe(name: str) -> str:
    """Source of probe ``name`` for the CURRENT locale (cached per locale)."""
    locale = _probe_locale()
    key = (name, locale)
    if key not in _PROBE_CACHE:
        _PROBE_CACHE[key] = _PROBE_BUILDERS[name](locale)
    return _PROBE_CACHE[key]


_JS_INFO = _probe("info")
_JS_EXPAND = _probe("expand")
_JS_CHIPS = _probe("chips")


# ──────────────────────────────────────────────────────────────
# Errors
# ──────────────────────────────────────────────────────────────

class ConsoleError(RuntimeError):
    """A console gate failed. Carries the gate name, evidence path and a
    machine-readable error code so callers (intent layer) can pick a
    recovery recipe per failure class."""

    def __init__(self, gate: str, message: str, *,
                 gates: Optional[dict] = None,
                 evidence: Optional[str] = None,
                 code: Optional[str] = None):
        super().__init__(f"[{gate}] {message}")
        self.gate = gate
        self.message = message
        self.gates = gates or {}
        self.evidence = evidence
        self.code = code


# ──────────────────────────────────────────────────────────────
# State file
# ──────────────────────────────────────────────────────────────

def console_home() -> Path:
    """Console state directory (override with PERPLEXITY_CONSOLE_HOME)."""
    return Path(os.environ.get("PERPLEXITY_CONSOLE_HOME", "~/.perplexity-console")).expanduser()


def state_path() -> Path:
    return console_home() / "state.json"


def _default_state() -> dict:
    return {
        "version": 1,
        "session": DEFAULT_SESSION,
        "group_title": DEFAULT_GROUP_TITLE,
        "active_task": None,
        "threads": {},
        "pending": None,
        "open_url": None,
        "open_url_at": None,
    }


def load_state() -> dict:
    """Read the console state file; missing/corrupt files yield defaults."""
    path = state_path()
    state = _default_state()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return state
    if isinstance(data, dict):
        for key in ("version", "session", "group_title", "active_task", "pending",
                    "open_url", "open_url_at"):
            if key in data:
                state[key] = data[key]
        if isinstance(data.get("threads"), dict):
            state["threads"] = data["threads"]
    return state


def save_state(state: dict) -> None:
    """Atomically persist the console state."""
    path = state_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(tmp, path)


# ──────────────────────────────────────────────────────────────
# Staged turn ("pending") ledger
#
# Granular commands (fill → submit → wait → extract) compose through this
# record: fill stages it with the pre-submit baselines, submit/wait/extract
# consume it. It is what makes step-by-step intent-driven use safe — each
# step knows exactly which turn it belongs to.
# ──────────────────────────────────────────────────────────────

PENDING_TTL = 1800.0  # seconds a staged turn stays valid


def _pending(state: dict) -> dict:
    p = state.get("pending")
    return p if isinstance(p, dict) else {}


def _pending_age_seconds(p: dict) -> float:
    ts = p.get("filled_at")
    if not ts:
        return 0.0
    try:
        dt = datetime.datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ").replace(
            tzinfo=datetime.timezone.utc)
        return (datetime.datetime.now(datetime.timezone.utc) - dt).total_seconds()
    except ValueError:
        return 0.0


def _pending_require(state: dict, *, stage: str) -> dict:
    p = _pending(state)
    if not p or not p.get("query"):
        raise ConsoleError(
            "pending",
            f"no staged turn for `{stage}`; run `perplexity console fill \"...\"` first",
            code="pending.missing")
    if stage in ("submit", "wait") and _pending_age_seconds(p) > PENDING_TTL:
        raise ConsoleError(
            "pending",
            f"staged turn is stale (>{int(PENDING_TTL / 60)} min old); re-run `console fill`",
            code="pending.stale")
    if stage == "submit" and p.get("submitted_at"):
        raise ConsoleError(
            "pending",
            "this turn was already submitted; use `console wait` / `console extract`, "
            "or `console fill` to stage a new turn",
            code="pending.already-submitted")
    if stage == "wait" and not p.get("submitted_at"):
        raise ConsoleError(
            "pending",
            "turn not submitted yet; run `console submit` first",
            code="pending.not-submitted")
    return p


def _log_run(op: str, *, ok: bool = True, gate: Optional[str] = None,
             url: Optional[str] = None, elapsed: Optional[float] = None,
             truncation_risk: Optional[bool] = None,
             error: Optional[str] = None) -> None:
    """Append one compact line to runs.jsonl (best-effort observability)."""
    try:
        path = console_home() / "runs.jsonl"
        path.parent.mkdir(parents=True, exist_ok=True)
        rec: dict = {"ts": _now_iso(), "op": op, "ok": bool(ok)}
        if gate:
            rec["gate"] = gate
        if url:
            rec["url"] = url
        if elapsed is not None:
            rec["elapsed_s"] = round(elapsed, 1)
        if truncation_risk is not None:
            rec["truncation_risk"] = bool(truncation_risk)
        if error is not None:
            rec["error"] = error
        with path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    except OSError:
        pass


# Codes that make a submit worth re-attaching once (T8): the staged page
# moved away, or the WebBridge lost the tab. Everything else fails fast.
_REATTACH_CODES = frozenset({"pending.page-moved", "attach.bad-response",
                             "attach.disconnected", "attach.no-tab"})


def _fail_log(op: str, exc: ConsoleError, state: Optional[dict], *,
              elapsed_s: Optional[float] = None) -> None:
    """Record a FAILED operation in runs.jsonl (T8): ok=False + error code.

    Best-effort like ``_log_run`` (never raises, never re-raises ``exc``):
    callers invoke it at the final re-raise exit so each failure is written
    exactly once.
    """
    url = None
    if isinstance(state, dict):
        p = state.get("pending")
        if isinstance(p, dict):
            url = p.get("url")
    _log_run(op, ok=False, gate=exc.gate or None, url=url,
             error=exc.code, elapsed=elapsed_s)


# ──────────────────────────────────────────────────────────────
# Small helpers
# ──────────────────────────────────────────────────────────────

def _now_iso() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _normalize(s: Any) -> str:
    return " ".join(str(s or "").split())


def _short(value: Any, limit: int = 140) -> str:
    try:
        return json.dumps(value, ensure_ascii=False)[:limit]
    except (TypeError, ValueError):
        return str(value)[:limit]


# ──────────────────────────────────────────────────────────────
# Fallback evidence: sanitized snapshot summaries + runs.jsonl events (D3=B)
# ──────────────────────────────────────────────────────────────

_URL_QUERY_RE = re.compile(r"(https?://[^\s?#]+)\?[^\s]*")
# suspected secret/token: a long opaque run of token-ish chars carrying BOTH
# letters and digits (hex ids, api keys, jwt fragments, signed URLs)
_TOKEN_RE = re.compile(r"(?=[A-Za-z0-9_\-]*[A-Za-z])(?=[A-Za-z0-9_\-]*\d)[A-Za-z0-9_\-]{16,}")


def _sanitize_summary_text(text: Any) -> str:
    """Strip URL query strings and suspected tokens from evidence text."""
    s = " ".join(str(text or "").split())
    s = _URL_QUERY_RE.sub(lambda m: m.group(1), s)
    s = _TOKEN_RE.sub("[token]", s)
    return s


def _snapshot_summary(*, role: Any = "", label: Any = "", text: Any = "",
                      limit: int = 80) -> str:
    """`role/label/text-head` snapshot of a hit element, safe for logs.

    Sanitized BEFORE and AFTER slicing so neither a full token/URL query nor
    a slice artifact can survive into the ≤80-char summary.
    """
    head = _sanitize_summary_text(str(text or ""))[:80]
    raw = "/".join(p for p in (_sanitize_summary_text(role),
                              _sanitize_summary_text(label), head) if p)
    return _sanitize_summary_text(raw)[:limit].strip()


def _log_fallback(rung: str, *, status: str, summary: str = "",
                  detail: Optional[dict] = None) -> None:
    """D3=B: one runs.jsonl event per fallback trigger (rung/hit/verdict)."""
    try:
        path = console_home() / "runs.jsonl"
        path.parent.mkdir(parents=True, exist_ok=True)
        rec: dict = {"ts": _now_iso(), "op": "fallback", "rung": rung,
                     "ok": status == "ok", "status": status,
                     "summary": _sanitize_summary_text(summary)[:80]}
        if detail:
            rec["detail"] = detail
        with path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    except OSError:
        pass


def _fallback_history(limit: int = 5) -> dict:
    """Drift-report `fallbacks` section: cumulative triggers + recent hits."""
    events: list = []
    try:
        text = (console_home() / "runs.jsonl").read_text(encoding="utf-8")
    except (OSError, ValueError):
        text = ""
    for line in text.splitlines():
        try:
            rec = json.loads(line)
        except (ValueError, TypeError):
            continue
        if isinstance(rec, dict) and rec.get("op") == "fallback":
            events.append({k: rec.get(k) for k in ("ts", "rung", "ok", "status", "summary")})
    by_rung: dict = {}
    for ev in events:
        by_rung[ev.get("rung") or "?"] = int(by_rung.get(ev.get("rung") or "?", 0)) + 1
    return {"total": len(events), "by_rung": by_rung, "recent": events[-max(1, limit):]}


def _bubble_owns(bubble_text: str, query: str) -> bool:
    """True when a user bubble carries exactly this query (UI appends HH:MM).

    Equality or a query-prefix is required; a bubble that merely CONTAINS the
    query while carrying extra text is a polluted submission and must fail
    the gate (a merged draft + query once produced exactly that).
    """
    t = _normalize(bubble_text)
    t = re.sub(r"\s*\d{1,2}:\d{2}\s*$", "", t)
    q = _normalize(query)
    if not q:
        return False
    if t == q or t.startswith(q):
        return True
    # the bubble probe truncates at 300 chars: tolerate truncation for long queries
    return len(t) >= 280 and q[:120] in t


def _url_matches(current: str, target: str) -> bool:
    cur = (current or "").rstrip("/")
    tgt = (target or "").rstrip("/")
    if not tgt:
        return bool(cur)
    if tgt == BASE_URL.rstrip("/"):
        return cur == tgt  # home means no thread path
    return cur.startswith(tgt)


def _js(driver: Any, code: str, default: Any = None, *, mutating: bool = True) -> Any:
    """Run a JS snippet and normalize its result.

    String results are attempted as JSON; a plain non-JSON string (e.g.
    'clicked:button[...]') is a legitimate value and is returned as-is.
    Only empty/None results fall back to ``default``. (The old behavior
    silently replaced plain-string results with the default, which made a
    successful submit click look like 'no-button'.)

    ``mutating=False`` marks read-only probes (may be retried on timeout).
    ``mutating=True`` (default) — no retry; important for submit/file-inject calls
    where a retry would double-fire the action.
    """
    value = driver.evaluate(code, mutating=mutating)
    if isinstance(value, str):
        if value == "":
            return default
        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return value
    return default if value is None else value


def _info(driver: Any) -> dict:
    value = _js(driver, _probe("info"), {}, mutating=False)
    return value if isinstance(value, dict) else {}


def _tabs(driver: Any) -> list:
    """Session tabs via list_tabs, or ConsoleError on bridge failure."""
    resp = driver.list_tabs()
    if not isinstance(resp, dict):
        raise ConsoleError("attach", f"list_tabs returned {type(resp).__name__}",
                           code="attach.bad-response")
    blob = json.dumps(resp, ensure_ascii=False).lower()
    if "no extension connected" in blob:
        raise ConsoleError("attach", "WebBridge extension is not connected",
                           code="attach.disconnected")
    data = resp.get("data")
    if not isinstance(data, dict):
        data = {}
    if resp.get("ok") is False or data.get("success") is False or resp.get("error"):
        raise ConsoleError("attach", f"list_tabs failed: {resp.get('error') or resp}",
                           code="attach.bad-response")
    tabs = data.get("tabs")
    return tabs if isinstance(tabs, list) else []


def _evidence(driver: Any) -> Optional[str]:
    """Best-effort failure screenshot; returns the path (never raises)."""
    try:
        path = console_home() / "evidence" / (
            datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-console.png")
        path.parent.mkdir(parents=True, exist_ok=True)
        driver.screenshot(str(path))
        return str(path)
    except Exception as exc:  # noqa: BLE001 — evidence must never mask the gate
        logger.debug("evidence screenshot failed: %s", exc)
        return None


# ──────────────────────────────────────────────────────────────
# No-progress circuit breaker (repeated-action guard)
# ──────────────────────────────────────────────────────────────

# Pure geometry / scroll offsets. Sub-pixel layout jitter on a page that is
# otherwise frozen must never read as progress — that is exactly the failure
# this guard exists to catch (an agent re-firing the same action dozens of
# times because "something changed" when only a rect wiggled).
_NO_PROGRESS_NOISE_KEYS = frozenset({
    "x", "y", "cx", "cy", "sx", "sy", "left", "right", "width", "height",
    "rect", "bounding", "scrolltop", "scrollleft", "scrollheight",
    "clientheight", "clientwidth", "offsetwidth", "offsetheight",
})


def _strip_noise(value: Any) -> Any:
    """Recursively drop geometry keys so only substantive signals remain."""
    if isinstance(value, dict):
        return {k: _strip_noise(v) for k, v in value.items()
                if str(k).lower() not in _NO_PROGRESS_NOISE_KEYS}
    if isinstance(value, (list, tuple)):
        return [_strip_noise(v) for v in value]
    return value


def _progress_signature(sample: Any) -> str:
    """Digest of the substantive progress signals in one poll sample.

    Everything except the geometry noise keys survives, so URL, bubble count
    and text, prose length/hash, studied-pill count, attachment chips and the
    presence of busy/target controls all count as progress; rect/pixel jitter
    does not.
    """
    blob = json.dumps(_strip_noise(sample), sort_keys=True,
                      ensure_ascii=False, default=str)
    return hashlib.sha1(blob.encode("utf-8")).hexdigest()


class NoProgressGuard:
    """Circuit breaker for polling/wait loops.

    Feed every poll sample to :meth:`observe`. When ``limit`` consecutive
    samples carry an identical progress signature the guard raises
    ``ConsoleError(code="act.no-progress")`` so the loop fails fast instead
    of spinning to its timeout on a page that is not moving. Callers that
    have their own recovery rung (or their own terminal error code) catch
    that code and decide what to do next.
    """

    def __init__(self, *, gate: str, limit: int = NO_PROGRESS_LIMIT,
                 driver: Any = None, what: str = "poll",
                 min_elapsed: float = 0.0) -> None:
        self.gate = gate
        self.limit = max(int(limit), 1)
        self.driver = driver
        self.what = what
        # Slow-page grace: samples observed within `min_elapsed` seconds of
        # the guard's first sample never count towards the streak, so a wait
        # with a long budget tolerates slow renders without weakening
        # fail-fast on a page that is frozen from the start (which still
        # trips `limit` polls after the grace window).
        self.min_elapsed = max(float(min_elapsed), 0.0)
        self.samples = 0
        self.streak = 0
        self._last: Optional[str] = None
        self._started: Optional[float] = None

    def reset(self) -> None:
        self.samples = 0
        self.streak = 0
        self._last = None
        self._started = None

    def observe(self, sample: Any) -> None:
        """Record one sample; raise ``act.no-progress`` on a frozen run."""
        signature = _progress_signature(sample)
        self.samples += 1
        if self._started is None:
            self._started = time.monotonic()
        if self.min_elapsed and time.monotonic() - self._started < self.min_elapsed:
            # grace window: slow pages may legitimately show nothing yet
            self._last = signature
            self.streak = 0
            return
        if self._last is not None and signature == self._last:
            self.streak += 1
        else:
            self.streak = 1
        self._last = signature
        if self.streak < self.limit:
            return
        raise ConsoleError(
            self.gate,
            f"连续 {self.streak} 次{self.what}无实质进展（状态完全未变），提前熔断"
            f" / no substantive progress in {self.streak} consecutive {self.what}s"
            f" (signal {signature[:12]}); verify the tab before retrying",
            gates={self.gate: {"ok": False, "no_progress": {
                "streak": self.streak, "limit": self.limit,
                "samples": self.samples, "signature": signature[:12]}}},
            evidence=_evidence(self.driver) if self.driver is not None else None,
            code="act.no-progress")


def _cdp_click(driver: Any, x: int, y: int, *, sleep: Callable[[float], None]) -> None:
    """Trusted mouse click via CDP — required for Radix portal menus, where
    synthetic .click() does nothing (menu items are portals outside the
    composer subtree; plain button chips DO respond to synthetic clicks)."""
    driver.cdp("Input.dispatchMouseEvent", {"type": "mouseMoved", "x": x, "y": y})
    sleep(0.08)
    driver.cdp("Input.dispatchMouseEvent",
               {"type": "mousePressed", "x": x, "y": y, "button": "left", "clickCount": 1})
    sleep(0.12)
    driver.cdp("Input.dispatchMouseEvent",
               {"type": "mouseReleased", "x": x, "y": y, "button": "left", "clickCount": 1})


def _press_escape(driver: Any, *, sleep: Callable[[float], None]) -> None:
    for kind in ("keyDown", "keyUp"):
        driver.cdp("Input.dispatchKeyEvent",
                   {"type": kind, "key": "Escape", "code": "Escape",
                    "windowsVirtualKeyCode": 27, "nativeVirtualKeyCode": 27})
        sleep(0.12)


# ──────────────────────────────────────────────────────────────
# Pre-action geometry/occlusion gate (融合项 d, narrow)
# ──────────────────────────────────────────────────────────────

_SUBMIT_SELECTORS = ('button[aria-label="提交"]',
                     'button[aria-label="搜索"]',
                     'button[aria-label="Submit"]')


def _action_point_ok(driver: Any, *, selector: Optional[str] = None,
                     selectors: Optional[Sequence[str]] = None,
                     rect: Optional[dict] = None) -> Optional[dict]:
    """Pre-action geometry/occlusion re-check via the read-only hit-test probe.

    Returns ``None`` when the action point is usable (target visible, inside
    the viewport, and the centre hit lands in the target's own subtree) and a
    reason dict ``{"reason", "rel", "summary"}`` when it is NOT — the caller
    must then fail closed (``act.target-occluded``) instead of firing the
    action blind. ``summary`` is the occluder/target
    ``tag/role/aria-label/text-head`` snapshot, sanitized (URL query strings
    and suspected tokens stripped) and ≤80 chars.

    A probe that is not operational (bridge returned nothing parseable) or a
    target that simply is not there (``not-found``) yields ``None``: those
    cases carry no occlusion verdict and keep the historical failure
    semantics of the calling rung (the codebase's `unavailable` convention).
    """
    if selectors:
        spec: dict = {"selectors": [str(s) for s in selectors]}
    elif selector:
        spec = {"selector": str(selector)}
    elif rect is not None:
        spec = {"rect": {k: v for k, v in dict(rect).items()
                         if k in ("x", "y", "w", "h", "width", "height")}}
    else:
        return {"reason": "no-spec", "rel": "", "summary": ""}
    code = _JS_HITTEST.replace("__SPEC__", json.dumps(spec, ensure_ascii=True))
    payload = _js(driver, code, None, mutating=False)
    if not isinstance(payload, dict) or "ok" not in payload:
        return None                       # probe not operational: no verdict
    if payload.get("ok"):
        return None
    reason = str(payload.get("reason") or "unusable")
    if reason == "not-found":
        return None      # nothing to act on: the rung's own semantics decide
    raw_hit = payload.get("hit")
    raw_target = payload.get("target")
    hit = raw_hit if isinstance(raw_hit, dict) else {}
    target = raw_target if isinstance(raw_target, dict) else {}
    src = hit or target
    summary = _snapshot_summary(role=src.get("role") or src.get("tag") or "",
                                label=src.get("label") or "",
                                text=str(src.get("text") or ""))
    return {"reason": reason, "rel": str(payload.get("rel") or ""),
            "summary": summary}


def _target_occluded_error(gate: str, what: str, blocked: dict,
                           driver: Any = None) -> ConsoleError:
    """Fail-closed error for a blocked action point (never a blind click)."""
    summary = str(blocked.get("summary") or "")
    return ConsoleError(
        gate,
        f"{what} 未通过执行前几何/遮挡复检（{blocked.get('reason')}"
        f"{'，遮挡者: ' + summary if summary else ''}）—— 动作未发出"
        f" / pre-action hit-test blocked the {what} "
        f"({blocked.get('reason')}); the action was NOT fired (fail-closed)",
        gates={gate: {"ok": False, "target": dict(blocked)}},
        evidence=_evidence(driver) if driver is not None else None,
        code="act.target-occluded")


# ──────────────────────────────────────────────────────────────
# Fallback rungs (probe → element-table rung → probe.fallback-exhausted)
#
# Each rung follows D1=A: the deterministic heuristic below only proposes
# CANDIDATES; a candidate is adopted only after a semantic readback (and an
# effect check where the rung acts). A rung that cannot prove its claim
# returns {"status": "exhausted"} and the caller raises the unified
# `probe.fallback-exhausted` (D2=A) — never a half result. "unavailable"
# means the rung's own probes were dead (nothing to fall back onto); the
# caller then keeps its historical fail-closed error code.
# ──────────────────────────────────────────────────────────────

FALLBACK_PROSE = "prose-table"
FALLBACK_OWNERSHIP = "ownership-table"
FALLBACK_EXPAND = "expand-table"

_PROSE_MIN_CHARS = 200          # readback floor for an adopted answer block
_PROSE_SENTENCE_PUNCT = "。！？.!?"
# container semantic weight for the "largest visible content block" score
_PROSE_WEIGHTS = {"main": 1.4, "article": 1.3, "section": 1.1, "div": 1.0}
_PROSE_CHROME_HINTS = frozenset({"nav", "aside", "footer", "header", "chrome"})


def _table_items(driver: Any) -> Optional[list]:
    """Element table items, or None when the rung-2 probe is not operational."""
    payload = _js(driver, _JS_TABLE, None, mutating=False)
    if isinstance(payload, dict) and isinstance(payload.get("items"), list):
        return payload["items"]
    return None


def _blocks_payload(driver: Any) -> Optional[dict]:
    """Content-block candidates, or None when the rung-2 probe is dead."""
    payload = _js(driver, _JS_BLOCKS, None, mutating=False)
    if isinstance(payload, dict) and isinstance(payload.get("blocks"), list):
        return payload
    return None


def _bound_payload(driver: Any, query: str) -> Optional[dict]:
    """Identity-binding read (query text on page/thread), None when dead."""
    code = _JS_BOUND_TMPL.replace("__QUERY__",
                                  json.dumps(str(query or ""), ensure_ascii=False))
    payload = _js(driver, code, None, mutating=False)
    if isinstance(payload, dict) and "bound" in payload:
        return payload
    return None


def _block_excluded(block: Any) -> bool:
    """True for navigation/sidebar/footer chrome or degenerate geometry."""
    if not isinstance(block, dict):
        return True
    if str(block.get("hint") or "") in _PROSE_CHROME_HINTS:
        return True
    rect = block.get("rect") or {}
    return int(rect.get("w") or 0) < 80 or int(rect.get("h") or 0) < 20


def _blocks_max_len(payload: Any) -> int:
    """Length of the largest non-chrome content block (0 when unknown)."""
    if not isinstance(payload, dict):
        return 0
    best = 0
    for block in payload.get("blocks") or []:
        if not _block_excluded(block):
            best = max(best, int(block.get("len") or 0))
    return best


def _answer_block(payload: Any) -> Optional[dict]:
    """Largest non-chrome content block (the answer-body candidate)."""
    best = None
    for block in ((payload or {}).get("blocks") or []):
        if _block_excluded(block):
            continue
        if best is None or int(block.get("len") or 0) > int(best.get("len") or 0):
            best = block
    return best


def _blocks_fingerprint(text: Any) -> str:
    """Deterministic fingerprint of a block's normalized text (freshness)."""
    return hashlib.sha1(_normalize(text).encode("utf-8")).hexdigest()


def _blocks_baseline(driver: Any) -> Optional[dict]:
    """Pre-submit content-block baseline (RC2/RC6 freshness mechanism).

    Snapshot of the CURRENT largest content block (length + fingerprint +
    DOM index) taken BEFORE this turn is submitted. None when the element-
    table rung is not operational — callers then keep their historical
    staleness fallbacks and must flag ``stale_risk`` on adoption.
    """
    payload = _blocks_payload(driver)
    if payload is None:
        return None
    best = _answer_block(payload)
    if best is None:
        return {"max_len": 0, "fingerprint": "", "i": -1}
    return {"max_len": int(best.get("len") or 0),
            "fingerprint": _blocks_fingerprint(best.get("text") or ""),
            "i": int(best.get("i") or 0)}


def _block_is_new(block: Any, baseline: Any) -> bool:
    """RC2 freshness: a candidate must be NEWER than the pre-submit baseline.

    Newer ⟺ longer than the baseline's largest block (the common growing-
    answer case), or a different fingerprint positioned at/after the baseline
    block in the DOM (a later, shorter, different answer — never the previous
    turn's longer answer). Without a baseline freshness cannot be judged;
    the caller keeps the historical behavior and flags ``stale_risk``.
    """
    if not isinstance(baseline, dict):
        return True
    if int(block.get("len") or 0) > int(baseline.get("max_len") or 0):
        return True
    return (_blocks_fingerprint(block.get("text") or "")
            != (baseline.get("fingerprint") or "")
            and int(block.get("i") or 0) >= int(baseline.get("i") or -1))


def _fallback_prose_len(driver: Any) -> Optional[int]:
    """Count-path fallback (``div.prose`` gone): largest content-block length.

    None when the element-table rung is not operational — callers then keep
    their historical prose-count behavior.
    """
    payload = _blocks_payload(driver)
    return None if payload is None else _blocks_max_len(payload)


def _blocks_have_new(payload: Any, baseline: Any) -> bool:
    """RC6: some QUALIFIED content block is newer than the pre-submit baseline.

    The fresh block must be a real prose candidate (non-chrome, ≥ readback
    floor) so incidental UI text (e.g. a short submitted query bubble) never
    reads as "the new answer landed".
    """
    if not isinstance(baseline, dict):
        return False
    for block in ((payload or {}).get("blocks") or []):
        if (_prose_block_score(block) is not None
                and _block_is_new(block, baseline)):
            return True
    return False


def _answer_len_now(driver: Any, info: Optional[dict] = None) -> int:
    """Answer length: ``div.prose`` path first, content-block rung otherwise."""
    info = info if info is not None else _info(driver)
    n = int(info.get("lastProseLen") or 0)
    if n > 0 or int(info.get("proseCount") or 0):
        return n
    return _fallback_prose_len(driver) or 0


def _prose_block_score(block: Any) -> Optional[float]:
    """Deterministic prose candidate score (D1=A): length × container weight.

    None when the block is excluded — chrome (nav/sidebar/footer/header by
    role/aria/class/position), degenerate geometry, or below the readback
    floor (a candidate must be ≥200 chars anyway).
    """
    if _block_excluded(block):
        return None
    length = int(block.get("len") or 0)
    if length < _PROSE_MIN_CHARS:
        return None
    if length > len(str(block.get("text") or "")):
        # RC2: the probe truncates `text` at 4000 chars while `len` is the
        # full length — a `len > len(text)` block is a HALF candidate and is
        # never adoptable ("绝不半成品"), however big it is.
        return None
    tag = str(block.get("tag") or "")
    role = str(block.get("role") or "")
    weight = _PROSE_WEIGHTS.get(tag, 0.8)
    if role == "main":
        weight = max(weight, _PROSE_WEIGHTS["main"])
    return float(length) * weight


def _prose_candidates(blocks: Any) -> list:
    """Best-first candidate order; equal score → later block wins (recency)."""
    scored = []
    for block in blocks or []:
        score = _prose_block_score(block)
        if score is not None:
            scored.append((score, int(block.get("i") or 0), block))
    scored.sort(key=lambda t: (t[0], t[1]), reverse=True)
    return [b for _, _, b in scored]


def _prose_readback_ok(text: Any) -> bool:
    """Semantic readback for an adopted answer block."""
    t = _normalize(text)
    return (len(t) >= _PROSE_MIN_CHARS
            and any(c in t for c in _PROSE_SENTENCE_PUNCT))


def _prose_fallback_rung(driver: Any, *, gate: str = "extract",
                         baseline: Optional[dict] = None) -> dict:
    """Rung 2 for answer-text extraction when `div.prose` is missing/empty.

    RC2 freshness: with a pre-submit ``baseline`` (see
    :func:`_blocks_baseline`) only blocks NEWER than the baseline are
    adoptable — the previous turn's longer answer must never be adopted.
    Without a baseline the historical behavior stands but the result carries
    ``stale_risk: true`` (honest labeling, never silent).
    """
    stale_risk = not isinstance(baseline, dict)
    guard = NoProgressGuard(gate=gate, driver=driver, what="fallback 语义回读")
    payload = _blocks_payload(driver)
    if payload is None:
        _log_fallback(FALLBACK_PROSE, status="unavailable")
        return {"status": "unavailable", "fallback_used": FALLBACK_PROSE,
                "stale_risk": stale_risk}
    candidates = _prose_candidates(payload.get("blocks") or [])
    attempts: list = []
    for cand in candidates:
        summary = _snapshot_summary(
            role=cand.get("role") or cand.get("tag") or "",
            label=cand.get("label") or "",
            text=str(cand.get("text") or ""))
        if not _block_is_new(cand, baseline):
            # RC2 staleness: older-or-equal to the pre-submit baseline block
            attempts.append({"i": cand.get("i"), "summary": summary,
                             "readback_ok": False, "stale": True})
            continue
        guard.observe({"len": cand.get("len"),
                       "text": str(cand.get("text") or "")[:200],
                       "cand": str(cand.get("i") or "")})
        # semantic readback: an INDEPENDENT second read of the live DOM
        again = _blocks_payload(driver)
        rb_text = ""
        for block in ((again or {}).get("blocks") or []):
            if block.get("i") == cand.get("i"):
                rb_text = str(block.get("text") or "")
                break
        ok = _prose_readback_ok(rb_text)
        attempts.append({"i": cand.get("i"), "summary": summary,
                         "readback_ok": ok, "stale": False})
        if ok:
            _log_fallback(FALLBACK_PROSE, status="ok", summary=summary,
                          detail={"attempts": len(attempts),
                                  "stale_risk": stale_risk})
            return {"status": "ok", "fallback_used": FALLBACK_PROSE,
                    "text": rb_text, "summary": summary, "attempts": attempts,
                    "stale_risk": stale_risk}
    summary = attempts[-1]["summary"] if attempts else ""
    _log_fallback(FALLBACK_PROSE, status="failed", summary=summary,
                  detail={"candidates": len(candidates),
                          "attempts": len(attempts),
                          "stale_risk": stale_risk})
    return {"status": "exhausted", "fallback_used": FALLBACK_PROSE,
            "summary": summary, "candidates": len(candidates),
            "attempts": attempts, "stale_risk": stale_risk}


# expand-button labels the fallback rung accepts as near-matches
_EXPAND_FAMILY = ("展开", "查看更多", "展开更多", "更多", "expand", "show more")
# RC3(c): the loose contains-arm is narrowed — the label must START the
# button text (展开…/查看更多…/show more…/expand…) or BE the whole text.
_EXPAND_STARTS = ("展开", "查看更多", "show more", "expand")
# …and anything settings/options/load-more shaped is NEVER an expand control
_EXPAND_REJECT = ("设置", "选项", "加载", "更多设置")


def _edit_distance(a: str, b: str, *, cap: int = 3) -> int:
    """Bounded Levenshtein distance (pure, deterministic)."""
    if abs(len(a) - len(b)) > cap:
        return cap + 1
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[-1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
        if min(prev) > cap:
            return cap + 1
    return prev[-1]


def _expand_candidate_score(item: Any) -> Optional[float]:
    """Deterministic expand-button candidate filter; lower score = better.

    None = NEVER click: non-button role (follow-up question rows live there),
    disabled, anything carrying ？/? (the previous review's misfire lesson),
    settings/options/load-more labels (RC3: 「更多设置」 is not an expand
    control), or text with no nearness to the expand family at all.
    """
    if not isinstance(item, dict):
        return None
    tag = str(item.get("tag") or "").lower()
    role = str(item.get("role") or "").lower()
    if role and role != "button":
        return None                      # 非 button role 一律排除
    if tag != "button" and role != "button":
        return None
    if item.get("disabled"):
        return None
    text = _normalize(item.get("text") or item.get("label") or "")
    label = _normalize(item.get("label") or "")
    joined = (text + " " + label).strip()
    if not joined or re.search(r"[？?]", joined):
        return None                      # 含 ？/? = 追问问题按钮，绝不点击
    low = joined.lower()
    if any(w in low for w in _EXPAND_REJECT):
        return None                      # 设置/选项/加载 类按钮绝不点击
    family = [f.lower() for f in _EXPAND_FAMILY]
    near = min(_edit_distance(low, f, cap=3) for f in family)
    loose = (any(low.startswith(p) for p in _EXPAND_STARTS)
             or low in family)
    if not loose and near > 2:
        return None
    # attempt order: strict text-nearness first (distance ≤2), then the
    # looser starts-with/equal arm; shorter labels before longer ones
    arm = float(near) if near <= 2 else 10.0
    return arm + min(len(joined), 30) / 100.0


# A finished answer ends on sentence punctuation; 「…」 or a mid-sentence
# tail is the deterministic truncation signal (RC3: hunt expand candidates
# ONLY when an expand control is expected). The scroll probe is deliberately
# NOT used as a trigger: it mutates (scrollTop/window.scrollTo — drift
# classifies it "action") and would move the page before the trusted click
# at cached coordinates.
_EXPANSION_TAIL_DONE = "。！？.!?"


def _expand_truncation_signal(block: Any) -> dict:
    """Whether the answer looks truncated (an expand control is expected)."""
    why: list = []
    if isinstance(block, dict):
        tail = str(block.get("text") or "").rstrip()
        if tail.endswith("…") or tail.endswith("..."):
            why.append("ellipsis-tail")
        elif tail and tail[-1] not in _EXPANSION_TAIL_DONE:
            why.append("unterminated-tail")
    return {"risk": bool(why), "why": why}


def _rect_adjacent(a: Any, b: Any, margin: int = 48) -> bool:
    """True when two rects intersect or sit within ``margin`` px of each other."""
    try:
        ax, ay = int(a.get("x") or 0), int(a.get("y") or 0)
        aw, ah = int(a.get("w") or 0), int(a.get("h") or 0)
        bx, by = int(b.get("x") or 0), int(b.get("y") or 0)
        bw, bh = int(b.get("w") or 0), int(b.get("h") or 0)
    except AttributeError:
        return False
    gap_x = max(0, max(bx - (ax + aw), ax - (bx + bw)))
    gap_y = max(0, max(by - (ay + ah), ay - (by + bh)))
    return gap_x <= margin and gap_y <= margin


def _expand_fallback_rung(driver: Any, *,
                          sleep: Callable[[float], None],
                          gate: str = "extract") -> dict:
    """Rung 2 for the expand control when the exact-label probe fully missed.

    RC3 trigger discipline: candidates are hunted ONLY when the answer looks
    truncated (ellipsis / mid-sentence tail) — on a healthy page with no
    expand control this rung must return ``none`` without clicking anything.
    Candidate clicks are further limited to the answer area (rect adjacent
    to the largest content block) and verified by effect (the content block
    must GROW) via trusted CDP mouse events; a click that grows nothing is
    not success.
    """
    items = _table_items(driver)
    if items is None:
        # RC5: every fallback trigger leaves a runs.jsonl event (D3=B)
        _log_fallback(FALLBACK_EXPAND, status="unavailable")
        return {"status": "unavailable", "fallback_used": FALLBACK_EXPAND}
    payload = _blocks_payload(driver)
    block = _answer_block(payload)
    trigger = _expand_truncation_signal(block)
    if not trigger["risk"]:
        _log_fallback(FALLBACK_EXPAND, status="none",
                      detail={"trigger": "no-truncation-signal"})
        return {"status": "none", "fallback_used": FALLBACK_EXPAND}
    scored = []
    for item in items:
        score = _expand_candidate_score(item)
        if score is None:
            continue
        rect = item.get("rect") if isinstance(item.get("rect"), dict) else {}
        if block is not None and not _rect_adjacent(rect, block.get("rect") or {}):
            continue        # RC3(b): answer-area candidates only
        scored.append((score, -int(item.get("i") or 0), item))
    if not scored:
        # nothing expand-like near the answer: nothing to expand — not a failure
        _log_fallback(FALLBACK_EXPAND, status="none",
                      detail={"trigger": ",".join(trigger["why"]),
                              "candidates": 0})
        return {"status": "none", "fallback_used": FALLBACK_EXPAND}
    scored.sort(key=lambda t: (t[0], t[1]))
    guard = NoProgressGuard(gate=gate, driver=driver, what="fallback 效果验证")
    attempts: list = []
    for _, _, cand in scored:
        summary = _snapshot_summary(
            role=cand.get("role") or cand.get("tag") or "",
            label=cand.get("label") or "",
            text=str(cand.get("text") or ""))
        # readback: the candidate must still be the same live button
        again = _table_items(driver)
        rb = next((b for b in (again or [])
                   if b.get("i") == cand.get("i")), None)
        rb_ok = (rb is not None and not rb.get("disabled")
                 and _normalize(rb.get("text") or "")
                 == _normalize(cand.get("text") or ""))
        if not rb_ok:
            attempts.append({"i": cand.get("i"), "summary": summary,
                             "readback_ok": False})
            continue
        before = _blocks_max_len(_blocks_payload(driver))
        rect = cand.get("rect") or {}
        cx = int(rect.get("x") or 0) + int(rect.get("w") or 0) // 2
        cy = int(rect.get("y") or 0) + int(rect.get("h") or 0) // 2
        # 融合项 d: a cached-coordinate click re-verifies its point first —
        # when the point no longer lands inside the candidate's subtree
        # (浮层覆盖 / layout drift) the click is NOT fired; the candidate
        # counts as a failed attempt and the rung moves to the next one.
        blocked = _action_point_ok(driver, rect=rect)
        if blocked is not None:
            attempts.append({"i": cand.get("i"), "summary": summary,
                             "readback_ok": True, "hit_ok": False,
                             "why": blocked.get("reason"),
                             "occluder": blocked.get("summary", "")})
            continue
        # RC4: the sample carries the candidate identity (index + click
        # coords, in a key geometry-stripping keeps) so N sibling buttons
        # with the same text are N different actions — only a REPEATED
        # same-index candidate with zero progress reads as frozen.
        guard.observe({"before": before,
                       "text": _normalize(cand.get("text") or "")[:60],
                       "cand": f"{cand.get('i')}:{cx},{cy}"})
        _cdp_click(driver, cx, cy, sleep=sleep)
        sleep(1.0)
        after = _blocks_max_len(_blocks_payload(driver))
        grew = after > before
        attempts.append({"i": cand.get("i"), "summary": summary,
                         "readback_ok": True, "grew": grew,
                         "before": before, "after": after})
        if grew:
            _log_fallback(FALLBACK_EXPAND, status="ok", summary=summary,
                          detail={"attempts": len(attempts)})
            return {"status": "ok", "fallback_used": FALLBACK_EXPAND,
                    "summary": summary, "attempts": attempts}
    summary = attempts[-1]["summary"] if attempts else ""
    _log_fallback(FALLBACK_EXPAND, status="failed", summary=summary,
                  detail={"candidates": len(scored), "attempts": len(attempts)})
    return {"status": "exhausted", "fallback_used": FALLBACK_EXPAND,
            "summary": summary, "candidates": len(scored), "attempts": attempts}


def _ownership_fallback_rung(driver: Any, query: str, *,
                             base_studied: Optional[int] = None,
                             timeout: float, poll: float,
                             sleep: Callable[[float], None]) -> dict:
    """Rung 2 for submit ownership when the user-bubble anchor is dead.

    WARN red line (highest constraint): composer state, URL changes and
    count changes alone can NEVER prove ownership. Ownership is claimed only
    with BOTH — (1) an independent identity binding: this turn's query text
    (the exact fill string, normalized-whitespace containment) present in
    the thread/page, never in the composer; AND (2) an effect signal: the
    answer area starts growing or the completion-marker count increases.
    Anything less → ``probe.fallback-exhausted`` (fail-closed).
    """
    guard = NoProgressGuard(gate="submit", driver=driver, what="fallback 归属轮询")
    first = _bound_payload(driver, query)
    if first is None:
        _log_fallback(FALLBACK_OWNERSHIP, status="unavailable")
        return {"status": "unavailable", "fallback_used": FALLBACK_OWNERSHIP}
    info0 = _info(driver)
    len0 = _answer_len_now(driver, info0)
    studied0 = (int(base_studied) if base_studied is not None
                else int(info0.get("studied") or 0))
    deadline = time.monotonic() + max(float(timeout), 0.0)
    bound: dict = first
    while True:
        info = _info(driver)
        cur = _bound_payload(driver, query)
        if cur is not None:
            bound = cur
        # RC1 (WARN): `bound:true` alone is not evidence — the text must have
        # landed on a concrete non-composer element (the probe's `text`).
        bound_ok = bool(bound.get("bound")) and bool(bound.get("text"))
        ans_len = _answer_len_now(driver, info)
        effect = (int(info.get("studied") or 0) > studied0) or (ans_len > len0)
        summary = _snapshot_summary(role=bound.get("role") or bound.get("tag") or "",
                                    label=bound.get("label") or "",
                                    text=bound.get("text") or "")
        # RC4: the ok-check runs BEFORE guard.observe (same order as the main
        # path's _wait_ownership) — a landing ownership win always beats the
        # breaker.
        if bound_ok and effect:
            _log_fallback(FALLBACK_OWNERSHIP, status="ok", summary=summary,
                          detail={"where": bound.get("where"),
                                  "bound": True, "effect": True})
            return {"status": "ok", "fallback_used": FALLBACK_OWNERSHIP,
                    "summary": summary, "bound_where": bound.get("where"),
                    "bound": True, "effect": True}
        guard.observe({**info, "bound": bound_ok, "ans_len": ans_len})
        if time.monotonic() >= deadline:
            _log_fallback(FALLBACK_OWNERSHIP, status="failed", summary=summary,
                          detail={"bound": bound_ok, "effect": effect})
            return {"status": "exhausted", "fallback_used": FALLBACK_OWNERSHIP,
                    "summary": summary, "bound": bound_ok, "effect": effect}
        sleep(max(poll, 0.05))


def _make_driver(cfg: Config, state: dict) -> Any:
    from .drivers.webbridge import WebBridgeDriver
    return WebBridgeDriver(cfg.webbridge_url, session=state.get("session") or DEFAULT_SESSION)


# ──────────────────────────────────────────────────────────────
# Attach-or-recreate
# ──────────────────────────────────────────────────────────────

def attach(driver: Any, state: dict, target_url: str, *,
           cfg: Optional[Config] = None,
           sleep: Callable[[float], None] = time.sleep) -> dict:
    """Ensure the console session has one tab, sitting on ``target_url``.

    Reuses the live tab when the session still has one; otherwise opens a
    fresh tab for ``target_url`` (a saved thread URL or the home page) in the
    same session with the console group title.
    """
    cfg = cfg or get_config()
    tabs = _tabs(driver)
    created = False

    if not tabs:
        driver.navigate(target_url, new_tab=True, group_title=state["group_title"])
        sleep(cfg.page_load_wait)
        created = True
        if not _tabs(driver):
            raise ConsoleError("attach", "navigate did not create a session tab",
                               code="attach.no-tab")
        return {"created": created, "tab_count": 1, "url": target_url}

    current = (_info(driver).get("url") or "")
    if not _url_matches(current, target_url):
        driver.navigate(target_url, new_tab=False)
        sleep(cfg.page_load_wait)
        current = (_info(driver).get("url") or "")
        if not _url_matches(current, target_url):
            raise ConsoleError(
                "attach", f"tab did not reach {target_url!r} (at {current!r})",
                code="attach.navigate")
    return {"created": created, "tab_count": len(_tabs(driver)), "url": current}


# ──────────────────────────────────────────────────────────────
# Gate helpers
# ──────────────────────────────────────────────────────────────

def _gate_fill(driver: Any, query: str, *, sleep: Callable[[float], None],
               attempts: int = 3) -> dict:
    """Gate 1: the composer must EQUAL the query AND the editor state must
    have committed — proven by the submit button being enabled.

    ``fill`` is the editor's only reliable mutation path and is
    clear-and-insert (replace), so a polluted composer is repaired by
    re-filling, not by keyboard/DOM clearing (those get reverted by the
    editor's controlled re-render; empty fill values are silent no-ops).
    The DOM text and the editor's internal React state can diverge; the
    submit button's disabled flag exposes the internal state (disabled =
    state empty even if the DOM shows text), so both must agree.
    """
    qn = _normalize(query)
    # 融合项 d (fill 路径): the composer click+fill is a gated action — the
    # target must be visible and un-occluded before either call fires
    # (fail-closed: act.target-occluded, never type blind under a 浮层).
    blocked = _action_point_ok(driver, selector="[contenteditable]")
    if blocked is not None:
        raise _target_occluded_error("fill", "composer click+fill", blocked, driver)
    detail: dict = {"composer_before": _composer(driver), "tries": []}
    for attempt in range(1, attempts + 1):
        driver.click("[contenteditable]")
        sleep(0.4)
        resp = driver.fill("[contenteditable]", query)
        sleep(FILL_SETTLE)
        info = _info(driver)
        after = _normalize(info.get("composer"))
        btn = info.get("submit_button")
        if after == qn and btn == "enabled":
            detail["tries"].append({"n": attempt, "resp": _short(resp), "btn": btn})
            return {"ok": True, "attempts": attempt, "method": "fill", **detail}
        if after == qn and btn in ("disabled", "missing"):
            # slow React commit? re-read once after a longer settle
            sleep(1.2)
            info = _info(driver)
            after2 = _normalize(info.get("composer"))
            btn2 = info.get("submit_button")
            if after2 == qn and btn2 == "enabled":
                detail["tries"].append({"n": attempt, "resp": _short(resp), "btn": btn2,
                                        "via": "delayed-commit"})
                return {"ok": True, "attempts": attempt, "method": "fill", **detail}
            after, btn = after2, btn2
        if after == "" and btn in ("disabled", "missing"):
            # fill was a silent no-op on an empty editor: trusted insertText
            driver.cdp("Input.insertText", {"text": query})
            sleep(FILL_SETTLE)
            info = _info(driver)
            after = _normalize(info.get("composer"))
            btn = info.get("submit_button")
            if after == qn and btn == "enabled":
                detail["tries"].append({"n": attempt, "resp": _short(resp), "btn": btn,
                                        "via": "cdp-insertText"})
                return {"ok": True, "attempts": attempt, "method": "cdp-insertText", **detail}
        detail["tries"].append({"n": attempt, "resp": _short(resp),
                                "after": after[:60], "btn": btn})
        detail["last_after"] = after[:100]
    raise ConsoleError(
        "fill",
        f"composer/editor state never committed (left={detail.get('last_after', '')!r}, "
        f"btn={detail['tries'][-1].get('btn')!r})",
        evidence=_evidence(driver), code="fill.not-committed")


def _composer(driver: Any) -> str:
    return _normalize(_info(driver).get("composer"))


def _wait_ownership(driver: Any, query: str, base_bubbles: int, *,
                    timeout: float, poll: float,
                    sleep: Callable[[float], None]) -> bool:
    """Gate 2 core: a new user turn OWNING this query must appear.

    Carries the no-progress circuit breaker: when ``NO_PROGRESS_LIMIT``
    consecutive polls show a byte-identical substantive signal (URL, bubble
    count/text, composer, studied pills, prose, busy controls — geometry
    noise stripped) the wait raises ``act.no-progress`` instead of burning
    the whole timeout on a frozen page. Ownership is checked BEFORE the
    guard observes, so a landing turn always wins over the breaker.
    """
    guard = NoProgressGuard(gate="submit", driver=driver, what="poll")
    deadline = time.monotonic() + timeout
    while True:
        info = _info(driver)
        if (int(info.get("bubbles") or 0) > base_bubbles
                and _bubble_owns(info.get("lastBubble") or "", query)):
            return True
        guard.observe(info)
        if time.monotonic() >= deadline:
            return False
        sleep(max(poll, 0.05))


def _ownership_or_exhausted(driver: Any, query: str, base_bubbles: int, *, timeout: float,
                            poll: float, sleep: Callable[[float], None]) -> tuple:
    """``_wait_ownership`` with the breaker translated to a plain verdict.

    Returns ``(owned, tripped, no_progress)``: ``tripped=True`` means the wait
    ended on ``act.no-progress`` (nothing moved at all), which is "not owned
    yet" for callers that still have a recovery rung to try; ``no_progress``
    is the breaker's detail dict (streak/limit/samples/signature) for that
    trip, or ``None`` when the wait ended without tripping. Exceptions other
    than the breaker propagate untouched.
    """
    try:
        return _wait_ownership(driver, query, base_bubbles, timeout=timeout,
                               poll=poll, sleep=sleep), False, None
    except ConsoleError as exc:
        if exc.code != "act.no-progress":
            raise
        detail = ((exc.gates or {}).get(exc.gate) or {}).get("no_progress")
        return False, True, detail


def _gate_submit(driver: Any, query: str, base_bubbles: int, *,
                 timeout: float, poll: float,
                 sleep: Callable[[float], None],
                 base_studied: Optional[int] = None) -> dict:
    """Gate 2: verify the composer once more, then submit.

    A late async draft-restore can merge extra text into the composer AFTER
    gate 1 passed, so equality is re-checked here and repaired by re-filling
    before any submit action runs. Submission itself goes through the submit
    button (multi-selector), falling back to the Enter combo.
    """
    actions = []
    qn = _normalize(query)
    sync = _info(driver)
    if (_normalize(sync.get("composer")) != qn
            or sync.get("submit_button") != "enabled"):
        refill = _gate_fill(driver, query, sleep=sleep)
        actions.append({"action": "refill-before-submit", "result": refill["method"],
                        "composer_before": refill.get("composer_before", "")[:80]})
    else:
        actions.append({"action": "composer-verified", "result": "equal"})

    # Freshness pass: one final replace right before sending so the editor
    # state is committed at submit time. An attachment can keep the submit
    # button enabled while the text state lags, which once produced a
    # file-only submission (observed live 2026-09-21).
    driver.fill("[contenteditable]", query)
    sleep(FILL_SETTLE)
    fresh = _info(driver)
    if (_normalize(fresh.get("composer")) != qn
            or fresh.get("submit_button") != "enabled"):
        refill = _gate_fill(driver, query, sleep=sleep)
        actions.append({"action": "refill-after-refresh", "result": refill["method"]})
    else:
        actions.append({"action": "composer-refresh", "result": "ok"})

    # 融合项 d (submit 路径): the submit-button click is gated the same way —
    # covered/off-viewport target ⇒ act.target-occluded, fail-closed, never a
    # blind click (the selector list mirrors `_JS_CLICK_SUBMIT`'s own order).
    blocked = _action_point_ok(driver, selectors=_SUBMIT_SELECTORS)
    if blocked is not None:
        raise _target_occluded_error("submit", "submit-button click", blocked, driver)
    clicked = _js(driver, _JS_CLICK_SUBMIT, "no-button")
    actions.append({"action": "click-submit-button", "result": clicked})
    if "clicked" not in str(clicked):
        # UI transition gaps can transiently unmount the button: retry once
        sleep(0.8)
        blocked = _action_point_ok(driver, selectors=_SUBMIT_SELECTORS)
        if blocked is not None:
            raise _target_occluded_error("submit", "submit-button click (retry)",
                                         blocked, driver)
        retry = _js(driver, _JS_CLICK_SUBMIT, "no-button")
        actions.append({"action": "click-submit-button-retry", "result": retry})
        clicked = retry
    # Both ownership waits run under the no-progress circuit breaker: a frozen
    # page ends them early (act.no-progress) instead of idling out the timeout.
    # The breaker means "nothing moved at all", so the Enter-combo rung still
    # gets its turn; only when every rung has been tried does the gate fail.
    # Trips are recorded PER RUNG: the terminal error must say which waits
    # actually tripped instead of blaming "every wait" when only one did.
    trips: list = []  # [(rung, breaker detail | None), ...]
    owned, tripped, np_detail = _ownership_or_exhausted(
        driver, query, base_bubbles, timeout=timeout, poll=poll, sleep=sleep)
    trips.append(("button", np_detail if tripped else None))
    if owned:
        mechanism = "button" if "clicked" in str(clicked) else "unexpected-none"
        return {"ok": True, "mechanism": mechanism, "actions": actions}

    combo = _js(driver, _JS_ENTER_COMBO, "no input")
    actions.append({"action": "enter-combo", "result": combo})
    owned, tripped, np_detail = _ownership_or_exhausted(
        driver, query, base_bubbles, timeout=timeout, poll=poll, sleep=sleep)
    trips.append(("combo", np_detail if tripped else None))
    if owned:
        return {"ok": True, "mechanism": "combo", "actions": actions}

    # Rung 3: element-table ownership fallback — only when the user-bubble
    # anchor is DEAD (no new turn marker at all). A bubble that appeared but
    # does not own the query is a failed gate, not a missing anchor, and
    # keeps the historical error codes below. WARN: this rung claims
    # ownership ONLY with an independent query-text binding plus an effect
    # signal — never on composer/URL/count changes alone.
    info_now = _info(driver)
    if int(info_now.get("bubbles") or 0) <= base_bubbles:
        fb = _ownership_fallback_rung(
            driver, query, base_studied=base_studied,
            timeout=timeout, poll=poll, sleep=sleep)
        if fb.get("status") == "ok":
            actions.append({"action": "ownership-fallback", "result": "ok",
                            "bound_where": fb.get("bound_where")})
            return {"ok": True, "mechanism": "ownership-fallback",
                    "actions": actions,
                    "fallback_used": fb.get("fallback_used"),
                    "fallback_summary": fb.get("summary", "")}
        if fb.get("status") == "exhausted":
            # D2=A: the fallback also failed → unified fail-closed code.
            raise ConsoleError(
                "submit",
                f"no user-bubble anchor AND the element-table ownership rung "
                f"could not prove ownership (query-text binding="
                f"{bool(fb.get('bound'))}, effect-signal={bool(fb.get('effect'))})"
                f" — fail-closed: BOTH an independent identity binding and an "
                f"effect signal are required (composer/URL/count alone never "
                f"prove ownership)",
                gates={"submit": {
                    "ok": False,
                    "fallback": {k: v for k, v in fb.items() if k != "text"},
                    "no_progress": {
                        "limit": NO_PROGRESS_LIMIT,
                        "rungs": {**{rung: ("tripped" if np is not None else "timeout")
                                     for rung, np in trips},
                                  "fallback": "exhausted"},
                        "tripped": [r for r, np in trips if np is not None],
                        "detail": {rung: np for rung, np in trips if np is not None},
                    }}},
                evidence=_evidence(driver), code="probe.fallback-exhausted")

    last = _info(driver).get("lastBubble") or ""
    detail = f"no new user turn observed after submit attempts (last bubble: {str(last)[:80]!r})"
    tripped_rungs = [rung for rung, np in trips if np is not None]
    no_progress = {
        "limit": NO_PROGRESS_LIMIT,
        "rungs": {rung: ("tripped" if np is not None else "timeout")
                  for rung, np in trips},
        "tripped": tripped_rungs,
        "detail": {rung: np for rung, np in trips if np is not None},
    }
    gates = {"submit": {"ok": False, "no_progress": no_progress}}
    if len(tripped_rungs) == len(trips):
        raise ConsoleError(
            "submit",
            f"{detail} — and every wait tripped the no-progress breaker "
            f"(zero substantive change across {NO_PROGRESS_LIMIT} polls)",
            gates=gates, evidence=_evidence(driver), code="act.no-progress")
    if tripped_rungs:
        waited = " and ".join(r for r, _ in trips if r not in tripped_rungs)
        raise ConsoleError(
            "submit",
            f"{detail} — the {' and '.join(tripped_rungs)} wait(s) tripped the "
            f"no-progress breaker (zero substantive change across "
            f"{NO_PROGRESS_LIMIT} polls) while the {waited} wait timed out with "
            f"the page still moving",
            gates=gates, evidence=_evidence(driver), code="submit.no-turn")
    raise ConsoleError(
        "submit", f"{detail} — both waits timed out without tripping the "
        f"no-progress breaker (the page kept moving but the turn never landed)",
        gates=gates, evidence=_evidence(driver), code="submit.no-turn")


def _gate_complete(driver: Any, base_studied: int, *,
                   base_prose_count: int = 0,
                   base_len: Optional[int] = None,
                   base_blocks: Optional[dict] = None,
                   wait_budget: float, poll: float,
                   sleep: Callable[[float], None],
                   monotonic: Callable[[], float] = time.monotonic,
                   hard_cap_factor: float = 6.0,
                   min_hard_cap: float = 900.0) -> dict:
    """Gate 3: the NEW turn's answer must appear, then settle (v2, T4).

    A stale answer from the previous turn must never satisfy this gate: a new
    answer has to be observed (``proseCount > base_prose_count`` or, when a
    ``base_len`` baseline is supplied, ``lastProseLen > base_len``) before
    stability counts (observed live 2026-09-21: a slow file-bearing answer let
    a naive stability check extract the previous turn's answer).

    Count-path (``div.prose`` gone): new-answer detection runs on the
    element-table rung's content blocks against the pre-submit ``base_blocks``
    baseline (same freshness mechanism as the prose fallback rung, RC6) — a
    fast answer that renders COMPLETELY before the first poll is new on that
    first poll, and a stale previous block never is. Without ``base_blocks``
    the historical first-sample baseline stands (staleness-safe, but a fast
    full render can then not prove novelty).

    v2 (live-verified 2026-09-23) adds three fail-safe layers on top of the
    deterministic ``_answer_settled`` v2.2 predicate:

    - **adaptive deadline** — a deadline reached while the answer is still
      growing (or the action signal says busy) extends by ``extension_step``,
      bounded by a hard cap (``wait_budget * hard_cap_factor`` / ``min_hard_cap``);
      otherwise the gate fails closed with ``complete.timeout`` + human-review
      escalation instead of returning a half-answer;
    - **contradiction flag** — a busy signal with frozen content for ~20 polls
      marks ``contradiction=True`` in the result (evidence conflict, reported
      but not fatal on its own);
    - **empty-probe fail-fast** — five consecutive empty WebBridge probes raise
      ``bridge.probe-failed`` immediately rather than spinning to the deadline.

    ``base_len=None`` (the call sites today) means no length baseline is
    known: new-answer detection then relies on ``proseCount`` alone, exactly
    as in v1.
    """
    poll_eff = max(poll, 0.01)
    start = monotonic()
    deadline = start + max(wait_budget, 0.0)
    hard_cap = max(wait_budget * hard_cap_factor, min_hard_cap)
    extension_step = max(wait_budget / 2, 60.0)
    # busy while frozen for ~20 polls (≈60s at the default poll=3.0)
    stall_seconds = 20 * poll_eff
    extensions = 0
    prev_len = base_len if base_len is not None else -1
    base_fb_len: Optional[int] = None   # staleness baseline for the count-path rung
    stable = 0
    empty_run = 0
    done_seen = False
    new_seen = False
    last_change_at = start
    info: dict = {}
    signal = ""
    contradiction = False
    while True:
        info = _info(driver) or {}
        if not info:
            empty_run += 1
            if empty_run >= 5:
                raise ConsoleError(
                    "complete",
                    "WebBridge 探针连续返回空 — 桥不可达或页面未加载。"
                    " / probe returned empty 5x",
                    gates={"complete": {
                        "ok": False, "probe_empty_runs": empty_run,
                        "elapsed_s": round(monotonic() - start, 1),
                        "escalation": "human-review"}},
                    evidence=_evidence(driver),
                    code="bridge.probe-failed")
        else:
            empty_run = 0
        if int(info.get("studied") or 0) > base_studied:
            done_seen = True
        now = monotonic()
        length = int(info.get("lastProseLen") or 0)
        fb_payload = None
        fb_len = None
        if length <= 0 and not int(info.get("proseCount") or 0):
            # `div.prose` is gone: count-path fallback (element-table rung).
            # RC6: novelty is judged against the PRE-SUBMIT blocks baseline
            # (a fully rendered fast answer is new on its first sample and a
            # stale previous block never is); without one the first prose-dead
            # sample keeps serving as the staleness baseline — a stale block
            # can still never settle.
            fb_payload = _blocks_payload(driver)
            fb_block = _answer_block(fb_payload)
            if fb_block is not None:
                fb_len = int(fb_block.get("len") or 0)
                if base_fb_len is None:
                    base_fb_len = fb_len
                length = fb_len
        if length != prev_len:
            if length > prev_len:
                last_change_at = now
            prev_len, stable = length, 0
        else:
            stable += 1
        busy = bool(info.get("stop_button")) or (
            (info.get("action_icon") or "") not in ("", SUBMIT_ICON_IDLE))
        if busy and stable * poll_eff >= stall_seconds:
            contradiction = True   # busy signal present but content frozen
        new_seen = ((base_len is not None and length > base_len)
                    or int(info.get("proseCount") or 0) > base_prose_count
                    or (fb_len is not None and base_fb_len is not None
                        and fb_len > base_fb_len)
                    or (fb_payload is not None and base_blocks is not None
                        and _blocks_have_new(fb_payload, base_blocks)))
        info_eff = info
        if fb_len:
            # feed the deterministic settle predicate the count-path values
            info_eff = {**info, "lastProseLen": length,
                        "proseCount": max(int(info.get("proseCount") or 0), 1)}
        settled, signal = _answer_settled(info_eff, prev_len, stable,
                                          new_seen=new_seen)
        if settled:
            break
        now = monotonic()
        if now >= deadline:
            growing_recently = (now - last_change_at) < extension_step
            if (growing_recently or busy) and now < hard_cap:
                deadline = now + extension_step
                extensions += 1
                continue
            raise ConsoleError(
                "complete",
                f"等待答案完成超时（fail-closed）；可用 extract --peek 复核现场。"
                f" / completion timeout after {now - start:.0f}s",
                gates={"complete": {
                    "ok": False, "new_seen": new_seen, "done_seen": done_seen,
                    "stable": stable, "chars": length,
                    "method": signal or "none",
                    "evidence": _evidence(driver), "info": info,
                    "elapsed_s": round(now - start, 1),
                    "contradiction": contradiction,
                    "escalation": "human-review"}},
                code="complete.timeout")
        sleep(poll_eff)
    elapsed = monotonic() - start
    return {"ok": True, "new_seen": new_seen, "done_seen": done_seen,
            "method": signal or "length-only", "signal": signal or "length-only",
            "stable": stable, "chars": length,
            "studied": int(info.get("studied") or 0),
            "generating": bool(info.get("generating")),
            "contradiction": contradiction,
            "deadline_extensions": extensions, "elapsed_s": round(elapsed, 1),
            "started": start, "completed": monotonic()}


# ──────────────────────────────────────────────────────────────
# Main entry points
# ──────────────────────────────────────────────────────────────

# ──────────────────────────────────────────────────────────────
# Model selector + file attachments
# ──────────────────────────────────────────────────────────────

def _model_button(driver: Any) -> dict:
    btn = _js(driver, _JS_MODEL_BTN, {})
    return btn if isinstance(btn, dict) else {}


def _tab_visible(driver: Any) -> Optional[bool]:
    """document.visibilityState via WebBridge (read-only).

    Trusted CDP clicks are SILENTLY DROPPED while the tab is hidden/occluded
    (observed 2026-09-27 — the same rung works immediately once the tab is
    visible). None means the probe could not be read (treat as visible).
    """
    info = _js(driver, _JS_VISIBILITY, {}, mutating=False)
    if isinstance(info, dict) and "visible" in info:
        return bool(info.get("visible"))
    return None


def _open_model_menu(driver: Any, *, sleep: Callable[[float], None],
                     attempts: int = 2) -> dict:
    """Open the model selector menu and return its rows (menu left OPEN).

    The menu is a Radix portal: synthetic .click() does nothing, a trusted
    CDP mouse click works (verified live 2026-09-21) — but only while the tab
    is actually visible. A hidden tab drops the click without any error, so
    run the visibility gate first: try `Page.bringToFront` through the
    WebBridge CDP channel, and raise `model.tab-hidden` (instead of the
    generic `model.menu-failed`) when the tab cannot be surfaced.
    """
    button = _model_button(driver)
    if not button.get("found"):
        raise ConsoleError("model", "model selector button not found in the composer",
                           code="model.no-button")
    if _tab_visible(driver) is False:
        try:
            driver.cdp("Page.bringToFront")
        except Exception:  # noqa: BLE001 — the visibility gate below decides
            pass
        sleep(0.6)
        if _tab_visible(driver) is False:
            raise ConsoleError(
                "model",
                ("the console tab is hidden/occluded — trusted clicks are silently "
                 "dropped; bring the Chrome tab to the front and retry"),
                evidence=_evidence(driver), code="model.tab-hidden")
    menu = _js(driver, _JS_MODEL_MENU, {})
    for _ in range(attempts):
        if isinstance(menu, dict) and menu.get("open"):
            break
        _cdp_click(driver, button["x"], button["y"], sleep=sleep)
        sleep(1.2)
        menu = _js(driver, _JS_MODEL_MENU, {})
    if not isinstance(menu, dict) or not menu.get("open"):
        raise ConsoleError("model", "model menu did not open after CDP clicks",
                           code="model.menu-failed")
    return {"button": button, "rows": menu.get("rows") or []}


def _close_model_menu(driver: Any, *, sleep: Callable[[float], None]) -> bool:
    menu = _js(driver, _JS_MODEL_MENU, {})
    if not (isinstance(menu, dict) and menu.get("open")):
        return True
    _press_escape(driver, sleep=sleep)
    sleep(0.4)
    menu = _js(driver, _JS_MODEL_MENU, {})
    return not (isinstance(menu, dict) and menu.get("open"))


def _clean_rows(rows: list) -> list:
    return [{"name": r.get("name") or "", "badges": r.get("badges") or [],
             "checked": bool(r.get("checked")), "submenu": bool(r.get("submenu")),
             "x": r.get("x"), "y": r.get("y")}
            for r in rows]


def _ensure_console_tab(driver: Any, state: dict, *, cfg: Config,
                        sleep: Callable[[float], None]) -> None:
    """Make sure the console session has a tab (no navigation if one exists)."""
    if _tabs(driver):
        return
    driver.navigate(BASE_URL, new_tab=True, group_title=state["group_title"])
    sleep(cfg.page_load_wait)


def console_models(*, config: Optional[Config] = None, driver: Any = None,
                   sleep: Callable[[float], None] = time.sleep) -> dict:
    """List the selectable models (name/badges/checked) and the current one."""
    cfg = config or get_config()
    state = load_state()
    drv = driver or _make_driver(cfg, state)
    _ensure_console_tab(drv, state, cfg=cfg, sleep=sleep)
    opened = _open_model_menu(drv, sleep=sleep)
    rows = _clean_rows(opened["rows"])
    closed = _close_model_menu(drv, sleep=sleep)
    current = next((r["name"] for r in rows if r["checked"]), None) \
        or opened["button"].get("label") or ""
    return {"ok": True, "current": current, "models": rows, "menu_closed": closed}


def console_set_model(name: str, *, config: Optional[Config] = None, driver: Any = None,
                      sleep: Callable[[float], None] = time.sleep) -> dict:
    """Switch the composer's model and VERIFY the new label before success."""
    cfg = config or get_config()
    state = load_state()
    drv = driver or _make_driver(cfg, state)
    _ensure_console_tab(drv, state, cfg=cfg, sleep=sleep)
    wanted = _normalize(name).casefold()
    if not wanted:
        raise ConsoleError("model", "empty model name")

    def find_row(rows):
        exact = [r for r in rows if _normalize(r.get("name", "")).casefold() == wanted]
        if not exact:
            exact = [r for r in rows if wanted in _normalize(r.get("name", "")).casefold()]
        return exact[0] if exact else None

    before = _model_button(drv).get("label")
    opened = _open_model_menu(drv, sleep=sleep)
    row = find_row(opened["rows"])
    if row is None:
        available = ", ".join(r.get("name", "?") for r in opened["rows"])
        _close_model_menu(drv, sleep=sleep)
        raise ConsoleError("model", f"model {name!r} not found; available: {available}",
                           code="model.not-found")
    if row.get("submenu"):
        _close_model_menu(drv, sleep=sleep)
        raise ConsoleError("model", f"{row.get('name')!r} is a submenu entry (not supported yet)",
                           code="model.submenu")

    label = ""
    for attempt in (1, 2):
        _cdp_click(drv, row["x"], row["y"], sleep=sleep)
        sleep(1.5)
        _close_model_menu(drv, sleep=sleep)
        label = _model_button(drv).get("label") or ""
        if wanted in _normalize(label).casefold():
            return {"ok": True, "from": before, "to": label, "attempts": attempt}
        if attempt == 1:
            opened = _open_model_menu(drv, sleep=sleep)
            row = find_row(opened["rows"]) or row
    raise ConsoleError("model", f"switch to {name!r} not verified (selector shows {label!r})",
                       evidence=_evidence(drv), code="model.verify-failed")


MAX_INJECT_BYTES = 8 * 1024 * 1024  # larger files need the chrome://extensions file-access route


def _inject_file(driver: Any, path: str) -> dict:
    """Attach a local file by building it in-page (DataTransfer + File).

    This bypasses Chrome's per-extension file access (off by default and not
    toggleable by the extension itself); the WebBridge ``upload`` action
    needs that permission, plain in-page File construction does not.
    """
    p = Path(path).expanduser()
    if not p.is_file():
        raise ConsoleError("file", f"file not found: {path}", code="file.not-found")
    data = p.read_bytes()
    if len(data) > MAX_INJECT_BYTES:
        raise ConsoleError(
            "file",
            f"{p.name} is {len(data)} bytes; in-page injection limit is {MAX_INJECT_BYTES} bytes "
            "(for larger files enable 'Allow access to file URLs' for the Kimi extension)",
            code="file.too-large")
    mime = mimetypes.guess_type(str(p))[0] or "application/octet-stream"
    code = (_JS_INJECT_FILE
            .replace("__B64__", json.dumps(base64.b64encode(data).decode("ascii")))
            .replace("__NAME__", json.dumps(p.name))
            .replace("__MIME__", json.dumps(mime)))
    res = _js(driver, code, {})
    if not isinstance(res, dict) or not res.get("ok"):
        raise ConsoleError("file", f"injection failed for {p.name}: {res}",
                           code="file.inject-failed")
    return {"name": p.name, "size": len(data), "mime": mime}


def _gate_files(driver: Any, files: list, *, sleep: Callable[[float], None],
                wait: float = 30.0, poll: float = 1.0,
                guard_min_elapsed: float = 5.0) -> dict:
    """Gate: every requested file must be attached AND shown as a chip.

    Idempotent: files already present as chips are skipped, so injecting the
    same set twice (e.g. attach-then-fill, or a recovery re-run) never
    duplicates attachments.

    The chip wait carries the no-progress breaker with a ``guard_min_elapsed``
    slow-page grace: chips can legitimately take seconds to surface after a
    large upload, so samples in the first ``guard_min_elapsed`` seconds never
    count towards the streak. Without it the breaker would cut the effective
    chip tolerance from the full ``wait`` budget down to ~3 polls (~6s).
    Pass ``guard_min_elapsed=0.0`` to restore pure fail-fast.
    """
    chips0 = _js(driver, _probe("chips"), {})
    current = chips0.get("attachments") if isinstance(chips0, dict) else []
    injected = []
    for f in files:
        name = Path(f).expanduser().name
        if name in (current or []):
            injected.append({"name": name, "size": None, "mime": None,
                             "already_attached": True})
            continue
        injected.append(_inject_file(driver, f))
    names = [i["name"] for i in injected]
    deadline = time.monotonic() + wait
    chips: Any = []
    guard = NoProgressGuard(gate="file", driver=driver, what="chip-poll",
                            min_elapsed=guard_min_elapsed)
    while True:
        payload = _js(driver, _probe("chips"), {})
        chips = payload.get("attachments") if isinstance(payload, dict) else []
        if all(n in (chips or []) for n in names):
            break
        # Every newly surfaced chip counts as progress; a chip list that is
        # frozen for NO_PROGRESS_LIMIT polls (past the slow-page grace) trips
        # the breaker instead of idling out the full `wait` budget.
        guard.observe({"attachments": chips,
                       "missing": [n for n in names if n not in (chips or [])]})
        if time.monotonic() >= deadline:
            raise ConsoleError("file", f"attachment chips not verified for {names} (saw {chips})",
                               evidence=_evidence(driver), code="file.chip-missing")
        sleep(max(poll, 0.05))
    # let the app finish processing the fresh upload before any composer work
    sleep(2.5)
    return {"ok": True, "injected": injected, "chips": chips}


def _ensure_task_context(drv: Any, state: dict, *, task: str, new_thread: bool,
                         cfg: Config, sleep: Callable[[float], None]) -> dict:
    """Attach to the task's thread (or home for a new thread) and verify.

    ``console open <url>`` binding: when set and the caller did not explicitly
    ask for a new thread, the staged turn continues the bound thread — a
    deliberate thread switch — instead of the task's previous thread or home.
    """
    thread = state["threads"].get(task) or {}
    open_url = state.get("open_url") or ""
    if new_thread:
        state["open_url"] = None
        state["open_url_at"] = None
        target = BASE_URL
    elif open_url and HREF_MATCH_SLACK in open_url:
        target = open_url
    else:
        target = thread.get("url") or BASE_URL
    attach_res = attach(drv, state, target, cfg=cfg, sleep=sleep)
    pre = _info(drv)
    if new_thread and HREF_MATCH_SLACK in (pre.get("url") or ""):
        # A new task must start from home, not inside another thread.
        drv.navigate(BASE_URL, new_tab=False)
        sleep(cfg.page_load_wait)
        pre = _info(drv)
        if HREF_MATCH_SLACK in (pre.get("url") or ""):
            raise ConsoleError("attach", "still inside a thread after new-thread navigation",
                               evidence=_evidence(drv), code="attach.still-thread")
    return {"attach": {"ok": True, **attach_res}, "pre": pre, "target": target}


def _stage_fill(drv: Any, state: dict, cfg: Config, query: str, *,
                task: str, new_thread: bool, files: Optional[list],
                sleep: Callable[[float], None]) -> dict:
    """Stage a turn: ensure context, attach files, fill+verify, record pending.

    Shared by ``console_ask``/``console_send``/``console_fill`` — one
    implementation, three surfaces.
    """
    ctx = _ensure_task_context(drv, state, task=task, new_thread=new_thread,
                               cfg=cfg, sleep=sleep)
    gates: dict = {"attach": ctx["attach"]}
    # RC2/RC6 freshness baseline: content-block snapshot BEFORE this turn is
    # submitted — fallback adoption and count-path new-answer detection must
    # be NEWER than this (a previous turn's answer must never be adopted or
    # settle as this turn's).
    base_blocks = _blocks_baseline(drv)
    file_names = [Path(f).expanduser().name for f in (files or [])]
    file_paths = [str(Path(f).expanduser()) for f in (files or [])]
    if files:
        gates["files"] = _gate_files(drv, files, sleep=sleep)

    try:
        gates["fill"] = _gate_fill(drv, query, sleep=sleep)
    except ConsoleError as fill_exc:
        if fill_exc.gate != "fill":
            raise
        if fill_exc.code == "act.target-occluded":
            # 融合项 d: occlusion is environmental — fail-closed as-is; the
            # desync reload self-heal below is for fill.not-committed only.
            raise
        # Bounded self-heal: a desynced editor (DOM shows text, React state
        # empty) is reset by one page reload; the gate is then retried once.
        logger.warning("fill gate failed (%s); reloading page once and retrying",
                       fill_exc.message)
        reload_url = _info(drv).get("url") or ctx["target"]
        drv.navigate(reload_url, new_tab=False)
        sleep(max(cfg.page_load_wait, 4.0))
        try:
            gates["fill"] = _gate_fill(drv, query, sleep=sleep)
            gates["fill"]["recovered"] = "reload"
        except ConsoleError as exc2:
            exc2.gates = {
                "fill_first_error": {"message": fill_exc.message,
                                     "evidence": fill_exc.evidence},
                **gates,
            }
            raise

    pre = ctx["pre"]
    pending = {
        "task": task,
        "query": query,
        "new_thread": bool(new_thread),
        "files": file_names,
        "file_paths": file_paths,
        "url": _info(drv).get("url") or "",
        "base_bubbles": int(pre.get("bubbles") or 0),
        "base_studied": int(pre.get("studied") or 0),
        "base_prose_count": int(pre.get("proseCount") or 0),
        "base_blocks": base_blocks,
        "filled_at": _now_iso(),
        "status": "filled",
    }
    state["pending"] = pending
    state["active_task"] = task
    save_state(state)
    return {"ok": True, "gates": gates, "pending": pending}


def _submit_with_recovery(drv: Any, cfg: Config, query: str, base_bubbles: int, *,
                          files: Optional[list],
                          submit_timeout: float, submit_recheck_timeout: float,
                          poll_interval: float,
                          sleep: Callable[[float], None],
                          context_gates: Optional[dict] = None,
                          gates_out: Optional[dict] = None,
                          expect_url: Optional[str] = None,
                          base_studied: Optional[int] = None) -> dict:
    """Submit gate with bounded recovery (delayed ownership → reload+retry).

    The recovery is duplicate-safe: it only re-submits after a delayed
    ownership recheck proves the turn was NOT actually sent.
    """
    if expect_url:
        current = _info(drv).get("url") or ""
        if not _url_matches(current, expect_url):
            raise ConsoleError(
                "pending",
                f"page moved: staged on {expect_url!r}, currently at {current!r}; "
                f"run `console fill` again",
                code="pending.page-moved")
    try:
        return _gate_submit(drv, query, base_bubbles,
                            timeout=submit_timeout, poll=poll_interval,
                            sleep=sleep, base_studied=base_studied)
    except ConsoleError as submit_exc:
        if submit_exc.gate != "submit":
            raise
        if submit_exc.code in ("probe.fallback-exhausted", "act.target-occluded"):
            # WARN red line: without an independent identity binding the
            # ownership claim can never be recovered by reloading/re-sending —
            # stop here (fail-closed), never retry a send on missing evidence.
            # Same for act.target-occluded (融合项 d): a covered/off-viewport
            # target is never blind-clicked and never auto-resubmitted.
            raise
        # First, give a slow/duplicated ownership read one more chance so a
        # late-but-correct turn never gets sent twice. A breaker trip here
        # means the page is frozen (nothing to duplicate) — treat it as
        # "not owned" and continue to the reload recovery below.
        late_owned, _, _ = _ownership_or_exhausted(
            drv, query, base_bubbles, timeout=submit_recheck_timeout,
            poll=poll_interval, sleep=sleep)
        if late_owned:
            return {"ok": True, "mechanism": "delayed-ownership",
                    "actions": [{"action": "late-ownership", "result": "ok"}]}
        # Bounded recovery: a mis-sent state (e.g. file-only submission /
        # stale editor state) is cleared by one page reload; re-inject
        # files and retry the submit gate exactly once.
        logger.warning("submit gate failed (%s); reloading and retrying once",
                       submit_exc.message)
        reload_url = _info(drv).get("url") or BASE_URL
        drv.navigate(reload_url, new_tab=False)
        sleep(max(cfg.page_load_wait, 4.0))
        files_retry = None
        if files:
            files_retry = _gate_files(drv, files, sleep=sleep)
            if gates_out is not None:
                gates_out["files_retry"] = files_retry
        try:
            result = _gate_submit(drv, query, base_bubbles,
                                  timeout=submit_timeout, poll=poll_interval,
                                  sleep=sleep, base_studied=base_studied)
            result["recovered"] = "reload"
            return result
        except ConsoleError as exc2:
            # keep the terminal gate's own detail (e.g. the per-rung
            # no_progress breakdown) alongside the recovery context
            merge = {**(exc2.gates or {}),
                     "submit_first_error": {"message": submit_exc.message,
                                            "evidence": submit_exc.evidence}}
            if files_retry is not None:
                merge["files_retry"] = files_retry
            if context_gates:
                merge.update(context_gates)
            exc2.gates = merge
            raise


def _scroll_to_bottom(driver: Any, *, prose_len: Callable[[], int],
                      max_rounds: int = 6,
                      sleep: Callable[[float], None] = time.sleep) -> dict:
    """Scroll the answer container to its bottom and wait for a settle.

    Probe ``_JS_SCROLL`` discovers the last prose's scrollable ancestor
    (live: ``div.scrollable-container.overflow-auto``; falls back to
    ``document.scrollingElement``). Settled ⟺ two consecutive EQUAL, non-zero
    prose-length readings AND the probe reports the bottom reached (length
    equality, not heights — lazy rendering keeps appending).
    """
    prev: Optional[int] = None
    res: dict = {}
    container = ""
    cur = 0
    settled = False
    rounds = 0
    for rounds in range(1, max(1, max_rounds) + 1):
        raw = _js(driver, _JS_SCROLL, {})
        res = raw if isinstance(raw, dict) else {}
        if res.get("container"):
            container = str(res["container"])
        cur = int(prose_len() or 0)
        if cur > 0 and cur == prev and bool(res.get("bottom")):
            settled = True
            break
        prev = cur
        if rounds < max_rounds:
            sleep(0.2)
    out: dict = {"settled": settled, "rounds": rounds, "container": container,
                 "prose": cur}
    if not settled:
        out["warning"] = "complete.scroll-unsettled"
    return out


_TERMINATORS = "。！？.!?;；:：）)】]`\"'”’…—|>"


def _truncation_risk(text: str, *, still_generating: bool) -> bool:
    """Advisory truncation flag: risky ⟺ still busy ∧ tail has no terminator.

    still_generating must be a busy signal (stop control visible OR action icon
    != idle) — NEVER the whole-page `generating` regex (pinned true by the
    model badge 『… 正在思考』)."""
    tail = (text or "").rstrip("​ \n\t")
    return bool(still_generating and tail and tail[-1] not in _TERMINATORS)


def _truncation_risk_fields(text: str, *, still_generating: bool) -> dict:
    risk = _truncation_risk(text, still_generating=still_generating)
    return {"answer_terminated": not risk, "truncation_risk": risk}


def _extract_step(drv: Any, state: dict, cfg: Config, *,
                  sleep: Callable[[float], None],
                  pending: Optional[dict] = None,
                  gates_out: Optional[dict] = None,
                  consume: bool = True) -> dict:
    """Expand, extract the turn-scoped answer + sources, update bookkeeping.

    With ``pending`` the thread record is updated and the staged turn is
    cleared (exactly once); without it this is a read-only ad-hoc extract.
    peek/again (``consume=False``): strictly read-only — no disk write, the
    staged turn is NOT consumed and thread turn counts are NOT incremented.
    """
    gates = gates_out if gates_out is not None else {}
    fallback_used: list = []
    fallback_summary = ""

    expand = _js(drv, _probe("expand"), "none")
    if expand == "clicked":
        sleep(1.0)
        gates["expand"] = expand
    else:
        # Rung 2 for the expand control: the exact-label probe fully missed.
        # Candidates come from the element table and only count as success
        # after readback + effect verification (the content block must GROW).
        fb = _expand_fallback_rung(drv, sleep=sleep)
        gates["expand"] = expand
        if fb.get("status") not in ("unavailable", "none"):
            gates["expand_fallback"] = {k: v for k, v in fb.items() if k != "text"}
        if fb.get("status") == "ok":
            fallback_used.append(fb["fallback_used"])
            fallback_summary = fb.get("summary", "")
        elif fb.get("status") == "exhausted":
            raise ConsoleError(
                "extract",
                f"expand control missed by the probe AND the element-table "
                f"fallback could not verify a candidate ({fb.get('candidates', 0)}"
                f" candidate(s), no click grew the answer) — fail-closed",
                gates=gates, evidence=_evidence(drv),
                code="probe.fallback-exhausted")

    # T5: lazy rendering appends while scrolling — reach the bottom first and
    # record the settle verdict as its own gate (advisory, never blocks).
    scroll_out = _scroll_to_bottom(
        drv,
        prose_len=lambda: _answer_len_now(drv),
        sleep=sleep)
    gates["scroll"] = scroll_out

    prose = _js(drv, _JS_PROSE, {}, mutating=False)
    if (not isinstance(prose, dict) or not prose.get("found")
            or not _normalize(prose.get("text"))):
        # Rung 2 for the answer text (`div.prose` missing/empty): adopt the
        # largest qualified content block only after a semantic readback —
        # and, with the pre-submit baseline (RC2), only when it is NEWER.
        fb = _prose_fallback_rung(
            drv, baseline=(pending or {}).get("base_blocks"))
        if fb.get("status") == "ok":
            prose = {"found": True, "text": fb["text"], "raw": fb["text"]}
            fallback_used.append(fb["fallback_used"])
            fallback_summary = fb.get("summary", "")
            gates["extract"] = {"ok": True, "chars": len(prose["text"]),
                                "fallback_used": fb["fallback_used"],
                                "fallback_summary": fb.get("summary", ""),
                                "stale_risk": bool(fb.get("stale_risk"))}
        elif fb.get("status") == "exhausted":
            gates["extract"] = {"ok": False,
                                "fallback_used": fb.get("fallback_used"),
                                "fallback_summary": fb.get("summary", ""),
                                "fallback_candidates": fb.get("candidates", 0)}
            raise ConsoleError(
                "extract",
                f"latest answer text is empty and the element-table fallback "
                f"had no adoptable content block ({fb.get('candidates', 0)}"
                f" candidate(s)) — fail-closed",
                gates=gates, evidence=_evidence(drv),
                code="probe.fallback-exhausted")
        else:
            gates["extract"] = {"ok": False}
            raise ConsoleError("extract", "latest answer text is empty",
                               gates=gates, evidence=_evidence(drv),
                               code="extract.empty")
    else:
        gates["extract"] = {"ok": True, "chars": len(prose["text"])}

    file_names = list((pending or {}).get("files") or [])
    if file_names:
        payload = _js(drv, _probe("chips"), {}, mutating=False)
        remaining = payload.get("attachments") if isinstance(payload, dict) else []
        gates["send"] = {"chips_cleared": not any(n in (remaining or []) for n in file_names)}

    sources = _js(drv, _JS_SOURCES, [], mutating=False)
    if not isinstance(sources, list):
        sources = []

    post = _info(drv)
    url = post.get("url") or ""
    # T6: busy = stop control visible OR non-idle action icon — the
    # whole-page `generating` regex is pinned true by the model badge, so it
    # must never feed this signal. Missing info ⇒ busy=False (flag only).
    busy = bool(post.get("stop_button")) or (
        (post.get("action_icon") or "") not in ("", SUBMIT_ICON_IDLE))
    if pending and consume:
        # consumption block: turn bookkeeping + staged-turn clear + persist.
        # consume=False (peek/again) skips ALL of it — read-only, no disk write.
        task_name = pending.get("task") or "default"
        q = pending.get("query") or ""
        now = _now_iso()
        if HREF_MATCH_SLACK in url:
            entry = dict(state["threads"].get(task_name) or {})
            switched = bool(entry.get("url")) and not _url_matches(entry["url"], url)
            entry.update({"url": url, "last_used_at": now})
            if (pending.get("new_thread") or switched
                    or not entry.get("created_at") or "url" not in entry):
                entry["created_at"] = now
                entry["label"] = _normalize(q)[:80]
                entry["turns"] = 1
            else:
                entry["turns"] = int(entry.get("turns") or 0) + 1
            if not entry.get("label"):
                entry["label"] = _normalize(q)[:80]
            state["threads"][task_name] = entry
        state["active_task"] = task_name
        state["pending"] = None  # the staged turn is consumed
        # The `console open <url>` binding is one-shot: it has served this turn
        # (the thread is now registered above), so drop it.
        state["open_url"] = None
        state["open_url_at"] = None
        save_state(state)

    return {
        "ok": True,
        "answer": prose["text"],
        "raw_answer": prose.get("raw", prose["text"]),
        "sources": sources,
        "url": url,
        "title": post.get("title") or "",
        "model": post.get("model") or "",
        "consumed": bool(pending and consume),
        **({"fallback_used": ",".join(fallback_used),
            "fallback_summary": fallback_summary} if fallback_used else {}),
        **_truncation_risk_fields(prose["text"], still_generating=busy),
    }


def console_ask(query: str, *, task: str = "default", new_thread: bool = False,
                files: Optional[list] = None,
                wait_budget: float = DEFAULT_WAIT, poll_interval: float = POLL_INTERVAL,
                submit_timeout: float = SUBMIT_TIMEOUT,
                submit_recheck_timeout: float = 6.0,
                judge: Optional[bool] = None,
                model: Optional[str] = None,
                config: Optional[Config] = None, driver: Any = None,
                sleep: Callable[[float], None] = time.sleep) -> dict:
    """Ask the resident console one question, with every step verified.

    Composite of the granular steps (fill → submit → wait → extract), each
    backed by the same gate implementation the step commands use. One task =
    one Perplexity thread; without ``new_thread`` the task's thread is
    continued as a follow-up.
    """
    cfg = config or get_config()
    state = load_state()
    drv = driver or _make_driver(cfg, state)
    if model:
        console_set_model(model, config=cfg, driver=drv, sleep=sleep)
    started = time.monotonic()

    try:
        staged = _stage_fill(drv, state, cfg, query, task=task,
                             new_thread=new_thread, files=files, sleep=sleep)
        gates = dict(staged["gates"])
        pending = staged["pending"]

        gates["submit"] = _submit_with_recovery(
            drv, cfg, query, pending["base_bubbles"], files=files,
            submit_timeout=submit_timeout,
            submit_recheck_timeout=submit_recheck_timeout,
            poll_interval=poll_interval, sleep=sleep, context_gates=gates,
            gates_out=gates,
            base_studied=pending.get("base_studied"))

        gates["complete"] = _gate_complete(
            drv, pending["base_studied"],
            base_prose_count=pending["base_prose_count"],
            base_blocks=pending.get("base_blocks"),
            wait_budget=wait_budget, poll=poll_interval, sleep=sleep)

        out = _extract_step(drv, state, cfg, sleep=sleep, pending=pending,
                            gates_out=gates)
        judgment = console_judge.judge_extraction(query, out["answer"],
                                                  flag=judge)
        _log_run("ask", ok=True, url=out["url"],
                 elapsed=time.monotonic() - started)

        return {
            "ok": True,
            "answer": out["answer"],
            "judge": judgment,
            "raw_answer": out["raw_answer"],
            "sources": out["sources"],
            "url": out["url"],
            "title": out["title"],
            "model": out["model"],
            "attachments": pending["files"],
            "task": task,
            "session": state["session"],
            "new_thread": new_thread,
            "gates": gates,
            "elapsed_s": round(time.monotonic() - started, 1),
            **({"fallback_used": out["fallback_used"],
                "fallback_summary": out.get("fallback_summary", "")}
               if out.get("fallback_used") else {}),
        }
    except ConsoleError as exc:
        # T8: the composite ask/send path records every failure too
        _fail_log("ask", exc, state, elapsed_s=time.monotonic() - started)
        raise


# ──────────────────────────────────────────────────────────────
# Granular steps (intent composition surface)
# ──────────────────────────────────────────────────────────────

def console_open(target: str, *, new_thread: bool = False,
                 config: Optional[Config] = None, driver: Any = None,
                 sleep: Callable[[float], None] = time.sleep) -> dict:
    """Attach the console tab to a task thread (by name) or a direct URL.

    A direct URL is additionally **bound** to the next fill/ask/send: the next
    staged turn continues that thread even if its task has an older thread of
    its own (one-shot binding, consumed when the turn is extracted). Switching
    by task name clears any leftover URL binding.
    """
    cfg = config or get_config()
    state = load_state()
    drv = driver or _make_driver(cfg, state)
    if target.startswith("http"):
        tabs = _tabs(drv)
        if tabs:
            drv.navigate(target, new_tab=False)
        else:
            drv.navigate(target, new_tab=True, group_title=state["group_title"])
        sleep(cfg.page_load_wait)
        info = _info(drv)
        if not _url_matches(info.get("url") or "", target):
            raise ConsoleError("attach", f"tab did not reach {target!r}",
                               evidence=_evidence(drv), code="attach.navigate")
        state["open_url"] = info.get("url") or target
        state["open_url_at"] = _now_iso()
        save_state(state)
        _log_run("open", ok=True, url=info.get("url"))
        return {"ok": True, "url": info.get("url") or "", "target": target,
                "new_thread": False, "bound": state["open_url"]}
    ctx = _ensure_task_context(drv, state, task=target, new_thread=new_thread,
                               cfg=cfg, sleep=sleep)
    state["active_task"] = target
    state["open_url"] = None
    state["open_url_at"] = None
    save_state(state)
    _log_run("open", ok=True, url=ctx["pre"].get("url"))
    return {"ok": True, "url": ctx["pre"].get("url") or "", "target": target,
            "new_thread": new_thread, "attach": ctx["attach"]}


def _reload_console_tab(cfg: Config, state: dict, *,
                        sleep: Callable[[float], None],
                        driver: Any = None) -> None:
    """Reload the console's current tab (used by Jev-directed recovery)."""
    drv = driver or _make_driver(cfg, state)
    current = _info(drv).get("url") or BASE_URL
    drv.navigate(current, new_tab=False)
    sleep(max(cfg.page_load_wait, 4.0))


def _run_with_jev_recovery(step: str, run: Callable[[], dict], *,
                           judge: Optional[bool], cfg: Config, state: dict,
                           sleep: Callable[[float], None],
                           driver: Any = None,
                           allow_reload: bool = True) -> dict:
    """Run a step; on failure with judging on, let Jev pick ONE bounded remedy.

    Concept from browser-use/jev-ultrafast: Jev chooses among offered
    operations, code owns execution and safety. Scope limits here:

    - only safe, non-send steps (fill / wait / extract) — send paths stay
      advisory-only so an automatic retry can never double-send;
    - the remedy set is fixed {retry-step, reload-and-retry, wait-longer,
      escalate} and exactly ONE extra attempt is executed;
    - the retried run passes every original gate again; any non-ok decision
      (escalate / unavailable / skipped) re-raises the original error;
    - ``allow_reload=False`` (peek/again: read-only paths) forbids the
      reload-and-retry remedy — a reload would re-stream the page — so a
      reload decision re-raises the original error instead of executing;
      every other route follows the normal ladder (backward compatible:
      default True keeps reload-and-retry available).
    """
    try:
        return run()
    except ConsoleError as exc:
        if step not in ("fill", "wait", "extract"):
            _fail_log(step, exc, state)  # T8: every final exit is recorded
            raise
        decision = console_judge.route_hint(exc.gate, exc.code, exc.message, flag=judge)
        route = decision.get("route") if decision.get("status") == "ok" else None
        if route not in ("retry-step", "reload-and-retry", "wait-longer") or (
                route == "reload-and-retry" and not allow_reload):
            # escalate / unavailable / skipped / reload-forbidden: record the
            # failure (T8), then let the original error stand
            _fail_log(step, exc, state)
            raise
        logger.warning("jev-directed recovery: %s (confidence %.2f) after %s",
                       route, decision.get("confidence") or 0.0, exc.code or exc.gate)
        if route == "reload-and-retry":
            _reload_console_tab(cfg, state, sleep=sleep, driver=driver)
        elif route == "wait-longer":
            sleep(6.0)
        try:
            result = run()
        except ConsoleError as exc2:
            exc2.gates = {"jev_recovery": {"route": route, "applied": True,
                                           "attempts": 1, "first_error": exc.message},
                          **exc2.gates}
            _fail_log(step, exc2, state)  # T8: bounded retry failed too
            raise
        if isinstance(result, dict):
            gates = result.setdefault("gates", {})
            if isinstance(gates, dict):
                gates["jev_recovery"] = {"route": route,
                                         "confidence": decision.get("confidence"),
                                         "applied": True, "attempts": 1}
        return result


def console_fill(query: str, *, task: str = "default", new_thread: bool = False,
                 files: Optional[list] = None,
                 judge: Optional[bool] = None,
                 config: Optional[Config] = None, driver: Any = None,
                 sleep: Callable[[float], None] = time.sleep) -> dict:
    """Stage a turn: attach files, fill the composer, verify — no send."""
    cfg = config or get_config()
    state = load_state()
    drv = driver or _make_driver(cfg, state)

    def _once() -> dict:
        staged = _stage_fill(drv, state, cfg, query, task=task, new_thread=new_thread,
                             files=files, sleep=sleep)
        _log_run("fill", ok=True, url=staged["pending"].get("url"))
        return {"ok": True, "gates": staged["gates"], "pending": staged["pending"]}

    return _run_with_jev_recovery("fill", _once, judge=judge, cfg=cfg, state=state,
                                  sleep=sleep, driver=drv)


def console_submit(*, config: Optional[Config] = None, driver: Any = None,
                   sleep: Callable[[float], None] = time.sleep,
                   submit_timeout: float = SUBMIT_TIMEOUT,
                   submit_recheck_timeout: float = 6.0,
                   poll_interval: float = POLL_INTERVAL,
                   allow_reattach: bool = True) -> dict:
    """Submit the staged turn (composer re-verified; bounded recovery).

    ``allow_reattach`` (T8): on ``pending.page-moved`` / bridge-lost
    (``attach.*``-family) errors the tab is re-attached via ``console_open``
    at MOST ONCE per call, then only the stage/verify readback is retried.
    A submit action that may already have been emitted is never replayed
    (double-send guard): for bridge-lost errors — whose send state is
    unknown — ownership is re-verified after the re-attach first and, if the
    turn already landed, the verify result is returned without re-sending.
    ``allow_reattach=False`` restores the fail-fast behavior exactly.
    Failures are recorded in runs.jsonl (``ok=False`` + error code).
    """
    cfg = config or get_config()
    state = load_state()
    drv = driver or _make_driver(cfg, state)
    reattached = False
    while True:
        try:
            pending = _pending_require(state, stage="submit")
            gates: dict = {}
            gates["submit"] = _submit_with_recovery(
                drv, cfg, pending["query"], int(pending.get("base_bubbles") or 0),
                files=list(pending.get("file_paths") or []),
                submit_timeout=submit_timeout,
                submit_recheck_timeout=submit_recheck_timeout,
                poll_interval=poll_interval, sleep=sleep, context_gates={},
                gates_out=gates, expect_url=pending.get("url"),
                base_studied=pending.get("base_studied"))
            break
        except ConsoleError as exc:
            if not (allow_reattach and not reattached
                    and (exc.code or "") in _REATTACH_CODES):
                _fail_log("submit", exc, state)
                raise
            # bounded re-attach ladder: ONE console_open, then readback only
            target = ((_pending(state) or {}).get("task")
                      or state.get("active_task") or "default")
            try:
                console_open(target, config=cfg, driver=drv, sleep=sleep,
                             new_thread=False)
            except ConsoleError as oexc:
                _fail_log("submit", oexc, state)
                raise oexc from exc
            reattached = True
            state = load_state()
            if exc.code != "pending.page-moved":
                # bridge lost mid-flight: send state unknown — verify FIRST,
                # never replay a submit that already landed. The ownership
                # recheck is an anti-double-send BOOLEAN contract, so the
                # no-progress breaker must not escape here: a trip only means
                # ownership could not be confirmed ("not sent" for this
                # check) and falls into the original bounded retry below.
                p2 = _pending(state) or {}
                q = p2.get("query")
                owned, _, _ = _ownership_or_exhausted(
                    drv, q or "", int(p2.get("base_bubbles") or 0),
                    timeout=submit_recheck_timeout, poll=poll_interval,
                    sleep=sleep)
                sent = bool(p2.get("submitted_at")) or (bool(q) and owned)
                if sent:
                    if not p2.get("submitted_at"):
                        p2["submitted_at"] = _now_iso()
                        p2["status"] = "submitted"
                        state["pending"] = p2
                        save_state(state)
                    _log_run("submit", ok=True, url=p2.get("url"))
                    return {"ok": True,
                            "gates": {"submit": {"ok": True,
                                                 "mechanism": "reattach-verify"}},
                            "pending_status": "submitted", "reattached": True}
            # not sent (page-moved fires pre-send): retry the readback once —
            # the `reattached` guard bounds this to a single extra attempt
    pending["submitted_at"] = _now_iso()
    pending["status"] = "submitted"
    state["pending"] = pending
    save_state(state)
    _log_run("submit", ok=True, url=pending.get("url"))
    out: dict = {"ok": True, "gates": gates, "pending_status": "submitted"}
    if reattached:
        out["reattached"] = True
    return out


def console_wait(*, config: Optional[Config] = None, driver: Any = None,
                 judge: Optional[bool] = None,
                 sleep: Callable[[float], None] = time.sleep,
                 wait_budget: float = DEFAULT_WAIT,
                 poll_interval: float = POLL_INTERVAL) -> dict:
    """Wait for the staged turn's answer to settle (turn-scoped completion)."""
    cfg = config or get_config()
    state = load_state()
    drv = driver or _make_driver(cfg, state)

    def _once() -> dict:
        pending = _pending_require(state, stage="wait")
        gate = _gate_complete(drv, int(pending.get("base_studied") or 0),
                              base_prose_count=int(pending.get("base_prose_count") or 0),
                              base_blocks=pending.get("base_blocks"),
                              wait_budget=wait_budget, poll=poll_interval, sleep=sleep)
        pending["completed_at"] = _now_iso()
        pending["status"] = "completed"
        state["pending"] = pending
        save_state(state)
        _log_run("wait", ok=True, url=pending.get("url"))
        return {"ok": True, "gates": {"complete": gate}}

    return _run_with_jev_recovery("wait", _once, judge=judge, cfg=cfg, state=state,
                                  sleep=sleep, driver=drv)


def console_extract(*, config: Optional[Config] = None, driver: Any = None,
                    judge: Optional[bool] = None,
                    strict: bool = False,
                    peek: bool = False,
                    again: bool = False,
                    sleep: Callable[[float], None] = time.sleep) -> dict:
    """Extract the newest answer (+sources); consumes the staged turn.

    ``strict`` turns the advisory truncation flag into a hard failure
    (``extract.truncation-risk``); by default a risky answer is only marked.

    peek/again are read-only re-reads (mutually exclusive):
    - ``peek=True``: reads the staged turn WITHOUT consuming it (no disk
      write, no turn increment — the pending record survives);
    - ``again=True``: re-reads without a staged turn at all (the task
      falls back to ``state["active_task"]``).
    Both disable the reload-and-retry remedy (``allow_reload=False``):
    a reload would re-stream the page under a read-only call.
    """
    if peek and again:
        raise ConsoleError("extract", "--peek 与 --again 互斥（只读重读只能选其一）",
                           code="extract.flag-conflict")
    cfg = config or get_config()
    state = load_state()
    drv = driver or _make_driver(cfg, state)

    def _once() -> dict:
        pending = None if again else (_pending(state) or None)
        gates: dict = {}
        out = _extract_step(drv, state, cfg, sleep=sleep, pending=pending,
                            gates_out=gates, consume=not peek)
        out["gates"] = gates
        out["task"] = (pending or {}).get("task") or state.get("active_task")
        # --again has no staged turn: fall back to the thread's recorded query
        # label so the judge is not starved of the question (bug 2026-09-27).
        task_for_query = out["task"] or "default"
        judge_query = ((pending or {}).get("query")
                       or (state.get("threads", {}).get(task_for_query) or {}).get("label")
                       or "")
        out["judge"] = console_judge.judge_extraction(
            judge_query, out.get("answer") or "", flag=judge)
        _log_run("extract", ok=True, url=out.get("url"),
                 truncation_risk=out.get("truncation_risk"))
        return out

    out = _run_with_jev_recovery("extract", _once, judge=judge, cfg=cfg, state=state,
                                 sleep=sleep, driver=drv,
                                 allow_reload=not (peek or again))
    if strict and out.get("truncation_risk"):
        err = ConsoleError("extract", "答案疑似截断（strict 模式）",
                           gates={"extract": {"truncation_risk": True}},
                           code="extract.truncation-risk")
        _fail_log("extract", err, state)  # T8: strict gate failure is recorded
        raise err
    return out


def console_send(query: str, *, task: str = "default", new_thread: bool = False,
                 files: Optional[list] = None,
                 config: Optional[Config] = None, driver: Any = None,
                 sleep: Callable[[float], None] = time.sleep,
                 submit_timeout: float = SUBMIT_TIMEOUT,
                 submit_recheck_timeout: float = 6.0,
                 poll_interval: float = POLL_INTERVAL) -> dict:
    """Stage and submit in one call (fill + submit); no wait/extract."""
    cfg = config or get_config()
    state = load_state()
    drv = driver or _make_driver(cfg, state)
    try:
        staged = _stage_fill(drv, state, cfg, query, task=task,
                             new_thread=new_thread, files=files, sleep=sleep)
        gates = dict(staged["gates"])
        pending = staged["pending"]
        gates["submit"] = _submit_with_recovery(
            drv, cfg, query, pending["base_bubbles"], files=files,
            submit_timeout=submit_timeout,
            submit_recheck_timeout=submit_recheck_timeout,
            poll_interval=poll_interval, sleep=sleep, context_gates=gates,
            gates_out=gates,
            base_studied=pending.get("base_studied"))
        pending["submitted_at"] = _now_iso()
        pending["status"] = "submitted"
        state["pending"] = pending
        save_state(state)
        _log_run("send", ok=True, url=pending.get("url"))
        return {"ok": True, "gates": gates, "pending": pending, "task": task}
    except ConsoleError as exc:
        # T8: send failures always leave an ok=False + error-code record
        _fail_log("send", exc, state)
        raise


def console_attach(files: list, *, config: Optional[Config] = None, driver: Any = None,
                   sleep: Callable[[float], None] = time.sleep) -> dict:
    """Attach local files to the composer (idempotent, chips verified)."""
    cfg = config or get_config()
    state = load_state()
    drv = driver or _make_driver(cfg, state)
    if not files:
        raise ConsoleError("file", "no files given", code="file.not-found")
    _ensure_console_tab(drv, state, cfg=cfg, sleep=sleep)
    gate = _gate_files(drv, files, sleep=sleep)
    pending = _pending(state)
    if not pending:
        pending = {"task": state.get("active_task") or "default", "query": None,
                   "new_thread": False, "files": [], "file_paths": [],
                   "url": _info(drv).get("url") or "", "filled_at": _now_iso(),
                   "status": "attached"}
    names = [i["name"] for i in gate["injected"]]
    pending["files"] = sorted(set(list(pending.get("files") or []) + names))
    pending["file_paths"] = sorted(set(list(pending.get("file_paths") or []) +
                                       [str(Path(f).expanduser()) for f in files]))
    state["pending"] = pending
    save_state(state)
    _log_run("attach", ok=True)
    return {"ok": True, "gates": {"files": gate}, "pending_files": pending["files"]}


def console_detach(name: str, *, config: Optional[Config] = None, driver: Any = None,
                   sleep: Callable[[float], None] = time.sleep) -> dict:
    """Remove one composer attachment by name (verified)."""
    cfg = config or get_config()
    state = load_state()
    drv = driver or _make_driver(cfg, state)
    code = ("""(() => { const removeBtn = Array.from(document.querySelectorAll('button'))"""
            """.find(b => (b.getAttribute('aria-label') || '') === __LABEL__); """
            """if (!removeBtn) return 'not-found'; removeBtn.click(); return 'clicked'; })()"""
            ).replace("__LABEL__", json.dumps(get_ui_string("remove_prefix", _probe_locale()) + name))
    result = _js(drv, code, "not-found")
    if result != "clicked":
        raise ConsoleError("file", f"attachment {name!r} not found as a chip",
                           code="file.chip-missing")
    sleep(1.0)
    chips = _js(drv, _probe("chips"), {}, mutating=False)
    remaining = chips.get("attachments") if isinstance(chips, dict) else []
    if name in (remaining or []):
        raise ConsoleError("file", f"attachment {name!r} still present after remove",
                           code="file.chip-missing")
    pending = _pending(state)
    if pending:
        pending["files"] = [n for n in (pending.get("files") or []) if n != name]
        pending["file_paths"] = [p for p in (pending.get("file_paths") or [])
                                 if Path(p).name != name]
        state["pending"] = pending
        save_state(state)
    _log_run("detach", ok=True)
    return {"ok": True, "detached": name, "chips": remaining or []}


def console_files(*, config: Optional[Config] = None, driver: Any = None,
                  sleep: Callable[[float], None] = time.sleep) -> dict:
    """List current composer attachments and the staged file set."""
    cfg = config or get_config()
    state = load_state()
    drv = driver or _make_driver(cfg, state)
    _ensure_console_tab(drv, state, cfg=cfg, sleep=sleep)
    chips = _js(drv, _probe("chips"), {}, mutating=False)
    attachments = chips.get("attachments") if isinstance(chips, dict) else []
    pending = _pending(state)
    return {"ok": True, "chips": attachments,
            "pending_files": pending.get("files") or [],
            "pending_status": pending.get("status")}


def console_status(*, config: Optional[Config] = None, driver: Any = None) -> dict:
    """Read-only view of console state plus a live tab readback."""
    state = load_state()
    out = {
        "session": state["session"],
        "group_title": state["group_title"],
        "active_task": state.get("active_task"),
        "threads": state.get("threads") or {},
        "pending": state.get("pending"),
        "live": None,
    }
    drv = driver or _make_driver(config or get_config(), state)
    try:
        tabs = _tabs(drv)
    except ConsoleError as exc:
        out["live"] = {"error": str(exc)}
        return out
    if not tabs:
        out["live"] = {"tabs": 0, "note": "no live tab in this session (attach will recreate)"}
        return out
    info = _info(drv)
    out["live"] = {
        "tabs": len(tabs),
        "url": info.get("url"),
        "title": info.get("title"),
        "on_thread": HREF_MATCH_SLACK in (info.get("url") or ""),
        "bubbles": info.get("bubbles"),
        "studied": info.get("studied"),
        "prose_count": info.get("proseCount"),
        "model": info.get("model"),
    }
    return out


def console_threads() -> dict:
    """List the recorded task threads."""
    state = load_state()
    return {
        "session": state["session"],
        "group_title": state["group_title"],
        "active_task": state.get("active_task"),
        "threads": state.get("threads") or {},
    }


# ──────────────────────────────────────────────────────────────
# Read-only probe drift report
# (`perplexity console drift` / `perplexity console selfcheck --drift`)
# ──────────────────────────────────────────────────────────────

# The 12 `_JS_*` probes, in source order, tagged read (safe to execute) or
# action (would click / type / scroll / inject a file). A read-only selfcheck
# must never fire an action probe: `_JS_CLICK_SUBMIT` literally submits a
# message, `_JS_ENTER_COMBO` types Enter, `_JS_EXPAND` clicks and
# `_JS_INJECT_FILE` is an uninstantiated template anyway.
DRIFT_PROBES: tuple = (
    ("info", "read"),
    ("prose", "read"),
    ("scroll", "action"),
    ("sources", "read"),
    ("click_submit", "action"),
    ("enter_combo", "action"),
    ("expand", "action"),
    ("model_btn", "read"),
    ("visibility", "read"),
    ("model_menu", "read"),
    ("chips", "read"),
    ("inject_file", "action"),
)

DRIFT_STATIC_REASONS: dict = {
    "scroll": "would scroll the page (mutating probe)",
    "click_submit": "would click the submit control",
    "enter_combo": "would dispatch Enter to the composer",
    "expand": "would click the expand control",
    "inject_file": "would inject a file into the composer (template: __B64__)",
}

_DRIFT_STATIC_MARKERS: dict = {
    "scroll": ("overflowY", "scrollingElement"),
    "click_submit": ('aria-label="提交"', ".click()"),
    "enter_combo": ("dispatchEvent", "Enter"),
    "inject_file": ("input[type=file]", "__B64__"),
}


def _drift_source(name: str) -> str:
    """Source of probe ``name`` (``info``/``expand``/``chips`` are locale-built)."""
    if name in _PROBE_BUILDERS:
        return _probe(name)
    return globals()["_JS_" + name.upper()]


def _drift_markers(name: str, locale: str) -> tuple:
    """Expected selectors/labels for a static (unexecuted) probe check."""
    if name == "expand":
        return (get_ui_string("expand", locale), get_ui_string("show_more", locale))
    return _DRIFT_STATIC_MARKERS.get(name, ())


def _drift_static_found(name: str, probes: dict) -> Optional[bool]:
    """Read-only `found` for an action probe, derived from an executed probe."""
    if name == "click_submit":
        button = (probes.get("info") or {}).get("summary") or {}
        state = button.get("submit_button")
        return None if state is None else state != "missing"
    return None


def _drift_summary(name: str, value: Any) -> tuple:
    """One executed probe -> ``(summary, found, anomalies)``.

    ``found`` reports whether the probe's target structure was present in the
    DOM (prose/model control/valid payload); ``anomalies`` flags anchor counts
    that do not match the shape the probe was written against.
    """
    if name == "info":
        if not isinstance(value, dict) or not value:
            return {"payload": value}, None, ["empty payload"]
        notes = []
        if not value.get("url"):
            notes.append("url is empty")
        if value.get("submit_button") == "missing":
            notes.append("submit control not found (submit_button=missing)")
        return {"url": value.get("url"),
                "bubbles": value.get("bubbles"),
                "studied": value.get("studied"),
                "prose_count": value.get("proseCount"),
                "submit_button": value.get("submit_button"),
                "stop_button": value.get("stop_button"),
                "action_icon": value.get("action_icon"),
                "model": value.get("model"),
                "composer_len": len(str(value.get("composer") or ""))}, True, notes
    if name == "prose":
        if not isinstance(value, dict):
            return {"payload": value}, None, ["payload is not an object"]
        found = bool(value.get("found"))
        text = str(value.get("text") or "")
        notes = ["found but text is empty"] if found and not text.strip() else []
        return {"found": found, "text_len": len(text)}, found, notes
    if name == "sources":
        if not isinstance(value, list):
            return {"payload": value}, False, ["payload is not a list"]
        return {"count": len(value)}, True, []
    if name == "model_btn":
        if not isinstance(value, dict):
            return {"payload": value}, None, ["payload is not an object"]
        found = bool(value.get("found"))
        return {"found": found, "label": value.get("label"),
                "expanded": value.get("expanded")}, found, []
    if name == "visibility":
        if not isinstance(value, dict) or "visible" not in value:
            return {"payload": value}, None, ["payload has no `visible` field"]
        notes = ([] if value.get("visible") else
                 ["tab is hidden — trusted clicks would be silently dropped"])
        return {"visible": bool(value.get("visible")),
                "visibilityState": value.get("visibilityState")}, True, notes
    if name == "model_menu":
        if not isinstance(value, dict) or "open" not in value:
            return {"payload": value}, None, ["payload has no `open` field"]
        rows = value.get("rows") or []
        notes = ["menu reports open with zero rows"] if value.get("open") and not rows else []
        return {"open": bool(value.get("open")), "rows": len(rows)}, True, notes
    if name == "chips":
        if not isinstance(value, dict):
            return {"payload": value}, None, ["payload is not an object"]
        attachments = value.get("attachments")
        if not isinstance(attachments, list):
            return {"payload": value}, False, ["attachments is not a list"]
        return {"count": len(attachments), "attachments": attachments}, True, []
    return {"value": value}, None, []


def console_drift(driver: Any = None, *, config: Optional[Config] = None) -> dict:
    """Read-only drift report over the 12 `_JS_*` probes.

    Every read-safe probe is executed exactly once (``mutating=False``) and
    summarised; the action-class probes are NEVER executed (a selfcheck must
    not click, type or inject) — they get a static source check instead: are
    the selectors/labels they were written against still there?

    Strictly read-only: no clicks, no input, no navigation, no state writes.

    Returns a structured dict: ``probes`` (per-probe mode/executed/found and
    key fields), ``missing_found`` (probes whose target was absent),
    ``anomalies`` (anchors that drifted from their expected shape) and
    ``counts``. ``ok`` is False when anything anomalous was found.
    """
    if driver is None:
        state = load_state()
        driver = _make_driver(config or get_config(), state)
    locale = _probe_locale()
    probes: dict = {}
    anomalies: list = []
    missing: list = []
    for name, mode in DRIFT_PROBES:
        entry: dict = {"mode": mode}
        if mode == "action":
            markers = _drift_markers(name, locale)
            absent = [m for m in markers if m not in _drift_source(name)]
            entry.update({"executed": False,
                          "reason": DRIFT_STATIC_REASONS.get(name, "action probe"),
                          "found": _drift_static_found(name, probes),
                          "markers": list(markers),
                          "markers_ok": not absent})
            if absent:
                anomalies.append(f"{name}: probe source lost marker(s) {absent}")
        else:
            try:
                value = _js(driver, _drift_source(name), None, mutating=False)
            except Exception as exc:  # noqa: BLE001 — one dead probe must not abort the report
                entry.update({"executed": False, "found": None,
                              "error": f"{type(exc).__name__}: {exc}"})
                anomalies.append(f"{name}: probe failed ({exc})")
                probes[name] = entry
                continue
            summary, found, notes = _drift_summary(name, value)
            entry.update({"executed": True, "found": found, "summary": summary})
            anomalies.extend(f"{name}: {note}" for note in notes)
        if entry.get("found") is False:
            missing.append(name)
        probes[name] = entry
    counts = {"total": len(DRIFT_PROBES),
              "read": sum(1 for _, m in DRIFT_PROBES if m == "read"),
              "action": sum(1 for _, m in DRIFT_PROBES if m == "action"),
              "executed": sum(1 for e in probes.values() if e.get("executed")),
              "found_false": len(missing),
              "anomalies": len(anomalies)}
    return {"ok": not anomalies, "kind": "drift", "locale": locale,
            "probes": probes, "missing_found": missing, "anomalies": anomalies,
            "fallbacks": _fallback_history(),
            "counts": counts}


def console_selfcheck(*, wait_budget: float = DEFAULT_WAIT,
                      poll_interval: float = POLL_INTERVAL,
                      submit_timeout: float = SUBMIT_TIMEOUT,
                      submit_recheck_timeout: float = 6.0,
                      config: Optional[Config] = None, driver: Any = None,
                      sleep: Callable[[float], None] = time.sleep) -> dict:
    """Run the full gate pipeline against the console with a canned query.

    First run creates the ``selfcheck`` thread; later runs continue it as
    follow-ups, so both the new-thread and continuation paths get exercised
    across invocations. Prints per-gate verdicts for the caller.
    """
    started = time.monotonic()
    try:
        result = console_ask(SELFCHECK_QUERY, task="selfcheck", new_thread=False,
                             wait_budget=wait_budget, poll_interval=poll_interval,
                             submit_timeout=submit_timeout,
                             submit_recheck_timeout=submit_recheck_timeout,
                             config=config, driver=driver, sleep=sleep)
    except ConsoleError as exc:
        return {"ok": False, "gate": exc.gate, "error": exc.message,
                "error_code": exc.code,
                "evidence": exc.evidence, "gates": exc.gates,
                "elapsed_s": round(time.monotonic() - started, 1)}
    return result
