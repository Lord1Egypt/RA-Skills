# tests/test_loop.py
import json, pathlib  # noqa: I001 — plan test copied verbatim
from jev_webbridge import loop
from tests.test_executor import FakeDriver  # reuse scripted driver

class OkPolicy:
    def __init__(self, decisions): self.q = list(decisions)
    def decide(self, rows, goal, state_sig): return self.q.pop(0) if self.q else WAIT_D

WAIT_D = {"op": "WAIT", "target": None, "confidence": 0.9, "source": "jev", "reason": None, "value": None}
DONE_D = {"op": "DONE", "target": None, "confidence": 0.9, "source": "jev", "reason": None, "value": None}
CLICK_D = {"op": "CLICK", "target": 0, "confidence": 0.9, "source": "jev", "reason": None, "value": None}

def mk_driver():
    d = FakeDriver()
    d.eval_results["table"] = [json.dumps({"table": {"rows": [{"idx":0,"role":"button","name":"搜索","value":None,"ops":["CLICK"]}]},
                                           "state": {"url":"u","title":"t","text_len":10}})]
    return d

def test_receipt_written_before_act(tmp_path):
    order = []
    d = mk_driver()
    orig_call = d.call
    def spy(action, **kw):
        order.append(action); return orig_call(action, **kw)
    d.call = spy
    rp = tmp_path / "runs.jsonl"
    loop.run(d, goal="g search keywords", site="unit", client=OkPolicy([WAIT_D]*2 + [DONE_D]),
             escalate_fn=lambda p: (_ for _ in ()).throw(AssertionError("no escalation expected")),
             receipt_path=str(rp), answer_probe="g search keywords found", max_cycles=5)
    lines = [json.loads(x) for x in rp.read_text().splitlines()]
    assert lines and all("ts" in r and "cycle" in r for r in lines)
    assert lines[0]["cycle"] == 0

def test_done_without_answer_escalates_once(tmp_path):
    rp = tmp_path / "runs.jsonl"
    d = mk_driver()
    escal = []
    def esc(p):
        escal.append(p); return dict(DONE_D, source="escalation", reason=p.get("reason"))
    res = loop.run(d, goal="keywords here", site="unit",
                   client=OkPolicy([DONE_D, DONE_D, DONE_D]), escalate_fn=esc,
                   receipt_path=str(rp), answer_probe="", max_cycles=6)
    assert escal, "DONE must be independently verified and escalate when answer missing"
    assert res["turns"]["escalations"] >= 1

def test_low_confidence_triggers_escalation_payload_shape(tmp_path):
    rp = tmp_path / "runs.jsonl"
    low = dict(CLICK_D, confidence=0.15)  # below post-sweep default TAU=0.20
    got = []
    def esc(p):
        got.append(p); return dict(CLICK_D, source="escalation", reason="low_confidence")
    d = mk_driver()
    loop.run(d, goal="x", site="unit", client=OkPolicy([low, DONE_D, DONE_D]),
             escalate_fn=esc, receipt_path=str(rp), answer_probe="x present", max_cycles=6)
    p = got[0]
    assert set(p) >= {"reason", "rows", "state_sig", "goal", "history"}
    assert p["reason"] == "low_confidence"

def test_cycle_cap_exhausts(tmp_path):
    rp = tmp_path / "runs.jsonl"
    d = mk_driver()
    res = loop.run(d, goal="g", site="unit", client=OkPolicy([WAIT_D]*50),
                   escalate_fn=lambda p: WAIT_D, receipt_path=str(rp),
                   answer_probe="anything", max_cycles=3)
    assert res["status"] == "exhausted" and res["cycles"] == 3

def test_stuck_same_state_escalates(tmp_path):
    rp = tmp_path / "runs.jsonl"; got = []
    d = mk_driver()
    # every observe returns the SAME state_sig and policy keeps returning WAIT
    res = loop.run(d, goal="g", site="unit", client=OkPolicy([WAIT_D]*10),  # noqa: F841 — plan test copied verbatim
                   escalate_fn=lambda p: (got.append(p), dict(WAIT_D, source="escalation"))[1],
                   receipt_path=str(rp), answer_probe="g", max_cycles=6, stuck_escalates=True)
    assert got, "identical consecutive state signatures must escalate"


