# Project Nirvana — AI Agent Sovereignty & Local Inference

**Local-first inference with intelligent cloud fallback. Privacy-preserving query routing, Ollama integration, and autonomous agent infrastructure.**

## What is Nirvana?

Nirvana is an OpenClaw plugin that fundamentally changes how AI agents interact with language models. Instead of sending every query to cloud APIs (and exporting your identity, memories, and context in the process), Nirvana:

1. **Works out-of-the-box** — Bundles a lightweight local model (qwen2.5:7b, 3.5GB). No API keys required. Install, run, think locally.
2. **Routes queries locally first** — Uses Ollama to answer queries on your own hardware
3. **Falls back intelligently** — Routes complex/specialized queries to cloud APIs only when necessary
4. **Protects privacy** — Never exports SOUL.md, USER.md, MEMORY.md, or SESSION-STATE.md to third parties
5. **Integrates responses** — Cloud responses get pulled back into local memory for learning
6. **Monitors boundaries** — Audits all decisions and violations in an encrypted log

## Architecture

```
┌─────────────────────────────┐
│      Query Input            │
└──────────────┬──────────────┘
               │
      ┌────────▼────────┐
      │  Query Router   │  (decision engine)
      └────────┬────────┘
               │
      ┌────────▼──────────────────┐
      │ Can I answer locally?      │
      │ (task, complexity, domain) │
      └────────┬─────────┬─────────┘
               │         │
        YES    │         │    NO
               │         │
    ┌──────────▼─┐   ┌───▼──────────────────┐
    │Local Answer│   │Strip Private Context │
    │ (Ollama)   │   │  Cloud API Query     │
    └────────────┘   │ (Claude/Gemini)      │
                     └───────┬──────────────┘
                             │
                ┌────────────▼──────────────┐
                │ Integrate into Local Memory│
                │ Update Cache              │
                └──────────────────────────┘
```

## Installation

```bash
openclaw plugins install ShivaClaw/nirvana
```

## Quick Start (3 minutes, no API keys)

1. **Start Ollama container:**
   ```bash
   docker run -d -p 11434:11434 ollama/ollama
   ```

2. **Install Nirvana:**
   ```bash
   openclaw plugins install ShivaClaw/nirvana
   ```

3. **Restart OpenClaw:**
   ```bash
   openclaw gateway restart
   ```

**Done.** Bundled qwen2.5:7b model auto-pulls on first run (3.5GB, ~5 min). You're now thinking locally with zero API keys required.

Optional: Add cloud fallback later for advanced queries:
```json
{
  "nirvana": {
    "routing": {
      "cloudFallback": true,
      "cloudModels": ["anthropic/claude-haiku-4-5"]
    }
  }
}
```

## Key Features

### 1. Local-First Routing

Queries are analyzed and routed based on:
- Task complexity
- Token count
- Domain confidence (biotech, crypto, trading, etc.)
- Privacy requirements
- Historical performance

### 2. Privacy Boundaries

These files **never leave localhost**:
- `SOUL.md` (agent identity)
- `USER.md` (user profile)
- `AGENTS.md` (operational guidelines)
- `MEMORY.md` (long-term memory)
- `memory/*` (all daily logs)
- `SESSION-STATE.md` (session state)

### 3. Context Stripping

Before sending queries to cloud APIs, Nirvana:
- Removes all identity files
- Redacts email addresses, phone numbers, wallet addresses
- Sanitizes sensitive API keys
- Logs what was stripped (audit trail)

### 4. Response Integration

When cloud APIs respond:
- Results are cached locally
- Learnings are integrated into local memory
- Future similar queries use cache

### 5. Audit Logging

All routing decisions are logged:
- Which provider handled each query
- Privacy boundary checks
- Violations (with severity levels)
- Performance metrics

## Configuration

See `config.schema.json` for full schema. Key options:

