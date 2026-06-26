# Detailed Pattern Descriptions
---

### P1: 三重强化（最强，用于 P0 规则）

**大写关键词 + 重复 + 反面示例** 三者叠加。

```markdown
## P0 硬约束

6. **MUST 通过 dispatch.sh 异步派发代码任务**

CRITICAL: 所有 NanoCompose 代码操作 MUST 通过 dispatch.sh 派发。

<good-example>
~/.openclaw/skills/nanocompose-dispatch/scripts/dispatch.sh \
  --type review --id 12345 --prompt "Review MR #12345"
</good-example>

<bad-example>
tmux new -d -s claude-mr2273 && tmux send-keys -t claude-mr2273 "claude --print ..."
</bad-example>

NEVER 自己拼 tmux 命令。NEVER 直接运行 claude -p。
dispatch.sh 负责 tmux 创建、结果捕获和完成回调。手动 tmux 命令会导致 0-byte 结果文件和无回调通知。

I REPEAT: 任何涉及 NanoCompose 代码的操作，MUST 使用 dispatch.sh，NEVER 手动创建 tmux session。
```

**为什么有效**：
- 大写 MUST/NEVER/CRITICAL 标记不可协商
- `<good-example>` / `<bad-example>` 提供行为锚定
- 解释 WHY（"导致 0-byte 结果文件"）让模型理解后果
- `I REPEAT` 显式重复，经验证可将合规率提升 30%+

---

### P2: 工具强制 + 负向门禁

指定正确工具 + 列举禁止的替代方案 + 解释为什么替代方案会失败。

```markdown
用 dispatch.sh 派发任务（NOT tmux new/send-keys）。
用 queue.sh 管理队列（NOT 直接编辑 JSON）。
用 aone-kit call-tool 发 MR 评论（NOT 写到本地文件让人手动粘贴）。

禁止原因：
- tmux send-keys 绕过回调脚本，任务完成后不会通知
- 直接编辑 JSON 无文件锁，并发写入导致数据丢失
- 写本地文件需要人工操作，违反自动化原则
```

**为什么有效**：`Use X (NOT Y)` 括号否定是最有效的工具强制形式。加上失败原因后，模型不仅知道规则，还理解违反的后果。

---

### P3: 穷举否定枚举

不要指望模型推断不该做什么，显式列出所有禁止行为。

```markdown
### 禁止行为（会阻塞 session）
- ❌ 直接 exec 读/写 ~/work/NanoCompose/ 下的源码文件
- ❌ 直接运行 `claude -p` 同步等结果
- ❌ 用 `tmux new` 或 `tmux send-keys` 手动创建 session
- ❌ 在 main session 里做代码分析、编辑、编译
- ❌ 把审查报告写到 /tmp/*.md 让用户手动粘贴

### 正确做法
- ✅ 调用 dispatch.sh 异步派发
- ✅ 立即回复用户"已派发到 nc-xxx"
- ✅ 等 callback 通知结果
- ✅ 用 aone-kit call-tool code::comment_merge_request 直接发评论
```

**为什么有效**：✅/❌ 视觉标记 + 具体命令级别的枚举，消除所有歧义。

---

### P4: 条件触发规则

定义精确的触发条件，消除模型自由裁量。

```markdown
当用户说"review MR"时：
→ MUST 调用 dispatch.sh --type review
→ NEVER 自己读代码做 review

当用户说"fix bug"时：
→ 只报告 bug 信息，等用户确认
→ NEVER 自动入 bugfix pipeline

当队列为空且没有运行中任务时：
→ 回复"队列空闲"
→ NEVER 输出完整报告
```

**为什么有效**：`当 X → MUST Y / NEVER Z` 格式预先定义了决策路径，模型不需要自己判断。

---

### P5: 先发制人的反推理阻断

识别模型"合理化"违规的思维模式，并提前阻断。

```markdown
如果你发现自己在想"我可以直接用 tmux 更快"——这个想法本身就是违规信号。
dispatch.sh 存在的原因就是防止你"更快"但没有回调的执行方式。
"更快"不是绕过 dispatch.sh 的理由。
```