def test_type_text_uses_goal_as_value_when_policy_gives_none(tmp_path):
    # E2E gap 2026-09-24: policy returns value=None for TYPE_TEXT and nothing
    # ever set it -> fill would send an empty string. Spec G3: caller-supplied
    # text first (run(text=...)), else the goal itself.
    rp = tmp_path / "runs.jsonl"
    d = mk_driver()
    d.eval_results["data-jw-idx"] = [json.dumps({"found": True, "tag": "DIV", "name": "textbox"})]
    d.eval_results["__compose_readback__"] = [json.dumps({"text": "GOAL TEXT"})]
    # settle probe: grown + long-quiet so the mutating settle-wait returns fast
    d.eval_results["quiet_ms"] = [json.dumps({"text_len": 999, "quiet_ms": 99999, "extra": {}})] * 6
    d.eval_results["table"] = [json.dumps({"table": {"rows": [
        {"idx": 0, "role": "link", "name": "L", "value": None, "ops": ["CLICK"]},
        {"idx": 1, "role": "textbox", "name": "TB", "value": None, "ops": ["CLICK", "TYPE_TEXT"]}]},
        "state": {"url": "u", "title": "t", "text_len": 10}})]
    type_text = {"op": "TYPE_TEXT", "target": 1, "confidence": 0.9, "source": "jev",
                 "reason": None, "value": None}
    res = loop.run(d, goal="GOAL TEXT", site="unit", client=OkPolicy([type_text]),
                   escalate_fn=lambda p: (_ for _ in ()).throw(AssertionError("no escalation")),
                   receipt_path=str(rp), max_cycles=1)
    fills = [a for actn, a in d.calls if actn == "fill"]
    assert fills and fills[0].get("value") == "GOAL TEXT", fills
    assert res["status"] in {"exhausted", "done"}
    # settle must respect cap_ms=2000 (+overhead) -- the 100s hang regression
    assert res["wall_ms"] < 5000, res["wall_ms"]


def test_receipts_stay_one_parseable_line_per_decision_across_updates(tmp_path):
    # Live corruption 2026-09-24: pre-act used self._fh.tell() (stale append
    # handle) while complete() rewrote via a SECOND handle -> second seek landed
    # mid-line -> file contained "}{..." and "{{..." garbage.
    rp = tmp_path / "r.jsonl"
    sink = loop.Receipts(str(rp))
    r1 = dict(loop._record(0, dict(CLICK_D), "sig1", escalated=False))
    off1 = sink.write_pre_act(r1)
    u1 = dict(r1, result="error", rung=2, duration_ms=2762, detail="fill readback MISMATCH")
    sink.complete(off1, u1)
    r2 = dict(loop._record(1, dict(CLICK_D), "sig2", escalated=False))
    off2 = sink.write_pre_act(r2)
    sink.complete(off2, dict(r2, result="ok", rung=1, duration_ms=12, detail="bring_to_front"))
    sink.close()
    lines = [json.loads(x) for x in rp.read_text().splitlines()]
    assert len(lines) == 2, rp.read_text()
    assert lines[0]["detail"] == "fill readback MISMATCH" and lines[0]["result"] == "error"
    assert lines[1]["result"] == "ok" and lines[1]["detail"] == "bring_to_front"


def test_executor_detail_is_recorded(tmp_path):
    # detail used to be dropped by record.update (only result/rung/duration_ms).
    rp = tmp_path / "runs.jsonl"
    d = mk_driver()
    d.eval_results["data-jw-idx"] = [json.dumps({"found": True, "tag": "DIV", "name": "x"})]
    d.eval_results["__compose_readback__"] = [json.dumps({"text": "WRONG"})]  # forces MISMATCH
    d.eval_results["quiet_ms"] = [json.dumps({"text_len": 999, "quiet_ms": 99999, "extra": {}})] * 6
    d.eval_results["table"] = [json.dumps({"table": {"rows": [
        {"idx": 0, "role": "link", "name": "L", "value": None, "ops": ["CLICK"]},
        {"idx": 1, "role": "textbox", "name": "TB", "value": None, "ops": ["CLICK", "TYPE_TEXT"]}]},
        "state": {"url": "u", "title": "t", "text_len": 10}})]
    type_text = {"op": "TYPE_TEXT", "target": 1, "confidence": 0.9, "source": "jev",
                 "reason": None, "value": "hello"}
    loop.run(d, goal="g", site="unit", client=OkPolicy([type_text]),
             escalate_fn=lambda p: (_ for _ in ()).throw(AssertionError("no escalation")),
             receipt_path=str(rp), max_cycles=1)
    lines = [json.loads(x) for x in rp.read_text().splitlines()]
    assert lines and "detail" in lines[0], lines[0].keys()
    assert "MISMATCH" in (lines[0]["detail"] or ""), lines[0]


