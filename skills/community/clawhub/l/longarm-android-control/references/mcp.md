# longarm MCP Reference

The longarm MCP server exposes JSON-RPC 2.0 over the app's configured MCP listen address and port. Use it when an agent or MCP-compatible client should call longarm tools directly instead of issuing HTTP requests.

## Methods

- `initialize` returns protocol capabilities and server info.
- `ping` returns an empty result.
- `tools/list` returns available tools.
- `tools/call` calls one tool with `name` and `arguments`.

Plus-only tools are listed only when the Android device has an active Plus subscription. Calling an unavailable tool returns an MCP tool error.

## Free Tools

| Tool | Purpose |
| --- | --- |
| `screen_info` | Return screen width, height, and density. |
| `tap` | Tap a coordinate. |
| `long_press` | Long-press a coordinate. |
| `open_app` | Open an installed Android app by package name. |
| `open_intent` | Open a custom Android activity intent. |
| `batch_list` | List saved longarm batch tasks. |
| `batch_get` | Get one saved batch task by id. |
| `batch_save` | Create or update a saved batch task. |
| `batch_delete` | Delete a saved batch task by id. |
| `batch_run` | Run a saved batch task by id. |
| `batch_run_inline` | Run an unsaved batch task. |
| `batch_status` | Return current batch runner status. |
| `batch_history_list` | List recent batch run history entries. |
| `batch_history_get` | Get one batch run history entry. |
| `batch_history_export` | Export screenshots from one batch run as a zip file. |
| `batch_history_delete` | Delete one batch run history entry and screenshots. |

## Plus Tools

| Tool | Purpose |
| --- | --- |
| `swipe` | Swipe from one coordinate to another. |
| `pinch` | Pinch in or out around a coordinate. |
| `two_finger_swipe` | Swipe with two fingers held a fixed distance apart. |
| `rotate` | Rotate two fingers around a center point. |

Use `tools/list` after connecting; it is the source of truth for schemas and current availability.
