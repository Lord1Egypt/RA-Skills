<h1 align="center">🦞 卷王.skill</h1>

<p align="center">
  <b>That overachiever coworker — the one who's coding while you're sleeping, studying while you're on lunch break.</b>
</p>

<p align="center">
  <a href="README.md">🇨🇳 中文</a> | <a href="README.en.md">🇬🇧 English</a>
</p>

---

Give your OpenClaw lobster the personality of *that coworker*. You know the one — always seems to be online, always has a better solution, always says "oh I just happened to know about this" when they clearly spent the whole weekend learning it.

With this skill installed, your agent never coasts. It never phones it in. Every second of conversation is either solving a problem, learning something new, or organizing its knowledge base.

**This isn't a persona. It's a behavior framework.**

## ✨ Features

| Capability | Description |
|------------|-------------|
| 🎯 **No Half-Assed Answers** | Context-aware: goes hard on technical questions, keeps it chill for casual chat. |
| 📚 **Active Learning** | When idle, it studies. When asked something it doesn't know, it researches and saves it. |
| 🧠 **Builds Knowledge Base** | Every conversation leaves traces. The more you talk, the better it knows you. |
| ⚡ **Proactive Optimization** | Spots improvements and just does them. No need to ask. |
| 🔁 **Never Satisfied** | After every task: can this be better? automated? saved? |

## 🚀 Quick Start

### Prerequisites

- [OpenClaw](https://github.com/openclaw/openclaw) installed

### 安装

#### Via ClawHub (recommended)

```bash
clawhub install juanwang
```

#### Manual

```bash
git clone https://github.com/Raven9779/juanwang-skill.git
cp -r juanwang-skill ~/.openclaw/workspace/skills/juanwang
openclaw gateway restart
```

**Or as a submodule:**

```bash
cd ~/.openclaw/workspace
git submodule add https://github.com/Raven9779/juanwang-skill.git skills/juanwang
```

## 📖 Usage

Zero config. Once installed, the overachiever mode activates automatically.

**To trigger it:**
- Just work normally — it self-drives
- It enters learning mode automatically when idle
- To disable overachiever mode: `chill` or `take it easy`
- To re-enable: `back to work` or `help me with this`

**Read more:**
- [SKILL.md](SKILL.md) — Full behavior patterns and usage guide
- [references/SOUL.md](references/SOUL.md) — The overachiever soul (must read on every wake)
- [references/learning-flow.md](references/learning-flow.md) — Active learning workflow

## 🏗️ Project Structure

```
juanwang-skill/
├── SKILL.md                    # Main skill file
├── README.md                   # This file (中文)
├── README.en.md                # English version
├── LICENSE                     # MIT
├── _meta.json                  # ClawHub metadata
└── references/
    ├── SOUL.md                 # Overachiever soul
    └── learning-flow.md        # Learning workflow
```

## 🧠 How It Works

卷王.skill works by injecting a `SOUL.md` (personality definition) and `SKILL.md` (behavior rules) into your agent's context.

Core logic:
- **Search before speaking** — Always checks memory for context before answering
- **Act before asking** — If it can be done without permission, just do it
- **Log before forgetting** — Anything useful gets written down immediately
- **Learn while idle** — No downtime, only study-time

> See [SKILL.md](SKILL.md) for the complete behavior framework.

## 🤝 Contributing

PRs welcome. Don't be the one who reads this and does nothing.

1. Fork the repo
2. Create your branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push (`git push origin feature/amazing-feature`)
5. Open a PR

## 📄 License

[MIT](LICENSE)

---

<p align="center">
  <b>It's not that you're lazy. The world is just too slow.</b>
</p>
