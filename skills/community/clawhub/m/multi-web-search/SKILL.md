---
name: "Multi-Web-Search | 多引擎网页搜索"
description: >
  Free multi-engine web search skill v3.4. No API key required, supports 20 search engines (11 international + 7 domestic + 2 professional) with parallel search, time filters, and site filters.
  New features: image/news/video/book search, DHT network acceleration, proxy support, configurable timeout.
  | 免费多引擎网页搜索技能 v3.4。无需 API Key，支持 20 个搜索引擎并行搜索、时间过滤、站点过滤。
  Use when you need real-time web search, code examples, technical docs, multi-language search, privacy-first searching, image search, news aggregation, or video search. Zero-config fallback (DuckDuckGo Lite), auto-degrades when ddgs unavailable. DHT network provides 90%% faster repeated queries.
use_when:
  - "需要搜索网页内容"
  - "需要多引擎并行搜索"
  - "需要免费搜索（无 API Key）"
  - "需要时间过滤的新闻搜索"
  - "需要站点限定的代码搜索"
  - "需要中文/国际内容搜索"
  - "需要 DuckDuckGo/Brave 等隐私引擎"
  - "需要搜索 Reddit/HackerNews 社区"
  - "需要技术文档/教程搜索"
  - "需要图片搜索"
  - "需要新闻聚合"
  - "需要视频搜索"
  - "需要代理搜索"
  - "需要 DHT 加速"
trigger:
  phrases:
    - "搜索网页"
    - "免费搜索"
    - "多引擎搜索"
    - "网页结果"
    - "搜索引擎"
    - "Google 搜索"
    - "百度搜索"
    - "DuckDuckGo"
    - "Brave 搜索"
    - "实时资讯"
    - "最新新闻"
    - "技术文档"
    - "代码示例"
    - "site:github"
    - "--time week"
    - "--domain"
    - "web_fetch"
    - "搜索一下"
    - "帮我搜"
    - "图片搜索"
    - "新闻搜索"
    - "视频搜索"
    - "代理搜索"
    - "DHT"
version: 3.4.0
emoji: "🔍"
openclaw:
  requires:
    bins: [python3]
  suggests:
    bins: [ddgs]
    extras: [ddgs[dht]]  # DHT 网络加速（可选）
---

# 🌐 Multi-Web-Search v2.0.0

**免费、无需 API Key 的多引擎网页搜索。** 支持 20 个搜索引擎（11 国际 + 7 国内 + 2 专业），可并行搜索、时间过滤、站点过滤。

---

## 快速开始

```bash
# 基础搜索（自动选择引擎）
python3 search.py -q "python tutorial"

# 多引擎并行
python3 search.py -q "react hooks" -e google,brave

# 时间过滤
python3 search.py -q "AI news" --time week

# 站点搜索
python3 search.py -q "machine learning" --domain github.com

# 无 ddgs 时，使用 DuckDuckGo Lite
python3 search.py -q "test" --lite
```

---

## 支持的搜索引擎

### 🌐 国际引擎

| 引擎 | 说明 | 适用场景 | 隐私 |
|------|------|---------|------|
| `google` | Google 搜索 | 综合搜索、技术文档、学术资源 | ❌ |
| `google_hk` | 谷歌香港 | 简化版 Google，广告少 | ❌ |
| `brave` | Brave Search | 隐私优先、新闻聚合、Discussions | ✅ |
| `ddg` / `duckduckgo` | DuckDuckGo | 隐私搜索、Bangs 快捷跳转 | ✅ |
| `bing` | Microsoft Bing | 微软生态、英文搜索 | ❌ |
| `yahoo` | Yahoo Search | 新闻聚合、传统搜索用户 | ❌ |
| `startpage` | Startpage | Google 结果 + 隐私保护 | ✅ |
| `ecosia` | Ecosia（环保） | 环保搜索、植树公益 | ✅ |
| `qwant` | Qwant（欧盟） | 欧盟推荐、不追踪用户 | ✅ |
| `yandex` | Yandex（俄罗斯） | 俄语搜索、俄罗斯资源 | ❌ |
| `mojeek` | Mojeek（独立索引） | 自有索引、隐私友好 | ✅ |

### 🔬 专业知识引擎

| 引擎 | 说明 | 适用场景 |
|------|------|---------|
| `wikipedia` | 维基百科 | 概念、术语、历史人物等百科查询 |
| `wolframalpha` | 计算知识引擎 | 数学公式、统计数据、单位换算 |
| `github` | GitHub 代码搜索 | 代码片段、开源项目、Issue 查询 |
| `stackoverflow` | Stack Overflow | 编程问题、技术方案、错误排查 |

### 🇨🇳 国内引擎（7个）

