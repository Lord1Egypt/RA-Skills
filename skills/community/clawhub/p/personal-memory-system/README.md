<div align="center">

# 个人AI记忆系统.skill

> *「你的每一天都是数字资产，别让它白白流失」*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![Skills](https://img.shields.io/badge/skills.sh-Compatible-green)](https://skills.sh)
[![Version](https://img.shields.io/badge/version-3.1.0-blue)](SKILL.md)
[![Privacy](https://img.shields.io/badge/data-local%20only-brightgreen)](SKILL.md)
[![GitHub](https://img.shields.io/badge/GitHub-ChenChen913%2Fmemory--system-black?logo=github)](https://github.com/ChenChen913/memory-system)

<br>

**一个持续生长的个人AI记忆系统，兼具人生记录仪和个人决策顾问两种属性。**

<br>

你给它的越多，它越懂你；它越懂你，它对你的价值就越大。<br>
三个月后，它开始看出你的规律；一年后，它比你更了解你自己。

<br>

[快速开始](#快速开始) · [功能介绍](#功能介绍) · [安全说明](#安全与隐私) · [多工具支持](#多工具支持) · [文件结构](#文件结构)

<br>

**其他语言 / Other Languages：**
[English](README_EN.md)

</div>

---

## 这是什么

**个人AI记忆系统**是一个 AI Skill，它把你的 AI 助手从"每次都要重新介绍自己的陌生人"变成"真正了解你的老朋友"。

- 📔 **人生记录仪**：每天记录，AI 帮你看出你自己都没注意到的规律
- 🧭 **个人决策顾问**：面对重要选择时，基于你的历史数据做沙盘推演
- 🎯 **目标追踪器**：持续追踪你的人生目标
- 🔮 **状态预测器**：每周/月/年给你基于数据的报告和预判

---

## 快速开始

### 安装

```bash
# 推荐方式
npx skills add ChenChen913/memory-system

# 指定安装到 Claude Code
npx skills add ChenChen913/memory-system -a claude-code

# 全局安装
npx skills add ChenChen913/memory-system -g
```

> **关于 skills.sh**：这个网站是 Skills 生态的排行榜，没有上传或注册界面。
> 只要用 `npx skills add ChenChen913/memory-system` 安装，安装量会自动统计到排行榜。
> 安装的人越多，在 skills.sh 上的排名越高。

### 初始化

安装后，对 AI 说：`初始化记忆系统`

AI 会引导你完成基础档案填写、目录建立、已有内容导入（约 10 分钟）。

### 日常使用

```
"记录今天"                → 开始写今天的日记
"随手记"                  → 快速记录几句话
"帮我做个推演"            → 决策沙盘分析
"生成本周周报"            → 本周状态总结
"你觉得我是什么样的人"    → AI 眼中的你
```

---

## 功能介绍

### 三个维度

**📅 现在维度**：日记记录 / 快速记录 / AI 智能回应 / 周总结+意图设定 / 月度总结 / 给未来自己的信

**📚 过去维度**：时间线（按年）/ 9 个主题档案（职业/关系/决策/健康/财务/性格/习惯/价值观/认知）/ AI 辅助回忆 / 已有内容导入

**🔮 未来维度**：三层信号系统 / 行为模式追踪 / 目标追踪 / 决策三情境推演 / 决策验证 / 周报/月报/年报

### 14 种特殊场景协议

危机协议 / 发泄协议 / 补记协议 / 重启协议 / 庆祝协议 / 纪念日检测 / 预警协议……覆盖所有真实使用场景。

---

## 安全与隐私

| 操作 | 状态 |
|---|---|
| 写入本地 `/memory/` 目录 | ✅ 是 |
| 调用外部 API / 主动发送数据 | ❌ 否 |
| 用户未触发时自主运行 | ❌ 否（autonomous_invocation: false）|

```bash
chmod 700 ~/memory/        # 限制目录权限
echo "memory/" >> .gitignore  # 避免提交到 Git
```

---

## 多工具支持

| 工具 | 支持 | 安装命令 |
|---|---|---|
| Claude Code | ⭐⭐⭐⭐⭐ | `npx skills add ChenChen913/memory-system -a claude-code` |
| OpenClaw | ⭐⭐⭐⭐⭐ | `npx skills add ChenChen913/memory-system` |
| Cursor | ⭐⭐⭐⭐ | `npx skills add ChenChen913/memory-system -a cursor` |
| Gemini CLI / Trae / Codex | ⭐⭐⭐ | 见 [AGENTS.md](AGENTS.md) |
| 本地模型（Ollama） | ⭐⭐⭐⭐⭐ | 见 [AGENTS.md](AGENTS.md) |

---

## 文件结构

```
memory-system/
├── SKILL.md                    # 主文件
├── AGENTS.md                   # 多工具适配
├── README.md                   # 中文说明
├── README_EN.md                # English
├── LICENSE
├── references/
│   ├── 00-initialization.md
│   ├── 01-present.md
│   ├── 02-past.md
│   ├── 03-future.md
│   ├── 05-protocols.md
│   └── 06-ai-voice.md
└── templates/（5个模板文件）
```

---

## 贡献与反馈

[GitHub Issues](https://github.com/ChenChen913/memory-system/issues) · [GitHub](https://github.com/ChenChen913/memory-system)

MIT License
