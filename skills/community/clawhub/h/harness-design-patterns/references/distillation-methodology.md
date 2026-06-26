# Distillation Methodology（蒸馏方法论）

从生产级 Agent 代码中提取可复用 pattern 的方法论。蒸馏自 LastWhisperDev 的实践经验和 Anthropic/OpenAI 的 harness engineering 博客。

## 核心原则

### PCA 降维类比

> 代码是高维的，但有价值的设计模式是低秩的。蒸馏的本质是找到主成分。

客观地提取"所有模式"反而是最没用的——因为没有视角就没有优先级。好的蒸馏需要：

1. **注入基向量**：人的品味、分析框架、已有经验作为投影方向
2. **沿基向量投影**：让 agent 从复杂代码中提取沿这些方向的主成分
3. **标注立场**：诚实地声明蒸馏的视角是什么

### 先建协调机制，再开始干活

在任何 agent 动手之前，先建：
- **Role Briefs**：每个 agent 是谁、规则是什么
- **Coordination Layer**：task board、progress log、handoff 模板
- **Quality Gates**：什么算完成、review checklist

### Review-Execution 分离

不让实现者审查自己的代码。用不同模型分别做 review 和 execution：
- Reviewer 以全新视角对照源码审查
- Executor 带着对先前决策的完整理解执行修改
- 两个 agent 互不可见对方的 session

### 每轮新 session

每轮 review-action 循环在全新 session 中进行。好处：
- 拿到完整的 token 预算
- 不被前几轮的上下文污染
- 通过 handoff 文件传递上下文（文件系统作为 API）

## 3 层 Context 设计

每个 agent 在每次执行时只需要 3 类 context：

1. **Agent Role**：角色定义和操作规则
2. **Task Handoff**：当前任务的具体信息（索引级别，不是全文）
3. **Repo Filesystem**：给 agent 一张地图，不是一本千页手册

> "Give Codex a map, not a 1,000-page instruction manual." — OpenAI

## 参考文献

- Anthropic: [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- OpenAI: [Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/)
- OpenAI: [How we used Codex to build Sora for Android in 28 days](https://openai.com/index/shipping-sora-for-android-with-codex/)
- Anthropic: [Building multi-agent systems: When and how to use them](https://claude.com/blog/building-multi-agent-systems-when-and-how-to-use-them)
- LastWhisperDev: [把 Claude Code 源码蒸馏成 Agent Skill](https://mp.weixin.qq.com/s/R9EgZlx1RnXK4L12OBQn-w)
