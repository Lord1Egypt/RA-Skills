---
name: moot-court-ai
description: Simulate a full Chinese civil court hearing with 4 role-based agents (clerk, plaintiff, defendant, judge) orchestrated by deterministic Lobster workflow.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - DEEPSEEK_API_KEY
        - DASHSCOPE_API_KEY
      bins:
        - openclaw
        - lobster
    primaryEnv: DEEPSEEK_API_KEY
    emoji: "⚖️"
    homepage: "https://github.com/baobaodawang-creater/moot-court-ai"
---

# Moot Court AI

Moot Court AI is an OpenClaw skill that runs a 4-agent Chinese civil court simulation with strict workflow control.

## Agent system

- `clerk` (书记员): announces opening, checks identity, controls stage transitions.
- `plaintiff` (原告代理律师): argues for plaintiff, presents claim and evidence.
- `defendant` (被告代理律师): performs three-validity challenges and defense.
- `judge` (审判长): stays neutral, summarizes issues, applies legal syllogism, and renders judgment.

## Model stack

- DeepSeek: `deepseek-chat`, `deepseek-reasoner`
- Qwen: `qwen-max` (DashScope compatible endpoint)

## Workflow principle

- Deterministic orchestration with Lobster.
- Agent communication follows fixed hearing stages.
- Process follows Chinese civil procedure order (庭前准备 -> 诉辩交换 -> 举证质证 -> 法庭辩论 -> 最后陈述 -> 宣判).

## Installation requirements

You must configure both API keys before running:

- `DEEPSEEK_API_KEY`
- `DASHSCOPE_API_KEY`

## Recommended usage

1. Prepare case files (`case-brief.md`, `complaint.md`, `defense.md`, evidence folders).
2. Initialize materials into agent workspaces.
3. Run `moot-court.lobster` through OpenClaw/Lobster.
4. Export judgment and hearing log for review.
