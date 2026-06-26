# Host Memory Governance

This host follows `memory-governor`.

Rules:

- classify memory before choosing a file
- route memory to target classes before resolving concrete paths
- use the local adapter map for host-specific paths
- fall back to local memory files when optional adapters are unavailable

This host does not assume:

- `AGENTS.md`
- OpenClaw workspace layout
- `self-improving`
- `proactivity`

In this host, `memory-governor` is treated as a generic governance core, not an OpenClaw-only package.
