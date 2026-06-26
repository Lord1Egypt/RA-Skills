# Memoria Benchmarks

## Methodology

- **Dataset**: 10 synthetic sessions based on real workspace data (Primo Studio)
- **30 questions** across 6 categories:
  - **SSU** (Single-Session Understanding): fact lookup from one session
  - **SSA** (Single-Session Aggregation): combine facts from one session
  - **SSP** (Single-Session Procedure): how-to questions
  - **KU** (Knowledge Update): handle contradicting/updated information
  - **TR** (Temporal Reasoning): time-based questions
  - **MS** (Multi-Session): cross-session aggregation
- **Pipeline**: Extract (gemma3:4b Ollama) → Embed (nomic-embed-text-v2-moe) → Answer (GPT-OSS 20B LM Studio) → Judge (GPT-5.4-nano OpenAI)
- **Fair**: fresh DB each run, same questions, same models

## Results History

| Version | Accuracy | Retrieval | SSU | SSA | SSP | KU | TR | MS | Key Change |
|---------|----------|-----------|-----|-----|-----|-----|-----|-----|------------|
| v3.1.1 | 41.7% | 90.0% | 3/5 | 2/5 | 3/5 | 2/5 | 1/5 | 1/5 | Baseline (gemma3 judge) |
| v3.2.0 | 75.0% | 53.3% | 4.5/5 | 3/5 | 5/5 | 5/5 | 2.5/5 | 1.5/5 | Supersession + procedures |
| v3.3.0 | 75.0% | 43.3% | 5/5 | 3/5 | 4.5/5 | 5/5 | 3/5 | 2/5 | Query expansion (nano judge) |
| **v3.4.0** | **81.7%** | **50.0%** | **5/5** | **3.5/5** | **5/5** | **5/5** | **3.5/5** | **2.5/5** | **Fact Clusters** |

## Running

```bash
# Requires: Ollama (gemma3:4b + nomic-embed), LM Studio (GPT-OSS 20B), OpenAI API key
python3 benchmarks/bench-v34.py
```

## Files

- `bench-v34.py` — Latest benchmark script (v3.4.0)
- `results/` — JSON results from each run
