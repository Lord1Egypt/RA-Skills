# Prompt Hardening × Execution Harness 集成指南

prompt-hardening 和 execution-harness 是互补的两层防御：

```
prompt-hardening（概率性：让 LLM 更可能遵守）
      ↓ 但 LLM 仍可能不遵守
execution-harness（确定性：hook 强制介入）
```

## 5 个集成点

### 1. P5（反推理阻断）→ Ralph block 消息

**已实现。** Ralph 的 block 消息使用 P5 模式预判 agent 的合理化倾向：

```
Do NOT rationalize that the remaining work can be done in a follow-up.
Do NOT claim completion with caveats like "mostly done" or "should work".
```

没有 P5 的 block 消息只说"继续工作"，agent 经常用"剩余的可以后续处理"来绕过。P5 预判并阻断这种推理。

### 2. P13（代码级强制）= Hook 本身

**概念映射。** prompt-hardening 的 P13 原则是"关键约束必须有代码级强制作为备份"。execution-harness 的每个 hook 脚本就是 P13 的实现——不依赖 LLM 遵守指令，而是在系统层面强制执行。

| prompt-hardening 指令 | execution-harness 强制 |
|----------------------|----------------------|
| "完成所有文件修改后再停止" | Ralph stop hook 阻止提前停止 |
| "不要用投机语言" | Doubt gate 检测 hedging 词 |
| "失败后换方案" | Tool error advisor deny 重复失败 |

### 3. P9（漂移防护）→ Hook Pair Bracket

**设计指南。** 长对话中 agent 会逐渐"忘记"规则（context drift）。P9 建议在对话中周期性重新注入关键约束。Hook Pair Bracket（Pattern 11）的 UserPromptSubmit hook 是注入点——每轮开始时注入提醒。

示例：

```json
{
  "hooks": {
    "UserPromptSubmit": [{
      "hooks": [{
        "type": "prompt",
        "prompt": "Reminder: you MUST run tests before claiming any task is complete. You MUST NOT use speculative language in your final response."
      }]
    }]
  }
}
```

### 4. P1（三重强化）→ Handoff 文档模板

**设计建议。** Handoff 文档的 5 个必要段落（Decided/Rejected/Risks/Files Modified/Remaining）可以用 P1 三重强化来确保 agent 实际遵守：

```
MUST write a handoff document before completing this stage.
The handoff MUST contain all 5 sections: Decided, Rejected, Risks, Files Modified, Remaining.
I REPEAT: do NOT skip the handoff document.
```

### 5. P4（条件触发）→ Adaptive Complexity

**设计建议。** Adaptive Complexity（Pattern 16）的 triage 结果可以触发不同强度的 prompt hardening：

- Trivial 任务：无额外硬化
- Standard 任务：P1 三重强化关键约束
- Critical 任务：P1 + P5 + P9 + P13 全套

## 何时用 prompt-hardening vs execution-harness

| 场景 | 首选 | 原因 |
|------|------|------|
| Agent 偶尔忘记某条规则 | prompt-hardening | 概率性修复足够 |
| Agent 反复违反同一条规则 | execution-harness | 需要系统级强制 |
| 新部署的规则 | 先 prompt-hardening，观察违规率 | 如果 >20% 违反，加 hook |
| 安全关键约束 | 两者都用 | P13 原则：必须有代码级备份 |
