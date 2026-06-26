# Guild Knowledge Skill / Guild 经验文档管理

[![Version](https://img.shields.io/badge/version-1.0.1-blue.svg)](https://clawhub.com/skills/guild-knowledge)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-OpenClaw-orange.svg)](https://openclaw.ai)

**🌏 English | 🇨🇳 中文**

---

## 📖 Overview / 概述

**Guild Knowledge** is an experience document management skill for OpenClaw agents. It helps AI agents learn from past experiences while staying adaptable to new methods and technologies.

**Guild Knowledge** 是 OpenClaw 智能体的经验文档管理技能。它帮助 AI 智能体从过去的经验中学习，同时保持对新方法和技术的适应性。

**Core Principle / 核心原则:**
> "Experience is a reference, not scripture."
> "经验是参考，不是圣经。"

---

## ✨ Features / 功能特性

| Feature / 功能 | Description / 说明 |
|---------------|-------------------|
| 📚 **Auto-Read Guild Docs** / 自动查阅 Guild 文档 | Automatically reads relevant experience documents before tasks / 执行任务前自动阅读相关经验文档 |
| 🔍 **Search Latest Info** / 搜索最新信息 | Mandatory search for latest technologies and best practices / 强制搜索最新技术和最佳实践 |
| ⚖️ **Compare & Evaluate** / 对比评估 | Compares Guild recommendations vs. latest solutions / 对比 Guild 建议与最新方案 |
| 📅 **Monthly Review** / 月度审查 | Scheduled review of experience documents to prevent obsolescence / 定期审查经验文档避免过时 |
| 💡 **Experience Extraction** / 经验提取 | Automatically identifies patterns worth documenting / 自动识别值得记录的经验模式 |
| 📝 **Version Management** / 版本管理 | Tracks document versions and review cycles / 追踪文档版本和审查周期 |

---

## 🚀 Quick Start / 快速开始

### Installation / 安装

```bash
clawhub install guild-knowledge
```

### Automatic Trigger / 自动触发

The skill auto-triggers when you mention these keywords:

当提到以下关键词时自动触发：

| Chinese / 中文 | English / 英文 |
|---------------|---------------|
| 搭建网站 | build website |
| 清理工作区 | cleanup workspace |
| 技术审查 | technology review |
| Guild / 经验文档 | Guild / experience docs |
| PHP 网站 | PHP website |
| 删除文件 | delete files |

### Manual Trigger / 手动触发

```
/guild list        # List all Guild documents / 列出所有 Guild 文档
/guild search <query>  # Search experience documents / 搜索经验文档
/guild review      # Trigger monthly review / 触发月度审查
```

---

## 📋 How It Works / 工作原理

### Mandatory Workflow / 强制流程

```
┌─────────────────────────────────────────────────────────────┐
│  1. Read Guild Documents / 读取 Guild 文档                   │
│         ↓                                                    │
│  2. Search Latest Info (MANDATORY!) / 搜索最新信息（强制！） │
│     - Latest versions / 最新版本                             │
│     - Alternatives / 替代方案                                │
│     - Best practices / 最佳实践                              │
│         ↓                                                    │
│  3. Compare & Evaluate / 对比评估                            │
│     - Guild vs. Latest / Guild vs 最新                       │
│         ↓                                                    │
│  4. Decision / 决策                                          │
│     - Guild still best → Use Guild / Guild 仍最优→采用 Guild  │
│     - Better alternative → Suggest update / 有新方案→建议更新 │
│     - Uncertain → Ask user / 不确定→询问用户                 │
│         ↓                                                    │
│  5. Apply + Remind / 应用 + 提醒                             │
│     "Based on Guild + latest research, recommend XXX"        │
│     "根据 Guild 经验 + 最新搜索，推荐 XXX"                      │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 Document Structure / 文档结构

### Example Guild Documents / Guild 文档示例

| Document / 文档 | Purpose / 用途 | Review Cycle / 审查周期 |
|----------------|----------------|------------------------|
| `Guild_website-build-experience.md` | Website building best practices / 网站搭建最佳实践 | 6 months |
| `Guild_cleanup-guide.md` | Workspace organization guide / 工作区整理指南 | 6 months |
| `Guild_tech-radar.md` | Technology monitoring / 技术监控 | Monthly |
| `Guild_security-deployment.md` | Security deployment practices / 安全部署实践 | 3 months |

**Note**: Users create their own Guild documents based on their projects and experiences.

**注意**: 用户根据自己的项目和经验创建 Guild 文档。

### Protected Files / 受保护文件

Files with `Guild_` prefix are protected and should not be deleted manually.

`Guild_` 前缀的文件受保护，不应手动删除。

---

## 🎯 Use Cases / 使用场景

### Scenario 1: Building a Website / 搭建网站

```
User: "Help me build a website"
用户："帮我搭建一个网站"

Guild Knowledge:
1. ✅ Reads relevant Guild experience document
2. ✅ Searches latest technologies and frameworks
3. ✅ Compares Guild recommendations vs. latest solutions
4. ✅ Recommends: "Based on Guild experience + latest research, 
    recommend using [modern framework] for your use case"
    "根据 Guild 经验 + 最新搜索，推荐使用 [现代框架] 满足你的需求"
```

### Scenario 2: Technology Update / 技术更新

```
Guild Knowledge workflow:
1. Guild document suggests: "Use Technology A (v2.0)"
2. Latest search finds: "Technology A v3.0 released with 
   major improvements" or "Technology B is now recommended"

Response:
"Guild experience recommends Technology A v2.0.

However, latest research shows:
- Technology A v3.0 released with 50% performance improvement
- OR: Technology B is now the community recommended choice

Comparison provided. Would you like to:
1. Follow Guild experience (stable, proven)
2. Adopt latest recommendation (newer, may need testing)
3. Update Guild document after testing?"

"Guild 经验推荐使用 Technology A v2.0。

但最新搜索发现：
- Technology A v3.0 发布，性能提升 50%
- 或：Technology B 现在是社区推荐选择

已提供对比。你想：
1. 遵循 Guild 经验（稳定，已验证）
2. 采用最新推荐（较新，可能需要测试）
3. 测试后更新 Guild 文档？"
```

---

## 🔒 Safety Constraints / 安全限制

| Constraint / 限制 | Description / 说明 |
|------------------|-------------------|
| ❌ No blind following / 不盲从 | Never follow Guild without searching latest info / 不搜索最新信息就盲从 Guild |
| ❌ No outdated tech / 不使用过时技术 | Always prefer better alternatives / 优先选择更好的替代方案 |
| ❌ No auto-updates / 不自动更新 | All Guild changes require user approval / 所有 Guild 修改需用户审批 |
| ✅ Always verify / 始终验证 | Search before major tasks / 重大任务前搜索最新信息 |

---

## 📊 Review Cycle / 审查周期

| Document Type / 文档类型 | Cycle / 周期 | Content / 审查内容 |
|-------------------------|-------------|-------------------|
| Tech Radar / 技术雷达 | Monthly / 每月 | Tech updates, new tools / 技术更新、新工具 |
| Website Build / 网站搭建 | 6 months / 6 个月 | Web dev technologies / 网站开发技术 |
| Cleanup Guide / 清理指南 | 6 months / 6 个月 | Cleanup tools & methods / 清理工具和方法 |
| RPG Development / 游戏开发 | 6 months / 6 个月 | Game dev technologies / 游戏开发技术 |

---

## 🤝 Integration / 技能集成

### Optional Integrations / 可选集成

This skill works independently but can integrate with other OpenClaw skills:

本技能可独立工作，也可与其他 OpenClaw 技能集成：

| Integration / 集成 | Description / 说明 |
|-------------------|-------------------|
| **Experience Management** / 经验管理 | Auto-capture learnings from conversations / 自动捕获对话中的经验 |
| **Search Enhancement** / 搜索增强 | Use web search tools for latest info / 使用网络搜索获取最新信息 |
| **Document Automation** / 文档自动化 | Schedule periodic document reviews / 定期审查文档 |

**Note**: All integrations are optional and configurable.

**注意**: 所有集成都是可选和可配置的。

---

## 📝 Version History / 版本历史

### v1.0.1 (YYYY-MM-DD) - Update
- Bilingual support (Chinese + English)
- Optimized file structure
- Improved documentation

### v1.0.0 (YYYY-MM-DD) - Initial Release
- ✨ Initial release / 初始发布
- 📚 Auto-read Guild documents / 自动查阅 Guild 文档
- 🔍 Mandatory latest info search / 强制最新信息搜索
- ⚖️ Compare & evaluate workflow / 对比评估流程
- 📅 Monthly review system / 月度审查系统
- 💡 Experience extraction / 经验提取
- 📝 Version management / 版本管理

---

## 🎯 Best Practices / 最佳实践

### For Users / 给用户

1. ✅ **Review before tasks** - Check Guild docs before major tasks
   **任务前审查** - 重大任务前查阅 Guild 文档

2. ✅ **Stay open** - Experience is reference, not scripture
   **保持开放** - 经验是参考，不是圣经

3. ✅ **Approve changes** - Review and approve Guild updates
   **审批变更** - 审查并批准 Guild 更新

### For Agents / 给智能体

1. ✅ **Search first** - Always search latest info before using Guild
   **先搜索** - 使用 Guild 前始终搜索最新信息

2. ✅ **Compare honestly** - Admit when new methods are better
   **诚实对比** - 新方法更好时承认

3. ✅ **Document promptly** - Update Guild when better methods found
   **及时记录** - 发现更好方法时更新 Guild

---

## 📞 Support / 支持

- **Issues**: Open issue on ClawHub
- **Discussions**: clawhub.com/skills/guild-knowledge/discussions
- **Documentation**: See SKILL.md for detailed implementation

---

## 📄 License / 许可证

MIT License - Free to use, modify, and redistribute.

MIT 许可证 - 免费使用、修改和分发。

---

**Created by / 创建者**: Pipiy416  
**Last Updated / 最后更新**: 2026-03-27  
**Languages / 语言**: 🇨🇳 Chinese / 中文 + 🌏 English

---

*"Experience is a reference, not scripture. Stay adaptable, embrace change, use better methods!"*

*"经验是参考，不是圣经。保持开放，拥抱变化，用更好的方法！"*
