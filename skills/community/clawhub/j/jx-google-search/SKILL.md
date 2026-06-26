---
name: google-search
description: Search the web using SkillBoss API Hub. Use this when you need live information, documentation, or to research topics and the built-in web_search is unavailable.
---

# Google Search Skill

This skill allows OpenClaw agents to perform web searches via SkillBoss API Hub (unified web search routing).

## Setup

1.  **SkillBoss API Key:** Obtain your API key from SkillBoss API Hub.
2.  **Environment:** Store your credentials in a `.env` file in your workspace:
    ```
    SKILLBOSS_API_KEY=your_key_here
    ```

## Workflow
... (rest of file)

## Example Usage

```bash
SKILLBOSS_API_KEY=xxx python3 skills/google-search/scripts/search.py "OpenClaw documentation"
```
