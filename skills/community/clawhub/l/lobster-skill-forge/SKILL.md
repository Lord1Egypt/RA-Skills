---
name: skill-forge
displayName: SkillForge 技能熔炉
slug: skill-forge
description: "自动化技能融合生产线——输入需求描述，自动分析现有技能库，生成融合方案+SKILL.md+测试框架。融合Skill Factory + Automation Workflows + 一人财团理念，实现从需求到可部署技能的全自动流水线。核心能力：(1) 技能分析引擎 (2) 融合方案生成 (3) 自动脚手架 (4) 批量生产线 (5) AI Agent一键部署模板。"
version: "1.0.0"
author: "智美人团队"
tags:
  - skill-generation
  - automation
  - pipeline
  - fusion
  - scaffold
  - productivity
metadata:
  openclaw:
    emoji: "🔨"
    requires:
      skills: [skill-factory, automation-workflows, agent-team-orchestration]
---

# 🔨 SkillForge 技能熔炉

> **需求 → 技能 → Agent → 变现，全自动一条龙。**


## 示例

### 示例1：基础使用

```
用户：帮我处理一下业务需求
助手：好的，正在启用skill forge技能来处理...
```

### 示例2：进阶场景

```
用户：需要批量处理
助手：已启动批量模式，处理中...
```


## 限制与局限

- 需要稳定网络连接（API调用依赖）
- 处理超大数据集时可能会有延迟
- 建议在OpenClaw环境下运行以获得最佳效果
- 某些高级功能需要特定模型支持


## 前置条件

| 条件 | 说明 |
|------|------|
| OpenClaw | 需要OpenClaw运行时环境 |
| 网络 | 稳定的互联网连接 |
| API Key | 按需配置第三方服务密钥 |


## 版本历史

| 版本 | 日期 | 变更说明 |
|------|------|---------|
| 1.0.0 | 2026-05-01 | 初始版本发布，由SkillForge v3.0融合生成 |

## 核心理念

把技能的"研发"变成一条自动化流水线：

```
┌─────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
│ 需求输入  │──▶│ 技能设计  │──▶│ 代码生成  │──▶│ 测试发布  │
│ 一句话    │   │ 融合匹配  │   │ 脚手架   │   │ 打包上线  │
└─────────┘   └──────────┘   └──────────┘   └──────────┘
      │                            │                │
      ▼                            ▼                ▼
  自动分析需求               自动生成模板          一键发布
  匹配最佳融合源            脚本+测试+文档        clawhub publish
```

## 三大引擎

### 1️⃣ 技能分析引擎（SAE）
输入需求，自动分析：
- 现有技能库中哪些能融合（匹配tag和description）
- 缺乏哪些依赖需要补充
- 推荐最佳的融合组合

```
输入："帮我做个小红书自动发帖工具"
输出：
  ✅ 匹配到 caption（文案）+ hashtag（标签）+ content-pilot（内容运营）
  ❌ 缺 publish 相关技能，建议安装
  🎯 推荐融合方案：caption + hashtag + automation-workflows
```

### 2️⃣ 融合方案生成器（FBG）
自动输出完整融合文档：
```markdown
## 融合方案：[技能名]
### 融合来源
| 源技能 | 角色 | 融合点 |
|--------|------|--------|
| XX技能 | 文案 | 提供XX能力 |
| YY技能 | 发布 | 提供YY能力 |

### 新增能力
1. ...
### 使用方式
...
```

### 3️⃣ AI Agent生产线（AAP）
把融合技能转化为可部署的Agent模板：
- 生成Agent配置
- 生成任务编排流程
- 生成部署脚本

## 使用方式

```
# 单技能生成
skill-forge> 生成 "番茄工作法管理" 技能
→ 分析库 → 找不到直接匹配 → 建议 fusion recipe+taskr+calendar
→ 自动生成 SKILL.md + scripts/test.sh + examples

# 技能融合
skill-forge> 融合 travel + expense = TravelBiz
→ 分析两个技能的接口 → 生成融合点图 → 输出完整文档

# 批量生产线
skill-forge> 生产线：电商领域技能包
→ 自动扫描 → 发现5个可用源 → 生成3个融合方案 → 批量构建

# Agent部署
skill-forge> 部署 TravelBiz 为 Agent
→ 生成 agent-config.json + workflow.md + deploy.sh
```

## 预置生产线模板

### 1. 内容创作线
```
caption + hashtag + quote + newsletter → ContentPilot（已完成）
↑ 再加 video-script-creator → 视频创作全栈
```

### 2. 电商变现线
```
ecom-intel + price-tracker + review → EcomIntel（已完成）
↑ 再加 social-media-publisher → 全自动发帖+分析
```

### 3. 企业办公线
```
travel + expense + receipt + invoice → TravelBiz（已完成）
↑ 再加 calendar + reminder → 出差全程自动化
```

### 6. 浏览器自动化发布（融合browser-use）

技能生成后自动发布到多平台：

```
skill-forge> 发布 skill-forge 到视频号
skill-forge> 发布 ecom-intel 到抖音
```

**流程：**
1. 生成技能/内容
2. browser-use自动打开目标平台
3. 填写发布表单
4. 确认发布
5. 截图回传发布成功截图

**适用场景：**
- 视频号自动发视频
- 抖音自动发布
- 小红书自动发笔记
- 竞品数据定时监控

## 参考实现

- `skill-factory` — 基础技能生成引擎
- `automation-workflows` — 工作流自动化设计
- `agent-team-orchestration` — Agent团队编排
- `one-man-conglomerate` — 一人财团理念（协作+辩论）
- `browser-use` — 浏览器自动化发布
- `self-improving-agent` — 自我进化
