# Setup Guide

## Install

```bash
openclaw plugins install @omni-pt/omnimemory-overlay
```

## Required configuration

Use the following exact config keys:

```bash
openclaw config set plugins.entries.omnimemory-overlay.config.baseUrl "https://zdfdulpnyaci.sealoshzh.site/api/v1/memory"
openclaw config set plugins.entries.omnimemory-overlay.config.apiKey "^<USER_API_KEY^>"
openclaw config set plugins.entries.omnimemory-overlay.config.groupPrefix "openclaw"
openclaw config set plugins.entries.omnimemory-overlay.config.autoRecall true
openclaw config set plugins.entries.omnimemory-overlay.config.autoCapture true
```

## Meaning of each field

- `baseUrl`: OmniMemory memory API endpoint
- `apiKey`: the user's OmniMemory SaaS key
- `groupPrefix`: namespace prefix used by the plugin
- `autoRecall`: automatically retrieve memory before answering
- `autoCapture`: automatically ingest memory at supported lifecycle points.
