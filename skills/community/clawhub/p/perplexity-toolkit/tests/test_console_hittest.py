"""执行前几何/遮挡二次验证（融合项 d, narrow）.

Before a click/fill fires on cached coordinates or a selector target, the
action point is re-verified against the live DOM (read-only ``_JS_HITTEST``
probe + ``_action_point_ok`` helper):

* (a) healthy target (visible, un-occluded) ⇒ zero behavior change —
  fill/click fire exactly as before and the historical suite stays green;
* (b) target covered by a floating layer (``elementFromPoint`` returns an
  unrelated element) ⇒ ``act.target-occluded`` and the action is NEVER
  fired (spy: no click/fill and no ``driver.cdp`` call);
* (c) target partially/fully outside the viewport ⇒ same code;
* (d) ``elementFromPoint`` returning a CHILD of the target (or the target's
  ancestor) ⇒ allowed (the point still lands in the target's subtree);
* (e) the error detail carries the occluder's sanitized
  tag/role/aria-label/text summary (≤80 chars, no URL query strings, no
  suspected tokens).

The probe's own DOM semantics are pinned as REAL behavior under node (the
FakeDriver only pattern-matches probe source — a canned dict proves nothing
about the matcher), same as the bound-probe harness in
``test_console_fallback``.
"""
import json
import re
import shutil
import subprocess
import sys; sys.path.insert(0, "src")

import pytest

from test_console import ConsoleFakeDriver, NOOP, make_config
from test_console_fallback import (
    FallbackFakeDriver,
    block,
    item,
    LONG_ANSWER,
    TRUNCATED_ANSWER,
)

from perplexity_toolkit import console
from perplexity_toolkit.console import (
    ConsoleError,
    _action_point_ok,
    console_extract,
    console_fill,
    console_submit,
)


@pytest.fixture(autouse=True)
def tmp_console_home(tmp_path, monkeypatch):
    monkeypatch.setenv("PERPLEXITY_CONSOLE_HOME", str(tmp_path))
    return tmp_path


# ──────────────────────────────────────────────────────────────
# canned hit-test probe verdicts
# ──────────────────────────────────────────────────────────────

def _node(tag, role="", label="", text=""):
    return {"tag": tag, "role": role, "label": label, "text": text}


HEALTHY_SELF = {"ok": True, "reason": "", "rel": "self",
                "target": _node("div", text="composer"),
                "hit": _node("div", text="composer")}

# (d) elementFromPoint returned a CHILD of the target: still in the subtree
HEALTHY_CHILD = {"ok": True, "reason": "", "rel": "descendant",
                 "target": _node("button", role="button", label="提交"),
                 "hit": _node("svg", text="")}

OCCLUDED = {"ok": False, "reason": "occluded", "rel": "other",
            "target": _node("div", text="composer"),
            "hit": _node("div", role="dialog", label="遮罩弹窗",
                         text="这是遮挡在上面的浮层内容")}

OFF_VIEWPORT = {"ok": False, "reason": "off-viewport", "rel": "",
                "target": _node("div", text="composer"), "hit": None}

NO_HIT = {"ok": False, "reason": "no-hit", "rel": "",
          "target": _node("div", text="composer"), "hit": None}

DEAD = ""          # probe not operational (bridge returned nothing)


def _hittest_kind(code):
    """Which gate fired the probe, from the injected spec's quoted keys."""
    if '"selectors"' in code:
        return "submit"
    if '"selector"' in code:
        return "fill"
    return "rect"


class HitTestMixin:
    """Dispatch the hit-test probe on its /*PPLX_HITTEST_PROBE*/ marker.

    ``hittest`` maps gate kind (fill/submit/rect) to a payload: a dict is
    the probe verdict, a LIST pops one verdict per call (per-candidate
    scripting), and ``""`` models a dead probe. Anything not configured
    models a dead probe too (historical behavior).
    """

    def _hittest_payload(self, code):
        kind = _hittest_kind(code)
        payload = (self.hittest or {}).get(kind, DEAD)
        if isinstance(payload, list):
            payload = payload.pop(0) if payload else DEAD
        return payload

    def evaluate(self, code, **kwargs):
        if "PPLX_HITTEST_PROBE" in code:
            self.calls.append(("evaluate", code[:60]))
            return self._hittest_payload(code)
        return super().evaluate(code, **kwargs)


