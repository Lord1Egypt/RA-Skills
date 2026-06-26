---
name: loot-drop
version: 1.0.0
description: >
  RPG-style loot drops for completing real coding tasks. Fix a bug? Random
  loot drop with stats. Ship a feature? Epic gear. Survive a production
  incident? Legendary weapon. Collect items, build your inventory, equip
  your developer loadout. Because every quest deserves treasure.
author: J. DeVere Cooley
category: fun-tools
tags:
  - gamification
  - rpg
  - rewards
  - motivation
metadata:
  openclaw:
    emoji: "💎"
    os: ["darwin", "linux", "win32"]
    cost: free
    requires_api: false
    tags:
      - zero-dependency
      - fun
      - gamification
---

# Loot Drop

> "In RPGs, every defeated enemy drops something. In software, every defeated bug should too."

## What It Does

Complete a task. Get loot. Every commit, bug fix, feature ship, and code review earns a random loot drop — a virtual item with randomized stats, rarity tiers, and flavor text pulled from the actual work you just completed.

It's a **randomized reward system** that makes the dopamine loop of coding visible and collectible.

## The Loot Table

### Rarity Tiers

| Tier | Color | Drop Rate | Trigger |
|---|---|---|---|
| ⬜ **Common** | Gray | 60% | Any commit |
| 🟢 **Uncommon** | Green | 25% | Bug fix, test added |
| 🔵 **Rare** | Blue | 10% | Feature shipped, review completed |
| 🟣 **Epic** | Purple | 4% | Major refactor, release tagged |
| 🟡 **Legendary** | Gold | 0.9% | Production incident survived, major milestone |
| 🔴 **Mythic** | Red | 0.1% | Extraordinary feats (secret triggers) |

### Item Categories

**Weapons** (Offensive coding tools)
```
⚔️  Swords    — Bug-killing implements
🏹  Bows      — Long-range debugging tools
🪄  Wands     — Refactoring instruments
🔨  Hammers   — Performance optimization tools
🗡️  Daggers   — One-liner fix specialists
```

**Armor** (Defensive coding gear)
```
🛡️  Shields   — Error handling protection
🧥  Chestplate — Test coverage armor
👢  Boots     — Migration speed boosters
🪖  Helmets   — Code review resistance
🧤  Gloves    — Typing speed enhancers
```

**Accessories** (Utility items)
```
💍  Rings     — Focus and concentration
📿  Amulets   — Luck and rare drop bonuses
📜  Scrolls   — Knowledge and documentation
🧪  Potions   — Quick fixes and patches
🔮  Orbs      — Prediction and planning tools
```

## Loot Drop Examples

### Common Drop ⬜

```
╔══════════════════════════════════════════════════════════════╗
║  💎 LOOT DROP!                                               ║
║  Triggered by: commit "update button styles"                 ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  ⬜ COMMON                                                   ║
║                                                              ║
║  🧤 Gloves of Minor Formatting                               ║
║  ──────────────────────────                                  ║
║  +2 CSS Proficiency                                          ║
║  +1 Pixel Precision                                          ║
║                                                              ║
║  "Worn by developers who understand that padding             ║
║   is not the same as margin. Barely."                        ║
║                                                              ║
║  ⌐■-■  Equip?  [Y/N]                                        ║
╚══════════════════════════════════════════════════════════════╝
```

### Uncommon Drop 🟢

```
╔══════════════════════════════════════════════════════════════╗
║  💎 LOOT DROP!                                               ║
║  Triggered by: commit "fix: race condition in session cache" ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  🟢 UNCOMMON                                                 ║
║                                                              ║
║  ⚔️ Blade of Synchronization                                 ║
║  ──────────────────────────                                  ║
║  +8 Concurrency Awareness                                    ║
║  +5 Race Condition Detection                                 ║
║  +3 Mutex Wielding                                           ║
║                                                              ║
║  Special: "Thread-Safe Strike"                               ║
║  — Your next concurrent code review catches 2x more issues   ║
║                                                              ║
║  "Forged in the fires of a production deadlock at 3am.       ║
║   Its edge is sharp enough to split a nanosecond."           ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### Rare Drop 🔵

```
╔══════════════════════════════════════════════════════════════╗
║  💎 LOOT DROP!                                               ║
║  Triggered by: Feature "multi-currency checkout" shipped     ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  🔵 RARE                                                     ║
║                                                              ║
║  🧥 Chestplate of International Commerce                     ║
║  ──────────────────────────────────────                      ║
║  +15 Currency Handling                                       ║
║  +12 Decimal Precision                                       ║
║  +8  Timezone Resistance                                     ║
║  +5  Localization Mastery                                    ║
║                                                              ║
║  Set Bonus (2/4 "Global Developer" set):                     ║
║  — Immune to floating point rounding errors                  ║
║                                                              ║
║  "Stitched from the tears of developers who learned          ║
║   that JPY doesn't have cents. The hard way."               ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### Epic Drop 🟣

