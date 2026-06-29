"""Tests pytest pour anti-loop v2.0."""
import sys
sys.path.insert(0, '..')

import pytest
from anti_loop import (
    AntiLoop, HealingMode, LoopType,
    PredictiveEntropy, NoveltyDetector, LoopTaxonomy,
    HealingInjector, SelfTuningThresholds, BreathRateMonitor,
    PreFlightRegex, LoopDNA, CrossHarnessAdapters,
)
from anti_loop.adapters import CrossHarnessAdapters as CHA


# ═════════════════════════════════════════════════════════════
# Predictive Entropy
# ═════════════════════════════════════════════════════════════

def test_entropy_initial_high():
    ent = PredictiveEntropy()
    assert ent.observe("action 1") >= 0
    assert ent.observe("action 2") >= 0

def test_entropy_collapse_on_repetition():
    ent = PredictiveEntropy(threshold=0.5)
    for _ in range(50):
        ent.observe("same action")
    assert ent.is_collapse_imminent() == True


# ═════════════════════════════════════════════════════════════
# Novelty Detector
# ═════════════════════════════════════════════════════════════

def test_novelty_high_on_first_action():
    det = NoveltyDetector()
    assert det.observe("totally different action") >= 0.9

def test_novelty_low_on_repetition():
    det = NoveltyDetector()
    det.observe("exact same action text")
    novelty = det.observe("exact same action text")
    assert novelty < 0.1


# ═════════════════════════════════════════════════════════════
# Loop Taxonomy
# ═════════════════════════════════════════════════════════════

def test_taxonomy_verbatim():
    tax = LoopTaxonomy()
    tax.observe("action", "intent")
    loop_type = tax.observe("action", "intent")
    assert loop_type == LoopType.VERBATIM

def test_taxonomy_cyclic():
    tax = LoopTaxonomy()
    tax.observe("A", "i")
    tax.observe("B", "i")
    loop_type = tax.observe("A", "i")
    assert loop_type == LoopType.CYCLIC


# ═════════════════════════════════════════════════════════════
# Healing Injector
# ═════════════════════════════════════════════════════════════

def test_heal_mode():
    h = HealingInjector(mode=HealingMode.HEAL)
    d = h.inject("test action", "find X")
    assert d["action"] == "heal"
    assert "system_message" in d
    assert d["should_continue"] == True

def test_hard_kill_mode():
    h = HealingInjector(mode=HealingMode.HARD_KILL)
    d = h.inject("test", "intent")
    assert d["action"] == "abort"
    assert d["should_continue"] == False

def test_pause_mode():
    h = HealingInjector(mode=HealingMode.PAUSE, pause_seconds=2.0)
    d = h.inject("test", "intent")
    assert d["action"] == "pause"
    assert d["duration_seconds"] == 2.0


# ═════════════════════════════════════════════════════════════
# Pre-Flight Regex
# ═════════════════════════════════════════════════════════════

def test_preflight_tautology():
    pf = PreFlightRegex()
    issues = pf.check("if X then X")
    assert len(issues) >= 1
    assert any("Tautology" in i["issue"] for i in issues)

def test_preflight_while_loop():
    pf = PreFlightRegex()
    issues = pf.check("while not converged: do same thing")
    assert any("Loop without exit" in i["issue"] for i in issues)

def test_preflight_safe_plan():
    pf = PreFlightRegex()
    issues = pf.check("Search the database for user 42")
    assert len(issues) == 0


# ═════════════════════════════════════════════════════════════
# Loop DNA
# ═════════════════════════════════════════════════════════════

def test_dna_record_and_recognize(tmp_path):
    storage = tmp_path / "loops.json"
    dna = LoopDNA(storage_path=storage)
    actions = ["lookup", "user", "42"]
    dna.record(actions, "healed")
    assert dna.is_known(actions)
    assert dna.get_known_count() == 1


# ═════════════════════════════════════════════════════════════
# AntiLoop Main
# ═════════════════════════════════════════════════════════════

def test_antiloop_full_cycle():
    guard = AntiLoop(mode="heal", max_iter=5)
    # 1st action: OK
    r1 = guard.observe("search for X", "find X")
    assert r1["intervene"] == False
    # 2nd action: loop
    r2 = guard.observe("search for X", "find X")
    assert r2["intervene"] == True
    assert r2["directive"]["action"] == "heal"

def test_antiloop_max_iter_triggers():
    guard = AntiLoop(mode="heal", max_iter=3)
    for i in range(3):
        guard.observe(f"unique action {i}", "find")
    result = guard.observe("yet another", "find")
    assert result["intervene"] == True
    assert result["iteration"] >= 3

def test_antiloop_preflight():
    guard = AntiLoop()
    issues = guard.pre_flight("if X then X")
    assert len(issues) >= 1


# ═════════════════════════════════════════════════════════════
# Cross-Harness Adapters
# ═════════════════════════════════════════════════════════════

def test_adapter_custom_fallback():
    class FakeResponse:
        content = "the response"
    text = CrossHarnessAdapters.adapt_custom(FakeResponse())
    assert text == "the response"

def test_adapter_dict():
    text = CrossHarnessAdapters.adapt_hermes({"message": "hello"})
    assert text == "hello"
