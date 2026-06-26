---
name: Confluence Integration
description: Confluence REST API integration via curl - lightweight solution without Python dependencies. Supports search, page operations, and file attachments.
homepage: https://github.com/lukaizj/confluence-integration-skill
tags:
  - confluence
  - wiki
  - documentation
  - rest-api
  - curl
requires:
  env:
    - CONFLUENCE_URL
    - CONFLUENCE_USER
    - CONFLUENCE_PASS
files:
  - confluence.sh
---

# Confluence Integration

Confluence integration skill for OpenClaw. Manage wiki pages, spaces, and content via REST API using pure curl/shell.

## Capabilities

- Search Confluence pages using CQL
- Get, create, and update pages
- List and view spaces
- Upload attachments to pages
- Create child pages

## Setup

1. Create a Confluence API token or use password
2. Get your Confluence base URL
3. Configure environment variables

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `CONFLUENCE_URL` | Yes | Your Confluence base URL (e.g., https://your-company.atlassian.net) |
| `CONFLUENCE_USER` | Yes | Your Confluence username or email |
| `CONFLUENCE_PASS` | Yes | Your password or API token |

**Security Note**: These credentials are only used locally and never exposed or stored externally.

## Usage Examples

```
Check connection to Confluence

Search for pages containing "kyuubi"

Get page with ID 123456

Create a new page in space DAT with title "Project Notes"

Update page 123456 with new content

Upload attachment to page 123456
```

## Commands

### check
Verify connection to Confluence instance.

### search
Search pages using Confluence Query Language (CQL).
```
text ~ "keyword"
space = "DAT" AND text ~ "spark"
type = page
```

### page get
Get a page by ID. Returns title, content, space, version.

### page create
Create a new page. Options:
- `--space`: Space key (required)
- `--title`: Page title (required)
- `--body`: Page content (required)
- `--parent`: Parent page ID for child pages

### page update
Update page content. Options:
- `--body`: New content
- `--title`: New title
- `--append`: Append to existing content

### page attach
Upload file attachment to a page.

### space list
List all accessible spaces.

## CQL Examples

| Search | Description |
|--------|-------------|
| `text ~ "kyuubi"` | Pages containing "kyuubi" |
| `space = "DAT"` | Pages in DAT space |
| `type = page` | All pages |
| `text ~ "spark" AND space = "DEV"` | Pages about spark in DEV space |