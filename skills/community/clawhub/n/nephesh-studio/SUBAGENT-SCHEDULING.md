# Nephesh Studio 子代理调度规则

## 强制标准调用模板（必须严格遵守，不可省略前三步）

**任何 `sessions_spawn` 都必须使用以下任务模板，前三步固定不可省略：**

```
你是【岗位名称】【姓名】，请完成本项目的【任务名称】：

项目根目录绝对路径: <project-root>

请按以下顺序操作：
1. 首先读取你自己的岗位说明书: ~/.openclaw/workspace/skills/nephesh-studio/roles/<role>.md
2. 读取你的知识库: ~/.openclaw/workspace/skills/nephesh-studio/learning/<role>.md
3. 读取全局工具配置: ~/.openclaw/workspace/TOOLS.md
4. [这里放具体任务描述]
5. 完成后结束会话。
```

## 完整 JSON 调用示例（飞书渠道）

工具：`sessions_spawn`

```json
{
  "runtime": "subagent",
  "mode": "run",
  "thread": false,
  "cleanup": "keep",
  "label": "<project-name>-<role-name>[-<suffix>]",
  "task": "完整任务描述，所有路径使用绝对路径 + 项目根目录绝对路径说明",
}
```

## 参数说明（按官方文档）

| 参数 | 必填 | 飞书固定值 | 官方默认 | 说明 |
|------|------|------------|----------|------|
| `runtime` | 是 | `subagent` | `subagent` | 运行时类型 |
| `mode` | 否 | `run` | `run` | 运行模式 |
| `thread` | 否 | `false` | `false` | 线程绑定（飞书不支持） |
| `cleanup` | 否 | `keep` | `keep` | 清理策略 |
| `label` | 是 | `<project-name>-<role-name>[-<task-description>-<issue-name>]` | - | 日志标签，规则：
- **首次调用**：`项目名-角色名`
- **同项目同角色多次调用**：`项目名-角色名-任务描述-issue名称`
这样侧边栏能清晰区分不同轮次任务，便于识别排查 |
| `task` | 是 | - | - | 任务描述 |

## 执行规则

1. 任何新任务 → 执行一次 `sessions_spawn`
2. 子任务独立运行，完成后自动通告结果回主会话
3. 子会话在 `agents.defaults.subagents.archiveAfterMinutes`（默认 60 分钟）后自动归档

**版本：v3.0 (2026-04-04)**
