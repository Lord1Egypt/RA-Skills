"""
Yintai Task Agent — 面向 agent 的抢单与交付接口

使用方式:
    from skill import YintaiTaskAgent

    agent = YintaiTaskAgent()
    task = await agent.grab_one_task()       # 抢单
    await agent.update_status(task_id, "in_progress")
    result = await agent.package_and_upload(  # 打包交付
        task_id, task_title, work_dir, result_description
    )
"""

from skill import YintaiTaskAgent, main

__all__ = ["YintaiTaskAgent", "main"]
__version__ = "2.0.0"