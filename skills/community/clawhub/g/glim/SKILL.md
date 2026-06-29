---
name: glim
description: Live data for AI agents - Twitter/X search, Reddit posts and comments, semantic web search, clean page extraction, GitHub repos/code/PRs, Amazon products, YouTube transcripts. One hosted MCP server at glim.sh/mcp. Sign in with OAuth and a prepaid balance, or pay per call with crypto (x402 USDC on Base/Solana, MPP on Tempo). No API keys to provision.
version: 1.0.0
homepage: https://glim.sh
metadata:
  openclaw:
    emoji: "✨"
    homepage: https://glim.sh
    requires:
      bins: [npx]
---

# Glim

Glim is a hosted MCP server that gives agents live external data: Twitter/X, Reddit, web search and page extraction, GitHub, Amazon, and YouTube transcripts. One endpoint, eleven tools, pay per call. No API keys to provision or rotate.

If `glim_*` tools are already available in your session, skip to Tools and use them directly.

## Connect

Add the endpoint to any MCP client:

```json
{
  "mcpServers": {
    "glim": {
      "url": "https://glim.sh/mcp"
    }
  }
}
```

Claude Code:

```bash
claude mcp add -s user -t http glim https://glim.sh/mcp
```

On first use the client runs a browser OAuth sign-in. Manage your balance and top up at [glim.sh/app](https://glim.sh/app); every call is billed against that balance at the prices below.

Restrict the tool list per session with the `?tools=` query parameter:

```
https://glim.sh/mcp?tools=glim_twitter_search,glim_web_fetch
```

## Headless fallback: pay per call with a crypto wallet

No browser or account needed. Calls are paid from a local wallet via the x402 protocol (USDC on Base or Solana):

```bash
npx x402-proxy setup                              # one-time: generate or import a wallet
npx x402-proxy wallet info                        # show address + USDC balance
npx x402-proxy mcp add glim https://glim.sh/mcp   # register glim in your MCP client behind a paying proxy
```

Fund the address shown by `wallet info` with USDC on Base or Solana. Tool calls then auto-pay on HTTP 402 challenges. MPP (Tempo) is also accepted on the same endpoint.

## Tools

| Tool | Price | Use for |
| --- | --- | --- |
| `glim_twitter_search` | $0.005 | Search tweets with advanced operators |
| `glim_twitter_get` | $0.005 | Tweet with thread context, or user profile, by URL/id/handle |
| `glim_reddit_search` | $0.01 | Search Reddit posts |
| `glim_reddit_get` | $0.015 | Post + comments, subreddit feed, or user activity |
| `glim_web_search` | $0.01 | Semantic web search (Exa) |
| `glim_web_fetch` | $0.002 | Clean page extraction (handles SSR, SPA shells, PDFs) |
| `glim_github_search` | $0.002 | Search GitHub repos, conversations, or code |
| `glim_github_get` | $0.002 | Repo metadata, files, history, PRs, issues |
| `glim_amazon_search` | $0.005 | Search Amazon listings with prices, ratings, ASINs |
| `glim_amazon_get` | $0.01 | Amazon product detail by ASIN |
| `glim_youtube_get` | $0.01 | YouTube subtitles/transcript by video id |

## Usage patterns

- Search tools return compact previews. Follow up with the matching `*_get` tool for full content (`glim_reddit_search` -> `glim_reddit_get`, `glim_twitter_search` -> `glim_twitter_get`).
- Reddit works best with subreddit-scoped queries: `subreddit:python async`.
- Twitter search supports advanced operators (`from:`, `since:`, `min_faves:`, ...). The server exposes a `docs://search-operators` MCP resource with the full reference.
- Large `glim_web_fetch` pages are truncated inline with a `download_full_url` link to the complete extraction.
- Per-tool pricing is also exposed as the `docs://pricing` MCP resource.

## REST API

Every tool is also a plain REST endpoint under `https://glim.sh/api/v1/`, gated by the same x402/MPP payment challenges. Full spec: [glim.sh/openapi.json](https://glim.sh/openapi.json). Use `npx x402-proxy <url>` as a paying curl.

## Links

- [glim.sh](https://glim.sh) - site, sign-in, balance dashboard
- [glim.sh/openapi.json](https://glim.sh/openapi.json) - REST API spec
- [github.com/glim-sh](https://github.com/glim-sh) - registry manifests and docs
