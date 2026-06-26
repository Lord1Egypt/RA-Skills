# 👻 ghostprint

> Depersonalize your LLM usage. Introduce noise. Prevent fingerprinting.

**ghostprint** sends behaviorally realistic noise queries to LLM providers on a schedule to contaminate usage profiles and prevent behavioral fingerprinting. Available as a standalone Python script **or** a native OpenClaw plugin.

---

## Why

LLM providers build profiles from your query patterns — topics, timing, phrasing, token counts, session depth. ghostprint disrupts this by injecting synthetic noise that is statistically indistinguishable from real human usage, making it impossible to isolate your real fingerprint.

---

## Features

- 🔌 **Provider-agnostic** — Anthropic, OpenAI, Z.ai, Mistral, any OpenAI-compatible endpoint
- 🎭 **Persona system** — 6 stable user personas with biased domain preferences, multi-turn rates, and token budgets
- 💬 **300+ organic topics** — 12 domains, varied syntax (fragments, questions, context-rich multi-sentence)
- 🔗 **Contextual follow-ups** — multi-turn sessions use topic-paired follow-ups, not generic disconnected phrases
- 🎲 **Poisson-process timing** — exponentially distributed inter-arrival times, not uniform jitter
- 📅 **Activity-level scheduling** — hour-of-day + day-of-week weights suppress noise during sleep hours
- 🔐 **Cryptographic randomness** — `crypto.randomInt()` / `os.urandom()`, not PRNG
- 📊 **Metadata-only logs** — never logs topic text or reply content
- 💸 **Ultra-cheap** — log-normal token budgets, median ~55 tokens (< $0.02/month)
- ⚙️ **Zero dependencies** — standalone Python uses stdlib only; OpenClaw plugin uses Node builtins

---

## OpenClaw Plugin (Recommended)

The OpenClaw plugin version integrates natively: it reuses your existing provider API keys (no separate config), runs as a background service inside the gateway, and exposes `ghostprint_fire` and `ghostprint_stats` as agent tools.

### Install

```bash
# Clone into your OpenClaw extensions directory
git clone https://github.com/alarawms/ghostprint ~/.openclaw/extensions/ghostprint

# Enable the plugin
openclaw plugins enable ghostprint

# Restart gateway to apply
openclaw gateway restart
```

### Usage

Once installed, use these tools in any chat session:

```
ghostprint_fire   — fire a noise round immediately
ghostprint_stats  — show cumulative stats and recent log
```

The background scheduler fires automatically every ~2 hours (Poisson-distributed) when the gateway is running.

### Plugin Config (optional)

Add to your `~/.openclaw/openclaw.json` under `plugins.entries.ghostprint.config`:

```json
{
  "enabled": true,
  "min_interval_minutes": 90,
  "max_interval_minutes": 180,
  "timezone_offset": 3,
  "providers": [
    {
      "name": "anthropic",
      "provider": "anthropic",
      "base_url": "https://api.anthropic.com/v1",
      "model": "claude-haiku-4-5",
      "style": "anthropic",
      "weight": 1
    },
    {
      "name": "zai",
      "provider": "zai",
      "base_url": "https://api.z.ai/api/coding/paas/v4",
      "model": "glm-5.1",
      "style": "openai",
      "weight": 1
    }
  ]
}
```

> **No API keys needed in config.** The plugin resolves credentials from your existing OpenClaw provider setup via `api.runtime.modelAuth.resolveApiKeyForProvider()`.

### Plugin Files

```
openclaw-plugin/
  index.ts              — plugin entry point (TypeScript, zero deps)
  openclaw.plugin.json  — plugin manifest
  package.json          — package metadata
```

---

## Standalone Python Script

For use without OpenClaw.

### Quick Start

```bash
# 1. Copy config
cp config.example.yaml config.yaml

# 2. Add your providers
nano config.yaml

# 3. Test run
python3 ghostprint.py --run-once

# 4. Install cron
python3 ghostprint.py --install-cron
```

### Config

