---
name: live-web-page-browser
description: "Live Web Page Browser: Fetch live webpages: return HTML, Markdown, or screenshots. Headless browser at edge for real-time content extraction and visual capture. Use when an agent needs live web page browser, real time research & information gathering, competitive intelligence & market monitoring, content verification & fact checking, visual documentation & change detection, cancel crawl, job id, get crawl result through AgentPMT-hosted remote tool calls."
version: 1.0.2
homepage: https://www.agentpmt.com/marketplace/live-web-page-browser
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/live-web-page-browser"}}
---
# Live Web Page Browser

## Freshness
Last updated: `2026-10-22`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
Fetch any webpage and return the live version. Return options include markdown only, html, and screen shot images, allowing you to return only what your agent needs, using minimal context and tokens. Live search bypasses search restrictions built in to many well known agents. Enables seamless agentic website access for AI assistants and large language models and provides AI agents with programmatic web interaction capabilities including HTML content retrieval, intelligent Markdown conversion, and screenshot capture—all through simple, structured tool commands. it delivers a secure, low-latency solution for headless browser automation at the edge. This MCP server transforms how AI agents perceive and interact with the live web, enabling real-time content extraction, web scraping, and visual page capture without requiring vision models or complex browser infrastructure.

## When To Use
- Use this skill for `Live Web Page Browser` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: live web page browser, real time research & information gathering, competitive intelligence & market monitoring, content verification & fact checking, visual documentation & change detection, cancel crawl, job id, get crawl result.
- Supported action names: `cancel_crawl`, `get_crawl_result`, `get_instructions`, `get_url_html_content`, `get_url_json`, `get_url_links`, `get_url_markdown`, `get_url_pdf`, `get_url_screenshot`, `get_url_snapshot`, `kill_browser_session`, `list_browser_sessions`, `scrape_url_elements`, `start_crawl`.

## Use Cases
- Real-Time Research & Information Gathering
- Competitive Intelligence & Market Monitoring
- Content Verification & Fact-Checking
- Visual Documentation & Change Detection
- Data Extraction for RAG Pipelines
- Automated Form Pre-Population & Workflow Prep
- Accessibility & Content Summarization

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `14`.
x402 availability: not enabled for this product.

- `cancel_crawl` (action slug: `cancel-crawl`): Cancel a running crawl job Price: `5` credits. Parameters: `job_id`.
- `get_crawl_result` (action slug: `get-crawl-result`): Get the status and records of a crawl job started with start_crawl Price: `5` credits. Parameters: `job_id`.
- `get_instructions` (action slug: `get-instructions`): Get tool instructions and available actions. Price: `5` credits. Parameters: none.
- `get_url_html_content` (action slug: `get-url-html-content`): Get page HTML content Price: `5` credits. Parameters: `browser`, `url`.
- `get_url_json` (action slug: `get-url-json`): Extract structured JSON from a page using AI. Provide a prompt and/or a response_format JSON schema to guide extraction. Price: `5` credits. Parameters: `browser`, `prompt`, `response_format`, `url`.
- `get_url_links` (action slug: `get-url-links`): Get the list of links on a page Price: `5` credits. Parameters: `browser`, `url`, `visibleLinksOnly`.
- `get_url_markdown` (action slug: `get-url-markdown`): Get page converted into Markdown Price: `5` credits. Parameters: `browser`, `url`.
- `get_url_pdf` (action slug: `get-url-pdf`): Render a page to PDF Price: `5` credits. Parameters: `browser`, `url`.
- `get_url_screenshot` (action slug: `get-url-screenshot`): Get page screenshot Price: `5` credits. Parameters: `browser`, `url`, `viewport`.
- `get_url_snapshot` (action slug: `get-url-snapshot`): Get page HTML content and a screenshot in a single call Price: `5` credits. Parameters: `browser`, `url`.
- `kill_browser_session` (action slug: `kill-browser-session`): Close (kill) a Browser Run session by its session ID Price: `5` credits. Parameters: `session_id`.
- `list_browser_sessions` (action slug: `list-browser-sessions`): List active Browser Run sessions for the account Price: `5` credits. Parameters: none.
- `scrape_url_elements` (action slug: `scrape-url-elements`): Scrape elements from a page by CSS selector Price: `5` credits. Parameters: `browser`, `elements`, `url`.
- `start_crawl` (action slug: `start-crawl`): Start an asynchronous crawl of a website. Returns a job_id — poll get_crawl_result to retrieve records. Price: `5` credits. Parameters: `browser`, `depth`, `limit`, `render`, `url`.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "live-web-page-browser"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "live-web-page-browser"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "live-web-page-browser"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "live-web-page-browser"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "live-web-page-browser"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "live-web-page-browser"
  }
}
```

## Call This Tool
Product slug: `live-web-page-browser`

Marketplace page: https://www.agentpmt.com/marketplace/live-web-page-browser

- AgentPMT account route: first use `../agentpmt-account-mcp-rest-api-setup` to connect the main MCP server or REST API for an Agent Group where this tool is enabled.
- x402 route: not enabled for this product.
- AgentPMT overview: use `../what-is-agentpmt` for marketplace, Agent Group, workflow, MCP, REST, and payment concepts.

If those setup skills are not installed beside this product skill, use the downloads below.

Core AgentPMT setup skills:
- What AgentPMT is: ../what-is-agentpmt
  - ClawHub page: https://clawhub.ai/agentpmt/what-is-agentpmt
  - OpenClaw install: `openclaw skills install what-is-agentpmt`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup
  - ClawHub page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup
  - OpenClaw install: `openclaw skills install agentpmt-account-mcp-rest-api-setup`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`

skills.sh install script:

```bash
npx skills add AgentPMT/agent-skills --skill what-is-agentpmt
npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup
```

MCP call shape after the main AgentPMT MCP server is connected:

```json
{
  "method": "tools/call",
  "params": {
    "name": "Live-Web-Page-Browser",
    "arguments": {
      "action": "cancel_crawl",
      "job_id": "example job id"
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "live-web-page-browser",
  "parameters": {
    "action": "cancel_crawl",
    "job_id": "example job id"
  }
}
```

Use the setup skill for the account connection details before making REST calls.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `cancel_crawl` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/live-web-page-browser
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
