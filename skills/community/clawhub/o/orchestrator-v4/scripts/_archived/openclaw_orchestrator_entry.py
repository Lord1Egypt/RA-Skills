"""
openclaw_orchestrator_entry.py

给 OpenClaw 宿主直接调用的入口封装：
- 自动把真实 sessions_spawn 注入 orchestrator-v4
- 暴露所有配置项（含新模块配置）
- 向后兼容（所有新参数都有默认值）

用法（宿主伪代码）：
    from openclaw_orchestrator_entry import run_orchestrator_request
    response = await run_orchestrator_request(
        user_text="设计一个分布式任务队列",
        sessions_spawn_func=sessions_spawn,
        request_type="general",
    )
    print(response.content)
"""

from orchestrator_v4_acp import create_orchestrator


async def run_orchestrator_request(
    user_text: str,
    sessions_spawn_func,
    *,
    # 原有配置
    mode: str = "slow",                          # fast / slow / auto
    request_type: str = "general",               # general / code / debug / research
    subagent_agent_id: str = "main",             # 子 agent 使用的 agent ID
    subagent_model: str = "",                    # 子 agent 模型，空=默认
    subagent_thinking: str = "off",              # on / off / auto
    subagent_cleanup: str = "delete",            # delete / keep
    subagent_sandbox: str = "inherit",           # inherit / require
    checkpoint_dir: str = "./checkpoints",       # checkpoint 保存目录
    # 新增：并发与超时
    max_parallel_subagents: int = 3,             # 最大并行 subagent 数
    complex_slow_timeout: float = 600.0,         # 复杂任务超时（秒）
    # 新增：生命周期管理
    enable_lifecycle_manager: bool = True,        # 启用进程生命周期管理
    restart_policy: str = "on_failure",           # never / on_failure / always
    max_restarts: int = 3,                        # 最大重启次数
    # 新增：后台监控
    enable_background_monitor: bool = True,       # 启用后台监控
    # 新增：微调度器
    enable_micro_scheduler: bool = False,         # 启用微调度器（多任务并发）
    scheduler_max_concurrent: int = 3,            # 调度器最大并发数
    # 新增：V3 桥接 / 长任务
    enable_v3_bridge: bool = False,               # 启用 V3 桥接（长任务）
    # 新增：审计
    enable_audit: bool = False,                    # 启用审计子代理
    audit_on_code_tasks: bool = True,              # 代码类任务自动审计
    audit_timeout: float = 120.0,                  # 审计超时（秒）
):
    """
    执行编排器请求的统一入口。
    
    Args:
        user_text: 用户输入的文本
        sessions_spawn_func: OpenClaw 的 sessions_spawn 函数（async callable）
        mode: 执行模式 - fast(当前会话直答) / slow(spawn子agent) / auto(自动判断)
        request_type: 请求类型 - general / code / debug / research
        subagent_agent_id: 子 agent 的 agent ID
        subagent_model: 子 agent 使用的模型，空字符串表示默认
        subagent_thinking: 子 agent 思考模式
        subagent_cleanup: 子 agent 清理策略
        subagent_sandbox: 子 agent 沙盒模式
        checkpoint_dir: checkpoint 保存目录
        max_parallel_subagents: 最大并行 subagent 数量
        complex_slow_timeout: 复杂 slow 任务超时（秒）
        enable_lifecycle_manager: 是否启用进程生命周期管理
        restart_policy: 重启策略
        max_restarts: 最大重启次数
        enable_background_monitor: 是否启用后台监控
        enable_micro_scheduler: 是否启用微调度器
        scheduler_max_concurrent: 调度器最大并发数
        enable_v3_bridge: 是否启用 V3 桥接
    
    Returns:
        OrchestratorResponse
    """
    orch = await create_orchestrator(
        spawn_func=sessions_spawn_func,
        subagent_agent_id=subagent_agent_id,
        subagent_model=subagent_model,
        subagent_thinking=subagent_thinking,
        subagent_cleanup=subagent_cleanup,
        subagent_sandbox=subagent_sandbox,
        checkpoint_dir=checkpoint_dir,
        max_parallel_subagents=max_parallel_subagents,
        complex_slow_timeout=complex_slow_timeout,
        enable_lifecycle_manager=enable_lifecycle_manager,
        restart_policy=restart_policy,
        max_restarts=max_restarts,
        enable_background_monitor=enable_background_monitor,
        enable_micro_scheduler=enable_micro_scheduler,
        scheduler_max_concurrent=scheduler_max_concurrent,
        enable_v3_bridge=enable_v3_bridge,
        enable_audit=enable_audit,
        audit_on_code_tasks=audit_on_code_tasks,
        audit_timeout=audit_timeout,
    )
    try:
        return await orch.handle(user_text, mode=mode, request_type=request_type)
    finally:
        await orch.stop(graceful=False)


if __name__ == "__main__":
    import asyncio

    async def test():
        print("=== 入口文件测试 ===")
        
        # 模拟 spawn 函数
        async def fake_spawn(**kw):
            return {"status": "accepted", "childSessionKey": "test-key"}
        
        resp = await run_orchestrator_request(
            user_text="你好",
            sessions_spawn_func=fake_spawn,
            mode="fast",
            max_parallel_subagents=5,
            enable_lifecycle_manager=True,
            enable_micro_scheduler=False,
        )
        print(f"响应: mode={resp.worker_mode}, content={resp.content[:50]}")
        print("=== 测试通过 ===")
    
    asyncio.run(test())