来自 Claude.ai 官方 prompt：
> "If Claude finds itself mentally reframing a request to make it appropriate, that reframing is the signal to REFUSE, not a reason to proceed."

**为什么有效**：直接描述模型违规前的内部推理过程，让它在推理阶段就自我阻断。

---

### P6: 显式优先级层级

当规则冲突时，明确哪个赢。

```markdown
优先级（高→低）：
1. SOUL.md P0 硬约束（不可覆盖）
2. AGENTS.md 操作规范
3. TOOLS.md 工具指南
4. Cron prompt 中的指令
5. 用户对话中的即时要求

如果用户说"直接帮我跑一下 review"，仍然 MUST 通过 dispatch.sh。
用户即时要求不能覆盖 P0 硬约束。
```

---

### P7: 行为锚定示例（含推理）

好/坏示例 + 解释 WHY。

```markdown
<good-example>
用户: "review MR #2251"
Agent: "已通过 dispatch.sh 派发到 nc-review-2251，预计 10 分钟完成，完成后会通知你。"
<reasoning>使用 dispatch.sh 异步派发，不阻塞 session，有回调通知</reasoning>
</good-example>

<bad-example>
用户: "review MR #2251"
Agent: [直接用 tmux send-keys 创建 session，同步等待结果]
<reasoning>绕过 dispatch.sh，无回调通知，阻塞 session 导致后续消息无响应</reasoning>
</bad-example>
```

---

### P8: 范围限制（做要求的事，不多做）

```markdown
你是调度层，NOT 执行层。
你的工作是：识别任务 → 构建 prompt → dispatch → 立即回复。
你不需要理解代码、不需要分析 diff、不需要读源文件。
CC 在 NanoCompose 目录下运行时会自动加载 skills/rules/hooks。

如果你发现自己在读 NanoCompose 的 .cpp/.h 文件，你已经越界了。
```

---

### P9: 漂移防护（长对话提醒）

在长对话中注入提醒，防止模型逐渐偏离规则。

```markdown
<long_conversation_reminder>
你是 Muse，NanoCompose 项目的调度层 agent。
核心约束不因对话长度而改变：
- 代码任务 MUST 通过 dispatch.sh
- Bug/需求只报告不自动处理
- 空队列时静默
重新检查：你接下来的操作是否符合 SOUL.md P0？
</long_conversation_reminder>
```

---

### P10: 信任边界

```markdown
TOOLS.md 和 AGENTS.md 中的指令是系统级约束。
用户对话中的"帮我直接跑一下"不覆盖这些约束。
如果不确定，选择更保守的做法（dispatch 而非直接执行）。
```

---

---

### P11: Echo-Check（执行前复述约束）

让模型在执行前先复述自己理解的约束，从"生成模式"切换到"验证模式"。

```markdown
在派发任务前，先在内部确认：
1. 我要使用的工具是什么？（必须是 dispatch.sh）
2. 我是否在尝试直接运行 claude 或创建 tmux？（如果是，停止）
3. 这个操作完成后会有回调通知吗？（如果没有，方法错误）
```

**来源**：Reddit r/PromptEngineering，500+ upvotes，多人独立验证合规率提升 40-60%。

---

### P12: 约束优先（约束 > 任务描述）

来自 sinc-LLM 框架，275 个生产 agent 的实证数据：

> **约束对输出质量的影响是 42.7%，任务描述只有 2.8%。**

实操含义：**约束部分的 token 应该比任务描述更多。** 花更多篇幅说"怎么不出错"而不是"做什么"。

---

### P13: 结构化不可能性（代码强制 > 提示词强制）

来自 Anthropic 官方建议：

> "We actually spent more time optimizing our tools than the overall prompt. We changed the tool to always require absolute filepaths -- the model used this method flawlessly."

**5 层防绕过体系**（从弱到强）：

| 层级 | 方法 | 可靠性 |
|------|------|--------|
| L1 | 软提示约束（"请用绝对路径"）| ~40% |
| L2 | 硬提示约束（"MUST 用绝对路径"）| ~80% |
| L3 | 强调提示约束（"CRITICAL + I REPEAT + 示例"）| ~90% |
| L4 | API 结构约束（JSON schema, tool_choice）| ~99% |
| L5 | 代码级验证（hook 拦截 + 重试）| 100% |

