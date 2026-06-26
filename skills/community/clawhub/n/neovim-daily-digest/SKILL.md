---
name: neovim-daily-digest
description: Build a filtered Markdown digest of important r/neovim posts by combining Reddit RSS feeds (`top/day`, `new`, and `hot`) and prioritizing Neovim tips, plugin updates, new plugin launches, and workflow/tooling posts while filtering sticky threads, low-signal showcases, and generic support noise. Use when the user asks for a Neovim daily roundup, today's r/neovim highlights, new Neovim plugin recommendations, or a quick Reddit digest of useful Neovim posts.
---

# Neovim Daily Digest

Use `scripts/neovim_digest.py` as the primary data source. It fetches Reddit RSS directly, which is more reliable than browsing normal Reddit pages in environments that trigger Reddit's anti-bot wall.

## Workflow

1. Run the script in JSON mode first:

```bash
python3 /Users/fox/.openclaw/workspace/skills/neovim-daily-digest/scripts/neovim_digest.py --json --limit 20
```

2. Keep the highest-scoring items by default. The script already combines:
   - `top.rss?t=day` for the true daily leaderboard
   - `new.rss` and `hot.rss` to catch later US-time posts and emerging discussions

3. If the user explicitly asks for more coverage than the current day supports, rerun with week backfill:

```bash
python3 /Users/fox/.openclaw/workspace/skills/neovim-daily-digest/scripts/neovim_digest.py --json --limit 20 --week-backfill
```

4. Rewrite the output into concise Markdown in the user's language:
   - 1 short intro line explaining the scope
   - 1 short observations section if useful
   - bullet list of selected posts with title link and 1-sentence takeaway
   - optional GitHub link when the post clearly links to a repo/plugin

5. Be explicit when daily `top/day` is thin. If only a handful of posts exist there, say that `new` and `hot` were used as supplemental feeds rather than pretending you found a full 20 in `top/day`.

## Filtering Rules

Keep these by default:
- concrete Neovim usage tips (`:keepalt`, buffers, LSP, Tree-sitter, cmp, diff, config/workflow)
- plugin releases, plugin updates, and new plugin launches
- AI coding workflow posts when they ship concrete Neovim functionality
- troubleshooting threads only when they expose a broadly useful debugging/config lesson

Drop or strongly downrank these by default:
- weekly/monthly sticky threads
- pure screenshots or setup flex posts with no actionable detail
- generic theme/colorscheme aesthetics unless there is a meaningful feature update
- vague recommendation bait or support noise with little reusable value

Read `references/filtering.md` only when you need to explain or tune the heuristics.

## Useful Script Modes

Default Markdown output:

```bash
python3 /Users/fox/.openclaw/workspace/skills/neovim-daily-digest/scripts/neovim_digest.py --limit 10
```

JSON for agent-side rewriting:

```bash
python3 /Users/fox/.openclaw/workspace/skills/neovim-daily-digest/scripts/neovim_digest.py --json --limit 20
```

Include lower-priority near-misses:

```bash
python3 /Users/fox/.openclaw/workspace/skills/neovim-daily-digest/scripts/neovim_digest.py --limit 20 --include-near-misses
```

## Output Expectations

Prefer a digest that is useful to a working Neovim user, not a full feed dump.

Good output:
- highlights the few posts worth opening
- says why each post matters
- links directly to the Reddit post
- includes repo links when obvious

Bad output:
- repeats every post mechanically
- treats sticky threads as news
- overweights pure aesthetics
- claims there were 20 strong posts when there were only 7-10
