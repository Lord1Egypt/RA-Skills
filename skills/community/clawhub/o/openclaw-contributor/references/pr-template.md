# OpenClaw PR template guide

Use this shape for OpenClaw PRs unless the repo or maintainers ask for something different.

## Title

Prefer a focused, subsystem-aware title.

Examples:

- `fix(web-search): honor OpenRouter-backed Perplexity runtime path`
- `[AI-assisted] fix(daemon): prefer stable wrapper path for user service launch`

## Body

```md
## Summary
- One sentence on the user-visible or maintainer-visible change.
- One sentence on the technical fix.

## Why
- What was broken, misleading, or brittle.
- Why this approach was chosen instead of alternatives.

## Validation
- `pnpm build`
- `pnpm check`
- `pnpm test`
- any subsystem-specific commands

## Screenshots
- before/after screenshots for UI or visual changes

## AI assistance
- AI-assisted: yes/no
- Testing level: untested / lightly tested / fully tested
- I reviewed the code and understand what it does.
```

## Notes

- Keep PRs focused.
- Call out risk areas plainly.
- Mention if this builds on an existing branch/PR.
- For security/auth changes, explain impact and rollback clearly.
