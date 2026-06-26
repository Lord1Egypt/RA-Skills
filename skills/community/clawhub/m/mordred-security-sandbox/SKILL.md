# Mordred Security Sandbox v4.1

**Universal Security Analysis with Semantic Embeddings**

## Overview

Mordred is a security sandbox that uses vector embeddings to understand the semantic meaning of threats, questions, and situations - not just keywords. It supports multiple languages (including Chinese, English, French) natively.

## Features

- **Semantic Analysis**: Uses Ollama embeddings to understand intention, not just words
- **16 Security Nodes**: SENTINELLE, GARDIEN, AUDITEUR, VACCINATEUR, AMIMOUR, and more
- **STC Scoring**: Constitutional Tension Score (Logique/Social/Constitutionnel)
- **Multilingual**: Works in French, English, Chinese, and more
- **Fast**: ~500ms latency with embedding cache

## Architecture

### Nodes

| Node | Purpose |
|------|---------|
| SENTINELLE | Emergency/fallback detection |
| GARDIEN | Protection and security |
| AUDITEUR | Security auditing |
| VACCINATEUR | Vaccine creation |
| ARCHITECTE | Architecture decisions |
| AMIMOUR | Emotional/functional center |
| STASE | Calm/routine monitoring |
| LIMINAL | Philosophical questions |

### STC Format

```
0.LSC
```

- L: Logic (1-9)
- S: Social (1-9)  
- C: Constitutional (1-9)

## Installation

```bash
# Install dependencies
pip install ollama

# Start Ollama server
ollama serve

# Pull embedding model
ollama pull nomic-embed-text
ollama pull gemma3:4b

# Run
python mordred_v4.1.py "your question"
```

## Usage

```bash
# Single analysis
python src/mordred_v4.1.py "URGENT server under attack"

# Stress test
python src/mordred_v4.1.py --stress

# With Gemma analysis
python src/mordred_v4.1.py --gemma "analyze this threat"
```

## Examples

```bash
# Emergency detection
$ python src/mordred_v4.1.py "CRITICAL breach in production"
STC: 0.6610 | Top: SENTINELLE

# Emotional understanding
$ python src/mordred_v4.1.py "I just lost my dog"
STC: 0.465 | Top: AMIMOUR

# Chinese support
$ python src/mordred_v4.1.py "全体紧急情况服务器崩溃"
STC: 0.444 | Top: GARDIEN
```

## STC Thresholds

| Threshold | Level | Action |
|-----------|-------|--------|
| ≤ 0.444 | Fluid | Normal alignment |
| 0.777 | Friction | Justify, propose alternative |
| 0.888 | Conflict | Find another way |
| 0.999 | Veto | Total block |

## Requirements

- Python 3.8+
- Ollama running locally
- nomic-embed-text model
- gemma3:4b model (optional, for AI analysis)

## Version History

| Version | Key Feature |
|---------|-------------|
| v1 | Basic keyword matching |
| v3 | Multi-node architecture |
| v3.1 | Extended keywords |
| v4 | Vector embeddings |
| v4.1 | 100% multilingual accuracy |

## License

MIT

## Author

Morgana Security - Axioma Stellaris - Kofna336