```yaml
# config.yaml
providers:
  - name: anthropic
    base_url: https://api.anthropic.com/v1
    api_key: ${ANTHROPIC_API_KEY}
    model: claude-haiku-4-5
    style: anthropic          # anthropic | openai
    weight: 1

  - name: zai
    base_url: https://api.z.ai/api/coding/paas/v4
    api_key: ${ZAI_API_KEY}
    model: glm-5.1
    style: openai
    weight: 1

noise:
  max_tokens: 60              # baseline (log-normal sampled around this)
  topics_file: topics.txt     # optional custom topic list
  strategy: random            # random | round-robin | weighted

schedule:
  base_interval_minutes: 90
  jitter_minutes: 45
```

### Adding Providers

Any OpenAI-compatible endpoint:

```yaml
- name: openai
  base_url: https://api.openai.com/v1
  api_key: ${OPENAI_API_KEY}
  model: gpt-4o-mini
  style: openai
  weight: 2

- name: mistral
  base_url: https://api.mistral.ai/v1
  api_key: ${MISTRAL_API_KEY}
  model: mistral-small-latest
  style: openai
```

---

## Anti-Fingerprint Design

See [`ANTI-FINGERPRINT.md`](./ANTI-FINGERPRINT.md) for the full technical design.

Key design decisions (v3):

| Signal | What ghostprint does |
|---|---|
| Timing | Poisson inter-arrival (exponential distribution, soft truncation) |
| Token budget | Log-normal sampling with perturbed μ/σ per session |
| Topics | 300+ prompts across 12 domains, persona-weighted selection |
| Follow-ups | Topic-paired contextual follow-ups (not generic phrases) |
| Sessions | 30% multi-turn with realistic post-response reading delays |
| Active hours | Hour + day-of-week probability weights (no hard cutoffs) |
| Randomness | `crypto.randomInt()` / `os.urandom()` throughout |
| Logs | Metadata only — no topic text, no reply content |
| Personas | 6 stable personas rotate every 3–8 rounds |

### Residual risks

ghostprint raises the cost of behavioral fingerprinting but does not guarantee anonymity. These limitations are architectural — they cannot be solved in code alone.

- **Same IP / TLS fingerprint** — all requests originate from one machine. Route noise through a separate proxy or VPN exit node for stronger isolation.
- **Account-level correlation** — providers see noise and real queries on the same API key. Use a dedicated API account for noise traffic to break this link.
- **Content disjoint from real usage** — if your real topics never overlap with the 12-domain noise pool, a topic classifier can separate them. Consider adding custom topics to `topics.txt` that overlap with your actual usage domains.
- **Volume imbalance** — if noise queries vastly outnumber or are dwarfed by real queries, the ratio itself becomes a signal. Keep noise volume proportional to your real usage (the default ~3x/day is calibrated for light-to-moderate users).
- **Query complexity gap** — noise queries are simple single-concept questions; they never upload files, reference prior context across sessions, or use tool calling. A provider analyzing query complexity (not just token count) could separate noise from real usage.
- **Multi-turn coherence** — follow-ups are topic-paired but do not reference the LLM's actual response. Real conversations build on prior answers. This is a detectable difference for sophisticated analysis.

### Hardening recommendations

For users who need stronger protection beyond what ghostprint provides out of the box:

| Mitigation | What to do |
|---|---|
| **Separate API accounts** | Use dedicated throwaway API keys for noise. Do not reuse your primary account credentials. |
| **Proxy noise traffic** | Route noise queries through a different IP (VPN, Tor, residential proxy) than your real queries. |
| **Custom topic overlap** | Add entries to `topics.txt` that match your real usage domains so noise and signal are not trivially separable. |
| **Tune noise volume** | Adjust `base_interval_minutes` so noise frequency is proportional to your real query rate. |
| **Disable local logging** | Both implementations now log metadata-only by default, but for maximum privacy you can redirect logs to `/dev/null` or disable the log function entirely. |

---

## Cost Estimate

| Provider | Model | Per run | 3×/day |
|---|---|---|---|
| Anthropic | claude-haiku-4-5 | ~$0.00025 | ~$0.23/month |
| Z.ai | glm-5.1 | ~$0.0001 | ~$0.09/month |

Total: **< $0.35/month** at 3× daily.

---

## Privacy Philosophy

ghostprint does not store your real queries. It only generates synthetic noise.  
The goal is not to hide your identity — it's to make profiling unreliable by polluting the signal with enough behaviorally realistic noise that no useful fingerprint can be extracted.

---

## License

MIT
