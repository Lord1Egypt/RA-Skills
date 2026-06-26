# 运势 (YunShi)

> 私人命理顾问 — 每日运程推送 · 八字紫微 · 占卜风水

An [OpenClaw](https://openclaw.ai) skill that brings traditional Chinese astrology into your chat. Covers BaZi (Four Pillars), ZiWei DouShu, QiMen DunJia, I Ching divination, marriage compatibility, and feng shui — with built-in algorithms and no external API dependencies.

---

## Features

### Chart Reading

| Feature | Trigger |
|---------|---------|
| BaZi (Four Pillars, Day Master, Useful God, Spirits) | `八字 1990-05-15 14:30` |
| ZiWei DouShu (Life Palace, 12 Palaces, Four Transformations) | `紫微 1990-05-15 男` |
| QiMen DunJia | `奇门 2026-03-24 15:00` |
| Auspicious Date Selection | `择吉 2026-04 开业` |

### Fortune Analysis

| Feature | Trigger |
|---------|---------|
| Annual / Decade Fortune | `2026年运势` / `未来十年运势` |
| Career / Wealth / Romance / Health | `财运好不好` |
| Marriage Compatibility | `合婚 张三 李四` |
| Feng Shui Layout | `风水分析` |

### Divination

| Feature | Trigger |
|---------|---------|
| Meihua Yi Shu (I Ching) | `梅花易数 3 5 2` |
| Liu Yao (Six Lines) | `六爻占卜` |
| QiMen Timing | `奇门选时 明天15:00` |

### Daily Fortune Push

Automatic morning push at **07:00** (today's fortune) and evening push at **20:00** (tomorrow's preview).

Each push includes: overall index, lucky color / direction / number, daily do's & don'ts, risk warnings, auspicious hours, and a daily quote.

```
每日运势开 / 开启运势推送   → Enable
每日运势关 / 关闭运势推送   → Disable
推送状态                   → Check status
```

---

## Cross-Validation Weights

| Question Type | BaZi | ZiWei | QiMen | Meihua | LiuYao |
|---------------|------|-------|-------|--------|--------|
| Lifetime Chart | 40% | 30% | — | — | — |
| Annual Fortune | 40% | 30% | 20% | 10% | — |
| Career Decision | 30% | 20% | 30% | — | 20% |
| Romance / Marriage | 40% | 30% | — | 10% | 20% |
| Immediate Question | — | — | 30% | 40% | 30% |

---

## Requirements

- Node.js >= 18
- Run `npm install` to install `iztro` (ZiWei DouShu) and `lunar-typescript` (lunar calendar)
- `OPENCLAW_KNOWLEDGE_DIR` *(optional)*: path to ZiWei pattern knowledge base (`.md` files). Skill degrades gracefully if absent.

---

## Installation

```bash
# Clone into your openclaw skills directory
cd ~/.openclaw/workspace/skills
git clone https://github.com/jiajiaoy/yunshi.git

# Install dependencies
cd yunshi && npm install
```

---

## Scripts

```bash
# Register / Profile
node scripts/register.js <userId> <name> <gender> <birthDate> <birthTime> [place]
node scripts/profile.js show <userId>
node scripts/profile.js add <userId> spouse|child <name> <birthDate> <gender>

# Chart Reading
node scripts/ziwei.js <birthDate> <gender> [hour]
node scripts/qimen.js [date] [hour]
node scripts/zhuanshi.js <YYYY-MM> <activityType> [userBaZi]
node scripts/fengshui.js [bazi] [year]

# Fortune / Compatibility / Divination
node scripts/daily-fortune.js [date]
node scripts/marriage.js <userId1> <userId2>
node scripts/meihua.js [num1-3]
node scripts/liuyao.js [010203] [question]

# Push Management
node scripts/daily-push.js --dry-run          # Simulate push
node scripts/daily-push.js --test <userId>    # Test push
node scripts/daily-push.js --list             # List active users
node scripts/push-toggle.js on|off|status <userId>

# Preference Tracking (call after each query)
node scripts/preference-tracker.js record <userId> <topic> explicit_query|topic_drill
node scripts/preference-tracker.js weights|top <userId> [N]
# topic: 财运|事业|感情|健康|婚姻|子女|官司|出行|风水
```

---

## Cron Push Setup

```bash
openclaw cron add "0 7 * * *" "cd ~/.openclaw/workspace/skills/yunshi && node scripts/daily-push.js"
openclaw cron list
openclaw cron delete <jobId>
```

> **子时算法**: Method `1` = 23:00–23:59 counts as next day (Ni Haisha school); Method `2` = counts as current day (traditional school)

---

## Supported Channels

`telegram` / `feishu` / `slack` / `discord`

---

## Risk Alert Levels

🔴 Critical (act immediately) · 🟡 Caution (handle carefully) · 🟢 Note (general reminder)

Categories: 🚨 Health · 💰 Finance · 💕 Romance · 💼 Career · ⚖️ Legal

---

## Privacy

User profiles are stored in `data/profiles/<userId>.json` and contain birth date, time, place, and family member data. Keep this directory private. Data is used only for personal astrology calculations.

---

## Notes

- When user-provided data conflicts with AI calculations, user data takes precedence
- Astrology is a reference, not a certainty
- Bilingual support: responds in the user's language; Chinese astrology terms are preserved with translations in parentheses

---

*Version 1.1.0 · Updated 2026-03-30 · MIT License*
