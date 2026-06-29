# 推理模式学术参考

## 1. Chain-of-Thought (CoT)

### 来源
Wei et al., "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models", NeurIPS 2022

### 核心发现
- 在 few-shot prompt 中加入"让我们一步一步思考"可显著提升数学/推理任务准确率
- GSM8K 数据集：CoT 将准确率从 17.7% 提升到 78.7%
- 对大型模型（>100B参数）效果更明显

### 最佳实践
1. 明确指示"逐步推理"
2. 给出带推理过程的示例（few-shot）
3. 保持推理链的连贯性，不要跳步
4. 最后用一句话总结答案

### 变体
- **Zero-shot CoT**: 直接加"Let's think step by step"（Kojima et al., 2022）
- **Self-Consistency + CoT**: 多次采样 CoT 路径后投票（Wang et al., 2022）
- **Faithful CoT**: 生成自然语言推理链 + 符号化中间步骤（Lyu et al., 2023）

---

## 2. Self-Consistency (SC)

### 来源
Wang et al., "Self-Consistency Improves Chain of Thought Reasoning in Language Models", ICLR 2023

### 核心发现
- 对同一问题生成多条独立推理路径，取多数投票结果
- GSM8K：从 CoT 的 74.4% 提升到 86.5%
- 采样次数越多，准确率越高（但边际递减）

### 最佳实践
1. 采样 5-10 次（经验值：5次性价比最高）
2. 使用较高温度（0.7-1.0）增加多样性
3. 确保每条路径独立（不共享中间状态）
4. 如果投票分散，说明问题有歧义

### 局限性
- 成本是单次推理的 N 倍
- 对开放式问题效果有限（没有"正确答案"可投票）
- 需要可比较的答案格式

---

## 3. Tree-of-Thought (ToT)

### 来源
Yao et al., "Tree of Thoughts: Deliberate Problem Solving with Large Language Models", NeurIPS 2023

### 核心发现
- 将推理过程组织为树状结构，每个节点是一个"思考步骤"
- 可以用 BFS 或 DFS 探索树
- 在需要规划/搜索的任务上显著优于 CoT

### 核心机制
1. **分解**: 将问题分解为多个中间步骤
2. **生成**: 每步生成多个候选方案
3. **评估**: 用启发式方法评估每个候选的"前景"
4. **搜索**: 用 BFS/DFS 在树中搜索最优路径
5. **回溯**: 如果当前路径不可行，回退到之前的节点

### 最佳实践
1. 初始分支 3-5 个（太多会增加评估成本）
2. 评估维度：可行性、成本、风险、效果
3. 淘汰最弱的 1-2 个，深入展开剩余的
4. 如果所有分支都不可行，重新定义问题

### 简化版（适用于 LLM Agent）
完整版 ToT 需要外部搜索算法，简化版让 LLM 自己完成：
1. 一次性生成多个思路
2. 自评每个思路的优劣
3. 选择最优的深入展开

---

## 4. ReAct

### 来源
Yao et al., "ReAct: Synergizing Reasoning and Acting in Language Models", ICLR 2023

### 核心发现
- 将推理（Reasoning）和行动（Acting）交替进行
- 比纯推理（CoT）或纯行动（直接调用工具）都更好
- 推理帮助决定下一步行动，行动结果帮助继续推理

### 核心循环
```
Thought: 我需要知道X的信息
Action: search("X")
Observation: X的信息是...
Thought: 基于这个信息，我需要...
Action: ...
...
Final Answer: ...
```

### 最佳实践
1. 每轮必须先 Thought 再 Action
2. Thought 要简洁，说明"为什么需要这个信息"
3. Action 要精确，参数要正确
4. 设置最大步数限制（防止无限循环）
5. 如果连续 2 次 Action 没有进展，重新评估策略

### 在 OpenClaw 中的映射
OpenClaw 的工具调用机制天然就是 ReAct：
- 模型决定调用哪个工具 = Action
- 工具返回结果 = Observation
- 模型基于结果继续 = Thought

---

## 5. Plan-and-Execute (P&E)

### 来源
Huang et al., "Large Language Models Can Self-Improve with Long-term Memory", 2023
+ HuggingGPT 的 Task Planning 阶段

### 核心发现
- 先生成完整计划，再逐步执行
- 比"边想边做"更可靠，尤其对长链条任务
- 计划阶段可以预判风险和依赖关系

### 核心阶段
1. **Planning**: 分解任务为子任务，确定顺序和依赖
2. **Execution**: 逐步执行每个子任务
3. **Verification**: 验证最终结果是否符合预期
4. **Replanning**（可选）: 如果执行中发现问题，重新规划

### 最佳实践
1. 计划要明确：每个步骤的输入/输出/预期结果
2. 标注依赖关系：哪些步骤可以并行，哪些必须串行
3. 预判风险：每个步骤可能失败的原因和备选方案
4. 执行时记录：每步的实际结果，便于回溯
5. 完成后验证：对比预期和实际，总结偏差

### 与 daily-agent 的关系
daily-agent 的调度流程（分类→评估→路由→执行→收尾）就是 P&E 的体现。
spawn 子代理执行的长任务，也是 P&E 模式。
