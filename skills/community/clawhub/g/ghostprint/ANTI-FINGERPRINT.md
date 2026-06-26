# Anti-Fingerprint Design — ghostprint v2.0

## What fingerprinting actually is

LLM providers don't just log "this user asked X". They build statistical profiles from:
- **Temporal patterns** — when do you query, how often, at what time of day
- **Token distributions** — how long are your prompts and responses
- **Topic clustering** — what domains you return to
- **Structural patterns** — do you always ask questions? Do you always use the same format?
- **Session patterns** — single-turn vs multi-turn, follow-up phrasing
- **Inter-request timing** — do your queries arrive metronomically (bot) or irregularly (human)?

## What v1 got wrong

| Signal | v1 behavior | Why it's a fingerprint |
|--------|-------------|------------------------|
| Timing | Uniform random `U(120, 160)` min | Uniform distribution is NOT how humans use LLMs |
| Token budget | Always 60 | Constant token count is a dead giveaway |
| Topic pool | 40 household/cooking questions | One-domain cluster is identifiable |
| Prompt structure | All "How do I..." / "Why does..." | Uniform syntax across 100% of requests |
| Session depth | Always single-turn | Real users have multi-turn conversations |
| Active hours | No restriction | Real users don't query at 3am |
| Randomness | `Math.random()` (PRNG) | Statistically distinguishable with ~1000 samples |
| Provider selection | Fixed 60%/40% bias | Fixed selection ratio is predictable |

## What v2 does instead

### 1. Cryptographic randomness
`crypto.randomInt()` for all timing and selection decisions. Passes statistical randomness tests that `Math.random()` fails at scale.

### 2. Poisson-process inter-arrival times
Real human usage follows a Poisson process — exponentially distributed inter-arrival times. v2 samples from `Exponential(mean)` rather than uniform `[min, max]`. This matches the statistical signature of real user behavior.

### 3. Log-normal token budget
Human response length preferences follow a log-normal distribution. v2 samples `LogNormal(μ=4.0, σ=0.8)` → range ~20–400 tokens with median ~55. Cheap but variable.

### 4. 300+ topics across 12 domains
Cooking, health, science, DIY, technology, finance, language, travel, psychology, history, lifestyle, and context-rich multi-sentence prompts. No single domain dominates.

### 5. Structural variety
Mix of terse fragments ("Best substitute for buttermilk?"), full questions, and multi-sentence context prompts ("I've been trying to learn Spanish for a year..."). Breaks syntactic clustering.

### 6. 30% multi-turn sessions
Simulates realistic conversations with 2–4 turns and realistic inter-turn delays (2–8s). Single-turn-only traffic is a bot signal.

### 7. Time-of-day suppression (quiet hours)
Noise is suppressed from midnight–7am local time. Real users don't query LLMs at 3am. A tool that fires at 3am is immediately identifiable as automated.

### 8. Randomized temperature
Real users have different creativity/precision preferences. v2 samples temperature from `U(0.3, 1.1)` per request.

### 9. Occasional system prompts (35%)
Real users sometimes set system contexts. Structural variety.

### 10. 8% idle round skip
Real users don't query every single interval — they skip days, take breaks. The occasional skipped round is part of the human behavioral signature.

### 11. Weighted Poisson provider selection
Provider selection uses weighted random draw with Poisson variance rather than a fixed 1 or 2 provider rule.

## Residual fingerprint risks

No tool is perfect. ghostprint raises the cost of behavioral fingerprinting, but it does not guarantee anonymity. These are architectural limitations — not bugs to be fixed.

- **Account-level correlation** — if you only have one account per provider, they can still associate all queries (noise + real) with you. Use separate accounts for noise if this is a concern.
- **IP-level fingerprinting** — all queries come from the same IP. Use a different exit node for noise queries if needed (future: `proxy` config option).
- **Volume disproportion** — if you send 1 real query per day and 50 noise queries per day, the ratio itself is a signal. Keep noise volume in proportion.
- **Content correlation** — if your noise topics are completely disjoint from your real topics (e.g., you only ever discuss AI but noise is all cooking), a classifier can still separate them. The 12-domain pool is designed to overlap with most user profiles.
- **Query complexity** — noise queries are simple single-concept questions. They never upload files, reference prior session context, or invoke tool calling. A provider analyzing structural complexity beyond token count could separate noise from real usage.
- **Multi-turn coherence** — follow-ups are topic-paired (v3 fix) but do not reference the LLM's actual response. Real conversations build iteratively on prior answers. Sophisticated sequence analysis could detect this.
- **Startup/shutdown correlation** — noise starts when the host machine boots and stops when it shuts down. A provider observing that noise-like queries start and stop synchronously with real queries can correlate them.

## Hardening for high-threat models

If you need stronger protection than the default configuration:

1. **Separate API accounts** — use throwaway keys for noise, not your primary credentials. This breaks account-level correlation entirely.
2. **Proxy noise traffic** — route noise through a VPN, Tor, or residential proxy so noise and real queries originate from different IPs.
3. **Custom topic overlap** — add entries to `topics.txt` that intersect with your real usage domains. If you work in ML, add ML-adjacent questions so a topic classifier cannot trivially separate signal from noise.
4. **Proportional volume** — tune `base_interval_minutes` so noise frequency matches your real query rate. ~3x/day is calibrated for light-to-moderate users.
5. **Always-on scheduling** — run ghostprint on a persistent server (not your laptop) so it does not start/stop with your work sessions.
6. **Disable local logging** — for maximum privacy, redirect logs to `/dev/null`. Both implementations now log metadata-only by default, but zero logging eliminates the last local evidence.

## Recommended config

```yaml
min_interval_minutes: 90
max_interval_minutes: 210
timezone_offset: 3      # your local GMT offset
```

This gives Poisson-distributed inter-arrival with mean ~2.5h, suppressed during sleep hours.