class HitFakeDriver(HitTestMixin, ConsoleFakeDriver):
    def __init__(self, *, hittest=None, **kw):
        super().__init__(share_tab=True, **kw)
        self.hittest = hittest


class HitFallbackFake(HitTestMixin, FallbackFakeDriver):
    def __init__(self, *, hittest=None, **kw):
        super().__init__(**kw)
        self.hittest = hittest


class ProbeDriver:
    """Minimal driver: records executed probe source + mutating flag."""

    def __init__(self, payload):
        self.payload = payload
        self.executed = []

    def evaluate(self, code, **kwargs):
        self.executed.append((code, kwargs.get("mutating")))
        return self.payload

    def screenshot(self, path):
        return None


def no_actions(drv, *extra):
    return [c for c in drv.calls
            if c[0] in ("click", "fill", "cdp", "navigate", *extra)]


# ──────────────────────────────────────────────────────────────
# probe source contract
# ──────────────────────────────────────────────────────────────

class TestHitProbeSource:

    def test_probe_is_read_only_and_structured(self):
        src = console._JS_HITTEST
        for forbidden in (".click()", "dispatchEvent", "insertText",
                          "input.files", "atob(", "scrollTop",
                          "window.scrollTo", "localStorage", "pushState"):
            assert forbidden not in src, forbidden
        assert "elementFromPoint" in src and "getBoundingClientRect" in src
        assert "contains" in src
        assert "__SPEC__" in src
        assert "/*PPLX_HITTEST_PROBE*/" in src
        assert "JSON.stringify" in src

    def test_spec_is_ascii_escaped_so_ui_labels_never_reach_the_executed_code(self):
        """The submit selectors carry UI labels (提交/搜索); with
        ensure_ascii injection the executed source never contains them
        verbatim (a label-bearing source can mis-dispatch label-based test
        doubles and drift checks)."""
        spec = {"selectors": list(console._SUBMIT_SELECTORS)}
        code = console._JS_HITTEST.replace(
            "__SPEC__", json.dumps(spec, ensure_ascii=True))
        assert "提交" not in code and "搜索" not in code
        assert "PPLX_HITTEST_PROBE" in code

    def test_probe_runs_mutating_false(self):
        drv = ProbeDriver(HEALTHY_SELF)
        _action_point_ok(drv, selector="[contenteditable]")
        assert len(drv.executed) == 1
        assert drv.executed[0][1] is False      # read-only, retryable


# ──────────────────────────────────────────────────────────────
# helper verdicts
# ──────────────────────────────────────────────────────────────

class TestActionPointOk:

    def test_usable_points_return_none(self):
        assert _action_point_ok(ProbeDriver(HEALTHY_SELF),
                                selector="[contenteditable]") is None
        assert _action_point_ok(ProbeDriver(HEALTHY_CHILD),
                                selectors=list(console._SUBMIT_SELECTORS)) is None
        assert _action_point_ok(ProbeDriver(HEALTHY_SELF),
                                rect={"x": 100, "y": 50, "w": 80, "h": 24}) is None

    def test_dead_probe_and_missing_target_keep_historical_behavior(self):
        # probe not operational → no verdict (rung's own semantics decide)
        assert _action_point_ok(ProbeDriver(DEAD),
                                selector="[contenteditable]") is None
        assert _action_point_ok(ProbeDriver({}), selector="x") is None
        # target simply not there → not an occlusion verdict
        assert _action_point_ok(ProbeDriver({"ok": False, "reason": "not-found"}),
                                selector="x") is None

    def test_blocked_points_carry_reason_and_summary(self):
        out = _action_point_ok(ProbeDriver(OCCLUDED),
                               selector="[contenteditable]")
        assert out["reason"] == "occluded" and out["rel"] == "other"
        assert out["summary"].startswith("dialog/遮罩弹窗")
        out2 = _action_point_ok(ProbeDriver(OFF_VIEWPORT), rect={"x": 1, "y": 2})
        assert out2["reason"] == "off-viewport"
        out3 = _action_point_ok(ProbeDriver(NO_HIT), rect={"x": 1, "y": 2})
        assert out3["reason"] == "no-hit"

    def test_empty_spec_fails_closed(self):
        assert _action_point_ok(ProbeDriver(HEALTHY_SELF)) == {
            "reason": "no-spec", "rel": "", "summary": ""}


