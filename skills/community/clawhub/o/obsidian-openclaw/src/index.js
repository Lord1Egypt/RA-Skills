/**
 * Obsidian Master Skill - 主入口文件
 * 
 * 基于三大 YouTube 频道教程的 Obsidian 完整配置方案
 * 
 * @author Don brand
 * @version 1.0.0
 * @since 2026-03-05
 */

const CONFIG = {
  name: 'obsidian-master',
  version: '1.0.0',
  description: 'Obsidian 大师级配置助手',
  author: 'Don brand'
};

/**
 * Skill 主函数
 * @param {Object} params - 参数对象
 * @returns {Promise<Object>} 执行结果
 */
async function main(params) {
  const { action, query } = params;
  
  console.log(`[Obsidian Master] 收到请求：${action}`);
  
  switch (action) {
    case 'setup':
      return await getSetupGuide();
    case 'plugins':
      return await getPluginsList();
    case 'templates':
      return await getTemplates();
    case 'ai':
      return await getAIIntegration();
    case 'workflow':
      return await getWorkflow();
    case 'checklist':
      return await getChecklist();
    default:
      return await getHelp();
  }
}

/**
 * 获取完整配置指南
 */
async function getSetupGuide() {
  return {
    title: 'Obsidian 完整配置指南',
    content: `
# Obsidian 完整配置指南

## 文件夹架构
\`\`\`
📁 Vault/
├── 📁 00-Inbox/           # 收集箱
├── 📁 01-Daily/           # 日记
├── 📁 02-Areas/           # 责任领域
├── 📁 03-Projects/        # 项目
├── 📁 04-Resources/       # 资源库
├── 📁 05-Archives/        # 归档
├── 📁 99-System/          # 系统配置
└── 📁 memory/             # OpenClaw 记忆
\`\`\`

## 核心插件
- 官方：模板、日记、双向链接、标签面板
- 社区：Dataview、Templater、QuickAdd、Calendar、Bases

## AI 集成
- Claude Skill：笔记总结、扩展、翻译
- OpenClaw：Telegram/微信消息自动整理
- Gemini 3：系统指令、避免幻觉

详细配置请参考：Obsidian 核心技巧与完整配置指南.md
    `
  };
}

/**
 * 获取插件推荐清单
 */
async function getPluginsList() {
  return {
    title: 'Obsidian 插件推荐清单',
    content: `
# Obsidian 插件推荐

## 官方必备插件
| 插件 | 用途 |
|------|------|
| 模板 | 快速创建标准化笔记 |
| 日记 | 自动生成每日笔记 |
| 双向链接 | 显示笔记关系 |
| 标签面板 | 管理标签系统 |
| 书签 | 快速访问常用笔记 |
| 大纲 | 查看笔记结构 |
| 搜索 | 全局内容检索 |

## 推荐社区插件
| 插件 | 用途 |
|------|------|
| Dataview | 数据库查询 |
| Templater | 高级模板 |
| QuickAdd | 快速添加内容 |
| Calendar | 日历视图 |
| Kanban | 看板管理 |
| Excalidraw | 绘图/白板 |
| Omnisearch | 增强搜索 |
| Bases | 数据库管理 |
    `
  };
}

/**
 * 获取模板系统
 */
async function getTemplates() {
  return {
    title: 'Obsidian 模板系统',
    content: `
# Obsidian 模板系统

## 每日笔记模板
\`\`\`markdown
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
\`\`\`

## 读书笔记模板
\`\`\`markdown
---
title: {{title}}
author: 
status: 阅读中
tags: [读书/{{主题}}]
created: {{date}}
---

# 《{{title}}》

## 📖 基本信息
## 💡 核心观点
## 📝 关键摘录
## 🤔 我的思考
## 🔗 关联笔记
\`\`\`

## 项目笔记模板
\`\`\`markdown
---
project: {{title}}
status: 进行中
priority: 高
tags: [项目/{{分类}}]
start_date: {{date}}
---

# {{title}}

## 🎯 项目目标
## 📋 任务清单
## 📊 进度跟踪
## 📝 会议记录
## 🔗 相关资源
\`\`\`
    `
  };
}

