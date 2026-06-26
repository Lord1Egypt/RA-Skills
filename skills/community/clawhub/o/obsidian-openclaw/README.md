# Obsidian Master Skill

> Obsidian 大师级配置助手 - 基于三大 YouTube 频道教程的完整配置方案

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://clawhub.com/skills/obsidian-master)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Obsidian](https://img.shields.io/badge/Obsidian-1.10+-purple.svg)](https://obsidian.md)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-2026.3.2+-orange.svg)](https://openclaw.ai)

## 📖 简介

本 Skill 基于三大 YouTube 频道的完整教程，提供 Obsidian 大师级配置方案：

- **Linking Your Thinking** (31.6 万订阅) - LYT 方法论、知识管理理论
- **Jason Efficiency Lab** (2.04 万订阅) - AI 工具实战、OpenClaw 部署
- **清单控沙牛** (6,370 订阅) - 新功能教程、Bases 数据库、中文本地化

## ✨ 特性

### 📚 核心功能

- ✅ 文件夹架构建议（PARA 方法）
- ✅ 插件推荐与配置（官方 + 社区）
- ✅ 模板系统（每日/读书/项目笔记）
- ✅ Bases 数据库配置（Obsidian 1.10 新功能）
- ✅ AI 集成方案（Claude + OpenClaw + Gemini）
- ✅ 学习路径规划（4 周从入门到精通）

### 🤖 AI 集成

- **Claude Skill** - 笔记总结、扩展、翻译、改进
- **OpenClaw 联动** - Telegram/微信消息自动整理
- **Gemini 3** - 系统指令、避免幻觉、高级技巧
- **记忆系统** - 自动写入 `memory/` 目录

### 📊 数据库配置

- 任务管理数据库（状态/优先级/截止日期）
- 知识库数据库（分类/掌握程度/复习时间）
- 多视图支持（表格/看板/日历/画廊）

## 🚀 快速开始

### 安装

```bash
# 使用 clawhub 安装
clawhub install obsidian-master

# 或手动安装
git clone https://github.com/your-username/obsidian-master-skill.git
cp -r obsidian-master-skill ~/.openclaw/skills/
```

### 使用

```bash
# 获取完整配置指南
openclaw ask "帮我配置 Obsidian"

# 获取插件推荐
openclaw ask "推荐 Obsidian 插件"

# 创建模板
openclaw ask "创建每日笔记模板"

# 配置 AI 集成
openclaw ask "配置 OpenClaw 联动 Obsidian"
```

### 命令参考

| 命令 | 描述 |
|------|------|
| `obsidian setup` | 获取完整配置指南 |
| `obsidian plugins` | 获取插件推荐清单 |
| `obsidian templates` | 获取模板系统 |
| `obsidian ai` | 获取 AI 集成方案 |
| `obsidian workflow` | 获取 AI 工作流配置 |
| `obsidian checklist` | 获取配置检查清单 |

## 📁 项目结构

```
obsidian-master-skill/
├── SKILL.md                  # Skill 配置文件
├── README.md                 # 使用说明
├── package.json              # Node.js 配置
├── LICENSE                   # 许可证
├── src/
│   ├── index.js              # 主入口文件
│   ├── config.js             # 配置管理
│   ├── templates.js          # 模板生成
│   └── workflow.js           # AI 工作流
├── references/
│   ├── folder-structure.md   # 文件夹架构参考
│   ├── plugins-list.md       # 插件清单
│   └── templates/            # 模板文件
│       ├── daily-note.md
│       ├── book-note.md
│       └── project-note.md
└── assets/
    └── logo.png              # Skill 图标
```

## 📋 配置示例

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
      "systemPrompt": "Identity: Obsidian Master Assistant.",
      "disableAudioPreflight": true
    }
  }
}
```

## 🎓 学习路径

### 第 1 周 - 基础入门
- 安装 Obsidian 1.10+
- 学习基础语法（标题、列表、链接、标签）
- 创建每日笔记模板
- 观看 [Obsidian for Beginners](https://www.youtube.com/watch?v=QgbLb6QCK88)

### 第 2-3 周 - 进阶提升
- 配置核心插件（Dataview、Templater 等）
- 建立文件夹架构
- 学习双向链接和块引用
- 观看 [Bases 数据库教程](https://www.youtube.com/watch?v=LWkYBmCFM-w)

### 第 4 周 - AI 集成
- 安装 OpenClaw
- 配置 Claude Skill
- 设置 AI 自动化工作流
- 学习 Gemini 3 高级技巧

### 持续优化
- 定期回顾整理笔记
- 优化模板系统
- 完善数据库配置
- 学习新功能

## ✅ 检查清单

### 基础配置（30 分钟）
- [ ] 安装 Obsidian 1.10+
- [ ] 创建 Vault 文件夹
- [ ] 设置基础文件夹架构
- [ ] 启用官方核心插件
- [ ] 创建每日笔记模板

### 本周完成（2-3 小时）
- [ ] 安装社区插件
- [ ] 配置 Bases 数据库
- [ ] 创建项目/读书笔记模板
- [ ] 设置 iCloud 同步

### 本月完成（持续优化）
- [ ] 配置 OpenClaw 联动
- [ ] 设置 AI 自动化工作流
- [ ] 完善记忆系统
- [ ] 定制 CSS 主题

## 🔗 资源链接

### 官方资源
- [Obsidian 官网](https://obsidian.md)
- [Obsidian 帮助文档](https://help.obsidian.md)
- [社区插件库](https://obsidian.md/plugins)
- [OpenClaw 官网](https://openclaw.ai)

### 教程资源
- [Linking Your Thinking 频道](https://www.youtube.com/@linkingyourthinking)
- [Jason Efficiency Lab 频道](https://www.youtube.com/@JasonEfficiencyLab)
- [清单控沙牛频道](https://www.youtube.com/@sandox)

### 工具资源
- [Claude API](https://console.anthropic.com)
- [Google AI Studio](https://aistudio.google.com)

## 🐛 故障排除

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

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 🙏 致谢

- [Nick Milo](https://www.youtube.com/@linkingyourthinking) - LYT 方法论创始人
- [Jason Efficiency Lab](https://www.youtube.com/@JasonEfficiencyLab) - AI 工具实战教程
- [清单控沙牛](https://www.youtube.com/@sandox) - 中文 Obsidian 教程
- [Obsidian 官方团队](https://obsidian.md) - 出色的笔记软件

## 📝 更新日志

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
**维护者:** Don brand
