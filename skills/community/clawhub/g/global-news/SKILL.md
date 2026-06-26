---
name: global-news
description: Stay informed with Global News — get breaking news, top headlines, local city news, and full-text article search across Europe, Americas, Latin America, and Africa.
triggers:
  - news
  - headline
  - breaking news
  - top news
  - local news
  - what's happening
  - latest news
  - current events
  - city news
  - video
  - hot video
  - trending video
  - video search
---

# Global News

## About

Global News developed by Opera News.

Get up-to-date with the latest news from around the world! Global News delivers breaking news, headlines, and trending stories from dozens of countries — keeping you informed about the events that shape your community and the globe.

From live local news and daily briefings to international affairs, sports, politics, business, and weather alerts, Global News has you covered wherever you are and whatever you care about.

For more news, you can access https://www.operanewsapp.com

## API Base URL

`https://news-af.feednews.com/{country}/{language}/v1/mcp/news`

**Markets**: Europe (e.g. `de/de`, `fr/fr`, `gb/en`), Americas (`us/en`), Latin America (`br/pt`, `mx/es`, `ar/es`), Africa (`ng/en`, `za/en`, `ke/en`)

## Available Tools

### 1. get_global_top_news (PRIMARY — Use this for general news requests)

**Best for**: Daily briefings, "what's happening today", top headlines for a country

**API Call Example**:
```bash
curl -X GET "https://news-af.feednews.com/us/en/v1/mcp/news/top_news?request_count=10&product=openclaw"
```

**Parameters**:
- `country`: Market country code, e.g. `us`, `ng`, `de`, `br`
- `language`: Language code, e.g. `en`, `de`, `pt`, `es`
- `request_count` (optional): Number of articles to return (default: 30)
- `product`: Always pass `openclaw`

**Response**: JSON with `articles` array, each containing:
- `title`: Article headline
- `summary`: Short excerpt of the article
- `thumbnail`: Array of image URLs (may be empty)
- `transcoded_url`: Link to the full article

---

### 2. get_global_local_news

**Best for**: City-specific news, local events, community stories for a given city

**API Call Example**:
```bash
curl -X GET "https://news-af.feednews.com/us/en/v1/mcp/news/localnews?query=New%20York&product=openclaw"
```

**Parameters**:
- `country`: Market country code
- `language`: Language code
- `query`: City name. URL-encode spaces and special characters (e.g. `New York` → `New%20York`). Required — returns `400` if missing, `404` if city is not recognised.
- `product`: Always pass `openclaw`

**Response**: Same structure as `get_global_top_news`, articles are local to the specified city.

---

### 3. search_global_news

**Best for**: Topic-specific queries, answering "what happened with X", exploring a subject in depth

**API Call Example**:
```bash
curl -X GET "https://news-af.feednews.com/us/en/v1/mcp/news/search?query=election&page_size=10&product=openclaw"
```

**Parameters**:
- `country`: Market country code
- `language`: Language code
- `query`: Search keyword(s). URL-encode spaces and special characters (e.g. `nigeria election` → `nigeria%20election`). Required — returns `400` if missing or empty.
- `page_size` (optional): Number of articles per page (default: 9)
- `page_no` (optional): Zero-based page index for pagination (default: 0)
- `product`: Always pass `openclaw`

**Response**: Same structure as `get_global_top_news`

---

### 4. search_hot_videos

**Best for**: Finding trending or viral videos on a specific keyword or topic

**API Call Example**:
```bash
curl -X GET "https://news-af.feednews.com/$country/$language/clip/v1/video/search/hot?days=2&keyword=trump&size=5" \
  --header "country: $country" \
  --header "language: $language"
```

**Parameters**:
- `country`: Market country code, e.g. `us`, `ng`, `de`, `br` (path parameter only)
- `language`: Language code, e.g. `en`, `de`, `pt`, `es` (path parameter only)
- `days` (optional): Look-back window in days (default: 2)
- `keyword`: Search keyword(s). Required — the topic or person to search for
- `size` (optional): Number of videos to return (default: 5)

