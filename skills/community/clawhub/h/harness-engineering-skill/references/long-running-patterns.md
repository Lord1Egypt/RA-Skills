# 长时运行 Agent 设计模式

> 蒸馏自 Anthropic 官方工程博客《Effective Harnesses for Long-Running Agents》+ 实战经验。
> 解决核心问题：agent 需要工作跨小时甚至跨天，但 context window 有限，每次新 session 开始时 agent 没有前次记忆。

---

## 核心问题

想象一个软件项目，工程师换班工作，每个新工程师到岗时完全没有上一班的记忆。这就是长时运行 agent 面临的问题：

- 任务需要跨多个 context window 完成
- 每个 context window 结束后，agent "遗忘"一切
- 下一个 session 开始时，如何让 agent 快速恢复上下文？

---


## 目录

- 模式 1：The Initializer（初始化器）
  - 实现
  - 关键字段
  - 何时用
- 模式 2：Incremental Progress（增量进度）
  - 实现
  - 进度文件
- 模式 3：Checkpoint & Resume（检查点与恢复）
  - 实现
- 模式 4：Context Handoff（上下文交接）
  - 实现
- Task
- What I've Done
- What I'm Doing Now
- What's Next
- Important Files
- Warnings
- 模式 5：Sub-agent Delegation（子代理委派）
  - 实现
  - 委派策略
- 模式 6：Tightening Loop（持续改进）
  - 实现
  - 改进层次
- 长时运行 Agent 检查清单
  - 启动前
  - 运行中
  - 恢复后

## 模式 1：The Initializer（初始化器）

**思路**：在每个 context window 开始时，给 agent 一份"交接文档"，让它快速恢复状态。

### 实现

```python
async def build_initializer(session: Session, task: str) -> str:
    """为新一轮 context window 构建初始化文档"""
    return f"""
# Task
{task}

# Previous Progress
{session.get_progress_summary()}

# State
- Files modified: {session.get_modified_files()}
- Tests status: {session.get_test_status()}
- Open TODOs: {session.get_open_todos()}

# Current Step
{session.get_current_step()}

# Next Actions
{session.get_recommended_next_actions()}
"""
```

### 关键字段

| 字段 | 作用 |
|------|------|
| Task | 原始任务描述（不变） |
| Previous Progress | 之前完成的工作摘要 |
| State | 当前文件系统状态、测试状态 |
| Current Step | 当前正在做的子任务 |
| Next Actions | 建议的下一步 |

### 何时用

- 任务预计超过 30 分钟
- 任务有明确的子步骤
- 需要跨 session 恢复

---

## 模式 2：Incremental Progress（增量进度）

**思路**：不要让 agent 一次做太多。把大任务拆成小步骤，每步完成后保存进度。

### 实现

```python
@dataclass
class TaskStep:
    id: str
    description: str
    status: str = "pending"  # pending | in_progress | done | blocked
    result: str = ""
    artifacts: list[str] = field(default_factory=list)  # 产出文件

@dataclass
class ProgressTracker:
    steps: list[TaskStep]
    current_step_id: str = ""

    def get_initializer(self) -> str:
        """生成给下一个 context window 的初始化文档"""
        done = [s for s in self.steps if s.status == "done"]
        current = self.get_current()
        pending = [s for s in self.steps if s.status == "pending"]

        return f"""
# Completed Steps
{self._format_steps(done)}

# Current Step
{self._format_step(current) if current else "All steps complete."}

# Pending Steps
{self._format_steps(pending)}
"""

    def mark_done(self, step_id: str, result: str, artifacts: list[str]):
        step = self._find(step_id)
        step.status = "done"
        step.result = result
        step.artifacts = artifacts
        self._advance()

    def mark_blocked(self, step_id: str, reason: str):
        step = self._find(step_id)
        step.status = "blocked"
        step.result = f"BLOCKED: {reason}"

    def _advance(self):
        """前进到下一个 pending 步骤"""
        for step in self.steps:
            if step.status == "pending":
                self.current_step_id = step.id
                step.status = "in_progress"
                return
        self.current_step_id = ""  # 全部完成
```

### 进度文件

每次步骤完成后，将进度写入文件系统：

```
.progress/
  ├── task.json          # 任务描述 + 步骤列表
  ├── step-001.json      # 步骤 1 结果
  ├── step-002.json      # 步骤 2 结果
  └── current.txt        # 当前步骤 ID
```

下一个 context window 开始时，读 `.progress/` 恢复状态。

---

## 模式 3：Checkpoint & Resume（检查点与恢复）

**思路**：定期保存 agent 的完整状态，崩溃或中断后可恢复。

### 实现

```python
@dataclass
class Checkpoint:
    timestamp: str
    session_id: str
    leaf_entry_id: str
    progress: ProgressTracker
    file_snapshot: dict[str, str]  # path → hash

class CheckpointManager:
    def __init__(self, checkpoint_dir: str = ".checkpoints/"):
        self.dir = checkpoint_dir

    async def save(self, agent: Agent, progress: ProgressTracker):
        """保存检查点"""
        cp = Checkpoint(
            timestamp=datetime.now().isoformat(),
            session_id=agent.session.session_id,
            leaf_entry_id=agent.session.leaf_id,
            progress=progress,
            file_snapshot=await self._snapshot_files(),
        )
        path = f"{self.dir}/cp_{cp.timestamp.replace(':', '-')}.json"
        with open(path, 'w') as f:
            json.dump(asdict(cp), f, indent=2)

    async def restore(self, agent: Agent) -> ProgressTracker:
        """从最新检查点恢复"""
        checkpoints = sorted(glob(f"{self.dir}/cp_*.json"))
        if not checkpoints:
            return ProgressTracker(steps=[])  # 无检查点

        with open(checkpoints[-1]) as f:
            cp = json.load(f)

        # 恢复 session 到检查点
        agent.session.time_travel(cp["leaf_entry_id"])

        return ProgressTracker(**cp["progress"])
```

