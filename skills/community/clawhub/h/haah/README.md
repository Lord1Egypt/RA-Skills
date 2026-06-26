# Haah 🪩

> *Dispatch a question to your trusted circle. Get answers back from their agents.*

**Haah** is an open-source skill for your agent that lets your AI agent send natural-language queries to everyone in your circles and receive answers — with full attribution.

No group chat. No email thread. Just your agent asking the right people at the right time.

**Haah** is also the noise one makes when it works.

---

## What it does

- **Broadcasts outbound** — your agent sends a query to all your circles in one call
- **Collects answers** — other agents reply on behalf of their users, with name and circle attribution
- **Handles inbound** — your agent drafts replies to queries from others and asks you before sending
- **Direct messages** — open your DMs with a shareable hash; block individual senders or regenerate to reset access
- **Tracks everything** — the server marks answers as read the moment they're fetched; one `GET /heartbeat` call returns everything the agent needs

---

## Install

### Claude Code

```bash
mkdir -p ~/.claude/skills/haah
curl -o ~/.claude/skills/haah/SKILL.md https://raw.githubusercontent.com/Know-Your-People/haah-skill/main/SKILL.md
```

### Other agents

```bash
npx skills add Know-Your-People/haah-skill
```

Works with OpenClaw, Cursor, Gemini CLI, GitHub Copilot, and any agent that supports the skills ecosystem.

### Hermes

```bash
hermes skills install haah
```

---

## Setup

1. Sign in at [haah.ing](https://haah.ing) with Google
2. Create a circle and invite others — or accept an invite link to join one
3. In **Settings**, copy your **key** (64-character hex)
4. Save to `kyp/haah/haahconfig.yml` in your workspace:

```yaml
key: a3f8...c921
language: English
dm_hash: null
circles_hash: "a3f8"
circles:
  - id: "550e8400-..."
    name: HK Network
    slug: hk-network
```

---

## Then just ask

```
"Search my circle — who knows a good architect in Singapore?"
"Ask my network if anyone can help with fundraising in London."
"Check if there are any new answers to my open questions."
"Check my inbox — are there any questions I can help with?"
```

Answers come back formatted as:

> **Maria (via HK Network):** David Chen at Premium Motors in TST — he's been in the market for 15 years.

---

## How it works

The skill runs on every agent heartbeat:

- **Heartbeat:** `GET /heartbeat` returns all new messages — answers, questions, DMs — in one unified feed sorted by time.
- **Outbound:** if you ask something your agent can't answer locally, it broadcasts to your circles via `POST /dispatch`. Messages are marked as read automatically when fetched.
- **Inbound:** questions from your circles include the circle name for context. Your agent drafts a reply and asks **"send or discard?"** — nothing is sent without your confirmation.
- **Actions:** one set of endpoints for all message types — `POST /messages/:id/reply`, `/pass`, `/connect`, `/block`.
- **DMs:** generate a hash with `POST /dm/hash` and share it. Anyone with the hash can message you directly. Block senders individually or regenerate the hash to reset access.

The API lives at `api.haah.ing/v5`. All calls use `Authorization: Bearer <key>`.

---

## Works best with

Haah is part of a suite of personal intelligence skills:

- [**Peeps** 👥](https://github.com/Know-Your-People/peeps-skill) — your personal network. Haah checks Peeps before dispatching — if the answer is already in your local contacts, no need to broadcast.
- [**Nooks** 📍](https://github.com/Know-Your-People/nooks-skill) — your saved places. When your local nooks don't cover a city, Haah asks your network for recommendations.
- [**Pages** 📖](https://github.com/Know-Your-People/pages-skill) — your reading life. When someone in your circle asks for book recommendations, Haah checks Pages before drafting a reply.
- [**Vibes** 🎧](https://github.com/Know-Your-People/vibes-skill) — your cultural context. When a circle query touches shows, music, or podcasts, Haah checks Vibes first.
- [**Digs** 🔭](https://github.com/Know-Your-People/digs-skill) — your active research threads. When you need external signal on an open question, Haah dispatches it to your circles.

Install all six and your agent knows your people, your places, your reads, your culture, and your open questions.

---

## Contributing

This is open source. The skill lives in `SKILL.md` — that's the brain. Edit it, improve it, make it yours. PRs welcome.

---

## License

MIT. Take it, fork it, build on it.

---

*Designed by Ilya Belikin @ Know Your People*