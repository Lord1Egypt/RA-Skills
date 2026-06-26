---
name: harmonia
description: Check PyTorch, Transformers, and CUDA compatibility. Detect GPU, driver mismatches, and version conflicts in ML environments. Use when the user sets up ML/AI tools, installs torch or transformers, hits dependency errors, or asks about compatible versions.
version: 1.0.0
author: ahmed-eladl
tags: ["ml", "pytorch", "cuda", "gpu", "transformers", "compatibility", "python", "diagnostics"]
metadata:
  openclaw:
    emoji: "🎵"
    homepage: https://github.com/ahmed-eladl/harmonia
    requires:
      bins:
        - pip
        - python3
    install:
      - id: pip
        kind: uv
        package: harmonia-ml
        bins: [harmonia]
        label: "Install harmonia (pip install harmonia-ml)"
---

# Harmonia — ML Dependency Harmony

Harmonia detects GPU, CUDA, driver, OS, Python, and installed ML packages — then reports exactly what's compatible with what. Zero dependencies, works offline.

## When To Use This Skill

- User asks to **set up a PyTorch or ML environment**
- User hits a **dependency error** with torch, transformers, torchaudio, torchvision, accelerate, or CUDA
- User asks **"what version of X works with Y"** for ML packages
- User asks to **check their GPU, CUDA, or driver setup**
- User says something like "my torch is broken", "CUDA error", "version mismatch", "which torch for my Python"
- User is installing **local models via Ollama** or setting up training

## Instructions

### Step 1: Install harmonia (if not already installed)

```bash
pip install harmonia-ml
```

### Step 2: Choose the right command based on the user's need

**Full environment scan** — use when diagnosing issues:
```bash
harmonia check
```
This scans OS, Python, GPU, CUDA driver chain, torch, transformers, and known conflicts all at once.

**Deep system diagnostics** — use when the user asks specifically about GPU, CUDA, or driver:
```bash
harmonia doctor
```
Shows GPU model, VRAM, driver version, CUDA (nvidia-smi vs nvcc vs torch), glibc, virtualenv status.

**Suggest compatible versions** — use when the user wants to know what works together:
```bash
# What works with a specific torch version?
harmonia suggest torch==2.5.1

# What works with a specific transformers version?
harmonia suggest transformers==4.44.2

# Best stack for specific Python + CUDA?
harmonia suggest transformers --python 3.11 --cuda 12.1
```

**Show compatibility matrix** — use when the user wants to see all options:
```bash
harmonia matrix pytorch
harmonia matrix transformers
```

**List known conflicts** — use when the user hit a specific error:
```bash
harmonia conflicts
```
Shows known bug patterns with exact error messages and fixes.

**JSON output** — use for programmatic processing:
```bash
harmonia check --json
```

### Step 3: Interpret the output for the user

- Lines starting with `❌` are **errors** that must be fixed
- Lines starting with `⚠️` are **warnings** worth noting
- Lines starting with `✅` mean everything is fine
- The `📦 Recommended compatible set` section gives the exact versions to install
- The `Install command` at the bottom can be copied and run directly

### Step 4: Help the user fix issues

When harmonia reports errors, help the user fix them by running the suggested commands. Common fixes:

- **Wrong companion version**: `pip install torchaudio==2.5.1` (use the version harmonia suggests)
- **CUDA mismatch**: Install torch with the correct CUDA index URL from the recommendation
- **torch too old for transformers**: `pip install torch>=2.4.0`
- **No virtualenv**: `python -m venv .venv && source .venv/bin/activate`

## Rules

- Always run `harmonia check` FIRST when a user reports any ML dependency issue — do not guess
- Always show the full output to the user — do not summarize away important details
- If harmonia is not installed, install it with `pip install harmonia-ml` before running commands
- Do NOT try to manually diagnose version compatibility — let harmonia do it
- When harmonia suggests a fix, offer to run the fix command for the user
- If the user asks about versions not in harmonia's database, say so and suggest checking the official docs

## Constraints

- This skill only checks compatibility — it does not install or modify packages unless the user asks
- harmonia works offline with a local database — it does not make API calls
- The database covers PyTorch 2.0–2.5 and Transformers 4.24–5.x — very old versions may not be covered
