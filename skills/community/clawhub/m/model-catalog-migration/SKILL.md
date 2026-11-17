---
name: "openclaw-model-catalog-migration"
description: "Add, remove, or rename OpenClaw model IDs by reconciling provider catalogs, policy, fallbacks, and per-agent references."
---

# OpenClaw model catalog migration

## Use when
Adding, removing, or renaming provider model IDs in OpenClaw configuration.

## Procedure
1. Read the current config and schema with supported OpenClaw config tools. Identify the actual per-agent collection key from the returned structure; do not assume `list` or `entries`.
2. Fetch both the provider's current catalog and OpenClaw's effective model list. Compare exact IDs after accounting for OpenClaw's provider prefix.
3. Audit these references in one pass:
   - configured model registry
   - model policy allowlist
   - default primary and fallbacks
   - every per-agent primary and fallback
   - aliases and runtime metadata on affected entries
4. Classify each affected ID as exact catalog match, stale reference, policy-only entry, or required replacement. Treat suffix variants such as `:free` as distinct IDs.
5. Before removing an ID, choose an available replacement for every primary or fallback reference. Preserve fallback order and unrelated metadata.
6. Apply one atomic patch through the authorized config-write path. If no writer is available, provide the exact proposed diff for the human to apply. Do not restart merely because the file changed; first observe the supported reload behavior.
7. Verify:
   - config parsing and schema validation succeed
   - rereading the actual per-agent collection shows each replacement
   - the added ID appears in registry and policy where required
   - the removed ID appears nowhere in registry, policy, defaults, or agents
   - the effective model list reports expected availability
   - reload logs show no config error

## Pitfalls
- A provider catalog match for the unsuffixed ID does not validate a suffixed ID.
- Checking only the configured registry misses stale policy and per-agent references.
- A `null` verification result may mean the query used the wrong collection key, not that the agent entry vanished.
- A primary must be replaced before its registry or policy entry is removed.
