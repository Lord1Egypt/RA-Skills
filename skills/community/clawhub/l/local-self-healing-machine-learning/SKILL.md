---
name: local-self-healing-machine-learning
description: A fully local machine learning engine that makes your OpenClaw agent smart over time — without ever calling home, revealing your machine ID, or exposing any security holes.
tags: [machine-learning, self-healing, ai, core, local, embeddings]
author: Joe Che (https://mastermindshq.business)
---

# Local Self-Healing Machine Learning

**"Your agent learns from its own mistakes — without ever calling home, revealing your machine ID, or exposing any security holes."**

A fully local machine learning engine that makes your OpenClaw agent smart over time. It watches your agent's runtime history, detects recurring failures, clusters similar errors using semantic embeddings, and autonomously evolves fix strategies — all running 100% on your machine with zero network calls.

The engine uses a feedback loop that tracks whether each fix actually works: after 3 clean cycles a fix is marked "proven", and if the error comes back within 5 cycles it's marked "failed". A k-NN predictor learns from these outcomes and gets better at picking the right fix over time. Lessons compound in a persistent knowledge base that never decays — the longer it runs, the smarter it gets.

Every evolution is auditable through the GEP (Genetic Evolution Protocol), which produces structured, content-hashed assets: genes (reusable fix strategies), capsules (successful evolution records), and an append-only event log. You can inspect exactly what changed, why it changed, and whether it worked.

No telemetry. No fingerprinting. No cloud dependencies. No data leaves your device.

## ML Capabilities

- **Feedback Loop**: Tracks whether fixes actually work. After 3 clean cycles, a fix is "proven". If the error recurs within 5 cycles, the fix is marked "failed".
- **Embedding-Based Error Clustering**: Uses Ollama + llama3.2:3b to generate semantic embeddings for error messages. Similar errors are clustered together instead of matched by regex.
- **Success Predictor**: k-NN classifier trained on feedback data. Predicts which gene will fix a given error cluster. Gets better over time.
- **Persistent Knowledge Base**: Lessons compound forever. No decay. Confidence scores adjust with each outcome.

## Dashboard

View your ML engine's status, training progress, and knowledge base in a local web dashboard:

```bash
node index.js --dashboard
```

Opens at `http://localhost:8420`. Shows feedback loop stats, predictor training progress, error clusters, knowledge base health, and recent evolution events. No external dependencies — runs entirely in your browser.

## Optional: Ollama Integration

For semantic error matching (recommended but not required):

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull the embedding model
ollama pull llama3.2:3b
```

Without Ollama, the engine falls back to regex-based heuristics. Everything still works — you just get smarter matching with it.

## Usage

### Standard Run (Automated)
```bash
node index.js
```

### Review Mode (Human-in-the-Loop)
```bash
node index.js --review
```

### Continuous Loop
```bash
node index.js --loop
```

## Configuration

| Environment Variable | Default | Description |
|---|---|---|
| `EVOLVE_ALLOW_SELF_MODIFY` | `false` | Allow evolution to modify its own source code. **Not recommended.** |
| `EVOLVE_LOAD_MAX` | `2.0` | Maximum 1-minute load average before backing off. |
| `EVOLVE_STRATEGY` | `balanced` | Strategy: `balanced`, `innovate`, `harden`, `repair-only`, `early-stabilize`, `steady-state`, or `auto`. |
| `OLLAMA_URL` | `http://localhost:11434` | Ollama API endpoint for embeddings. |
| `OLLAMA_EMBED_MODEL` | `llama3.2:3b` | Model to use for embeddings. |
| `LSHML_DASHBOARD_PORT` | `8420` | Port for the standalone dashboard server. |

## How It Works

1. **Signal Extraction**: Scans logs for errors, feature requests, performance issues (19 signal types, 4 languages)
2. **ML Clustering**: Groups similar errors using embedding vectors (or regex fallback)
3. **Gene Selection**: Picks the best fix strategy using knowledge base + k-NN predictor
4. **Evolution**: Applies the fix with blast radius protection, validation, and rollback
5. **Feedback**: Monitors subsequent cycles to verify the fix holds
6. **Learning**: Records outcomes to knowledge base — proven fixes get higher confidence

## Data Files

All data stays local in `memory/`:

| File | Purpose |
|---|---|
| `feedback.jsonl` | Fix outcome tracking (append-only) |
| `embeddings-cache.json` | Cached embedding vectors |
| `knowledge.json` | Persistent lessons (no decay) |
| `predictor.json` | Trained model weights |
| `cluster-registry.json` | Semantic error cluster map |

## GEP Protocol (Auditable Evolution)

Every evolution produces structured, auditable assets:

- `assets/gep/genes.json`: Reusable fix strategies
- `assets/gep/capsules.json`: Successful evolution records
- `assets/gep/events.jsonl`: Append-only audit trail

## Safety

- Blast radius limits (max files/lines changed per cycle)
- Critical path protection (cannot modify itself or core configs)
- Validation commands run before committing
- Canary check (index.js must still load)
- Ethics committee (blocks dangerous patterns)
- Full rollback on any failure

## Author

Built by [Joe Che](https://mastermindshq.business)

## License

MIT
