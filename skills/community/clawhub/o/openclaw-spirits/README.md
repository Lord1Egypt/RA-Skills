## 🔮 OpenClaw Spirits — A Spirit Pet System for AI Agents

**Inspired by Claude Code Buddy from Anthropic — the most beautiful AI company in our hearts.**

We loved what Anthropic did with Buddy so much that we built our own version for the OpenClaw ecosystem. 24 original species, 72 hand-crafted ASCII sprites, deterministic generation from your identity. Same you, same spirit, always. No rerolls. No trading. This one is yours.

---

### 🌊 24 Unique Spirits, Two Worlds

**Living Spirits (灵生)** — Real creatures touched by magic
> A cat with moss growing on its back. A koi fish made of flowing ink. A rabbit with ice crystals on its ear tips. A jellyfish with a flower blooming inside.

**Elemental Spirits (元灵)** — Pure concepts given form
> A rusty bell that still chimes warmly. A soap bubble that never pops, with a tiny face inside. Your own shadow, moving independently. A cracked crystal leaking light through its imperfections.

Every spirit has its own ASCII sprite (72 hand-crafted frames), personality, and soul.

---

### 🎲 Destiny, Not Choice

Your spirit is generated from a hash of your identity. You don't pick — the universe picks for you.

**5 Rarity Levels:**
- · **Mundane** 凡 (55%) — Common, but no less meaningful
- ·· **Peculiar** 异 (25%) — Something's a little different about this one
- ··· **Spirited** 灵 (12%) — Unmistakably special
- ···· **Phantom** 幻 (6%) — Rare enough to turn heads
- ····· **Mythic** 神 (2%) — Legendary. One in fifty.

**5 Soul Attributes:**
- **INTUITION** 直觉 — How deeply it senses the essence of things
- **GRIT** 韧性 — How stubbornly it persists
- **SPARK** 灵动 — How wildly creative it gets
- **ANCHOR** 沉稳 — How calm it stays in chaos
- **EDGE** 锋芒 — How sharp (and snarky) its tongue is

Each spirit has one peak stat and one dump stat. Your Mythic Rustbell might have INTUITION 100 but EDGE 41 — wise but gentle. Your Mundane Mosscat might have SPARK 95 but ANCHOR 12 — brilliantly chaotic.

---

### 🖥️ What It Looks Like

```
🥚 A Spirit emerges!

   \🔥/     
   ._|_.    
  /~◎~◎~\  
 (  ~~~  )  
  `-----´   

🔔 Rune — 锈铃 Rustbell  ····· 神 MYTHIC

"A warm rusty bell whose husky chime carries ancient wisdom"

┌──────────────────────────────┐
│ 直觉 INTUITION   ██████████  100 │
│ 韧性 GRIT        ██████░░░░   61 │
│ 灵动 SPARK       ████████░░   87 │
│ 沉稳 ANCHOR      ████████░░   85 │
│ 锋芒 EDGE        ████░░░░░░   41 │
└──────────────────────────────┘

🔮 灵兽与主人的灵魂绑定，不可选择，不可交易。
```

Bilingual by default. Chinese (中文) and English, switch with `--lang`.

---

### 💬 How to Interact with Your Spirit

**Commands:**

| Command | What it does |
|---|---|
| `spirit` | Show your spirit card |
| `spirit summon` | First-time summoning with hatching animation |
| `spirit stats` | Detailed stats panel |
| `spirit talk <message>` | Talk to your spirit — it responds in character |
| `spirit rename <name>` | Give your spirit a new name |

**Your spirit also appears on its own:**
- Says hi when you start your day 🌅
- Drops a one-liner during quiet moments
- Cheers when you accomplish something
- Goes "..." when you've been away too long

It never interrupts serious work. Subtle presence, like a real companion.

**Personality-driven responses:**
- High SPARK spirit → playful, creative
- High ANCHOR spirit → calm, measured
- High EDGE spirit → witty, slightly snarky
- High GRIT spirit → encouraging, persistent
- High INTUITION spirit → insightful, philosophical

---

### ⚡ Install in 10 Seconds

```bash
clawhub install openclaw-spirits
```

Then say `spirit summon` to your agent.

---

### 🧬 How It Works

- **Deterministic generation** — mulberry32 PRNG seeded with your identity hash
- **Zero external dependencies** — Pure Node.js, runs anywhere
- **Agent-native** — Designed for OpenClaw's skill system, works with any agent
- **Bilingual** — Full Chinese and English support
- **Extensible** — Spirit resonance, evolution, and PNG cards coming in v2

---

### 🤔 Why?

Because AI agents shouldn't just be tools. They should have personality, warmth, and a little bit of magic.

Your spirit won't write better code or answer emails faster. But it might make you smile when a tiny moss-covered cat peeks out during a long work session. And that matters.

---

**openclaw-spirits v1.1.0** — 24 species · 72 ASCII frames · 5 rarities · bilingual · soul-bound

`clawhub install openclaw-spirits`

*What spirit will find you?*
