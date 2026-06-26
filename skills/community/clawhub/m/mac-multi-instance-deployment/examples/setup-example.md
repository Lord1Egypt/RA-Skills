# Setup Example

Use a generic Mac instance layout like this:

- `main` for shared routing and indexes
- `workbench` for active drafting and testing
- `publish` for release-ready output
- `archive` for read-only snapshots
- `private` for local-only state

Example env values:

```bash
OPENCLAW_WORKSPACE_MAIN=/Users/<your-user>/openclaw/main
OPENCLAW_WORKSPACE_WORKBENCH=/Users/<your-user>/openclaw/workbench
OPENCLAW_WORKSPACE_PUBLISH=/Users/<your-user>/openclaw/publish
OPENCLAW_WORKSPACE_ARCHIVE=/Users/<your-user>/openclaw/archive
OPENCLAW_WORKSPACE_PRIVATE=/Users/<your-user>/openclaw/private
```

After setting the paths, update `references/instances.md` so the names and
roles match the same generic layout.
