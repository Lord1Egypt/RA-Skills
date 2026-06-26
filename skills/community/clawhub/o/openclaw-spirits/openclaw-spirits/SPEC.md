# OpenClaw Spirits — Product Spec v1

## Overview
A companion spirit system for OpenClaw agents. Each user gets a unique spirit deterministically generated from their identity. Published as a ClawHub skill.

## 24 Spirits (Two Categories)

### Living Spirits (灵生) — 12 species
| ID | ZH | EN | Base | Trait |
|---|---|---|---|---|
| 1 | 苔猫 | Mosscat | Cat | Moss and tiny mushrooms on back |
| 2 | 墨鲤 | Inkoi | Koi fish | Body like flowing ink |
| 3 | 烬蛾 | Embermoth | Moth | Ember glow on wing edges |
| 4 | 霜兔 | Frostpaw | Rabbit | Ice crystals on ear tips |
| 5 | 铃蛙 | Bellhop | Frog | Belly is a small bell |
| 6 | 星龟 | Astortoise | Turtle | Star map on shell |
| 7 | 纸鸢 | Foldwing | Bird | Origami-like wings |
| 8 | 齿鼠 | Cogmouse | Mouse | Gear tail |
| 9 | 影鸦 | Umbracrow | Crow | Semi-transparent shadow body |
| 10 | 裂晶蛇 | Crackviper | Snake | Crystal body with glowing cracks |
| 11 | 萤菇 | Glowshroom | Mushroom | Faint bioluminescence |
| 12 | 泡水母 | Bubbloom | Jellyfish | Transparent, flower blooming inside |

### Elemental Spirits (元灵) — 12 species
| ID | ZH | EN | Form | Trait |
|---|---|---|---|---|
| 13 | 墨灵 | Inkling | Living ink drop | Shape-shifts with mood |
| 14 | 锈铃 | Rustbell | Rusty bell | Warm, husky sound |
| 15 | 苔石 | Mossrock | Mossy rock | Occasionally blinks |
| 16 | 霜齿 | Frostfang | Ice crystal fox outline | Angular, melts and reborns |
| 17 | 迴纹 | Loopwyrm | Self-biting dragon | Eternal cycle |
| 18 | 泡铃 | Bubbell | Unbreakable soap bubble | Has a tiny face inside |
| 19 | 齿轮兽 | Cogbeast | Three gears forming an animal | Self-running |
| 20 | 影子 | Umbra | Your shadow, moves on its own | Semi-independent will |
| 21 | 星沙 | Stardust | Glowing cosmic dust | Floats, curious |
| 22 | 裂纹 | Crackle | Cracked crystal with light leaking | Beauty in imperfection |
| 23 | 烛芯 | Wickling | Sentient candle | Flame sways with mood |
| 24 | 弦音 | Echochord | Floating string | Plays chords when touched |

## Rarity (5 levels)
| Level | ZH | EN | Weight | Symbol |
|---|---|---|---|---|
| 1 | 凡 | Mundane | 55% | · |
| 2 | 异 | Peculiar | 25% | ·· |
| 3 | 灵 | Spirited | 12% | ··· |
| 4 | 幻 | Phantom | 6% | ···· |
| 5 | 神 | Mythic | 2% | ····· |

## Stats (5 attributes)
| ZH | EN | Meaning |
|---|---|---|
| 直觉 | INTUITION | Sensing the essence of problems |
| 韧性 | GRIT | Persistence through difficulty |
| 灵动 | SPARK | Creativity and unexpected connections |
| 沉稳 | ANCHOR | Staying clear amid chaos |
| 锋芒 | EDGE | Sharpness of expression and humor |

## Eyes (6 styles)
◦ ◈ ✧ ● ◎ ⊙

## Accessories (unlock by rarity)
| EN | ZH | Condition |
|---|---|---|
| none | 无 | Mundane |
| bell | 小铃铛 | Peculiar+ |
| halo | 浮光环 | Spirited+ |
| starmark | 星纹额 | Spirited+ |
| thundermark | 雷纹 | Phantom+ |
| scroll | 古卷 | Phantom+ |
| crownfire | 冠火 | Mythic only |

## Generation
- Algorithm: mulberry32 PRNG + hashString (same as Claude Code, math not copyrightable)
- Input: userId or any seed string
- Output: species (1-24), rarity, eye, accessory, shiny (1%), stats
- Deterministic: same seed → same spirit, always
- Salt: "openclaw-spirit-2026"

## Commands
- `buddy` or `buddy show` — Display your spirit card
- `buddy hatch [userId]` — First-time hatching animation
- `buddy stats` — Detailed stats panel
- `buddy talk <message>` — Talk to your spirit
- `buddy rename <name>` — Rename your spirit
- `buddy reroll` — NOT supported (destiny, not choice)

## Language Support
- `--lang zh` — Chinese display (default for Feishu)
- `--lang en` — English display (default for others)
- Spirit names always show both: "苔猫 Mosscat" or just "Mosscat"
- Stats show bilingual: "直觉 INTUITION" or just "INTUITION"

## Display Format (v1 — code block)

### Chinese
```
🥚 灵兽降世！

   ~,~,~
   /\_/\
  ( ◈  ◈ )
  (  ω  )
   ") (")~

🐱 Mochi — 苔猫 Mosscat  ·· 异 PECULIAR

"背上长满苔藓的慢热小猫，等你足够安静时才会靠近"

┌──────────────────────────────┐
│ 直觉 INTUITION  ████████░░  82 │
│ 韧性 GRIT       ███░░░░░░░  33 │
│ 灵动 SPARK      █████████░  91 │
│ 沉稳 ANCHOR     ██░░░░░░░░  18 │
│ 锋芒 EDGE       █████░░░░░  52 │
└──────────────────────────────┘

🔮 灵兽与主人的灵魂绑定，不可选择，不可交易。
```

### English
```
🥚 A Spirit emerges!

   ~,~,~
   /\_/\
  ( ◈  ◈ )
  (  ω  )
   ") (")~

🐱 Mochi — Mosscat  ·· PECULIAR

"A slow-warming cat with moss on its back, who only approaches when you're quiet enough"

┌──────────────────────────────┐
│ INTUITION  ████████░░  82    │
│ GRIT       ███░░░░░░░  33    │
│ SPARK      █████████░  91    │
│ ANCHOR     ██░░░░░░░░  18    │
│ EDGE       █████░░░░░  52    │
└──────────────────────────────┘

🔮 Spirits are soul-bound. No choosing. No trading.
```

## Passive Presence (Agent Guidance in SKILL.md)
- During heartbeat: 5% chance spirit says a one-liner in its personality
- When user says hi/good morning: spirit may wave
- After long silence (>2h): spirit may say "..."
- Never during serious work or urgent tasks

## File Structure
```
openclaw-buddy/
├── SKILL.md
├── SPEC.md
├── scripts/
│   ├── generate.js    # Deterministic generation (24 species)
│   ├── render.js      # ASCII sprite rendering
│   ├── display.js     # Full card rendering (zh/en)
│   ├── soul.js        # LLM soul generation
│   └── buddy.sh       # CLI entry point
├── references/
│   └── species-guide.md
└── assets/
    └── sprites.json   # 24 species × 3 frames = 72 frames
```

## Storage
- Companion file: `{baseDir}/assets/companion.json` (inside skill directory)
- Contains: name, personality, species, rarity, eye, accessory, shiny, stats, hatchedAt, lang

## Future (v2+)
- PNG card rendering (HTML → screenshot)
- Spirit resonance (when two users have same species)
- Spirit evolution (accessories/mutations over time)
- Feishu interactive card format
