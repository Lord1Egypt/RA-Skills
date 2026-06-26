---
name: multi-agent
description: Production-ready multi-agent orchestration system for OpenClaw. Implements Coordinator Mode with real parallel worker spawning via sessions_spawn, XML task notifications, state persistence, and four-phase workflow (Research → Synthesis → Implementation → Verification).
---

# Multi-Agent Skill (Phase 2.5 - Production Ready)

生产级多智能体协调系统，支持真实的并行 Worker 执行和完整的四阶段工作流。

## Quick Start

### 1. 准备 Worker

```bash
cd skills/multi-agent
python3 scripts/coordinator_v2.py prepare "Your task description" --role researcher
```

这会生成：
- Worker 规格文件 `.openclaw/scratchpad/workers/{id}.json`
- Worker 提示词 `.openclaw/scratchpad/prompts/prompt-{id}.txt`

### 2. 派生 Worker（真实执行）

```bash
# 读取生成的 prompt 并派生
prompt=$(cat .openclaw/scratchpad/prompts/prompt-{worker-id}.txt)

sessions_spawn --label "multi-agent-worker-{worker-id}" \
               --task "$prompt" \
               --timeout 300 \
               --cleanup keep
```

### 3. 处理完成通知

当 Worker 完成时，它会输出 XML 格式的通知。收集并处理：

```bash
python3 scripts/coordinator_v2.py notify {worker-id} --file notification.xml
```

### 4. 生成规格文档

```bash
# 从已完成的 Research Workers 生成规格
python3 scripts/coordinator_v2.py spec {worker-id-1} {worker-id-2} {worker-id-3}
```

### 5. 运行演示

```bash
# 四阶段工作流演示（模拟执行）
python3 scripts/demo_workflow.py "Your task here"
```

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         COORDINATOR                              │
│  - spawn_worker()   : Prepare worker spec and prompt            │
│  - process_notification() : Handle worker completion            │
│  - generate_spec()  : Synthesize findings from workers          │
└────────────────────┬────────────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
   ┌─────────┐  ┌─────────┐  ┌─────────┐
   │ Worker 1│  │ Worker 2│  │ Worker 3│  ... (parallel)
   │(Research│  │(Research│  │(Research│
   │    1)   │  │    2)   │  │    3)   │
   └────┬────┘  └────┬────┘  └────┬────┘
        │            │            │
        └────────────┼────────────┘
                     ▼
           ┌─────────────────┐
           │   SYNTHESIS     │  Coordinator generates spec
           │  (generate_spec)│
           └────────┬────────┘
                    ▼
        ┌───────────┴───────────┐
        ▼                       ▼
   ┌─────────┐            ┌─────────┐
   │Worker 4 │            │Worker 5 │
   │(Impl 1) │            │(Impl 2) │
   └────┬────┘            └────┬────┘
        │                      │
        └──────────┬───────────┘
                   ▼
         ┌─────────────────┐
         │  VERIFICATION   │
         │ (Worker 6, 7...)│
         └─────────────────┘
```

## File Structure

```
skills/multi-agent/
├── SKILL.md                    # 本文件
├── test-report-phase2.5.md     # 测试报告
├── scripts/
│   ├── coordinator_v2.py       # ⭐ 主协调器（生产级）
│   ├── demo_workflow.py        # 四阶段工作流演示
│   ├── coordinator.py          # Phase 1: 模拟版
│   ├── coordinator_phase2.py   # Phase 2: 过渡版
│   ├── worker.py               # Worker 参考实现
│   └── protocol.py             # XML 协议
└── references/
    └── ARCHITECTURE.md         # 架构设计文档

.openclaw/scratchpad/           # 运行时生成的共享知识
├── workers/                    # Worker 状态
├── results/                    # Worker 结果
├── specs/                      # 规格文档
├── prompts/                    # Worker 提示词
└── coordinator_state.json      # 协调器状态
```

## XML Protocol

Worker 必须按以下格式返回结果：

```xml
<task-notification>
  <task-id>{worker-id}</task-id>
  <status>completed|failed</status>
  <summary>One-line summary</summary>
  <result>
    Detailed findings, changes made, or test results...
    Include specific file paths and code snippets.
  </result>
</task-notification>
```

## Four-Phase Workflow

### Phase 1: Research (并行探索)
- 派生 2-4 个 Researcher Worker
- 每个从不同角度探索问题
- 并行执行，收集发现

### Phase 2: Synthesis (综合)
- Coordinator 读取所有 Researcher 的发现
- 生成 Implementation Specification
- 定义具体的实现步骤

### Phase 3: Implementation (实现)
- 派生 1-2 个 Implementer Worker
- 基于规格执行代码修改
- 可以并行处理不同模块

### Phase 4: Verification (验证)
- 派生 1-2 个 Verifier Worker
- 运行测试，检查回归
- 验证实现正确性

## Commands

### coordinator_v2.py

```bash
# 准备 Worker（创建规格和提示词）
python3 coordinator_v2.py prepare "Task description" --role researcher

# 处理 Worker 完成通知
python3 coordinator_v2.py notify {worker-id} --file notification.xml

# 列出 Workers
python3 coordinator_v2.py list
python3 coordinator_v2.py list --status completed

# 从 Workers 生成规格
python3 coordinator_v2.py spec {id1} {id2} {id3}
```

### demo_workflow.py

```bash
# 运行完整演示（模拟执行）
python3 demo_workflow.py "Your task"

# 查看真实使用示例
python3 demo_workflow.py --real
```

## Integration with OpenClaw

This skill leverages OpenClaw's native capabilities:

| OpenClaw Feature | Multi-Agent Usage |
|-----------------|-------------------|
| `sessions_spawn` | Spawn real worker agents |
| `sessions_send` | Send messages to workers |
| `sessions_list` | List active workers |
| `sessions_history` | Collect worker results |

## State Persistence

- Worker 状态自动保存到 `.openclaw/scratchpad/workers/`
- Coordinator 状态保存到 `.openclaw/scratchpad/coordinator_state.json`
- 支持断点续传：重启后可以恢复之前的 Workers

## Testing

```bash
# 运行演示
python3 scripts/demo_workflow.py

# 检查生成的文件
ls -la .openclaw/scratchpad/
cat .openclaw/scratchpad/specs/spec-*.md
```

## Next Steps

1. **Use it**: 用真实任务测试四阶段工作流
2. **Improve prompts**: 优化 Worker 提示词模板
3. **Add features**: 实现 Agent Teams（Phase 3）
4. **Monitor**: 添加 Token 消耗和耗时统计

## References

- [Architecture Design](references/ARCHITECTURE.md)
- [Test Report](test-report-phase2.5.md)
- [Claude Code Coordinator Mode](https://zread.ai/instructkr/claude-code/19-coordinator-mode)
