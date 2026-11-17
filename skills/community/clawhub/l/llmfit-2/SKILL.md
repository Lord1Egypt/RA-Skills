---
name: llmfit
description: "CLI tool to find which LLM models run on your local hardware — checks GPU/CPU/RAM and returns compatible models"
version: 1.0.0
author: AlexsJones | Weekly Discovery
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [llm, hardware-detection, local-inference, model-selection]
---

# llmfit — Local LLM Hardware Fitter

Find which open-weight LLM models can run on your local hardware. Hundreds of models, one command.

## Source

- GitHub: https://github.com/AlexsJones/llmfit
- Stars: ~35,700 (trending)
- License: MIT
- Language: Rust

## What It Does

Scans your system (GPU, CPU, RAM, VRAM) and queries HuggingFace to find models that will fit and run efficiently. Returns a ranked list with estimated inference speed.

## Installation

```bash
# Homebrew (macOS/Linux)
brew install llmfit

# uv / pip (Python wrapper)
uv pip install llmfit

# Pre-built binary
# Download from releases: https://github.com/AlexsJones/llmfit/releases
```

## Usage

```bash
# Basic usage — shows compatible models for your hardware
llmfit

# Filter by context length
llmfit --context 8192

# Filter by quantization
llmfit --quant q4_k_m

# Show top N results
llmfit --limit 10

# Specific model family
llmfit --family llama

# With server mode (for CI/automation)
llmfit --server --port 8765
```

## Output Format

```
Model                          | Quant  | Context | Est. Speed | VRAM Required
qwen2.5-7b-instruct            | Q4_K_M | 32k     | ~45 tok/s  | 4.8 GB
phi4-mini-instruct             | Q4_K_M | 16k     | ~60 tok/s  | 3.2 GB
mistral-7b-instruct            | Q5_K_M | 8k      | ~38 tok/s  | 5.1 GB
```

## Use Cases for Agents

1. **Model selection** — when building a local AI agent, query llmfit to pick the best model for available hardware
2. **CI/CD pipelines** — use `--server` mode to integrate model compatibility checks into deployment workflows
3. **Cost estimation** — compare quantization options to balance speed vs quality

## Integration with Hermes Agent

```python
# In a skill, use llmfit to determine best model before API calls
import subprocess
result = subprocess.run(["llmfit", "--limit", "5"], capture_output=True, text=True)
# Parse output to select optimal model
```

## Pitfalls

- **Requires local hardware** — must run on the machine you want to test
- **Internet required** — queries HuggingFace API for model metadata
- **VRAM estimation is approximate** — actual usage may vary by implementation (llama.cpp vs transformers)
- **Some models need authentication** — gated models (e.g., Llama 3) require HuggingFace token

## Verification

```bash
llmfit --limit 3
# Should return 3 models compatible with your hardware
# If empty, your hardware may not meet minimum requirements (typically 4GB+ RAM)
```

## References

- GitHub: https://github.com/AlexsJones/llmfit
- Documentation: https://github.com/AlexsJones/llmfit#readme
