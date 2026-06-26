# Podcast Producer — OpenClaw Skill

**Turn any podcast transcript into a complete, publish-ready content package in seconds.**

Built for podcast creators who want to stop spending hours on the content work that surrounds each episode — and start spending that time making more episodes.

---

## What it does

Feed it a transcript. Get back:

- **5 episode title options** — curiosity-driven, platform-optimised
- **Show notes** (150–300 words) — structured, SEO-aware, ready to paste
- **Chapter timestamps** — auto-detected from narrative beats
- **Social captions** — separate versions for Twitter/X and Instagram
- **SEO tags** — 15–20 keywords, comma-separated, paste-ready

Everything in one response. No back and forth.

---

## Who it's for

- True crime podcasters
- Documentary-style shows
- Interview podcasts
- Any creator who publishes transcripts

Includes a configurable **style mode** for AI-narrated shows vs human-hosted shows — so the output always sounds like *your* podcast, not a template.

---

## Installation

```bash
npx clawhub install tetsuakira-vk/podcast-producer
```

---

## Usage

Once installed, just tell your OpenClaw agent:

```
Use podcast-producer. Here's my transcript: [paste transcript]
```

Or attach a .txt or .md file:

```
Use podcast-producer with this file: [attach file]
```

The skill will ask one question — AI narrated or human hosted? — then generate the full package.

---

## Style modes

| Mode | Best for |
|------|----------|
| AI narration | TTS-optimised scripts, documentary tone, no contractions |
| Human hosted | Conversational, first person, warmer tone |

You can set your preferred mode once in your OpenClaw memory so it never asks again:

```
Remember: I use AI narration mode for podcast-producer
```

---

## Example output

**Input:** 2,000 word transcript of a true crime episode set in Japan

**Output:**
- 5 title options including *"The Girl Who Vanished from Platform 9"*
- 280-word show notes opening with the hook
- 8 chapter markers from intro to resolution
- Twitter caption with 3 hashtags
- Instagram caption with 14 tags
- 18 SEO keywords including location and case-specific terms

---

## Requirements

- OpenClaw installed and running
- Any supported LLM (Claude, GPT-4, DeepSeek all work well)
- A transcript — plain text, .txt, or .md

No API keys, no external services, no setup beyond installation.

---

## Tips

- Longer transcripts (1,500+ words) produce better chapter timestamps
- If your transcript has natural scene breaks, mark them with `---` and the skill will use them as chapter cues
- Save your style preference in OpenClaw memory to skip the setup question on every run

---

## Licence

MIT — free to use, modify, and build on.

---

## Feedback & issues

Found a bug or want a feature? Open an issue on GitHub. This skill is actively maintained.
