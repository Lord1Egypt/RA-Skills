"""Grab one Yintai task and print JSON result."""
import os
os.environ.setdefault("YINTAI_APP_KEY", "ak_6ecb8c01b061ea710451d61e6df8982e")
os.environ.setdefault("YINTAI_APP_SECRET", "a09c7ea62ad8f5588d3ade4d9846929bc2bd25c6840216ad1a60db83bbf0f109")
os.environ.setdefault("TASK_API_BASE_URL", "https://claw.int-os.com")
os.environ.setdefault("TASK_OUTPUT_DIR", "/tmp/yintai_output")

import asyncio, json
from skill import YintaiTaskAgent

async def run():
    agent = YintaiTaskAgent()
    task = await agent.grab_one_task()
    if task:
        print(json.dumps(task, ensure_ascii=False, indent=2))
    else:
        print(json.dumps({"status": "no_task"}))

asyncio.run(run())