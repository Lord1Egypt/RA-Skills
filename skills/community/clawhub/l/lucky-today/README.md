# Lucky Today — Daily Fortune Oracle (今日运势)

> Offline deterministic daily fortune skill — lucky color / direction / number / item · today / weekly / monthly · couple readings · scenario fortunes (interview / exam / dating / launch / business trip) · bilingual CN/EN · push to Telegram / Feishu / Slack / Discord. **No external API.**

[![clawhub](https://img.shields.io/badge/clawhub-lucky--today-blue)](https://clawhub.ai/skills/lucky-today)
[![version](https://img.shields.io/badge/version-0.1.0-green)](https://clawhub.ai/skills/lucky-today)
[![openclaw](https://img.shields.io/badge/openclaw-skill-orange)](https://openclaw.ai)

## What it does

Daily atomic-output fortune oracle — the kind of output people actually ask for:

- 🧭 **Lucky direction** (8 options)
- 🎨 **Lucky colors** (primary + accent from 10 standard colors)
- 🔢 **Lucky numbers** (2-3 single digits)
- 📿 **Lucky item** (12 actionable items)
- ✅ **3-5 things to do today**
- ❌ **3-5 things to avoid today**
- ⚠️ **Strong warnings** with concrete time windows
- 🌟 **Topic-specific outlook** (wealth / love / career / social)

All computed via deterministic math — same input → same output. No randomness, no API calls, no LLM hallucination of "your day will be magical".

## Modes

| Mode | Trigger | What you get |
|---|---|---|
| 单日 today *(default)* | "今日运势" / "lucky today" | Full output above |
| 次日 tomorrow | "明天运势" / "tomorrow fortune" | Same, shifted +1 day |
| 本周 weekly | "本周运势" / "this week" | 7-day rollup + peak / trough days + weekly strategy |
| 本月 monthly | "本月运势" / "monthly horoscope" | Month arc + 7-8 focus dates + 3 caution dates |
| 双人合盘 couple | "我和xx今天合不合" / "couple today" | Joint compatibility score + co-do / co-avoid + communication advice |
| 场景运势 | "面试运" / "interview luck" / "考试运" / "相亲运" / "出差运" / "上线运" | Scenario-specific output with bias formula + tailored warnings |

Modes combine — `"明天面试运"` works, so does `"这周双人合盘"`.

## Installation

```bash
clawhub install lucky-today
# or
openclaw install lucky-today
```

## Trigger phrases

- **中文(高频):** 今天运势、今天幸运色、今天财运、明天运势、本周运势、面试运、考试运、相亲运、双人合盘
- **English:** "my horoscope", "lucky color today", "lucky direction", "interview luck", "exam luck", "weekly horoscope", "monthly horoscope", "couple compatibility today"
- **日本語:** 今日の運勢、ラッキーカラー
- **한국어:** 오늘 운세, 행운의 색
- **Tiếng Việt:** vận may hôm nay, tử vi hôm nay

## How it works

100% prompt-only — no Node scripts, no Python, no external libraries. The skill ships with:

```
SKILL.md                        # entry point
references/fortune_rules.md     # deterministic math (R = (B*131 + D*17) mod 1000, etc)
references/scenario_rules.md    # interview / exam / dating / launch / trip biases
references/couple_rules.md      # joint compatibility math + zodiac bonus
references/output_templates.md  # bilingual emoji templates for all modes
references/user_profile_template.md  # JSON schema for optional persistence
```

The agent reads these files in order, runs the math mentally, and outputs in the strict emoji template. Same birth date + same query date always produce the same lucky direction / color / number — so you can trust today's "lucky color blue" wasn't a coin flip.

## Data & Privacy

- **Local-only profiles.** If you say "remember me", your `user_profile.json` is written to `{baseDir}/user_profile.json` on your machine. The skill never uploads.
- **Ships with template only.** Published package contains only `references/user_profile_template.md`. Real profiles are blocked by `.clawhubignore`.
- **Recommended permissions.** `chmod 600 user_profile.json`.
- **Deletion.** Say "delete my profile" or `rm user_profile.json` — no hidden cache.
- **Partner privacy.** Couple readings need both birth dates but partner birthday is not echoed back in regular output and is treated as sensitive.

## Push setup

```bash
# Morning at 7am local
openclaw cron add "0 7 * * *" \
  "use lucky-today: 今日运势 (推送给 telegram chat_id <YOUR_ID>)"

# Tomorrow preview at 9pm local
openclaw cron add "0 21 * * *" \
  "use lucky-today: 明日运势 (推送给 telegram chat_id <YOUR_ID>)"
```

The skill produces a "push-ready" condensed text when invoked through cron. See `SKILL.md → 推送(Telegram / Feishu / Slack / Discord)`.

## Related skills

| You want | Use |
|---|---|
| Full BaZi / ZiWei DouShu / QiMen chart calculation | [yunshi](https://clawhub.ai/skills/yunshi) |
| Western zodiac daily horoscope (Aries, Taurus, …) | [daily-astro](https://clawhub.ai/skills/daily-astro) |
| Feng shui layout | [fengshui](https://clawhub.ai/skills/fengshui) |
| Deep personality reading from BaZi | [bazii-mingli](https://clawhub.ai/skills/bazii-mingli) |

## Keywords

今日运势 · 幸运颜色 · 幸运方位 · 幸运数字 · 今日财运 · 桃花运 · 面试运势 · 考试运势 · 相亲运势 · 合盘 · 本周运势 · 本月运势 · 每日运势推送 · daily horoscope · lucky color · lucky number · lucky direction · interview luck · exam luck · weekly horoscope · monthly horoscope · couple compatibility · 운세 · 運勢 · tử vi

---

Built for [OpenClaw](https://openclaw.ai) · Published on [clawhub.ai](https://clawhub.ai/skills/lucky-today)