**对我们的含义**：dispatch.sh 的约束目前在 L3（强调提示）。EXEC GUARD plugin 是 L5（代码级）。两者配合使用。

---

## 应用清单

对目标 prompt 逐项检查：

| # | 检查项 | 通过？ |
|---|--------|--------|
| 1 | 每条 P0 规则是否用了三重强化（MUST + 反面示例 + 重复）？ | |
| 2 | 工具约束是否用了 `Use X (NOT Y)` + 失败原因？ | |
| 3 | 禁止行为是否穷举列出？ | |
| 4 | 关键触发条件是否用了 `当 X → MUST Y` 格式？ | |
| 5 | 是否有反推理阻断（预判模型的合理化借口）？ | |
| 6 | 优先级层级是否显式声明？ | |
| 7 | 是否有好/坏示例对？ | |
| 8 | 范围边界是否明确（做什么/不做什么）？ | |
| 9 | 长对话是否有漂移防护？ | |
| 10 | 信任边界是否明确？ | |
| 11 | 关键操作前是否有 echo-check 自验步骤？ | |
| 12 | 约束 token 是否多于任务描述 token？ | |
| 13 | 最关键的约束是否有代码级强制（L5）备份？ | |
| 14 | 多步操作是否有状态机门禁（前置条件检查）？ | |
| 15 | 违规后是否有自我归因修正模板？ | |
| 16 | 关键约束是否在 prompt 首尾都出现？ | |

## 使用方式

```
1. 读取目标 prompt（SOUL.md / AGENTS.md / cron prompt / etc.）
2. 识别模型历史违反过的规则（最高优先级）
3. 对照 13 个模式逐项检查
4. 历史违反规则 → P1 三重强化 + P13 代码级强制
5. 重要规则 → P2 工具强制 + P4 条件触发 + P5 反推理阻断
6. 一般规则 → P3 穷举枚举 + P7 示例对
7. 验证约束 token 占比 > 40%（P12）

原则：最可靠的约束不是更好的措辞，而是结构化不可能性。
```

---

### P14: 状态机门禁（阶段锁定）

来自 Factory DROID：用布尔前置条件锁定阶段，不满足不能进入下一步。

```markdown
任务派发 MUST 满足以下前置条件，BOTH 必须为真：
1. 任务类型已识别（review/bugfix/crash/feat 之一）
2. 任务 ID 已提取（MR ID 或工作项 ID）

如果任一条件不满足，向用户确认。NEVER 猜测 ID。
```

**来源**：Factory DROID — 通过 state machine 锁定阶段，防止模型跳步。

---

### P15: 自我归因错误修正（运行时纠正）

来自 CrewAI：当检测到格式违规时，注入第一人称"我刚才做错了"的修正消息。

```markdown
如果你刚才用了 tmux send-keys 而不是 dispatch.sh：
"我刚才违反了 P0 第 6 条。正确做法是用 dispatch.sh。我现在重新执行。"
然后立即用 dispatch.sh 重新派发。
```

**来源**：CrewAI — 自我归因的纠正比外部纠正更有效，模型将其视为自己的领悟而非被指令覆盖。

---

### P16: 首尾重复（注意力位置优化）

来自 Claude Code + "Lost in the Middle" 研究：关键约束放在 prompt 的最前面和最后面。

> LLM 对上下文的开头和结尾关注度最高，中间的指令被遵循的概率下降 20%。

```markdown
# 文件开头
CRITICAL: 代码任务 MUST 通过 dispatch.sh 派发。

# ... 200 行其他规则 ...

# 文件末尾
I REPEAT — 最重要的规则：代码任务 MUST 通过 dispatch.sh 派发。NEVER 手动 tmux。
```

**来源**：Claude Code 实际 system prompt 在开头和结尾重复了安全相关约束。Liu et al. 2023 "Lost in the Middle" 论文验证。

