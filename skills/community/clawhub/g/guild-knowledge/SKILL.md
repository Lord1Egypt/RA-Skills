---
name: guild-knowledge
description: Guild 经验文档管理技能。核心原则：经验是参考，不是圣经。自动查阅 Guild 文档 + 搜索最新信息 + 对比评估。| Guild experience document management skill. Core principle: Experience is a reference, not scripture. Auto-reads Guild docs + searches latest info + compares and evaluates.
version: 1.0.1
license: MIT
languages: [zh-CN, en]
author: Pipiy416
homepage: https://github.com/Pipiy416/guild-knowledge
tags: [经验管理，文档，知识管理，Guild, experience-management, documentation, knowledge-base, best-practices]
auto_trigger: true
trigger:
  keyword_zh: 搭建网站 | 创建网站 | 清理工作区 | 删除文件 | 整理文件 | 技术审查 | 新技术 | 技术雷达 | Guild | 经验文档 | 经验文件
  keyword_en: build website | create website | cleanup workspace | delete files | organize files | technology review | new technology | tech radar | Guild | experience docs | experience documents
---

# Guild Knowledge Skill / Guild 经验文档管理

**版本 (Version):** 1.0.1  
**创建日期 (Created):** YYYY-MM-DD  
**核心原则 (Core Principle):** 经验是参考，不是圣经 | Experience is a reference, not scripture

---

## 📜 核心原则 / Core Principle

```
"经验是参考，不是圣经"
Experience is a reference, not scripture.
```

### 强制流程 / Mandatory Workflow

```
1. 读取 Guild 文档 / Read Guild document
   ↓
2. 搜索最新信息（强制！）/ Search latest info (MANDATORY!)
   - 技术最新版本 / Latest technology versions
   - 替代方案 / Alternative solutions
   - 最佳实践 / Best practices
   ↓
3. 对比评估 / Compare & Evaluate
   - Guild 建议 vs 最新方案 / Guild vs Latest
   ↓
4. 决策 / Decision
   - Guild 仍最优 → 采用 Guild
   - 新方案更好 → 建议更新
   - 不确定 → 询问用户
   ↓
5. 应用 + 提醒 / Apply + Remind
```

### 禁止行为 / Forbidden Actions

```
❌ 盲从 Guild 经验，不搜索最新信息
❌ 使用过时的技术/工具
❌ 发现更好的方法不更新文档
❌ 未经用户审批修改 Guild 文档
```

---

## 🎯 自动触发 / Auto-Trigger

### 触发词示例 / Example Trigger Keywords

| 中文触发词 | English Trigger | 说明 / Description |
|-----------|----------------|-------------------|
| 搭建网站 | build website | 网站搭建相关任务 |
| 清理工作区 | cleanup workspace | 工作区整理相关 |
| 技术审查 | technology review | 技术评估相关 |
| Guild | Guild | 文档管理相关 |

**注意**: 用户可以根据自己的 Guild 文档自定义触发词。

**Note**: Users can customize trigger keywords based on their own Guild documents.

---

## 📋 功能列表 / Features

### 功能 1：自动查阅 + 搜索 / Auto-Read + Search

```yaml
触发：用户提到相关任务
动作:
  1. 自动读取对应 Guild 文档
  2. 搜索最新信息
  3. 对比评估
  4. 给出建议
  5. 提醒是否更新文档
```

---

### 功能 2：文档检索 / Document Retrieval

```yaml
命令:
  /guild list        # 列出所有 Guild 文档
  /guild search <关键词>  # 搜索经验文档
  /guild review      # 触发审查
```

---

### 功能 3：分级审查 / Tiered Review

```yaml
审查策略:
  📊 技术类文档：每月审查
  📚 经验类文档：3 个月审查
  📖 规范类文档：6 个月审查

审批模式：所有修改需用户审批
```

---

### 功能 4：索引更新 / Index Update

```yaml
流程:
  扫描 Guild/文件夹
      ↓
  检测新文件/内容变更
      ↓
  生成更新建议
      ↓
  用户审批 → 更新索引
```

---

### 功能 5：经验提取 / Experience Extraction

```yaml
筛选标准:
  ✅ 重复出现≥3 次
  ✅ 跨项目/跨场景适用
  ✅ 有明确解决方案
  
流程:
  审查学习记录
      ↓
  识别高质量经验
      ↓
  建议创建 Guild 文档
      ↓
  用户审批 → 创建文档
```

---

### 功能 6：版本管理 / Version Management

