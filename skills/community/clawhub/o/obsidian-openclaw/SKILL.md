---
name: obsidian-master
description: Obsidian 大师级配置助手 - 基于三大 YouTube 频道教程，提供完整的 Obsidian 配置、插件推荐、模板系统、AI 集成（Claude/OpenClaw/Gemini）和知识管理最佳实践。
author: Don brand
version: 1.0.0
license: MIT
tags:
  - obsidian
  - knowledge-management
  - note-taking
  - ai-integration
  - openclaw
  - claude
  - gemini
  - productivity
generatedBy: OpenClaw with Qwen3.5-plus
createdAt: 2026-03-05
updatedAt: 2026-03-05
source:
  - https://www.youtube.com/@linkingyourthinking
  - https://www.youtube.com/@JasonEfficiencyLab
  - https://www.youtube.com/@sandox
---

# Obsidian Master Skill

基于三大 YouTube 频道（Linking Your Thinking、Jason Efficiency Lab、清单控沙牛）的完整教程，提供 Obsidian 大师级配置方案。

## 功能特性

### 📚 核心功能

1. **文件夹架构建议** - PARA 方法的 Obsidian 实现
2. **插件推荐与配置** - 官方 + 社区插件完整清单
3. **模板系统** - 每日笔记、读书笔记、项目笔记模板
4. **Bases 数据库配置** - Obsidian 1.10 新功能完整指南
5. **AI 集成方案** - Claude Skill + OpenClaw + Gemini 3
6. **学习路径规划** - 4 周从入门到精通

### 🤖 AI 集成

- **Claude Skill** - 笔记总结、扩展、翻译、改进
- **OpenClaw 联动** - Telegram/微信消息自动整理到 Obsidian
- **Gemini 3** - 系统指令、避免幻觉、高级技巧
- **记忆系统** - 自动写入 `memory/` 目录

### 📊 数据库配置

- 任务管理数据库（状态/优先级/截止日期）
- 知识库数据库（分类/掌握程度/复习时间）
- 多视图支持（表格/看板/日历/画廊）

## 使用方法

### 快速启动

```bash
# 安装 skill
clawhub install obsidian-master

# 使用 skill
openclaw ask "帮我配置 Obsidian"
openclaw ask "推荐 Obsidian 插件"
openclaw ask "创建每日笔记模板"
```

### 可用命令

| 命令 | 描述 |
|------|------|
| `obsidian setup` | 获取完整配置指南 |
| `obsidian plugins` | 获取插件推荐清单 |
| `obsidian templates` | 获取模板系统 |
| `obsidian ai` | 获取 AI 集成方案 |
| `obsidian workflow` | 获取 AI 工作流配置 |
| `obsidian checklist` | 获取配置检查清单 |

### 配置文件

Skill 会生成以下配置文件到你的工作区：

- `Obsidian 核心技巧与完整配置指南.md` - 完整配置文档
- `memory/topics/系统配置与规则.md` - OpenClaw 记忆配置
- `memory/topics/日程与计划.md` - 任务管理配置
- `memory/topics/项目开发.md` - 项目管理配置
- `memory/topics/主人偏好与习惯.md` - 个人偏好配置

## 技术规格

### 系统要求

- Obsidian 1.10+
- Node.js v22.12+
- OpenClaw v2026.3.2+
- （可选）Claude API Key
- （可选）Google AI Studio API Key

### 依赖项

- OpenClaw Core
- （可选）Claude Skill
- （可选）OpenClaw Gateway

## 学习资源

### 视频教程

| 频道 | 订阅者 | 特色 |
|------|--------|------|
| [Linking Your Thinking](https://www.youtube.com/@linkingyourthinking) | 31.6 万 | LYT 方法论、知识管理理论 |
| [Jason Efficiency Lab](https://www.youtube.com/@JasonEfficiencyLab) | 2.04 万 | AI 工具实战、OpenClaw 部署 |
| [清单控沙牛](https://www.youtube.com/@sandox) | 6,370 | 新功能教程、Bases 数据库 |

### 推荐学习路径

1. **第 1 周** - 基础入门（安装、基础语法、每日笔记）
2. **第 2-3 周** - 进阶提升（Bases 数据库、插件配置）
3. **第 4 周** - AI 集成（Claude Skill、OpenClaw 联动）
4. **持续** - 系统优化（定期回顾、模板优化）

## 配置示例

### 文件夹架构

```
📁 Vault/
├── 📁 00-Inbox/           # 收集箱
├── 📁 01-Daily/           # 日记
├── 📁 02-Areas/           # 责任领域
├── 📁 03-Projects/        # 项目
├── 📁 04-Resources/       # 资源库
├── 📁 05-Archives/        # 归档
├── 📁 99-System/          # 系统配置
└── 📁 memory/             # OpenClaw 记忆
```

### 每日笔记模板

```markdown
---
date: {{date}}
tags: [日记/每日]
---

# {{date:YYYY 年 MM 月 DD 日}}

## 📅 今日计划
- [ ] 

## 📝 今日记录

## 🧠 今日想法

## 📚 今日学习

## ✅ 今日完成
- [ ] 

## 🔄 明日计划
- [ ] 
```

### OpenClaw 配置

```json
{
  "agents": {
    "defaults": {
      "compaction": {
        "mode": "safeguard",
        "memoryFlush": {
          "enabled": true
        }
      }
    }
  },
  "channels": {
    "telegram": {
      "systemPrompt": "Identity: Obsidian Master Assistant. Mode: /nothink.",
      "disableAudioPreflight": true
    }
  }
}
```

## 检查清单

### 基础配置（30 分钟）
- [ ] 安装 Obsidian 1.10+
- [ ] 创建 Vault 文件夹
- [ ] 设置基础文件夹架构
- [ ] 启用官方核心插件
- [ ] 创建每日笔记模板

### 本周完成（2-3 小时）
- [ ] 安装社区插件（Dataview、Templater 等）
- [ ] 配置 Bases 数据库
- [ ] 创建项目/读书笔记模板
- [ ] 设置 iCloud 同步

### 本月完成（持续优化）
- [ ] 配置 OpenClaw 联动
- [ ] 设置 AI 自动化工作流
- [ ] 完善记忆系统
- [ ] 定制 CSS 主题

## 故障排除

### 常见问题

| 问题 | 解决方案 |
|------|----------|
| 插件无法安装 | 检查网络连接，使用镜像源 |
| 模板不生效 | 检查模板文件夹路径配置 |
| AI 无响应 | 检查 API Key 有效性 |
| 同步冲突 | 使用 iCloud/云同步的版本控制 |

### 诊断命令

```bash
# 检查 OpenClaw 状态
openclaw gateway status

# 检查记忆系统
openclaw memory search --query "Obsidian 配置"

# 检查插件状态
openclaw tools list
```

## 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

MIT License - 详见 LICENSE 文件

## 致谢

- [Nick Milo](https://www.youtube.com/@linkingyourthinking) - LYT 方法论创始人
- [Jason Efficiency Lab](https://www.youtube.com/@JasonEfficiencyLab) - AI 工具实战教程
- [清单控沙牛](https://www.youtube.com/@sandox) - 中文 Obsidian 教程
- [Obsidian 官方团队](https://obsidian.md) - 出色的笔记软件

## 更新日志

### v1.0.0 (2026-03-05)
- 初始版本发布
- 包含完整的 Obsidian 配置指南
- 集成 OpenClaw 记忆系统
- 提供 AI 工作流配置方案
- 包含三大 YouTube 频道教程汇总

---

**Skill ID:** `obsidian-master`  
**版本:** `1.0.0`  
**最后更新:** `2026-03-05`
