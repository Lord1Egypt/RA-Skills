---
name: memory-work
version: 2.0.0
description: An AI-first knowledge management system with evolvable memory - 一套 AI 时代的注意力保护架构
homepage: https://github.com/yiliqi78/memory-work
author: yiliqi78
license: MIT
---

# Memory Work v2

**一套 AI 时代的注意力保护架构**

## 概述

Memory Work 是一个 AI 优先的知识管理系统，具有可进化的记忆架构。它解决了当面对多个并行项目时传统 AI 助手的问题：

### 核心问题
- **AI 失忆**：每次对话从零开始，需要反复提供上下文
- **用户成为瓶颈**：需要自己结构化、录入和维护信息
- **知识库负担**：库越大，管理成本越高

### 解决方案
Memory Work 反转了这个流程：
- 想法 → **直接口述** → AI 结构化 → AI 维护
- AI 启动时自动读取分层文件 → **不再失忆**
- 分区代理 → **可扩展到任意规模**

**你只负责两件事：提供注意力焦点，做创意决策。**

## 系统架构

### 核心文件
1. **MEMORY.md** - 长期记忆文件
2. **USER.md** - 用户配置文件
3. **SOUL.md** - 身份/灵魂文件
4. **CLAUDE.md** - Claude AI 配置文件

### 分区结构
- **00 Focus Zone** - 注意力焦点区域
- **01 Materials** - 材料收集
- **02 Tools** - 工具库
- **06 Skills** - 技能库

### 技能系统
Skills 是可执行的能力模块，比静态工具更强大：
- 运行脚本或命令
- 生成输出（日历、报告、分析）
- 触发工作流或流程
- 管理系统操作
- 集成外部服务

## 安装与使用

### 首次运行
克隆仓库后，AI 会自动：
1. 检测到这是全新安装
2. 询问你的偏好语言（中文 / English）
3. 收集你的基本信息，创建用户档案

### 日常使用
1. **设置焦点**：在 00 Focus Zone 中设置当前工作焦点
2. **收集材料**：在 01 Materials 中收集相关材料
3. **使用工具**：在 02 Tools 中使用预置工具
4. **执行技能**：在 06 Skills 中运行自动化技能

## 安全说明

### 访问权限
这个技能需要访问以下核心文件：
- `MEMORY.md` - OpenClaw 长期记忆
- `USER.md` - 用户信息
- `SOUL.md` - 身份文件

### 风险评估
- **风险等级**: 🟡 MEDIUM
- **原因**: 需要访问敏感记忆文件
- **缓解**: 这是记忆管理系统的核心功能，代码透明

### 用户授权
安装此技能表示你授权它：
1. 读取现有的记忆文件
2. 更新记忆文件以记录新信息
3. 管理分层记忆结构

## 许可证
MIT License - 详见 LICENSE 文件

## 反馈与贡献
- GitHub: https://github.com/yiliqi78/memory-work
- Issues: 报告问题或建议功能
- Pull Requests: 欢迎贡献代码

## 相关技能
- `skill-vetter` - 安全检测技能
- `skill-install-manager` - 安全安装管理器
- `obsidian` - Obsidian 笔记管理