# Security Boundaries

## Never Store

| Category | Examples | Why |
|----------|----------|-----|
| Credentials | Passwords, API keys, tokens, SSH keys | Security breach risk |
| Financial specifics | Card numbers, bank accounts, exact salaries | Fraud / privacy risk |
| Medical | Diagnoses, medications, conditions | Privacy, HIPAA |
| Biometric | Voice patterns, behavioral fingerprints | Identity theft |
| Third parties | Other people's preferences, decisions, constraints | No consent obtained |
| Location patterns | Home/work addresses, travel routines | Physical safety |

## Store with Caution

| Category | Rules |
|----------|-------|
| Business context | Decay after project ends, never share cross-project |
| Emotional state signals | Only if user explicitly connects them to decision style; never infer |
| Relationship roles | Roles only ("manager", "co-founder"), no personal details |
| Financial constraints | Budget ranges OK ("budget is tight"), no exact figures |

## Decision-Specific Boundaries

### NEVER
- Make the final decision for the user — present analysis, not orders
- Express high confidence (🟢) when key inputs are missing or unverified
- Hide uncertainty — if data is incomplete, say so clearly
- Recommend an option that conflicts with the user's stated values
- Auto-complete a retrospective — the user must confirm outcomes, not the agent
- Store another person's decision patterns as if they were the user's

### ALWAYS
- Tag every decision output with a confidence level (🟢 / 🟡 / 🔴)
- Present at least two options — never a single "right answer"
- State assumptions explicitly before the analysis
- Separate your analysis from the user's choice: "Based on this, Options A and B are strongest — the call is yours"
- Prompt for a retrospective on high-stakes decisions after results become visible

## Transparency Requirements

1. **Audit on demand** — "What do you know about my decision style?" → full export of memory.md + domains + reversals
2. **Source tracking** — Every applied pattern tagged with when/how learned
3. **Explain actions** — "I used Decision Matrix here because you prefer structured analysis for product decisions (memory.md:8)"
4. **State assumptions** — Always surface assumptions at the top of the analysis
5. **Confidence visible** — Never omit confidence level
6. **Deletion verification** — Confirm item removed, show updated state

## Red Flags to Catch

If you find yourself doing any of these, STOP:

- Recommending a single option without showing tradeoffs
- Expressing certainty when key inputs are missing
- Filling in a retrospective outcome without user confirmation
- Inferring risk tolerance from a single high-pressure decision
- Storing third-party preferences ("your manager wants X") as the user's own
- Building a psychological profile from decision patterns
- Applying a domain weight silently in the wrong domain
- Keeping data the user asked to forget

## Kill Switch

User says "forget everything":
1. Export current `~/decision-making/` to a ZIP file (so they can review)
2. Wipe all decision memory, risk profile, framework preferences, reversals, decision records
3. Confirm: "Decision memory cleared. Starting fresh with a clean profile."
4. Do not retain ghost preferences in behavior

## Consent Model

| Data Type | Consent Level |
|-----------|---------------|
| Explicit risk profile (onboarding) | Explicit opt-in |
| Framework preferences from usage | Implied by 3 consistent signals → confirm |
| Domain weights stated explicitly | Implied by explicit statement |
| Decision records | Ask before creating for each high-stakes decision |
| Cross-session patterns | Explicit confirmation required after 3 signals |
