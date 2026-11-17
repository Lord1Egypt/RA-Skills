# Network Request Twister

> Observe and modify browser network requests/responses via Chrome DevTools Protocol — no browser extensions required.

A [Crush](https://crush.sh) skill.

## What it does

- **Monitor** HTTP traffic in real time with JSONL output and URL/type filters
- **Block** requests (analytics, tracking, ads) before they reach the server
- **Mock** API responses with custom JSON
- **Modify** request/response headers, URLs, cookies, query params, and bodies
- **Inject** scripts or HTML into pages
- 25 match conditions + 17 actions, covering request and response stages

## Install

```bash
npx skills add 241x/network-request-twister
```

## Usage

Once installed, the skill triggers when you ask your AI assistant things like:

```
"Show me what requests this page makes"
"Block all analytics requests on this site"
"Replace the /api/users response with custom JSON"
"Add an Authorization header to all API calls"
"Remove UTM tracking parameters from URLs"
```

See [SKILL.md](SKILL.md) for full documentation and `examples/` for config templates.
