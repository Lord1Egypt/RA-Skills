# Hunt 🎯

**Digital bounty hunter — find, track, and conquer online hackathons, build your portfolio, and live the digital nomad life.**

Hunt is an OpenClaw skill that turns your AI agent into a personal hackathon scout. It finds legit online hackathons, vets them for quality, tracks them in a `map.md` file, and reminds you before each event starts.

---

## 🚀 Quick Start

### 1. Install
Place the skill in your workspace:
```bash
cp -r hunt/ ~/.openclaw/workspace/skills/
```

### 2. Hunt
Say **"hunt"** to your agent. It'll browse the web and find upcoming online hackathons that match your skills.

### 3. Track
Say **"add 1,3,5 to map"** to save selected hackathons. They get written to `map.md` and reminders are set automatically.

### 4. Check
Say **"show map"** anytime to see your bounty board.

---

## 🧠 How It Works

```
You: "hunt"
  Agent scouts MLH, Devfolio, Devpost, lablab.ai
  → Filters: online only, free, no web3, matches your skills
  → Presents a numbered list

You: "add 1,3,5 to map"
  Agent writes entries to map.md
  → Sets cron reminder 1 day before each event
  → Confirms what was added

You: "show map"
  Agent reads map.md and displays your board

You: "remove 2 from map"
  Agent deletes entry, cancels reminder, renumbers
```

---

## 📦 Files

```
hunt/
├── SKILL.md              # Agent instructions (core logic)
├── README.md             # This file
├── references/
│   └── map-format.md     # map.md format reference
└── hunt.skill            # Packaged distributable skill
```

---

## 📋 Criteria for Hackathons

| Criteria | Rule |
|----------|------|
| Online | 100% digital, no travel required |
| Free | $0 to register and participate |
| Open | Registration still open |
| No web3 | No blockchain/crypto/NFT unless you ask |
| Suitable | Matches your skill level (from USER.md) |

---

## 📍 The Map

Your `map.md` tracks everything:

```markdown
# 🗺 Hunt Map

## Active

### 1. Global Hack Week: GenAI
- **Host:** Major League Hacking (MLH)
- **Dates:** May 8–14, 2026
- **Theme:** Generative AI
- **Link:** https://events.mlh.io/
- **Reminder:** ✅ Set
- **Status:** Upcoming
- **Notes:** Beginner-friendly, daily challenges
```

---

## ⏰ Reminders

Hunt sets cron reminders automatically. They fire **1 day before** each event as a system event — you'll get a notification on Telegram (or whatever channel you use).

---

## ⚙️ Requirements

- OpenClaw agent (any model)
- `web_fetch` tool enabled
- Cron scheduling capability
- File read/write access to workspace

---

## 🧭 Philosophy

> Work anywhere. No boss. Total freedom.
>
> Every hackathon is a bounty. Every project ships your portfolio forward.
> The map is your treasure tracker. Hunt well.

---

## 📝 License

MIT — use it, fork it, ship it.