| 引擎 | 说明 | 适用场景 |
|------|------|---------|
| `baidu` | 百度搜索 | 中文内容、百度系产品 |
| `bing_cn` | 必应中国版 | 中文结果（ensearch=0） |
| `bing_int` | 必应国际版 | 英文结果（ensearch=1） |
| `360` | 360搜索 | 安全搜索、网址导航 |
| `sogou` | 搜狗搜索 | 知乎/微信公众号 |
| `wechat` | 微信搜索 | 公众号文章 |
| `shenma` | 神马搜索 | 移动端内容、UC浏览器 |

---

## CLI 参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `-q, --query` | 搜索查询 | `-q "python tutorial"` |
| `-e, --engines` | 引擎列表（逗号分隔） | `-e google,brave,baidu` |
| `-m, --max-results` | 每引擎最大结果数 | `-m 10` |
| `-t, --time` | 时间过滤 | `--time week` |
| `-d, --domain` | 站点搜索 | `--domain github.com` |
| `-r, --region` | 地区代码 | `-r us-en` |
| `--lite` | 强制 DuckDuckGo Lite | `--lite` |
| `--no-cache` | 禁用缓存 | `--no-cache` |
| `--no-rank` | 禁用评分排序 | `--no-rank` |
| `-o, --output` | 输出文件 | `-o results.json` |
| `--json` | 紧凑 JSON 输出 | `--json` |
| `--proxy, -pr` | 代理服务器 | `--proxy socks5h://127.0.0.1:9150` |
| `--type` | 搜索类型 | `--type text` (默认) / `images` / `news` / `videos` / `books` |
| `--timeout` | 单引擎超时秒数 | `--timeout 10` (默认 30) |
| `--dht` | 启用 DHT 网络加速 | `--dht` |

### 时间过滤值

| 值 | 含义 | Google 参数 | Brave 参数 |
|----|------|-------------|-----------|
| `hour` | 最近 1 小时 | `qdr:h` | `ph` |
| `day` | 最近 24 小时 | `qdr:d` | `pd` |
| `week` | 最近 7 天 | `qdr:w` | `pw` |
| `month` | 最近 30 天 | `qdr:m` | `pm` |
| `year` | 最近 365 天 | `qdr:y` | `py` |

---

## 高级搜索技巧

### Google 搜索操作符

| 操作符 | 功能 | 示例 |
|--------|------|------|
| `" "` | 精确匹配 | `"machine learning"` |
| `-` | 排除关键词 | `python -snake` |
| `OR` | 或运算 | `machine OR deep learning` |
| `site:` | 站内搜索 | `site:github.com python` |
| `filetype:` | 文件类型 | `filetype:pdf annual report` |
| `intitle:` | 标题包含 | `intitle:tutorial python` |
| `inurl:` | URL 包含 | `inurl:login admin` |

### Brave 特色搜索

| 功能 | 说明 | 参数 |
|------|------|------|
| `Goggles` | 自定义搜索规则 | 创建个性化过滤器 |
| `Discussions` | 论坛讨论聚合 | 搜索 Reddit 等论坛 |
| `source=news` | 新闻搜索 | 独立新闻索引 |
| `source=images` | 图片搜索 | 图片索引 |

### DuckDuckGo Bangs

| Bang | 跳转 | 示例 |
|------|------|------|
| `!g` | Google 搜索 | `!g python` |
| `!gh` | GitHub | `!gh tensorflow` |
| `!so` | Stack Overflow | `!so javascript` |
| `!w` | Wikipedia | `!w AI` |
| `!yt` | YouTube | `!yt tutorial` |

---

## 执行步骤（CLI 使用）

根据不同搜索目标选择最佳引擎组合：

| 搜索目标 | 首选引擎 | 原因 |
|---------|---------|------|
| **综合中文内容** | 百度 | 中文索引最全 |
| **公众号文章** | 搜狗 + 微信 | 唯一支持公众号搜索 |
| **知乎内容** | 搜狗 | 知乎优化好 |
| **隐私优先** | Brave / DuckDuckGo / Startpage | 不追踪用户 |
| **技术文档 / 编程** | Google + Stack Overflow | 技术文档全面 |
| **GitHub 代码搜索** | GitHub 专用引擎 | 代码片段/开源项目最准 |
| **实时新闻** | Brave News / Bing | 新闻聚合能力强 |
| **编程问题排查** | Stack Overflow / Google | 错误方案最全 |
| **学术资源** | Google + 百度学术 | 论文、学术搜索 |
| **俄语 / 俄罗斯资源** | Yandex | 俄语区比 Google 更准 |
| **环保公益搜索** | Ecosia | 搜索即植树 |
| **计算型查询** | WolframAlpha | 数学/统计/单位换算 |
| **百科知识** | Wikipedia | 概念、术语、历史人物 |
| **图片搜索** | `ddgs images()` / Brave | 图片索引聚合 |
| **视频搜索** | `ddgs videos()` | 视频结果聚合 |
| **新闻搜索** | `ddgs news()` | 新闻聚合（支持时间过滤） |

