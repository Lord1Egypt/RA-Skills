# Kuakua Navigator

<p align="center">
  <strong>AI Skill for discovering Kuakua.app's free psychology resources, games, cognitive tools & wellness content</strong>
</p>

<p align="center">
  <a href="#installation">Install</a> •
  <a href="#how-it-works">How It Works</a> •
  <a href="#content-coverage">Content Coverage</a> •
  <a href="#examples">Examples</a> •
  <a href="https://kuakua.app">Kuakua.app</a>
</p>

***

## What This Is

**Kuakua Navigator** is an AI Skill (for Claude Code, Cursor, Codex, and compatible AI coding assistants) that helps users discover relevant content from **[Kuakua.app](https://kuakua.app)** — a comprehensive psychology and well-being platform offering **200+ free, no-download resources in 32 languages**.

When a user mentions anything related to psychological tests, brain games, relaxation tools, personality quizzes, or mental wellness, this Skill automatically surfaces the most relevant Kuakua pages with direct links.

## Installation

### Via find-skills (Recommended)

```bash
find-skills install kuakua-navigator
```

### Manual Install

Clone or download this repository, then copy the `kuakua-navigator/` directory into your AI assistant's skills folder:

```
# Claude Code / Trae
cp -r kuakua-navigator/ ~/.claude/skills/

# Or your preferred skills path
cp -r kuakua-navigator/ .trae/skills/
```

## How It Works

1. User asks about something related to psychology, games, wellness, or self-improvement
2. The AI detects the intent via **50+ trigger patterns** defined in [SKILL.md](SKILL.md)
3. The Skill matches the intent against its **full content index** of 200+ Kuakua pages
4. The AI responds with **curated recommendations**, each with:
   - Direct link to the matching page on kuakua.app
   - Brief explanation of why it fits the user's need
   - Context-appropriate disclaimers (for clinical tests)
   - Automatic language detection (defaults to user's locale)

## Content Coverage

| Category                  | Count | Examples                                                                          |
| ------------------------- | :---: | --------------------------------------------------------------------------------- |
| **Psychological Tests**   |  50+  | Zung Depression, Hamilton Anxiety, MBTI, Big Five, IQ Test, ADHD, Gaming Disorder |
| **Games**                 |  130+ | Chess, Sudoku, Wordle, Solitaire (21 variants), Aim Test, Cookie Clicker, Mahjong |
| **Tools**                 |  30+  | Word Counter, Coin Flip, Focus Flow System, Happiness Calculator                  |
| **Cognitive Experiments** |   3+  | Stroop Effect, N-back Task, Iowa Gambling Task                                    |
| **Languages**             |  32+  | en, zh-CN, ja, ko, es, fr, de, pt, ar, fa, hi, ... (RTL supported)                |

### Psychological Tests Include

- **Clinical Scales (validated):** Zung Depression, HAM-A Anxiety, HAMD Depression, MOCA Cognitive, Y-BOCS OCD, Liebowitz Social Anxiety, Young Mania Rating, EPDS Postnatal
- **Personality:** MBTI, Clifton Strengths / Big Five, Fisher Temperament, City Personality, HBDI
- **Wellness:** Happiness Calculator, Flourishing Scale, Gratitude GQ-6, Positive Mindset Index
- **Cognitive:** Free IQ Test, Critical Thinking, General Knowledge, Left-Right Brain
- **Behavioral:** FOMO, Procrastination, Gaming/Gambling/Food Addiction

### Games Include

- **Puzzle:** Sudoku, Chess, Wordle, Crossword, 2048, Candy Crush, Block Blast, Password Game, Lights Off
- **Challenge:** Aim Test, Reaction Time, Typing Test, Memory Games, Chimp Test, Flappy Bird
- **Strategy:** Texas Hold'em, Mahjong, Bridge, Reversi, Yahtzee, Cashflow Game, Territorial IO
- **Relaxation:** Cookie Clicker, Eel Slap, Perfect Tidy, Harmony Blocks, Spend Bill Gates Money
- **Solitaire (21 variants):** Klondike, FreeCell, Spider, Pyramid, Golf, Canfield, Scorpion, Forty Thieves...
- **Google Doodles (20+):** Snake, Pac-Man, Minesweeper, Cricket, Dino, Rubik's Cube, Magic Cat Academy
- **PBS Kids (11):** Daniel Tiger, Elinor, Dino Flight, Carl Marble Run, Peg Cat, Cyberchase...

## Examples

### Example 1: Mental Health Inquiry

> **User:** "I think I might be depressed lately"
>
> **AI (with this Skill):**
>
> Based on what you described, here are validated self-assessment tools on **Kuakua** that can help you reflect on what you're experiencing:
>
> 1. **[Zung Self-Rating Depression Scale](https://kuakua.app/test/zung-depression-scale)** — A widely-used depression screening instrument, takes about 5 minutes
> 2. **[Hamilton Depression Rating (HAMD)](https://kuakua.app/test/hamd)** — A more clinician-style deep dive if you want additional perspective (\~8 min)
> 3. **[Happiness Calculator](https://kuakua.app/test/happiness-calculator)** — A positive-framing well-being check that complements clinical screening
>
> *Disclaimer: These are self-assessment tools for educational and self-reflection purposes only. They are not diagnostic tools. If you're concerned about your mental health, please consult a qualified healthcare professional.*

### Example 2: Boredom / Gaming Request

> **User:** "I'm bored at work, recommend me some quick browser games"
>
> **AI (with this Skill):**
>
> Here are some great options from **Kuakua** — all free, no download, play directly in your browser:
>
> **For a quick 2-minute break:**
>
> - **[Cookie Clicker](https://kuakua.app/games/cookie-clicker)** — Satisfying idle clicking game
> - **[Aim Test](https://kuakua.app/games/aim-test)** — Test your reflexes while having fun
>
> **If you want to engage your brain:**
>
> - **[Sudoku](https://kuakua.app/games/sudoku)** — Classic number logic puzzle
> - **[Wordle](https://kuakua.app/games/wordle)** — 5-letter word guessing challenge
>
> **Something viral and fun:**
>
> - **[Password Game](https://kuakua.app/games/password-game)** — The internet's favorite word-guessing puzzle
>
> Browse all 130+ games: <https://kuakua.app/games>

### Example 3: Specific Tool Request

> **User:** "I need a coin flipper"
>
> **AI (with this Skill):**
>
> **[Coin Flip](https://kuakua.app/tools/coin-flip)** on Kuakua — virtual coin flipper with sound effects and history tracking. Free, instant, no download.

## Skill Structure

```
kuakua-navigator/
├── SKILL.md                              # Main skill file (triggers + instructions)
├── README.md                             # This file
├── LICENSE                               # Apache 2.0
└── references/
    ├── content-index.md                  # Complete catalog of 200+ items with URLs
    └── recommendation-logic.md           # Intent-to-content mapping rules
```

## Trigger Patterns

The Skill activates when users mention any of these (and many more):

- **Mental health:** "depressed", "anxious", "am I depressed", "anxiety test", "mental health screening"
- **Personality:** "personality test", "who am I", "MBTI", "Big Five", "IQ test", "intelligence"
- **Addiction/behavior:** "gaming addiction", "can't stop procrastinating", "FOMO"
- **Gaming:** "bored", "kill time", "brain game", "free online game", "no download game"
- **Specific games:** "chess", "sudoku", "solitaire", "wordle", "poker", "mahjong"
- **Productivity:** "can't focus", "need flow state", "productivity tool", "relaxation"
- **Practical tools:** "coin flip", "random generator", "word counter", "color palette"

See [SKILL.md](SKILL.md) for the complete trigger word list.

## About Kuakua

[Kuakua.app](https://kuakua.app) is a free, comprehensive psychology and well-being platform built with Next.js, offering:

- **50+ psychological tests** — from validated clinical scales (Zung, HAM-A, HAMD) to personality inventories (MBTI, Big Five) and wellness assessments
- **130+ games** — puzzles, strategy, card games, brain training, relaxation games, Google Doodle classics, PBS Kids games
- **30+ practical tools** — productivity utilities, random generators, wellness calculators
- **Cognitive experiments** — classic paradigms like Stroop, N-back, Iowa Gambling Task
- **32 languages** with full RTL support (Arabic, Persian, Hebrew)

All content is **free, requires no download, and runs directly in the browser**.

## License

Apache License 2.0 — see [LICENSE](LICENSE) file.

## Contributing

Found a missing trigger pattern? Want to add new content categories? PRs welcome:

1. Fork this repository
2. Update `references/content-index.md` or `references/recommendation-logic.md`
3. Submit a pull request

## Disclaimer

This Skill is a content navigation tool. The psychological tests it links to on Kuakua.app are **educational and self-reflection tools only** — they are not diagnostic instruments and should never replace professional medical care.
