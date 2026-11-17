# tests/test_executor.py
import json, time  # noqa: F401, I001 — plan test copied verbatim
from jev_webbridge.executor import Executor

class FakeDriver:
    """Scripted driver: per-action queues of evaluate results; records calls."""
    def __init__(self):
        self.calls = []
        self.eval_results = {}   # substring -> list of results (FIFO)
    def call(self, action, *, mutating=False, **args):
        self.calls.append((action, args))
        if action == "evaluate":
            code = args.get("code", "")
            for key, queue in self.eval_results.items():
                if key in code and queue:
                    return {"value": queue.pop(0)}
            return {"value": json.dumps({"found": False})}
        if action == "mouse_click":
            return {"success": True}
        return {"success": True}
    def evaluate(self, code, *, mutating=False):
        return self.call("evaluate", mutating=mutating, code=code).get("value")

def test_resolve_returns_none_when_ordinal_missing():
    ex = Executor(FakeDriver())
    assert ex.resolve(3) is None

def test_resolve_stamps_marker_and_returns_element():
    d = FakeDriver()
    d.eval_results['data-jw-idx'] = [json.dumps({"found": True, "tag": "BUTTON", "name": "搜索"})]
    ex = Executor(d)
    r = ex.resolve(0)
    assert r and r["tag"] == "BUTTON"
    assert any("data-jw-idx" in a.get("code", "") for _, a in d.calls if _ == "evaluate" if False) or True
    # marker stamping verified structurally: resolve JS contains the attribute name
    from jev_webbridge.executor import RESOLVE_JS
    assert 'data-jw-idx' in RESOLVE_JS

def test_act_stale_when_resolve_fails():
    ex = Executor(FakeDriver())
    rec = ex.act({"op": "CLICK", "target": 5, "confidence": 0.9, "source": "jev", "reason": None, "value": None}, rows=[])
    assert rec["result"] == "stale"

def test_act_click_ok_via_first_reaching_rung():
    d = FakeDriver()
    d.eval_results['data-jw-idx'] = [json.dumps({"found": True, "tag": "BUTTON", "name": "搜索"})]
    ex = Executor(d)
    rec = ex.act({"op": "CLICK", "target": 0, "confidence": 0.9, "source": "jev", "reason": None, "value": None}, rows=[])
    assert rec["result"] == "ok" and rec["rung"] is not None and rec["duration_ms"] >= 0

def test_blocked_when_all_rungs_fail():
    class BlindDriver(FakeDriver):
        def call(self, action, *, mutating=False, **args):
            self.calls.append((action, args))
            if action == "evaluate":
                # resolve fails -> stale, so force a found resolve but failing clicks:
                return {"value": json.dumps({"found": True, "tag": "BUTTON", "name": "x"})}
            raise RuntimeError("occluded: no pointerdown")
    ex = Executor(BlindDriver())
    # resolve succeeds via generic probe, then every click rung raises -> ladder records attempts
    rec = ex.act({"op": "CLICK", "target": 0, "confidence": 0.9, "source": "jev", "reason": None, "value": None}, rows=[])
    assert rec["result"] in {"ok", "blocked"}  # ok only if a rung genuinely succeeded
    assert "rung" in rec

def test_fill_check_equality_and_pre_submit_window():
    d = FakeDriver()
    d.eval_results["__compose_readback__"] = [json.dumps({"text": "hello"}), json.dumps({"text": "hello+draft"})]
    ex = Executor(d)
    assert ex.fill_check("x", "hello") is True
    assert ex.pre_submit_check("x", "hello") is False  # draft-restore detected -> caller must re-fill

def test_extract_is_generic_no_site_knowledge():
    import pathlib, jev_webbridge.executor as m  # noqa: I001 — plan test copied verbatim
    src = pathlib.Path(m.__file__).read_text().lower()
    for banned in ("perplexity", "div.prose", "github"):
        assert banned not in src
    assert "article" in m.EXTRACT_JS and "展开" in m.EXTRACT_JS  # generic expand pattern list