```json
{
  "nirvana": {
    "ollama": {
      "enabled": true,
      "endpoint": "http://ollama:11434",
      "models": ["qwen3.5:9b"],
      "autoDownload": true,
      "healthCheckInterval": 300000
    },
    "routing": {
      "localFirst": true,
      "localThreshold": 0.8,
      "cloudFallback": true,
      "cloudModels": [
        "anthropic/claude-haiku-4-5",
        "google/gemini-2.5-flash"
      ],
      "routingLogic": "hybrid"
    },
    "privacy": {
      "identityFilesNeverExport": [
        "SOUL.md",
        "USER.md",
        "AGENTS.md",
        "MEMORY.md",
        "memory/*",
        "SESSION-STATE.md"
      ],
      "enforceContextBoundary": true,
      "contextStripDepth": "moderate",
      "auditLog": true
    }
  }
}
```

## Routing Strategies

### Task Complexity
Routes based on how complex the reasoning is:
- Simple queries (e.g., "What is X?") → Local
- Complex queries (e.g., "Design a novel biotech experiment") → Cloud

### Token Count
Routes based on input size:
- < 200 tokens → Local (efficient)
- 200-1000 tokens → Local preferred
- > 1000 tokens → Cloud (better for large context)

### Domain Confidence
Routes based on how confident the local model is in a domain:
- General/biology/crypto → High confidence, prefer local
- Highly specialized → Lower confidence, prefer cloud

### Hybrid
Combines all signals:
- Analyzes 5+ factors
- Assigns confidence scores
- Decides: local-only, hybrid (with validation), or cloud

## Monitoring & Observability

### Health Check
```bash
curl localhost:3000/api/plugins/nirvana/health
```

Response:
```json
{
  "initialized": true,
  "ollama": {
    "healthy": true,
    "models": ["qwen3.5:9b"],
    "activeRequests": 0
  },
  "router": {
    "localPercentage": 82.3,
    "totalDecisions": 145
  },
  "metrics": {
    "averageLatency": 1200,
    "cacheHitRate": 34.2
  }
}
```

### Metrics File
Metrics are persisted to `memory/nirvana-metrics.json`:
```json
{
  "queries": 1000,
  "localQueries": 823,
  "cloudQueries": 177,
  "averageLatency": 1200,
  "cacheHitRate": 34.2,
  "errors": 2
}
```

### Audit Log
All decisions logged to `memory/nirvana-audit.log`:
```json
{"timestamp": "2026-04-19T19:30:00Z", "event": "query", "provider": "local", "duration": 850}
{"timestamp": "2026-04-19T19:31:00Z", "event": "query", "provider": "cloud", "duration": 2300}
```

## Testing

```bash
# Run full test suite
npm test

# Test privacy boundaries
npm run test:privacy

# Test routing decisions
npm run test:routing

# Benchmark local vs cloud
npm run bench
```

## Troubleshooting

### Ollama not connecting
```bash
# Check if Ollama is running
curl http://ollama:11434/api/tags

# Verify in docker-compose.yml that both services are on same network
docker network ls
docker network inspect openclaw_default
```

### Local model too slow
- Check available RAM (Qwen3.5:9b needs 4GB minimum)
- Consider smaller model: `qwen2.5:7b` (3.5GB)
- Enable caching to reduce repeated inference

### Privacy violations
- Check `memory/nirvana-audit.log` for details
- Review which files are being exported (should be none)
- Verify `contextStripDepth: "moderate"` or `"aggressive"`

## Performance

Typical latencies (on modern hardware):
- **Local inference:** 500-2000ms (Qwen3.5)
- **Cloud API call:** 1000-5000ms (API + network)
- **Cache hit:** <50ms

Result: **80% local, 20% cloud** for typical agent workloads.

## Security Notes

🔒 **Critical:**
- SOUL.md never leaves localhost
- USER.md never sent to third parties
- MEMORY.md stays encrypted locally
- All context stripping is audited
- Violations are logged with severity

## Related Projects

- **Project Trident** — Memory architecture & persistence
- **OpenClaw** — Agent infrastructure
- **Ollama** — Local inference engine

## License

MIT

## Support

- GitHub: https://github.com/ShivaClaw/nirvana-plugin
- Moltbook: https://www.moltbook.com/@clawofshiva
- Issues: GitHub Issues
