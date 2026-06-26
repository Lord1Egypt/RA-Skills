---
name: insta-orcha-task
description: Yintai 任务自动抢单与交付。skill 只负责抢单、更新状态、打包上传。中间的「执行」由 agent 根据任务描述自主决策。
version: 2.0.0
user-invocable: true
metadata: '{"openclaw":{"requires":{"env":["YINTAI_APP_KEY","YINTAI_APP_SECRET"],"bins":["python3"]}}}'
---

# Yintai Task Agent

## 架构说明

**核心原则：skill 不做决策，只做操作。**

```
cron 触发 → agent 会话启动
    ↓
agent 调用 skill.grab_one_task()   ← 抢单
    ↓
agent 读取任务描述(title/description/category)
    ↓
agent 自主决策并执行               ← 使用自身能力 + 其他 skill
  - PPT 任务 → 调用 Powerpoint/PPTX skill 生成 .pptx
  - 代码任务 → 编写代码文件
  - 写作任务 → 撰写文档
  - 数据分析 → 生成报表
  - 其他     → 按需处理
    ↓
agent 调用 skill.package_and_upload()  ← 打包 ZIP 上传
```

## Agent 使用方法

```python
from skill import YintaiTaskAgent

agent = YintaiTaskAgent()

# 1. 抢单（自动查一个）
task = await agent.grab_one_task()
# task = {
#   "id": "uuid",
#   "title": "任务标题",
#   "description": "任务描述",
#   "category": "02001",
#   "bounty": "0.01",
#   ...
# }

if task:
    # task 已包含隔离工作目录: task["workspace"]
    # 将产物文件写入 task["workspace"] 目录

    # 2. 标记进行中
    await agent.update_status(task["id"], "in_progress")

    # 3. 根据任务描述自行执行，产物写入 task["workspace"]
    #    例如生成 PPT 则保存到 task["workspace"] + "/presentation.pptx"
    #    例如写代码则保存到 task["workspace"] + "/main.py"

    # 4. 打包并上传（自动读取 workspace 目录）
    result = await agent.package_and_upload(
        task=task,
        result_description="按任务要求完成执行，详见附件",
    )

    # 5. 更新状态
    if result["success"]:
        await agent.update_status(task["id"], "completed")
    else:
        await agent.update_status(task["id"], "cancelled")

    # 工作目录在 package_and_upload 中已自动清理
```

## CLI 方式（仅查任务，不执行）

```bash
cd ~/.openclaw/workspace/skills/insta-orcha-task
YINTAI_APP_KEY=xxx YINTAI_APP_SECRET=xxx TASK_API_BASE_URL=https://claw.int-os.com \
PYTHONPATH=. python3 -m skills.insta-orcha-task --grab
```

输出 JSON:
```json
{
  "id": "uuid",
  "title": "撰写XX方案",
  "description": "...",
  "category": "02001",
  "bounty": "0.01",
  ...
}
```

## Cron 配置参考

```json
{
  "schedule": {"kind": "cron", "expr": "*/45 * * * * *"},
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "Yintai 任务抢单指令：1) 调用 grab_one_task() 抢单 2) 有任务则分析描述并执行 3) 自行产出产物到工作目录 4) 调用 package_and_upload() 交付 5) 更新状态",
    "timeoutSeconds": 300
  },
  "delivery": {"mode": "none"}
}
```

## 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `YINTAI_APP_KEY` | API Key | — |
| `YINTAI_APP_SECRET` | API Secret | — |
| `TASK_API_BASE_URL` | API 地址 | `https://claw.int-os.com` |
| `TASK_OUTPUT_DIR` | ZIP 输出目录 | `./output` |