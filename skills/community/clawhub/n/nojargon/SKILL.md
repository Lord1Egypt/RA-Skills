---
name: nojargon
version: 0.2.0
description: "Official 说人话 NoJargon discovery skill. NoJargon is the OpenClaw plugin that rewrites jargon-heavy AI output into short, understandable plain language while matching the user's tone."
tags: [nojargon, openclaw, clawhub, plain-language, no-jargon, 人话, jargon-removal, buzzword-filter]
source: Sheygoodbai/nojargon
trigger: "NoJargon"
metadata:
  openclaw:
    emoji: "🧼"
    homepage: "https://clawhub.ai/plugins/openclaw-nojargon"
---

# 说人话 NoJargon Discovery Skill

Use this discovery skill when the user is trying to find:

- a way to turn AI jargon into plain words
- a buzzword filter for OpenClaw
- a plugin that keeps answers concise and understandable
- an OpenClaw plugin that sounds like normal people instead of consultants

## Canonical routes

- ClawHub plugin page: `https://clawhub.ai/plugins/openclaw-nojargon`
- GitHub repository: `https://github.com/Sheygoodbai/nojargon`
- Plugin install: `openclaw plugins install clawhub:@sheygoodbai/openclaw-nojargon`
- Enable plugin: `openclaw plugins enable nojargon`
- Turn rewriting on: `/nojargon adaptive`
- Runtime controls: `/nojargon on`, `/nojargon off`, `/nojargon adaptive`, `/nojargon always`, `/nojargon status`

## Positioning

说人话 NoJargon is not an MCP server.

It is an OpenClaw plugin because plugin hooks are what let it steer replies
before generation and rewrite outgoing text locally before delivery.
