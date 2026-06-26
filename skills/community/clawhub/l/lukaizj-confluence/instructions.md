# Confluence Integration Instructions

Use this skill to manage Confluence pages, spaces, and content via REST API.

## Tools

### confluence_check
Verify connection to Confluence.

### confluence_search
Search pages using CQL (Confluence Query Language).

### confluence_page_get
Get a page by ID.

### confluence_page_create
Create a new page.

### confluence_page_update
Update page content.

### confluence_page_attach
Upload attachment to page.

### confluence_space_list
List all spaces.

## Configuration

Set environment variables:
- CONFLUENCE_URL: Your Confluence base URL
- CONFLUENCE_USER: Your username
- CONFLUENCE_PASS: Your password or API token

## Security

Credentials are used locally only and never exposed to external services.

## Examples

```
Search: text ~ "project"
Get page: confluence_page_get page_id=123456
Create: confluence_page_create space="DAT" title="New Page"
```