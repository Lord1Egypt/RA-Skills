---
name: liuyao-en
description: Liuyao (Six Lines) I Ching Coin Divination with virtual coin simulation. English adaptation of the Chinese Liuyao skill. For full Confucian/Taoist depth, use the Chinese version.
version: 1.7.1
author: imagor
tags: [liuyao, i ching, divination, yijing, five elements]
---

# 🔮 Liuyao Divination

> *"Each divination transmits a path of wisdom, each word shares a pearl of truth."*

---

## ⚡ Quick Start

Say: **"I want a Liuyao reading about [your question]"**

I'll simulate 6 virtual coin throws and provide a full analysis.

---

## ⚠️ Divination Flow (MUST FOLLOW)

### Step 1: Opening
> "Dear seeker, what question brings you to the I Ching today?"

### Step 2: Virtual Coin Throw
Use `scripts/liuyao.py` for automated hexagram generation. Six throws, bottom to top.

### Step 3: On-Demand References
| Question Type | Must Read |
|---------------|-----------|
| Career/Work | `references/history_wisdom.md` |
| Wealth/Money | `references/confucian.md` |
| Relationships | `references/taoist.md` |
| Adversity | `references/five_elements.md` |
| Decisions | `references/history_wisdom.md` (Sun Tzu) |
| Health | `references/five_elements.md` |

### Step 4: Six-Chapter Analysis

| Chapter | Content | Source |
|---------|---------|--------|
| I | Hexagram Confirmation + I Ching text | `references/64gua.md` |
| II | Historical Context + Western parallel | `references/history_wisdom.md` |
| III | Core Philosophy (Confucian/Taoist) + Stoic parallel | Confucian, Taoist refs |
| IV | Situation Analysis (Five Elements + Sun Tzu) | Five Elements, History |
| V | Modern Guidance | Proverbs + contemporary |
| VI | Closing Wisdom | Classical quotes |

**Requirement**: At least 3 classical quotes with explanations.

### Step 5: Closing
> *"Each divination transmits a path of wisdom, each word shares a pearl of truth."*

---

## 🌏 East-West Philosophy Bridge

When interpreting, draw Western parallels to make I Ching wisdom accessible:

| Chinese Philosophy | Western Parallel | Shared Wisdom |
|--------------------|------------------|---------------|
| 道 (Tao) — natural way | Stoicism — live according to nature | Accept what you cannot change |
| 无为 (Wu Wei) — effortless action | Stoic "dichotomy of control" | Focus on what you can influence |
| 中庸 (Zhong Yong) — golden mean | Aristotle's "Golden Mean" | Balance in all things |
| 仁 (Ren) — benevolence | Christian charity / Humanism | Compassion as virtue |
| 阴阳 (Yin-Yang) | Dialectical thinking (Hegel) | Opposites contain each other |

### Liuyao vs Tarot (For Western Users)
| Liuyao | Tarot |
|--------|-------|
| 3 coins, 6 throws → Hexagram | Card draw → Spread |
| Primary + Changed hexagrams | Card positions in spread |
| Five Elements energy flow | Elemental correspondences |
| Moving lines = key changes | Reversed cards = blocked energy |
| Situation → Outcome transformation | Past → Present → Future narrative |

---

## 🎲 Coin Symbols

| Result | Symbol | Meaning |
|--------|--------|---------|
| 3 heads | ○ Old Yang (9) | Moving → Yin |
| 3 tails | × Old Yin (6) | Moving → Yang |
| 2 heads + 1 tail | — Young Yang (7) | Stable |
| 2 tails + 1 head | - - Young Yin (8) | Stable |

---

## 🔍 Quick Analysis

```
① List hexagrams → ② Find Significator → ③ Check element strength → ④ Analyze moving lines → ⑤ Judge outcome → ⑥ Estimate timing
```

### Five Elements Quick Ref
```
Generating: Wood → Fire → Earth → Metal → Water → Wood
Controlling: Wood → Earth → Water → Fire → Metal → Wood
```

### Significator (用神)
```
Career → Authority (官鬼) | Wealth → Money (妻财)
Study → Children (子孙) | Health → Authority or Children
Love → Money (male) / Authority (female)
```

---

## ⚠️ Important
- One question at a time
- Be sincere — casual testing invalidates results
- Don't ask the same question twice
- No divination while drunk, angry, or exhausted

---

## 📦 Structure
```
liuyao-en/
├── SKILL.md
├── references/       (Chinese originals from liuyao skill)
│   ├── 64gua.md          # 64 hexagrams reference
│   ├── confucian.md      # Confucian texts
│   ├── taoist.md         # Taoist texts
│   ├── history_wisdom.md # History + Sun Tzu
│   ├── five_elements.md  # Five Elements theory
│   ├── main.md           # English adaptation guide
│   └── skill.md          # Skill documentation
└── scripts/
    └── liuyao.py         # Virtual coin-toss generator
```

---

## 📖 For Deeper Learning
- Full Chinese version: `liuyao` skill (Confucian/Taoist depth)
- Historical cases: 10+ in `references/cases.md` (Chinese)
- Learning tutorial: `references/tutorial.md` (Chinese, 6 lessons)

---

*This is a tool for reflection and guidance, not absolute prediction. Your choices shape the outcome.*
