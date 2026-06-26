---
name: 内容裂变工厂
description: 小红书热点追踪 × 爆文生成 × 知识卡片 × 公众号发布全链路自动化
category: AI
triggers: 小红书选题, 内容创作, 热点爆文, 知识卡片, 跨平台发布, 选题雷达
---

# 内容裂变工厂 (内容裂变工厂)

> 热点追踪 → AI 分析 → 爆文生成 → 知识卡片 → 公众号发布 → 飞书存档

## 🎯 解决痛点

- ❌ 每天刷小红书、微博、知乎热点，找选题耗时 1-2 小时
- ❌ 找到选题后还要手动整理素材、写文章，效率低
- ❌ 好不容易写完文章，配图还要另外找工具制作
- ❌ 发布到多个平台需要重复操作，容易遗漏
- ❌ 辛苦产出的内容无法沉淀为团队知识资产

## 💡 解决方案

```
小红书热搜 + 微博热搜 + 知乎热榜（Agent-Reach）
        ↓
┌─────────────────────────────┐
│  summarize (AI)             │ → 热点分析、话题价值评估、选题建议
└────────────┬────────────────┘
             │ 分析结果
      ┌──────▼──────┐
      │ card-renderer│ → 生成 Mac/赛博朋克/包豪斯风知识卡片
      └──────┬──────┘
             │ 卡片图
      ┌──────▼──────────────┐
      │ wechat-article-pro  │ → 生成 3000-5000 字公众号深度文章
      └──────┬──────────────┘
             │ 完整文章
      ┌──────▼────────┐
      │  feishu_doc  │ → 发布至飞书存档，永久沉淀
      └──────────────┘
```

## 📦 包含 Skills

| Skill | 作用 | 调用顺序 |
|-------|------|---------|
| Agent-Reach | 抓取小红书/微博/知乎热搜榜 | 1 |
| summarize | AI 分析热点趋势、评估话题价值 | 2 |
| card-renderer | 生成精美的知识卡片图 | 3 |
| wechat-article-pro | 生成公众号风格深度文章 | 4 |
| feishu_doc | 发布存档至飞书文档 | 5 |

## 🔧 前置要求

1. **Agent-Reach**：已配置小红书、微博、知乎抓取权限
2. **card-renderer**：已安装并配置图像生成后端
3. **feishu_doc**：飞书机器人已配置文档写入权限
4. **wechat-article-pro**：AI 写作模型已配置

## 📝 使用方法

### 触发方式

```
/内容裂变工厂
生成今日内容选题
小红书爆文生成
热点文章一键搞定
```

### 手动执行

```bash
# 方式 1：通过 OpenClaw
openclaw run 内容裂变工厂

# 方式 2：指定行业领域
openclaw run 内容裂变工厂 --niche 科技

# 方式 3：仅生成草稿（不发布）
openclaw run 内容裂变工厂 --draft true
```

### 定时执行（推荐）

```bash
# 每天早上 8:30 UTC (=北京时间16:30) 自动生成当天选题
openclaw cron add \
  --name "每日内容裂变工厂" \
  --schedule "30 8 * * *" \
  --skill 内容裂变工厂
```

## 🔄 工作流详情

### Step 1: 热点抓取

```yaml
步骤: 1
技能: Agent-Reach
输入:
  tasks:
    - search_xiaohongshu_trending
    - search_weibo_hot
    - search_zhihu_hot
  params:
    niche: "${inputs.niche}"
    limit: 20
输出:
  trending_data: ${step1.trending.json}
```

### Step 2: AI 趋势分析

```yaml
步骤: 2
技能: summarize
输入:
  content: ${step1.trending_data}
  tasks:
    - analyze_trending_topics
    - score_topic_viral_potential
    - suggest_content_angles
  outputFormat: structured_json
输出:
  analysis: ${step2.analysis.json}
  top_topics: ${step2.topics.json}
  angles: ${step2.angles.json}
```

### Step 3: 生成知识卡片

