# Offline Safety

This offline skill is intentionally narrow.

It may:

- query the bundled airport-lounge snapshot through local MCP
- summarize or compare any returned lounge records, across all covered lounge programs/sources
- read bundled catalog metadata and filter lists

It must not:

- call remote MCP endpoints
- fetch network resources
- ask for secrets
- trigger deploys or data rebuilds
- claim that the bundled snapshot is live data

If a request needs a lounge missing from the bundled snapshot or fresher data than the bundle provides, say that the offline bundle lacks that coverage or is stale rather than guessing.
