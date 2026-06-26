---
name: google-serper-search
description: This skill should be used when the user asks to "search the web", "search for information", "find information online", "search Google", "search for images", "find pictures", or requests any web search or image search functionality.
---

# Google Serper Search

This skill enables you to search the web and find images using the Serper API.

## When to Use This Skill

Use this skill when the user:
- Asks to search for information online
- Needs current/recent information not in your knowledge base
- Requests to find images or pictures
- Wants to verify facts or get latest updates
- Asks questions that require web search

## How to Use

### Advanced Search

You can now use advanced parameters to filter results.

```bash
python3 scripts/serper_search.py "query" --type news --gl us --hl en --tbs "past week"
```

#### Parameters:
- **Type (`--type`)**: search, images, videos, places, maps, reviews, news, shopping, lens, scholar, patents, autocomplete.
- **Country (`--gl`)**: 2-letter country code (e.g., `us`, `cn`, `jp`, `gb`).
- **Language (`--hl`)**: Google language code (e.g., `en`, `zh-cn`, `zh-tw`, `ja`).
- **Date range (`--tbs`)**: `past hour`, `past 24 hours`, `past week`, `past month`, `past year`.

The script returns JSON with:
- `knowledgeGraph`: Key facts about the topic
- `organic`: Search results with title, link, and snippet
- `peopleAlsoAsk`: Related questions
- `relatedSearches`: Related search terms

### Image Search

When the user needs images, run:

```bash
python3 scripts/serper_search.py "search query" --type images
```

Returns JSON with image URLs, thumbnails, dimensions, and sources.

## Response Format

After getting search results:
1. Parse the JSON response
2. Present results in a clear, organized format
3. Include relevant links and sources
4. For images, describe what was found and provide image URLs

## Example Usage

User: "Search for the latest news about AI"
You: Use Bash tool to run the search script, then format and present the results.

User: "Find pictures of mountains"
You: Use Bash tool to run image search, then present the image URLs and descriptions.
