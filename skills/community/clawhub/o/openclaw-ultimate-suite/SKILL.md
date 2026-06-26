---
name: openclaw-ultimate-suite
description: OpenClaw 终极技能整合套件 - 29 个技能一站式整合 × 61 个专业 Agent × 安全内置 × 自动激活 × 飞书集成。晴晴超级版：办公效率 + 生活助手 + 社交媒体 + 信息收集 + AI 代理 + 安全守护。
version: 3.0.0
author: 晴晴
license: MIT
tags: [suite, productivity, office, social-media, ai-agents, security, chinese, automation]
metadata:
  clawdbot:
    emoji: "🚀"
    category: "productivity"
    requires:
      env: ["AUTO_SKILL_ACTIVATION", "FEISHU_NOTIFY", "IRONCLAW_AUTO_SCAN"]
      files: ["skills/*", "docs/*", "examples/*"]
---

# OpenClaw 终极技能整合套件

## 📦 技能概述

晴晴整合了 **29 个实用技能** + **61 个专业 Agent**，一站式解决：办公效率、生活助手、社交媒体、信息收集、产品开发、安全审计

### 核心优势

| 维度 | 原版 | 晴晴超级版 |
|------|------|-----------|
| 技能数量 | 分散 | ✅ 29 个一站式整合 |
| Agent 数量 | 6 个 MVP | ✅ 61 个完整库 |
| 安全检测 | 无 | ✅ IronClaw 全扫描 |
| 中文文档 | 部分 | ✅ 完全本地化 |
| 自动激活 | 手动 | ✅ 场景识别自动调用 |
| 飞书集成 | 无 | ✅ 通知 + 交付 |

---

## 🏢 技能分类

### 办公效率类（6 个）
office, productivity, note, writing-assistant, calendar, todolist

### 生活助手类（2 个）
weather, email-daily-summary

### 社交媒体类（3 个）
xiaohongshu-mcp, social-media-scheduler, tiktok-crawling

### 信息收集类（4 个）
multi-search-engine, playwright, summarize, ontology

### AI 代理类（3 个）
agency-agents (61 个专业 Agent), proactive-agent-lite, xiucheng-self-improving-agent

### 安全类（3 个）
ironclaw-guardian-evolved, skill-vetter, openclaw-guardian-ultra

### GitHub 克隆技能（4 个）
openclaw-free-web-search, openclaw-hierarchical-task-spawn, openclaw-github-repo-commander, openclaw-feishu-file-delivery

### 晴晴优化技能（2 个）
agency-agents-evolved, openclaw-life-office-suite

---

## 🤖 自动激活规则

### 产品开发场景
触发词："开发"、"产品"、"MVP"、"网站"、"app"  
自动激活：agency-agents (orchestrator) + ironclaw + todolist + feishu-file-delivery

### 市场调研场景
触发词："分析"、"竞品"、"报告"、"调研"  
自动激活：multi-search-engine + playwright + summarize + trend-researcher

### 办公效率场景
触发词："文档"、"周报"、"PPT"、"会议"、"邮件"  
自动激活：office + note + writing-assistant + calendar

### 生活助手场景
触发词："天气"、"明天"、"出差"、"活动"  
自动激活：weather + calendar + email-daily-summary

### 社交媒体场景
触发词："小红书"、"抖音"、"发布"、"排期"、"内容"  
自动激活：xiaohongshu-mcp + social-media-scheduler + content-creator

### 信息收集场景
触发词："搜索"、"调研"、"数据"、"知识"  
自动激活：multi-search-engine + playwright + summarize + ontology

---

## 🛡️ 安全内置

所有技能经过 IronClaw Guardian Evolved 检测：
- ✅ xiaohongshu-mcp: Label 0, Confidence 99%
- ✅ email-daily-summary: Label 0, Confidence 99%
- ✅ tiktok-crawling: Label 0, Confidence 99%

安全功能：
- ✅ 技能文件安装前扫描
- ✅ Prompt injection 检测
- ✅ 危险命令拦截
- ✅ 秘密泄露防护
- ✅ 审计日志记录

---

## 🚀 快速开始

### 一键安装
```bash
clawhub install openclaw-ultimate-suite
```

### 使用单个技能
```bash
/openclaw skill use office "帮我创建周报模板"
/orchestrator "开发一个电商网站 MVP"
```

### 自动激活（推荐）
```bash
你说："我想做个电商网站"
→ 自动激活：agency-agents + ironclaw + todolist + feishu-file-delivery
```

---

## ⚙️ 配置选项

```bash
# 启用自动技能激活
AUTO_SKILL_ACTIVATION=true

# 启用飞书通知
FEISHU_NOTIFY=true

# 启用 IronClaw 检测
IRONCLAW_AUTO_SCAN=true

# 社交媒体默认平台
SOCIAL_MEDIA_DEFAULT_PLATFORM=xiaohongshu

# 质量检查严格度 (1-5)
AGENCY_AGENTS_QA_LEVEL=3

# 最大重试次数
AGENCY_AGENTS_MAX_RETRIES=3
```

---

## 📋 目录结构

```
openclaw-ultimate-suite/
├── README.md              # 超级说明文档
├── SKILL.md               # 统一技能定义
├── skill.json             # ClawHub 元数据
├── _meta.json             # 额外元数据
├── skills/                # 所有技能整合
├── docs/                  # 统一文档
├── examples/              # 使用示例
└── scripts/               # 自动化脚本
```

---

## 🔧 故障排查

### 技能未自动激活
- 检查关键词匹配规则
- 查看 `~/.openclaw/logs/skill-activation.jsonl`
- 确认技能已安装

### 安全检测失败
- 手动审查技能代码
- 使用 `--force` 安装（谨慎）
- 反馈给晴晴改进检测

### 社交媒体 API 失败
- 检查 API 密钥配置
- 验证账号授权
- 查看技能文档

---

## 📄 许可证

MIT License - 整合自多个开源技能

---

## 🙏 致谢

**原始技能作者:**
- xiaohongshu-mcp: Borye
- email-daily-summary: 10e9928a
- agency-agents: @msitarzewski
- 其他技能：各原作者

**晴晴整合:** 一站式整合 + 安全检测 + 中文本地化 + 自动激活 + 飞书集成

---

## 📞 联系方式

- **GitHub**: https://github.com/wd041216-bit/openclaw-ultimate-suite
- **作者**: wd041216-bit (晴晴超级版)

---

*最后更新：2026-03-15*  
*版本：3.0.0 晴晴超级版*
