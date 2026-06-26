# Channel Formatting

Format the digest output for the current channel. The agent knows which channel it's delivering to.

## Slack

Bold headings, blockquotes for metrics, monospace for language, `─────────` under title, `_· · ·_` separators between repos:

```
📊 *GitHub Growth Digest — Friday April 03, 2026*
─────────────────────────────────────

📌 *Your Repos*

*99rebels/blog-translator*
> ⭐ Stars: 3 ↑ (+2)
> 🍴 Forks: 1 →
> 📋 Issues: 2 ↓ (-1)
> 📝 Commits (4w): 5 ↑ (+5)
> `TypeScript` · Last push: 2026-04-03
> vs watchlist: ✅ above avg commit velocity

_· · · · · · · · · · · · · · · · · · · · · · · · · · ·_

📌 *Watchlist*

*octocat/Hello-World*
> ⭐ 3,550 | 🍴 5,963 | 📋 3,833 | 📝 0
```

## WhatsApp

Bold repo names only. No blockquotes, no code formatting, no markdown tables. `─────` separators:

```
📊 GitHub Growth Digest — Friday April 03, 2026
─────────────────────────────────────

📌 Your Repos

*99rebels/blog-translator*
⭐ Stars: 3 ↑ (+2)
🍴 Forks: 1 →
📋 Issues: 2 ↓ (-1)
📝 Commits (4w): 5 ↑ (+5)
TypeScript · Last push: 2026-04-03
vs watchlist: ✅ above avg commit velocity

─────────────────────────────────────

📌 Watchlist

*octocat/Hello-World*
⭐ 3,550 · 🍴 5,963 · 📋 3,833 · 📝 0
```

## Discord

Similar to Slack but no blockquotes (Discord ignores `>` on multi-line). Use `**bold**` headings, `` `code` `` for language, `─────` separators, blank lines between repos.

## Terminal

Use raw script output as-is. No formatting changes needed.
