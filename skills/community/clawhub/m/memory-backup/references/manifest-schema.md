# Manifest schema

Write `manifest.json` into the root of each archive.

Recommended shape:

```json
{
  "createdAt": "2026-04-23T12:00:00Z",
  "workspace": "/path/to/workspace",
  "configInspected": [
    "/home/user/.openclaw/openclaw.json"
  ],
  "detectedSystems": {
    "coreMemory": { "enabled": true, "present": true },
    "dreaming": { "enabled": true, "present": true },
    "memoryWiki": { "enabled": true, "present": true },
    "activeMemory": { "enabled": true, "present": false }
  },
  "approvedSystems": ["coreMemory", "dreaming", "memoryWiki"],
  "includedPaths": [
    {
      "path": "MEMORY.md",
      "kind": "file",
      "reason": "long-term memory"
    }
  ],
  "excludedPaths": [
    {
      "path": "memory/.dreams/session-corpus",
      "reason": "transcript-derived corpus excluded by default"
    }
  ],
  "missingPaths": [
    {
      "path": "memory/dreaming/rem",
      "reason": "enabled feature path not present on disk"
    }
  ],
  "notes": [
    "Config files were inspected for discovery only and were not included in the archive."
  ]
}
```

Rules:
- keep paths relative to the workspace when practical
- use absolute paths for external locations such as wiki vaults outside the workspace
- do not include API keys, tokens, wallet addresses, or raw config secrets
- state why ambiguous paths were excluded
