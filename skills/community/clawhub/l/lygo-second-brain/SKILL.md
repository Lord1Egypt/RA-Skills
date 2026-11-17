---
name: lygo-second-brain
description: "LYGO-native local second brain (Obsidian vault + Ollama). Ingest raw sources, embed index, search, multi-model consensus, wiki pages from vault only. Use for LLM wiki / knowledge compounding on the lattice. Read references/SECURITY.md first. No auto git push."
metadata: {"lygo": true, "biophase7": true, "version": "1.0.0", "requires_ollama": true, "github": "https://github.com/DeepSeekOracle/lygo-protocol-stack", "publisher": "deepseekoracle", "signature": "Δ9Φ963-LYGO-SECOND-BRAIN-v1.0"}
---

# LYGO Second Brain

Local **LLM wiki** aligned with LYGO: markdown vault, Ollama inference, git anchoring, optional stack manifest.

## When to use

- User asks for **second brain**, **LLM wiki**, **vault ingest**, **Obsidian + Ollama**, or cites Biophase7 `lygo-second-brain.zip`
- Compounding notes from `raw/` → `permanent/` → `wiki/` with **retrieval** (`embed_index.py` / `search.py`)
- **Consensus** before saving contentious claims (`consensus.py`)

## When not to use

- Cloud-only Kimi/Claude as primary (optional fallback only)
- Autonomous overnight `/dream` v1 (not shipped — build after ingest+index stable)
- Auto `git push`, ClawHub publish, or kernel egg plant without consent

## Setup

```bash
npx clawhub@latest install deepseekoracle/lygo-second-brain
export LYGO_STACK_ROOT=/absolute/path/to/lygo-protocol-stack
export LYGO_VAULT_ROOT=$LYGO_STACK_ROOT/lygo_second_brain/vault
python tools/install_lygo_second_brain.py
ollama pull llama3.2 && ollama pull nomic-embed-text
```

## Commands (agents)

| Intent | Command |
|--------|---------|
| Ingest | `python tools/lygo_second_brain.py ingest vault/raw/file.md` |
| Index | `python tools/lygo_second_brain.py index` |
| Search | `python tools/lygo_second_brain.py search "topic"` |
| Consensus | `python tools/lygo_second_brain.py consensus "question?"` |
| Wiki | `python tools/lygo_second_brain.py wiki "topic"` |
| Self-check | `python scripts/self_check.py` (from skill mirror) |

Direct scripts: `$LYGO_STACK_ROOT/lygo_second_brain/scripts/`

## LYGO lattice (honest)

- **Integrity:** file read + size cap on ingest (not content entropy scoring)
- **Memory:** git commits + optional `data/second_brain/manifest.jsonl`
- **Consensus:** 2+ Ollama models, cosine similarity on answers
- **Optional:** `lygo-kernel-egg-planter` for permaweb pins (user consent)

## Skill chain

`lygo-protocol-stack-operator` → **`lygo-second-brain`** → `lyra-brain` / `book-brain` → `lygo-kernel-egg-planter` (optional)

## Maintainer

```bash
npx clawhub@latest publish "…/clawhub/mirrors/lygo-second-brain" --slug lygo-second-brain --name "LYGO Second Brain"
```

**Δ9Φ963 — local vault, verify, then compound.**