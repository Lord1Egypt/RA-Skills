---
name: live-script-planner
description: 根据用户输入（产品、目标、直播类型等）生成专业的直播间口播、互动和逼单脚本。支持参数化调用，可指定带货类/种草类/品牌宣讲类等不同风格。
---

# SKILL.md for live-script-planner

## Description

这是一个参数化的直播脚本策划技能，可根据用户传入的参数生成不同风格的直播话术方案。支持**带货类**、**种草类**、**品牌宣讲类**等多种直播类型。

## Core Parameters

| 参数名 | 必填 | 说明 |
|---|---|---|
| `live_stream_type` | 否 | 直播类型 (带货类/种草类/品牌宣讲类) |
| `product_name` | 是 | 产品名称 |
| `key_selling_points` | 是 | 核心卖点（3-5 个） |
| `promotional_details` | 是 | 优惠信息 |
| `live_stream_duration` | 否 | 直播时长 (e.g., 60 分钟) |

## Dependencies

- `prompt_template.txt` - 核心提示词模板
