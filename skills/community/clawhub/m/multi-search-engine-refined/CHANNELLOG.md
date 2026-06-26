# Multi Search Engine

## 基本信息

- **名称**: multi-search-engine
- **版本**: v2.0.1
- **描述**: 集成 4 个搜索引擎：Google、DuckDuckGo、Brave、WolframAlpha；支持高级搜索语法
- **发布时间**: 2026-02-06

## 搜索引擎

Google、DuckDuckGo、Brave Search、WolframAlpha（均为 `google.com` / `duckduckgo.com` / `search.brave.com` / `wolframalpha.com` 域名）

## 核心功能

- Google 高级操作符（site:, filetype:, intitle: 等）
- 时间筛选（小时/天/周/月/年）
- DuckDuckGo HTML 搜索与 Bangs（`!g`、`!brave`）
- Brave 独立索引与时间/新闻/媒体参数
- WolframAlpha 知识计算

## 更新记录

### v2.0.1 (2026-02-06)
- 精简文档，优化发布

### v2.0.0 (2026-02-06)
- 新增国际搜索引擎能力
- 强化深度搜索能力

### v1.0.0 (2026-02-04)
- 初始版本

## 使用示例

```javascript
web_fetch({"url": "https://www.google.com/search?q=python"})

web_fetch({"url": "https://duckduckgo.com/html/?q=privacy"})

web_fetch({"url": "https://search.brave.com/search?q=news&source=news"})

web_fetch({"url": "https://www.wolframalpha.com/input?i=100+USD+to+EUR"})

web_fetch({"url": "https://www.google.com/search?q=site:github.com+python"})
```

MIT License