# ──────────────────────────────────────────────────────────────
# (a)/(b)/(c)/(d): fill path (composer click+fill)
# ──────────────────────────────────────────────────────────────

class TestFillGate:

    def test_healthy_fill_is_unchanged(self):
        """(a) visible + un-occluded ⇒ click+fill fire exactly as before."""
        drv = HitFakeDriver(hittest={"fill": HEALTHY_SELF})
        res = console_fill("健康问题", config=make_config(), driver=drv,
                           sleep=NOOP, judge=False)
        assert res["ok"] is True
        assert drv.composer == "健康问题"
        assert ("click", "[contenteditable]") in drv.calls
        assert any(c[0] == "fill" for c in drv.calls)

    def test_child_hit_allows_the_fill(self):
        """(d) the centre hit landing on a CHILD of the target is usable."""
        drv = HitFakeDriver(hittest={"fill": HEALTHY_CHILD})
        res = console_fill("子元素命中", config=make_config(), driver=drv,
                           sleep=NOOP, judge=False)
        assert res["ok"] is True and drv.composer == "子元素命中"

    def test_occluded_composer_raises_and_fires_nothing(self):
        """(b) floating layer over the composer ⇒ act.target-occluded and
        NEITHER the click NOR the fill fires (fail-closed, 绝不盲点)."""
        drv = HitFakeDriver(hittest={"fill": OCCLUDED})
        with pytest.raises(ConsoleError) as exc:
            console_fill("被挡住的问题", config=make_config(), driver=drv,
                         sleep=NOOP, judge=False)
        assert exc.value.code == "act.target-occluded"
        assert exc.value.gate == "fill"
        assert exc.value.gates["fill"]["target"]["reason"] == "occluded"
        assert no_actions(drv) == []        # no click / fill / cdp / navigate
        assert drv.composer == ""

    def test_off_viewport_target_raises_the_same_code(self):
        """(c) partially/fully out of the viewport ⇒ same fail-closed code."""
        for payload in (OFF_VIEWPORT, NO_HIT):
            drv = HitFakeDriver(hittest={"fill": payload})
            with pytest.raises(ConsoleError) as exc:
                console_fill("视口外", config=make_config(), driver=drv,
                             sleep=NOOP, judge=False)
            assert exc.value.code == "act.target-occluded"
            assert no_actions(drv) == []

    def test_occlusion_skips_the_desync_reload_self_heal(self):
        """act.target-occluded must surface as-is — the fill.not-committed
        reload self-heal never runs on an occlusion verdict."""
        drv = HitFakeDriver(hittest={"fill": OCCLUDED})
        with pytest.raises(ConsoleError) as exc:
            console_fill("直接失败", config=make_config(), driver=drv,
                         sleep=NOOP, judge=False)
        assert exc.value.code == "act.target-occluded"
        assert not [c for c in drv.calls if c[0] == "navigate"]


# ──────────────────────────────────────────────────────────────
# (a)/(b)/(c): submit path (submit-button click)
# ──────────────────────────────────────────────────────────────

