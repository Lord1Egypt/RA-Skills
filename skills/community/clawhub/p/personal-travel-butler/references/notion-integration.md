# Notion Integration Guide

Use this guide when configuring or checking live Notion sync.

## Configuration

Store secrets in environment variables, not in Markdown or JSON files:

```sh
export NOTION_TOKEN="<notion-token>"
export NOTION_PARENT_PAGE_ID="..."
export NOTION_TRAVEL_DATA_SOURCE_ID="..."
export NOTION_VERSION="2026-03-11"
```

`NOTION_VERSION` defaults to `2026-03-11` in the scripts. The Notion API requires a `Notion-Version` header on REST requests.

## Notion Setup

1. Create a Notion integration or personal access token in the Notion developer portal.
2. Create or choose a parent page and enable the connection under that page's integration/connection menu.
3. Copy the parent page link or page ID into `NOTION_PARENT_PAGE_ID`.
4. Run `scripts/notion_setup.py --parent-page-id "$NOTION_PARENT_PAGE_ID"` first to preview the database and properties.
5. Run `scripts/notion_setup.py --parent-page-id "$NOTION_PARENT_PAGE_ID" --apply` to create the `Travel Entries` database and required properties.
6. Copy the printed data source ID into `NOTION_TRAVEL_DATA_SOURCE_ID`.
7. Run `scripts/notion_check.py --dry-run` first, then `scripts/notion_check.py` when credentials are available.

## Safety Rules

- Never write `NOTION_TOKEN` into files under `travel-db/`.
- The parent page ID and data source ID may be stored locally; the token must stay in the environment or a local secrets manager.
- Default sync commands to dry-run and require `--apply` for writes.
- Respect Notion rate limits. If Notion returns 429 or 529, wait for `Retry-After`.
- Keep conflicts manual: do not overwrite Markdown or Notion when both changed since the last sync.

## Official References

- Version header: https://developers.notion.com/reference/versioning
- Retrieve a data source: https://developers.notion.com/reference/retrieve-a-data-source
- Query a data source: https://developers.notion.com/reference/query-a-data-source
- Create a page: https://developers.notion.com/reference/post-page
- Request limits: https://developers.notion.com/reference/request-limits
