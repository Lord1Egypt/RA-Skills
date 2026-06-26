---
name: medical-doctor-matcher
slug: medical-doctor-matcher
version: 0.1.0
description: 当用户需要根据主诉、病史、地区和就诊偏好，推荐最合适的医院与医生，并在可行时生成模拟挂号与陪诊安排时使用。
metadata:
  openclaw:
    skillKey: medical-doctor-matcher
    category: healthcare
    tags:
      - healthcare
      - doctor-matching
      - hospital-recommendation
      - appointment
      - escort
---

# 医疗就诊匹配助手

## Overview
把用户的主诉、病史、年龄、地区、就诊偏好转成结构化画像，完成科室判断、医院筛选、医生匹配、Top 3 推荐，并在有需要时生成模拟挂号和陪诊安排。

## When to Use
在下面场景触发本技能：
1. 用户说不清该去哪个医院、哪个科、哪个医生。
2. 用户给出症状、病史、检查结果，希望获得就诊建议与医生推荐。
3. 用户希望按地区、医院等级、可挂号时间、是否需要陪诊做联合筛选。
4. 用户需要自动挂号或陪诊安排的模拟流程。

不要在下面场景单独依赖本技能：
1. 明显急危重症：胸痛持续加重、呼吸困难、意识障碍、大出血、抽搐、卒中征象。此时先建议急诊/120。
2. 用户要求明确诊断、处方、治疗方案。本技能只做就医分流与匹配，不替代医生诊疗。
3. 缺少最基本的主诉或地区信息且无法合理补全时。

## Quick Workflow
1. 先收集信息：主诉、持续时间、病史、过敏史、年龄、性别、地区、预算、是否要挂号、是否要陪诊。
2. 参考 `references/symptom_to_specialty.md` 完成科室初筛与风险识别。
3. 需要可执行演示时，使用 `scripts/recommend.py` 读取输入 JSON 与 `data/` 下模拟数据，输出 Top 3 推荐。
4. 输出必须包含：推荐理由、医院信息、医生信息、匹配分、风险提示、是否已生成模拟挂号/陪诊安排。
5. 若用户症状涉及急危重症，先给风险提示，再提供急诊方向，不做普通门诊优先推荐。

## Core Rules
1. 始终先做风险分层，再做医院与医生匹配。
2. 不把“推荐医院/医生”表达成“已经完成诊断”。
3. 推荐结果至少给 3 个选项，且说明为什么排在前面。
4. 当地区信息不足时，优先询问或使用用户提供的城市/区域；没有时只能给出“示例推荐”。
5. 自动挂号与陪诊在本技能中默认是模拟流程，除非你已经接入真实挂号/陪诊 API。
6. 输出时优先使用结构化格式，参考 `schemas/response_schema.json`。
7. 需要更详细的匹配规则时，按需读取 `references/` 下文档，不要把全部规则一次性塞进回答。

## Bundled Files
| 文件 | 用途 |
|---|---|
| `references/workflow.md` | 完整工作流与交互步骤 |
| `references/symptom_to_specialty.md` | 症状到科室映射与风险规则 |
| `references/output_template.md` | 建议输出模板 |
| `schemas/request_schema.json` | 输入结构 |
| `schemas/response_schema.json` | 输出结构 |
| `data/*.json` | 模拟医院、医生、号源、陪诊数据 |
| `scripts/recommend.py` | 基于模拟数据生成推荐、挂号、陪诊结果 |

## Recommended Output Sections
1. 用户病情摘要
2. 风险等级与建议
3. 推荐科室
4. Top 3 医院医生推荐
5. 模拟挂号结果（如需要）
6. 模拟陪诊安排（如需要）
7. 注意事项

## Example Trigger
- “我发烧咳嗽三天，在朝阳区，应该挂哪个医院哪个医生？”
- “妈妈膝盖痛半年了，想在海淀区找骨科专家，并且最好这两天能挂上号。”
- “小孩反复发热，帮我找儿科医院和医生，顺便安排陪诊。”
