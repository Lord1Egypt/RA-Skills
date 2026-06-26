# Manusilized Core Patches

This directory contains the modified core files for OpenClaw. Since Manusilized upgrades the core architecture (specifically the Ollama provider), it cannot be installed merely as a standalone skill.

## How to apply

1. Copy `ollama-stream.ts` and `ollama-models.ts` from this repository.
2. Replace the original files in your OpenClaw installation at `src/agents/`.
3. Rebuild your OpenClaw project using `pnpm build`.

Alternatively, please support our official PR to get these features merged into the main OpenClaw repository!
