# postnext-social-manager

A Claude Agent Skill for managing social media through [PostNext](https://postnext.io). It lets an agent connect-aware, upload media, compose, schedule, and publish posts across Twitter/X, Instagram, LinkedIn, Threads, YouTube, TikTok, and Bluesky, and read analytics - all via the PostNext public API with a single API key.

## Install

Copy this directory into your skills location (for Claude Code, a `skills/` directory the harness scans), then set your key:

```bash
export POSTNEXT_API_KEY=<your key>   # create at https://postnext.io/account/api-keys
```

The bundled `postnext` helper needs `curl` and `jq`. In an environment with no shell (for example claude.ai), the skill can still read channels, posts and analytics with the curl recipes in `references/`. Publishing, scheduling, cancelling, deleting, uploading and analytics sync need the helper, so they always go through its preview and `--confirm` step.

## Quick start

```bash
./postnext channels                                   # what is connected
./postnext post --provider twitter --text "Hello" --media ./hero.png   # prints a preview, sends nothing
./postnext post --provider twitter --text "Hello" --media ./hero.png --confirm <code>   # after the user approves
./postnext schedule --provider instagram --text "Launch" --media ./a.jpg --at 2026-07-25T14:00:00Z
./postnext analytics best-time twitter
```

Run `./postnext help` for the full command list. `post`, `schedule`, `cancel`, `delete`, `upload` and `analytics sync` always preview first and need the `--confirm` code from that preview to run. `bash tests/confirm.sh` checks this offline.

## What is in here

| Path | What |
|------|------|
| `SKILL.md` | Skill entry point: setup, the core loop, and a router to the references. |
| `postnext` | Bash helper (curl + jq) that handles the API's error-prone parts. |
| `references/` | Per-area docs (posts, media, channels, analytics, errors) with helper commands and read-only curl recipes. |
| `tests/confirm.sh` | Proves the six account-changing commands send nothing without a matching `--confirm` code. |

## Scope

Covers the PostNext social publishing and analytics loop. Out of scope (use the PostNext MCP at `mcp.postnext.io` or the web app): connecting channels, WordPress/blog posts, brand-profile edits, and team management.

## License

MIT. See `LICENSE`. Not affiliated with post-bridge; inspired by the shape of its social-manager skill.
