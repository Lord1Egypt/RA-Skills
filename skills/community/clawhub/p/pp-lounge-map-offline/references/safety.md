# Offline Safety

This offline skill is intentionally narrow.

It may:

- query the bundled lounge snapshot through local MCP
- summarize or compare returned lounge records
- read bundled catalog metadata and filter lists

It must not:

- call remote MCP endpoints
- fetch network resources
- ask for secrets
- trigger deploys or data rebuilds
- claim that the bundled snapshot is live data

If a request needs fresher data than the bundled snapshot provides, say that the offline bundle is stale rather than guessing.
