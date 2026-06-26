---
name: playwright-browser
description: |
  Use Playwright to browse websites with a real (non-headless) browser and extract data by hooking network responses.
  Use when the user wants to:
  - View a website's content, especially SPAs (Single Page Applications)
  - Navigate websites and click links
  - Search for keywords within web pages
  - Extract data from JavaScript-heavy sites
  - Capture API responses directly
  Triggers on: "查看网页", "browse site", "get content from URL", 
  "extract data from website", "hook API responses", "抓取网页内容",
  "find link", "click link", "search page"
---

# Playwright Browser Skill

## Purpose

This skill enables OpenClaw to launch a real Chrome/Chromium browser (non-headless), navigate to websites, and extract content by:
1. Scraping rendered DOM content
2. Hooking and capturing network responses (XHR/Fetch API calls)
3. Finding and clicking links
4. Searching for keywords in page content
5. Focusing on specific elements

## Prerequisites

Ensure Playwright is installed:
```bash
pip install playwright
playwright install chromium
```

## Usage

### 1. Basic Navigation and Content Extraction

```python
from skills.playwright-browser.scripts.browser_agent import SyncBrowserAgent

agent = SyncBrowserAgent(headless=False)
content = agent.get_page_content("https://example.com")
print(f"Title: {content['title']}")
agent.close()
```

### 2. Find and Click Links

```python
from skills.playwright-browser.scripts.browser_agent import SyncBrowserAgent

agent = SyncBrowserAgent(headless=False)
agent.navigate("https://sina.com")

# Find links containing specific text
links = agent.find_links_by_text("军事")
for link in links:
    print(f"Found: {link['text']} -> {link['href']}")

# Click the first matching link
agent.find_link_and_click("军事")

agent.close()
```

### 3. Search Page Content

```python
agent = SyncBrowserAgent(headless=False)
agent.navigate("https://mil.news.sina.com.cn/")

# Search for keyword in page
results = agent.search_page_content("伊朗")
for r in results:
    print(f"Found: {r['text']}")

# Focus on first result
if results:
    agent.focus_on_element(results[0])

agent.close()
```

### 4. Hook Network Responses

```python
agent = SyncBrowserAgent(headless=False)

def on_api_response(response):
    if response.resource_type in ['xhr', 'fetch']:
        print(f"API: {response.url}")

agent.hook_network_responses(on_api_response)
agent.navigate("https://spa-app.example.com")

# Get all captured API calls
api_calls = agent.get_captured_api_calls()
agent.close()
```

## Safety Guidelines

- **NEVER** navigate to suspicious or potentially malicious URLs
- Always validate URLs before navigation
- Respect robots.txt and website terms of service
- Warn user when accessing sites that may contain sensitive content
- Close browser when done to free resources
