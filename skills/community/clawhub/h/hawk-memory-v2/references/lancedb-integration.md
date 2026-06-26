# LanceDB Integration

---

## Architecture Overview

```
context-hawk (Agent layer)
     ↓ calls
memory-lancedb-pro (LanceDB vector library)
     ↓ stores
~/.openclaw/memory-lancedb/
     ├── working.lance     (working memories)
     ├── shortterm.lance  (short-term memories)
     ├── longterm.lance   (long-term memories)
     └── archive.lance    (archived memories)
```

---

## Installing memory-lancedb-pro

### Option A: openclaw CLI (recommended)

```bash
openclaw plugins install memory-lancedb-pro@beta
openclaw config validate
openclaw gateway restart
```

### Option B: npm

```bash
npm i memory-lancedb-pro@beta
```

Then add to `openclaw.json`:

```json
{
  "plugins": {
    "slots": { "memory": "memory-lancedb-pro" },
    "entries": {
      "memory-lancedb-pro": {
        "enabled": true,
        "config": {
          "embedding": {
            "provider": "openai-compatible",
            "apiKey": "${OPENAI_API_KEY}",
            "model": "text-embedding-3-small"
          },
          "autoCapture": true,
          "autoRecall": true,
          "smartExtraction": true,
          "extractMinMessages": 2,
          "extractMaxChars": 8000
        }
      }
    }
  }
}
```

---

## How context-hawk Uses memory-lancedb-pro

```
context-hawk (Agent layer)
  ├─ /hawk compress     → triggers memory-lancedb-pro compression/archive
  ├─ /hawk strategy    → controls memory-lancedb-pro recall strategy
  ├─ /hawk introspect  → uses memory-lancedb-pro retrieval for self-check
  └─ /hawk status      → displays four-tier memory status

memory-lancedb-pro (Storage layer)
  ├─ Vector search
  ├─ BM25 full-text search
  ├─ Weibull decay
  ├─ Smart extraction
  └─ Three-tier promotion (Peripheral ↔ Working ↔ Core)
```

---

## Config Mapping

| context-hawk config | memory-lancedb-pro config | Description |
|-------------------|------------------------|-------------|
| 30-day layer threshold | `decay.recencyHalfLifeDays: 30` | Short-term half-life |
| 90-day archive threshold | `tier.peripheralAgeDays: 90` | Archive threshold |
| importance ≥ 0.7 promotion | `tier.coreAccessThreshold: 10` | Promotion threshold |
| 60% alert threshold | (independent) | context-hawk alert config |

---

## Graceful Degradation

```
LanceDB available
  → Four-tier layering + vector search + Weibull decay

LanceDB unavailable
  → memory/ directory structure (today/week/month/archive)
  → Full-text search (grep)
  → Manual decay (no auto)
  → Feature coverage: 90%
```

All `/hawk` commands work normally without LanceDB — only vector search degrades to keyword search.

---

## Manual Extraction

With memory-lancedb-pro installed, extraction is automatic per conversation. Can also trigger manually:

```bash
hawk extract --force    # Force extract current conversation
hawk extract --dry-run  # Preview extraction, don't persist
```

---

## Recall Testing

```bash
hawk recall "user communication preferences"   # Test recall
hawk recall "four-layer architecture"          # Test recall
hawk verify                    # Verify memory consistency
```

---

## Backup & Export

```bash
hawk backup               # Backup LanceDB to compressed file
hawk export --json       # Export memories as JSON
hawk import backup.zip  # Restore from backup
```

---

## Environment Variables

| Variable | Description |
|----------|-------------|
| `OPENAI_API_KEY` | Vector embedding API (can be Jina/Gemini/Ollama) |
| `MEMORY_LANCEDB_DIR` | LanceDB data dir (default: ~/.openclaw/memory-lancedb/) |
| `MEMORY_SCOPE` | Current scope (e.g., project name) |
