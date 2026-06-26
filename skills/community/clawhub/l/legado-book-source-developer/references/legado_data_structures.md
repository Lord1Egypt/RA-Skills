# Legado Data Structures & Source Code Analysis

Based on analysis of 397,380 lines of Legado source code.

## Table of Contents
1. [BookSource Data Structure](#booksource)
2. [Rule Data Structures](#rules)
3. [Rule Parsing Engine](#engine)
4. [Database Schema](#database)
5. [Required Fields Summary](#required)

---

## BookSource Data Structure (BookSource.kt)

```kotlin
data class BookSource(
    @PrimaryKey var bookSourceUrl: String = "",       // Required
    var bookSourceName: String = "",                   // Required
    var bookSourceGroup: String? = null,               // 分组
    var bookSourceType: Int = 0,                       // 0=文本 1=音频 2=图片 3=文件 4=视频
    var bookUrlPattern: String? = null,
    var customOrder: Int = 0,
    var enabled: Boolean = true,
    var enabledExplore: Boolean = true,
    var jsLib: String? = null,
    var enabledCookieJar: Boolean? = true,
    var concurrentRate: String? = null,
    var header: String? = null,
    var loginUrl: String? = null,
    var loginUi: String? = null,
    var loginCheckJs: String? = null,
    var coverDecodeJs: String? = null,
    var bookSourceComment: String? = null,
    var variableComment: String? = null,
    var lastUpdateTime: Long = 0,
    var respondTime: Long = 180000L,
    var weight: Int = 0,
    var exploreUrl: String? = null,
    var exploreScreen: String? = null,
    var ruleExplore: ExploreRule? = null,
    var searchUrl: String? = null,
    var ruleSearch: SearchRule? = null,
    var ruleBookInfo: BookInfoRule? = null,
    var ruleToc: TocRule? = null,
    var ruleContent: ContentRule? = null,
    var ruleReview: ReviewRule? = null,
    var eventListener: Boolean = false,
    var customButton: Boolean = false
)
```

---

## Rule Data Structures

### SearchRule

```kotlin
data class SearchRule(
    var checkKeyWord: String? = null,    // 校验关键字
    var bookList: String? = null,        // Required
    var name: String? = null,            // Required
    var author: String? = null,
    var intro: String? = null,
    var kind: String? = null,
    var lastChapter: String? = null,
    var updateTime: String? = null,
    var bookUrl: String? = null,         // Required
    var coverUrl: String? = null,
    var wordCount: String? = null
)
```

### BookInfoRule

```kotlin
data class BookInfoRule(
    var init: String? = null,
    var name: String? = null,            // Required
    var author: String? = null,
    var intro: String? = null,
    var kind: String? = null,
    var lastChapter: String? = null,
    var updateTime: String? = null,
    var coverUrl: String? = null,
    var tocUrl: String? = null,
    var wordCount: String? = null,
    var canReName: String? = null,
    var downloadUrls: String? = null
)
```

### TocRule

```kotlin
data class TocRule(
    var preUpdateJs: String? = null,
    var chapterList: String? = null,     // Required
    var chapterName: String? = null,     // Required
    var chapterUrl: String? = null,      // Required
    var formatJs: String? = null,
    var isVolume: String? = null,
    var isVip: String? = null,
    var isPay: String? = null,
    var updateTime: String? = null,
    var nextTocUrl: String? = null
)
```

### ContentRule

```kotlin
data class ContentRule(
    var content: String? = null,         // Required
    var subContent: String? = null,      // 副文规则
    var title: String? = null,           // 有些网站只能在正文中获取标题
    var nextContentUrl: String? = null,  // 下一章链接 (NOT prevContentUrl!)
    var webJs: String? = null,
    var sourceRegex: String? = null,
    var replaceRegex: String? = null,
    var imageStyle: String? = null,
    var imageDecode: String? = null,
    var payAction: String? = null,
    var callBackJs: String? = null
)
```

---

## Rule Parsing Engine (AnalyzeRule.kt)

**Parsing Modes:**
| Mode | Engine | Use Case |
|------|--------|----------|
| Default | JSoup CSS | Standard HTML parsing |
| Json | JSONPath | JSON data sources |
| XPath | XPath | XML/HTML documents |
| Js | JavaScript | Script evaluation |
| WebJs | WebView JS | Dynamic/SPA content |

**Rule String Format:** `CSS选择器@提取类型##正则表达式##替换内容`

**Key Methods:**
```kotlin
fun getString(ruleStr: String?, mContent: Any?, isUrl: Boolean): String
fun getStringList(ruleStr: String?, mContent: Any?, isUrl: Boolean): List<String>?
fun setContent(content: Any?, baseUrl: String?): AnalyzeRule
```

**Processing Flow:**
1. Parse rule string into `SourceRule` list
2. Apply each rule sequentially
3. Handle mode switching (CSS/JSON/XPath/JS)
4. Apply regex replacements
5. Return final result

---

## Database Schema (Room)

```sql
CREATE TABLE bookSources (
    bookSourceName TEXT NOT NULL,
    bookSourceGroup TEXT,
    bookSourceUrl TEXT NOT NULL PRIMARY KEY,
    bookSourceType INTEGER NOT NULL,
    bookUrlPattern TEXT,
    customOrder INTEGER NOT NULL DEFAULT 0,
    enabled INTEGER NOT NULL DEFAULT 1,
    enabledExplore INTEGER NOT NULL DEFAULT 1,
    jsLib TEXT,
    enabledCookieJar INTEGER DEFAULT 0,
    header TEXT,
    loginUrl TEXT,
    loginUi TEXT,
    coverDecodeJs TEXT,
    bookSourceComment TEXT,
    variableComment TEXT,
    lastUpdateTime INTEGER NOT NULL,
    respondTime INTEGER NOT NULL DEFAULT 180000,
    weight INTEGER NOT NULL DEFAULT 0,
    exploreUrl TEXT,
    exploreScreen TEXT,
    ruleExplore TEXT,
    searchUrl TEXT,
    ruleSearch TEXT,
    ruleBookInfo TEXT,
    ruleToc TEXT,
    ruleContent TEXT
);

CREATE INDEX index_book_sources_bookSourceUrl ON bookSources(bookSourceUrl);
```

---

## Required Fields Summary

### BookSource (minimum viable)
- `bookSourceUrl` — Primary Key
- `bookSourceName` — Display name
- `searchUrl` — Search URL template
- `ruleSearch` — Search rules
- `ruleBookInfo` — Book info rules
- `ruleToc` — TOC rules
- `ruleContent` — Content rules

### ruleSearch (minimum)
- `bookList` — List container selector
- `name` — Book name selector
- `bookUrl` — Book URL selector

### ruleToc (minimum)
- `chapterList` — Chapter list selector
- `chapterName` — Chapter name selector
- `chapterUrl` — Chapter URL selector

### ruleContent (minimum)
- `content` — Content selector

### Forbidden Fields
- **NO** `prevContentUrl` — does not exist in Legado source code
- **NO** `:contains()` — use `text.关键词`
- **NO** `:first-child` / `:last-child` — use `.0` / `.-1`

---

## Key Source Code Findings

1. **No `prevContentUrl`**: Confirmed nonexistent in ContentRule.kt
2. **Rule storage**: All rules stored as TEXT, converted via GSON
3. **Caching**: String rules, regex, and scripts all cached in HashMaps
4. **Multiple format support**: Rules support both JSON object and primitive string
5. **Regex caching**: Compiled regex cached for performance
6. **WebView integration**: Dynamic content via `webJs` and `BackstageWebView`
7. **JSON deserialization**: Custom deserializers handle flexible input formats
