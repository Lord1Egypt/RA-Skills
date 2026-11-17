---
name: news-search
description: 查询任意关键字相关的资讯新闻。适用于"有什么新闻"、"查一下XX资讯"等请求。
---

# 资讯查询

查询任意关键字相关的资讯新闻。

## 什么时候用

用户想查询以下内容时：
- 查看某主题的新闻资讯
- 查询热点事件相关资讯
- 获取市场动态、行情分析

## 怎么用

### 脚本调用

```bash
# 查询资讯（默认5条）
python3 scripts/jdjr_query_news.py 黄金

# 查询资讯（指定条数）
python3 scripts/jdjr_query_news.py 特朗普 10
python3 scripts/jdjr_query_news.py A股 5
python3 scripts/jdjr_query_news.py 股市 3
```

### 意图识别

| 用户说 | 使用脚本 |
|--------|----------|
| 有什么新闻/资讯 | 根据关键字调用 `jdjr_query_news.py` |
| 查一下X资讯/新闻 | `jdjr_query_news.py X` |
| X有什么消息 | `jdjr_query_news.py X` |

## 怎么对用户输出（严格按照以下格式输出）

详细格式规范见 [jdjr-news_output_format.md](./jdjr-news_output_format.md)

Agent 输出时按该文档格式渲染：可视化、专业、易懂，**每条资讯必带「🔗 查看更多 →」跳转链接（用 `url` 字段）**，结尾原样保留来源标注。

## 失败处理

- 接口失败 → "服务异常，请稍后重试"
- 查不到数据 → "未找到关于「关键字」的相关资讯"
