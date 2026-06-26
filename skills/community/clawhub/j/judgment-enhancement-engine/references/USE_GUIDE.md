# 使用指南 — 判断力增强引擎

## 安装

### 方式一：一键安装（推荐）

```bash
# Linux / macOS / WSL
bash scripts/setup.sh

# Windows
双击 scripts/setup.bat
# 或在 cmd 中运行:
scripts\setup.bat
```

安装脚本自动检测 Python 并验证引擎。

### 方式二：直接使用
```bash
cp engine.py ./my_project/
```

### 方式三：ClawHub 安装
```bash
clawhub install judgment-enhancement-engine
cd judgment-enhancement-engine
bash scripts/setup.sh  # 补充安装
```

## 快速上手

### 基础用法

```python
from engine import JudgmentEnhancementEngine, JudgmentResult

# 1. 定义世界模型
class SimpleWorldModel:
    def get_possible_outcomes(self, state, action):
        if action == "move_right":
            return [("position_1", 0.9, 1), ("position_0", 0.1, 0)]
        return [("position_0", 1.0, 0)]
    
    def is_terminal(self, state):
        return state == "goal"
    
    def get_legal_actions(self, state):
        if state == "position_0":
            return ["move_right", "stay"]
        return ["stay"]

# 2. 定义目标函数
class SimpleObjective:
    def evaluate(self, state):
        return 10.0 if state == "goal" else 0.0

# 3. 创建引擎
engine = JudgmentEnhancementEngine(
    world_model=SimpleWorldModel(),
    objective=SimpleObjective(),
    risk_tolerance=0.5,
    lookahead_depth=2
)

# 4. 做决策
result = engine.enhance_judgment("position_0")
print(f"Best: {result.best_action}")
print(f"Confidence: {result.confidence:.2f}")

# 5. 记录结果
engine.record_outcome("position_0", result.best_action, 0.8)
```

### 运行内置演示

```bash
python engine.py
```

演示输出一个 5x5 GridWorld 的决策过程。

### 搭配认知引擎使用

```python
from engine import CognitiveEnhancer
from engine import JudgmentEnhancementEngine

brain = CognitiveEnhancer()
judge = JudgmentEnhancementEngine(
    world_model=my_world_model,
    objective=my_objective
)

# 认知引擎提供记忆，判断引擎做决策
context = brain.recall("similar decisions")
result = judge.enhance_judgment(current_state, context)
```

## 参数调优建议

| 场景 | risk_tolerance | lookahead_depth | simulation_breadth | use_greedy_rollout |
|------|----------------|-----------------|-------------------|--------------------|
| 保守决策 | 0.2 | 3 | 5 | True |
| 探索性 | 0.7 | 2 | 3 | False |
| 实时响应 | 0.5 | 1 | 2 | False |
| 高精度 | 0.3 | 4 | 6 | True |

## 测试

```bash
# Python 测试
python scripts/test-basic.py

# Node.js 测试
node scripts/test-client.js
```
