---
name: knowledge-card-factory
version: 1.0.0
description: 智能知识卡片生产流水线。自动化完成热点发现、内容深挖、AI 配图、多端发布的完整流程。适用于自媒体运营、知识分享、品牌营销等场景。
author: OpenClaw AgentSkills Architect
tags:
  - content-creation
  - automation
  - social-media
  - ai-workflow
  - productivity
requires:
  - brave-search
  - agent-reach
  - nano-banana-pro
  - xiaohongshu-mcp
optional:
  - card-renderer
  - weather
  - feishu-doc
  - summarize
---

# Knowledge Card Factory

智能知识卡片生产流水线 — 从选题到发布的全自动化解决方案。

## 何时使用

当用户需要：
- 快速生产社交媒体内容
- 制作知识卡片/信息图
- 自动化内容发布流程
- 热点追踪与借势营销

触发关键词：
- "做一张知识卡片"
- "帮我生成内容发小红书"
- "自动化内容生产"
- "热点内容创作"

## 工作流程

### 1. 热点发现 (brave-search)

```bash
# 使用 brave-search 搜索热点
# 示例: 搜索 AI 行业趋势
search_query = "{用户指定的主题} 最新 趋势 2026"
```

**输出**:
- 热点话题列表
- 相关新闻报道
- 关键数据点

### 2. 内容深挖 (agent-reach)

```bash
# 使用 agent-reach 跨平台抓取
# 支持: Twitter/X, 小红书, B站, 公众号, 微博, LinkedIn
```

**操作**:
1. 基于热点话题搜索多平台内容
2. 提取核心观点和数据
3. 生成内容摘要

### 3. 卡片创作

#### 方案 A: AI 配图 (nano-banana-pro)
```
提示词模板:
"Create a {style} style illustration about {topic}, 
featuring {key_elements}, modern, clean design"
```

#### 方案 B: 卡片渲染 (card-renderer)
```
支持风格:
- Mac Pro 风格
- 赛博朋克
- 包豪斯
- 清新简约
```

### 4. 多端发布 (xiaohongshu-mcp)

```yaml
发布配置:
  platform: xiaohongshu
  content:
    title: {生成的标题}
    body: {生成的正文}
    images: [{图片路径}]
    tags: [{话题标签}]
```

## 使用示例

### 示例 1: 制作 AI 趋势卡片

**用户指令**:
> "帮我做一张 AI Agent 发展趋势的知识卡片，发到小红书"

**执行步骤**:

```python
# Step 1: 热点发现
topics = brave_search("AI Agent 发展趋势 2026")

# Step 2: 内容深挖
content = agent_reach(
    platforms=["twitter", "xiaohongshu", "wechat"],
    query="AI Agent trends"
)

# Step 3: 生成配图
image = nano_banana_pro(
    prompt="AI Agent ecosystem diagram, futuristic style",
    size="1024x1024"
)

# Step 4: 发布
result = xiaohongshu_publish(
    title="2026 AI Agent 五大趋势",
    content=content.summary,
    images=[image]
)
```

**输出**:
```
✅ 知识卡片已发布
📄 标题: 2026 AI Agent 五大趋势
🔗 链接: https://xiaohongshu.com/note/xxx
👀 预览: [卡片图片]
```

### 示例 2: 天气出行指南

**用户指令**:
> "帮我做一张北京周末出行天气指南"

**执行步骤**:

```python
# Step 1: 获取天气
weather_data = weather("北京", days=3)

# Step 2: 搜索热门景点
spots = brave_search("北京周末热门景点")

# Step 3: 渲染卡片
card = card_renderer(
    template="清新简约",
    data={
        weather: weather_data,
        recommendations: spots
    }
)
```

## 配置选项

### workflow.json

```json
{
  "name": "knowledge-card-factory",
  "version": "1.0.0",
  "stages": [
    {
      "id": "discover",
      "skills": ["brave-search"],
      "config": {
        "result_limit": 10,
        "freshness": "week"
      }
    },
    {
      "id": "research",
      "skills": ["agent-reach"],
      "config": {
        "platforms": ["twitter", "xiaohongshu", "wechat"],
        "max_results": 20
      }
    },
    {
      "id": "create",
      "skills": ["nano-banana-pro", "card-renderer"],
      "config": {
        "default_style": "cyberpunk",
        "image_size": "1024x1024"
      }
    },
    {
      "id": "publish",
      "skills": ["xiaohongshu-mcp"],
      "config": {
        "auto_publish": false,
        "require_confirmation": true
      }
    }
  ],
  "error_handling": {
    "retry": 3,
    "on_failure": "save_draft"
  }
}
```

## 错误处理

| 错误类型 | 处理方式 |
|----------|----------|
| 搜索失败 | 重试 3 次，使用缓存数据 |
| 配图生成失败 | 降级到文字卡片 |
| 发布失败 | 保存本地草稿，通知用户 |

## 注意事项

1. **发布前确认**: 默认开启 `require_confirmation`，确保用户审核后再发布
2. **内容质量**: 生成的内容需要用户确认，避免 AI 幻觉
3. **图片版权**: AI 生成图片需标注来源
4. **平台规则**: 不同平台有不同发布限制，注意合规

## 扩展能力

- **添加新渠道**: 实现对应平台的 Skill 接口
- **自定义模板**: 在 templates/ 目录添加卡片模板
- **数据源扩展**: 在 sources/ 目录添加新数据源