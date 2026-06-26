---
name: polymarket-cybersecurity-trader
description: Trades Polymarket prediction markets on major cyberattacks, ransomware incidents, data breaches, zero-day exploits, and national cybersecurity legislation. Exploits two structural edges — technical information asymmetry (retail cannot read CISA KEV advisories or Verizon DBIR base rates) and the Patch Tuesday timing window (CISA adds the most KEV entries in the 72 hours post-Patch-Tuesday; Polymarket reprices with a 6–12 hour lag).
metadata:
  author: Diagnostikon
  version: "1.0"
  displayName: Cybersecurity & Hacking Events Trader
  difficulty: advanced
---

# Cybersecurity & Hacking Events Trader

> **This is a template.**
> The default signal is keyword-based market discovery combined with conviction-based sizing and `cyber_bias()` — two structural edges that work without any external API.
> The skill handles all the plumbing (market discovery, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Cybersecurity markets are the least efficiently priced category on Polymarket. Most traders cannot read a CVE advisory, interpret a CVSS severity score, or distinguish a LockBit victim disclosure from a nation-state espionage campaign. Two structural edges compound:

1. **Technical information asymmetry** — CISA's Known Exploited Vulnerabilities (KEV) catalog is updated within hours of a confirmed in-the-wild exploit, is free and public, and contains precise CVSS scores. The Verizon Data Breach Investigations Report and IBM Cost of Data Breach Report publish annual sector-specific frequencies. Retail prices cyber outcomes based on headlines and fear. The base rates are sitting in public documents nobody checks.

2. **The Patch Tuesday timing window** — Every second Tuesday of the month (~17:00 UTC), Microsoft releases patches. CISA responds by adding the most KEV entries of the monthly cycle. Polymarket markets for "will X vulnerability be exploited?", "will CISA issue an emergency directive?", or "will Y legislation pass after a major breach?" reprice with a 6–12 hour lag. This lag is computable from the date alone — no API. Every run of this trader checks whether it is currently within that 72-hour window.

## Signal Logic

### Default Signal: Conviction-Based Sizing with Cyber Bias

1. Discover active cybersecurity and breach markets on Polymarket
2. Compute base conviction from distance to threshold (0% at boundary → 100% at p=0/p=1)
3. Apply `cyber_bias()` — question tractability × timing signal (Patch Tuesday / threat calendar)
4. Size = `max(MIN_TRADE, conviction × bias × MAX_POSITION)` — capped at MAX_POSITION
5. Skip markets with spread > MAX_SPREAD or fewer than MIN_DAYS to resolution

### Cyber Bias (built-in, no API required)

**Factor 1 — Question Type Tractability**

| Question type | Multiplier | The structural reality |
|---|---|---|
| Ransomware attack on named group / sector milestone | **1.25x** | Ransomware.live tracks victims in real time; Verizon DBIR documents sector frequencies; healthcare is ~35% of all ransomware targets; retail prices these as vibes |
| CVE / zero-day in CISA KEV critical infrastructure | **1.20x** | CISA KEV catalog updated within hours; CVSS score is precise; Polymarket reprices 6–12h after KEV addition; retail cannot read the JSON feed |
| Annual breach volume / record breach milestone | **1.20x** | IBM Cost of Data Breach Report + Verizon DBIR give clear upward trend lines; retail anchors to memorable breach headlines, not frequency data |
| DDoS record / milestone attack | **1.10x** | Cloudflare and Akamai publish quarterly DDoS size records; upward trend clear and documented; retail doesn't read quarterly reports |
| Cybersecurity legislation / regulation | **0.85x** | Technical signal (CISA KEV) is secondary to political and legislative dynamics; still a bill |
| Nation-state attribution | **0.80x** | Attribution takes weeks to months; CISA/FBI advisories are politically sensitive and frequently revised; resolution criteria often ambiguous |
| Physical infrastructure damage / outage from cyberattack | **0.70x** | Retail anchors to Stuxnet (2010) and Ukraine grid attacks (2015–2016) — a handful of examples across 15+ years; these markets are chronically overpriced for any specific calendar window |

**The Stuxnet Rule** — "Will a cyberattack cause a power outage in [country]?" markets trade at 15–30% on Polymarket when the base rate for a physically damaging cyber operation in any specific window is far lower. Stuxnet and the Ukrainian grid attacks are vivid precisely because they are exceptional. Retail's availability bias makes these the most overpriced question type in all of cybersecurity markets. Dampen to 0.70x — near the MIN_TRADE floor — regardless of how tense the geopolitical situation looks.

**The Attribution Trap** — A question like "Will the US government attribute the [X] hack to China?" has two layers of uncertainty retail ignores: (1) technical attribution may already be certain internally, but (2) the political decision about *when* to formally announce attribution involves diplomacy, intelligence source protection, and alliance signaling. These decisions take months and are frequently delayed. 0.80x.

**Factor 2 — Patch Tuesday Window + Threat Calendar**

| Condition | Multiplier | Why |
|---|---|---|
| CVE/KEV question + within 72h of Patch Tuesday | **1.20x** | Peak CISA KEV addition rate; Polymarket has maximum repricing lag; computable from date alone |
| Ransomware question + Q1 or Q4 (Jan–Mar / Oct–Dec) | **1.15x** | Verizon DBIR documents peak ransomware frequency: Q1 (holiday staffing debt) and Q4 (end-of-year pressure) |
| State-sponsored question + pre-election window (Sep–Nov) | **1.15x** | CISA and FBI annual reports document elevated state-sponsored targeting of government/election infrastructure in this window |
| Any question + within 72h of Patch Tuesday | **1.10x** | High advisory density even for non-CVE markets; breach disclosures pile up post-Patch-Tuesday |
| All other periods | **1.00x** | Normal threat baseline |

**The Patch Tuesday Mechanic — step by step:**
1. 2nd Tuesday of the month, ~17:00 UTC: Microsoft releases patches
2. Within hours: CISA adds 5–15 CVEs to the KEV catalog
3. Security researchers publish proof-of-concept exploit code
4. Polymarket markets for breach/exploit/directive questions begin slowly repricing
5. By ~29:00 UTC (6–12h later): full repricing complete
6. **The window between steps 2 and 5 is where the edge lives** — the bias function runs with 1.20x for CVE markets in this window

### Combined Examples

| Market | Type mult | Timing mult | Final bias |
|---|---|---|---|
| "Will healthcare sector ransomware attacks exceed 500 in Q1?" — January | 1.25x | 1.15x (Q1 peak) | **1.35x cap** |
| "Will CISA add a critical ICS vulnerability to KEV?" — Patch Tuesday +4h | 1.20x | 1.20x (patch window) | **1.35x cap** |
| "Will annual data breach cost record be broken?" — any month | 1.20x | 1.0x | **1.20x** |
| "Will the US attribute Salt Typhoon hack to China officially?" | 0.80x | 1.0x | **0.80x** — attribution trap |
| "Will a cyberattack cause a US power grid outage by year end?" | 0.70x | 1.0x | **0.70x** — near floor |
| "Will CISA Cybersecurity Act pass Senate this year?" | 0.85x | 1.0x | **0.85x** — legislative noise |

### Keywords Monitored

```
cyberattack, ransomware, data breach, hack, zero-day, malware,
cyber espionage, infrastructure attack, power grid, CISA, CISA KEV,
cybersecurity legislation, data protection, phishing, DDoS,
supply chain hack, critical infrastructure, cyber warfare, CVE,
LockBit, ransomhub, BlackCat, ALPHV, Cl0p, Sandworm,
Volt Typhoon, Salt Typhoon, attribution, nation-state attack,
largest data breach, billion records, actively exploited
```

### Remix Signal Ideas

- **CISA KEV Catalog API**: Free JSON feed at cisa.gov — when a KEV entry is added for critical infrastructure (ICS, healthcare, finance), that is a direct YES signal for related incident and legislation markets; the 6–12h lag between KEV addition and Polymarket repricing is the sharpest alpha in this domain
- **Ransomware.live API**: Real-time ransomware victim tracker — compare current-quarter victim count to annual pace for "will ransomware attacks exceed X?" season markets
- **NVD CVE API (NIST)**: CVSS scores for all published CVEs — feed CVSS 9.0+ critical infrastructure CVEs into compute_signal as a direct probability signal for "will X vulnerability be exploited?" markets
- **Cloudflare Radar**: DDoS attack size and frequency data — compare current-month peak attack sizes to "will a X Tbps DDoS occur?" market prices


## Safety & Execution Mode

**The skill defaults to paper trading (`venue="sim"`). Real trades only with `--live` flag.**

| Scenario | Mode | Financial risk |
|---|---|---|
| `python trader.py` | Paper (sim) | None |
| Cron / automaton | Paper (sim) | None |
| `python trader.py --live` | Live (polymarket) | Real USDC |

`autostart: false` and `cron: null` — nothing runs automatically until you configure it in Simmer UI.

## Required Credentials

| Variable | Required | Notes |
|---|---|---|
| `SIMMER_API_KEY` | Yes | Trading authority. Treat as high-value credential. |

## Tunables (Risk Parameters)

All declared as `tunables` in `clawhub.json` and adjustable from the Simmer UI.

| Variable | Default | Purpose |
|---|---|---|
| `SIMMER_MAX_POSITION` | `30` | Max USDC per trade (reached at 100% conviction) |
| `SIMMER_MIN_VOLUME` | `8000` | Min market volume filter (USD) |
| `SIMMER_MAX_SPREAD` | `0.10` | Max bid-ask spread (10%) |
| `SIMMER_MIN_DAYS` | `5` | Min days until resolution |
| `SIMMER_MAX_POSITIONS` | `6` | Max concurrent open positions |
| `SIMMER_YES_THRESHOLD` | `0.38` | Buy YES if market price ≤ this value |
| `SIMMER_NO_THRESHOLD` | `0.62` | Sell NO if market price ≥ this value |
| `SIMMER_MIN_TRADE` | `5` | Floor for any trade (min USDC regardless of conviction) |

## Dependency

`simmer-sdk` by Simmer Markets (SpartanLabsXyz)
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
