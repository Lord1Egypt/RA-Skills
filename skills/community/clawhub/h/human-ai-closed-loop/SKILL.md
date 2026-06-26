---
name: human-ai-closed-loop
version: 1.0.0
author: KingOfZhao
description: 人机闭环认知 Skill —— AI 整理清单→人类实践证伪→想象力注入→AI 结构化输出的持续进化循环
tags: [cognition, human-ai, closed-loop, feedback, evolution, collaboration]
license: MIT
homepage: https://github.com/KingOfZhao/AGI_PROJECT
---

# Human-AI Closed Loop Cognition Skill

## 元数据

| 字段       | 值                              |
|------------|-------------------------------|
| 名称       | human-ai-closed-loop           |
| 版本       | 1.0.0                          |
| 作者       | KingOfZhao                     |
| 发布日期   | 2026-03-31                     |
| 置信度     | 96%                            |

## 核心能力

实现四阶段人机闭环持续进化：

```
Phase 1: AI 整理清单
  └─ 将任务分解为「已验证事实」+「待证伪假设」+「未知盲区」

Phase 2: 人类实践证伪
  └─ 人类在真实世界运行清单，收集反例和边界条件

Phase 3: 人类想象力注入
  └─ 人类输入直觉、经验、创意（AI 无法独立产生的洞见）

Phase 4: AI 结构化输出
  └─ 吸收人类输入，更新世界模型，输出升级版清单
  └─ 置信度重新标注，循环开始下一轮
```

## 安装命令

```bash
clawhub install human-ai-closed-loop
# 或手动安装
cp -r skills/human-ai-closed-loop ~/.openclaw/skills/
```

## 调用方式

```python
from skills.human_ai_closed_loop import HumanAIClosedLoop

loop = HumanAIClosedLoop(workspace=".", session_id="project_xyz")

# Phase 1: AI 整理清单
checklist = loop.generate_checklist(task="优化包装生产线良率")

# Phase 4: 人类反馈注入后重新输出
loop.inject(
    falsified=["假设A在高温下失效"],
    imagination=["可以用声波检测替代视觉检测"],
    new_facts=["供应商B的纸板厚度偏差达到±0.3mm"]
)
updated = loop.synthesize()
print(updated.confidence, updated.checklist_v2)
```
