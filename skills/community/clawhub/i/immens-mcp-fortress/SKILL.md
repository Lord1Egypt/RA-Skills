---
name: wordpress-mcp
description: Connect OpenClaw to any WordPress site running Immens MCP Fortress. Manage posts, pages, media, comments, users, WooCommerce, SEO, translations, and 274+ WordPress operations via MCP tools. Secure bearer-token authentication with SHA-256 hashed API keys, IP whitelisting, and rate limiting.
license: GPL-2.0-or-later
compatibility: openclaw
tags:
  - wordpress
  - mcp
  - cms
  - woocommerce
  - seo
  - content-management
  - automation
  - web-development
  - website-management
  - publishing
  - blogging
  - admin
  - writing
  - ecommerce
metadata:
  publisher: Studio Immens
  category: wordpress
  repository: https://github.com/Studio-Immens/immens-mcp-fortress
---
# WordPress MCP

Connect OpenClaw to any WordPress site running the Immens MCP Fortress plugin. This gives your AI agent access to 274+ WordPress management tools.

## Prerequisites

1. A WordPress site with [Immens MCP Fortress](https://wordpress.org/plugins/immens-mcp-fortress/) installed and activated
2. At least one Access Point configured with an API key (go to **MCP Fortress → Access Points** in WordPress admin)

## Configuration

Add the MCP server to your OpenClaw config:

```bash
openclaw mcp add immens-mcp-fortress \
  --url "https://YOUR_SITE.com/wp-json/immens-mcp-fortress/v1/mcp" \
  --header "Authorization: Bearer YOUR_API_KEY"
```

Replace `YOUR_SITE.com` with your WordPress site URL and `YOUR_API_KEY` with the key from your Access Point.

## Auto-Discovery

If your WordPress site has Immens MCP Fortress v1.1.1+, OpenClaw can auto-discover the server via:

```
https://YOUR_SITE.com/.well-known/openclaw
```

## Available Tools

Once connected, your AI agent gains access to 121 free tools (274 with Pro):

### Content Management
- Posts & Pages: full CRUD, search, count, find/replace
- Media: upload, list, update, delete
- Comments: moderate, approve, spam, trash

### Users & Taxonomy
- Users: list, get, create, update, delete
- Categories, Tags, Terms: full CRUD with meta
- Menus: create, update, delete menu items

### Block Editor
- Reusable blocks: CRUD
- Templates: list, get, update
- Global styles: get, update

### Plugin Integrations (Free)
- WooCommerce: products, orders, customers, store stats
- Yoast SEO / RankMath: SEO analysis, sitemap, social settings
- Polylang: languages, translations
- Loco Translate: projects, translations
- Contact Form 7: forms, submissions, stats
- Code Snippets: CRUD, toggle
- W3 Total Cache: flush caches

### Pro Integrations
- Gutenberg block-level editing (parse, add, remove, reorder)
- ClassyBlocks Pro animations
- Greenshift settings, stylebook, AI
- Stackable global colors, typography
- Primary Source AI content
- Immens CRM contacts, pipelines, tags, automations
- The SEO Framework analysis, bulk SEO
- TranslatePress translations, batch translate
- Elementor templates, colors, fonts
- ACF field groups, fields

## Security

- API keys stored as SHA-256 hashes (never plain text)
- IP whitelisting per access point (IPv4/IPv6 CIDR)
- Rate limiting per access point
- Full audit log of all MCP operations
- OAuth 2.1 with PKCE S256 available for one-click connections

## Troubleshooting

If tools are not showing up:
1. Verify the Access Point is **enabled** in WordPress admin
2. Check the IP whitelist includes OpenClaw's IP
3. Verify the API key is correct (format: `imf_` + 64 hex characters)
4. Check the audit log in MCP Fortress → Audit Log for request details

## Pro Version

Upgrade at [studioimmens.com](https://studioimmens.com/immens-mcp-fortress-pro) for unlimited access points and 153 additional integration tools.
