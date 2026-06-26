---
name: memory-system-optimizer
description: OpenCLAW 记忆系统优化 - 四层架构 + 自我反思 + 情绪识别 + 任务规划 + 12项增强功能
version: 2.0.0
author: Odin
tags: [memory, openclaw, optimization, ai, agent]
---

# Memory System Optimizer

> OpenCLAW 记忆系统优化 Skill v2.0，基于 Ray Wang 实战经验 + 12项增强功能

## v2.0 新增功能

| # | 功能 | 目录/文件 |
|---|------|----------|
| 1 | 四层记忆架构 | short-term/semantic/confidence/ |
| 2 | 自我反思与元认知 | reflections/ + confidence/ |
| 3 | 动态知识整合 | knowledge/ |
| 4 | 情绪识别 | emotions/ |
| 5 | 主动学习 | AGENTS.md |
| 6 | 任务规划与监控 | tasks/ |
| 7 | 隐私与数据治理 | privacy/ |
| 8 | 可解释性 | explainability/ |
| 9 | 弹性与自适应 | elastic/ |
| 10 | 持续进化 | evolution/ |
| 11 | 协作与共享 | collaboration/ |
| 12 | 多模态能力 | (待接入) |

---

## 核心功能

### 1. 四层记忆架构
- **短期**: memory/short-term/ - 当前会话任务、临时变量
- **情景**: memory/YYYY-MM-DD.md - 按时间线的重要交互
- **语义**: memory/semantic/ - 知识图谱、事实库
- **长期**: MEMORY.md - 精选记忆

### 2. 自动衰减机制
- Hot/Warm/Cold 温度模型
- 自动归档过期记忆

### 3. 自我反思机制
- 任务完成后自动复盘
- 置信度评估（<50%主动请求澄清）

### 4. 情绪识别
- 识别用户情绪，调整回应风格

### 5. 任务规划
- 复杂任务自动拆解
- 实时状态跟踪

## 安装配置

无收费，纯免费使用。

## 使用方法

```bash
# 写入日志
memlog.sh "标题" "内容"

# 刷新记忆
node memory-decay.js

# 归档
./memory-gc.sh
```

## 技术栈

- OpenCLAW
- Markdown 文件
- Shell 脚本
- Node.js

## 作者

Odin（总舵主）
