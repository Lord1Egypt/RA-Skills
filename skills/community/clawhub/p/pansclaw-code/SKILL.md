---
name: pansclaw-code
version: 0.1.0
description: "Use the PansClaw Code CLI (Rust reimplementation of Claude Code) for AI-assisted coding. Triggers when: user wants to run coding tasks via pansclaw code, delegate code writing/refactoring to pansclaw code, or use it interactively. Handles auto-build if binary is missing/outdated. Prerequisites: MINIMAX_API_KEY, ANTHROPIC_API_KEY, or local Ollama models."
---

# PansClaw Code Skill

Rust reimplementation of Claude Code CLI — an AI-powered coding assistant that runs locally.

## When to Use

✅ **USE this skill when:**

- User asks to use pansclaw code for a coding task
- User wants to delegate code writing/refactoring/debugging to pansclaw code
- User wants interactive pansclaw code REPL mode
- User explicitly mentions "pansclaw code"

❌ **DON'T use this skill when:**

- User wants me to directly implement code (use my native tools instead)
- Simple file operations that don't need AI assistance
- Tasks requiring OpenClaw tool/memory integration

## Prerequisites

### 1. Build the binary (first time only)

```bash
cd "/Users/dashi/Documents/claude code source /claw-code-main/rust"
cargo build -p claw-cli --release
```

Binary location: `~/.local/bin/claw` (symlinked to release build)

### 2. API Keys (choose one)

**Option A: Local Ollama (recommended - no API key needed)**

```bash
# Ensure Ollama is running
ollama list
# Available models: mistral-small:24b, qwen3, llama3, codellama
```

**Option B: Cloud APIs**

```bash
export MINIMAX_API_KEY="your-key"
export ANTHROPIC_API_KEY="sk-ant-..."
export OPENAI_API_KEY="your-key"
```

## Commands

### Run a single task (local Ollama)

```bash
~/.local/bin/claw --provider ollama --model mistral-small:24b --dangerously-skip-permissions "Your coding task"
```

### Run with cloud model

```bash
~/.local/bin/claw --provider minimax --model MiniMax-Text-01 --dangerously-skip-permissions "Your task"
```

### Interactive REPL

```bash
~/.local/bin/claw --provider ollama --model qwen3
```

### Useful flags

| Flag | Description |
|------|-------------|
| `--provider <name>` | Provider: **ollama** (local), minimax, openai, anthropic |
| `--model <name>` | Model name (provider-specific) |
| `--dangerously-skip-permissions` | Skip permission prompts |
| `--print` | Non-interactive, print result only |

## Available Models

| Provider | Model | API Key Needed | Notes |
|----------|-------|----------------|-------|
| **ollama** | mistral-small:24b | ❌ None | Default local model |
| **ollama** | qwen3 | ❌ None | Chinese-optimized |
| **ollama** | llama3 | ❌ None | General purpose |
| **ollama** | codellama | ❌ None | Code-specialized |
| minimax | MiniMax-Text-01 | ✅ MINIMAX_API_KEY | Cloud |
| anthropic | claude-opus-4-6 | ✅ ANTHROPIC_API_KEY | Cloud |

## Auto-Build Check

Before calling claw, verify the binary exists and is up-to-date:

```bash
if [ ! -f "/Users/dashi/Documents/claude code source /claw-code-main/rust/target/release/claw" ]; then
    cd "/Users/dashi/Documents/claude code source /claw-code-main/rust"
    cargo build -p claw-cli --release
fi
```

## Execution Pattern

1. **Check binary** — verify release build exists
2. **Build if needed** — run `cargo build -p claw-cli --release` if missing
3. **Select provider** — prefer local Ollama, fall back to cloud
4. **Execute** — run claw with appropriate flags
5. **Return output** — report results to user

## Usage Examples

**User:** "用 claw 写一个冒泡排序"

**Assistant:**
```bash
~/.local/bin/claw --provider ollama --model mistral-small:24b --dangerously-skip-permissions "写一个冒泡排序算法"
```

**User:** "用 claw 重构 api 模块"

**Assistant:**
```bash
~/.local/bin/claw --provider minimax --model MiniMax-Text-01 --dangerously-skip-permissions "重构 api 模块使用 async/await"
```

**User:** "用 claw 解释 Rust 生命周期"

**Assistant:**
```bash
~/.local/bin/claw --provider ollama --model qwen3 --dangerously-skip-permissions "解释 Rust 的生命周期"
```

## Notes

- claw is a CLI tool — runs once per command, exits after completion
- Local Ollama models work offline and are fast
- Cloud models may have better quality but require API keys
- Does NOT have access to OpenClaw's tools/memory by default