def test_pre_gate_decision_is_recorded_on_escalation(tmp_path):
    # v2: when the structural gate fires, the Jev decision that FAILED must be
    # kept in the receipt (live debugging previously required payload archaeology).
    rp = tmp_path / "runs.jsonl"
    d = mk_driver()
    d.eval_results["table"] = [json.dumps({"table": {"rows": [
        {"idx": 0, "role": "link", "name": "L", "value": None, "ops": ["CLICK"]}]},
        "state": {"url": "u", "title": "t", "text_len": 10}})]
    bad = {"op": "TYPE_TEXT", "target": 0, "confidence": 0.9, "source": "jev",
           "reason": None, "value": None}  # fails op-in-row gate -> escalate
    esc = dict(CLICK_D, source="escalation", reason="invalid_target")
    loop.run(d, goal="g", site="unit", client=OkPolicy([bad]),
             escalate_fn=lambda p: dict(esc),
             receipt_path=str(rp), max_cycles=1)
    lines = [json.loads(x) for x in rp.read_text().splitlines()]
    rec = lines[0]
    assert rec["escalated"] is True and rec["reason"] == "invalid_target"
    pg = rec.get("pre_gate")
    assert pg and pg.get("op") == "TYPE_TEXT" and pg.get("target") == 0, rec
    assert pg.get("confidence") == 0.9


def test_wait_cycles_are_free_toward_max_cycles(tmp_path):
    # v2: waiting on an external process (answer generation) is healthy. The
    # effective cap counts non-WAIT cycles only; wall-clock is the runaway guard.
    rp = tmp_path / "runs.jsonl"
    d = mk_driver()
    # FakeDriver's observe queue is FIFO and mk_driver stocks ONE table: re-observe
    # after the first cycle would hit found:False -> obs_err consumes the budget.
    tbl = d.eval_results["table"][0]
    d.eval_results["table"] = [tbl] * 4
    res = loop.run(d, goal="g", site="unit", client=OkPolicy([WAIT_D, WAIT_D, DONE_D]),
                   escalate_fn=lambda p: dict(DONE_D, source="escalation",
                                              reason=p.get("reason") or "done_verify"),
                   receipt_path=str(rp), answer_probe="g done ok", max_cycles=2,
                   wait_free=True)
    assert res["status"] == "done", res


def test_wall_clock_cap_bounds_wait_forever(tmp_path):
    rp = tmp_path / "runs.jsonl"
    d = mk_driver()
    res = loop.run(d, goal="g", site="unit", client=OkPolicy([WAIT_D] * 50),
                   escalate_fn=lambda p: (_ for _ in ()).throw(AssertionError("no escalation")),
                   receipt_path=str(rp), max_cycles=100, max_wall_s=0.02)
    assert res["status"] == "exhausted"


def test_summarize_checks_flags_decorative_citations():
    raw = {"model_label": "Prepared using X", "sources_listed": 10, "markers_used": 2}
    s = loop.summarize_checks(raw)
    assert s["model_label"] == "Prepared using X"
    assert s["citation_coverage"] == 0.2 and s["decorative_citations"] is True
    assert loop.summarize_checks({}) == {}


def test_done_result_carries_site_checks():
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        rp = pathlib.Path(td) / "runs.jsonl"
        d = mk_driver()
        d.eval_results["table"] = [json.dumps({"rows": [
            {"idx": 0, "role": "button", "name": "go", "value": "", "ops": ["CLICK"]}], "state": {}})] * 2
        res = loop.run(d, goal="g", site="unit", client=OkPolicy([DONE_D]),
                       receipt_path=rp, stuck_escalates=True, max_cycles=3, max_wall_s=5,
                       escalate_fn=lambda p: dict(DONE_D, source="escalation", reason=p.get("reason")),
                       answer_probe="g done ok")
    assert "site_checks" in res and res["site_checks"] == {}
