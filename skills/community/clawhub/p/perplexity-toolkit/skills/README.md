# Agent skills

The CLI in this repo is the default Perplexity execution route. The direct
browser route is an explicit user choice. These three skills carry the
operational knowledge an agent needs to route Perplexity work safely: which
route to take, how to keep browser sessions from fragmenting, and when an
answer is allowed to be called verified.

They are plain Markdown with YAML frontmatter, so any agent framework that
loads `SKILL.md` files can use them.

## Route contract

There are two user-facing routes:

1. If the user explicitly says **web page, browser, Chrome, WebBridge, Kimi
   WebBridge, open Perplexity, or continue the current browser thread**, use
   `perplexity-web-automation` directly. Do not invoke the CLI first.
2. For every other Perplexity request, use the `perplexity` CLI first. If the
   CLI is unavailable or fails, stop and report that fact; do not silently
   switch to the user's browser. Switch only after the user explicitly allows
   the browser route.

The current CLI is a CLI interface over the toolkit's WebBridge driver. It is
not an API or headless backend; even the default CLI route ultimately uses
Kimi WebBridge and Chrome.

## What each one is for

| Skill | Layer | Use it for |
|---|---|---|
| `perplexity-search` | Policy | Quick lookups and the shared source-verification contract |
| `perplexity-conversational-research` | Router/workflow | Applies the route contract (also available as local `perplexity route`) and organizes deep or multi-turn research |
| `perplexity-web-automation` | Direct-web execution | Perplexity-specific logged-in Chrome / WebBridge actions, plus the standalone helper |

`perplexity-search` owns the canonical candidate-vs-verified boundary and the
HEAD-vs-readback rule. The other skills reference it rather than restating it.
Choose one high-level route per task; do not load all three as competing
workflows.

## Install

Point your agent's skill directory at these, rather than copying them — a copy
goes stale the moment this repo updates.

```bash
git clone https://github.com/mfang0126/perplexity-toolkit.git ~/src/perplexity-toolkit

# Symlink into wherever your framework loads skills from.
# Claude Code / Hermes example:
ln -s ~/src/perplexity-toolkit/skills/perplexity-search           ~/.claude/skills/perplexity-search
ln -s ~/src/perplexity-toolkit/skills/perplexity-web-automation   ~/.claude/skills/perplexity-web-automation
ln -s ~/src/perplexity-toolkit/skills/perplexity-conversational-research \
                                                                  ~/.claude/skills/perplexity-conversational-research
```

Then `git pull` in the clone to update all three at once.

## Two reliability tiers, on purpose

`perplexity-web-automation/scripts/perplexity_search.py` reimplements logic that
also exists in `perplexity_toolkit.search`. That overlap is deliberate, but the
script is an **explicitly authorized fallback/diagnostic**, not an automatic
route switch.

| | `perplexity_toolkit` | `perplexity_search.py` |
|---|---|---|
| Imports | its own package (config, drivers, utils, i18n, verify) | standard library only, shells out to `curl` |
| Runs when nothing is installed | no | yes, only after the user permits the direct-browser route |
| Role | primary CLI executor | explicit direct-browser helper and diagnostic |
| Retry / backoff | yes (`_search_with_retry`) | none, by design |

The script's independence is its entire value. A toolkit installed into one
environment is invisible to an agent running a different interpreter — an
observed failure mode, not a hypothetical one. If the script imported the
toolkit, the fallback would vanish precisely when it is needed, and nobody
would notice until the day the toolkit broke.

So: **do not deduplicate these two.** If shared logic genuinely needs to move,
vendor it as a stdlib-only module inside `scripts/`. The missing retry is also
intentional — a diagnostic should show the raw failure rather than mask it.

## Requirements

The skills reference the `perplexity` CLI as an optional route and Kimi
WebBridge as the browser layer. See the repo README for installing the CLI
(`pipx` is recommended so it lands on `PATH`) and for the setup self-check.

Cross-references between these skills use skill **names**, never absolute
paths, so they resolve regardless of where you install them.
