# Neron — Quick Start

**@NeronBetaBot** in Telegram. Your second brain with a graph underneath.

---

## Record

Send anything to the bot:
- **Voice message** → auto-transcribed, stored as note
- **Text** → stored as note
- **Photo with caption** → stored with context

That's it. Just talk to it like a journal. Neron extracts the rest automatically: mood, activities, body state, people mentioned, tasks implied.

---

## Commands

| Command | What it does |
|---------|-------------|
| `/start` | Begin |
| `/ai` | Ask your graph a question ("how was my week?", "what did I say about Dima?") |
| `/tasks` | See open tasks, create new ones |
| `/token` | Get MCP token for agent integration |

---

## What Neron Extracts (automatically)

Every note you send gets analyzed. No extra effort from you.

**Mood** — valence (negative ↔ positive) + energy (low ↔ high) + emotions list.
Record a voice note saying "ну такое, устал, но норм" → Neron tags: `valence: 0.2, energy: 0.3, emotions: [tired, neutral]`.

**Activities** — what you did. "Пошёл в качалку" → `type: exercise, description: gym`.

**Body** — sleep, substances, wake time. "Лёг в 3, встал в 10, покурил" → `sleep: 7h, woke_up_at: 10:00, substance: weed`.

**People** — anyone you mention gets linked. "Созвонился с Димой по дизайну" → note MENTIONS person:Dima.

**Tasks** — implied actions get captured. "Надо бы запушить скилл на гитхаб" → task created, status: pending.

---

## Cool Things to Try

### Ask your graph
`/ai How was my mood this week?`
→ Gets mood data from all your notes, shows trend, tells you what days were good and why.

`/ai What patterns do you see?`
→ Analyzes correlations: "You write more when energy is high. Your energy drops after days with substance use. You mention Dima mostly in productive contexts."

`/ai Stale tasks`
→ Shows tasks you created but never touched. Calls you out.

### Mood graph over time
`/ai Show my mood for the last 2 weeks`
→ Day-by-day valence + energy. See the shape of your emotional landscape.

### People map
`/ai Who do I mention most?`
→ Ranked list of people in your notes. Who occupies your headspace.

### Activity ↔ mood correlation
`/ai What activities make me feel best?`
→ Cross-references activities with mood scores. Data-driven self-knowledge.

### Substance tracking
`/ai How does weed affect my next day?`
→ Compares next-day mood after substance use vs clean days. No judgment, just data.

### Deep search by meaning
`/ai Find notes where I was feeling lost or confused`
→ Uses AI embeddings to find notes by *meaning*, not just keywords. Even if you never wrote the word "confused", it finds notes with that vibe. Works cross-language — search in English, find Russian notes.

---

## Agent Integration (for power users)

Connect your AI agent to your graph for autonomous access:
- **Claude** → [Connect to Claude guide](CONNECT-CLAUDE.md) (uses `/password`)
- **Other agents** (OpenClaw, Cursor, Claude Code) → [Connect Agent guide](CONNECT-AGENT.md) (uses `/token`)

---

## Privacy

- Your data lives in an isolated database schema (multi-tenant, schema-per-user)
- Voice notes are transcribed and stored — originals are not kept
- No data shared between users
- Tokens are per-user and revocable