```yaml
文档头部格式:
---
guild_version: 1.0
created: YYYY-MM-DD
updated: YYYY-MM-DD
author: [作者名]
review_cycle: 6months
---
```

---

## 📖 使用示例 / Usage Examples

### 示例 1：技术选型 / Example 1: Technology Selection

```
用户：帮我搭建一个网站

Guild Knowledge:
1. ✅ 读取相关 Guild 经验文档
2. ✅ 搜索最新技术栈和框架
3. ✅ 对比 Guild 建议 vs 最新方案
4. ✅ 回复:
   "根据 Guild 经验 + 最新搜索，推荐：
   - 技术栈：[根据需求推荐]
   - 框架：[现代框架]
   
   需要我开始实施吗？"
```

---

### 示例 2：发现新工具 / Example 2: Discovering New Tools

```
Guild Knowledge 发现:
- Guild 建议：[原有方案]
- 最新搜索：[新工具] 有更新

回复:
"Guild 经验推荐使用 [原有方案]。

但最新搜索发现：[新工具] 已更新

对比:
- 原有方案：[优点/缺点]
- 新方案：[优点/缺点]

建议：测试后决定是否更新 Guild 文档。
需要我测试吗？"
```

---

### 示例 3：月度审查 / Example 3: Monthly Review

```
时间：每月 1 号 09:00

生成报告:
"📊 Guild 月度审查报告 - [年月]

✅ 无需更新:
- [领域 A]：Guild 建议 [版本]，最新 [版本]

⚠️ 建议更新:
- [工具/技术]：发现新版本
  建议：[具体建议]

请审批:
- 回复"批准" → 应用修改
- 回复"跳过" → 本次不修改"
```

---

## 🔒 安全限制 / Safety Constraints

```yaml
修改限制:
  - 所有 Guild 文档修改 → 必须用户审批
  - 不能删除 Guild 文件
  - 不能移动 Guild 文件出 Guild/文件夹

审批模式:
  - 所有修改都需审批（无论大小）
```

---

## 📁 文件结构示例 / Example File Structure

```
Guild/
├── README.md           # Guild 文件夹说明
├── INDEX.md            # 文档索引
├── .guild_manifest.json # 机器可读清单
├── Guild_[主题 1].md    # 经验文档 1
├── Guild_[主题 2].md    # 经验文档 2
└── Guild_[主题 3].md    # 经验文档 3

.learnings/
├── LEARNINGS.md        # 学习记录
├── ERRORS.md           # 错误记录
└── FEATURE_REQUESTS.md # 功能请求
```

**注意**: 用户根据自己的项目创建 Guild 文档，以上仅为示例结构。

**Note**: Users create Guild documents based on their own projects. Above is example structure only.

---

## 🔄 与其他技能协作 / Integrations

本技能可独立工作，也可与其他技能协作：

**This skill works independently but can integrate with other skills:**

| 协作场景 / Integration | 说明 / Description |
|----------------------|-------------------|
| 学习记录 / Learning Capture | 从对话中提取经验 / Extract experience |
| 文档审查 / Document Review | 定期审查文档 / Periodic review |
| 经验推广 / Experience Sharing | 发布到 ClawHub / Share to ClawHub |

**注意**: 所有集成都是可选的。

**Note**: All integrations are optional.

---

## 📊 审查周期示例 / Example Review Cycles

| 文档类型 / Document Type | 周期 / Cycle | 内容 / Content |
|---------|---------|---------|
| 技术雷达 / Tech Radar | 每月 / Monthly | 技术更新 / Tech updates |
| 项目经验 / Project Experience | 6 个月 | 技术栈更新 / Stack updates |
| 安全规范 / Security Guidelines | 3 个月 | 最佳实践 / Best practices |

**注意**: 用户自定义审查周期。

**Note**: Users define their own review cycles.

---

## 📝 版本历史 / Version History

```
[YYYY-MM-DD] v1.0.1 - 更新 / Update
  - 添加中英文双语支持
  - 优化文件结构
  - 改进文档说明
  - Author: Pipiy416

[YYYY-MM-DD] v1.0.0 - 初始创建 / Initial Release
  - 创建 Guild Knowledge Skill
  - 核心原则："经验是参考，不是圣经"
  - 实现自动查阅 + 最新信息搜索
```

---

*经验是参考，不是圣经。保持开放，拥抱变化，用更好的方法！*

*Experience is a reference, not scripture. Stay adaptable, embrace change, use better methods!*
