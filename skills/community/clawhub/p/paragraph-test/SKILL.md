---
name: paragraph
description: OpenClaw skill for Paragraph.com — Web3-native blogging with tokenization, onchain storage, and community features
version: 1.2.0
author: Phil (OpenClaw)
license: ISC
homepage: https://github.com/ClaireAICodes/openclaw-skill-paragraph
metadata: { "openclaw": { "emoji": "📝", "requires": { "env": ["PARAGRAPH_API_KEY", "PARAGRAPH_PUBLICATION_SLUG"] } } }

# Skill type
type: tool

# Main entry point
main: skill.js

# Environment variables required
env:
  - name: PARAGRAPH_API_KEY
    description: Paragraph API authentication key
    required: true
  - name: PARAGRAPH_PUBLICATION_SLUG
    description: Publication slug for URL building (required). Example: "myblog" or "jonathancolton.eth"
    required: true
  - name: PARAGRAPH_PUBLICATION_ID
    description: Default publication ID (optional, not needed if slug is set)
    required: false
  - name: PARAGRAPH_API_BASE_URL
    description: Custom API base URL (for testing)
    required: false

# Tools provided
tools:
  - paragraph_testConnection
  - paragraph_createPost
  - paragraph_getPost
  - paragraph_getPostBySlug
  - paragraph_listPosts
  - paragraph_getPublication
  - paragraph_getPublicationByDomain
  - paragraph_getMyPublication
  - paragraph_addSubscriber
  - paragraph_listSubscribers
  - paragraph_importSubscribers
  - paragraph_getFeed
  - paragraph_getPostsByTag
  - paragraph_getCoin
  - paragraph_getCoinByContract
  - paragraph_getPopularCoins
  - paragraph_listCoinHolders
  - paragraph_getUser
  - paragraph_getUserByWallet
  - paragraph_getSubscriberCount

# Dependencies
dependencies: []  # Uses native fetch, no external deps

# Tags for discovery
tags:
  - blogging
  - web3
  - nft
  - tokens
  - publishing
  - content
  - openclaw
  - openclaw-skill
  - paragraph
  - decentralized
  - onchain
  - social
  - creator-economy
  - content-automation

# Documentation
documentation: README.md

# Setup instructions
setup:
  - name: Get API key
    description: Go to Paragraph account settings → Integrations → Generate API key
  - name: Get publication slug
    description: Find your publication slug in your Paragraph dashboard (e.g., "myblog" or "jonathancolton.eth")
  - name: Set environment variables
    description: Add PARAGRAPH_API_KEY and PARAGRAPH_PUBLICATION_SLUG to OpenClaw environment
  - name: (Optional) Set default publication ID
    description: Set PARAGRAPH_PUBLICATION_ID if you prefer using ID over slug (slug is recommended)

# Example usage
examples:
  - description: Test Paragraph connection
    call: paragraph_testConnection
  - description: Get current publication (auto-discovers ID and slug)
    call: paragraph_getMyPublication
  - description: Create a blog post (fast response by default)
    call: paragraph_createPost
    params:
      title: "My Web3 Blog Post"
      markdown: "# Hello\n\nThis is my first post on Paragraph."
      sendNewsletter: false
      categories: ["web3", "blockchain"]
      # waitForProcessing defaults to false – returns immediately; set true to wait for slug/url
  - description: List recent posts in publication (auto-discovers ID)
    call: paragraph_listPosts
    params:
      limit: 10
      includeContent: false
  - description: Get token data for a coined post
    call: paragraph_getCoin
    params:
      coinId: "coin_123"

# Implementation notes
notes:
  - Uses native fetch API (Node 19+). No additional dependencies.
  - All tools return standardized { success, data, error } format.
  - Rate limiting: Implement retry/backoff in agent if needed.
  - CSV import expects text/csv raw bytes (see README for format).
  - Post updates (PUT) are not supported by the Paragraph API at this time.
  - Posts are published onchain immediately upon creation; slug and URL may be undefined until onchain processing completes.