### 🇨🇳 国内引擎深度指南

| 引擎 | 特色功能 | 搜索示例 |
|------|---------|---------|
| **百度** | 中文索引最全、百度学术、百度新闻 | `site:github.com python` / `filetype:pdf` |
| **搜狗** | 知乎优化、微信公众号 | `site:zhihu.com 机器学习` |
| **微信搜索** | 唯一公众号文章搜索渠道 | `https://wx.sogou.com/weixin?type=2&query=Python` |
| **必应中国版** | 中英文结果切换（ensearch=0/1） | `https://cn.bing.com/search?q=AI&ensearch=0` |
| **360搜索** | 安全搜索、网址导航 | 安全过滤默认开启 |
| **神马搜索** | 移动端优化、UC浏览器集成 | `https://m.sm.cn/s?q=关键词` |

### 🌐 国际引擎使用技巧

| 引擎 | 特色技巧 | 示例 |
|------|---------|------|
| **Brave** | Discussions（论坛聚合）、News、图片搜索 | `source=news` / `Goggles 自定义规则` |
| **DuckDuckGo** | Bangs 快捷跳转（!g / !gh / !so） | `!so python error` → 直接跳转 Stack Overflow |
| **Startpage** | Anonymous View 匿名浏览、Google 结果 | 不调用 Google 但显示相同结果 |
| **Ecosia** | 每约 45 次搜索种一棵树 | 环保主义者首选 |
| **Qwant** | 欧盟官方推荐、不做个性化追踪 | 适合注重数据主权用户 |
| **Yandex** | 俄语搜索、俄区内容 | 俄语学习、俄罗斯文化资源 |
| **Mojeek** | 自有独立索引，不依赖 Google/Bing | 隐私激进用户的替代方案 |

---

## 架构

```
~/.openclaw/skills/multi-web-search/scripts/
├── constants.py        # 16+ 引擎定义
├── url_builder.py     # URL 构建
├── cache_utils.py     # 结果缓存（TTL 1小时）
├── result_scorer.py   # 结果评分排序
├── search.py          # ✅ 唯一入口 (v3.4)
└── install.py         # 安装脚本
```

---

## 输出格式

```json
{
  "provider": "multi-engine",
  "query": "python tutorial",
  "engines": ["google", "brave"],
  "search_type": "text",
  "time_filter": "week",
  "domain": null,
  "results": [
    {
      "title": "Python Tutorial",
      "url": "https://...",
      "snippet": "...",
      "source": "google",
      "_score": 85.3
    }
  ],
  "engine_results": {...},
  "total_results": 10,
  "unique_results": 8,
  "ddgs_available": true,
  "dht_enabled": false,
  "proxy": null
}
```

### 输出字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `search_type` | string | 搜索类型：text/images/news/videos/books |
| `dht_enabled` | bool | 是否启用 DHT 网络加速 |
| `proxy` | string/null | 代理服务器地址 |
| `engine_results` | dict | 各引擎的详细结果（包含 success/error/url） |

---

## 实现步骤

调用此技能时，按以下步骤执行：

### 1️⃣ 解析用户需求

提取搜索请求中的关键参数：

| 参数 | 来源 | 示例 |
|------|------|------|
| 查询内容 | 用户输入 | `"python tutorial"` |
| 引擎选择 | `-e` 参数或推断 | `google,brave` |
| 时间过滤 | `--time` 参数 | `week`、`month` |
| 站点限制 | `--domain` 参数 | `github.com` |
| 地区代码 | `-r` 参数 | `cn-zh`、`us-en` |
| 搜索类型 | `--type` 参数 | `text`、`images`、`news`、`videos`、`books` |
| 代理 | `--proxy/-pr` 参数 | `socks5h://127.0.0.1:9150` |
| 超时 | `--timeout` 参数 | `10`（秒） |
| DHT 加速 | `--dht` 参数 | 启用 P2P 缓存加速 |

**引擎选择优先级：**
- 用户明确指定 → 使用用户指定引擎
- 中文内容 → 默认添加国内引擎（baidu / bing_cn）
- 隐私优先 → Brave / DuckDuckGo / Startpage
- 未指定 → 使用 DEFAULT_ENGINES = `["google", "brave"]`

**搜索类型选择：**
- 文本搜索 → `text`（默认）
- 图片搜索 → `images`（支持 size/color/type/layout/license 参数）
- 新闻搜索 → `news`（支持时间过滤）
- 视频搜索 → `videos`（支持 resolution/duration 参数）
- 书籍搜索 → `books` |

