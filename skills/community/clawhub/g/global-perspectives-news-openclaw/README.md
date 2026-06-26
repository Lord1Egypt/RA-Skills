# 🌍 Global Perspectives News — See the Elephant Whole

![Built for OpenClaw](https://img.shields.io/badge/Built%20for-OpenClaw-ff6b35?logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZD0iTTEyIDJDNi40OCAyIDIgNi40OCAyIDEyczQuNDggMTAgMTAgMTAgMTAtNC40OCAxMC0xMFMxNy41MiAyIDEyIDJ6Ii8+PC9zdmc+) ![Available on ClawHub](https://img.shields.io/badge/Available%20on-ClawHub-5c6bc0) ![Powered by Tavily](https://img.shields.io/badge/Powered%20by-Tavily%20MCP-orange) ![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey)

> *Six blind men each touched a different part of an elephant and came away with six completely different truths. None of them were wrong. None of them were complete.*
>
> *This skill is built on that idea.*

---

## What This Is

**Global Perspectives News** is an [OpenClaw](https://openclaw.ai) skill that generates personalized news digests — not from a single source, but from media across multiple countries, in the language of your choice.

The same story looks radically different depending on where you read it. A geopolitical conflict covered by US, Russian, Chinese, and Middle Eastern outlets will produce four entirely different narratives — each accurate within its own frame, each missing the others'.

Most people only access news in one or two languages, from one cultural context. That's not a failure of curiosity — it's just the reality of language barriers and information overload. This skill removes those barriers.

---

## The Idea Behind It

The inspiration is the ancient parable of the **blind men and the elephant** (盲人摸象).

Each person who touches the elephant believes they understand it. The man who touches the trunk thinks it's a rope. The man who touches the leg thinks it's a tree. They're all right. They're all wrong.

Global news works the same way. Take any major event:

| Outlet | What they call it |
|--------|-------------------|
| CNN (US) | "a humanitarian crisis" |
| TASS (Russia) | "NATO aggression" |
| Al Jazeera (Middle East) | "a failure of Western foreign policy" |
| Caixin (China) | "market and supply chain disruption" |
| Daily Maverick (Africa) | "another conflict the Global South will pay for" |
| Folha de S.Paulo (Brazil) | "a distant war with direct consequences for our food prices" |

All from the same event. All true in their own way. None of them complete.

**This skill gives you the whole elephant.**

It's designed for:
- People who want to understand the world, not just their corner of it
- Non-native speakers who can only comfortably read in one or two languages
- Anyone tired of algorithmic bubbles that only serve what you already believe
- Researchers, writers, analysts, and curious minds who want primary perspectives, not filtered summaries

You don't need to speak 10 languages. You just need to ask.

---

## What It Does

- **Asks what you care about** — from AI research to Champions League to local city news
- **Lets you choose media sources by country** — US, UK, China, Russia, Middle East, India, Africa, Latin America, and more
- **Delivers in your language** — English, Chinese, Spanish, French, Japanese, German, or bilingual
- **Structures depth by your preference** — headlines only, standard summaries, or deep analysis with "why it matters"
- **Flags when perspectives diverge** — e.g., *"US and Chinese sources frame this story very differently — see both angles below"*
- **Remembers your preferences** — save your settings to `~/.claw/data/global-perspectives-news-prefs.json` so next time it goes straight to searching

---

## How to Use

This is an [OpenClaw](https://openclaw.ai) skill. Install it via ClawHub CLI:

```bash
npx clawhub@latest install global-perspectives-news
```

Then trigger it from any connected interface (WhatsApp, Telegram, Discord, etc.) by saying:

```
/global-perspectives-news
```

Or just naturally ask your Claw:
```
Give me today's global news briefing
```

**Requirements:**
- [OpenClaw](https://openclaw.ai) set up and running
- [Tavily MCP](https://tavily.com) connected (for live web search)

**Manual installation:**
```bash
# Copy SKILL.md into your Claw skills directory
cp -r global-perspectives-news-openclaw ~/.claw/skills/global-perspectives-news/
```

---

## What It Looks Like

### Snippet 1 — Choose Your Lens

The first thing you pick is *whose eyes you want to see through*. Not a topic filter — a perspective filter.

```
Different countries cover the same story from very different angles.
Which countries' media would you like to draw from?

Official Media:
 1. United States      — CNN, NYT, WSJ, The Atlantic
 2. United Kingdom     — BBC, The Guardian, Financial Times
 3. Europe             — Der Spiegel (DE), Le Monde (FR), Kyiv Independent (UA)
 4. Russia             — RT, TASS, Kommersant (English editions)
 5. China              — SCMP, Caixin, Xinhua, Global Times (English editions)
 6. Middle East        — Al Jazeera, Arab News, Jerusalem Post, Haaretz
 7. Japan              — Nikkei Asia, Japan Times
 8. Singapore/APAC     — Straits Times, CNA
 9. India              — The Hindu, Times of India, Economic Times
10. Latin America      — Folha de S.Paulo, O Globo (Brazil + non-Hispanic LATAM)
11. Hispanic World     — Infobae, El País América (Spanish-speaking Americas + Spain)
12. Africa             — AllAfrica, Daily Maverick, The East African
13. Canada             — Globe and Mail, CBC News, Toronto Star, Maclean's
14. Australia & NZ     — ABC News Australia, Sydney Morning Herald, RNZ
15. South Korea        — Korea Herald, Chosun Ilbo (English), Hankyoreh
16. Turkey             — TRT World, Hurriyet Daily News, Daily Sabah
17. Southeast Asia     — Rappler (PH), Bangkok Post, Jakarta Post, CNA

Social Media (public sentiment):
18. Weibo              — Chinese public sentiment & trending topics (热搜榜)
19. Xiaohongshu        — Chinese lifestyle, consumer trends, Gen Z culture
20. TikTok / 抖音      — global and Chinese viral content, youth trends
21. Instagram          — visual culture, lifestyle, brand sentiment
22. Telegram           — war zones, political movements, opposition channels
23. LinkedIn           — professional sentiment, industry trends
24. Twitter/X          — global real-time reaction and trending hashtags
25. Reddit             — English-language community discussion and analysis

No filter:
26. Global / No preference — let the best sources win
```

---

### Snippet 2 — When Narratives Collide

When you select sources from different parts of the world, the briefing flags where they diverge — explicitly, without editorializing.

```
## 🌍 US-China Tariffs — March 2026

- Trump raises tariffs on Chinese goods to 145% — White House calls
  it "the strongest trade action in American history"
  Administration frames the move as protecting American manufacturing
  and forcing a reset of an "unfair" decades-long trade relationship.
  Source: WSJ

- Beijing retaliates with 125% tariffs on US goods; Ministry of
  Commerce calls Washington's move "economic bullying"
  China's state media emphasizes national resilience and frames the
  tariffs as proof that the US fears China's rise, not responds to it.
  Source: Xinhua

- Asian markets fall; supply chain rerouting already underway
  Manufacturers in Vietnam, Mexico, and India report a surge in
  inquiries as multinationals begin moving production out of China
  to avoid the tariff crossfire.
  Source: Nikkei Asia

⚠️ Note: Perspectives diverge significantly across source regions.
   US outlets frame tariffs as a long-overdue correction to trade imbalance.
   Chinese state media portrays them as protectionism masking fear of
   competition. European outlets focus on collateral damage to global
   supply chains. Indian and Southeast Asian business press sees
   opportunity — and anxiety — in being caught between two giants.
```

---

### Snippet 3 — The Same World, Your Language

A story from Caixin can arrive in Spanish. A story from Le Monde can arrive in Japanese.

```
Reading language:
  A. English
  B. Chinese 中文
  C. Spanish  Español
  D. French   Français
  E. Japanese 日本語
  F. German   Deutsch
  G. Bilingual — pick any two (e.g. "G, English + Chinese")

Depth:
  A. Headlines only  (title + one line)
  B. Standard        (title + 2-sentence summary)
  C. Deep            (title + summary + why it matters)
```

*Language stops being a wall.*

---

### Snippet 4 — Top 10 Local News, Anywhere

Ask for any city or country and get a ranked digest of what's actually happening there.

```
# 🏙️ Shanghai Today — March 2026

1. F1 Chinese Grand Prix wraps up: 230,000+ attended over 3 days
   Source: Xinhua

2. Secondary housing transactions hit 12-month high
   Source: Caixin

3. Shanghai–Ningbo cross-sea rail corridor enters national 15th Five-Year Plan
   Source: Xinhua

## Today's Takeaway
Shanghai is accelerating on two tracks: global visibility and domestic market recovery.
```

---

## Supported Languages (Output)

| Language | Code |
|----------|------|
| English | A |
| Chinese 中文 | B |
| Spanish Español | C |
| French Français | D |
| Japanese 日本語 | E |
| German Deutsch | F |
| Bilingual (any two) | G |

---

## Supported Media Sources

The skill is designed to be open-ended — the list below reflects what's built in by default, but any region, outlet, or platform can be added by editing `SKILL.md` to match your needs.

**Official Media (default):** United States · United Kingdom · Canada · Australia & NZ · Europe · Russia · Turkey · China · Japan · South Korea · Southeast Asia · Singapore/APAC · India · Middle East · Latin America · Hispanic World · Africa · and more

**Social Pulse (default):** Weibo · Xiaohongshu · TikTok/抖音 · Instagram · Telegram · LinkedIn · Twitter/X · Reddit · and more

**Want more?** Fork this repo and edit `SKILL.md` — it's plain text, no code required.

---

## Differences from the Claude Code Version

This is the **OpenClaw port** of the original [Claude Code skill](https://github.com/christinazhang139/global-perspectives-news). Changes made:

| | Claude Code | OpenClaw |
|---|---|---|
| Install | `~/.claude/skills/` | `npx clawhub@latest install global-perspectives-news` |
| Trigger | `/global-perspectives-news` in terminal | Chat message in WhatsApp/Telegram/Discord |
| Prefs saved to | `~/.claude/global-perspectives-news-prefs.json` | `~/.claw/data/global-perspectives-news-prefs.json` |
| Registry | Claude Code skill system | [ClawHub](https://clawhub.ai) |

The news logic, media sources, language options, and briefing format are identical.

---

## Philosophy

The goal is not to tell you what to think. It's to show you that multiple truths can coexist — and that understanding the world requires hearing more than one of them.

Language should not be the reason you only see part of the elephant.

---

## License

CC BY-SA 4.0 — Free to use, share, and adapt with attribution.

Original Claude Code version: [christinazhang139/global-perspectives-news](https://github.com/christinazhang139/global-perspectives-news)

---

*Built for [OpenClaw](https://openclaw.ai) · Available on [ClawHub](https://clawhub.ai) · Powered by [Tavily MCP](https://tavily.com)*
