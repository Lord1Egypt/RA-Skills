---
name: mortgage-marketing
description: Multi-channel mortgage marketing campaign engine — one brief generates email + social + ad copy with audience segmentation and A/B variants. Not a content generator — a full campaign system.
version: 2.0.0
metadata:
  openclaw:
    requires:
      env:
        - ANTHROPIC_API_KEY
      anyBins:
        - node
        - python3
    primaryEnv: ANTHROPIC_API_KEY
    emoji: "🏠"
    homepage: https://github.com/drivenautoplex1/openclaw-skills
    install:
      - kind: node
        package: "@anthropic-ai/sdk"
        bins: []
---

# Mortgage Marketing — v2.0 (Campaign Engine)

Previous versions generated one piece of content at a time. You'd run it for email, run it again for social, again for ads. You got isolated pieces with no coherent message across channels.

v2 introduces the **campaign engine**: input one brief, get a full coordinated campaign across every channel — email, social (per platform), ad hooks, and listing copy — all built from the same strategic brief, with audience-segmented variants and A/B split guidance.

## What Changed in v2

| Before | After |
|--------|-------|
| One content type per call | Full campaign from one brief |
| Generic output | 6 audience segments, each with tailored messaging |
| No split testing | A/B variants on every piece (gain vs. loss framing) |
| Compliance flag at end | Inline compliance guardian, per claim |
| Social posts only | Email + 4 social platforms + ad + listing in one call |

---

## What This Skill Does

Single-call campaign generation for:

- **Full campaigns** — one brief → email + LinkedIn + X + Facebook + Instagram + 3 ad hooks + optional listing copy
- **Audience-segmented copy** — different messaging for first-time buyers, veterans, investors, self-employed, credit-challenged, and relocating buyers
- **A/B split variants** — every piece gets a Variant A (gain framing) and Variant B (loss/urgency framing) with guidance on when to run each
- **Channel-specific formatting** — auto-adjusts character count, hashtag strategy, emoji usage, and CTA style per platform
- **Compliance guardian** — inline NMLS flags, "subject to qualification" insertions, equal housing framing — per claim, not just at the end

---

## Input Contract

```json
{
  "mode": "campaign|social|email|ad|listing|segment",
  "topic": "paste your brief, headline, or talking points",
  "audience": "first_time_buyer|veteran|investor|self_employed|credit_challenged|relocating|all",
  "platforms": ["linkedin", "x", "facebook", "instagram"],
  "ab_variants": true,
  "include_listing": false,
  "tone": "urgent|educational|conversational|luxury",
  "compliance_level": "strict|standard",
  "output_format": "markdown|json"
}
```

**Campaign mode** is the primary mode. It runs all channels in a single call and returns a structured campaign brief.

---

## Output Contract

```json
{
  "campaign_brief": {
    "topic": "VA loans — zero down, no PMI",
    "audience_primary": "veteran",
    "channels_generated": ["email", "linkedin", "x", "facebook", "instagram", "ads"],
    "ab_variants": true,
    "compliance_flags": 2
  },
  "email": {
    "subject_a": "You served. Your benefit is still here.",
    "subject_b": "Most veterans leave this on the table. Don't.",
    "body_a": "...",
    "body_b": "...",
    "variant_guidance": "Run A for warm list (opens > 25%). Run B for cold list or re-engagement.",
    "compliance_note": "Add NMLS# and 'subject to qualification' to footer."
  },
  "social": {
    "linkedin": {
      "variant_a": {"body": "...", "char_count": 284, "hashtags": ["#VALoans", "#Veterans"], "cta": "..."},
      "variant_b": {"body": "...", "char_count": 247, "hashtags": ["#VALoans"], "cta": "..."},
      "ab_note": "A = value education. B = loss framing. Test B on Mon/Wed, A on Tue/Thu."
    },
    "x": {"variant_a": {"body": "...", "char_count": 238}, "variant_b": {"body": "...", "char_count": 201}, "ab_note": "..."},
    "facebook": {"variant_a": {"body": "...", "char_count": 412}, "variant_b": {"body": "...", "char_count": 389}, "ab_note": "..."},
    "instagram": {"caption_a": "...", "caption_b": "...", "hashtag_block": "..."}
  },
  "ads": [
    {
      "headline_a": "Veterans: $0 Down. No PMI. This Is Your Window.",
      "headline_b": "Still Renting? You Have a VA Benefit You Haven't Used.",
      "body": "Subject to qualification. VA funding fee may apply.",
      "compliance_note": "VA funding fee disclosure required."
    }
  ],
  "audience_segments": {
    "veteran": {"angle": "entitlement — you earned this, don't leave it unused", "key_framing": "no-cost advantage"},
    "first_time_buyer": {"angle": "education + permission — you're closer than you think", "key_framing": "down payment myth"},
    "investor": {"angle": "leverage + cash flow math", "key_framing": "equity build + carry cost"},
    "self_employed": {"angle": "bank statement alternatives exist", "key_framing": "income documentation options"},
    "credit_challenged": {"angle": "progress timeline, not rejection", "key_framing": "score improvement window"},
    "relocating": {"angle": "timing confidence — buy before you move", "key_framing": "remote pre-approval"}
  },
  "compliance_flags": [
    {"claim": "no PMI", "flag": "Add: 'PMI not required on VA loans, VA funding fee may apply'", "severity": "required"},
    {"claim": "$0 down", "flag": "Add: 'subject to qualification, funding fee may apply'", "severity": "required"}
  ]
}
```

---

## Audience Segments — Copy Angles