class TestSubmitGate:

    def test_healthy_submit_clicks_as_before(self):
        """(a) visible + un-occluded ⇒ the submit click fires unchanged."""
        drv = HitFakeDriver(hittest={"fill": HEALTHY_SELF, "submit": HEALTHY_SELF})
        console_fill("提交问题", config=make_config(), driver=drv,
                     sleep=NOOP, judge=False)
        res = console_submit(config=make_config(), driver=drv, sleep=NOOP)
        assert res["ok"] is True
        assert drv.bubbles and drv.bubbles[-1].startswith("提交问题")
        assert drv._submit_clicks >= 1

    def test_occluded_submit_never_fires_the_click(self):
        """(b) covered submit button ⇒ act.target-occluded, the JS submit
        probe never runs (no turn is ever sent)."""
        drv = HitFakeDriver(hittest={"fill": HEALTHY_SELF, "submit": OCCLUDED})
        console_fill("不会发出的问题", config=make_config(), driver=drv,
                     sleep=NOOP, judge=False)
        with pytest.raises(ConsoleError) as exc:
            console_submit(config=make_config(), driver=drv, sleep=NOOP)
        assert exc.value.code == "act.target-occluded"
        assert exc.value.gate == "submit"
        assert drv.bubbles == []            # nothing was submitted
        assert drv._submit_clicks == 0      # _JS_CLICK_SUBMIT never fired
        assert not [c for c in drv.calls if c[0] == "cdp"]

    def test_off_viewport_submit_raises_the_same_code(self):
        """(c) submit control out of the viewport ⇒ same code, no click."""
        drv = HitFakeDriver(hittest={"fill": HEALTHY_SELF, "submit": OFF_VIEWPORT})
        console_fill("视口外提交", config=make_config(), driver=drv,
                     sleep=NOOP, judge=False)
        with pytest.raises(ConsoleError) as exc:
            console_submit(config=make_config(), driver=drv, sleep=NOOP)
        assert exc.value.code == "act.target-occluded"
        assert drv.bubbles == [] and drv._submit_clicks == 0

    def test_child_hit_on_the_submit_button_is_allowed(self):
        """(d) the centre hit landing on the button's icon (a child) passes."""
        drv = HitFakeDriver(hittest={"fill": HEALTHY_SELF,
                                     "submit": HEALTHY_CHILD})
        console_fill("图标命中", config=make_config(), driver=drv,
                     sleep=NOOP, judge=False)
        res = console_submit(config=make_config(), driver=drv, sleep=NOOP)
        assert res["ok"] is True and drv.bubbles


# ──────────────────────────────────────────────────────────────
# expand fallback rung: cached-coordinate click re-verification
# ──────────────────────────────────────────────────────────────

class TestExpandRungGate:

    def test_healthy_candidate_clicks_exactly_as_before(self):
        """(a) un-occluded cached point ⇒ the trusted CDP click fires at the
        same rect centre as the historical rung."""
        drv = HitFallbackFake(
            table=[item(0, "展开全文", x=100, y=50, w=80, h=24)],
            blocks=[block(0, TRUNCATED_ANSWER)], grow_on_click=True,
            hittest={"rect": HEALTHY_SELF})
        drv.prose = ["答案 42。"]
        res = console_extract(config=make_config(), driver=drv, sleep=NOOP)
        assert res["ok"] is True
        assert res["fallback_used"] == "expand-table"
        assert drv.cdp_clicks == [(140, 62)]     # rect centre, trusted CDP

    def test_occluded_candidate_is_not_clicked(self):
        """(b) covered candidate ⇒ no click at all (driver.cdp never called)
        and the rung exhausts with its existing fail-closed semantics."""
        drv = HitFallbackFake(
            table=[item(0, "展开全文", x=100, y=50, w=80, h=24)],
            blocks=[block(0, TRUNCATED_ANSWER)], grow_on_click=True,
            hittest={"rect": OCCLUDED})
        drv.prose = ["答案 42。"]
        with pytest.raises(ConsoleError) as exc:
            console._extract_step(drv, console.load_state(), make_config(),
                                  sleep=NOOP)
        assert exc.value.code == "probe.fallback-exhausted"
        assert drv.cdp_clicks == []
        assert not [c for c in drv.calls if c[0] == "cdp"]   # spy: no cdp call
        attempts = exc.value.gates["expand_fallback"]["attempts"]
        assert attempts[-1]["hit_ok"] is False
        assert attempts[-1]["why"] == "occluded"

    def test_off_viewport_candidate_is_not_clicked(self):
        """(c) cached point out of the viewport ⇒ same skip-and-exhaust."""
        drv = HitFallbackFake(
            table=[item(0, "展开全文", x=100, y=50, w=80, h=24)],
            blocks=[block(0, TRUNCATED_ANSWER)], grow_on_click=True,
            hittest={"rect": OFF_VIEWPORT})
        drv.prose = ["答案 42。"]
        with pytest.raises(ConsoleError) as exc:
            console._extract_step(drv, console.load_state(), make_config(),
                                  sleep=NOOP)
        assert exc.value.code == "probe.fallback-exhausted"
        assert drv.cdp_clicks == []

    def test_occluded_candidate_skips_to_the_next_one(self):
        """记 attempt 失败换下一候选: the occluded candidate is recorded as a
        failed attempt and the NEXT candidate is verified and clicked."""
        drv = HitFallbackFake(
            table=[item(0, "展开全文", x=100, y=50, w=80, h=24),
                   item(1, "展开一下吧", x=100, y=150, w=80, h=24)],
            blocks=[block(0, TRUNCATED_ANSWER)], grow_on_click=True,
            hittest={"rect": [OCCLUDED, HEALTHY_SELF]})
        drv.prose = ["答案 42。"]
        res = console_extract(config=make_config(), driver=drv, sleep=NOOP)
        assert res["ok"] is True and res["fallback_used"] == "expand-table"
        assert drv.cdp_clicks == [(140, 162)]    # ONLY the second candidate
        gate = res["gates"]["expand_fallback"]
        assert gate["attempts"][0]["i"] == 0 and gate["attempts"][0]["hit_ok"] is False
        assert gate["attempts"][1]["i"] == 1 and gate["attempts"][1]["grew"] is True


