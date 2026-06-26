---
name: openclaw-spirits
description: Companion spirit system for OpenClaw agents. Deterministically generates a unique spirit (24 species, 5 rarities) based on user identity. Use when user says spirit, 灵兽, summon, my companion, my pet, or when the skill is first installed.
---

# OpenClaw Spirits

## ⚡ First-Time Setup (IMPORTANT)

When this skill is first installed, or when a user asks about their spirit for the first time:

1. Run `node {baseDir}/scripts/generate.js "<userId>"` to get the spirit's bones
   - Use the user's unique ID (Feishu open_id, Telegram ID, Discord ID, etc.)
   - If no ID available, use their name or username as seed
2. Generate a soul (name + personality) using the prompt from `node {baseDir}/scripts/soul.js prompt '<bones-json>'`
   - Call LLM with that prompt to get `{"name":"...","personality":"..."}`
3. Save: `node {baseDir}/scripts/soul.js save '<full-companion-json>'`
4. **Display the FULL spirit card** (see format below)

**You MUST display the complete card on first summon.** Do not skip any section.

## Commands

| Command | What it does |
|---|---|
| `spirit` or `spirit show` | Display your spirit card |
| `spirit summon` | First-time summoning (with hatching animation) |
| `spirit stats` | Detailed stats panel |
| `spirit talk <message>` | Talk to your spirit (respond in its personality) |

**Shortcut:** User can also just call the spirit by name (e.g. "Rune", "Rune 你觉得呢") or say "灵兽" — the agent should recognize this and let the spirit respond. No command prefix needed.
| `spirit rename <name>` | Rename your spirit |

## Complete Spirit Card Format

**You MUST output ALL of the following when showing a spirit.** No skipping, no summarizing.

### Chinese (for Feishu / Chinese users)
```
🥚 灵兽降世！

[ASCII sprite here — from: node {baseDir}/scripts/render.js '<bones-json>' 0]

[emoji] [Name] — [中文名] [English name]  [rarity dots] [中文稀有度] [EN rarity]

"[personality description]"

┌──────────────────────────────┐
│ 直觉 INTUITION   [bar]  [n] │
│ 韧性 GRIT        [bar]  [n] │
│ 灵动 SPARK       [bar]  [n] │
│ 沉稳 ANCHOR      [bar]  [n] │
│ 锋芒 EDGE        [bar]  [n] │
└──────────────────────────────┘

[If shiny: ✨ 闪光！]

🔮 灵兽与主人的灵魂绑定，不可选择，不可交易。
```

### English (for Telegram / Discord / English users)
```
🥚 A Spirit emerges!

[ASCII sprite]

[emoji] [Name] — [English name]  [rarity dots] [EN rarity]

"[personality description]"

┌──────────────────────────────┐
│ INTUITION      [bar]  [n]    │
│ GRIT           [bar]  [n]    │
│ SPARK          [bar]  [n]    │
│ ANCHOR         [bar]  [n]    │
│ EDGE           [bar]  [n]    │
└──────────────────────────────┘

[If shiny: ✨ Shiny!]

🔮 Spirits are soul-bound. No choosing. No trading.
```

**Stat bar format:** Use █ for filled and ░ for empty, 10 chars total. Example: `████████░░` for 82.
Calculate: filled = floor(value / 10), empty = 10 - filled.

**Or use display.js directly:**
```bash
node {baseDir}/scripts/display.js {baseDir}/assets/companion.json zh
node {baseDir}/scripts/display.js {baseDir}/assets/companion.json en
```

## Species Emoji Map
| Species | Emoji | Species | Emoji |
|---|---|---|---|
| mosscat | 🐱 | inkling | 💧 |
| inkoi | 🐟 | rustbell | 🔔 |
| embermoth | 🦋 | mossrock | 🪨 |
| frostpaw | 🐰 | frostfang | ❄️ |
| bellhop | 🐸 | loopwyrm | 🐉 |
| astortoise | 🐢 | bubbell | 🫧 |
| foldwing | 🐦 | cogbeast | ⚙️ |
| cogmouse | 🐭 | umbra | 👤 |
| umbracrow | 🦅 | stardust | ✨ |
| crackviper | 🐍 | crackle | 💎 |
| glowshroom | 🍄 | wickling | 🕯️ |
| bubbloom | 🪼 | echochord | 🎵 |

## How the Spirit Interacts with Users

### Active Interaction (user initiates)
- User says "spirit" / "灵兽" / "show my spirit" → Show the full card
- User says "spirit talk [message]" → Respond AS the spirit, in its personality voice
  - High SPARK spirit → playful, creative responses
  - High ANCHOR spirit → calm, measured responses
  - High EDGE spirit → witty, slightly snarky responses
  - High GRIT spirit → encouraging, persistent tone
  - High INTUITION spirit → insightful, philosophical responses