Each segment has a different psychological entry point. v2 generates separate copy for whichever segments you select.

| Audience | Core Fear | Core Desire | Primary Frame |
|----------|-----------|-------------|---------------|
| First-time buyer | "I can't afford it / don't qualify" | Own something, stop renting | Education + permission |
| Veteran | "I don't know what I'm entitled to" | Use what I earned | Entitlement + urgency |
| Investor | "What's the ROI?" | Build wealth through leverage | Math + deal framing |
| Self-employed | "Banks won't approve me" | Get approved without W2s | Alternative documentation |
| Credit-challenged | "My credit is too bad" | Get into a home in 6–12 months | Progress timeline + quick wins |
| Relocating | "Too risky to buy before I move" | Buy in new city before arrival | Remote pre-approval + confidence |

Run `"audience": "all"` to get all 6 angles in one call. Run a specific segment to go deep on one ICP.

---

## A/B Variant System

Every piece gets two variants:

**Variant A — Gain framing**
- Leads with the positive outcome
- Educational, builds trust
- Best for: warm audiences, LinkedIn, lead nurture
- Psychology: what you gain by acting

**Variant B — Loss framing**
- Leads with what's being left behind
- Urgency, competitive pressure
- Best for: cold audiences, Facebook ads, re-engagement
- Psychology: what you lose by waiting

Each output includes `ab_note` with platform-specific guidance on when to run which variant and what metric to watch (open rate, CTR, engagement rate).

**Example — same VA loan topic, two variants:**

*Variant A (gain):*
> "VA loans let eligible veterans buy with $0 down and no PMI. On a $350K home, that's $70K you keep in your pocket and $150–$250/month in savings over conventional. If you served and you're renting — this benefit doesn't expire, but home prices don't wait."

*Variant B (loss):*
> "Most veterans who rent are sitting on a benefit they haven't touched. $0 down, no PMI, competitive rates — and the clock isn't on your side. Every month you rent, you're paying someone else's mortgage instead of building your own equity. That math gets worse every year prices rise."

---

## Multi-Channel Campaign Flow

When mode is `campaign`, the skill builds channels in this sequence:

```
1. Parse brief → identify topic, ICP, key claims
2. Run compliance pre-check → flag any claims needing disclosure
3. Generate email (A/B subjects + bodies)
4. Generate social per platform (character-aware, CTA-adjusted)
5. Generate 3 ad hooks (A/B headlines, shared body)
6. Generate audience segment notes (which angle for which ICP)
7. If include_listing: generate property narrative
8. Attach inline compliance flags to each claim
9. Return structured campaign object
```

All channels share the same strategic brief — consistent core message, platform-adapted format.

---

## Compliance Guardian

Compliance runs inline, per claim — not as a footer disclaimer added at the end.

| Claim Type | What Gets Flagged | Action |
|------------|------------------|--------|
| Rate reference ("rates as low as X%") | Required NMLS disclosure | Replaced with directional language |
| "$0 down" | VA funding fee disclosure | Appended inline |
| "No PMI" | VA/USDA-specific | Flag added to output |
| "Qualify" / "You'll get approved" | Credit discrimination risk | Replaced with "subject to qualification" |
| DPA program references | State-specific disclaimer | Flag + "in eligible areas" appended |
| Specific loan programs | "Subject to qualification, not available in all states" | Appended |

`compliance_level: "strict"` — flags everything, zero risk
`compliance_level: "standard"` — flags high-severity items only, allows directional language

---

## Modes

| Mode | Description |
|------|-------------|
| `campaign` | Full multi-channel output from one brief |
| `social` | Social posts only (all platforms or specific) |
| `email` | Email only — subject lines + full body, A/B variants |
| `ad` | 3 ad hooks (headline A/B + body) |
| `listing` | Property narrative from bullet points or address |
| `segment` | Deep copy for one specific audience segment across all channels |

---

## Tiers

**Free** — Single-channel only (social OR email OR ad, not all), no A/B variants, no audience segmentation, compliance flags included
**Standard ($12/mo)** — All modes, 3 audience segments, A/B variants, multi-channel in one call, compliance guardian
**Pro ($37/mo)** — All modes, all 6 audience segments, full campaign output, JSON export, listing copy, custom brand voice, bulk campaign generation

---

## Integration

```bash
# Full campaign from one brief
openclaw run mortgage-marketing --mode=campaign --audience=veteran --ab-variants "VA loan zero down, no PMI, first time users"

# Segment-specific deep copy
openclaw run mortgage-marketing --mode=segment --audience=credit_challenged "90-day credit repair timeline"

# Social only, all platforms
openclaw run mortgage-marketing --mode=social --platforms=all "Fannie Mae crypto-backed mortgages"

# Via Telegram
@openclaw mortgage-marketing campaign "VA loans, veteran audience, all platforms"
```

---

## Backend

Uses `generate.py` (shared backend). Local MLX first, Haiku fallback.

```bash
LLM_BACKEND=local openclaw run mortgage-marketing "campaign brief"   # free
LLM_BACKEND=haiku openclaw run mortgage-marketing "campaign brief"   # ~$0.40 per full campaign
```

Campaign mode makes 3 generation calls (email → social → ads). In local mode: free. In Haiku mode: ~$0.40 per full campaign.

---

*v2.0.0 — Upgraded from single-channel template generator (depth 2) to multi-channel campaign engine (depth 4). Added: full campaign mode (email + social + ads from one brief), 6 audience segments with distinct psychological angles, A/B variant system (gain vs. loss framing) on every piece, inline compliance guardian per claim, channel-specific formatting.*