/**
 * 获取 AI 集成方案
 */
async function getAIIntegration() {
  return {
    title: 'AI 集成方案',
    content: `
# AI 集成方案

## Claude Skill 配置
1. 安装 Claude Skill 插件
2. 配置 API Key
3. 常用指令：
   - /summarize - 总结当前笔记
   - /expand - 扩展想法
   - /translate - 翻译内容
   - /improve - 改进写作

## OpenClaw 联动
1. 安装 OpenClaw
2. 配置飞书/Telegram
3. 设置自动同步

## Gemini 3 高级技巧
1. 系统指令 (System Instructions)
2. 避免 AI 幻觉
3. 交互禁忌

详细配置请参考：Obsidian 核心技巧与完整配置指南.md
    `
  };
}

/**
 * 获取 AI 工作流配置
 */
async function getWorkflow() {
  return {
    title: 'AI 工作流配置',
    content: `
# AI 工作流配置

## 信息收集 → Obsidian
\`\`\`
Telegram/微信消息
    ↓
OpenClaw 接收
    ↓
AI 整理分类
    ↓
写入 Obsidian Inbox
    ↓
定期整理到对应文件夹
\`\`\`

## 记忆系统集成
\`\`\`
📁 memory/
├── MEMORY.md              # 长期记忆
├── topics/                # 主题记忆
│   ├── 系统配置与规则.md
│   ├── 日程与计划.md
│   ├── 项目开发.md
│   └── 主人偏好与习惯.md
└── YYYY-MM-DD.md          # 每日日志
\`\`\`

## OpenClaw 配置
\`\`\`json
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
  }
}
\`\`\`
    `
  };
}

/**
 * 获取配置检查清单
 */
async function getChecklist() {
  return {
    title: '配置检查清单',
    content: `
# 配置检查清单

## 基础配置（30 分钟）
- [ ] 安装 Obsidian 1.10+
- [ ] 创建 Vault 文件夹
- [ ] 设置基础文件夹架构
- [ ] 启用官方核心插件
- [ ] 创建每日笔记模板

## 本周完成（2-3 小时）
- [ ] 安装社区插件
- [ ] 配置 Bases 数据库
- [ ] 创建项目/读书笔记模板
- [ ] 设置 iCloud 同步

## 本月完成（持续优化）
- [ ] 配置 OpenClaw 联动
- [ ] 设置 AI 自动化工作流
- [ ] 完善记忆系统
- [ ] 定制 CSS 主题
    `
  };
}

/**
 * 获取帮助信息
 */
async function getHelp() {
  return {
    title: 'Obsidian Master Skill 帮助',
    content: `
# Obsidian Master Skill 帮助

## 可用命令
| 命令 | 描述 |
|------|------|
| \`obsidian setup\` | 获取完整配置指南 |
| \`obsidian plugins\` | 获取插件推荐清单 |
| \`obsidian templates\` | 获取模板系统 |
| \`obsidian ai\` | 获取 AI 集成方案 |
| \`obsidian workflow\` | 获取 AI 工作流配置 |
| \`obsidian checklist\` | 获取配置检查清单 |

## 学习资源
- [Linking Your Thinking](https://www.youtube.com/@linkingyourthinking) - 31.6 万订阅
- [Jason Efficiency Lab](https://www.youtube.com/@JasonEfficiencyLab) - 2.04 万订阅
- [清单控沙牛](https://www.youtube.com/@sandox) - 6,370 订阅

## 相关文档
- Obsidian 核心技巧与完整配置指南.md
- Linking Your Thinking - Obsidian 课程网址大全.md
    `
  };
}

// 导出模块
module.exports = {
  CONFIG,
  main,
  getSetupGuide,
  getPluginsList,
  getTemplates,
  getAIIntegration,
  getWorkflow,
  getChecklist,
  getHelp
};
