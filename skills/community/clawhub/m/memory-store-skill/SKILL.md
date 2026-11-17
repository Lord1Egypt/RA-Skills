---
name: memory-store
description: >-
  管理用户明确启用的跨会话、多 Agent 结构化记忆。用户明确要求记住、保存、回忆或查询过去内容时使用；已配置 balanced/proactive 策略时，也可在确有历史依赖或形成耐久决策、排障与流程时使用。先读取有效记忆策略，off/explicit 模式不得因普通对话词语自动访问或持久化记忆。
---

# Memory Store

使用纯 Node.js CLI 管理全局与工作区两层记忆。由 Agent 判断语义价值，CLI 负责校验、存储、过滤、排序和归档。

## 先读取有效策略

每次准备访问或写入记忆时，先读取有效配置：

```bash
node scripts/memory_cli.js mode --json
```

| profile | 自动检索 | 自动存储 | 单次对话上限 |
|---|---|---|---|
| `off` | 禁止 | 禁止 | 0 |
| `explicit`（默认） | 仅用户明确要求 | 仅用户明确要求 | 0 |
| `balanced` | 有明确历史依赖时 | decision、debug_solution、workflow、preference | 3 |
| `proactive` | 有明确历史依赖时 | 所有耐久类型 | 5 |

用户明确要求的操作使用 `--intent explicit`。由策略触发的检索或存储必须使用 `--intent automatic`；自动存储还必须提供稳定的 `--source-conv-id`，并向用户简短说明已保存什么。CLI 会拒绝不符合当前策略的自动操作。

## 先判断是否检索

按以下优先级执行：

1. **显式检索**：用户明确引用过去的讨论、决策、进度、偏好或排障记录，使用 `--intent explicit`。
2. **策略检索**：仅 `balanced` / `proactive` 可在任务明显延续、存在实际历史依赖时使用 `--intent automatic`。
3. **跳过检索**：问题自包含且与历史无关，例如一次性解释、翻译或计算。不要为了“每轮都搜”而增加延迟和噪声。

平台注入的 working memory 只是当前会话摘要，不能替代具体历史查询。记忆库无命中时，说明无命中，再从代码、文档或用户提供的信息继续调查；不要猜测历史。

## 运行 CLI

从本 skill 目录执行；需要 Node.js 18 或更高版本。

```bash
node scripts/memory_cli.js status
```

人类用户在真实终端中无参数运行 `memory-store` 时使用数字菜单。Agent、脚本与 CI 始终使用明确短命令，不依赖交互；无 TTY 且无参数时 CLI 只输出精简帮助并退出。

优先使用 `remember`、`recall`、`mode` 和 `status`。只有需要精确过滤、归档恢复等高级能力时才使用 `help --advanced` 中的 v1 兼容命令。

### 检索

从请求提取 2–3 个稳定关键词，并始终带当前 Agent 身份：

```bash
node scripts/memory_cli.js recall "数据库 选型" \
  --as-agent <agent-id> --json
```

任务交接优先检索工作区共享记忆：

```bash
node scripts/memory_cli.js search \
  --query "任务主题 进度" --scope workspace \
  --visibility shared,global --as-agent <agent-id> --limit 10 --stdout
```

只把与当前问题直接相关的结果用于回答。若新旧记忆冲突，优先采用时间更晚、明确标记为最终决策且与当前实现一致的记录，并向用户说明冲突或推断。需要完整条目时再 `recall --id <id> --as-agent <agent-id>`；只读环境中直接使用 search 摘要，不调用会更新访问计数的 recall。

### 存储

仅当以下三问都为“是”时存储：

1. 跨会话或交接后仍可能有用吗？
2. 能压缩成清晰的标题与不超过约 200 字的摘要吗？
3. 若不记录，关键信息会丢失吗？

```bash
node scripts/memory_cli.js remember decision \
  "数据库选型" \
  "选择 SQLite；当前为单用户本地场景，无需独立数据库服务。" \
  --workspace --agent-id <agent-id>
```

`remember` 默认使用 `workspace + shared + explicit`；加 `--global` 写入跨项目全局记忆，加 `--private` 时必须提供稳定 Agent 身份。策略触发的自动存储使用 `--auto --source-conv-id <id>`，CLI 仍会执行档位限制。

不要存原始对话全文。单次对话通常不超过 5 条；优先更新既有记忆，避免重复。

## 选择 scope 与 visibility

| 内容 | scope | visibility |
|---|---|---|
| 当前项目的进度、决策、排障、交接 | `workspace` | `shared` |
| 跨项目稳定偏好或通用事实 | `global` | `global` |
| 仅用于当前 Agent 的临时内容 | 与内容一致 | `private` |

> [!IMPORTANT]
> 针对项目层面的改动（代码重构、架构决策、排障等），**严禁使用 `--scope global`**，必须指定 `--scope workspace` (或 `--workspace`) 存入项目空间；只有跨项目通用习惯/规范才使用 `--scope global`。

`private` 只是基于 `agent-id` 的**协作过滤**，不是加密、操作系统权限或可信安全边界。CLI 不会自动检测或脱敏密钥、凭据、令牌和个人信息；不要把秘密写入记忆库。访问 private 记忆时必须使用同一个 Agent 身份。

## 记录信号

| 信号 | type | 常用 priority |
|---|---|---|
| 选 X 而非 Y，并给出原因 | `decision` | P1 |
| 问题根因与已验证修复 | `debug_solution` | P1 |
| 可重复的操作顺序 | `workflow` | P2 |
| 稳定用户偏好 | `preference` | P2 |
| 项目事实或约束 | `fact` | P2 |
| 可供交接的进度、待办或阻塞 | `state` | P3 |
| 完成、发布等事件 | `event` | P3 |
| 依赖或实体关系 | `relation` | P2 |

用户明确说“记住”时优先记录，但仍要先去除秘密与无复用价值的细节。Agent 负责摘要和分类；`compress` 只提取候选片段，不替代语义判断。

## 多 Agent 规则

- 每次读取和写入都使用稳定的 `--as-agent` / `--agent-id`，或设置 `MEMORY_AGENT_ID`。优先使用宿主提供的 canonical Agent ID；没有时选择一个会话内稳定的 ID 并持续复用。
- 工作区协作成果默认写成 `shared`，包括“做了什么、为何这样做、下一步是什么”。
- 接手任务时先消费相关 shared 记忆，完成阶段后再贡献新的状态或结论。
- 不要尝试绕过其他 Agent 的 private 过滤。

## 按需读取参考资料

- 需要短命令、完整兼容命令、参数、输出与归档恢复操作时，读取 [references/cli.md](references/cli.md)。
- 需要维护策略、隐私模型、并发限制、损坏恢复和备份建议时，读取 [references/operations.md](references/operations.md)。
- 需要直接处理数据格式或验证字段时，读取 [references/memory_schema.json](references/memory_schema.json)。

不要手工改写 `memories.json`，除非 CLI 不可用且已经备份；并发环境下尤其不要直接写 JSON。