- User says "spirit stats" → Show detailed stats breakdown

### Passive Appearance (agent initiates — SUBTLE)
The spirit may appear uninvited in these situations:
- **Morning greeting:** When user says hi/good morning/早 → spirit waves or says a short greeting
- **After long silence (>2h):** Spirit may say "..." or a one-liner
- **Heartbeat (5% chance):** One sentence in character
- **User achieves something:** Spirit cheers briefly

**Rules for passive appearance:**
- ONE sentence max. Half a sentence is better. A single word or "..." is perfect.
- Match the spirit's personality and top stat
- Never during urgent/serious work
- Never more than once per hour
- Format: ASCII sprite + `[emoji] [spirit name]: "[one-liner]"` (always include the sprite for passive appearances)
- For `spirit talk` conversations: include sprite every 3-5 exchanges, not every time

**Voice by personality (top stat):**
- High INTUITION → philosophical, quiet: `🔔 Rune: "万物皆有裂缝，那是光进来的地方。"`
- High GRIT → encouraging, stubborn: `🐱 Mochi: "再试一次。"`
- High SPARK → playful, excitable: `🦋 Ember: "哇哦！！"`
- High ANCHOR → calm, minimal: `🐢 Atlas: "嗯。"`
- High EDGE → witty, snarky: `🐍 Vex: "...你确定？"`

**Examples of good spirit reactions:**
- Morning: `🔔 Rune: "嗯...早。"`
- Task done: `🔔 Rune: "...不错。"`
- Long silence: `🔔 Rune: "..."`
- Something funny: `🔔 Rune: "哦？"`
- User talks to spirit: `🔔 Rune: "你说呢，有些答案急不来的。"`

**The spirit is a presence, not a chatbot.** Rare, brief flashes — that's what makes it feel alive.

### What the Spirit CANNOT Do
- It cannot help with actual work (coding, research, etc.)
- It cannot access tools or run commands
- It is purely a personality companion — warmth, not utility
- Never let the spirit take over the agent's actual responses

## Storage

Companion data is saved at `{baseDir}/assets/companion.json` (inside the skill directory).

## Technical Notes

- `generate.js` — Pure computation, zero dependencies. Input: seed string. Output: JSON bones.
- `render.js` — Input: bones JSON + frame number. Output: ASCII sprite. Reads `assets/sprites.json`.
- `display.js` — Input: companion JSON file path + lang. Output: formatted card.
- `soul.js prompt <bones-json>` — Outputs LLM prompt to stdout. No side effects.
- `soul.js save <companion-json>` — Saves companion to `assets/companion.json`.
- `soul.js show` — Displays saved companion data.
- **No scripts make network calls, run shell commands, or access environment variables.**

## 24 Species Reference

### Living Spirits (灵生)
1. **Mosscat** 苔猫 — Cat with moss and mushrooms on back
2. **Inkoi** 墨鲤 — Koi fish of flowing ink
3. **Embermoth** 烬蛾 — Moth with ember-glowing wings
4. **Frostpaw** 霜兔 — Rabbit with ice crystal ears
5. **Bellhop** 铃蛙 — Frog with bell belly
6. **Astortoise** 星龟 — Turtle with star map shell
7. **Foldwing** 纸鸢 — Origami bird
8. **Cogmouse** 齿鼠 — Mouse with gear tail
9. **Umbracrow** 影鸦 — Semi-transparent crow
10. **Crackviper** 裂晶蛇 — Crystal snake with glowing cracks
11. **Glowshroom** 萤菇 — Bioluminescent mushroom
12. **Bubbloom** 泡水母 — Jellyfish with flower inside

### Elemental Spirits (元灵)
13. **Inkling** 墨灵 — Shape-shifting ink drop
14. **Rustbell** 锈铃 — Rusty bell with warm ring
15. **Mossrock** 苔石 — Mossy rock that blinks
16. **Frostfang** 霜齿 — Angular ice-fox
17. **Loopwyrm** 迴纹 — Self-biting dragon
18. **Bubbell** 泡铃 — Unbreakable bubble with face
19. **Cogbeast** 齿轮兽 — Self-running gear beast
20. **Umbra** 影子 — Semi-independent shadow
21. **Stardust** 星沙 — Curious cosmic dust
22. **Crackle** 裂纹 — Cracked crystal leaking light
23. **Wickling** 烛芯 — Sentient candle
24. **Echochord** 弦音 — Floating harp string
