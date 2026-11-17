# tests/test_policy.py
import pytest

from jev_webbridge import policy

ROWS = [{"idx": 0, "role": "button", "name": "搜索", "value": None, "ops": ["CLICK"]},
        {"idx": 1, "role": "textbox", "name": "问任何事情", "value": "", "ops": ["CLICK", "TYPE_TEXT"]}]

def test_tau_and_outage_constants():
    # 0.60 -> 0.20 after the 2026-09-24 probe sweep (see probe report)
    assert policy.TAU == 0.20
    assert policy.JEV_OUTAGE_N == 3

def test_needs_escalation_low_confidence():
    d = {"op": "CLICK", "target": 0, "confidence": 0.41, "source": "jev", "reason": None, "value": None}
    assert policy.needs_escalation(d, tau=0.60) == "low_confidence"
    assert policy.needs_escalation(d) is None  # default tau=0.20 (post-sweep)

def test_no_escalation_when_confident():
    d = {"op": "CLICK", "target": 0, "confidence": 0.9, "source": "jev", "reason": None, "value": None}
    assert policy.needs_escalation(d) is None

def test_escalation_for_escalation_source_and_done():
    d = {"op": "CLICK", "target": 0, "confidence": 0.99, "source": "escalation", "reason": "stuck", "value": None}
    assert policy.needs_escalation(d) is None  # escalation decisions are already elevated; loop handles DONE itself
    d2 = {"op": "DONE", "target": None, "confidence": 0.9, "source": "jev", "reason": None, "value": None}
    assert policy.needs_escalation(d2) == "done_verify"

def test_target_must_be_in_table():
    d = {"op": "CLICK", "target": 99, "confidence": 0.95, "source": "jev", "reason": None, "value": None}
    assert policy.needs_escalation(d, rows=ROWS) == "invalid_target"

def test_outage_counter_triggers_at_three():
    c = policy.OutageCounter()
    assert c.record(False) is False
    assert c.record(False) is False
    assert c.record(False) is True
    assert policy.OutageCounter().record(True) is False

def test_jev_client_builds_two_choice_questions(monkeypatch):
    captured = {}
    def fake_jev_ask(questions, api_key=None, endpoint=None):
        captured["questions"] = questions
        return [{"choice": "TYPE_TEXT", "confidence": 0.91},
                {"choice": "1", "confidence": 0.88}]
    monkeypatch.setattr(policy, "_jev_ask", fake_jev_ask)
    c = policy.JevClient(api_key="k", endpoint="https://unit.test")
    d = c.decide(ROWS, goal="搜索 x", state_sig="prose=0")
    assert len(captured["questions"]) == 2
    assert d["op"] == "TYPE_TEXT" and d["target"] == 1
    assert d["confidence"] == pytest.approx(0.88)  # joint = min(op, target)
    assert d["source"] == "jev"

def test_jev_client_maps_wait_and_done_without_target(monkeypatch):
    monkeypatch.setattr(policy, "_jev_ask",
        lambda *a, **k: [{"choice": "WAIT", "confidence": 0.8}, {"choice": "none_of_these", "confidence": 0.2}])
    d = policy.JevClient(api_key="k").decide(ROWS, goal="g", state_sig="s")
    assert d["op"] in policy.NO_TARGET_OPS and d["target"] is None
    assert policy.needs_escalation(d) is None or d["confidence"] < policy.TAU

def test_target_criteria_include_element_description(monkeypatch):
    # Probe finding 2026-09-24: q2 criteria were bare indices — the model could
    # not see WHAT each element is. Labels must carry role + name.
    captured = {}
    def fake(questions, api_key=None, endpoint=None):
        captured["q"] = questions
        return [{"choice": "CLICK", "confidence": 0.9}, {"choice": "0: button: \u641c\u7d22", "confidence": 0.8}]
    monkeypatch.setattr(policy, "_jev_ask", fake)
    policy.JevClient(api_key="k").decide(ROWS, goal="g", state_sig="s")
    crit = captured["q"][1]["criteria"]
    # criteria is a dict {id: description} — API validates probabilities against ids
    assert isinstance(crit, dict), type(crit)
    assert crit.get("0", "").startswith("button:"), crit


def test_state_level_ops_always_offered(monkeypatch):
    # WAIT/DONE/BLOCKED are state-level ops, not element-bound: they must be in
    # q1 criteria even when no row carries them — the API validates choice ids.
    captured = {}
    def fake(questions, api_key=None, endpoint=None):
        captured["q"] = questions
        return [{"choice": "WAIT", "confidence": 0.9}, {"choice": "none_of_these", "confidence": 0.9}]
    monkeypatch.setattr(policy, "_jev_ask", fake)
    policy.JevClient(api_key="k").decide(ROWS, goal="g", state_sig="s")
    ids = set(captured["q"][0]["criteria"])
    assert {"WAIT", "DONE", "BLOCKED"} <= ids, ids
    assert "SELECT" not in ids  # element-bound op with no supporting row stays out


def test_parse_leading_index_from_labeled_choice():
    d = policy._parse([{"choice": "CLICK", "confidence": 0.9},
                       {"choice": "47: a: README.md", "confidence": 0.9}], ROWS)
    assert d["target"] == 47
    d2 = policy._parse([{"choice": "CLICK", "confidence": 0.9},
                        {"choice": "none_of_these", "confidence": 0.9}], ROWS)
    assert d2["target"] is None


def test_jev_unavailable_propagates(monkeypatch):
    def boom(*a, **k): raise policy.JevUnavailable("down")
    monkeypatch.setattr(policy, "_jev_ask", boom)
    with pytest.raises(policy.JevUnavailable):
        policy.JevClient(api_key="k").decide(ROWS, goal="g", state_sig="s")


def test_row_desc_lists_available_ops():
    # Jev kept pairing TYPE_TEXT with plain links because labels hid ops.
    row = {"idx": 7, "role": "link", "name": "收起 项目", "value": "", "ops": ["CLICK"]}
    desc = policy._row_desc(row)
    assert "[CLICK]" in desc and "link" in desc


def test_op_target_incompatibility_is_invalid_target():
    rows = [
        {"idx": 0, "role": "button", "name": "x", "value": "", "ops": ["CLICK"]},
        {"idx": 1, "role": "textbox", "name": "y", "value": "", "ops": ["CLICK", "TYPE_TEXT"]},
    ]
    d = {"op": "TYPE_TEXT", "target": 0, "confidence": 0.9, "source": "jev",
         "reason": None, "value": None}  # TYPE_TEXT on a CLICK-only row
    assert policy.needs_escalation(d, rows=rows) == "invalid_target"
    d_ok = dict(d, target=1)
    assert policy.needs_escalation(d_ok, rows=rows) is None
