# Hook 事件语义速查

向用户解释「这个 hook 什么时候跑、能干什么、成本多高」时读本文件。

## 目录
- [事件全表](#事件全表)
- [matcher 的含义](#matcher-的含义)
- [hook 类型：command vs prompt](#hook-类型command-vs-prompt)
- [PreToolUse 的返回协议](#pretooluse-的返回协议)
- [成本排序](#成本排序)

## 事件全表

| 事件 | 触发时机 | 每轮跑几次 | 能造成什么 |
|---|---|---|---|
| `UserPromptSubmit` | 用户提交后、模型看到之前 | 1 | 可读取并影响你的输入，可注入上下文 |
| `PreToolUse` | 每次工具调用**前** | 每个工具调用 1 次 | **可拦截**（`deny`）、**可要求确认**（`ask`）、可注入 `additionalContext` |
| `PostToolUse` | 每次工具调用**后** | 每个工具调用 1 次 | 观察结果、累积状态（如失败计数） |
| `Stop` | 一轮回答结束时 | 1 | 可触发自动续跑（loop 类 hook 靠它实现）、播提示音 |
| `SubagentStop` | 每个子 agent 结束时 | 视子 agent 数 | 清理子 agent 资源 |
| `PreCompact` | 上下文压缩前 | 压缩时 1 | 抢救即将丢失的状态到文件 |
| `SessionStart` | 会话启动/恢复 | 启动时 1 | 注入初始上下文、恢复持久状态 |
| `SessionEnd` | 会话结束 | 1 | 收尾、落盘 |
| `Notification` | 发通知时 | 不定 | 自定义通知渠道 |
| `PermissionRequest` | 弹权限询问时 | 不定 | 提示用户有待批项 |

**每轮都跑的四个**：`UserPromptSubmit`、`PreToolUse`、`PostToolUse`、`Stop`。这四类是 token 与延迟的主要来源，审计时优先处置。

## matcher 的含义

matcher 的语义**随事件而变**，同一个字符串在不同事件里指不同东西：

| 事件类别 | matcher 匹配什么 | 例子 |
|---|---|---|
| `PreToolUse` / `PostToolUse` | **工具名**（正则） | `Bash`、`Bash\|Read\|Edit`、`Write\|MultiEdit` |
| `SessionStart` | **启动方式** | `startup`（冷启动）、`resume`（恢复）、`compact`（压缩后重启） |
| 其余事件 | 一般用通配 | `*` 或 `.*` = 全部；缺省 = 全部 |

`*` 与 `.*` 都表示全匹配。matcher 缺省等于不过滤。

判断覆盖面时**按事件类别读 matcher**——把 `SessionStart` 的 `compact` 误读成工具名会得出错误结论。

## hook 类型：command vs prompt

| 类型 | 机制 | token 成本 |
|---|---|---|
| `command` | 跑外部脚本，stdin 收 JSON，stdout 回 JSON | 低（除非它输出大量文字/注入上下文） |
| `prompt` | **直接把一段提示词注入上下文** | **高——注入的每个字都算 token** |

审计时把 `prompt` 型单独列出。它没有脚本文件可读，提示词内容就在 `hooks.json` 里，直接看即可。

## PreToolUse 的返回协议

`PreToolUse` 是唯一能阻断工具调用的事件。约定：

- **无输出** → 放行
- **输出 JSON** → 按 `hookSpecificOutput.permissionDecision` 处理：
  - `allow` — 直接放行
  - `ask` — 弹权限询问，等用户
  - `deny` — 拒绝该次调用
- `additionalContext` 字段的文字会注入上下文（影响模型判断 + 烧 token）

dry run 判读：有输出即会干预，看 `permissionDecision` 定严重程度。

## 成本排序

处置优先级从高到低：

1. **`prompt` 型 + 每轮事件** — 每轮注入文字，最贵
2. **`PreToolUse`** — 每个工具调用前跑，且可能拦截，既贵又改行为
3. **`PostToolUse`** — 每个工具调用后跑
4. **`UserPromptSubmit` / `Stop`** — 每轮 1 次
5. **`SessionStart` / `SessionEnd` / `PreCompact`** — 每会话个位数次，通常可留
6. **`Notification` / `PermissionRequest`** — 事件驱动，频率低

一次工具密集的会话里，`PreToolUse` 可能跑上百次——它通常是「变慢」「token 涨得快」的头号嫌疑。
