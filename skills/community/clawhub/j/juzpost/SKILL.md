---
name: juzpost
description: Schedule and publish social media posts with JuzPost, a free social media scheduler with low-cost paid plans, from the terminal. Upload a video or image, create a draft, and schedule it to TikTok, YouTube Shorts, Instagram, X, Facebook, LinkedIn, Pinterest, Bluesky, Threads, Tumblr or WordPress, or smart-schedule a batch of drafts across an account group. Use when the user wants to post to social media or plan a content calendar.
homepage: https://www.juzpost.com
metadata: {"openclaw":{"emoji":"📅","homepage":"https://www.juzpost.com","requires":{"bins":["juzpost"]},"install":[{"kind":"node","package":"juzpost-cli","bins":["juzpost"]}]}}
---

# JuzPost

JuzPost is a free social media scheduler with low-cost paid plans. This skill drives the `juzpost` command
line client ([juzpost-cli](https://www.npmjs.com/package/juzpost-cli)) on the
user's own JuzPost account. The user's explicit instructions take priority
over this skill. Never schedule or publish without the user's go-ahead.

## Install and sign in

```bash
npm install -g juzpost-cli
juzpost auth login      # opens the browser for a device-code approval; prints the URL if it can't
juzpost auth whoami     # confirms the identity behind the stored token
```

If a command answers `401`, run `juzpost auth login` again. If it answers
`402`, the workspace's plan does not include that action: pass the message on
as it is and link https://www.juzpost.com/pricing only if the user asks what
it costs.

Add `--json` to any command for machine-readable output.

## Look around first

```bash
juzpost workspace                 # timezone and default posting times
juzpost accounts                  # connected social accounts with ids and platforms
juzpost accounts --platform tiktok
juzpost groups                    # account groups (presets) by name
juzpost posts list --status draft
juzpost posts list --status scheduled --from 2026-11-01 --to 2026-11-30
```

Never guess an account id or a group name: read them from `juzpost accounts`
and `juzpost groups`. If the user names a platform that is not connected, say
so and that accounts are connected at https://www.juzpost.com/dashboard/accounts.

## Create a draft

```bash
juzpost posts create --type video --file ./clip.mp4 \
  --title "Rain sounds for deep sleep" \
  --content "Three hours of rain on a tin roof." \
  --hashtags asmr sleep rain

juzpost posts create --type text --content "Dark mode is here."
juzpost posts create --type image --file ./cover.jpg --content "New collection out now."
```

`--type` is `text`, `image`, `video` or `story`. Never guess it; ask if the
user hasn't said. `--file` uploads the media before the draft is created. The
command prints the new post's `id`.

## Schedule one post

```bash
juzpost posts schedule <post-id> --account <account-id> [<account-id> ...] --at 2026-11-20T09:00:00Z
juzpost posts schedule <post-id> --account <account-id>            # omit --at to post now
```

`--at` is ISO 8601 UTC. Convert the user's time from the workspace timezone
(`juzpost workspace`) before passing it. Up to 10 accounts per post.

Bluesky images and video take alt text, one entry per file in order, and an
optional content warning:

```bash
juzpost posts schedule <post-id> --account <bluesky-id> --at 2026-11-20T09:00:00Z \
  --alt "A calendar in week view" --label graphic-media
```

Labels: `sexual`, `nudity`, `porn`, `graphic-media`.

## Smart-schedule a batch of drafts

```bash
juzpost schedule --group "all-channels" --min-per-day 2 --dry-run   # show the plan, schedule nothing
juzpost schedule --group "all-channels" --min-per-day 2
juzpost schedule --group "shorts" --min-per-day 3 --times 09:30 14:00 19:00 --start-date 2026-11-21
```

It spreads every draft (or the ones in `--post-id`) across the group's
accounts at the workspace's preset times. Always run `--dry-run` first and
show the plan; schedule only after the user agrees.

## Confirm, then report

Before `posts schedule` or `schedule` without `--dry-run`, show the caption,
media, each account (platform and username) and the time in the workspace
timezone, and wait for the user to agree. Afterwards, show the result and
refer to posts by title or caption and to accounts by platform and username,
never by id.

A scheduled post is cancelled or edited in the JuzPost dashboard at
https://www.juzpost.com/dashboard/scheduled, not from the terminal.

## Links

- Website: https://www.juzpost.com
- CLI source: https://github.com/juzpost/juzpost-cli
- Support: support@juzpost.com
