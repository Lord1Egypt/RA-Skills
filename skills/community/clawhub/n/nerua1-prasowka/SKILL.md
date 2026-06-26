---
name: prasowka
description: >
  Generate a daily news portal as a single HTML file.
  Uses fetch_news.py + web_fetch + LLM for summaries.
  18 categories, dark/light toggle, responsive layout.
tools:
  - exec
  - web_search
  - web_fetch
  - write
---

# Daily News Portal (Prasowka)

Generate a daily news portal as a single HTML file.

## Parameters
- OUTPUT: `<workspace>/canvas/prasowka-{YYYYMMDD}.html`
- DATA_DIR: `<workspace>/skills/prasowka/data`
- REFS_DIR: `<workspace>/skills/prasowka/references`

## Steps

### Step 1: Initialize
```bash
mkdir -p <workspace>/canvas <workspace>/skills/prasowka/data
DATE=$(date +%Y%m%d)
SEEN_URLS_FILE="$DATA_DIR/seen_urls.json"
```

### Step 2: Load Configuration
Read `$REFS_DIR/topics.md` — format:
```
ai-models: 15
ai-tools: 10
ai-video: 15
...
```

### Step 3: Fetch News per Topic
Launch a subagent for each topic:
```python
def fetch_topic_news(topic, limit):
    result = subprocess.run([
        "python3", "scripts/fetch_news.py",
        "--topic", topic,
        "--limit", str(limit)
    ], capture_output=True, text=True)
    
    if result.returncode != 0:
        return web_search(f"latest {topic} news {limit}")
    
    return json.loads(result.stdout)
```

### Step 4: Filter URLs
```python
def filter_new_urls(articles, seen_urls):
    return [a for a in articles if a['url'] not in seen_urls]
```

### Step 5: Fetch & Summarize per Article
Launch a subagent for each article:
```python
def summarize_article(url):
    content = web_fetch(url, extract_text=True)
    if not content or len(content) < 100:
        return None
    summary = llm_summarize(content[:3000])
    return summary
```

### Step 6: Generate HTML
Use template with dark/light toggle, 18 categories, 2-3 sentence summaries.

### Step 7: Save & Update
- Save HTML to canvas
- Update seen_urls.json
- Run prasowka-guardian validation

## Error Handling
- fetch_news.py fails → fallback to web_search
- Article unavailable → skip
- Summary empty → use first 3 sentences
- Don't stop — keep going

## Requirements
- `scripts/fetch_news.py`
- `references/topics.md`
- `references/format.md`

---

If this saved you time: [☕ PayPal.me/nerudek](https://www.paypal.me/nerudek)