# ──────────────────────────────────────────────────────────────
# (e) detail sanitization
# ──────────────────────────────────────────────────────────────

DIRTY_OCCLUDED = {
    "ok": False, "reason": "occluded", "rel": "other",
    "target": _node("div", text="composer"),
    "hit": _node("div", role="dialog",
                 label="推广浮层 https://spam.example.com/x?token=FAKEtestTokEn00001&u=1",
                 text="内部密钥 FAKEhash0000000000ab 与 FAKEupper1234567890ab 结尾"),
}


class TestOccluderSummarySanitized:

    def test_detail_summary_strips_url_query_and_tokens(self):
        drv = HitFakeDriver(hittest={"fill": DIRTY_OCCLUDED})
        with pytest.raises(ConsoleError) as exc:
            console_fill("脱敏检查", config=make_config(), driver=drv,
                         sleep=NOOP, judge=False)
        assert exc.value.code == "act.target-occluded"
        summary = exc.value.gates["fill"]["target"]["summary"]
        assert len(summary) <= 80
        blob = json.dumps({"m": exc.value.message, "g": exc.value.gates},
                          ensure_ascii=False)
        # no URL query strings, no suspected tokens — anywhere in the detail
        assert "?" not in summary
        for leak in ("token=FAKEtest", "FAKEtestTokEn00001", "FAKEhash0000000000ab",
                     "FAKEupper1234567890ab", "?u=1"):
            assert leak not in blob, leak
        assert re.search(r"https://spam\.example\.com/x", summary)
        assert "[token]" in summary


# ──────────────────────────────────────────────────────────────
# the REAL probe JS as DOM behavior — executed in node over a stub DOM
# ──────────────────────────────────────────────────────────────

NODE = shutil.which("node")

_HIT_DOM_PRE = (
    "function mk(spec) {\n"
    "  const el = {name: spec.name || '', tagName: String(spec.tag).toUpperCase(),\n"
    "    innerText: spec.t || '', textContent: spec.t || '',\n"
    "    parentElement: null, attrs: spec.attrs || {}, kids: [], rect: spec.rect || null};\n"
    "  el.getAttribute = (n) => (n in el.attrs ? el.attrs[n] : null);\n"
    "  el.getBoundingClientRect = () => ({x: el.rect.x, y: el.rect.y,\n"
    "    width: el.rect.w, height: el.rect.h});\n"
    "  el.contains = (n) => { for (let p = n; p; p = p.parentElement) if (p === el) return true; return false; };\n"
    "  for (const k of (spec.kids || [])) { const c = mk(k); c.parentElement = el; el.kids.push(c); }\n"
    "  return el;\n"
    "}\n"
    "function flat(el, acc) { acc.push(el); for (const c of el.kids) flat(c, acc); return acc; }\n"
    "const ALL = flat(mk("
)
_HIT_DOM_MID = (
    "), []);\n"
    "const CFG = __CFG__;\n"
    "const byName = (n) => (n === null ? null : (ALL.find((e) => e.name === n) || null));\n"
    "globalThis.window = {innerWidth: CFG.vw, innerHeight: CFG.vh};\n"
    "globalThis.document = {\n"
    "  querySelector: (sel) => (CFG.select[sel] === undefined ? null : byName(CFG.select[sel])),\n"
    "  querySelectorAll: (sel) => (sel === '*' ? ALL : []),\n"
    "  elementFromPoint: (x, y) => {\n"
    "    const k = x + ',' + y;\n"
    "    return (CFG.hit[k] === undefined ? null : byName(CFG.hit[k]));\n"
    "  },\n"
    "};\n"
    "process.stdout.write(String("
)
_HIT_DOM_POST = "));\n"