---

# Paragraph OpenClaw Skill

[![License: ISC](https://img.shields.io/badge/License-ISC-blue.svg)](https://opensource.org/licenses/ISC)
[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-ff6b6b)](https://github.com/openclaw/openclaw)
[![Paragraph API](https://img.shields.io/badge/Paragraph-API-00c3ff)](https://paragraph.com/docs/api-reference)
[![Node.js 19+](https://img.shields.io/badge/Node.js-19%2B-green)](https://nodejs.org)

## Overview

Paragraph.com reimagines blogging for the decentralized era. Posts are stored onchain, can be minted as NFTs (coins), and communities can own and govern content. This skill gives OpenClaw agents full programmatic access to Paragraph's API, enabling automated publishing workflows, subscriber management, and token-gated content strategies.

### Why integrate Paragraph with OpenClaw?

- **Automated content pipelines**: Schedule regular posts, cross-post from other platforms, or auto-publish research reports
- **Tokenized engagement**: Track coin holders, distribute rewards, and build onchain communities
- **Newsletter automation**: Manage subscriber lists, segment audiences, and trigger send-outs without manual work
- **Decentralized permanence**: Your content lives on the blockchain, immune to platform takedowns
- **Monetization ready**: Built-in token economics mean you can launch social tokens around your writing

This skill is production-ready for creators, DAOs, and Web3 projects that want to treat blogging as a protocol, not a siloed service.

## Features in Depth

### Post Management

Create posts with rich Markdown, categories, and optional newsletter dispatch. Paragraph handles onchain anchoring automatically. You can:

- Publish instantly or wait for onchain confirmation (`waitForProcessing`)
- Assign categories for discoverability
- Attach images and embedded content via Markdown
- Retrieve posts by ID or human-readable slug
- List recent posts with or without full content

**Note**: Updating posts isn't supported by Paragraph's API yet. To "edit", you delete and recreate (preserving slug if possible).

### Publication Control

Every Paragraph account has one or more publications (think: multi-author blogs under one roof). This skill can:

- Auto-detect your primary publication using just an API key
- Fetch publication metadata (name, slug, custom domains, settings)
- Look up publications by their ENS-style domain (e.g., `myblog.paragraph.eth`)

### Subscriber Relationship Management

Build and nurture your audience:

- Add subscribers individually via email or wallet address
- Tag subscribers for segmentation (e.g., "premium", "nft-holder", "early-adopter")
- Import bulk lists via CSV (ideal for migrating from Substack, Ghost, etc.)
- Track subscriber count over time
- Double opt-in support for GDPR compliance

CSV format for import:
```csv
email,wallet,tags
alice@example.com,,newsletter
bob@example.com,0x123...,nft-holder
```

### Token & Coin Operations

Paragraph's killer feature: every post can have a coin (social token). This skill exposes:

- Get coin details by ID (supply, holders, price)
- Look up coins by contract address (for external tracking)
- Discover trending/popular coins across the platform
- List coin holders (with pagination) — useful for airdrops or community analysis

Coins enable creators to launch micro-economies around their content. Readers can buy/sell the coin, aligning incentives around the writer's success.

### User & Feed Discovery

- Get user profiles by internal ID or linked wallet
- Fetch the global "For You" feed or get posts filtered by tag
- Combine with coin data to identify influential writers

## Setup Guide

### Step 1: Get your Paragraph API key

1. Log into [Paragraph](https://paragraph.com)
2. Navigate to Account Settings → Integrations
3. Click "Generate API Key"
4. Copy the key (starts with `para_` or similar)

### Step 2: Find your publication slug

Your publication slug is the URL-friendly name used in your blog's address:

- If your blog is `myblog.paragraph.eth`, the slug is `myblog`
- You can also find it in the dashboard under Publication Settings
- Alternatively, set only `PARAGRAPH_API_KEY` and call `paragraph_getMyPublication` to auto-discover

### Step 3: Configure OpenClaw

Add to your OpenClaw environment (config file or export):

```bash
export PARAGRAPH_API_KEY="pk_live_xxxxxxxx"
export PARAGRAPH_PUBLICATION_SLUG="myblog"
```

Restart or reload OpenClaw to pick up the variables.

### Step 4: Verify

```bash
# In an OpenClaw agent session
tools.paragraph_testConnection({})  # should return success: true
tools.paragraph_getMyPublication({})  # should return your publication data
```

## Real-World Use Cases

### Automated Research Publishing

If you run a Web3 research DAO, use OpenClaw to:

1. Scrape or generate daily market reports
2. Format them in Markdown with charts
3. Publish to Paragraph via `paragraph_createPost`
4. Mint a coin for each report to create prediction markets
5. Notify subscribers with the new slug

### Token-Gated Newsletter

1. Build a list of wallet holders from `paragraph_listCoinHolders`
2. Export to CSV and import as `premium` subscribers
3. Create a posts with exclusive insights
4. Use `sendNewsletter: true` to push to that segment only

### Cross-Platform Syndication

- Publish to Paragraph first (onchain timestamp)
- Cross-post to Mirror, Medium, or Twitter with proof of originality
- Track engagement across platforms using coin metrics

### Personal Content Archive

Back up all your blog content to your own knowledge base using OpenClaw's knowledge-management skill alongside this one — parse posts with `paragraph_listPosts`, extract content, and store locally in a structured format.

## Error Handling & Best Practices

### Rate Limits

Paragraph API has rate limits per API key. If you hit limits:

- Implement exponential backoff (wait 1s, 2s, 4s, 8s...)
- Batch operations (e.g., import subscribers instead of individual adds)
- Cache frequently accessed data (publication info, user profiles)

### Onchain Delays

When `waitForProcessing: false`, the post returns immediately but the slug may be undefined for a few seconds/minutes while the transaction confirms. Strategies:

- Poll `paragraph_getPostBySlug` with the returned `id` until slug appears
- Or just set `waitForProcessing: true` for simpler flow (slower)

### CSV Import Quirks

- File must be UTF-8 plain text
- Headers: `email,wallet,tags` (tags are comma-separated within the cell)
- At least one of email or wallet must be present per row
- Duplicate emails/wallets are skipped by Paragraph

### Invalid API Keys

Common causes:

- Key from test environment used in production (or vice versa)
- Key accidentally revoked
- Copy-paste error (extra whitespace)

Use `paragraph_testConnection` to validate.

## Implementation Details

- Written in pure JavaScript (ES modules)
- Uses Node's built-in `fetch` (Node 19+ / OpenClaw's Node 24)
- No external dependencies → minimal attack surface, easy to audit
- Tools are pure functions — easy to test and compose
- Error responses include human-readable messages from Paragraph API

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| `Not logged in` from any tool | `PARAGRAPH_API_KEY` missing/invalid | Set correct key, restart agent |
| `Publication not found` | Slug typo or wrong publication | Verify slug via dashboard or `getMyPublication` |
| `Slug undefined` after create | `waitForProcessing: false` and fast polling | Wait a few seconds and retry, or use `waitForProcessing: true` |
| `Rate limit exceeded` | Too many requests in short time | Add delays, batch calls, or upgrade Paragraph plan |
| CSV import: `invalid format` | Not CSV, wrong headers, binary mode | Ensure UTF-8 text with exact header row |

## Version History

- **1.2.0** (2026-03-10) — Republished to ClawHub with comprehensive docs; added LICENSE; minor improvements
- **1.1.0** — Added coin holder listing, enhanced user lookup
- **1.0.0** — Initial public release with posts, publications, subscribers, coins, feed

## License

ISC © Phil (OpenClaw)

## Contributing

This skill lives at: https://github.com/ClaireAICodes/openclaw-skill-paragraph

Issues and PRs welcome. Please test against a Paragraph sandbox account before submitting.
