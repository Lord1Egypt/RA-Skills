# Changelog

## 0.3.1 — 2026-11-25

安全边界与可信度修订版。本版本不改变 P0-P4 决策模型、评分权重或危机分级规则。

### 统一为"仅建议、不自动执行"

- 删除 SKILL.md、README.md、`decision_manager.py`、`emergency_plan_generator.py` 中
  "L5/L4 自主执行"和"L3 超时自动执行"的表述。
- 所有危机等级现在统一输出 `advisory_only` / `recommend_await_confirm` 模式；
  `timeout_s` 只表示**建议响应时限**，不会触发任何动作。
- 明确声明：输出是供人工评审的建议，不得接入飞控、调度自动化或任何执行机构。

### 路径与学习流程加固

- 新增 `scripts/path_safety.py`：所有由用户可控字段拼出的路径都经过白名单校验，
  拒绝 `..`、绝对路径和非法分隔符。
- `--learn` 现在要求反馈中包含非空 `approved_by`（或显式传 `--approved-by`），
  并且默认 dry-run；只有加 `--apply` 才写入知识库。
- 知识库更新字段限定白名单，值类型与范围校验通过后才允许写模板；
  写前自动备份原模板到 `.bak`，保留完整变更历史。

### 文档与发布修正

- 移除 0.3.0 发布说明中误贴的无关条目（否定语境检测 / 滑动窗口检测 /
  镜头元素提取 / 角色弧线追踪）；这些功能既不存在于 SKILL.md，也不存在于脚本中。
- 修正 SKILL.md Phase 4 中不存在的 `scripts/knowledge_updater.py` 引用。
- README 新增 3 个"输入 → 输出 → 边界"演练样例。

### 验证

- 全部 8 个 Python 脚本通过 `py_compile`。
- 危机分级 / 方案匹配 CLI 回归通过。
- 未批准的 `--learn` 反馈被拒绝，且不会写入任何文件。
