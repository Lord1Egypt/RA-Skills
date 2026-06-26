## Listing Discovery and Scoping

- When `adRoots` are configured and the user asks for a specific listing, run
  `kleinanzeigen_list_ads` before publishing, updating, deleting, downloading,
  or extending. Use it to resolve the exact local ad directory, config path,
  title, ID, and active state.
- Prefer scoped operations with `adDirectories` or `adConfigPaths` after
  discovery. Avoid broad selectors like `all` unless the user explicitly wants a
  broad operation.
- For a single listing request such as "publish the sample listing", first list
  with a query, then verify or publish only the matching directory/config path.
- `kleinanzeigen_delete` still requires explicit `adIds`, even when the
  operation is also scoped to a directory or config path.
