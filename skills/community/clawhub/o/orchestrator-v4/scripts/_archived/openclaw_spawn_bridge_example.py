"""
openclaw_spawn_bridge_example.py

示例：在宿主（OpenClaw agent / 运行时包装层）里，把真实 sessions_spawn
以 async 函数形式注入给 orchestrator-v4。

注意：这个脚本本身只是桥接示例，不能在纯 Python 里直接调用聊天工具。
必须由拥有 `sessions_spawn` 工具权限的宿主来传入真实实现。
"""

import asyncio
from orchestrator_v4_acp import create_orchestrator


async def run_with_spawn_bridge(user_text: str, sessions_spawn_func):
    """
    sessions_spawn_func 需要是一个 async callable，签名等价于：
        await sessions_spawn_func(**payload) -> dict | str

    典型 payload：
        runtime="subagent"
        agentId="main"
        label="slow-worker-xxxx"
        mode="run"
        task="..."
        timeoutSeconds=300
        runTimeoutSeconds=300
        cleanup="delete"
        sandbox="inherit"
        cwd="..."
        model="..."           # 可选
        thinking="off"        # 可选
    """
    orch = await create_orchestrator(
        spawn_func=sessions_spawn_func,
        subagent_agent_id="main",
        subagent_thinking="off",
        subagent_cleanup="delete",
        subagent_sandbox="inherit",
    )
    try:
        return await orch.handle(user_text, mode="slow")
    finally:
        await orch.stop(graceful=False)


# ===== 下面是纯本地调试示例（不会真的 spawn） =====

async def fake_sessions_spawn(**payload):
    return {
        "accepted": f"[fake spawn ok] label={payload.get('label')} timeout={payload.get('timeoutSeconds')}"
    }


async def _demo():
    response = await run_with_spawn_bridge("设计一个分布式任务队列", fake_sessions_spawn)
    print(response.content)


if __name__ == "__main__":
    asyncio.run(_demo())
