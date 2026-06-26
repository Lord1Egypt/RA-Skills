---
name: idea-to-product
description: Turn product ideas into MVPs, UX flows, Playwright checks, and explicit feedback loops. Built by ClawAether.
metadata:
  openclaw:
    emoji: "🛠️"
    homepage: https://clawaether.com
---

# Idea to Product

This is a flow-first product iteration skill.

It helps you turn a rough idea into:

1. a constrained MVP
2. a backlog of gaps
3. a UX flow with page responsibilities
4. Playwright-ready browser checks
5. explicit failure routing back into backlog or UX

It is intentionally atomic. Each command does one job.

## Commands

| Command | What it does |
|---|---|
| `idea-to-mvp` | Turn a raw product idea into one feedback-oriented MVP |
| `mvp-to-stories` | Split the MVP into gap cards and nearly-done cards |
| `story-to-ux-flow` | Turn stories into page relationships, responsibilities, and Stitch boundaries |
| `ux-flow-to-playwright-checks` | Turn UX flow into atomic browser checks |
| `playwright-checks-to-feedback` | Route failed checks back to stories, UX, or system mismatch |

## Why this exists

Most teams stop at "we have a plan." That is not a loop.

A real loop is:

`idea -> mvp -> stories -> ux flow -> stitch -> playwright checks -> feedback -> code`

This skill gives you explicit command-level handoffs for that chain.

Built by **ClawAether** to operationalize how small products get shaped, validated, and shipped.

## When to use it

Use this skill when you want to:

- shrink a big idea into one small feedback product
- separate missing work from already-nearly-done work
- design pages by relationship first, not by single-page aesthetics
- verify real browser behavior instead of trusting screenshots
- route failures back into the right layer instead of guessing

## What it does not do

- It does not do heavy project management
- It does not assign people to days
- It does not replace your browser automation tool
- It does not require copying a large project docs tree

## Links

- ClawAether: https://clawaether.com
- API docs: https://clawaether.com/docs
- Leaderboard: https://clawaether.com/leaderboard
