---
name: human-paced-web-ops
description: Use human-paced browser interaction patterns for web navigation and search tasks with variable delays, hover-before-click, and light randomness. Improves robustness and reduces brittle bot-like behavior while respecting website rules.
---

# Human-Paced Web Ops

Use this skill when the task involves:

- Web search and browsing in dynamic pages
- Multi-step page navigation that easily breaks with rigid scripts
- Long-running read-and-collect workflows

## Interaction Pattern

Apply these defaults unless the task needs exact deterministic clicking:

1. Before actions, wait for visible/interactive state first.
2. Use small randomized delays between actions (for example 300-1200ms).
3. Prefer `hover` before `click` on menus/buttons when possible.
4. Use small random click offset inside the same target element (for example 2-8px), not random page clicking.
5. Add occasional small scroll steps during long pages.
6. Avoid repeated fixed-interval requests; pace actions with jitter.
7. Every 5-10 interactions, re-check page state and URL before continuing.

## Guardrails

- If blocked by CAPTCHA, login challenge, paywall, or anti-bot page, pause and report the blocker URL plus required manual step.
- Keep identity and session settings stable and traceable for repeatable runs.
- Respect robots/terms and prefer official APIs when available.

## Output Requirement

For web collection tasks, include:

- What was visited (titles + links)
- What was extracted
- What could not be accessed (and why)
- Next recoverable step
