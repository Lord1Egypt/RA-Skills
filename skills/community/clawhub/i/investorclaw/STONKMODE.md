# Stonkmode — Entertainment Mode + Dr. Stonk Financial Education

**v1.0.1** | 30 fictional cable TV finance personalities + educational mode

---

## What is Stonkmode?

After serious portfolio analysis, enable **Stonkmode** for AI-generated
narrative commentary featuring 30 distinct fictional cable finance TV
personalities. Each persona has a unique voice, perspective, and comedic
flair — turning dry financial metrics into entertaining (and accurate)
portfolio narratives.

**Stonkmode is entertainment, not advice.** Its existence is the
clearest signal that InvestorClaw is NOT institutional financial
software.

---

## Enable Stonkmode

Stonkmode is a state toggle on the running ic-engine container. Ask
your agent to enable it:

```text
Switch to stonkmode.
What's in my portfolio?
```

The agent routes "switch to stonkmode" through `portfolio_ask`, which
flips the engine into stonkmode for subsequent calls. The engine reads
state from `~/.investorclaw/stonkmode.json` (mounted as
`/data/stonkmode.json` inside the container).

Stonkmode wraps analysis output in character narration while preserving
all underlying financial rigor. All math stays deterministic Python.
The LLM only generates the entertaining framing.

To disable:

```text
Turn off stonkmode.
```

---

## The 30 Personas

Stonkmode includes personalities across five archetypes:

**HIGH ENERGY** (3): Blitz Thunderbuy, Brick "Diamond Hands"
Stonksworth, Sal "The Pit" Decibelli

**SERIOUS** (5): Aldrich Whisperdeal, Prescott Pennington-Smythe,
Dominique "Closing Bell" Valcourt, Dr. Amara Osei-Bonsu, Carmen "Fib"
Torres

**MENTORS** (3): Big Jim Cashonly, Sunny Rainyday-Fund, Baron Von
Cashflow

**POLICY VETERANS** (2): Biff Chadsworth III, Skip "Well, Actually"
Contrarian

**HUMOR** (5): Professor What?, Penny "The Algorithm" Stock, Zeke
"YOLO" Riskowitz, Isabella "Vibe Check" Sentiment, Chad "Calls Only"
Bullion

**SPECIALTY** (7): Rashida "ESG Mandate" Williams, Koji "Yield Curve"
Tanaka, Margot "Rebalance" Dutoit, Felix "Carry Trade" Leverage,
Priya "Margin" Malhotra, Wolfgang "Volatility Surface" Heisenberg,
Nora "Market Hours" Overnight

**EDUCATORS** (1): Dr. Stonk — Spock-like persona for financial
education explanations

Avatars (30 SVG persona portraits + 1 Dr. Stonk PNG) ship inside the
ic-engine container at `/opt/ic-engine/.venv/lib/python3.12/site-packages/ic_engine/assets/stonkmode-avatars/`.
The dashboard at `localhost:18092` renders them in the Stonkmode tab.

---

## Dr. Stonk — Financial Education Mode

Ask your agent for verbose explanations to unlock **Dr. Stonk
explanations**:

```text
What's my Sharpe ratio? Use Dr. Stonk to explain it.
```

Dr. Stonk (Mr. Spock persona) provides plain-English definitions and
context for:

- Portfolio metrics (Sharpe ratio, beta, max drawdown, concentration
  indices)
- Bond mathematics (YTM, duration, convexity, FRED Treasury benchmarks)
- Market data and analyst consensus
- Modern Portfolio Theory optimization

All explanations are educational only — never offering specific
buy/sell recommendations.

---

## Configuration

Stonkmode is controlled by:

1. **State file**: `/data/stonkmode.json` inside the container
   (persisted via the `ic-engine-data` Docker volume on the host).
   Toggle via your agent's `portfolio_ask` call.

2. **Environment variables** in `compose.yml`:
   - `INVESTORCLAW_NARRATIVE_PROVIDER` — `openai_compat` (default) or
     `ollama`
   - `INVESTORCLAW_NARRATIVE_ENDPOINT` — `https://api.together.xyz/v1`
     (default) or local Ollama endpoint
   - `INVESTORCLAW_NARRATIVE_MODEL` — `google/gemma-4-31B-it`
     (default; serverless on Together) or `MiniMaxAI/MiniMax-M2`
     (paid dedicated endpoint required)
   - `INVESTORCLAW_STONKMODE_DISABLED` — set to `true` to disable in
     CI / test environments

See [SKILL.md § Model recommendations](SKILL.md#model-recommendations)
for the full narrative-provider reference.

---

## Example Output

Sample (from Blitz Thunderbuy):

> "THUNDER-BUY ALERT! Your portfolio is 68% equities with a Sharpe
> ratio of 1.42 — not bad for holding patterns, but we're leaving
> alpha on the table. The concentration here? AAPL eating 12% of your
> allocation while your bonds languish at 2.1% YTM. Time to rebalance
> and LET'S GO LONG!"

The deterministic envelope underneath this prose is identical to
non-stonkmode output. Stonkmode narration is purely presentation-layer.

See [docs/STONKMODE_ARCHITECTURE.md](docs/STONKMODE_ARCHITECTURE.md)
for the full pipeline (market-condition detection → archetype weighting
→ pair selection → narration → dashboard render).

---

## What Stonkmode Is NOT

❌ Not investment advice — purely entertainment
❌ Not a robo-advisor decision engine — personas don't pick stocks
❌ Not replacing a financial advisor — use output as conversation
   starters only
❌ Not altering portfolio math — narration layer is read-only on the
   signed envelope

---

## Cost + latency

| Mode | Cost per query | Latency |
|---|---|---|
| Cloud (Together AI, default) | ~$0.001–0.005 / narration | +1–3 s |
| Local (Ollama on host) | $0 | +2–5 s (GPU-bound) |

Stonkmode adds one extra LLM call to a typical `portfolio_ask` flow —
the persona narration. The deterministic pipeline runtime is unchanged.

---

## See also

- [docs/STONKMODE_ARCHITECTURE.md](docs/STONKMODE_ARCHITECTURE.md) —
  full pipeline, market-condition detection, archetype weighting
- [docs/STONKMODE_AVATAR_LEGEND.md](docs/STONKMODE_AVATAR_LEGEND.md) —
  30-persona avatar grid reference
- [SKILL.md](SKILL.md) — agent-readable spec, model recommendations,
  troubleshooting
- [DISCLAIMER.md](DISCLAIMER.md) — educational-only framing

---

**Questions?** Open an issue:
https://github.com/mnemos-os/mnemos-ic-runtime/issues
