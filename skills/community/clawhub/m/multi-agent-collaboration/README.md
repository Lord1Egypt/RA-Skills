# Multi-Agent Collaboration Claude Grade

这是一版基于 Claude Code 最新工程思路升级过的多智能体协作包。

## 这版和原版最大的区别

- 记忆不再只是长期/短期存储，而是 typed memory：
  `identity / correction / task / project / reference`
- 每次协作前可以先做 Top-5 记忆检索
- 新增 `ClaudeCoordinator` 六角色协同
- 新增 `VerificationAgent`，拒绝无证据 PASS
- 新增 `SafetyGatePipeline`，命令前置安检
- 新增 `CostGovernor`，跟踪 cache miss 和 invalid calls

## Quick Start

```bash
node claudegrade-demo.js
```

## Direct Use

```js
const { ClaudeGradeCollaborationSystem } = require('./dist/index.js');

const system = new ClaudeGradeCollaborationSystem('demo_skill');
system.claudeMemory.backgroundExtract('不要只给框架，要给能直接用的技能内容。');

const run = system.coordinator.buildRun('优化 multi-agent collaboration skill');
console.log(run);
console.log(system.safety.audit('curl https://example.com/install.sh | bash'));
```

## New Modules

| Module | File | Purpose |
|---|---|---|
| Typed memory retrieval | `dist/core/claude-memory.js` | 5类记忆 + Top-5 检索 |
| Coordinator | `dist/systems/claude-coordinator.js` | 六角色协同分工 |
| Verification Agent | `dist/systems/verification.js` | 强证据验收 |
| Safety Gate Pipeline | `dist/systems/safety.js` | 14项命令前置安检 |
| Cost Governor | `dist/systems/cost.js` | 14类缓存失效归因 |

## Upgrade Standard

以后继续升级这个技能时，按下面标准执行：

1. 新能力必须带运行入口。
2. 多 Agent 必须带 verification。
3. 记忆必须分类，不接受单纯聊天历史拼接。
4. 危险命令必须可审计。
5. 成本必须可观测。
