# Orchestrator

智能任务编排系统，让 AI Agent 具备多线程工作能力。

## 功能

- 自动扫描项目规模（文件数、行数、体积）
- 智能规划子任务数量和拆分策略
- 三级 Worker 路由（Fast / Slow / Long）
- 大项目按模块拆分，自适应超时
- 子代理文件读取约束，防止超时
- 并发限流、失败自动重试（指数退避）
- 审计质检、暂停/恢复/改思路
- OpenClaw Bridge 桥接层，一键规划+派发

## 安装

```bash
clawhub install orchestrator-v4
```

或手动复制到 OpenClaw workspace 的 `skills/` 目录。

## 使用

```python
from openclaw_bridge import run_orchestrated_task

result = await run_orchestrated_task(
    task="分析这个项目的架构",
    target_dir="/path/to/project",
    sessions_spawn_func=sessions_spawn,
    max_parallel=5,
)
```

详细使用说明见 [SKILL.md](SKILL.md)。

## 文件结构

```
scripts/
  openclaw_bridge.py          # OpenClaw 主会话桥接层
  orchestrator_v4_acp.py      # 主控（扫描+规划+路由+审计+追踪）
  lifecycle_manager.py        # 进程生命周期管理
  background_monitor.py       # 后台监控（心跳、超时）
  micro_scheduler.py          # 微调度器（优先级、DAG 依赖）
  v3_bridge.py                # 长任务桥接（JSON Line IPC）
  v3_worker.py                # 长任务 Worker 子进程
  audit_agent.py              # 审计子代理
  hybrid_worker_acp.py        # 混合 Worker 模板
  openclaw_orchestrator_entry.py  # 统一入口
```

## License

MIT
