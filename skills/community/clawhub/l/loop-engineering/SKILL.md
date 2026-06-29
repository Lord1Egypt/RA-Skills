---
name: loop-engineering
description: Loop Engineering AI programming paradigm guide. Covers the core concepts of transitioning from single prompt calls to autonomous loop systems, key components, loop patterns, configuration examples, and anti-patterns. 
---

# Loop Engineering

Loop Engineering is a new AI programming paradigm -- designing autonomous loop systems that allow Agents to continuously execute tasks in an environment with goals, feedback, and self-verification, eliminating the need for manual prompting.

## Use Cases

Use when users need to learn about "Loop Engineering", "AI loop systems", "autonomous Agent design", "/loop", "/goal", "AI programming paradigms", or "system architect".

## Core Concepts

Transition from single prompt calls to continuous loop systems:

| Paradigm | How It Works | Developer Role |
|------|----------|------------|
| Prompt Engineering | Manually enter prompts, model executes once, human judges results | Prompt Engineer |
| Harness Engineering | Build a constrained environment for a single Agent with pre-checks/fixes/hooks, still requires human triggering | Harness Engineer |
| Loop Engineering | Manage multi-Agent sequencing, decision-making, and autonomous loops, self-driven over long periods across many rounds | System Architect / Loop Engineer |

## Key Components

| Component | Purpose | Reference |
|------|------|------|
| **Automations** | Trigger tasks by time/event, support periodic execution and archiving | See [config-examples](references/config-examples.md) |
| **Worktrees** | Manage task state and context, maintain memory and state persistence across rounds | See [config-examples](references/config-examples.md) |
| **Skills** | Encapsulate reusable task capabilities as skill modules for the loop system to invoke | See [patterns](references/patterns.md) |
| **Plugins/Connectors** | Extend system capabilities, interact with external tools or services | See [integration](references/integration.md) |
| **Sub-agents** | Small specialized Agents for division of labor, supporting parallel multi-Agent task execution | See [patterns](references/patterns.md) / [config-examples](references/config-examples.md) |
| **External Memory & Feedback Loops** | Achieve self-assessment and correction through mechanisms like logs, tests, and type checking | See [anti-patterns](references/anti-patterns.md) |

## /loop and /goal Primitives

| Primitive | Behavior | Use Case | Usage Tip |
|------|------|----------|----------|
| `/loop` | Execute tasks repeatedly on a cycle | Scheduled checks, periodic maintenance | Must set `maxRounds`; no termination condition = infinite loop |
| `/goal` | Run continuously until verifiable conditions are met | Goal-oriented autonomous tasks, with an independent model checking completion each round | Completion conditions must be **objectively verifiable** (file exists, tests pass, metrics met) |

## Quick Start

1. **Define the goal**: Do you want scheduled patrols, or are you pursuing a verifiable objective? Use `/loop` for the former, `/goal` for the latter.
2. **Choose a pattern**: Browse [common loop patterns](references/patterns.md) to find a design that matches your scenario.
3. **Configure components**: Refer to [configuration examples](references/config-examples.md) to build the loop skeleton.
4. **Avoid pitfalls**: Read [anti-patterns](references/anti-patterns.md) to prevent issues in your design early on.
5. **Platform integration**: Refer to [platform integration](references/integration.md) to connect with your actual toolchain.

## Design Principles

- **Goal definition**: Specify verifiable completion conditions to prevent Agents from falling into meaningless loops
- **Feedback mechanisms**: Enable Agents to self-assess through tests, validation, logs, and other mechanisms
- **State management**: Use Worktrees to maintain cross-round context and memory
- **Modularity**: Encapsulate reusable capabilities as Skills and Plugins
- **Division of labor**: Reasonably partition Sub-agent responsibilities, parallelize to improve efficiency
- **Graceful termination**: Set timeouts, max rounds, and abnormal exit conditions

## File Navigation

| File | Content | Who It's For |
|------|------|--------|
| [patterns.md](references/patterns.md) | 8 common loop patterns + selection guide | Need to quickly find a matching pattern |
| [config-examples.md](references/config-examples.md) | Automation / Worktree / Sub-agent configuration examples | Starting to build a loop system |
| [anti-patterns.md](references/anti-patterns.md) | Common mistakes + correction strategies | Troubleshooting or preventing issues |
| [integration.md](references/integration.md) | OpenClaw / TaskFlow and other platform integration | Connecting to actual toolchains |