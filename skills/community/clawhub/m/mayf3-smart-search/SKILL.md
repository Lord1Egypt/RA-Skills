---
name: smart-search
description: "Multi-engine search with auto-fallback, result parsing, and quality scoring via DDGS local library. Use when: searching the web, gathering information, market research, tech lookup, news search, fact checking. Triggers on 'search', '搜索', 'find info', 'look up', '调研', '查一下'. Not for: browser automation searches, internal file search, code search within repos."
---

# Smart Search

多引擎搜索集成：DDGS 本地库优先，**自动语言检测**，自动降级，结构化结果，搜索→提取一体化。

## 设计原则

1. **本地 DDGS 优先**（结构化结果、多后端、中英文）
2. **自动语言检测**（CJK 查询自动选 bing 优先链，英文自动选 brave 优先链）
3. **自动降级**（引擎挂了自动换下一个）
4. **搜索→提取一体化**（DDGS 搜索 + `extract()` 获取全文）
5. **超时保护**（`--timeout` 线程安全，`--type all` 可用）
6. **垂直搜索优先**（先选对战场，再选武器）

## 快速参考

**唯一必记规则：** 用 `--fallback`，脚本会自动根据查询语言选择最优后端链（中文→bing优先，英文→brave优先）。需要全文时加 `--extract`。需要强制指定语言时用 `--lang en/cn`。脚本化调用时用 `--urls-only` 只输出 URL。

## 引擎优先级

### Tier 0：DDGS 本地库（首选）

| 后端 | 速度 | 适用场景 | 状态 |
|------|------|---------|------|
| **brave** | ~1.1-1.7s | **英文首选** | ✅ 稳定 |
| **bing** | ~1.5s | **中文首选** | ✅ 稳定 |
| **yandex** | ~1.4s | 中文备选 | ⚠️ EN 搜索有时失败 |
| **yahoo** | ~1.1s | 备选 | ✅ 稳定 |

> DDGS 返回结构化 JSON（title/href/body），无需手动解析 HTML。
> `extract()` 方法可直接获取 URL 全文 markdown（~0.5s），搜索→提取一站式。
> ⚠️ brave 短时间连续搜索（>4次）可能返回空结果，切换到 yandex/yahoo。
> ⚠️ `threads()` 是 DDGS 类变量（控制并发线程数），不是搜索方法，不可调用。

### Tier 1：web_fetch 降级方案

| 引擎 | 响应时间 | 适用场景 |
|------|---------|---------|
| **Bing CN** | ~500ms | 降级首选，通用搜索 |
| **360** | ~1200ms | 英文搜索意外好 |
| **Sogou** | ~1800ms | 微信内容，长文搜索 |

### 不可用引擎（反爬拦截）

~~DuckDuckGo~~、~~Brave Search~~、~~Google~~、~~百度~~ — web_fetch 被反爬拦截，但 DDGS 库可通过 brave/bing 后端获取结果。

## 使用方法

### 方法 1：DDGS 脚本搜索（首选）

```bash
# 通用搜索（自动检测语言）
python3.12 {{SKILL_DIR}}/scripts/ddgs_search.py -q "搜索关键词" --fallback -m 5

# 版本信息
python3.12 {{SKILL_DIR}}/scripts/ddgs_search.py --version

# 强制指定语言（覆盖自动检测）
python3.12 {{SKILL_DIR}}/scripts/ddgs_search.py -q "AI agent" --lang cn --fallback  # 强制中文链
python3.12 {{SKILL_DIR}}/scripts/ddgs_search.py -q "人工智能" --lang en --fallback  # 强制英文链

# 指定后端 + JSON 输出
python3.12 {{SKILL_DIR}}/scripts/ddgs_search.py -q "query" -b brave -o json

# 搜索类型：text/news/videos/images/books
python3.12 {{SKILL_DIR}}/scripts/ddgs_search.py -q "AI news" --type news --fallback -m 5
python3.12 {{SKILL_DIR}}/scripts/ddgs_search.py -q "AI agent" --type all -m 3
python3.12 {{SKILL_DIR}}/scripts/ddgs_search.py -q "AI agent" --type all+ -m 3  # 含 images
# ⚠️ --type books 结果多来自影子图书馆（Library Genesis 等），谨慎用于版权内容
python3.12 {{SKILL_DIR}}/scripts/ddgs_search.py -q "machine learning" --type books

# 全文提取（--extract-length 控制输出长度，默认2000字符）
python3.12 {{SKILL_DIR}}/scripts/ddgs_search.py -q "topic" --extract
python3.12 {{SKILL_DIR}}/scripts/ddgs_search.py --extract-url "https://example.com/article"
python3.12 {{SKILL_DIR}}/scripts/ddgs_search.py --extract-url "https://example.com/article" --extract-length 5000

# 自动降级 + 语言检测（中文→bing优先，英文→brave优先）
python3.12 {{SKILL_DIR}}/scripts/ddgs_search.py -q "query" --fallback -m 5

# 超时保护（防止搜索挂死）
python3.12 {{SKILL_DIR}}/scripts/ddgs_search.py -q "query" --timeout 15 --fallback

# 静默模式（隐藏 stderr 重试/超时消息）
python3.12 {{SKILL_DIR}}/scripts/ddgs_search.py -q "query" --quiet --fallback

# 只输出 URL（一行一条，方便管道处理）
python3.12 {{SKILL_DIR}}/scripts/ddgs_search.py -q "query" --urls-only --fallback
python3.12 {{SKILL_DIR}}/scripts/ddgs_search.py -q "query" --urls-only --type all --fallback

# 时间过滤（d=天, w=周, m=月, y=年）
python3.12 {{SKILL_DIR}}/scripts/ddgs_search.py -q "最新新闻" -t d --fallback

# 批量搜索（自动语言检测+后端轮换）
python3.12 {{SKILL_DIR}}/scripts/ddgs_search.py --batch-file queries.txt -m 3 -o json
```