def _hit_probe_run(spec, tree, cfg):
    """Run the REAL hit-test probe in node over a stub DOM ``tree``.

    ``tree``: nested {"tag", "name", "t", "attrs", "rect", "kids"} dicts.
    ``cfg``: {"vw", "vh", "select": {css: name}, "hit": {"x,y": name}}.
    """
    assert NODE is not None
    src = console._JS_HITTEST.replace(
        "__SPEC__", json.dumps(spec, ensure_ascii=True))
    harness = (_HIT_DOM_PRE + json.dumps(tree, ensure_ascii=False)
               + _HIT_DOM_MID.replace("__CFG__", json.dumps(cfg, ensure_ascii=False))
               + src + _HIT_DOM_POST)
    proc = subprocess.run([NODE, "-e", harness], capture_output=True, text=True)
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout)


def _tree(*, composer_rect, inner=None, overlay=None):
    """body > [composer [inner]], overlay — the canonical occlusion shape."""
    kids = []
    if inner:
        kids.append({"tag": "span", "name": "inner", "t": "",
                     "rect": inner["rect"]})
    body_kids = [{"tag": "div", "name": "composer", "t": "输入问题",
                  "attrs": {"aria-label": "输入框"}, "rect": composer_rect,
                  "kids": kids}]
    if overlay:
        body_kids.append({"tag": "div", "name": "overlay", "t": "弹窗内容",
                          "attrs": {"role": "dialog", "aria-label": "遮罩"},
                          "rect": overlay["rect"]})
    return {"tag": "body", "name": "body", "t": "", "kids": body_kids}


