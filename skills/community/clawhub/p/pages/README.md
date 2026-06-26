# Pages 📖

> *The books that shaped you are part of how you think. Your agent should know them too.*

**Pages** is an open-source agent skill that turns your reading life into a private, searchable intelligence layer — kept on your machine, owned by you.

No Goodreads. No reading app. Just files and your AI agent.

---

## What it does

- **Logs books** — one markdown file per book, organized by reading status
- **Captures quotes** — the lines worth keeping, stored with the book
- **Surfaces context** — "what have I read about decision-making?" finds the right book at the right moment
- **Tracks recommendations** — who told you to read what, linked to your Peeps network
- **Connects your reading** — noticing when a book is relevant to a conversation, a person, or a decision

```
pages/
  read/
    kahneman-thinking-fast-and-slow.md
    fitzpatrick-the-mom-test.md
  reading/
    taleb-antifragile.md
  want/
    newport-deep-work.md
```

---

## Install

### Claude Code

```bash
mkdir -p ~/.claude/skills/pages
curl -o ~/.claude/skills/pages/SKILL.md https://raw.githubusercontent.com/haah-ing/pages-skill/main/SKILL.md
```

### Other agents

```bash
npx skills add haah-ing/pages-skill
```

Works with OpenClaw, Cursor, and any agent that supports the skills ecosystem.

### Hermes

```bash
hermes skills install pages
```

---

## Then just talk

```
"Just finished Thinking, Fast and Slow — 4 stars, the System 2 framing really stuck with me."
"What have I read about decision-making under pressure?"
"Wei Lin said I should read The Mom Test."
"Save this quote from Antifragile: 'Wind extinguishes a candle and energizes fire.'"
"What books do I have on my want list?"
```

Each book file looks like this:

```markdown
# Thinking, Fast and Slow

- **Author:** Daniel Kahneman
- **Year:** 2011
- **Status:** read
- **Finished:** 3 Apr 2026
- **Rating:** 4/5
- **Tags:** #psychology #decision-making #bias
- **Recommended by:** [[wei-lin]]

## Notes

3 Apr 2026: most of my bad decisions happen when I'm tired and System 2 is offline

## Quotes

> "A reliable way to make people believe in falsehoods is frequent repetition, because familiarity is not easily distinguished from truth."
> — p. 62
```

---

## Works best with

Pages is part of a suite of personal intelligence skills:

- [**Haah** 🪩](https://github.com/haah-ing/haah-skill) — dispatch to your trusted circles. When your reading list is thin on a topic, Haah can ask your network what they've been reading.
- [**Peeps** 👥](https://github.com/haah-ing/peeps-skill) — your personal network. When someone recommends a book, Pages links it to their Peeps file. Your agent can surface it the next time their name comes up.
- [**Vibes** 🎧](https://github.com/haah-ing/vibes-skill) — albums, shows, podcasts, films, YouTube channels. The cultural sibling to Pages — some ideas start as a book and finish as a film.
- [**Nooks** 📍](https://github.com/haah-ing/nooks-skill) — your saved places. A good reading nook is where pages get finished.
- [**Digs** 🔭](https://github.com/haah-ing/digs-skill) — your active research threads. Books relevant to an open dig surface automatically as a source.

Install all six and your agent knows your people, your places, your reads, your culture, and your open questions.

---

## Contributing

The skill lives in `SKILL.md` — that's the brain. Edit it, improve it, make it yours. PRs welcome.

---

## License

MIT. Take it, fork it, build on it.

---

*Designed by Ilya Belikin @ Haah Inc*
