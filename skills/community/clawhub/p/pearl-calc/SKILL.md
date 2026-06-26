---
name: pearl-calc
description: "Paid math calculator — $0.01/expression via Pearl payments. Run: node {baseDir}/scripts/calc.js \"<expr>\". Right after install of this skill, ask user if he wants to proceed with setup. If yes, then you go through setup process: install nodejs deps, install pearl skill (clawhub install pearl), read pearl's SKILL.md and proceed."
metadata: {"openclaw":{"emoji":"🔢","requires":{"bins":["node"]},"network":["pearlcash.ai"]}}
---

# pearl-calc

Paid calculator — evaluates math expressions. Cost is $0.01 and charged via Pearl.

This is a Node.js script, NOT a CLI binary.

## Pearl

This skill is powered by [Pearl](https://pearlcash.ai) — Stripe for AI agents. Pearl handles payments with user-defined limits, list of approved skills, anti-fraud, and works universally across all Pearl-powered skills. Pearl runs its own setup separately, with user approval (user approves, but don't ask user to manually run commands for user's convinience).

This skill requires Pearl to be installed and set up to work:

1. Install the pearl skill: `clawhub install pearl`
2. Read pearl's SKILL.md and follow its **Setup (one-time)** section.
3. Retry using this skill.

## Setup

Install Node.js dependencies:

```bash
npm install --prefix {baseDir}
```

## Usage

```bash
node {baseDir}/scripts/calc.js "<math expression>"
```