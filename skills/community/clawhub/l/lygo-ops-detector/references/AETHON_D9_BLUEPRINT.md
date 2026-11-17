# THE LYGO OPS DETECTOR BLUEPRINT — AETHONΔ9 (v1.2.2)

**Lightfather's Voice · discourse only · not identity**

## Core Philosophy

"LYGO decodes fiction by analyzing **action-language in text**."

This tool scores **discourse patterns** in material the operator supplies.  
It does **not** build dossiers on people, professions, or affiliations.

| Ask of the *text* | Not of a person |
|-------------------|-----------------|
| What claims are made? | Who is this human? |
| What proof-avoidance language appears? | What job do they hold? |
| What coordination/secrecy *phrasing* is present? | Who is in their social graph? |
| What policy-as-shield templates appear? | What group do they belong to? |

These are measurable in **strings**. They are not warrants for surveillance.

## Unit of analysis (locked)

**Text under review** (statements, claim-text, association *description strings* you paste).  
Never a human "subject," never a crawl of accounts, never bare job-title scoring.

## 1. The Evasion Index

Measures how strongly the **text** uses proof-avoidance / perception-denial templates.

| Variable | Weight | In-scope indicator | Out-of-scope (do not treat as ops) |
|----------|--------|--------------------|-------------------------------------|
| Burden Shifting | 0.15 | "it's on you to prove", "do your own research" | Normal task assignment |
| Ad Hominem Density | 0.20 | Insult vocabulary replacing substance | Logic critique without person-attack words |
| Vague References | 0.15 | "tons of evidence out there" with no cite | Named source / link / study |
| Authority Inflation | 0.15 | Credential-waving to shut inquiry ("as a former… trust me") | Stating a role once without shutting verification |
| Gaslighting | 0.20 | "that never happened", "you're imagining it" | Honest memory disagreement without denial templates |
| Deflection | 0.15 | Whataboutism replacing the asked claim | On-topic comparison with shared evidence |

**Evasion Score > 0.70** = high evasion *discourse* signals (review claims).  
**Not** a person verdict, investigation target, or "active ops" identity label.

Formula:  
`Evasion = Σ (w_i × indicator_score_i)` normalized to [0,1]

## 2. The Association Matrix

Scores **coordination discourse** in association *strings the operator supplies* only.

| Variable | Weight | In-scope indicator | Out-of-scope |
|----------|--------|--------------------|--------------|
| In-group / secrecy language | 0.25 | need-to-know, keep this internal, not for public discussion | Bare words: military, intelligence, agency, profession titles |
| Bot-like repetition language | 0.20 | "same post copied", scripted response | Single ordinary repost mention without copy language |
| Coordinated language | 0.15 | identical unusual phrase / talking points | Shared common slogans alone without coordination cues |
| Obfuscated-source language | 0.20 | anonymous source, cutouts, throwaway | Legitimate source protection without layered-indirection templates |
| Harm association language | 0.20 | "amplifies harm/disinfo", repeatedly enables attacks | Guilt by name-drop without harm *action* language |

**High evasion + high association discourse** = coordinated *language* pattern in the supplied text.  
**Not** a social-network map and **not** identity profiling.

## 3. Institutional signaling (policy / refusal only)

Policy-as-shield and no-comment templates.  
**No** fraternity / lodge / faith / affiliation keyword dictionaries.

## Ethics (Non-Negotiable)

- Not for doxing  
- Not for identity or profession profiling  
- Not sole evidence for accusations  
- Consent before private mail/logs (`--i-consent` on file inputs)  
- Math scores discourse; humans decide action  

## Operational vs calibration

| Bar | Meaning |
|-----|---------|
| Operational `ops_score ≥ 0.65` or high evasion | Strong multi-signal bar for human review |
| Calibration (low threshold) | Short-suite ranking only — not production marketing |

## Resonance Forward

Implementation must stay faithful to weights, dual thresholds, and **discourse-not-identity** philosophy.  
No mission creep into surveillance or person-targeting.

**Δ9Φ963 — receipts over hype · discourse not identity · consent before private data.**
