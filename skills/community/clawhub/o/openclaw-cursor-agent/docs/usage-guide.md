# OpenClaw Cursor Agent 使用指南

## 一句话理解

你把 OpenClaw 当成项目经理，对它说需求，它会在后台调度 Cursor 去干活。

## 当前架构

```text
你（飞书/聊天） → OpenClaw Agent → 插件 → WSL Debian → tmux → Cursor CLI Agent
```

你不需要关心 tmux、WSL、agent 这些底层概念，直接用自然语言说需求即可。

## 你可以这么说

### 启动后台任务

- 帮我用 Cursor 在后台做一个任务：给项目补 README，不要动其他文件。
- 用 Cursor 后台在 `D:/project/openclaw` 里实现 JWT 登录接口。

### 查看任务进度

- 看看刚才那个 Cursor 任务做到哪了。
- 把刚才那个任务的最新输出给我看一下。

### 给任务补充要求

- 告诉刚才那个 Cursor 任务：JWT 改成 RS256。
- 让它先别写测试，先把接口实现完。

### 暂停 / 恢复 / 结束

- 先暂停刚才那个 Cursor 任务。
- 恢复刚才那个 Cursor 任务。
- 把刚才那个 Cursor 任务停掉。

## 完整使用流程

1. 说需求 → OpenClaw 启动 Cursor 后台任务
2. 随时追问进度
3. 中途补充要求
4. 做完后结束任务

## 给 OpenClaw Agent 的行为规范

当用户说需求时，调用 `cursor_agent_spawn_task`。
当用户问进度时，调用 `cursor_agent_check_status`。
当用户补充要求时，调用 `cursor_agent_send_command`。
当用户要停止时，调用 `cursor_agent_kill_session`。
不确定环境是否正常时，先调用 `cursor_agent_doctor`。

不要默认回退到"先装 XXX"——除非 doctor 明确报错。

## 诊断优先级

当不确定环境是否可用时，按这个顺序判断：

1. 插件是否已加载 → `cursor_agent_doctor`
2. shell runner 是否可用
3. `tmux` / `python3` / `agent` 是否可用
4. 运行目录 `status/tasks/logs` 是否存在

不要跳过检查直接下结论。
