---
name: openclaw-doctor
description: 一键检查 OpenClaw 系统健康状态（配置、模型、cron、记忆）
homepage: https://docs.openclaw.ai
metadata: {"clawdbot":{"emoji":"🩺","requires":{"bins":["node"]}}}
---

# 🩺 OpenClaw 健康检查

一键全面检查 OpenClaw 系统状态，发现问题并给出修复建议。

## 检查项目

### 1. 系统状态
- OpenClaw 版本
- Node.js 版本
- 运行时间、内存占用
- Gateway 进程状态

### 2. 配置检查
- 配置文件是否有效（openclaw.json）
- 频道连接状态（飞书/Telegram 等）
- 模型配置是否正确
- 权限设置是否合理

### 3. 模型连通性
- 主模型能否正常响应
- Fallback 模型是否可用
- API Key 是否有效

### 4. 定时任务
- Cron 任务数量和状态
- 最近一次执行是否成功
- 有没有连续失败的任务

### 5. 记忆系统
- MEMORY.md 是否存在
- daily notes 最近更新时间
- TOOLS.md 是否有内容

### 6. 技能加载
- 已安装技能数量
- 技能格式是否正确
- 有没有重复或冲突的技能

## 使用方式

AI 调用步骤：
1. 检查 openclaw.json 配置文件
2. 执行 `openclaw status` 获取系统状态
3. 执行 `openclaw cron list` 查看定时任务
4. 检查 workspace 文件（MEMORY.md, TOOLS.md 等）
5. 汇总结果，给出健康评分（0-100）和修复建议

## 输出格式

```
🩺 OpenClaw 健康检查报告

系统状态：✅/⚠️/❌
- 版本：xxx
- 运行时间：xxx
- 内存：xxx

配置：✅/⚠️/❌
- 频道：xxx
- 模型：xxx

定时任务：✅/⚠️/❌
- 总数：x
- 正常：x
- 异常：x

记忆系统：✅/⚠️/❌

健康评分：xx/100
建议修复：xxx
```

## 注意事项
- 检查时不要修改任何配置
- 发现问题先报告，不要自动修复（除非用户明确要求）
- 敏感信息（API Key 等）用 *** 脱敏