@pytest.mark.skipif(NODE is None, reason="node is required to execute probe JS")
class TestHitProbeRealJS:
    """(a)-(d) as REAL DOM behavior of the probe."""

    VW, VH = 1280, 800

    def _cfg(self, hit, select=None):
        return {"vw": self.VW, "vh": self.VH,
                "select": select or {}, "hit": hit}

    def test_selector_hit_on_target_itself_is_ok(self):
        """(a) healthy: elementFromPoint returns the target itself."""
        out = _hit_probe_run(
            {"selector": "[contenteditable]"},
            _tree(composer_rect={"x": 100, "y": 600, "w": 600, "h": 80}),
            self._cfg({"400,640": "composer"},
                      select={"[contenteditable]": "composer"}))
        assert out["ok"] is True and out["rel"] == "self"

    def test_hit_on_a_child_of_the_target_is_ok(self):
        """(d) the target's CENTRE lands on its own subtree element."""
        out = _hit_probe_run(
            {"selector": "[contenteditable]"},
            _tree(composer_rect={"x": 100, "y": 600, "w": 600, "h": 80},
                  inner={"rect": {"x": 350, "y": 620, "w": 100, "h": 40}}),
            self._cfg({"400,640": "inner"},
                      select={"[contenteditable]": "composer"}))
        assert out["ok"] is True and out["rel"] == "descendant"

    def test_hit_on_an_ancestor_of_the_target_is_ok(self):
        """spec: 命中目标的祖先（点在容器上）也算可用."""
        out = _hit_probe_run(
            {"rect": {"x": 200, "y": 100, "w": 80, "h": 24}},
            {"tag": "body", "name": "body", "t": "", "kids": [
                {"tag": "div", "name": "wrap", "t": "",
                 "rect": {"x": 180, "y": 80, "w": 120, "h": 64}, "kids": [
                     {"tag": "button", "name": "btn", "t": "展开全文",
                      "rect": {"x": 200, "y": 100, "w": 80, "h": 24}}]}]},
            self._cfg({"240,112": "wrap"}))
        assert out["ok"] is True and out["rel"] == "ancestor"

    def test_overlay_covering_the_target_is_occluded(self):
        """(b) elementFromPoint returns the floating layer ⇒ unusable."""
        out = _hit_probe_run(
            {"selector": "[contenteditable]"},
            _tree(composer_rect={"x": 100, "y": 600, "w": 600, "h": 80},
                  overlay={"rect": {"x": 0, "y": 0, "w": 1280, "h": 800}}),
            self._cfg({"400,640": "overlay"},
                      select={"[contenteditable]": "composer"}))
        assert out["ok"] is False and out["reason"] == "occluded"
        assert out["rel"] == "other"
        assert out["hit"]["tag"] == "div" and out["hit"]["role"] == "dialog"

    def test_target_fully_outside_the_viewport_is_unusable(self):
        """(c) completely out of the viewport ⇒ off-viewport."""
        out = _hit_probe_run(
            {"rect": {"x": 100, "y": 900, "w": 80, "h": 24}},
            _tree(composer_rect={"x": 100, "y": 900, "w": 80, "h": 24}),
            self._cfg({}))
        assert out["ok"] is False and out["reason"] == "off-viewport"

    def test_target_partially_outside_with_centre_off_screen_is_unusable(self):
        """(c) partially out of the viewport — the actuated centre has left
        the screen ⇒ same verdict (nothing valid to click there)."""
        out = _hit_probe_run(
            {"rect": {"x": 100, "y": 740, "w": 600, "h": 120}},
            _tree(composer_rect={"x": 100, "y": 740, "w": 600, "h": 120}),
            self._cfg({}))
        assert out["ok"] is False and out["reason"] == "off-viewport"

    def test_degenerate_rect_is_unusable(self):
        out = _hit_probe_run(
            {"rect": {"x": 100, "y": 100, "w": 0, "h": 24}},
            _tree(composer_rect={"x": 100, "y": 100, "w": 0, "h": 24}),
            self._cfg({"100,112": "composer"}))
        assert out["ok"] is False and out["reason"] == "degenerate"

    def test_rect_mode_point_outside_the_candidate_subtree_is_occluded(self):
        """expand-rung contract: the cached point must still land inside the
        ORIGINAL candidate's subtree — a layer now covering it (and no
        rect-matching element anywhere near the hit) ⇒ unusable."""
        out = _hit_probe_run(
            {"rect": {"x": 200, "y": 100, "w": 80, "h": 24}},
            {"tag": "body", "name": "body", "t": "", "kids": [
                {"tag": "button", "name": "btn", "t": "展开全文",
                 "rect": {"x": 500, "y": 400, "w": 80, "h": 24}},
                {"tag": "div", "name": "overlay", "t": "弹窗",
                 "attrs": {"role": "dialog"},
                 "rect": {"x": 180, "y": 80, "w": 200, "h": 100}}]},
            self._cfg({"240,112": "overlay"}))
        assert out["ok"] is False and out["reason"] == "occluded"

    def test_rect_mode_hit_inside_candidate_subtree_is_ok(self):
        """rect mode, hit on a CHILD of the rect-matched candidate ⇒ ok."""
        out = _hit_probe_run(
            {"rect": {"x": 200, "y": 100, "w": 80, "h": 24}},
            {"tag": "body", "name": "body", "t": "", "kids": [
                {"tag": "button", "name": "btn", "t": "展开全文",
                 "rect": {"x": 200, "y": 100, "w": 80, "h": 24}, "kids": [
                     {"tag": "svg", "name": "icon", "t": "",
                      "rect": {"x": 230, "y": 100, "w": 40, "h": 24}}]}]},
            self._cfg({"240,112": "icon"}))
        assert out["ok"] is True and out["rel"] == "descendant"

    def test_selector_not_found_reports_not_found(self):
        out = _hit_probe_run(
            {"selector": "[contenteditable]"},
            _tree(composer_rect={"x": 100, "y": 600, "w": 600, "h": 80}),
            self._cfg({}, select={}))
        assert out["ok"] is False and out["reason"] == "not-found"
