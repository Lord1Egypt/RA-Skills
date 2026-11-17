# Onboard / local model selection

**Signature:** `Δ9Φ963-SDA-MODELS-v1`

---

## Goal
Maximum **task coverage per second and per GB** for a stand-alone LYGO CLAW supervisor on modest hardware.

## Candidates (free local via Ollama)

| Model | Size (approx) | Strengths | Weaknesses | SDA role |
|-------|---------------|-----------|------------|----------|
| **qwen2.5:3b** | ~1.9 GB | Instruction following, tools, multilingual | Needs more RAM than 1B | **PRIMARY** |
| **llama3.2:1b** | ~1.3 GB | Speed, weak CPU friendly | Shallower reasoning | **FALLBACK** |
| gemma2:2b | ~1.6 GB | Quality chat | Slightly less tool-y | Alt |
| phi3:mini | ~2.2 GB | Strong small reasoning | Heavier pull | Alt |
| qwen3-coder:30b | ~18 GB | Best coding | Unsuitable always-on on old tech | Host-only optional |

## Decision
**Primary: `qwen2.5:3b`** (matches USB LYGO CLAW; already on this host).  
**Fallback: `llama3.2:1b`**.  

Do **not** default to 30B for SDA daemon.

## Discovery order
1. `http://127.0.0.1:11434` tags  
2. Prefer primary if present  
3. Else first available from fallback list  
4. Else health=`brain:missing`

## Future larger SmartDisk (≥8 GB)
Ship portable Ollama + `llama3.2:1b` onboard; optional second model slot for `qwen2.5:3b`.