```yaml
步骤: 3
技能: card-renderer
输入:
  topics: ${step2.top_topics}
  styles: ["mac", "cyberpunk", "bauhaus"]
  outputFormat: image
输出:
  cards: ${step3.cards[]}
```

### Step 4: 生成公众号文章

```yaml
步骤: 4
技能: wechat-article-pro
输入:
  topic: "${step2.top_topics[0]}"
  angles: "${step2.angles[0]}"
  style: 公众号深度文章风格
  wordCount: 3500
  reference_cards: ${step3.cards}
输出:
  article: ${step4.article_md}
  title: ${step4.title}
```

### Step 5: 发布存档至飞书

```yaml
步骤: 5
技能: feishu_doc
输入:
  action: create
  title: "内容裂变 | ${step4.title} | $(date +%Y-%m-%d)"
  content: |
    # ${step4.title}

    ${step4.article_md}

    ## 配图卡片
    ![知识卡片](${step3.cards[0]})

    ## 选题分析
    ${step2.analysis}
  grant_to_requester: true
输出:
  doc_url: ${step5.docUrl}
  doc_id: ${step5.docId}
```

## 📊 输出示例

### 生成的文章结构

```markdown
# 【热点解读】为什么这个话题突然爆了？

> 选题来源：小红书热搜 #xxx | 微博热搜 #yyy | 知乎热榜 #zzz

## 🔥 热点速览
- 热度指数：98/100
- 爆发时间：2026-04-29
- 覆盖人群：25-35岁都市女性
- 关联话题：#xxx #yyy #zzz

## 📊 话题分析
[AI 深度分析热点成因、传播路径、用户情绪]

## 💡 内容创作角度建议
1. 情感共鸣角度
2. 实用干货角度
3. 争议话题角度
...

## ✍️ 核心内容
[3000-5000字深度文章]

## 📌 配图建议
[针对每个章节的配图提示]

---
*由内容裂变工厂自动生成 | $(date)*
```

## ⚙️ 自定义配置

### 修改热点来源

编辑 `workflow.json` 中的 sources 配置：

```json
{
  "sources": {
    "xiaohongshu": {
      "enabled": true,
      "categories": ["时尚", "美食", "科技", "职场"]
    },
    "weibo": {
      "enabled": true,
      "types": ["hot", "fellow", "notice"]
    },
    "zhihu": {
      "enabled": true,
      "categories": ["热搜", "推荐"]
    }
  }
}
```

### 修改卡片风格

```json
{
  "card_styles": ["mac", "cyberpunk", "bauhaus"],
  "card_count": 3
}
```

## 🔒 安全说明

- 抓取内容仅用于内容创作灵感
- 尊重各平台内容版权，创作内容需原创
- 飞书文档权限默认为创建者私有

## ⚠️ 注意事项

1. **选题时效性**：热点生命周期通常 24-72h，建议尽早创作发布
2. **内容原创**：AI 生成内容需二次加工，确保原创性
3. **平台规则**：各平台有不同的推荐机制，请遵守平台规范
4. **频率控制**：建议每日执行 1 次，避免过度采集

## 🚀 扩展用法

### 1. 多话题并行生成

```bash
# 每次生成 3 个不同角度的内容
openclaw run 内容裂变工厂 --count 3 --parallel true
```

### 2. 指定话题创作

```bash
# 针对特定话题深度创作
openclaw run 内容裂变工厂 --topic "AI耳机市场分析"
```

### 3. 输出草稿不发布

```bash
# 仅生成内容，不发布到任何平台
openclaw run 内容裂变工厂 --draft true
```

## 📞 故障排除

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| 热点抓取为空 | Agent-Reach 未配置 | 检查小红书/微博 Cookie 配置 |
| 卡片生成失败 | card-renderer 后端异常 | 确认图像生成服务运行正常 |
| 文章生成失败 | 分析内容不足 | 增加热点来源或 RSS 补充 |
| 飞书发布失败 | 权限不足 | 确认 feishu_doc 机器人权限 |
