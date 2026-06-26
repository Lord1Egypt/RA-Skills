---
name: jinritoutiao-keyword-collector
description: Automatically accesses the Jinri Toutiao homepage via browser automation, inputs keywords into the search bar, and collects related keyword suggestions from the auto-suggest dropdown.
---

# Jinri Toutiao Keyword Collector

## Feature Overview

This skill uses browser automation to access Jinri Toutiao (www.toutiao.com), simulates user behavior of entering keywords in the search box, and automatically collects the relevant keyword suggestions displayed in the search dropdown.

## Trigger Conditions

Trigger this skill when the user mentions any of the following keywords:
- 今日头条关键词
- 收集头条关键词
- 头条搜索建议
- 头条热门词
- 头条 SEO
- 头条话题
- Jinri Toutiao keywords
- Collect Toutiao keywords
- Toutiao search suggestions
- Toutiao trending keywords
- Toutiao SEO
- Toutiao topics

## Use Cases

- SEO keyword research and optimization
- Content creation inspiration gathering
- Trending topic discovery
- Competitor keyword analysis
- Market research and trend analysis

## Operation Workflow

### 1. Launch Browser

Use the `browser` tool to launch the browser:

```
action: start
profile: openclaw
```

### 2. Access Jinri Toutiao Homepage

Navigate to Jinri Toutiao:

```
action: navigate
targetUrl: https://www.toutiao.com
```

Wait for the page to fully load.

### 3. Get Page Snapshot

Use `snapshot` to get the page element structure and locate the search box:

```
action: snapshot
refs: aria
```

Search for the search box element in the snapshot results (typically an input element containing keywords like "search").

### 4. Input Keywords

Use the `act` tool to input keywords into the search box:

```
action: act
ref: <ref value of the search box>
kind: type
text: <user-provided keyword>
slowly: true
```

Set `slowly: true` to ensure the page can properly trigger the auto-suggest functionality.

### 5. Wait for Suggestion Dropdown

After input is complete, wait 1-2 seconds for the auto-suggest dropdown to load:

```
action: act
kind: wait
timeMs: 2000
```

### 6. Get Dropdown Snapshot

Take another page snapshot, this time capturing the keyword list in the auto-suggest dropdown:

```
action: snapshot
refs: aria
```

### 7. Extract Keywords

Extract all keyword text from the snapshot results within the suggestion dropdown. The dropdown typically contains multiple `option`, `li`, or `div` elements, each containing a suggested keyword.

### 8. Output Format

```
Keyword: [Input Keyword]
Search Suggestions:
1. Suggestion 1
2. Suggestion 2
3. Suggestion 3
...
```

### 9. Cleanup (Optional)

If the user has no further requests, close the browser:

```
action: close
```

## Important Notes

1. **Network Latency**: Jinri Toutiao page loading may take time; ensure sufficient waiting time before operations
2. **Element Locating**: Using `refs: aria` provides more stable element references
3. **Input Speed**: Setting `slowly: true` ensures the page can properly trigger auto-suggest
4. **Anti-scraping Mechanisms**: Avoid frequent requests in a short period; it is recommended to wait 5-10 seconds between multiple collections
5. **Session Persistence**: For multiple collections, keep the browser session open to improve efficiency

## Batch Collection for Multiple Keywords

To collect suggestions for multiple keywords:

1. Keep the browser session open
2. Repeat steps 4-7 for each keyword
3. Use `act` with `kind: type` to clear the search box before entering a new keyword
4. Compile all results into a summary report

## Troubleshooting

### Search Box Not Found

- Check if the page has fully loaded
- Try refreshing the page and retrying
- Use a more detailed snapshot (add the `depth` parameter)

### Suggestion Dropdown Does Not Appear

- Ensure input speed is slow enough (`slowly: true`)
- Increase wait time (`timeMs: 3000` or longer)
- Check if the network connection is normal

### Keyword List is Empty

- Verify the input keyword is valid
- Try testing with common keywords
- Check if Jinri Toutiao has updated its page structure

## Reference Resources

- Browser Automation Best Practices: See `references/browser-automation-best-practices.md`
- Jinri Toutiao Page Structure Description: See `references/toutiao-structure.md`