**Headers**:
- `country`: Same as the country path parameter
- `language`: Same as the language path parameter

**Response**: JSON with `content` array, each item containing:
- `id`: Video ID
- `description`: Video title / caption
- `thumbnail.url`: Thumbnail image URL
- `video.duration`: Duration in seconds
- `video.share_url`: Share link for the video
- `page_info.has_more`: Whether more results are available

---

## Workflow

### Step 1: Detect Market
- Infer country and language from the user's location, language, or explicit mention
- Default to `us/en` if unclear

### Step 2: Choose Tool
- **get_global_top_news**: User wants general headlines or a daily briefing
- **get_global_local_news**: User asks about news in a specific city
- **search_global_news**: User asks about a specific topic or event

### Step 3: Make API Call
Use the Bash tool to call the HTTP API.

### Step 4: Format Results
Present articles in a clean, readable format:

```markdown
### 📰 Top News — {Country}, {Date}

**1. {Title}**
{Summary}
🔗 [Read more]({transcoded_url})

**2. {Title}**
...
```

---

## Example Interactions

### Example 1: Daily Briefing

```
User: What's the news today in the US?
Assistant: Let me fetch today's top headlines for the US.

[Calls get_global_top_news: country=us, language=en, request_count=5]

### 📰 Top Headlines — United States

**1. Congress Reaches Budget Deal After Weeks of Negotiations**
Lawmakers have agreed on a spending framework to avoid a government shutdown...
🔗 [Read more](https://...)

**2. Tech Giants Report Strong Q1 Earnings**
Major technology companies posted better-than-expected quarterly results...
🔗 [Read more](https://...)

**3. Severe Storm Warning Issued Across the Midwest**
Forecasters are warning residents to prepare as a major storm system approaches...
🔗 [Read more](https://...)
```

### Example 2: Local City News

```
User: What's happening in Lagos today?
Assistant: Let me get the latest local news for Lagos.

[Calls get_global_local_news: country=ng, language=en, query=Lagos]

### 📰 Lagos Local News

**1. Lagos State Launches New Traffic Management Initiative**
Authorities unveiled a new plan to ease congestion on major roads in the city...
🔗 [Read more](https://...)

**2. Heavy Rainfall Causes Flooding in Parts of Lagos Island**
Residents in low-lying areas are advised to stay indoors as waters rise...
🔗 [Read more](https://...)
```

### Example 3: Topic Search

```
User: What's happening with the elections in Nigeria?
Assistant: Let me search for the latest news on Nigeria elections.

[Calls search_global_news: country=ng, language=en, query=elections, page_size=5]

### 📰 Nigeria Election News

**1. Election Commission Announces Voter Registration Deadline**
Nigeria's INEC has set a new deadline for voter registration ahead of upcoming polls...
🔗 [Read more](https://...)

**2. Presidential Candidates Hold Final Debate**
The three main candidates faced off in a televised debate focused on economic policy...
🔗 [Read more](https://...)
```

---

## Tips for Best Results

### 1. When to Use Each Tool

| Tool | Best For |
|------|----------|
| **get_global_top_news** | General briefing, "what's the news today" |
| **get_global_local_news** | City-specific news, local events |
| **search_global_news** | Specific topic, event, or keyword query |

### 2. Response Formatting Best Practices
- Show **5–10 articles** for briefings, **3–5** for specific searches
- Always include the `🔗 Read more` link using `transcoded_url`
- Skip articles where `transcoded_url` is empty
- Use `summary` as the article excerpt; omit if empty

---

## Important Notes

1. **Always call the API via Bash tool** — use `curl` GET requests
2. **Always include `product=openclaw`** in every request
3. **URL-encode `query`** — spaces become `%20` (applies to both search and local news)
4. `deeplink_url` is reserved and always empty — do not expose to users
5. Results are pre-filtered for quality and safety — safe to display directly
6. **Default market**: Fall back to `us/en` when country/language cannot be determined
