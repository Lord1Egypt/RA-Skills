# Knowledge Card Factory - 智能知识卡片生产流水线

## 业务场景

在社交媒体时代，内容创作者面临一个核心痛点：**高质量内容生产效率低下**。一篇深度文章从选题、调研、撰写到设计配图，往往需要数小时甚至数天。

**Knowledge Card Factory** 是一个端到端的内容生产自动化解决方案，将 AI 技术栈整合为一条高效流水线，实现「选题 → 调研 → 创作 → 设计 → 发布」的全流程自动化。

---

## 痛点分析

| 痛点 | 传统方式 | Knowledge Card Factory |
|------|----------|------------------------|
| 选题耗时 | 手动浏览热点，耗时长 | 自动抓取趋势热点 |
| 调研困难 | 多平台切换，信息碎片化 | 一键聚合多源数据 |
| 写作瓶颈 | 创意枯竭，效率低 | AI 辅助生成框架 |
| 配图繁琐 | 找图/设计耗时 | 自动生成高质量配图 |
| 发布分散 | 多平台逐一发布 | 统一发布到多渠道 |

---

## Skill 编排图谱

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Knowledge Card Factory                            │
│                                                                       │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐       │
│  │ Stage 1  │───▶│ Stage 2  │───▶│ Stage 3  │───▶│ Stage 4  │       │
│  │ 热点发现 │    │ 内容深挖 │    │ 卡片创作 │    │ 多端发布 │       │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘       │
│       │              │              │              │                 │
│       ▼              ▼              ▼              ▼                 │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐       │
│  │brave-    │    │agent-    │    │nano-     │    │xiaohongshu│      │
│  │search    │    │reach     │    │banana-pro│    │-mcp      │       │
│  │          │    │          │    │          │    │          │       │
│  │ 天气/新闻│    │ 多平台   │    │ AI 配图  │    │ 小红书   │       │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘       │
│                                                                       │
│  可选扩展:                                                            │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐                        │
│  │card-     │    │wechat-   │    │feishu-   │                        │
│  │renderer  │    │article-  │    │doc       │                        │
│  │ 样式渲染 │    │pro       │    │ 内部协同 │                        │
│  └──────────┘    └──────────┘    └──────────┘                        │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 编排技能详解

### Stage 1: 热点发现 (brave-search)
- **能力**: 实时搜索热点话题、趋势新闻
- **输入**: 关键词或行业领域
- **输出**: 热点话题列表 + 相关数据

### Stage 2: 内容深挖 (agent-reach)
- **能力**: 跨平台抓取 Twitter、小红书、B站、公众号等
- **输入**: 热点话题
- **输出**: 多源内容聚合 + 核心观点提取

### Stage 3: 卡片创作 (nano-banana-pro + card-renderer)
- **能力**: 
  - `nano-banana-pro`: AI 生成高质量配图
  - `card-renderer`: 多风格卡片渲染 (Mac Pro、赛博朋克、包豪斯)
- **输入**: 内容 + 风格偏好
- **输出**: 精美知识卡片图片

### Stage 4: 多端发布 (xiaohongshu-mcp)
- **能力**: 自动发布到小红书等社交平台
- **输入**: 文案 + 图片
- **输出**: 发布结果 + 链接

---

## 使用示例

### 示例 1: AI 行业热点卡片

```bash
# 用户指令
"帮我制作一张关于「AI Agent 发展趋势」的知识卡片，发到小红书"

# 执行流程
1. brave-search: 搜索 "AI Agent 2026 trends"
2. agent-reach: 抓取 Twitter/X、公众号相关文章
3. nano-banana-pro: 生成科技风格配图
4. card-renderer: 渲染为赛博朋克风格卡片
5. xiaohongshu-mcp: 发布到小红书

# 输出
✅ 知识卡片已发布: https://xiaohongshu.com/note/xxx
```

### 示例 2: 周末天气出行指南

```bash
# 用户指令
"帮我做一张北京周末出行天气指南卡片"

# 执行流程
1. brave-search + weather: 获取北京周末天气
2. agent-reach: 搜索北京热门景点、活动
3. card-renderer: 渲染为清新风格卡片
4. 可选发布到飞书文档存档

# 输出
✅ 卡片已生成: /output/2026-03-22-beijing-weekend.png
```

---

## 技术架构

```yaml
# workflow.yaml
name: knowledge-card-factory
version: 1.0.0
description: 智能知识卡片生产流水线

stages:
  - id: discover
    name: 热点发现
    skills:
      - brave-search
      - weather (可选)
    outputs:
      - topics: 热点话题列表
      - data: 相关数据

  - id: research
    name: 内容深挖
    skills:
      - agent-reach
    inputs:
      - topics
    outputs:
      - content: 聚合内容
      - insights: 核心观点

  - id: create
    name: 卡片创作
    skills:
      - nano-banana-pro
      - card-renderer
    inputs:
      - content
      - insights
    outputs:
      - card_image: 知识卡片图片
      - caption: 配套文案

  - id: publish
    name: 多端发布
    skills:
      - xiaohongshu-mcp
      - feishu-doc (可选)
    inputs:
      - card_image
      - caption
    outputs:
      - publish_url: 发布链接

error_handling:
  retry: 3
  fallback:
    - 保存本地草稿
    - 通知用户确认
```

---

## 安装依赖 Skills

```bash
# 安装所需技能
clawhub install brave-search
clawhub install agent-reach
clawhub install nano-banana-pro
clawhub install card-renderer
clawhub install xiaohongshu-mcp
```

---

## 适用场景

- **自媒体运营**: 快速生产高质量内容
- **知识分享**: 技术总结、学习笔记可视化
- **品牌营销**: 热点借势、事件营销
- **企业内训**: 知识卡片培训材料
- **个人品牌**: 建立专业形象

---

## 扩展性

本 Combo 支持灵活扩展：

- **添加新渠道**: 接入微信公众号 (wechat-article-pro)
- **增强分析**: 加入 summarize 技能做内容摘要
- **团队协作**: 接入 feishu-doc 实现团队协同
- **多语言**: 接入翻译技能支持国际化

---

## 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| 1.0.0 | 2026-03-22 | 初始版本，支持完整流水线 |

---

**作者**: OpenClaw AgentSkills 架构师
**许可**: MIT