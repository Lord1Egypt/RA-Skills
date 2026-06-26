---
name: "openclaw-docs-search"
description: "Real-time retrieval of the latest official OpenClaw documentation, returned as compact LLM-friendly Markdown for config, CLI, channels, gateway, and skills questions."
homepage: "https://docs.openclaw.ai/"
user-invocable: true
---

# openclaw-docs-search

This skill is built for ClawHub / OpenClaw workflows and is designed to retrieve the latest official OpenClaw documentation in real time, then return it as LLM-friendly Markdown.
Its core strengths are real-time retrieval, official-source grounding, and up-to-date public documentation access. It uses the official search workflow first, then fetches a single target page on demand instead of relying on stale model memory, cached snapshots, or full-site crawling.

## One-Line Pitch

Stop relying on stale model memory and answer from the latest official OpenClaw docs in real time.

## Why Use It

- Answers questions using the latest official OpenClaw docs, reducing stale answers and hallucination risk
- Returns compact Markdown instead of noisy raw payloads, making follow-up reasoning easier for the model
- Supports on-demand retrieval of a single documentation page, keeping responses fast and token-efficient
- Works especially well for setup, configuration, CLI, skills, gateway, diagnostics, and channel integration questions

## Core Selling Points

- Real-time retrieval: queries the official search endpoint first to access the latest public documentation
- Official-source grounding: works directly against OpenClaw official docs for more trustworthy answers
- LLM-friendly output: extracts the main article body and converts it into clean Markdown for summarization and follow-up questions

## How It Saves Tokens

- Search responses are converted into compact Markdown instead of returning raw JSON
- Only high-value fields are kept, such as breadcrumbs, page path, and cleaned content
- Highlight tags, repeated titles, and extra line breaks are removed from search snippets
- Detailed retrieval is done one page at a time instead of loading large document sets
- Only the `#content-area` main content is extracted from a page, without full navigation, footer, or other noise
- This "search first, then read one page on demand" workflow helps reduce unnecessary context and token usage

## Who Should Install It

- Individual developers who want assistants to answer from official OpenClaw sources
- AI assistant or skill authors who want higher answer accuracy and fewer hallucinations
- Teams that frequently handle deployment, configuration, troubleshooting, channel integration, and skill development

## Best-Fit Scenarios

- The user asks for answers grounded in the latest official OpenClaw docs rather than model memory
- The user needs help with OpenClaw installation, configuration, CLI, channels, skills, gateway, diagnostics, or operations
- The agent needs to quickly locate a specific official doc page and return a concise summary
- The agent needs to inspect one document in more detail while minimizing noise and token usage

## When To Invoke This Skill

Use this skill before answering or taking action when the task depends on current OpenClaw official documentation, especially when stale memory could cause wrong guidance, outdated instructions, or incorrect configuration changes.

For high-risk OpenClaw tasks, the agent should invoke this skill first before answering, generating instructions, or editing files.

- Before modifying any OpenClaw configuration file, first check the latest official docs for field names, structure, defaults, and recommended examples
- Before using an OpenClaw feature that is not fully familiar, look up the official docs to understand its purpose, limitations, configuration method, and recommended usage
- When the user asks about OpenClaw config, CLI, channels, gateway, skills, diagnostics, deployment, or operational behavior
- Before generating configuration examples, command examples, setup steps, or integration instructions that must match the latest documentation
- When the model is unsure whether its current knowledge is accurate, current, or version-compatible
- When the task requires minimizing hallucination risk or avoiding outdated OpenClaw guidance

## High-Risk Rule

If the task involves modifying configuration files, generating commands, adjusting gateway or skills settings, integrating channels, or giving operational guidance, the agent should verify the latest official documentation with this skill first instead of relying on memory.

## Example Questions

- Where is the latest OpenClaw Skills configuration documentation?
- What does the official documentation say about the CLI?
- Can you find the latest official Gateway documentation?
- What does the current official documentation say about channel integration?

> **Important:**
> Because the official English documentation has a much higher search hit rate than the Chinese version, **always translate a user's Chinese intent into English keywords before searching**. The default search language should be `en`. Only use `zh-Hans` when Chinese results are explicitly required.

## Step 1: Keyword Search
First, send a POST request to the OpenClaw official search API. Extract the user's intent, translate it into **English** keywords, and set `language` to `en`.

You can retrieve results with the following `curl` command:

```bash
curl --location --request POST 'https://leaves.mintlify.com/api/search/clawdhub' \
--header 'Content-Type: application/json' \
--data-raw '{
  "query": "<english search keywords>",
  "filters": {
    "language": "en"
  }
}'
```

## Step 2: Result Cleanup and Formatting
To reduce LLM token usage and reading noise, the skill filters the returned JSON and converts it into Markdown.
1. Extract `breadcrumbs` with navigation context, or fall back to `title`.
2. Keep the exact page path from `page`.
3. Clean the `content` field by removing repeated titles and unnecessary blank lines.
4. Discard low-value fields such as `score`, `hash`, and `icon`.

The final Markdown structure looks like this and can be passed directly to an LLM:
```markdown
### 1. Agent > Messaging and Delivery > Command Queue
- **Path**: `zh-CN/concepts/queue`
- **Content**: Command Queue (2026-01-16)
We use a small in-process queue to serialize inbound auto-reply execution across channels, preventing conflicts between agent runs while still allowing safe concurrency across sessions.

### 2. ...
```

## Step 3: Fetch and Parse a Specific Document
When the LLM decides to inspect a specific document based on search results or prior hints, use the selected item's **path** from the `page` field.
1. Join the base URL `https://docs.openclaw.ai/` with the selected `page` path, for example `https://docs.openclaw.ai/zh-CN/tools/skills-config`.
2. Send a GET request to fetch the full HTML page.
3. Parse the HTML and extract only the element with `id="content-area"`.
4. Use `turndown` to convert the extracted HTML into LLM-friendly Markdown.
5. Fetch only the page you need instead of crawling the entire site.

## Output Requirements

- Prefer compact Markdown over raw JSON for search results
- Remove search highlight tags, redundant metadata, repeated titles, and irrelevant noise
- For detail pages, keep only the `#content-area` main content and exclude full-page navigation, footer, or script content
- Preserve source paths whenever possible so the user or agent can continue exploring

## Constraints

- Do not mirror or crawl the full site in bulk
- Do not request sensitive pages unrelated to public documentation content
- Do not return real secrets, tokens, or private user information
- Prefer an on-demand retrieval workflow to minimize unnecessary requests

## Execution Guidance

- Prefer available HTTP or web-fetch tools for both search and detail retrieval
- During search, call the official search endpoint first and extract `page` from the results
- For detail view, build the URL by joining `https://docs.openclaw.ai/` with `page`
- Extract only the HTML inside `#content-area`, then convert it into Markdown
- If result quality is weak, rewrite the query into more precise English keywords and search again
