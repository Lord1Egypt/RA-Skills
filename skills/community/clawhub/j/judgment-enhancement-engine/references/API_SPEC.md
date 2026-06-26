# API 规格说明书 — 判断力增强引擎 (Judgment Enhancement Engine)

## JudgmentEnhancementEngine

核心类，基于蒙特卡洛前瞻模拟增强 AI Agent 判断力。

### 构造函数

```python
JudgmentEnhancementEngine(
    world_model: WorldModel,
    objective: ObjectiveFunction,
    risk_tolerance: float = 0.5,
    lookahead_depth: int = 3,
    simulation_breadth: int = 4,
    history_size: int = 100,
    max_compute_time_sec: float = 1.0,
    use_greedy_rollout: bool = True
)
```

**参数：**
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `world_model` | WorldModel | 必填 | 世界模型，定义状态转移和动作空间 |
| `objective` | ObjectiveFunction | 必填 | 目标函数，评估状态效用 |
| `risk_tolerance` | float | 0.5 | 0=极端风险厌恶，1=风险中性 |
| `lookahead_depth` | int | 3 | 递归展望层数 |
| `simulation_breadth` | int | 4 | 每层最大评估动作数 |
| `history_size` | int | 100 | 历史记录最大容量 |
| `max_compute_time_sec` | float | 1.0 | 最大计算时间（秒） |
| `use_greedy_rollout` | bool | True | True=贪心(准确)，False=均匀采样(快速) |

---

### 协议

#### WorldModel
```python
class WorldModel:
    def get_possible_outcomes(self, state: Any, action: Any) -> List[Tuple[Any, float, float]]:
        """返回 [(next_state, probability, reward), ...]"""
    
    def is_terminal(self, state: Any) -> bool:
        """判断是否终止状态"""
    
    def get_legal_actions(self, state: Any) -> List[Any]:
        """返回当前状态下的合法动作列表"""
```

#### ObjectiveFunction
```python
class ObjectiveFunction:
    def evaluate(self, state: Any) -> float:
        """返回状态效用值（越高越好）"""
```

---

### 方法

#### `enhance_judgment(state: Any) -> JudgmentResult`
在不确定性下评估所有可能动作，返回最佳选择。

- **输入：** `state` — 当前状态
- **输出：** `JudgmentResult`（见下方）

#### `record_outcome(state: Any, action: Any, actual_utility: float) -> None`
记录实际执行结果，用于历史修正。

- **输入：** `state` — 状态；`action` — 执行的动作；`actual_utility` — 实际获得的效用

#### `clear_history() -> None`
清空所有历史记录和反思积累。

---

### JudgmentResult

| 字段 | 类型 | 说明 |
|------|------|------|
| `best_action` | Any | 选中的最佳动作 |
| `scores` | dict | 各动作的风险调整效用（{action: score}） |
| `raw_utilities` | dict | 各动作的原始期望效用 |
| `risk_metrics` | dict | 各动作的风险指标（expectation, variance, std, var95） |
| `reasoning` | str | 人类可读的决策推理 |
| `confidence` | float | 0~1 置信度 |

---

### 错误码

| 情况 | 行为 |
|------|------|
| 无合法动作 | 状态/action=None，confidence=0，reasoning="no_legal_actions" |
| 超时 | 返回部分结果，record_outcome 带 score=0 标记 |
| history 满 | 自动淘汰最早记录 |
