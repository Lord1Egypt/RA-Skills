---
name: mac-ai-optimizer
version: 1.0.0
description: |
  Optimize macOS for AI workloads (OpenClaw, Docker, Ollama). Turn an 8GB Mac into a lean AI server node with near-16GB performance by disabling background services, reducing UI overhead, configuring Docker limits, and enabling SSH remote management.
tags: ["macos", "optimization", "docker", "ai-server", "memory", "openclaw", "ollama"]
metadata: {"openclaw":{"emoji":"🖥️","requires":{"os":"darwin"}}}
---

# Mac AI Optimizer

Optimize macOS for AI workloads (OpenClaw, Docker, Ollama). Turn an 8GB Mac into a lean AI server node with near-16GB performance for Agent tasks.

## Tools

### optimize_memory
Reduce macOS idle memory from ~6GB to ~2.5GB by disabling Spotlight indexing, Siri, photo analysis, and other background services.

Usage: "Optimize this Mac's memory for AI workloads"

### reduce_ui
Lower GPU and RAM usage by disabling animations, transparency, and Dock effects.

Usage: "Reduce UI overhead on this Mac"

### docker_optimize
Configure Docker Desktop resource limits to prevent it from consuming all available memory. Sets CPU, RAM, and swap to balanced values.

Usage: "Optimize Docker for this Mac"

### enable_ssh
Enable remote login (SSH) so this Mac can be managed remotely as an AI compute node.

Usage: "Enable SSH on this Mac"

### system_report
Show current memory, CPU, swap usage, and running service count. Helps decide what to optimize.

Usage: "Show system resource report"

### full_optimize
Run all optimizations in sequence: system report -> memory -> UI -> Docker -> SSH. One command to turn a Mac into an AI server node.

Usage: "Full optimize this Mac for OpenClaw"

## Trigger
When the user asks to optimize Mac for AI, reduce memory usage, set up Mac as AI server, improve OpenClaw performance, or run AI workloads on low-memory Mac.

## Example prompts
- "Optimize this Mac for running OpenClaw"
- "My Mac only has 8GB RAM, make it run AI better"
- "Turn this Mac mini into an AI server"
- "Reduce memory usage so Docker runs better"
- "Set up this Mac as a remote AI node"
