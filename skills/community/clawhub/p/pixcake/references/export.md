# Export

## Overview

该 reference 用于准备并提交 PixCake 导出任务，重点是收口：

- 导出范围
- 导出目录
- 导出结果表达
- 导出任务状态与进度

## Tools

- `get_project_images`
- `batch_export_images`
- `get_task_status`

## Core Rules

- 导出是异步提交，不等于已完成
- 导出前必须明确图片范围
- 导出目录必须是真实路径
- 只有 `get_task_status` 能用于确认导出任务的状态和进度

## Common Flows

### 导出项目图片

1. 先确认目标项目
2. 必要时读取 `get_project_images`
3. 确认导出范围
4. 调用 `batch_export_images`

### 导出指定图片

1. 明确图片范围
2. 必要时读取 `get_project_images`
3. 调用 `batch_export_images`

### 导出到指定目录

1. 先用 shell / command 定位真实目录
2. 路径不明确时继续澄清
3. 再调用 `batch_export_images`

### 查询导出任务状态

1. 先确认任务 ID
2. 调用 `get_task_status`
3. 根据返回状态与进度表达“处理中”或“已完成”

## Out Of Scope

当前不支持：

- 精选导出
- 星标导出
- AI 挑图结果导出
- 依赖未暴露筛选能力的导出

如果用户能明确给出项目或图片范围，可以继续做普通导出；否则停止。

## Guardrails

- 不把“任务已创建”说成“已经导出完成”
- 不在没有 `get_task_status` 返回结果时自行推断导出已完成
- 不在范围不清楚时盲导出整个项目
- 不自己猜导出目录