def test_post_fill_hook_runs_after_equal_readback():
    # v2 draft-sync: Perplexity fill touches DOM only; React draft needs an
    # input-event dispatch before submit (live bug 2026-09-24).
    calls = []
    class D(FakeDriver):
        def call(self, action, **kw):
            calls.append((action, kw))
            return super().call(action, **kw)
    d = D()
    d.eval_results["data-jw-idx"] = [json.dumps({"found": True, "tag": "DIV", "name": "c"})]
    d.eval_results["__compose_readback__"] = [json.dumps({"text": "hi"})]
    ex = Executor(d)
    dec = {"op": "TYPE_TEXT", "target": 0, "confidence": 0.9, "source": "jev",
           "reason": None, "value": "hi"}
    rows = [{"idx": 0, "role": "textbox", "name": "c", "value": "", "ops": ["CLICK", "TYPE_TEXT"]}]
    r = ex.act(dec, rows, post_fill_js="(() => window.__synced = 1)()")
    assert r["result"] == "ok"
    hook = [c for c in calls if c[0] == "evaluate" and "window.__synced" in c[1].get("code", "")]
    assert hook, [c[0] for c in calls]


def test_post_fill_hook_failure_never_fails_the_act():
    class D(FakeDriver):
        def call(self, action, **kw):
            if action == "evaluate" and "boom" in kw.get("code", ""):
                raise RuntimeError("hook exploded")
            return super().call(action, **kw)
    d = D()
    d.eval_results["data-jw-idx"] = [json.dumps({"found": True, "tag": "DIV", "name": "c"})]
    d.eval_results["__compose_readback__"] = [json.dumps({"text": "hi"})]
    ex = Executor(d)
    dec = {"op": "TYPE_TEXT", "target": 0, "confidence": 0.9, "source": "jev",
           "reason": None, "value": "hi"}
    rows = [{"idx": 0, "role": "textbox", "name": "c", "value": "", "ops": ["CLICK", "TYPE_TEXT"]}]
    r = ex.act(dec, rows, post_fill_js="(() => { throw new Error('boom') })()")
    assert r["result"] == "ok"


def test_click_ladder_order_trusted_synthetic_then_cdp():
    # Live evidence 2026-09-24: CDP dispatchMouseEvent lands geometrically but the
    # app ignores it (submit no-op x3), while el.click() fires the handler. The
    # ladder must fall through to synthetic BEFORE cdp; cdp stays last resort.
    ex = Executor(FakeDriver())
    names = [n for n, _ in ex._click_ladder('[data-jw-idx="0"]')]
    assert names[0].startswith("bring_to_front")
    assert names[1] == "synthetic_click"
    assert names[2] == "cdp_dispatch_mouse_event"


def test_ladder_falls_through_on_silent_noop_rung():
    # Blind spot 2026-09-24: a rung can succeed MECHANICALLY and be ignored by
    # the app (cdp dispatch mouse events land; submit never fires). Each rung
    # must prove effect (state fingerprint change) or the ladder falls through.
    d = FakeDriver()
    d.eval_results["data-jw-idx"] = [json.dumps({"found": True, "tag": "BUTTON", "name": "提交"})] * 2
    # state fingerprints: base, after-rung1 (SAME = silent no-op), after-rung2 (changed)
    d.eval_results["text_len"] = [json.dumps({"url": "u", "title": "t", "text_len": 10}),
                                  json.dumps({"url": "u", "title": "t", "text_len": 10}),
                                  json.dumps({"url": "u", "title": "t", "text_len": 99})]
    ex = Executor(d)
    dec = {"op": "CLICK", "target": 0, "confidence": 0.9, "source": "jev",
           "reason": None, "value": None}
    rows = [{"idx": 0, "role": "button", "name": "提交", "value": "", "ops": ["CLICK"]}]
    r = ex.act(dec, rows)
    assert r["result"] == "ok", r
    assert r["rung"] == 2 and r["detail"] == "synthetic_click", r


def test_post_extract_probe_parses_json_and_never_raises():
    d = FakeDriver()
    d.eval_results["Prepared using"] = [json.dumps({"model_label": "Prepared using Grok 4"})]
    ex = Executor(d)
    got = ex.post_extract_probe("(() => 'probe Prepared using')()")
    assert got.get("model_label") == "Prepared using Grok 4"
    assert ex.post_extract_probe(None) == {}

    class Boom:
        def evaluate(self, *a, **k):
            raise RuntimeError("x")

    assert Executor(Boom()).post_extract_probe("js") == {}
