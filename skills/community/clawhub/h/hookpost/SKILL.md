---
name: hookpost
description: Draft, schedule and publish social media posts to X, LinkedIn, Threads, Bluesky, Instagram, Facebook Pages, YouTube, TikTok, Pinterest, Discord, Slack, Telegram, Dev.to and more through the user's Hookpost workspace, using the hookpost CLI. Use when the user asks to post, tweet, schedule, queue or draft something for a social network, to connect a new social account, to attach an image or video, to see what is scheduled, or to check how a post did.
homepage: https://github.com/jatinder14/hookpost-mcp/tree/main/cli
metadata: {"openclaw":{"requires":{"bins":["hookpost"]},"install":[{"id":"npm","kind":"node","package":"hookpost","bins":["hookpost"],"label":"Install the hookpost CLI (npm)"}]}}
---

# Hookpost

Hookpost (https://hookpost.hookstep.in) is a hosted social media scheduler. The `hookpost` CLI acts on the user's own Hookpost workspace. Always pass `--json` and read the JSON it prints.

## Setup (once)

1. If `hookpost` is missing: `npm install -g hookpost`.
2. `hookpost whoami --json`. If it says `"signedIn": false`, run `hookpost login`. It prints a code and a link: show both to the user and wait while they approve in the browser. On a machine with no browser, ask the user for their API key (Hookpost > Settings > Developers) and run `hookpost login --key <key>`, or use the `HOOKPOST_API_KEY` environment variable.

## How to work

1. `hookpost channels --json` lists the connected channels. Map the user's words ("my LinkedIn") to a channel `id`. If two could match, ask which one.
2. The network they want is not connected? `hookpost connect <platform> --json` (for example `linkedin`, `x`, `threads`, `instagram`, `youtube`; Bluesky, Telegram and other networks that need a password or server address are added in the Hookpost app) returns a `url`. Give it to the user; it works for 24 hours. Once they say it is done, run `hookpost channels --json` again for the new id. `hookpost connect --json` lists the platforms a link can add.
3. Before writing for a network, `hookpost rules <channelId> --json` gives its maximum length, rules and settings. Write each post for its network instead of pasting one text everywhere.
4. Save drafts unless the user clearly asks to schedule or publish:
   `hookpost post "<text>" --channel <id> --draft --json`
   Scheduled and published posts go out to real accounts. Before scheduling or publishing, show the exact text, the channel names and the time (the user's timezone and UTC) and wait for a yes. Then use `--at <ISO date with zone>` or `--now`.
5. Every created post comes back with a `previewUrl`. Give it to the user so they can see the post as it will look, or send it to someone to approve.
6. Threads: `--thread "<text>"` adds a follow-up (a reply on X, Threads and Bluesky; a comment elsewhere). Repeat it for more.
7. Media: `--media <file or https URL>` attaches an image or video; repeat it for several. `hookpost upload <file|url> --json` uploads without posting.
8. Several channels at once: `--channel a,b,c`. `--settings` is for one channel at a time.
9. `hookpost posts --days 14 --json` lists what is scheduled. `hookpost analytics <channelId> --days 30 --json` and `hookpost analytics post <postId> --json` read analytics.
10. `hookpost delete <postId>` deletes a post and its group. Confirm with the user first.

## When something fails

The JSON error has `error` and `status`.
- 401: the key is missing, wrong or was rotated. Run `hookpost login` again.
- 402, or a message about the plan or free posts: the workspace has used its 3 free posts and needs the Hookpost plan, at https://hookpost.hookstep.in/pricing.
- 400 with a network's name: the post breaks that network's rules (too long, missing media or a setting). Fix it and try again; nothing was created.
- A post in ERROR state later: the network refused it at publish time; the reason is on the post in the Hookpost calendar.
