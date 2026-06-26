"""判断力增强引擎 — 基础功能测试"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from engine import JudgmentEnhancementEngine

class SimpleWorld:
    def __init__(self):
        self.pos = 0
    def get_possible_outcomes(self, state, action):
        if action == "right":
            return [("pos_1", 0.9, 1), ("pos_0", 0.1, 0)]
        return [("pos_0", 1.0, 0)]
    def is_terminal(self, state):
        return state == "goal"
    def get_legal_actions(self, state):
        return ["right", "stay"]

class SimpleObjective:
    def evaluate(self, state):
        return 10.0 if state == "goal" else 0.0

def test_basic():
    print("=== Judgment Enhancement Engine Tests ===\n")
    
    # Test 1: engine creation
    engine = JudgmentEnhancementEngine(
        world_model=SimpleWorld(),
        objective=SimpleObjective(),
        risk_tolerance=0.5,
        lookahead_depth=2,
        simulation_breadth=3,
        use_greedy_rollout=True
    )
    print("[PASS] Engine created")
    
    # Test 2: enhance_judgment returns valid result
    result = engine.enhance_judgment("pos_0")
    assert result.best_action is not None, "Should return a best action"
    assert 0 <= result.confidence <= 1, "Confidence should be 0-1"
    print(f"[PASS] enhance_judgment: best={result.best_action}, confidence={result.confidence:.2f}")
    
    # Test 3: result structure
    assert hasattr(result, 'scores'), "Should have scores"
    assert hasattr(result, 'raw_utilities'), "Should have raw_utilities"
    assert hasattr(result, 'risk_metrics'), "Should have risk_metrics"
    assert hasattr(result, 'reasoning'), "Should have reasoning"
    print(f"[PASS] Result structure: {len(result.scores)} actions evaluated")
    
    # Test 4: record_outcome
    engine.record_outcome("pos_0", result.best_action, 0.8)
    print("[PASS] record_outcome")
    
    # Test 5: clear_history
    engine.clear_history()
    print("[PASS] clear_history")
    
    print("\n=== ALL TESTS PASSED ===")

if __name__ == '__main__':
    test_basic()
