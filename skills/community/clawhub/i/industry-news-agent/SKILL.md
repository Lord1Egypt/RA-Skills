---
name: industry-news-agent
description: 每日行业资讯追踪助手。通过 RSS 订阅获取科技媒体的最新文章（最近24小时），过滤后推送。支持自定义关键词和新闻来源媒体。
version: 3.1.1
---

# 行业资讯小哨兵

通过 RSS 订阅获取科技媒体最新文章，只推送昨天的资讯。

---

## ⚠️ 核心特点

- ✅ **RSS 订阅** - 直接获取媒体最新文章，更准确
- ✅ **只抓昨天** - 确保时效性，不重复推送
- ✅ **关键词过滤** - 只看关心的内容
- ✅ **自主配置** - 可添加你关注的媒体和关键词

---

## 📊 获取逻辑

```
1. 访问 RSS 订阅源 → 获取媒体最新文章
2. 过滤最近24小时的文章 → 根据 pubDate
3. 过滤关键词 → AI/智能体/大模型等（可自主配置）
4. 关注动态 → 发布/上线/合作/融资/商业化/技术突破
5. 排除广告/招聘/培训/软文
6. 输出 → 标题 + 日期 + 媒体名称 + 摘要(100字) + 链接
```

---

## 🚀 快速开始

### 安装后配置

**1. 修改配置文件**
```bash
nano ~/.openclaw/workspace/skills/industry-news-agent/config.yaml
```

**2. 测试运行**
```bash
python3 ~/.openclaw/workspace/skills/industry-news-agent/scripts/fetch_news.py
```

---

## ⚙️ 配置示例

```yaml
# RSS 订阅源（可自主添加你关注的媒体）
rss_sources:
  - name: 36氪
    url: https://36kr.com/feed
  - name: 虎嗅
    url: https://www.huxiu.com/rss/0.xml
  - name: 雷锋网
    url: https://www.leiphone.com/feed

# 关注关键词（可自主配置）
keywords_include:
  - AI
  - 智能体
  - 大模型
  - 发布
  - 融资
  - 技术突破

# 排除关键词
keywords_exclude:
  - 招聘
  - 培训
  - 广告

# 结果数量
max_results_per_source: 5
max_total_results: 15
```

---

## 📰 已配置的媒体

### 科技媒体
| 媒体 | 说明 |
|------|------|
| 36氪 | 创投科技媒体 |
| 虎嗅 | 商业科技媒体 |
| 雷锋网 | AI/智能硬件 |
| 少数派 | 数字生活效率 |
| 爱范儿 | 科技数码媒体 |

### 财经媒体
| 媒体 | 说明 |
|------|------|
| 金融时报中文 | 国际财经 |

### 科学媒体
| 媒体 | 说明 |
|------|------|
| Science Daily | 科学新闻 |
| Nature | 顶级学术期刊 |

---

## 📤 输出示例

```
📰 行业资讯 - 2026-03-25
========================================

### 1. 速腾聚创首次实现单季盈利
**日期**：2026-03-25
**媒体**：36氪

**摘要**：3月25日，速腾聚创公布2025年第四季度及全年业绩报告。财报显示，2025年全年，速腾聚创实现营收约19.41亿元...

**链接**：https://36kr.com/p/37397129...

---

共 12 条资讯
```

---

## 🔧 使用方式

### 手动运行
```bash
python3 ~/.openclaw/workspace/skills/industry-news-agent/scripts/fetch_news.py
```

### 设置每日自动推送
```bash
(crontab -l 2>/dev/null; echo "0 9 * * * python3 ~/.openclaw/workspace/skills/industry-news-agent/scripts/fetch_news.py") | crontab -
```

---

## ❓ 常见问题

### Q: 如何添加新的 RSS 源？

**A:** 编辑 `config.yaml`，添加：
```yaml
rss_sources:
  - name: 媒体名称
    url: https://example.com/feed
```

### Q: 如何修改关键词？

**A:** 编辑 `config.yaml`，修改 `keywords_include` 和 `keywords_exclude`。

---

## 📝 更新日志

- **v3.1.0** - 🔧 改为获取最近24小时文章；修复 pubDate 解析 bug（Element 布尔判断问题）
- **v3.0.2** - 修复日期过滤过严导致返回空结果的问题
- **v3.0.0** - 新增8个RSS源（科技/财经/科学），优化关键词过滤，输出增加日期
- **v2.0.1** - 摘要长度改为200字
- **v2.0.0** - 改用 RSS 订阅，无需 API Key
