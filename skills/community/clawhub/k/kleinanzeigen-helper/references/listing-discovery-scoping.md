## Listing Discovery and Scoping

- When `adRoots` are configured and the user asks for a specific listing, run
  `kleinanzeigen_list_ads` before publishing, updating, deleting, downloading,
  or extending. Use its returned `adDirectory` or `adPath` handle with the
  title, ID, and active state to scope the next tool call.
- Prefer scoped operations with `adDirectories` or `adConfigPaths` after
  discovery. Avoid broad selectors like `all` unless the user explicitly wants a
  broad operation.
- For a single listing request such as "publish the sample listing", first list
  with a query, then verify or publish only the matching relative handle.
- `kleinanzeigen_delete` still requires explicit `adIds`, even when the
  operation is also scoped to a relative ad handle.
