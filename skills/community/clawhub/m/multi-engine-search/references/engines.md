# Search Engine Reference

## Supported Engines

### Tavily (Recommended)

**Type:** API-based
**Speed:** Fastest
**Requirements:** API key

Tavily is a search API optimized for AI agents. It provides:
- Fast, clean results
- Optional AI-generated answer summaries
- No rate limiting for reasonable use
- Simple JSON output

**Get API Key:** https://tavily.com

**Configuration:**
```bash
# Environment variable
export TAVILY_API_KEY="tvly-xxxx"

# Or in ~/.openclaw/.env
TAVILY_API_KEY=tvly-xxxx
```

---

### Google

**Type:** Browser-based
**Speed:** Slow
**Requirements:** agent-browser

**URL Template:**
```
https://www.google.com/search?q={query}
```

**Best for:**
- Comprehensive web results
- International content
- Academic and technical queries
- Image search (add `&tbm=isch`)

**URL Parameters:**
- `hl` - Interface language (e.g., `hl=en`, `hl=zh-CN`)
- `lr` - Limit to language (e.g., `lr=lang_zh-CN`)
- `num` - Results per page (default 10)
- `tbm=isch` - Image search
- `tbm=nws` - News search

**Example URLs:**
```
https://www.google.com/search?q=openai&hl=en&num=20
https://www.google.com/search?q=AI&tbm=nws
https://www.google.com/search?q=cats&tbm=isch
```

---

### Bing

**Type:** Browser-based
**Speed:** Slow
**Requirements:** agent-browser

**URL Template:**
```
https://www.bing.com/search?q={query}
```

**Best for:**
- Microsoft ecosystem content
- Image and video search
- Alternative to Google

**URL Parameters:**
- `setlang` - Interface language
- `count` - Results per page
- `first` - Offset for pagination

**Example URLs:**
```
https://www.bing.com/search?q=microsoft+azure&count=20
https://www.bing.com/images/search?q=cats
https://www.bing.com/videos/search?q=tutorials
```

---

### Baidu

**Type:** Browser-based
**Speed:** Slow
**Requirements:** agent-browser

**URL Template:**
```
https://www.baidu.com/s?wd={query}
```

**Best for:**
- Chinese content
- Domestic Chinese websites
- Local Chinese services
- Chinese news and media

**URL Parameters:**
- `wd` - Search query (word)
- `rn` - Results per page
- `pn` - Page number offset
- `tn` - Search type (news, images, etc.)

**Special Searches:**
```
https://www.baidu.com/s?wd=关键词&tn=news  # News
https://image.baidu.com/search?word=关键词  # Images
https://www.baidu.com/s?wd=关键词&tn=baidulocal  # Local
```

---

### DuckDuckGo

**Type:** Browser-based
**Speed:** Slow
**Requirements:** agent-browser

**URL Template:**
```
https://duckduckgo.com/?q={query}
```

**Best for:**
- Privacy-focused search
- No tracking or profiling
- Clean results
- Alternative perspectives

**URL Parameters:**
- `kl` - Region (e.g., `kl=cn-zh`, `kl=us-en`)
- `ia` - Instant answer type

**Example URLs:**
```
https://duckduckgo.com/?q=openai&kl=us-en
https://duckduckgo.com/?q=隐私&kl=cn-zh
```

---

## Comparison Table

| Engine | Type | Speed | Chinese Support | Privacy | Best For |
|--------|------|-------|-----------------|---------|----------|
| Tavily | API | ⚡⚡⚡ | Good | Medium | General search, AI summaries |
| Google | Browser | ⚡ | Excellent | Low | Comprehensive results, international |
| Bing | Browser | ⚡ | Good | Medium | Microsoft content, images |
| Baidu | Browser | ⚡ | Excellent | Low | Chinese content, local services |
| DuckDuckGo | Browser | ⚡ | Fair | High | Privacy-focused searches |

---

## Choosing the Right Engine

### By Content Type

| Content | Recommended Engine |
|---------|-------------------|
| General web | Tavily (fast) or Google (comprehensive) |
| Chinese content | Baidu |
| Academic/technical | Google or Tavily |
| News | Google News, Baidu News |
| Images | Google Images, Bing Images, Baidu Images |
| Privacy-sensitive | DuckDuckGo |

### By Use Case

| Use Case | Recommended |
|----------|-------------|
| Quick lookup | Tavily |
| Research | All engines (aggregated) |
| Chinese market research | Baidu + Google |
| International news | Google News |
| Privacy matters | DuckDuckGo |
| Technical documentation | Tavily or Google |

---

## Rate Limiting & Best Practices

1. **Keep requests reasonable** - Don't spam search engines
2. **Use Tavily for bulk searches** - API is designed for automation
3. **Browser searches are slower** - Each requires page load
4. **Cache results** - Avoid repeating identical queries
5. **Respect robots.txt** - Follow site policies

---

## Troubleshooting

### Tavily Errors

```
"TAVILY_API_KEY not found"
```
→ Set environment variable or add to `~/.openclaw/.env`

```
"requests module not installed"
```
→ Run: `pip install requests`

### Browser Errors

```
"agent-browser not found"
```
→ Run: `npm install -g agent-browser && agent-browser install`

```
"Search timed out"
```
→ Page took too long to load. Try again or use different engine.

### No Results

- Check query encoding (use URL encoding for special characters)
- Try different engine
- Verify network connectivity
- Check if search engine is blocking automated requests
