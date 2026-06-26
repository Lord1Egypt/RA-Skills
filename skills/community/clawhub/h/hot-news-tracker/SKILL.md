---
name: "hot-news-tracker"
description: "追踪今日头条热点榜单或按关键词搜索新闻资讯。当用户想了解当前热点、今日热榜、实时新闻、热搜排行，或想搜索某个话题/关键词的相关新闻时调用。常见表达：'今天有什么热点'、'最近发生了什么大事'、'帮我看看热搜'、'搜一下XX的新闻'、'XX最新动态'、'有没有关于XX的新闻'、'今天的热门话题'。"
---

# 热点新闻追踪指南

## 能力说明

通过 `gnomic` CLI 工具接入今日头条数据源，支持两种使用方式：

- **获取热榜**：实时拉取头条热榜 Top 50，含热度值和跳转链接
- **关键词搜索**：搜索指定话题的相关新闻，含摘要、媒体来源和分类标签

---

## 使用方式

### 获取今日头条热榜

```bash
gnomic news hot
```

**JSON 输出结构：**
```json
{
  "success": true,
  "data": {
    "code": 200,
    "data": {
      "name": "toutiao",
      "type": "热榜",
      "total": 50,
      "updateTime": "2026-04-02 09:49:17",
      "link": "https://www.toutiao.com/",
      "data": [
        {
          "index": 0,
          "title": "热点标题",
          "hot_value": "34480552",
          "image_url": "封面图片URL",
          "url": "https://www.toutiao.com/trending/xxxxx/",
          "mobilUrl": "移动端链接"
        }
      ]
    }
  }
}
```

> `data.data.data` 为热榜条目数组，按 `index` 升序排列（0 = 最热），`hot_value` 为热度数值字符串，数值越大越热。

---

### 关键词搜索新闻

```bash
gnomic news search "<关键词>"
```

**示例：**
```bash
gnomic news search "人工智能"
gnomic news search "A股"
```

**JSON 输出结构：**
```json
{
  "success": true,
  "data": {
    "news": [
      {
        "title": "文章标题",
        "summary": "文章摘要",
        "media_name": "媒体名称",
        "time": "2026-04-02 09:00",
        "cover": "封面图片URL",
        "url": "文章链接",
        "categories": ["news_tech/artificial_intelligence", "news_tech"]
      }
    ]
  }
}
```

> `data.news` 为搜索结果数组，`categories` 为头条内部分类标签，`media_name` 为发布媒体。

---

### 文本格式输出

```bash
gnomic news hot -f text
gnomic news search "关键词" -f text
```

---

## 操作流程

### 判断使用哪条命令

| 用户意图 | 使用命令 |
|----------|----------|
| 看热榜/热搜/今日大事 | `gnomic news hot` |
| 搜索某个话题/关键词 | `gnomic news search "<关键词>"` |

### 获取热榜后的展示方式

从 `data.data.data` 数组提取条目，推荐格式：

```
🔥 今日头条热榜（更新时间：updateTime）

1. [标题](url)  热度：hot_value
2. [标题](url)  热度：hot_value
...
```

- `index + 1` 为排名
- `hot_value` 可格式化展示（如 34,480,552）
- 如需展示封面图，使用 `![](image_url)`

### 搜索新闻后的展示方式

从 `data.news` 数组提取条目，推荐格式：

```
📰 「关键词」相关新闻

标题（来源：media_name｜时间：time）
摘要内容...
🔗 url
```

---

## 注意事项

- 热榜数据实时拉取，`updateTime` 为最近一次更新时间
- 搜索结果按相关性排序，条数不固定，通常 5~10 条
- `categories` 字段为头条内部分类编码，无需展示给用户
- 请求通常在 2~5 秒内返回

---

## 补充：命令不可用时

如果执行 `gnomic` 命令时提示找不到命令，说明 `gnomic-cli` 尚未安装，执行以下命令安装：

```bash
npm install -g gnomic-cli
```

`gnomic-cli`开源地址：https://github.com/huyi9531/gnomic_cli