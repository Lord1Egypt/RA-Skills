---
name: learning-coordinator
version: 2.0.0
layer: processing
function_type: learning_coordination
health: healthy
adapter: learning_coordinator_adapter
dependencies: []
slug: learning-coordinator
homepage: https://clawhub.com/skills/learning-coordinator
description: Coordinates learning signals, pattern promotion, and stage management
  for self-improving memory. Monitors corrections and preferences to identify emerging
  patterns and manage learning stages. Integrates with Memory Sync Enhanced star architecture
  via adapter.
changelog: Initial release – single-function plugin split from SIPA skill.
metadata:
  clawdbot:
    emoji: 🎓
    requires:
      bins: []
    os:
    - linux
    - darwin
    - win32
    configPaths:
    - ~/self-improving/
    configPaths.optional: []
---

## When to Use

- Need to check learning stage of a pattern or correction
- Want to identify emerging patterns from repeated corrections
- Need to coordinate promotion/demotion of patterns across memory tiers
- Integrating with correction‑logger and preference‑tracker for learning workflows

## Architecture
### NeverOnce 增强功能
- ✅ **有效性反馈集成**：从增强correction-logger获取有效性分数，跟踪修正使用历史
- ✅ **动态阶段转换算法**：基于有效性的自动阶段提升/降级
  - 高有效性模式 → 加速确认
  - 低有效性模式 → 自动降级或标记
- ✅ **反馈循环监控**：跟踪模式有效性趋势，识别高/低效学习模式
- ✅ **学习速度计算**：基于有效性和反馈趋势的学习速度评估
- ✅ **增强报告生成**：模式有效性报告、反馈循环统计、学习进度跟踪
- ✅ **自动调整规则**：基于置信度的自动阶段调整，减少人工干预

### 增强算法
1. **阶段置信度计算**：
   ```
   confidence = (repetition_count * 0.4) + (effectiveness_score * 0.4) + (time_factor * 0.2)
   ```
2. **学习速度评估**：
   ```
   learning_speed = (help_ratio * 0.6) + (effectiveness_trend * 0.4)
   ```
3. **自动调整阈值**：
   - 自动提升: confidence ≥ 0.8
   - 自动降级: effectiveness ≤ 0.2
            
### 集成说明
- **依赖**: 增强correction-logger v2.0.0+（可选，但推荐）
- **数据源**: 从纠正记录器获取有效性分数和反馈历史
- **兼容性**: 原有API完全兼容，新增增强方法可选使用


The plugin provides a `LearningCoordinator` class that:

1. **Monitors learning signals** – watches corrections and preferences via their respective adapters.
2. **Manages learning stages** – tracks patterns through stages: tentative, emerging, pending, confirmed, archived.
3. **Coordinates promotion/demotion** – applies rules for when to move patterns between stages and tiers.
4. **Exposes learning statistics** – reports on learning progress and pattern evolution.

The plugin does not store its own data; it relies on existing adapters (correction‑logger, preference‑tracker) and the learning‑rules file (`learning.md`).

## Installation

```bash
clawhub install learning-coordinator
```

Or manually copy the plugin directory to your workspace skills folder.

## Configuration

Default configuration loads the learning rules file and references other adapters:

```yaml
learning_rules_file: ~/self-improving/learning.md
correction_adapter: "correction_logger"
preference_adapter: "preference_tracker"
auto_create: true
```

## API Reference

### LearningCoordinator Class

```python
from learning_coordinator import LearningCoordinator

coordinator = LearningCoordinator(config=None)

# Get learning statistics
stats = coordinator.get_learning_stats()

# Check emerging patterns
emerging = coordinator.get_emerging_patterns(threshold=2)

# Promote a pattern (after user confirmation)
result = coordinator.promote_pattern(correction_ids=[1, 2, 3], new_status="confirmed")

# Get stage counts
stage_counts = coordinator.get_stage_counts()

# Health check
health = coordinator.health_check()
```

### Adapter Interface

The plugin includes a `LearningCoordinatorAdapter` that conforms to the star‑architecture `MemoryAdapter` base class, providing:

- `health_check()` – reports availability of required adapters and rule file
- `get_stats()` – returns learning statistics (stage counts, promotion rates, etc.)
- `search(query, limit=10)` – searches across learning rules and pattern descriptions
- `sync()` – ensures coordinator state is in sync (no‑op for this plugin)
- `get_learning_stats()`, `get_emerging_patterns()`, `promote_pattern()` – convenience methods

## Integration with Star Architecture

Once installed and its adapter is registered in the star‑architecture registry, other plugins can query learning coordination via the adapter factory:

```python
from integration.adapter_factory import AdapterFactory

factory = AdapterFactory()
coordinator_adapter = factory.get_adapter("learning_coordinator")
if coordinator_adapter:
    stats = coordinator_adapter.get_learning_stats()
    emerging = coordinator_adapter.get_emerging_patterns(threshold=2)
```

## Learning Rules

The plugin reads the `learning.md` file (see SIPA skill) to obtain:

- **Trigger definitions** – what counts as a learning signal
- **Confirmation flow** – how and when to ask for user confirmation
- **Stage evolution** – rules for moving between stages
- **Anti‑patterns** – what not to learn

The file is treated as read‑only; modifications must be made manually.

## Troubleshooting

**Missing adapters** – If correction‑logger or preference‑tracker adapters are unavailable, the coordinator will operate with limited functionality.

**Rule file not found** – If `learning.md` does not exist, the plugin will create a minimal version based on the SIPA skill's default content.

**Permission errors** – Ensure the process has read access to the learning rules file.

## Related Plugins

- **correction‑logger** – logs user corrections and system improvements
- **preference‑tracker** – manages user preferences and patterns
- **heartbeat‑manager** – manages heartbeat state and logs
- **reflection‑logger** – logs self‑reflection entries

## Version History

- **v0.1.0** – Initial split from SIPA skill, basic coordination, star‑architecture adapter.

## 错误码

| 错误码 | 描述 | 解决方案 |
|--------|------|----------|
| E001 | 未知错误 | 检查日志，联系开发者 |
| E002 | 配置错误 | 验证配置文件格式 |
| E003 | 依赖缺失 | 安装所需依赖包 |
