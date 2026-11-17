# dahd_open_data

Digital Art History Directory — Open Data Collections.

- Page: https://dahd.hcommons.org/open-data-collections/
- Machine endpoint: `https://dahd.hcommons.org/wp-json/wp/v2/pages?slug=open-data-collections`
- Auth: none
- Rate limit: undocumented; low-volume discovery only.
- Citation: page URL above.

## Actions

- `list_sources` — parse the directory into `{name, url, description}` entries.
- `get_source` — find sources by `name` or `query` substring.
- `refresh_catalog` — re-fetch and parse current page.

## Gotchas

The public page may redirect through HCommons silent login, but WordPress REST JSON is readable without login. Treat DAHD as a source-discovery directory, not as authoritative current documentation for linked APIs; verify each linked source before integration.