### 方法 2：DDGS Python API（嵌入脚本时）

```python
from ddgs import DDGS
with DDGS() as d:
    # 搜索
    results = list(d.text("query", max_results=5, backend="brave"))
    for r in results:
        print(r["title"], r["href"], r["body"])

    # 搜索后提取全文
    content = d.extract(results[0]["href"], fmt="text_markdown")
    print(content["content"])

    # 其他类型
    news = list(d.news("AI agent", max_results=3))
    images = list(d.images("AI agents", max_results=3))
    videos = list(d.videos("AI agents", max_results=3))
    books = list(d.books("machine learning", max_results=3))
```

### 方法 3：web_fetch 降级（紧急场景）

```javascript
// 中文搜索 → Bing CN（500ms，非结构化）
// 必须用 extractMode: "text"，markdown 模式会过滤掉搜索结果
web_fetch({"url": "https://cn.bing.com/search?q=Python+教程", "extractMode": "text"})
```

### 高级语法（web_fetch 场景）

```javascript
// 站内搜索
web_fetch({"url": "https://cn.bing.com/search?q=site:github.com+react", "extractMode": "text"})
// 精确匹配
web_fetch({"url": "https://cn.bing.com/search?q=\"exact+phrase\"", "extractMode": "text"})
// 时间过滤（after: 已验证有效）
web_fetch({"url": "https://cn.bing.com/search?q=\"RAG\"+after:2025-06-01", "extractMode": "text"})
```

> 详细语法实测结果和 Bing CN 关键词碰撞问题，见 [references/advanced-syntax.md](references/advanced-syntax.md)

## 自动降级策略

**`--fallback` 自动语言检测：** 中文查询 → bing 优先链，英文查询 → brave 优先链。

**中文降级链：** bing → yandex → yahoo → brave
**英文降级链：** brave → yandex → yahoo → bing

**DDGS 全部失败时：** DDGS → web_fetch Bing CN → web_fetch 360 → web_fetch Sogou

判断失败条件：DDGS 抛异常、返回空、超时（>15s 或 `--timeout` 值）

## 多引擎交叉验证

重要搜索用 2-3 个引擎验证：

```javascript
const r1 = web_fetch({"url": "https://cn.bing.com/search?q=keyword", "extractMode": "text"})
const r2 = web_fetch({"url": "https://www.so.com/s?q=keyword", "extractMode": "text"})
// 取交集作为高可信结果
```

## 最佳引擎组合

| 场景 | 推荐组合 |
|------|---------|
| 通用英文搜索 | DDGS brave 单后端 |
| 通用中文搜索 | DDGS bing 单后端 |
| 需要验证的搜索 | DDGS brave + bing |
| 微信/公众号内容 | web_fetch Sogou + WeChat |
| 紧急快速搜索 | web_fetch Bing CN（500ms） |
| 新闻搜索 | DDGS news() |

## 关键词构造技巧

1. **用独特、高区分度的词**，而非自然语言长句
   - ✅ `SearXNG JSON API format`
   - ❌ `请问SearXNG的JSON API格式是什么样的`
2. **高权重来源优先**：`site:edu.cn 量子计算`
3. **注意时效性**：搜索结果不一定反映最新信息
4. **索引延迟**：新内容可能几天后才被索引

## 常见问题

| 问题 | 解决 |
|------|------|
| 结果为空 | web_fetch 改用 `extractMode: "text"` |
| 国际引擎失败 | 换国内引擎，或用 DDGS |
| 结果不相关 | 加引号精确匹配或用 `site:` |
| 时间过滤 | 用 `after:` 操作符（已验证有效） |
| brave 连续搜索空 | 切换到 yandex/yahoo，或等几分钟 |

## 详细参考

- **[references/advanced-syntax.md](references/advanced-syntax.md)** — 高级搜索语法实测、Bing CN 关键词碰撞问题
- **[references/vertical-search.md](references/vertical-search.md)** — 垂直搜索引擎速查（学术/代码/新闻/图书等）
- **[references/credibility-assessment.md](references/credibility-assessment.md)** — 搜索结果可信度评估框架（CRAAP + SIFT）
- **[references/search-apis.md](references/search-apis.md)** — 搜索 API 升级路径（TinyFish/Exa/Tavily/Bocha 等）
- **[references/changelog.md](references/changelog.md)** — 完整版本更新日志（v1.0 → v3.6）

## 实测数据摘要（2026-06-04）

| 引擎 | 响应时间 | web_fetch | 英文质量 | 中文质量 |
|------|---------|-----------|---------|---------|
| DDGS brave | ~1.1-1.7s | N/A（库） | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| DDGS bing | ~1.5s | N/A（库） | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| DDGS yandex | ~1.4s | N/A（库） | ⭐⭐（EN 不稳定） | ⭐⭐⭐ |
| DDGS extract() | ~0.5s | N/A（库） | — | — |
| Bing CN | ~500ms | ✅ | ⭐⭐ | ⭐⭐⭐⭐ |
| 360 | ~1200ms | ✅ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
