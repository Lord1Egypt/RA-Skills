---
name: lossless-claw
description: 无损回忆技能。对对话或会话记录做本地蒸馏，提取身份信息、偏好、任务和长期知识，剔除噪声并保留可追溯日志。
---

# Lossless Claw

通过“短期全量记录 + 长期结构化沉淀”实现无损回忆。

## 工作流

1. 读取会话文本或日志
2. 提取身份、偏好、任务、知识
3. 将原始内容保留到短期日志
4. 将高价值内容提升到长期层
5. 生成可追溯摘要

## 推荐命令

```bash
python3 scripts/personal_ai_memory.py distill --input /path/to/session.md
python3 scripts/personal_ai_memory.py distill --input /path/to/session.md --apply
```

## 输出目标

- 重要内容永久固化
- 无效噪声不进入长期层
- 保留完整短期回溯链路
