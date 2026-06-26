from core.experiment import ExperimentEngine
import os

engine = ExperimentEngine()

# 測試正常路徑
print("Testing normal run...")
engine.run_experiment({
    "hypothesis_description": "P0 Test: Normal Run",
    "proposed_config_changes": {"learning_rate": 0.0005}
})

# 測試失敗路徑 (模擬錯誤)
print("Testing failure run...")
class MockHypothesis(dict):
    def get(self, key, default=None):
        if key == "proposed_config_changes":
            raise ValueError("Simulated OOM Error for RCA Test")
        return super().get(key, default)

try:
    engine.run_experiment(MockHypothesis({
        "hypothesis_description": "P0 Test: Failure RCA",
    }))
except:
    pass

print("
Final results.tsv content:")
with open("results.tsv", "r") as f:
    print(f.read())
