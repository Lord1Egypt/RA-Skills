---
name: legado-book-source-developer
description: Legado (阅读) Android app book source development skill. For creating book sources for novel/manga websites, debugging existing book source rules, querying Legado knowledge (CSS selectors, rule formats, POST requests), and analyzing website HTML structure. Covers searchUrl, ruleSearch, ruleToc, ruleContent, ruleBookInfo configuration. Use only with user-owned or authorized websites.
---

# Legado Book Source Developer

A toolkit for creating, debugging, and managing Legado book sources. Includes analysis tools, real book source examples, and a knowledge base built from Legado source code.

## Quick Start

```
1. Detect encoding → 2. Fetch real HTML → 3. Query knowledge base → 4. Analyze structure → 5. Create book source
```

Rules should be derived from actual HTML analysis rather than assumptions.

## Usage Scope

This skill is intended for developing book sources for websites the user owns or has authorization to access. The included tools (URL analysis, HTML fetching, source uploading) should only be used on target sites with the user's explicit consent. Do not use these tools for unauthorized scraping, bypassing access controls, or accessing content without permission.

## Tools

### Knowledge Query
| Tool | Purpose |
|------|---------|
| `search_knowledge(query)` | Search knowledge base |
| `get_css_selector_rules()` | CSS selector reference (paginated) |
| `get_real_book_source_examples(limit)` | Real book source analysis results |
| `get_book_source_templates(limit)` | Proven book source templates |
| `read_file_paginated(path, page)` | Read large files with pagination |
| `list_all_knowledge_files()` | List all knowledge files |

### HTML Analysis
| Tool | Purpose |
|------|---------|
| `smart_fetch_html(url, method, body, headers, charset)` | Fetch HTML with encoding support |
| `smart_web_analyzer(html)` | Full page structure analysis |
| `smart_bookinfo_analyzer(html)` | Book info page analysis |
| `smart_toc_analyzer(html)` | Table of contents analysis |
| `smart_content_analyzer(html)` | Content page analysis |

### Book Source Management
| Tool | Purpose |
|------|---------|
| `edit_book_source(complete_source="JSON")` | Create/edit book source |
| `validate_book_source.py` | Validate book source JSON (in `tools/`) |

### Analysis Scripts (in `tools/`)
| Script | Deps | Purpose |
|--------|------|---------|
| `analyze_url.py` | requests, bs4 | Website analysis (encoding + structure + search API) |
| `analyze_url.sh` | curl | Website analysis (no Python required) |
| `quick_analyze.py` | requests, bs4 | Quick analysis with auto HTML storage |
| `js_param_analyzer.py` | requests, bs4 | JS parameter/endpoint analysis |
| `validate_book_source.py` | — | Book source JSON validation (no deps) |
| `upload_book_source.py` | requests | Upload book source to public image host (default: tu.406np.xyz) for shareable direct links |

> No Python? See `references/no_python_workflow.md` for using host MCP tools (browser, HTTP, code execution).

## 3-Phase Workflow

### Phase 1: Information Collection

**Step 1: Query Knowledge Base**
```
search_knowledge("CSS选择器格式 提取类型 @text @html @href @src")
get_real_book_source_examples(limit=5)
get_book_source_templates(limit=3)
```

**Step 2: Detect Encoding (once, at start)**
```
detect_charset(url="http://example.com")
```
- UTF-8 → omit charset (default)
- GBK/GB2312 → add `"charset":"gbk"` to all requests

**Step 3: Fetch Real HTML**
```
smart_fetch_html(url="http://example.com/search", charset="gbk")
smart_fetch_html(url="http://example.com/search", method="POST",
                 body="keyword={{key}}&t=1", charset="gbk")
```

**Step 4: Analyze Structure**
```
smart_web_analyzer(html="...")
smart_bookinfo_analyzer(html="...")
smart_toc_analyzer(html="...")
smart_content_analyzer(html="...")
```

### Phase 2: Review

1. Write rules based on knowledge base + real HTML analysis
2. Validate CSS selectors, extraction types, regex format
3. Handle special cases (no cover, lazy loading, merged info)

When uncertain, ask the user rather than guessing.

### Phase 3: Create Book Source

1. Prepare complete JSON with all required fields
2. Call `edit_book_source(complete_source="完整JSON")`
3. Output as standard JSON array (no comments, no code blocks)

## Rule String Format

```
CSS选择器@提取类型##正则表达式##替换内容
```

**Extraction Types:**
- `@text` — text content (includes children)
- `@ownText` — element text only (excludes children)
- `@html` — HTML structure
- `@textNode` — text nodes
- `@href` — link URL
- `@src` — image source
- `@js` — JavaScript processing

**Numeric Indices:**
- `.0` = first, `.-1` = last (NOT `:first-child` / `:last-child`)

**Text Selection:**
- `text.关键词` (NOT `:contains()`)

## Common Patterns

**Standard list with cover:**
```json
{"bookList": ".book-list .item", "name": ".title@text", "bookUrl": "a@href", "coverUrl": "img@src"}
```

**No cover on search page:**
```json
{"coverUrl": ""}
```

**Lazy loading images:**
```json
{"coverUrl": "img@data-original||img@src"}
```

**nextContentUrl rule:** Chapter number changes → SET it. Page number only → LEAVE EMPTY.

## Known Constraints

**Unsupported fields (not in Legado source):**
- `prevContentUrl` does not exist
- `:contains()` pseudo-class is not supported (use `text.关键词`)
- `:first-child` / `:last-child` are not supported (use `.0` / `.-1`)

**Recommended practices:**
- Base rules on real HTML analysis rather than assumptions
- Query the knowledge base before writing rules
- Detect encoding once at the start

**Required fields:** See `references/legado_data_structures.md` for complete field specs from BookSource.kt, SearchRule.kt, TocRule.kt, ContentRule.kt, BookInfoRule.kt.

## References

| File | Content |
|------|---------|
| `references/legado_development_guide.md` | Workflow, HTML patterns, encoding, regex, troubleshooting |
| `references/legado_data_structures.md` | Source code analysis: data structures, rule engine, DB schema |
| `references/Legado书源开发完整指南.md` | Comprehensive development guide |
| `references/用户交互指南.md` | Common scenario interaction flows |
| `references/方法-JS扩展类.md` | JavaScript API documentation |
| `references/Legado书源编码处理指南.md` | Encoding handling guide |
| `references/knowledge_base/book_sources/` | Real book source analysis (MD) |
| `references/book_source_database/book_sources/` | Book source database (JSON) |

## Most Used Patterns (from real sources)

**CSS Selectors:** `img`(40x), `h1`(30x), `div`(13x), `content`(12x), `intro`(11x), `h3`(9x)

**Extraction Types:** `@href`(81x), `@text`(72x), `src`(60x), `@html`(33x), `@js`(25x)
