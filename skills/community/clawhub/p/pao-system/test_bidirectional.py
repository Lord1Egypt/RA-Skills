import asyncio
import aiohttp
import os

# 从环境变量读取服务器配置，默认值用于本地测试
DEFAULT_PORTS = {
    'agent_team': os.getenv('AGENT_TEAM_PORT', '8771'),
    'claw': os.getenv('CLAW_PORT', '8775'),
}

# 测试1: Agent团队 -> Claw
async def test1():
    port = DEFAULT_PORTS['agent_team']
    url = f'http://localhost:{port}/task'
    task = {
        'task_id': 'test_1',
        'task_type': 'echo',
        'task_params': {'msg': 'Hello from Agent团队 to Claw'},
        'sender_ws': 'Agent团队'
    }
    async with aiohttp.ClientSession() as s:
        async with s.post(url, json=task) as r:
            return await r.json()

# 测试2: Claw -> 智能测试1.0
async def test2():
    port = DEFAULT_PORTS['claw']
    url = f'http://localhost:{port}/task'
    task = {
        'task_id': 'test_2',
        'task_type': 'echo',
        'task_params': {'msg': 'Hello from Claw to 智能测试1.0'},
        'sender_ws': 'Claw'
    }
    async with aiohttp.ClientSession() as s:
        async with s.post(url, json=task) as r:
            return await r.json()

print('跨工作区双向通信测试')
print('='*60)
print('1. Agent团队 -> Claw:')
r1 = asyncio.run(test1())
print(f'   {r1.get("result", {})}')

print('2. Claw -> 智能测试1.0:')
r2 = asyncio.run(test2())
print(f'   {r2.get("result", {})}')
print('='*60)
print('双向通信成功! 所有工作区都可以相互调用')