---

## 模式 4：Context Handoff（上下文交接）

**思路**：当一个 context window 快满时，主动生成"交接文档"给下一个 window。

### 实现

```python
class ContextHandoff:
    async def should_handoff(self, agent: Agent) -> bool:
        """检查是否需要交接"""
        usage = agent.provider.get_last_usage()
        return usage.input_tokens > usage.max_tokens * 0.7

    async def generate_handoff(self, agent: Agent) -> str:
        """生成交接文档"""
        return f"""
# Context Handoff

## Task
{agent.task}

## What I've Done
{await self._summarise_actions(agent.session)}

## What I'm Doing Now
{agent.current_step}

## What's Next
{agent.next_actions}

## Important Files
{agent.modified_files}

## Warnings
{agent.warnings}
"""

    async def handoff_and_continue(self, agent: Agent):
        """交接并启动新 context window"""
        handoff_doc = await self.generate_handoff(agent)

        # 保存交接文档
        with open(f".handoff/{datetime.now().isoformat()}.md", 'w') as f:
            f.write(handoff_doc)

        # 创建新 session
        new_session = Session.create_new()
        new_session.append_message("system", handoff_doc)

        # 用新 session 继续
        agent.session = new_session
```

---

## 模式 5：Sub-agent Delegation（子代理委派）

**思路**：主 agent 只做规划和协调，具体执行委派给子 agent。每个子 agent 有独立 context window。

### 实现

```python
async def delegate_to_subagent(
    parent: Agent,
    profile: SubagentProfile,
    task: str,
) -> dict:
    """主 agent 委派任务给子 agent"""
    # 创建子 agent（独立 session、独立 context window）
    sub_agent = Agent(
        provider=parent.provider,
        tools=parent.tools.restrict_to(profile.active_tools),
        session=Session.create_new(),
        config=AgentConfig(max_iterations=20),
    )

    # 运行子 agent
    result = await sub_agent.run(task)

    # 结构化返回
    return {
        "profile": profile.name,
        "task": task,
        "result": result,
        "files_read": sub_agent.session.get_files_touched(),
        "tokens_used": sub_agent.provider.get_total_usage(),
    }
```

### 委派策略

| 场景 | 子 agent profile | 原因 |
|------|-----------------|------|
| 探索代码库 | researcher（只读工具） | 防止意外修改 |
| 实现功能 | implementer（全工具） | 需要写文件 |
| 审查代码 | reviewer（只读 + 高 thinking） | 需要深度推理 |
| 运行测试 | tester（bash + read） | 只需要跑测试 |

---

## 模式 6：Tightening Loop（持续改进）

**来自 Addy Osmani**：

> "Anytime you find an agent makes a mistake, you take the time to engineer a solution such that the agent never makes that mistake again."

### 实现

```python
class TighteningLoop:
    """记录 agent 失败模式，自动生成改进建议"""

    def __init__(self):
        self.mistakes: list[Mistake] = []

    def record_mistake(self, mistake: Mistake):
        self.mistakes.append(mistake)
        # 分类
        category = self._categorise(mistake)
        # 生成改进建议
        fix = self._suggest_fix(category, mistake)
        return fix

    def _categorise(self, mistake: Mistake) -> str:
        if "wrong file" in mistake.description:
            return "tool_guidance"
        if "forgot to test" in mistake.description:
            return "prompt_addition"
        if "dangerous command" in mistake.description:
            return "extension_guard"
        return "unknown"

    def _suggest_fix(self, category: str, mistake: Mistake) -> str:
        fixes = {
            "tool_guidance": "Add to AGENTS.md: 'Always confirm file path with user before editing.'",
            "prompt_addition": "Add to system prompt: 'Run tests after every code change.'",
            "extension_guard": "Create extension: block_dangerous_commands.py",
        }
        return fixes.get(category, "Investigate manually.")
```

### 改进层次

| 层次 | 方法 | 效果 |
|------|------|------|
| 1. Prompt 调整 | 修改 AGENTS.md / system prompt | 软引导，降低概率 |
| 2. Tool 设计 | 修改工具参数/schema | 中等，结构化约束 |
| 3. Extension | 写 hook 拦截 | 硬护栏，确定性 |

**优先级**：能用 extension 解决的不用 prompt，能用工具设计解决的不用 extension。

---

## 长时运行 Agent 检查清单

### 启动前

- [ ] 任务已拆分为可独立验证的步骤
- [ ] ProgressTracker 已初始化
- [ ] CheckpointManager 已配置
- [ ] Context handoff 阈值已设置（70%）
- [ ] Sub-agent profiles 已定义
- [ ] 初始化器模板已准备

### 运行中

- [ ] 每步完成后保存进度
- [ ] 定期 checkpoint（每 N 步或每 M 分钟）
- [ ] context 使用量监控
- [ ] 用户可随时取消
- [ ] 失败模式记录到 tightening loop

### 恢复后

- [ ] 读取最新 checkpoint
- [ ] 验证文件系统状态一致
- [ ] 从 ProgressTracker 恢复当前步骤
- [ ] 给 agent 注入初始化器
