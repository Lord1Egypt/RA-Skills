---
name: lobster-coordinator
description: 三层多Agent协调器（参考Claude Code架构），支持AgentTool单任务委托、Swarm团队协作、Coordinator模式全局调度。当任务复杂需要多Agent协作时自动激活。
metadata: {"openclaw":{"requires":["sessions_spawn","subagents","sessions_send"]}}
---

# Coordinator Mode — 三层多Agent架构

基于 Claude Code 源码的三层多Agent架构，适配 OpenClaw。

## 架构层次

```
Level 3: Coordinator Mode（全局调度）
         ├── 分解任务 → 创建 Team → 分配 Worker → 汇总
         ├── 用 scratchpad 共享中间数据
         └── 用 AgentSummary 监控进度
Level 2: Swarm（团队协作）
         ├── 多个 Agent 组成 Team
         ├── 通过 sessions_send 互发消息
         └── 文件系统持久化通信
Level 1: AgentTool（单任务委托）
         ├── sessions_spawn 创建单个 sub-agent
         ├── 支持 background: true 异步执行
         └── 结果自动回流
```

## Level 1: AgentTool（单任务委托）

### 触发条件
- 单个明确子任务
- 需要特定能力的专项工作

### Agent 定义格式
```markdown
---
description: Agent描述
tools: [read, write, exec, web_search]  # 工具白名单
model: zai/glm-5.1                       # 可指定不同模型
effort: thorough                          # quick/normal/thorough
background: true                          # 是否后台运行
---
# Agent 指令...
```

### 调用方式
```
sessions_spawn:
  runtime: "subagent"
  mode: "run"
  task: "{从agents/目录加载Agent定义 + 具体任务}"
  streamTo: "parent"
```

### 权限隔离规则
- 继承父 Agent 的 alwaysAllow 规则
- **不**继承 alwaysDeny 规则（子Agent可能需要不同权限）
- 独立工具白名单（Agent定义中指定）
- 高风险操作需要用户单独确认

## Level 2: Swarm（团队协作）

### 触发条件
- 需要多个 Agent **互相通信**完成复杂任务
- Agent之间有信息依赖但可异步协作

### 团队概念
```
Team:
  ├── name: string           # 团队名称
  ├── members: TeamMember[]  # 成员列表
  └── scratchpad: string     # 共享数据目录路径

TeamMember:
  ├── name: string           # Agent名称
  ├── role: string           # 角色（来自Agent定义）
  └── sessionKey: string     # 对应的会话ID
```

### 消息传递
通过 `sessions_send` 在 Agent 之间传递消息：
```
Agent A → sessions_send(sessionKey: "B的session", message: "...")
Agent B → 在下一个turn收到消息
```

### 创建 Swarm
```
1. 确定需要的角色和Agent
2. 为每个Agent创建 sessions_spawn(mode: "session", thread: true)
3. 记录每个成员的 sessionKey
4. 通过 sessions_send 分配初始任务
5. 定期用 AgentSummary 检查进度
```

## Level 3: Coordinator Mode（全局调度）

### 触发条件
- 任务需要拆分为3+个独立子任务
- 用户明确要求"并行"、"同时"、"一起"
- 单Agent处理时间预估 > 5分钟

### 工作流程
```
1. 任务分析
   ├── 评估复杂度（简单/中等/复杂）
   ├── 简单 → 直接回答，不浪费Agent
   └── 复杂 → 进入协调器模式

2. 任务拆解
   ├── 拆分为独立子任务
   ├── 标记依赖关系（DAG）
   └── 为每个子任务匹配Agent角色

3. Worker 分派
   ├── 无依赖 → 同时spawn多个Worker
   ├── 有依赖 → 按序spawn
   └── 最多同时5个Worker

4. 进度监控（AgentSummary）
   ├── 每30秒检查一次Worker状态
   ├── 生成3-5词进度摘要
   └── 向用户报告整体进度

5. 结果汇总
   ├── 收集所有Worker结果
   ├── 交叉验证一致性
   ├── 整合为统一输出
   └── 向用户呈现完整方案
```

### Scratchpad（共享工作空间）
协调器和Worker共享数据的目录：
```
/Users/wil/.openclaw/workspace/memory/scratchpad/{task-id}/
  ├── task-plan.md      # 任务计划
  ├── worker-results/   # 各Worker输出
  └── final-report.md   # 最终汇总
```

## Agent Summary（进度摘要机制）

### 摘要策略
- 每30秒检查一次后台Worker状态
- 生成极简摘要（3-5个词描述当前状态）
- 复用父会话上下文，最大化缓存命中
- 格式：`"Reading runAgent.ts"` / `"Fixing null check"` / `"Searching docs"`

### 实现
```
subagents list → 获取所有Worker状态
对每个活跃Worker:
  sessions_history(sessionKey, limit=2) → 获取最新消息
  生成进度摘要 → 报告给用户
```

## 模式自动切换

```
收到任务
  │
  ├── 单一、简单 → 直接处理（无Agent）
  ├── 单一、复杂 → Level 1: AgentTool
  ├── 多任务并行 → Level 3: Coordinator
  └── 需要Agent间通信 → Level 2: Swarm
```

## 两阶段 Review 模式（参考 Superpowers）

每个 Worker 完成任务后，执行两阶段 review：

### Stage 1: Spec Compliance Review
- 代码是否完全匹配任务规格？
- 有没有遗漏的功能点？
- 有没有多余的添加？
- 不通过 → Worker 修复 → 重新 review

### Stage 2: Code Quality Review
- 代码质量、可维护性
- 是否遵循项目约定
- 测试覆盖率
- 不通过 → Worker 修复 → 重新 review

**顺序很重要**：先验证规格符合，再验证代码质量。不要跳过或颠倒。

### 模型选择策略
- **机械任务**（1-2个文件，规格清晰）→ 快速/便宜模型
- **集成任务**（多文件协调、模式匹配）→ 标准模型
- **架构/设计/Review** → 最强模型

## Santa Method（双重独立验证）

参考 ECC 的 Santa Method：

```
生成者(Agent A) → 产出物
  ↓
审查者B(独立) + 审查者C(独立)  — 无共享上下文
  ↓
B通过 AND C通过 → 发布（NICE）
否则 → 修复 → 重新审查（NAUGHTY）
```

适用场景：发布/部署前的最终验证、合规检查、技术文档、面向用户的内容。
不适用：内部草稿、探索性研究、有自动化测试流程的代码。

## 资源限制
- 最多同时 5 个 Worker
- Worker 默认超时 300 秒
- Worker 失败不影响其他 Worker
- 汇总时验证结果正确性和一致性
- 后台Agent完成任务后自动汇报
