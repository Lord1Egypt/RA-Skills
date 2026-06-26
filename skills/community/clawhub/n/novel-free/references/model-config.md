# 模型配置指南

## 动态模型检测

Phase 0 时，Coordinator 读取 `openclaw.json`，检测当前宿主环境中可用的模型列表，并以 `provider/model-id` 格式展示给用户选择。

> 说明：具体读取函数与展示方式可由宿主实现决定；文档中的相关代码块仅用于说明流程，不代表固定 API 契约。

## 模型 ID 格式规范

> ⚠️ **强制要求：** `meta/config.md` 和 `meta/agent-registry.json` 中的模型值**必须**使用 `provider/model-id` 格式。这是子 Agent 调度所需的标准写法，格式错误将导致子任务无法按预期调用。

| 格式 | 示例 | 说明 |
|------|------|------|
| ✅ `provider/model-id` | `anthropic/claude-opus-4-6` | 正确格式（仅示例） |
| ✅ `provider/model-id` | `openai/gpt-4o` | 正确格式（仅示例） |
| ✅ `provider/model-id` | `google/gemini-2.5-pro` | 正确格式（仅示例） |
| ❌ 自然语言名 | `Claude Opus` | 错误：缺少 provider/model-id |
| ❌ 自然语言名 | `GPT-4` | 错误：缺少 provider 前缀 |

如用户在 Phase 0 Step 0-4 中输入自然语言名称，Coordinator 须对照 `openclaw.json` 解析出的模型列表，将其转换为正确的 `provider/model-id` 格式后写入配置文件。

## 默认推荐映射

> 以下为**能力导向推荐**。品牌与型号只作示例，不构成固定默认值，应以本地可用模型为准。

| 角色 | 推荐模型类型 | 说明 |
|------|-------------|------|
| Coordinator | 当前会话模型 | 主控，不参与 spawn |
| Worldbuilder | 高推理模型 | 世界观需要深度逻辑与约束一致性 |
| CharacterDesigner | 高推理模型 | 角色弧光与关系设计需要洞察力 |
| OutlinePlanner | 高推理模型 | 结构设计与全局铺排 |
| ChapterOutliner | 长上下文模型 | 需消化大量前置材料 |
| MainWriter | 长上下文 + 文学表达更强模型 | 核心写作，调用最频繁 |
| OOCGuardian | 长上下文模型 | 需比对大量摘要与追踪表 |
| BattleAgent | 通用模型 | 仅处理局部战斗段落 |
| FinalReviewer | 高推理模型 | 终审需要全维度把控 |
| ReaderSimulator | 通用模型 | 读者视角反馈 |
| StyleAnchorGenerator | 高推理模型 | 风格设计与约束提炼 |
| RollingSummarizer | 长上下文模型 | 摘要压缩与信息保真 |

> `12Agent` 是体系名；实际可分配模型的是 **11 个子 Agent**，Coordinator 为当前主会话，不写入子 Agent 注册表。

## 模型回退

当某模型拒绝、故障或超时时，Coordinator 按回退链自动切换。

**详细策略** → 读取 `model-fallback-strategy.md`
