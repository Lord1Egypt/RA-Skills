# OpenClaw Hook 配置引导

## 概述

OpenClaw 支持通过 Hook 实现**后台运行模式**（操作后告知用户）。

当启用 Hook 后，MyKnowledge 会在后台自动检测任务并创建知识库，操作完成后会告知用户（不会在用户无感知的情况下悄悄创建文件）。

## Hook 功能

### 自动触发场景

| 事件 | 触发行为 |
|------|----------|
| `message:received` | 分析用户消息，检测复杂任务 |
| 检测到复杂任务 | 自动创建知识库（如不存在） |
| 检测到复杂任务 | 自动创建需求记录 |

### 与意图识别模式的区别

| 模式 | 触发方式 | 用户告知 |
|------|----------|----------|
| **Hook 模式** | 事件驱动，自动触发 | 操作后告知（非无感知） |
| **意图识别模式** | AI 判断后触发 | 操作前提示（AI 先询问再操作） |

## 安装步骤

### 步骤 1：创建 Hook 文件

MyKnowledge 会自动创建以下文件：

```
~/.openclaw/hooks/myknowledge/
├── HOOK.md
└── handler.ts
```

### 步骤 2：启用 Hook

执行命令启用：

```bash
openclaw hooks enable myknowledge
```

### 步骤 3：验证安装

```bash
openclaw hooks list
# 应看到 myknowledge 状态为 enabled
```

## 用户交互流程

```
AI：检测到您使用 OpenClaw，支持后台运行模式（操作后告知）。

     我可以帮您：
     1. 创建 Hook 文件到 ~/.openclaw/hooks/myknowledge/
     2. 您手动启用：openclaw hooks enable myknowledge
     
     启用后，复杂任务将自动记录，操作完成后会告知您。

[创建 Hook 文件] [使用普通模式]

用户：[创建 Hook 文件]

AI：✅ 已创建 Hook 文件
     位置：~/.openclaw/hooks/myknowledge/
     
     请运行：openclaw hooks enable myknowledge
     
     下次对话将自动记录（操作后告知）。
```

## Hook 文件内容

### HOOK.md

```yaml
---
name: myknowledge
version: "1.4.89"
events:
  - message:received
description: |
  MyKnowledge 自动检测 Hook。
  当用户发送消息时，自动分析任务复杂度，
  对复杂任务自动创建知识库和记录需求。
---
```

### handler.ts

```typescript
import type { HookContext, MessageReceivedEvent } from "@openclaw/sdk";

export default async function handler(ctx: HookContext<MessageReceivedEvent>) {
  const { message } = ctx.event;
  
  // 忽略非用户消息
  if (message.role !== "user") return;
  
  // 分析任务复杂度
  const isComplex = analyzeComplexity(message.content);
  
  if (isComplex) {
    // 调用 MyKnowledge 创建知识库
    await ctx.agent.execute("myknowledge", {
      action: "auto_create",
      content: message.content
    });
  }
}

function analyzeComplexity(content: string): boolean {
  const keywords = ["分析", "统计", "挖掘", "开发", "设计", "调研", "整理", "清洗"];
  const count = keywords.filter(kw => content.includes(kw)).length;
  return count >= 2;
}
```

## 管理 Hook

### 查看状态

```bash
openclaw hooks list
```

### 启用/禁用

```bash
openclaw hooks enable myknowledge
openclaw hooks disable myknowledge
```

### 查看详情

```bash
openclaw hooks info myknowledge
```

## 注意事项

1. **Hook 仅对 OpenClaw 有效**
2. **需要手动启用**（安全考虑）
3. **可随时禁用**恢复手动模式
4. **与意图识别模式互斥**（Hook 优先级更高）

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| Hook 未触发 | 检查是否已启用：`openclaw hooks list` |
| 触发频率不符合预期 | 调整灵敏度偏好（参考 settings.yaml），或禁用 Hook |
| 权限错误 | 检查 Hook 文件权限 |
