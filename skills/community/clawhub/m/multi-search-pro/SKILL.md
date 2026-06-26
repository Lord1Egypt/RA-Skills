---
name: "multi-search-pro"
version: "1.0.0"
description: "增强型多引擎搜索，集成17个搜索引擎（含中国内8个）+ 股票财经专用搜索 + 新闻聚合。触发词：'帮我搜索'、'查一下'、'搜索'、'财经新闻'、'最新消息'。支持百度/谷歌/必应/搜狗+财经专项：新浪财经/东方财富/雪球/财联社。无API密钥要求。"
---

# Multi Search Pro

增强型多引擎搜索，集成17个通用引擎 + 8个财经专项引擎。

## 通用搜索引擎 (17个)

### 中国引擎 (8)
- **百度**: `https://www.baidu.com/s?wd={keyword}`
- **必应中国**: `https://cn.bing.com/search?q={keyword}&ensearch=0`
- **必应国际**: `https://cn.bing.com/search?q={keyword}&ensearch=1`
- **360搜索**: `https://www.so.com/s?q={keyword}`
- **搜狗**: `https://www.sogou.com/web?query={keyword}`
- **微信搜索**: `https://wx.sogou.com/weixin?type=2&query={keyword}`
- **头条搜索**: `https://so.toutiao.com/search?keyword={keyword}`
- **集思录**: `https://www.jisilu.cn/explore/?keyword={keyword}`

### 国际引擎 (9)
- **Google**: `https://www.google.com/search?q={keyword}`
- **Google HK**: `https://www.google.com.hk/search?q={keyword}`
- **DuckDuckGo**: `https://duckduckgo.com/html/?q={keyword}`
- **Yahoo**: `https://search.yahoo.com/search?p={keyword}`
- **Startpage**: `https://www.startpage.com/sp/search?query={keyword}`
- **Brave Search**: `https://search.brave.com/search?q={keyword}`
- **Ecosia**: `https://www.ecosia.org/search?q={keyword}`
- **Qwant**: `https://www.qwant.com/?q={keyword}`
- **WolframAlpha**: `https://www.wolframalpha.com/input?i={keyword}`

## 财经专项引擎 (8)

### 新闻资讯
- **新浪财经**: `https://finance.sina.com.cn/search/?q={keyword}`
- **东方财富新闻**: `https://search.eastmoney.com/news/?keywords={keyword}`
- **财联社**: `https://www.cls.cn/search?keyword={keyword}`
- **雪球**: `https://xueqiu.com/search?q={keyword}`

### 股票数据
- **东方财富行情**: `https://so.eastmoney.com/s?keyword={keyword}`
- **同花顺**: `https://search.10jqka.com.cn/?tid=news&keyword={keyword}`
- **凤凰财经**: `https://finance.ifeng.com/search.aspx?q={keyword}`
- **网易财经**: `https://money.163.com/search?word={keyword}`

### 研报数据
- **东方财富研报**: `https://report.eastmoney.com/search?kw={keyword}`

## 触发词

当用户说以下内容时激活：
- "帮我搜索"、"查一下"、"搜索一下"
- "财经新闻"、"最新消息"
- "找一下"、"哪个好"
- "搜搜这个"、"帮我找"

## 搜索策略

### 一般搜索
```
1. 首选 DuckDuckGo（隐私保护）或 百度（中文）
2. 如果找不到，用 Google 补充
3. 特定网站用 site: 限定
```

### 财经/股票搜索
```
1. 首选 新浪财经 或 东方财富
2. 新闻类用 财联社
3. 社区讨论用 雪球
```

### 新闻搜索（带时间过滤）
```
1. 百度新闻 或 必应新闻
2. 加时间过滤：tbs="qdr:w"（一周内）
3. site:过滤特定媒体
```

## 高级语法

| 语法 | 示例 | 说明 |
|------|------|------|
| `site:` | `site:github.com python` | 限定网站 |
| `filetype:` | `filetype:pdf report` | 文件类型 |
| `""` | `"machine learning"` | 精确匹配 |
| `-` | `python -snake` | 排除词 |
| `OR` | `cat OR dog` | 或搜索 |
| `intitle:` | `intitle:报告` | 标题含关键词 |

## 时间过滤参数

| 参数 | 含义 |
|------|------|
| `tbs=qdr:h` | 一小时内 |
| `tbs=qdr:d` | 一天内 |
| `tbs=qdr:w` | 一周内 |
| `tbs=qdr:m` | 一月内 |
| `tbs=qdr:y` | 一年内 |

## 财经搜索示例

```javascript
// 搜索某公司最新新闻（一周内）
web_fetch({"url": "https://finance.sina.com.cn/search/?q=宁德时代&tbs=qdr:w"})

// 搜索某板块最新动态
web_fetch({"url": "https://search.eastmoney.com/news/?keywords=新能源车&t=1"})

// 搜索某股票研报
web_fetch({"url": "https://report.eastmoney.com/search?kw=贵州茅台"})

// 搜索美股新闻
web_fetch({"url": "https://www.google.com/search?q=Apple+stock+news&tbs=qdr:w"})

// 搜索加密货币
web_fetch({"url": "https://duckduckgo.com/html/?q=bitcoin+price+analysis"})

// 搜索财经数据
web_fetch({"url": "https://www.wolframalpha.com/input?i=GDP+China+2024"})
```

## DuckDuckGo Bangs 快捷跳转

| 指令 | 目标 |
|------|------|
| `!g` | Google |
| `!gh` | GitHub |
| `!so` | Stack Overflow |
| `!w` | Wikipedia |
| `!yt` | YouTube |
| `!bd` | 百度 |
| `!xf` | 东方财富 |

## WolframAlpha 快捷查询

- 汇率换算：`100 USD to CNY`
- 股市数据：`AAPL stock`
- 天气查询：`weather Beijing`
- 数学计算：`integrate x^2 dx`
- 数据对比：`GDP China vs USA`

## 隐私保护

推荐以下隐私搜索引擎（无追踪）：
- **DuckDuckGo** - 推荐日常使用
- **Startpage** - Google结果但隐私保护
- **Brave Search** - 独立索引
- **Qwant** - 欧盟GDPR合规

## 多引擎对比搜索

对于重要信息，同时搜索多个引擎：

```
1. 百度 + Google（中文信息交叉验证）
2. 新浪财经 + 东方财富（财经信息交叉验证）
3. 雪球 + 知乎（社区讨论对比）
```

## 搜索结果评估

| 来源类型 | 可靠性 | 用途 |
|----------|--------|------|
| 政府/监管网站 | ⭐⭐⭐⭐⭐ | 政策/公告 |
| 头部财经媒体 | ⭐⭐⭐⭐ | 新闻/快讯 |
| 交易所官网 | ⭐⭐⭐⭐⭐ | 公告/数据 |
| 社区讨论 | ⭐⭐⭐ | 情绪/观点 |
| 自媒体 | ⭐⭐ | 参考 |

## 常见场景

| 场景 | 推荐引擎 | 搜索词示例 |
|------|---------|-----------|
| 查某股票最新消息 | 新浪财经+雪球 | "宁德时代 公告" |
| 查大盘分析 | 东方财富 | "A股 今日分析" |
| 查板块机会 | 财联社 | "新能源 政策" |
| 查某公司研报 | 东方财富研报 | "贵州茅台 研报" |
| 查技术教程 | Google+StackOverflow | "python 教程 site:github.com" |
| 查财经数据 | WolframAlpha | "China GDP 2024" |
