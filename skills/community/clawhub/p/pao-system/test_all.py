import asyncio
import aiohttp

async def test_worker(ws_id, ws_name, port):
    url = f'http://localhost:{port}/execute'
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json={
                'task_id': 'test',
                'task_type': 'echo',
                'task_params': {'msg': f'hello from {ws_id}'},
                'sender_ws': 'test'
            }) as resp:
                result = await resp.json()
                return f'{ws_name} ({port}): {result.get("result", {}).get("ws_id", "ERROR")}'
    except Exception as e:
        return f'{ws_name} ({port}): FAIL - {e}'

workers = [
    ('ws_aitest', '智能测试1.0', 8767),
    ('20260324111248', '数据查询与统计', 8768),
    ('20260318105539', '通用Agent能力', 8769),
    ('20260319091421', '智能测试1.0', 8770),
    ('20260325123700', 'Skill孵化工厂', 8771),
    ('20260325123703', 'Skill验证', 8772),
    ('20260401081603', '开发集成', 8773),
    ('20260417103904', '新工作区', 8774),
]

results = asyncio.run(asyncio.gather(*[test_worker(*w) for w in workers]))
print('=' * 60)
print('跨工作区通信测试结果')
print('=' * 60)
for r in results:
    print(r)
print('=' * 60)