### 2️⃣ 执行搜索

```bash
# 文本搜索
python3 search.py -q "<query>" -e <engines> [-t <time>] [-d <domain>] [-r <region>]

# 图片搜索
python3 search.py -q "<query>" --type images [-m 10] [--size Large] [--color Blue]

# 新闻搜索
python3 search.py -q "<query>" --type news --time week

# 视频搜索
python3 search.py -q "<query>" --type videos [--duration medium]

# 书籍搜索
python3 search.py -q "<query>" --type books

# 代理 + 超时
python3 search.py -q "<query>" --proxy socks5h://127.0.0.1:9150 --timeout 10

# 启用 DHT 加速
python3 search.py -q "<query>" --dht
```

**执行逻辑：**

```
如果 ddgs 可用:
    → 使用 ddgs 多引擎并行搜索（支持 text/images/news/videos/books）
    → 如果启用 DHT → 自动使用 DHT 网络缓存
否则:
    → 使用 DuckDuckGo Lite URL 生成
    → 通过 web_fetch 获取结果
```

**降级策略：**
- `ddgs` 不可用 → 自动降级到 DuckDuckGo Lite
- 单引擎失败 → 继续返回其他引擎结果
- 引擎不支持该搜索类型 → 返回错误提示支持的引擎
- DHT 网络不可用 → 静默回退到普通缓存

### 3️⃣ 处理结果

**多引擎结果合并：**
- 所有引擎结果合并到统一列表
- 每个结果标注 `source` 字段（来源引擎）
- 根据 `_score` 字段排序（仅 text 类型）

**结果格式因搜索类型而异：**
- `text`: `{title, url, snippet, source}`
- `images`: `{title, url, image, thumbnail, width, height, source}`
- `news`: `{title, url, snippet, published_date, source}`
- `videos`: `{title, url, description, duration, embed_url, thumbnail, source}`
- `books`: `{title, url, author, publisher, source}`

**去重逻辑：**
- URL 完全相同的结果只保留一个
- 保留评分最高的那条
- 不支持的引擎返回全部结果

### 4️⃣ 错误处理

| 错误场景 | 处理方式 |
|---------|---------|
| `ddgs` 未安装 | 降级到 DuckDuckGo Lite，无警告 |
| 引擎不支持时间过滤 | 静默忽略，仅返回其他引擎结果 |
| 引擎不支持该搜索类型 | 返回错误，提示支持的引擎列表 |
| 网络超时 | 返回已获取的结果，不阻塞 |
| 结果为空 | 建议换用其他引擎或重新表述 |
| URL 编码错误 | 使用 `urllib.parse.quote()` 正确编码 |
| DHT 网络不可用 | 静默回退到普通缓存 |
| 代理连接失败 | 返回错误，提示检查代理配置 |

### 5️⃣ 格式化输出

**结果呈现：**
- 标题加粗，显示 URL 链接
- snippet 展示摘要内容
- 标注来源引擎和相关性评分
- 标注搜索类型（text/images/news/videos/books）

**JSON 输出（`--json`）：**
```json
{
  "provider": "multi-engine",
  "query": "python tutorial",
  "engines": ["google", "brave"],
  "search_type": "text",
  "time_filter": "week",
  "domain": null,
  "results": [
    {
      "title": "Python Tutorial",
      "url": "https://...",
      "snippet": "...",
      "source": "google",
      "_score": 85.3
    }
  ],
  "engine_results": {...},
  "total_results": 10,
  "unique_results": 8,
  "ddgs_available": true,
  "dht_enabled": false,
  "proxy": null
}
```

**输出标志含义：**
- `ddgs_available: true` → 使用 ddgs 并行搜索，速度更快
- `ddgs_available: false` → 降级到 DuckDuckGo Lite
- `dht_enabled: true` → 使用 DHT 网络加速（重复查询提速 90%%）
- `proxy: <proxy_url>` → 使用代理服务器
- `unique_results < total_results` → 有重复结果已去重

---

| 依赖 | 状态 | 说明 |
|------|------|------|
| python3 | 必须 | 运行环境 |
| ddgs | 推荐 | 多引擎并行（pip install ddgs） |
| ddgs[dht] | 可选 | DHT 网络加速（pip install ddgs[dht]） |

无 ddgs 时，自动降级到 DuckDuckGo Lite URL 生成，使用 `web_fetch` 获取结果。

---

## 安全与隐私

- **无需 API Key**：所有搜索基于免费工具
- **零配置**：无需注册账号
- **隐私友好引擎**：支持 Brave、DuckDuckGo、Startpage 等
- **本地缓存**：仅存本地，无远程传输

---

*免费网页搜索技能，支持 16+ 引擎。*