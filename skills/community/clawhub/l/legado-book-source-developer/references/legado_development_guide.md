# Legado Book Source Development Guide

## Table of Contents
1. [Workflow Details](#workflow-details)
2. [Encoding Detection & Handling](#encoding)
3. [HTML Structures & Solutions](#html-structures)
4. [nextContentUrl Decision Rules](#nextcontenturl)
5. [Regular Expression Formats](#regex)
6. [Troubleshooting](#troubleshooting)
7. [Best Practices](#best-practices)
8. [Advanced Features](#advanced-features)

---

## Workflow Details

### Phase 1 Detail: Information Collection

**1.1 Browser Developer Tools (获取真实请求)**

Record from Network panel:
- Request method (GET/POST)
- Full request URL
- All request headers
- Request body (for POST)
- Query parameters
- Response status code & Content-Type

**1.2 JavaScript File Analysis**

Identify key JS files: `search.js`, `common.js`, `app.js`

Extract from JS:
- Search function call patterns
- Parameter generation logic (encryption, signing)
- API endpoint configuration
- Request header configuration
- Encoding methods

```bash
cd tools && python js_param_analyzer.py
```

**1.3 Real HTML Acquisition**

Must fetch: homepage, search results, book detail, TOC, content page.

Save requirements: complete HTML, correct encoding, all `<script>` and `<link>` tags.

### Phase 1 Detail: User Inquiry for Uncertainty

**Scenario 1: Unknown search interface parameters**
Ask user: open DevTools → Sources → search for `signature`, `token`, `encrypt`, `sign`. Get related JS code.

**Scenario 2: Complex HTML / anti-scraping**
Ask user: check Network XHR/Fetch for API requests, or use headless browser.

**Scenario 3: Anti-scraping detected**
Ask user: provide login credentials, website docs, or choose another site.

---

## Encoding Detection & Handling

**Critical: Detect BEFORE fetching HTML!**

```python
detected_charset = detect_charset(url="http://example.com")
# Then use in all requests:
smart_fetch_html(url="...", charset=detected_charset)
```

**Encoding rules:**
- UTF-8 → omit charset parameter (default)
- GBK → add `"charset":"gbk"` to POST/GET requests
- GB2312 → use `"charset":"gbk"` (GBK compatible)

**searchUrl encoding example:**
```
UTF-8: /search?q={{key}}
GBK:  /search,{"method":"POST","body":"key={{key}}","charset":"gbk"}
```

---

## HTML Structures & Solutions

### Structure 1: Standard List (with cover)

```html
<div class="book-list">
  <div class="item">
    <img src="cover.jpg" class="cover"/>
    <a href="/book/1" class="title">Book Name</a>
  </div>
</div>
```

```json
{"ruleSearch": {"bookList": ".book-list .item", "name": ".title@text", "bookUrl": "a@href", "coverUrl": "img@src"}}
```

### Structure 2: Search Page (no cover, merged info)

```html
<div class="hot_sale">
  <a href="/book/1">
    <p class="title">Book Name</p>
    <p class="author">Category | Author: Name</p>
  </a>
</div>
```

```json
{"ruleSearch": {"bookList": ".hot_sale", "name": ".title@text", "author": ".author.0@text##.*| |Author:##", "kind": ".author.0@text##\\|.*##", "bookUrl": "a@href", "coverUrl": ""}}
```

### Structure 3: Lazy Loading Images

```html
<img class="lazy" data-original="cover.jpg" src="placeholder.jpg"/>
```

```json
{"coverUrl": "img.lazy@data-original||img@src"}
```

---

## nextContentUrl Decision Rules

**Core: Set ONLY for true next chapter links.**

| Scenario | Button Text | URL Pattern | Action |
|----------|------------|-------------|--------|
| True next chapter | "下一章", "下章" | /ch/1 → /ch/2 | **SET** |
| Same chapter pagination | "下一页", "继续阅读" | /ch/1_1 → /ch/1_2 | **LEAVE EMPTY** |
| Ambiguous | "下一", "下页" | Check URL | Compare URLs |

---

## Regular Expression Formats

**Format 1: Delete matched content**
```
选择器@提取类型##正则表达式
```

**Format 2: Replace matched content**
```
选择器@提取类型##正则表达式##替换内容
```

**Format 3: Extract using capture groups**
```
选择器@提取类型##正则表达式(捕获组)##$1
```

**Examples:**
```json
{
  "author": ".author@text##.*Author:##",
  "author": ".author@text##Author:(.*)##$1",
  "content": "#content@html##<div id=\"ad\">[\\s\\S]*?</div>|Please bookmark##"
}
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Search no results | Verify CSS selectors; check if structure changed; add headers/cookies |
| Content missing | Check dynamic loading; set cookies; add login logic |
| Directory order wrong | Add `-` before list selector: `-ul.chapter-list li` |
| Advertisements | Use `@ownText` instead of `@text`; clean with regex |
| Pagination | `nextContentUrl` for content; `nextTocUrl` for TOC |
| Image hotlinking | Configure Referer header in `header` field |
| Encoding (garbled) | Detect encoding before fetching; use in all requests |

---

## Best Practices

1. Always query knowledge base first
2. Detect encoding before fetching HTML
3. Reference real examples (134 real book sources)
4. Validate with real HTML — never assume structure
5. Handle special cases: no cover, lazy loading, merged info
6. Use proven templates
7. Test thoroughly
8. Use `knowledge_learner` for continuous improvement
9. Use `user_intervention` for complex scenarios

---

## Advanced Features

### Rule Processing Modes (AnalyzeRule.kt)
- **Default** → JSoup CSS selectors
- **Json** → JSONPath
- **XPath** → XPath selectors
- **Js** → JavaScript evaluation
- **WebJs** → WebView JavaScript

### Advanced BookSource Fields
- `checkKeyWord` — search validation keyword
- `subContent` — secondary content appended to main content
- `title` — extract title from content page
- `payAction` — purchase action (JS or URL with `{{js}}`)
- `callBackJs` — event listener callback JS
- `preUpdateJs` — JS executed before TOC update
- `formatJs` — formatting JS
- `imageStyle` — image display style (default centered, FULL=max width)
- `imageDecode` — image bytes decryption JS
- `webJs` — WebView JS injection for dynamic content
- `coverDecodeJs` — cover image decryption JS
- `loginCheckJs` — login detection JS
- `exploreScreen` — discovery filter rules

### Caching Mechanisms
- String rules → `stringRuleCache` HashMap
- Regular expressions → `regexCache` HashMap
- Scripts → `scriptCache` HashMap

### WebSocket Debug Interface
- URL: `ws://127.0.0.1:1235/bookSourceDebug`
- Message: `{key: "搜索关键词", tag: "源链接"}`

### Learning & Auditing
- `knowledge_learner` — learn from new book sources
- `knowledge_applier` — apply learned patterns
- `knowledge_enhanced_analyzer` — enhanced analysis with knowledge
- `audit_knowledge_base` — validate knowledge base integrity
- `knowledge_auditor` — audit specific items
