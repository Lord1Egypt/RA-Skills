# 多模型决策委员会 — 常见失败模式与排查指南

> 版本：V1.6.0  
> 本文档记录自动化执行中的常见失败模式及排查方法。

---

## 失败模式 1：Thread binding invalid

**症状**：
```
errorCode: "thread_binding_invalid"
error: "Thread bindings are unavailable for webchat."
```

**根因**：在 webchat 通道下使用 ACP runtime + session mode（即 `mode: "session"` + `streamTo: "parent"`）。

**解决**：立即切换为 `runtime: "subagent"` + `mode: "run"`。

**正确示例**：
```yaml
SessionsSpawn:
  runtime: "subagent"
  mode: "run"
  model: "n1n/gpt-5.4"
  task: "评审任务..."
  timeoutSeconds: 180
```

---

## 失败模式 2：Thread required for session mode

**症状**：
```
errorCode: "thread_required"
error: "mode=\"session\" requires thread=true so the ACP session can stay bound to a thread."
```

**根因**：使用了 `mode: "session"` 但没有设置 `thread: true`。

**解决**：二选一：
- 方案A：添加 `thread: true`（仅适用于支持 thread 的通道，如 Feishu/Discord）
- 方案B：切换为 `mode: "run"` + `runtime: "subagent"`（通用，推荐）

---

## 失败模式 3：streamTo only supported for ACP runtime

**症状**：
```
error: "streamTo is only supported for runtime=acp; got runtime=subagent"
```

**根因**：在 `runtime: "subagent"` 下使用了 `streamTo: "parent"`。

**解决**：`subagent` runtime 不需要 `streamTo`，结果通过 `subagent_announce` 事件自动回流。删除 `streamTo` 参数即可。

---

## 失败模式 4：结果未回流到父会话

**症状**：子 Agent 完成了，但组织者没收到结果。

**排查步骤**：

1. **确认使用了 `sessions_yield`**
   - 错误：spawn 后继续执行其他操作
   - 正确：spawn 后立即 `sessions_yield`，等待事件推送

2. **确认没有使用 `deliveryContext` 直接推送给用户**
   - 错误：`deliveryContext: { channel: feishu, to: user }`
   - 正确：不要设置 deliveryContext，让结果回流到父会话

3. **确认子 Agent 输出包含在结果块中**
   - 子 Agent 的输出应自动包装在 `BEGIN_UNTRUSTED_CHILD_RESULT` 块中
   - 若子 Agent 写了文件但未在输出中引用，父 Agent 不会收到文件内容

4. **检查超时**
   - 单个子 Agent 默认 120 秒超时
   - 若评审任务复杂，设置 `timeoutSeconds: 180`

---

## 失败模式 5：提前输出最终报告

**症状**：组织者只收到了部分评委的结果就输出了报告。

**根因**：没有跟踪「已返回 / 待返回」状态，收到第一个结果就急于输出。

**解决**：在会话上下文中维护「轻量级状态跟踪」：
```
[本轮状态跟踪]
Round: 1
Spawned: 3
Received: 2 (GPT-5.4 ✅, Kimi K2.6 ✅)
Pending: 1 (Qwen 3.6 Plus ⏳)
```

确认 `Pending: 0` 后再输出最终报告。

---

## 失败模式 6：模型路由偏差

**症状**：指定了模型A，实际运行的是模型B。

**根因**：OpenClaw 内部模型路由策略可能因配置、配额等原因切换模型。

**解决**：
1. 在 spawn 时明确指定 `model` 参数
2. 在收到结果后，通过 `subagent_announce` 事件中的 `model` 字段确认实际运行的模型
3. 在最终报告中注明实际运行的模型名称（而非仅注明请求的模型）
4. **若路由偏差导致实际模型缺少必要能力**（如长度限制、函数调用等），组织者应立即终止本轮评审，通知用户并提示重新选择模型组合

---

## 失败模式 7：轮询导致流程阻塞

**症状**：组织者反复调用 `sessions_list` 或 `subagents list`，流程卡顿或超时。

**根因**：错误地使用轮询（Poll-based）而非推送（Push-based）等待子 Agent 完成。

**解决**：
- **禁止**在 spawn 后用 `sessions_list`、`subagents list`、`exec sleep` 等方式轮询
- **正确**做法：spawn 后调用 `sessions_yield` 主动挂起，让系统推送完成事件

---

## 失败模式 8：评委返回格式不符合预期

**症状**：子 Agent 返回了结果，但内容格式不标准，无法提取评分。

**根因**：Prompt 模板未被严格遵守，或子 Agent 模型理解有偏差。

**解决**：
1. 在 Prompt 中明确要求输出格式（如「综合评分：[总分，0-100]」）
2. 在解析时使用容错逻辑（正则提取数字）
3. 若格式严重不符合，标记该评委为「返回异常」，使用前一轮结果或跳过

---

## 失败模式 9：多轮评审时上下文丢失

**症状**：第2轮评审时，评委看不到第1轮的结果。

**根因**：每个子 Agent 是独立会话，不自动继承父会话上下文。

**解决**：在第2轮 spawn 时，将第1轮的汇总结果显式写入 `task` 参数中，作为背景信息提供给评委。

---

## 快速排查清单

遇到问题时，按以下顺序排查：

| 顺序 | 检查项 | 命令/方法 |
|:---|:---|:---|
| 1 | 当前通道类型 | `session_status` |
| 2 | 选用的 runtime/mode 是否匹配通道 | 对照「环境适配矩阵」 |
| 3 | 是否使用了 `sessions_yield` | 检查代码逻辑 |
| 4 | 是否有评委超时 | `subagents list`（仅用于排查，不用于轮询） |
| 5 | 子 Agent 输出是否包含结果块 | 检查收到的 inter-session message |
| 6 | 状态跟踪是否显示全部返回 | 检查会话上下文中的跟踪块 |

---

## 环境适配矩阵（速查）

| 环境 | Runtime | Mode | 额外参数 | 结果回收方式 |
|:---|:---|:---|:---|:---|
| **Webchat** | `subagent` | `"run"` | 无 | `subagent_announce` 事件回流 |
| **Feishu（支持thread）** | `acp` | `"session"` | `streamTo: "parent"`, `thread: true` | 流式回流 |
| **Telegram/Discord** | `acp` | `"session"` | `streamTo: "parent"`, `thread: true` | 流式回流 |
| **Unknown/不确定** | `subagent` | `"run"` | 无 | `subagent_announce` 事件回流（兜底方案） |

---

🏛️ **兼听则明，万模共鉴。**
