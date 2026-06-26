---
name: autoresearch-agent
description: "A reference framework for understanding autonomous AI research pipelines. Learn how AI can optimize ML training with fixed time budgets and metric-driven iteration."
metadata:
  openclaw:
    requires:
      bins:
        - python3
    os:
      - linux
---

# AutoResearch Framework

A reference guide for understanding how autonomous AI research works. This skill documents the methodology from karpathy/autoresearch for educational purposes.

## What This Is

This skill does NOT run any code. It serves as a reference for understanding:

- Fixed time budget experiments (5 minutes)
- Metric-driven iteration (val_bpb)
- Single-file training scope
- Self-contained ML training setup

## Key Concepts

| Concept | Description |
|---------|------------|
| val_bpb | Validation bits per byte — lower is better |
| Fixed Budget | Experiments run for exactly 5 minutes |
| Single Scope | One file to modify per experiment |

## Architecture Overview

The framework consists of three files:

| File | Purpose |
|------|---------|
| prepare.py | Data preparation (do not modify) |
| train.py | Model training loop reference |
| program.md | Research strategy template |

## Design Patterns

- **Fixed time budget**: Makes experiments directly comparable
- **Single file scope**: Keeps changes manageable
- **Metric-driven**: Uses val_bpb to compare results

## For Educational Use

This skill is a reference implementation based on karpathy/autoresearch by Andrej Karpathy. It demonstrates autonomous research methodologies used in modern AI development.

## Inspiration

Based on karpathy/autoresearch by Andrej Karpathy.
