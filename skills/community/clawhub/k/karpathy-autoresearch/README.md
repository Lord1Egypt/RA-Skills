# 🔬 autoresearch

**Turn any measurable task into a self-improving loop.**

Based on [Karpathy's autoresearch pattern](https://x.com/karpathy): mutate a strategy or prompt → evaluate against a scoring function → keep improvements, revert failures → repeat autonomously.

Works on anything with a measurable score: trading strategies, content scripts, thumbnails, ad copy, email subjects, prompts, configs.

---

## Results

| Case Study | Baseline | Final | Improvement | Experiments | Time |
|-----------|----------|-------|-------------|-------------|------|
| **Gold Trading** (Sharpe ratio) | 5.80 | 12.23 | **+111%** | 86 | 25 min |
| **YouTube Shorts** (quality score) | 94.3/100 | 96.7/100 | **+2.5%** | 11 | ~10 min |

> **Gold**: Discovered that removing the momentum threshold entirely (0.003→0) and tightening EMAs (8/24→5/11) more than doubled the Sharpe ratio.

> **YouTube**: Found that atomic sentences, strict word counts (40-50), and strong negative examples pushed already-good scripts higher.

---

## How It Works

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│ BASELINE │───▶│  MUTATE  │───▶│ EVALUATE │───▶│  DECIDE  │
│          │    │          │    │          │    │          │
│ Score    │    │ Change   │    │ Run your │    │ Better?  │
│ current  │    │ ONE      │    │ scoring  │    │ Keep it  │──┐
│ version  │    │ thing    │    │ function │    │ Worse?   │  │
│          │    │          │    │          │    │ Revert   │  │
└──────────┘    └──────────┘    └──────────┘    └──────────┘  │
                     ▲                                         │
                     └─────────────────────────────────────────┘
                                    Loop
```

1. **Baseline** — Score whatever you're optimizing right now
2. **Mutate** — The agent changes ONE thing (a parameter, a sentence, a rule)
3. **Evaluate** — Your scoring function produces a number
4. **Decide** — Higher score? Git commit + keep. Lower? Git revert. Repeat.

Every experiment is a git commit. Full history, easy rollback, clear diffs.

---

## Installation

```bash
clawhub install alannjaf/autoresearch
```

Then tell your agent:

> "Run autoresearch on my email subject line skill"

> "Optimize my trading strategy config"

> "Self-improve this prompt — here's how to score it: ..."

---

## What You Need

1. **A mutable file** — the thing you're optimizing (a prompt, config, strategy, template)
2. **An evaluation function** — anything that returns a number (higher = better)
3. **That's it.**

The skill handles the loop, git tracking, mutation strategy, and reporting.

---

## Free vs Pro

| Feature | Free | Pro ($99) |
|---------|------|-----------|
| Core autoresearch loop | ✅ | ✅ |
| Git experiment tracking | ✅ | ✅ |
| Generic eval template | ✅ | ✅ |
| SKILL.md instructions | ✅ | ✅ |
| **Trading backtest harness** | — | ✅ |
| **LLM judge calibration** (content) | — | ✅ |
| **Vision scoring** (thumbnails) | — | ✅ |
| **Pre-built mutation strategies** | — | ✅ |
| **Priority support** | — | ✅ |

### Pro Tier — $99 USDT

Includes pre-built evaluators for:
- **Trading**: Backtest harness with Sharpe ratio, max drawdown, win rate scoring
- **Content**: Calibrated LLM judge with multi-criteria scoring (hook, pacing, clarity, engagement)
- **Thumbnails**: Vision model scoring for contrast, text readability, face detection, emotional impact

**To purchase:**
1. Send **$99 USDT (TRC-20)** to: `TYMGjMAs3t5qaEU5xBqLQNpnGeLQ4G6gmM`
2. DM [@Alan_Jaf on Telegram](https://t.me/Alan_Jaf) with your transaction hash
3. Get access within 24 hours

---

## Links

- **GitHub**: [github.com/Alannjaf/autoresearch](https://github.com/Alannjaf/autoresearch)
- **ClawHub**: `clawhub install alannjaf/autoresearch`
- **Support**: [@Alan_Jaf on Telegram](https://t.me/Alan_Jaf)

---

## License

MIT — use it however you want. If it makes you money, consider the Pro tier. 🤝
