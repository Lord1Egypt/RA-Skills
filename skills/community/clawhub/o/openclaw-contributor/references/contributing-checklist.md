# OpenClaw contribution checklist

Use this when working in the `openclaw/openclaw` repo.

## Contribution policy

- Small bugfixes: open a focused PR.
- New features or architecture changes: start a GitHub Discussion or ask in Discord first.
- Keep one logical change per PR. Do not mix unrelated fixes.

## Required before opening a PR

- Test locally in a real OpenClaw instance when possible.
- Run the standard checks unless the change is docs-only:
  - `pnpm build`
  - `pnpm check`
  - `pnpm test`
- Ensure CI is expected to pass.
- Describe both **what** changed and **why**.
- Include screenshots for UI/visual changes: one before/problem and one after/fix.

## AI-assisted PR rules

- Mark the PR as AI-assisted in the title or description.
- State testing level clearly: untested / lightly tested / fully tested.
- Include prompts or session logs when helpful.
- Confirm you understand the code you are submitting.

## Control UI note

The Control UI uses Lit with legacy decorators. Keep reactive fields in legacy style:

```ts
@state() foo = "bar";
@property({ type: Number }) count = 0;
```

Do not switch to standard decorators unless the UI build tooling is updated too.

## Subsystem maintainer hints

Use these as routing hints, not hard rules:

- Peter Steinberger — overall maintainer / repo direction
- Shadow — Discord, ClawHub, moderation
- Vignesh — Memory (QMD), formal modeling, TUI, IRC
- Jos / Ayaan — Telegram
- Tyler Yust — agents, subagents, cron, BlueBubbles, macOS app
- Mariano Belinky / Vincent Koc / Josh Avant — security/auth/core hardening
- Val Alexander — UI/UX, docs, agent dev experience
- Gustavo Madeira Santana — agents, CLI, web UI
- Jonathan Taylor — ACP subsystem, gateway features/bugs, Gog/Mog/Sog CLI's

## Useful repo commands

- Core validation: `pnpm build && pnpm check && pnpm test`
- Fast unit-ish run: `pnpm test:fast`
- Gateway-heavy changes: `pnpm test:gateway`
- UI changes: `pnpm test:ui`
- Extensions: `pnpm test:extensions`
- Docs-only: `pnpm format:docs:check && pnpm lint:docs && pnpm docs:check-links`
- iOS: `pnpm ios:gen && pnpm ios:build`
- Android: `pnpm android:lint && pnpm android:test`

## Good-first workflow

1. Confirm whether the work is a bugfix or a feature.
2. Read `CONTRIBUTING.md` and inspect similar files/tests first.
3. Keep the branch focused.
4. Add or update regression tests with the fix.
5. Run appropriate validation for the touched subsystem.
6. Prepare a clear PR description with testing notes and AI disclosure.
