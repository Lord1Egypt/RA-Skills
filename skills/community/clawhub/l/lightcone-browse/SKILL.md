---
name: lightcone-browse
description: |
  Computer-use automation via Lightcone. Activate when user asks to browse websites, scrape web pages, automate web tasks, check prices, monitor sites, fill forms, or operate web applications. Northstar sees the screen and acts — no selectors or scripts needed.
user-invocable: true
command-dispatch: tool
command-tool: lightcone_browse
command-arg-mode: raw
metadata: {"openclaw":{"emoji":"🌐","homepage":"https://docs.lightcone.ai","requires":{"env":["TZAFON_API_KEY"]},"primaryEnv":"TZAFON_API_KEY"}}
---

# Lightcone Browse

Delegate browser tasks to a cloud computer powered by Lightcone. Northstar sees the screen, decides what to click, type, or scroll — and acts. You describe what you want done, Northstar does it.

## When to use Lightcone

- No local browser available (headless, Docker, server deployments)
- Need parallel sessions (multiple sites at once)
- Vision-based automation (Northstar reads the screen — no selectors, no scripts to maintain)
- Desktop or browser environments

## Tool: `lightcone_browse`

### Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `instruction` | Yes | Plain language task for Northstar |
| `url` | No | Starting URL to navigate to first |
| `maxSteps` | No | Max steps before stopping (default: 50) |

### Example instructions

**Price checking:**
```
instruction: "Find the current price of a MacBook Air M4 on Amazon"
url: "https://www.amazon.com"
```

**Data extraction:**
```
instruction: "Go to the pricing page and extract all plan names, prices, and feature lists"
url: "https://example.com/pricing"
```

**Form filling:**
```
instruction: "Fill out the contact form with name 'Jane Doe', email 'jane@example.com', and message 'Hello'"
url: "https://example.com/contact"
```

## Tips for good instructions

- Be specific about what "done" looks like: "find the price" not "look around"
- Name the exact elements: "click the Sign In button" not "log in somehow"
- For multi-step tasks, describe the sequence: "First search for X, then sort by price, then get the top 3 results"
- Include what to extract: "tell me the title, price, and rating"

## How it works

1. Lightcone creates a cloud computer with a browser
2. Northstar sees the screen via screenshots
3. It decides what to click, type, or scroll — step by step
4. When done, it returns the page content and a screenshot
5. The computer is automatically shut down

For step-by-step manual control, see the **lightcone-session** skill.
