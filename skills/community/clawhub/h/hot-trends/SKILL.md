---
name: hot-trends
description: "抓取真实热搜数据，支持百度热搜、头条热搜、GitHub Trending。用于需求挖掘、趋势分析、市场洞察。触发词：热搜、热榜、趋势、trending、挖掘需求。"
metadata:
  openclaw:
    emoji: "🔥"
    category: "trending"
    tags: ["baidu", "toutiao", "github", "trending", "hot", "需求挖掘"]
    requires:
      bins: ["python3"]
---

# 🔥 热搜趋势监控

真实抓取热搜数据，零API Key，纯公开接口。

## 支持平台

| 平台 | 数据源 | 状态 |
|------|--------|------|
| 百度热搜 | top.baidu.com API | ✅ |
| 头条热搜 | toutiao.com API | ✅ |
| GitHub | github.com/trending | ✅ |

## 使用方式

```bash
# 某个平台
python3 skills/hot-trends/hot.py baidu -n 20
python3 skills/hot-trends/hot.py toutiao -n 20
python3 skills/hot-trends/hot.py github -n 20
python3 skills/hot-trends/hot.py github -l python  # 指定语言

# 全部
python3 skills/hot-trends/hot.py all

# 关键词过滤（需求挖掘用）
python3 skills/hot-trends/hot.py all -k AI
python3 skills/hot-trends/hot.py baidu -k 大模型 -n 50
```