```
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║  ✨💎 EPIC LOOT DROP! 💎✨                                     ║
║  Triggered by: Tagged release v2.0.0                        ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  🟣 EPIC                                                     ║
║                                                              ║
║  🪄 Staff of the Full Rewrite                                ║
║  ──────────────────────────────                              ║
║  +25 Architecture Vision                                     ║
║  +20 Refactoring Power                                       ║
║  +18 Test Coverage Generation                                ║
║  +15 Breaking Change Management                              ║
║  +10 Team Leadership                                         ║
║                                                              ║
║  Special: "Phoenix Protocol"                                 ║
║  — Once per sprint, completely rewrite a module with         ║
║    zero regression bugs                                      ║
║                                                              ║
║  "Only awarded to those who have survived a major version    ║
║   release. The staff remembers every merge conflict,         ║
║   every failed pipeline, every moment of doubt.              ║
║   And it chose YOU."                                         ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### Legendary Drop 🟡

```
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║  ⚡🌟💎 LEGENDARY LOOT DROP! 💎🌟⚡                             ║
║  Triggered by: Survived Incident INC-5000 (P0, 3am)        ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  🟡 LEGENDARY                                                ║
║                                                              ║
║  🛡️ Shield of the Night Watch                                ║
║  ──────────────────────────────                              ║
║  +40 Incident Response                                       ║
║  +35 Calm Under Pressure                                     ║
║  +30 Root Cause Analysis                                     ║
║  +25 Production Debugging                                    ║
║  +20 Stakeholder Communication                               ║
║                                                              ║
║  Special: "3am Clarity"                                      ║
║  — When activated during an incident, immediately reveals    ║
║    the most likely root cause. 24-hour cooldown.             ║
║                                                              ║
║  Passive: "Pager Immunity"                                   ║
║  — +50% resistance to pager anxiety for 48 hours             ║
║                                                              ║
║  "This shield was not forged. It was earned — in the dark,   ║
║   in production, when everything was on fire and the only    ║
║   thing between catastrophe and resolution was you,          ║
║   a laptop, and a very large coffee."                        ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

## Developer Inventory

```
╔══════════════════════════════════════════════════════════════╗
║                  🎒 YOUR INVENTORY                           ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  EQUIPPED:                                                   ║
║  ├── ⚔️ Blade of Synchronization [🟢 Uncommon]               ║
║  ├── 🧥 Chestplate of International Commerce [🔵 Rare]       ║
║  ├── 👢 Boots of Quick Deployment [🟢 Uncommon]              ║
║  ├── 🪖 Helm of Code Review [⬜ Common]                      ║
║  └── 💍 Ring of Focused Debugging [🔵 Rare]                  ║
║                                                              ║
║  TOTAL STATS:                                                ║
║  ├── Bug Slaying: +34                                        ║
║  ├── Code Quality: +28                                       ║
║  ├── Performance: +15                                        ║
║  ├── Debugging: +22                                          ║
║  └── Architecture: +12                                       ║
║                                                              ║
║  COLLECTION: 47 items (3🟡 5🟣 12🔵 15🟢 12⬜)               ║
║  RAREST: 🟡 Shield of the Night Watch                        ║
║                                                              ║
║  SETS IN PROGRESS:                                           ║
║  ├── "Global Developer" — 2/4 pieces (need boots + helm)     ║
║  ├── "The Debugger" — 3/5 pieces (need weapon + amulet)      ║
║  └── "Full Stack" — 1/6 pieces (long way to go)              ║
╚══════════════════════════════════════════════════════════════╝
```

## When to Invoke

- Runs automatically on qualifying events (commits, releases, incidents)
- Check inventory anytime for a morale boost
- Compare collections with teammates (friendly competition)
- Equip your loadout before a big coding session (for vibes)

## Why It Matters

Coding rewards are invisible and delayed. The satisfaction of shipping a feature comes days or weeks after the work. The satisfaction of fixing a bug is gone by the time the PR merges. Loot Drop provides **immediate, tangible, collectible rewards** for real work — making the feedback loop tighter and more fun.

Plus, a Legendary loot drop at 3am during an incident? That actually makes the pager sting a little less.

Zero external dependencies. Zero API calls. Pure randomized joy.
