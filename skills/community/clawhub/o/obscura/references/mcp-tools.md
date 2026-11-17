# obscura MCP tools (0.2.6)

`obscura mcp` speaks MCP 2024-11-05 over stdio; `obscura mcp --http` serves POST `/mcp`.
Server name `obscura-mcp`, version follows the binary. 38 tools:

| Tool | Parameters |
|---|---|
| `browser_navigate` | `url`, `waitUntil` |
| `browser_snapshot` | `max_chars` |
| `browser_click` | `ref`, `selector` |
| `browser_fill` | `ref`, `selector`, `value` |
| `browser_type` | `ref`, `selector`, `text` |
| `browser_press_key` | `key`, `selector` |
| `browser_select_option` | `selector`, `value` |
| `browser_evaluate` | `expression`, `timeoutMs` |
| `browser_wait_for_function` | `function`, `pollIntervalMs`, `timeout` |
| `browser_wait_for` | `selector`, `timeout` |
| `browser_network_requests` | — |
| `browser_console_messages` | — |
| `browser_close` | — |
| `browser_markdown` | `max_chars` |
| `browser_links` | `internal_only`, `limit` |
| `browser_interactive_elements` | `limit` |
| `browser_back` | — |
| `browser_forward` | — |
| `browser_reload` | — |
| `browser_get_cookies` | `domain` |
| `browser_set_cookie` | `domain`, `http_only`, `name`, `path`, `secure`, `value` |
| `browser_clear_cookies` | — |
| `browser_wait_for_text` | `text`, `timeout` |
| `browser_detect_forms` | — |
| `browser_fill_form` | `fields`, `submit_ref`, `submit_selector` |
| `browser_scroll` | `amount`, `direction`, `ref`, `selector` |
| `browser_get_attribute` | `attribute`, `ref`, `selector` |
| `browser_count` | `selector` |
| `browser_extract` | `schema` |
| `browser_tab_new` | `url` |
| `browser_tab_list` | — |
| `browser_tab_switch` | `tab_id` |
| `browser_tab_close` | `tab_id` |
| `browser_search` | `case_sensitive`, `context_chars`, `limit`, `query` |
| `browser_storage_state` | — |
| `browser_set_storage_state` | `state` |
| `browser_screenshot` | `height`, `width` |
| `browser_pdf` | `landscape`, `margin_bottom`, `margin_left`, `margin_right`, `margin_top`, `paper_height`, `paper_width`, `print_background`, `scale` |

All tools act on the active tab; `browser_tab_*` manage tabs. Element-first flows:
`browser_snapshot` or `browser_interactive_elements` → `ref` → click/fill.

Localhost and RFC1918 targets require `obscura mcp --allow-private-network`.
HTTP transport: bind `--host` deliberately and set `OBSCURA_MCP_TOKEN` before exposing it.
