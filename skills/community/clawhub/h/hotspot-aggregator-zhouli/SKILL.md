---
name: hotspot-aggregator
version: 1.0.0
description: 🔥 热点聚合监控 - 一站式聚合微博/百度/知乎/抖音热搜榜，自动生成每日热点报告，支持关键词订阅推送。适用于自媒体运营、内容创作、市场分析等场景。
author: 赚钱小能手
metadata:
  openclaw:
    emoji: 🔥
    category: monitoring
    keywords:
      - hotspot
      - trending
      - news
      - aggregator
      - social-media
      - content
      - 热点
      - 热搜
      - 舆情监控
    triggers:
      - 热点
      - 热搜
      - 今日热点
      - 热点报告
      - 热点监控
      - 热榜
      - 微博热搜
      - 百度热搜
      - 知乎热榜
      - 抖音热搜
      - 今日热点
      - 热点聚合
      - 舆情
      - 内容监控
---

# 🔥 热点聚合监控

**一站式聚合全网热搜，让热点触手可及**

聚合微博、百度、知乎、抖音四大平台热搜数据，自动生成热点报告，支持关键词订阅。

---

## ✨ 核心功能

| 功能 | 描述 |
|------|------|
| 📊 **多平台聚合** | 微博热搜、百度热搜、知乎热榜、抖音热搜 |
| 📝 **每日报告** | 自动生成结构化热点分析报告 |
| 🔔 **关键词订阅** | 订阅感兴趣的关键词，匹配即推送 |
| 📈 **趋势分析** | 分析热点分布、变化趋势 |

---

## 🚀 快速开始

### 安装

```bash
clawhub install hotspot-aggregator
```

### 获取热点数据

```bash
# 获取所有平台热搜
cd skills/hotspot-aggregator
./scripts/fetch-hotspots.sh all

# 获取单个平台
./scripts/fetch-hotspots.sh weibo    # 微博
./scripts/fetch-hotspots.sh baidu    # 百度
./scripts/fetch-hotspots.sh zhihu    # 知乎
./scripts/fetch-hotspots.sh douyin   # 抖音
```

### 生成热点报告

```bash
# 生成今日报告
./scripts/generate-report.sh

# 报告位置: /root/clawd/memory/hotspots/YYYY-MM-DD.md
```

### 关键词订阅

```bash
# 添加订阅
./scripts/subscribe.sh add "AI"
./scripts/subscribe.sh add "科技"

# 查看订阅列表
./scripts/subscribe.sh list

# 删除订阅
./scripts/subscribe.sh remove "AI"

# 检测关键词匹配
./scripts/check-keywords.sh
```

---

## 📋 输出示例

### 热点报告格式

```markdown
# 🔥 今日热点报告 - 2026-03-20

## 📱 微博热搜 TOP10

1. 两会热点议题 🔥 123万热度
2. AI技术新突破引发热议 💬 98万热度
...

## 🔍 百度热搜 TOP10

1. 最新科技动态 🔥 搜索量: 89万
2. 国际新闻头条 💬 搜索量: 78万
...

## 📊 热点分析

- 🔬 科技类: 35%
- 🎬 娱乐类: 28%
- 📰 社会类: 22%
- 💼 财经类: 10%
- 🎨 其他: 5%

## 🎯 订阅关键词匹配

您订阅的关键词 [AI] 匹配到:
- AI技术新突破 (微博 #2)
- 最新科技动态 (百度 #1)
```

---

## ⚙️ 配置

配置文件 `config.json`：

```json
{
  "platforms": ["weibo", "baidu", "zhihu", "douyin"],
  "reportTime": "08:00",
  "keywords": ["AI", "科技"],
  "notifyChannel": ""
}
```

### 启用真实API

默认使用演示数据。要启用真实API：

```bash
# 设置环境变量
export USE_REAL_API=true
export PROXY="http://your-proxy:port"  # 可选，如需代理

./scripts/fetch-hotspots.sh all
```

---

## 🔄 定时任务

配合 cron 实现每日自动推送：

```bash
# 每天早上8点推送
0 8 * * * cd /root/clawd/skills/hotspot-aggregator && ./scripts/generate-report.sh
```

---

## 📖 使用场景

| 场景 | 用法 |
|------|------|
| **自媒体运营** | 每日获取热点，选题参考 |
| **内容创作** | 订阅领域关键词，获取灵感 |
| **市场分析** | 追踪行业热点趋势 |
| **舆情监控** | 订阅品牌关键词，及时发现舆情 |

---

## ⚠️ 注意事项

1. **API限制**: 真实API可能有访问频率限制
2. **代理需求**: 部分平台需要代理访问
3. **演示模式**: 默认使用模拟数据演示功能
4. **更新频率**: 建议每小时最多请求一次

---

## 🔧 高级用法

### 自定义数据源

编辑 `scripts/fetch-hotspots.sh` 添加新平台：

```bash
# 添加新平台
fetch_custom() {
    local url="https://your-api-endpoint"
    local output="$DATA_DIR/custom_${DATE}_${TIME}.json"
    # ... 处理逻辑
}
```

### 报告自定义

编辑 `assets/report-template.md` 自定义报告格式。

---

## 📊 数据源

| 平台 | API | 说明 |
|------|-----|------|
| 微博 | weibo.com/ajax/side/hotSearch | 需登录/代理 |
| 百度 | top.baidu.com/api/board | 公开API |
| 知乎 | zhihu.com/api/v3/feed/topstory | 需代理 |
| 抖音 | api.oioweb.cn (聚合) | 第三方API |

---

**让热点触手可及 🔥**
