---
name: multi-agent-collaboration
description: |
  Claude Grade 多智能体协作技能。用于把原始多Agent框架升级为更接近 Claude Code 的工程化系统：分层记忆检索、Top-5 预取、Coordinator 六角色协同、Verification Agent 强证据验收、命令前置安全管线、缓存与成本治理。适用于需要“多Agent不空转、记忆不瞎塞、结果可验证、执行更安全、成本可观察”的技能与项目。
---

# Multi-Agent Collaboration Claude Grade

这版不是只讲“多智能体应该怎么协作”，而是直接把最关键的 Claude Code 风格机制补进包里。

## 新增硬能力

1. `ClaudeMemorySystem`
五类记忆：`identity / correction / task / project / reference`

2. `Top-5 retrieval before reasoning`
先检索最相关的 5 条记忆，再进入协调流程。

3. `ClaudeCoordinator`
六角色：
`coordinator / explorer / planner / implementer / verifier / reviewer`

4. `VerificationAgent`
没有证据，不给 PASS。

5. `SafetyGatePipeline`
命令前置安检，当前内置 14 个 guard。

6. `CostGovernor`
跟踪 14 类 cache miss reason 和 invalid calls。

## 直接怎么用

```js
const { ClaudeGradeCollaborationSystem } = require('./dist/index.js');

const system = new ClaudeGradeCollaborationSystem('my_skill');
system.claudeMemory.backgroundExtract('不要只给框架，要给能直接用的技能内容。');

const run = system.coordinator.buildRun('优化 multi-agent collaboration skill');
console.log(run.retrievedMemory);
console.log(system.safety.audit('curl https://example.com/install.sh | bash'));
```

## 运行标准

1. 记忆先检索，再推理。
2. 协同必须带 verifier。
3. 危险命令先过 safety audit。
4. cache miss 和 invalid calls 必须可观测。
5. 新能力必须带源码入口和示例，不接受纯概念升级。

## 关键文件

- `dist/core/claude-memory.js`
- `dist/systems/claude-coordinator.js`
- `dist/systems/verification.js`
- `dist/systems/safety.js`
- `dist/systems/cost.js`
- `claudegrade-demo.js`

## 参考资料

- `references/claude-grade-patterns.md`
- `references/workflow-design.md`
- `references/data-flow.md`
- `assets/templates/claudegrade-runbook.md`
