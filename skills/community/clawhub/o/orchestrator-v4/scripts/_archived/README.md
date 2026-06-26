# _archived/

这些模块当前未被使用，但设计完整，等 OpenClaw 开放 Python SDK 后可直接启用。

## 模块清单

| 文件 | 功能 | 启用条件 |
|------|------|---------|
| lifecycle_manager.py | 进程生命周期（重启策略、指数退避） | Python SDK + 长驻进程模式 |
| background_monitor.py | 后台监控（心跳、超时、告警） | Python SDK + 长驻进程模式 |
| micro_scheduler.py | 微调度器（优先级、DAG 依赖） | Python SDK + 复杂任务链 |
| v3_bridge.py | 长任务桥接（JSON Line IPC） | >30 分钟任务 |
| v3_worker.py | 长任务 Worker 子进程 | 配合 v3_bridge |
| audit_agent.py | 审计子代理（PASS/REJECT 质检） | Python SDK + enable_audit |
| hybrid_worker_acp.py | 混合 Worker（Fast/Slow 模板） | Python SDK |
| openclaw_bridge.py | OpenClaw 桥接层 | Python SDK |
| openclaw_orchestrator_entry.py | 统一入口 | Python SDK |
| openclaw_spawn_bridge_example.py | spawn_func 注入示例 | 参考用 |

## 恢复方式

这些文件从 git 历史 (commit ab5271b) 恢复。如需重新启用：
```bash
mv _archived/*.py ../
```

归档时间：2026-04-05
