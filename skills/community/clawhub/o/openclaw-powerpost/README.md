# PowerPost Skill for OpenClaw

Tell your agent what to post. It writes the captions, makes the images, and publishes them for you.

[![Version](https://img.shields.io/badge/version-0.4.0-blue)](https://github.com/tarekhoury/openclaw-powerpost)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

---

## What it does

You say "post about our product launch on Instagram and TikTok" and the agent takes it from there. It researches the topic, writes captions that fit each platform, generates images or videos if you want them, and publishes to your connected accounts. You can also pass in URLs as research sources so the captions reference specific pages. You review everything before it goes live.

Posts can go out now, or be scheduled for later (up to 60 days out), or canceled before they fire. After publishing, the agent can pull per-item analytics — views, likes, comments — so you can ask "how did that one do?" without leaving the chat.

Platforms: Instagram, TikTok, X (Twitter), YouTube, Facebook, LinkedIn, and more as they're added.

The agent can also run in draft-only mode if you'd rather review and publish manually.

---

## What you need

- A PowerPost account ([sign up here](https://powerpost.ai))
- An API key ([create one here](https://powerpost.ai/settings/api))
- Your workspace ID ([find it here](https://powerpost.ai/settings/workspaces))
- At least one connected social account ([connect here](https://powerpost.ai/settings/connections))

New accounts get 50 free credits to start.

---

## Install

```bash
# From ClawHub
openclaw skill install powerpost

# Or clone it
git clone https://github.com/tarekhoury/openclaw-powerpost.git ~/.openclaw/skills/powerpost
```

---

## Configure

You need to set two credentials. The API key can go in the Skills UI or via config. The workspace ID has to be set via config (the UI only has one field per skill).

```bash
# API key (or paste it into the "API key" field in the OpenClaw Skills UI)
openclaw config set skills.entries.powerpost.apiKey "pp_live_sk_YOUR_KEY"

# Workspace ID
openclaw config set skills.entries.powerpost.env.POWERPOST_WORKSPACE_ID "YOUR_WORKSPACE_ID"
```

If you prefer environment variables:

```bash
export POWERPOST_API_KEY="pp_live_sk_YOUR_KEY"
export POWERPOST_WORKSPACE_ID="YOUR_WORKSPACE_ID"
```

---

## Try it

Just talk to your agent:

```
"Post about our new product launch on Instagram and TikTok"
"Write captions about AI trends for all platforms"
"Generate an image for my last post"
"Generate a 5-second video of a sunset over the ocean"
"Check my PowerPost credits"
"Upload this image and write captions about it"
"Create a draft about our company update but don't publish yet"
"Post about this page: https://example.com/launch"
"What's on my calendar for next week?"
"Plan a post about our product launch for March 25th on Instagram and TikTok"
"Move that calendar entry to Friday"
"Delete that calendar entry"
"Schedule this post for Friday at 9am ET"
"Cancel that scheduled post"
"How did my last Instagram post do?"
```

---

## API key scopes

Each API key has a set of scopes that control what it can do. The dashboard ships three presets:

| Preset | What it can do | Good for |
|---|---|---|
| Full access | Everything, including publishing | Agents that post on your behalf |
| Draft only | Generate, upload, and draft — but can't publish, schedule, or cancel | When a human reviews before posting |
| Read only | Only the `:read` scopes (no generation, no publishing) | Reporting, analytics dashboards |

You can also pick scopes individually. The full list is in [`SKILL.md`](SKILL.md#api-key-scopes).

---

## Supported platforms

| Platform | Post types |
|---|---|
| Instagram | Feed, Reel, Story |
| TikTok | Video, Photos |
| X (Twitter) | Post |
| YouTube | Video, Short |
| Facebook | Post, Reel, Story |
| LinkedIn | Post |

---

## Credits

Every generation and publish uses credits. Costs vary by what you're doing — caption generation, image model, video model and duration, publishing platform. The exact cost shows up in every API response.

---

## Links

- [API docs](https://powerpost.ai/docs)
- [Dashboard](https://powerpost.ai)
- [Support](https://powerpost.ai/contact)
