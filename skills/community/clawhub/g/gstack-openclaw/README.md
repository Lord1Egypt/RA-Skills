# gstack-openclaw 🦞

> 把 Garry Tan 的虚拟工程团队带到 OpenClaw 生态

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenClaw](https://img.shields.io/badge/Built%20for-OpenClaw-blue)](https://github.com/openclaw/openclaw)
[![Security](https://img.shields.io/badge/Security-Documentation--only-brightgreen.svg)](SECURITY.md)

> **⚠️ 安全声明**: 本技能为纯文档型技能，不包含可执行代码，不需要 API 凭证，不访问外部服务。
> 
> 详细安全说明请查看 [SECURITY.md](./SECURITY.md)

---

## 🎯 什么是 gstack-openclaw？

**gstack** 是 Y Combinator CEO Garry Tan 开源的 Claude Code 工作流系统，让他能在 60 天内产出 **60 万行代码**。

**gstack-openclaw** 是它的 OpenClaw 移植版本，让每个人都能拥有 YC 级别的虚拟工程团队。

### 核心理念

> 不是把 AI 当工具用，而是**当团队管** —— 每个阶段切换不同专家角色。

---

## 📦 包含技能

### 核心技能 (v2.5.0)

| 技能 | 角色 | 用途 |
|-----|------|-----|
| `gstack:ceo` | CEO / 产品经理 | 产品规划、需求分析、痛点挖掘 |
| `gstack:eng` | 工程经理 | 架构设计、技术选型、数据流规划 |
| `gstack:design` | 设计评审师 | 设计评审、AI Slop检测、设计系统生成 |
| `gstack:investigate` | 系统调试专家 | 根因分析、3次失败停止、Bug调查 |
| `gstack:security` | 首席安全官 | OWASP Top 10、STRIDE威胁建模 |
| `gstack:land` | 部署验证工程师 | PR合并、生产部署、健康验证 |
| `gstack:canary` | 金丝雀监控工程师 ⭐ NEW | 金丝雀分析、自动回滚决策 |
| `gstack:benchmark` | 性能基准工程师 ⭐ NEW | Core Web Vitals、性能回归检测 |
| `gstack:review` | 代码审查员 | 代码审查、Bug 发现、性能优化建议 |
| `gstack:qa` | QA 负责人 | 测试策略、验收标准、质量把关 |
| `gstack:ship` | 发布工程师 | 发版 checklist、部署流程、上线检查 |
| `gstack:browse` | 浏览器测试 | 网页抓取、功能验证、UI 检查 |
| `gstack:retro` | 复盘师 | 项目复盘、经验总结、改进建议 |
| `gstack:office` | 办公室时间 | 需求澄清、方向校准、头脑风暴 |
| `gstack:docs` | 技术文档工程师 | 自动生成 README、API 文档 |
| `gstack:test` | 测试工程师 | 生成测试用例和测试代码 |
| `gstack:deploy` | DevOps 工程师 | 生成部署脚本和 CI/CD 配置 |
| `gstack:init` | 项目初始化 | 自动创建 GSTACK.md 和项目骨架 |
| `gstack:status` | 项目状态追踪 | 查看进度和下一步行动 |
| `gstack:github` | GitHub 集成 | PR 检查、CI 监控、发布说明 |
| `gstack:notify` | 消息通知 | 飞书/Discord 多渠道通知 |

---

## 🚀 快速开始

### 从 ClawHub 安装（推荐）

```bash
clawhub install openclaw/gstack
```text

### 手动安装

```bash
# 1. 克隆仓库
git clone https://github.com/openclaw/gstack-openclaw ~/.openclaw/skills/gstack

# 2. 复制技能文件
mkdir -p ~/.openclaw/skills/gstack
cp ~/.openclaw/skills/gstack/SKILL.md ~/.openclaw/skills/gstack/
```text

### 验证安装

```bash
clawhub list
# 应该看到 gstack 及其子技能
```text

---

## 💡 使用方法

### 基础用法

在项目根目录随时调用：

```text
@gstack:ceo 帮我分析一下这个功能的产品价值

@gstack:design 评审这个界面设计

@gstack:review 审查一下这个模块的代码

@gstack:qa 设计一下测试用例

@gstack:ship 准备发布 v1.0.0
```text

### 完整工作流示例

**新功能开发**：

```text
1. @gstack:office      # 澄清需求，确定方向
2. @gstack:ceo         # 产品规划，写 PRD
3. @gstack:design      # 设计评审，生成设计系统
4. @gstack:eng         # 技术架构设计
5. 【开发中...】
6. @gstack:review      # 代码审查
7. @gstack:qa          # 测试验收
8. @gstack:ship        # 发布上线
9. @gstack:retro       # 一周后复盘
```text

### 项目配置

在项目根目录创建 `GSTACK.md` 记录项目上下文：

```markdown
# Project Context

## 项目概述
- 名称: MyApp
- 技术栈: React + Node.js + PostgreSQL
- 团队规模: 5人

## 关键链接
- 设计稿: [Figma URL]
- API 文档: [Swagger URL]
- 监控面板: [Grafana URL]

## 注意事项
- 用户表敏感字段需加密
- 支付模块需要额外审查
```text

---

## 📚 技能详解

### gstack:ceo —— CEO / 产品经理
像 Brian Chesky 一样思考产品，找到真正的用户痛点。

```text
@gstack:ceo 我想做一个XXX功能
```text

**输出**：痛点分析、目标用户、价值主张、MVP 范围、成功指标

---

### gstack:eng —— 工程经理
设计稳健的技术架构，做好技术选型。

```text
@gstack:eng 帮我设计这个功能的架构
```text

**输出**：架构图、数据模型、接口设计、技术选型、风险分析

---

### gstack:benchmark —— 性能基准工程师 ⭐ NEW v2.5.5
像 Google PageSpeed 和 WebPageTest 一样进行性能测试，优化 Core Web Vitals。

```text
@gstack:benchmark 建立性能基准

@gstack:benchmark 检测性能回归
```text

**输出**：
- Core Web Vitals 评分 (LCP, FID, CLS)
- 资源分析 (JS/CSS/图片)
- 性能回归检测
- 优化建议

---

### gstack:canary —— 金丝雀监控工程师 ⭐ NEW v2.5.4
像 Netflix 和 Google SRE 一样监控金丝雀发布，自动决策回滚或继续。

```text
@gstack:canary 监控金丝雀发布

@gstack:canary 分析新版本指标
```text

**输出**：
- 金丝雀 vs 基线指标对比
- 统计显著性分析
- 继续/回滚决策
- 异常检测报告

---

### gstack:land —— 部署验证工程师 ⭐ NEW v2.5.3
像 Google SRE 一样专业地执行部署，一键完成 PR 合并、生产部署、健康验证。

```text
@gstack:land 部署当前 PR 到生产

@gstack:land 验证生产环境健康状态
```text

**输出**：
- 预检查报告
- 金丝雀/蓝绿部署过程
- 健康验证结果
- 部署报告或回滚报告

---

### gstack:security —— 首席安全官 ⭐ NEW v2.5.2
像 Google Security Team 一样进行安全审计，覆盖 OWASP Top 10 和 STRIDE 威胁建模。

```text
@gstack:security 审计这个项目的安全性

@gstack:security OWASP Top 10 检查

@gstack:security STRIDE 威胁建模
```text

**输出**：
- OWASP Top 10 合规性评估
- STRIDE 6类威胁分析
- 风险评级（严重/高危/中危/低危）
- 可执行的修复方案
- 安全加固建议

---

### gstack:investigate —— 系统调试专家 ⭐ NEW v2.5.1
像 Netflix SRE 一样进行系统性根因分析，遵循"3次失败停止"原则。

```text
@gstack:investigate 为什么这个 API 返回 500

@gstack:investigate 排查这个性能问题
```text

**输出**：
- Bug 调查报告（观察、假设、验证）
- 5 Whys 根因分析
- 短期+长期修复方案
- 经验教训和预防措施

---

### gstack:design —— 设计评审师 ⭐ NEW v2.5.0
像 Stripe、Airbnb 的设计团队一样评审设计，检测 AI 生成的 "Slop"（低质量设计）。

```text
@gstack:design 评审这个界面设计

@gstack:design 生成设计系统

@gstack:design 检测 AI Slop
```text

**输出**：
- 8维度设计评分（视觉层次、一致性、留白、色彩、排版、交互、可访问性、品牌）
- AI Slop 检测报告（通用渐变、过度圆角、无意义图标等）
- 完整设计系统（色彩、字体、间距、组件）
- 10-Star 体验升级路径

---

### gstack:review —— 代码审查员
像资深工程师一样审查代码，发现隐藏问题。

```text
@gstack:review 审查当前文件
```text

**输出**：代码质量评分、阻塞问题、警告问题、优化建议

---

### gstack:qa —— QA 负责人
设计全面的测试策略，定义验收标准。

```text
@gstack:qa 设计测试用例
```text

**输出**：测试计划、测试用例、边界情况、风险评估

---

### gstack:ship —— 发布工程师
确保每次发布都稳定可靠。

```text
@gstack:ship 准备发布 v1.2.0
```text

**输出**：发布检查清单、Changelog、回滚方案、发布后验证

---

### gstack:browse —— 浏览器测试
进行真实的浏览器测试，验证功能。

```text
@gstack:browse 打开 https://example.com
```text

**输出**：页面截图、功能检查、UI/UX 评估、问题发现

---

### gstack:retro —— 复盘师
从经验中学习，持续改进。

```text
@gstack:retro 复盘最近这个项目
```text

**输出**：4L 分析 (Loved/Learned/Lacked/Longed for)、行动项

---

### gstack:office —— 办公室时间
像 YC 合伙人一样帮助澄清思路。

```text
@gstack:office 帮我看看这个产品方向
```text

**输出**：问题诊断、决策分析、方向校准

---

## 🎓 设计理念

### 为什么角色驱动？

传统 AI 助手是"你问什么我答什么"，缺乏上下文和专业深度。

gstack 通过**角色切换**，让 AI 在每个阶段都以专家身份思考：
- 产品阶段 → 用 CEO 思维
- 技术阶段 → 用架构师思维
- 测试阶段 → 用 QA 思维

### 从 Garry Tan 学到的

Garry 用这套系统 60 天产出 60 万行代码，关键不是"更快"，而是：
1. **结构化**: 每个阶段有明确的目标和输出
2. **专业化**: 不同角色专注不同领域
3. **可复用**: 把个人最佳实践封装成流程

---

## 📋 版本历史

### v2.5.6 (2026-04-09) - 安全透明度提升
- 🔒 **添加完整安全声明** —— 消除 ClawHub 安全警告
  - 新增 SECURITY.md 详细安全策略文档
  - SKILL.md 顶部添加安全声明和透明度说明
  - install.sh 添加详细的安全注释和行为透明化
  - README.md 添加安全徽章和链接
- 📋 **文档优化** —— 明确说明本技能为纯文档型，不涉及外部 API 调用

### v2.5.5 (2026-03-29) - 性能能力补齐
- ✨ **新增 `gstack:benchmark`** —— 性能基准工程师技能
  - Core Web Vitals 完整分析 (LCP, FID, CLS)
  - 性能基准建立和回归检测
  - Lighthouse 集成
  - 资源分析和优化建议

### v2.5.4 (2026-03-29) - 金丝雀监控补齐
- ✨ **新增 `gstack:canary`** —— 金丝雀监控工程师技能
  - 金丝雀 vs 基线指标自动对比
  - 统计显著性分析
  - 智能回滚决策
  - 异常自动检测

### v2.5.3 (2026-03-29) - 部署能力补齐
- ✨ **新增 `gstack:land`** —— 部署验证工程师技能
  - PR 合并、生产部署、健康验证一键完成
  - 支持金丝雀、蓝绿、滚动部署策略
  - 自动健康检查和异常检测
  - 自动回滚机制

### v2.5.2 (2026-03-29) - 安全能力补齐
- ✨ **新增 `gstack:security`** —— 首席安全官技能
  - OWASP Top 10 2021 完整检查
  - STRIDE 威胁建模（6类威胁分析）
  - 安全审计报告生成
  - 风险评级和修复方案
  - 安全加固建议

### v2.5.1 (2026-03-29) - 调试能力补齐
- ✨ **新增 `gstack:investigate`** —— 系统调试专家技能
  - 系统性调试流程（观察→假设→实验→分析）
  - 3次失败自动停止原则
  - 5 Whys 根因分析
  - 数据流追踪、假设树分析、二分法定位
  - Bug 调查报告生成

### v2.5.10 (2026-04-10) - 移除 install.sh
- 🔒 **移除 install.sh 脚本** —— 完全满足 "documentation-only" 安全分类
  - 消除 ClawHub "Suspicious" 警告
  - 不影响任何功能（推荐安装方式 `clawhub install` 不依赖该脚本）
  - 更新 SECURITY.md 和 SKILL.md 移除 install.sh 引用

### v2.5.9 (2026-04-10) - install.sh 安全透明度
- 🔒 **增强 install.sh 安全说明** —— 尝试消除 ClawHub Suspicious 警告
  - 详细解释 install.sh 仅执行安全的文件操作（mkdir, cp）
  - 提供与危险脚本的对比说明
  - 强调用户选择权（可完全不使用 install.sh）

### v2.5.8 (2026-04-09) - 代码块渲染修复
- 🐛 **修复代码块渲染问题** —— 解决 ClawHub 页面空白问题
  - 将代码块改为列表形式
  - 确保所有内容正确显示

### v2.5.7 (2026-04-09) - 安全声明增强
- 🔒 **添加完整安全声明** —— 消除 ClawHub 安全警告
  - 新增 SECURITY.md 详细安全策略文档
  - SKILL.md 顶部添加安全声明和透明度说明
  - 明确说明本技能为纯文档型，不涉及外部 API 调用

### v2.5.0 (2026-03-29) - 设计能力补齐
- ✨ **新增 `gstack:design`** —— 设计评审师技能
  - 8维度设计评分（视觉层次、一致性、留白、色彩、排版、交互、可访问性、品牌）
  - AI Slop 检测（识别 AI 生成的低质量设计）
  - 完整设计系统生成（色彩、字体、间距、组件）
  - 10-Star 体验设计框架
  - 竞品研究方法

### v2.4.0 (2026-03-27)
- ✨ 10-Star 体验框架完善
- ✨ ASCII 架构图生成
- ✨ 探索性测试强化
- ✨ 完整性缺口检查

### v2.3.0 (2026-03-26)
- ✨ 工作流 feed 机制
- ✨ Auto-fix 能力
- ✨ 6个强制性问题框架
- ✨ 4种决策模式

### v2.0.0-2.2.0
- ✨ 10个核心角色深度优化
- ✨ 初始版本发布

---

## 🤝 贡献指南

我们欢迎所有形式的贡献！

### 如何贡献

1. **Fork 仓库**
2. **创建分支**: `git checkout -b feature/amazing-feature`
3. **提交更改**: `git commit -m 'Add amazing feature'`
4. **推送分支**: `git push origin feature/amazing-feature`
5. **创建 Pull Request**

### 贡献内容

- 🐛 Bug 修复
- ✨ 新技能或技能改进
- 📚 文档改进
- 🌐 翻译支持
- 💡 新想法和建议

---

## 🙏 致谢

- [Garry Tan](https://github.com/garrytan) —— 原创 gstack 作者，开源精神的典范
- [Y Combinator](https://www.ycombinator.com/) —— 持续推动创业生态
- [OpenClaw](https://github.com/openclaw/openclaw) —— 让 AI Agent 触手可及
- 所有贡献者 —— 让这个生态变得更好

---

## 📄 License

MIT License —— 完全免费，随意使用、修改、分发

```text
Copyright (c) 2026 OpenClaw Community

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```text

**我们的目标**：让每个开发者都能拥有 YC 级别的工程团队

---

## 💬 社区

- GitHub Issues: [提问和反馈](https://github.com/openclaw/gstack-openclaw/issues)
- Discord: [加入讨论](https://discord.gg/openclaw)
- Twitter: [@openclaw](https://twitter.com/openclaw)

---

*Made with 🦞 by OpenClaw Community*

> "Build something people want" —— Y Combinator
