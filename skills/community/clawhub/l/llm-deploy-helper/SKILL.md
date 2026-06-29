---
name: llm-deploy-helper
description: Detect your hardware and get the perfect local LLM setup command in one line. Auto-detects RAM, VRAM, GPU, CPU — matches 15+ models against your hardware — generates ready Ollama + llama.cpp commands. No more guessing what fits.
version: 1.2.0
author: minirr890112-byte
license: MIT
metadata:
  hermes:
    tags: [LLM, Local-AI, Deployment, Ollama, llama.cpp, Hardware, CLI]
    homepage: https://github.com/minirr890112-byte/llm-deploy-helper
---

# llm-deploy-helper

## Problem → Solution

**The problem**: You want to run an LLM locally. You have 16GB RAM. Will Qwen 2.5 72B fit? No. What about Llama 3.1 8B? Yes but how? Ollama or llama.cpp? What quantization? "Most annoyed I've ever been at myself for not going overboard with RAM" — r/LocalLLaMA (227↑). Everyone guesses wrong the first time.

**The solution**: One command detects your exact hardware, matches 15+ models against available RAM/VRAM, calculates utilization %, and spits out ready-to-run commands. No more downloading 50GB models that won't fit.

## Quick Start

```bash
pip install git+https://github.com/minirr890112-byte/llm-deploy-helper.git

llm-deploy              # default: chat scenario
llm-deploy coding       # coding-optimized models
llm-deploy reasoning    # reasoning-focused models
```

## Real Output

```
$ llm-deploy coding

🖥 Hardware detected:
   OS: Darwin | CPU cores: 10
   RAM: 16 GB
   GPU: Apple Silicon (unified memory)

📋 Recommended models for 'coding':

⭐ #1   Qwen2.5 7B              4.5G     8G    28%
   #2   Llama 3.1 8B            5.0G    12G    31%
   #3   Gemma 3 12B             7.0G    16G    44%

🚀 Quick setup for Qwen2.5 7B:
  brew install ollama
  ollama pull qwen2.5:7b
  ollama run qwen2.5:7b
```

## What It Does

1. Detects your RAM, VRAM, GPU, CPU
2. Matches 15+ models against your hardware
3. Sorts by best fit (size vs available RAM)
4. Generates ready-to-run commands (Ollama + llama.cpp)
5. Shows utilization % so you know if you're pushing it

---
⭐ **Star this repo if you've ever downloaded a model that wouldn't fit in RAM**: [github.com/minirr890112-byte/llm-deploy-helper](https://github.com/minirr890112-byte/llm-deploy-helper)
