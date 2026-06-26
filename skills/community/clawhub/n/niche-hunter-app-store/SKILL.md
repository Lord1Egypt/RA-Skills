---
name: niche-hunter-app-store
description: NicheHunter Ultra — Headless App Store Market Intelligence engine for OpenClaw (VPS). Detects underserved niches, analyzes competitors, validates monetization signals, scores opportunities quantitatively, and generates investor-grade MVP PRDs. Optimized for Telegram.
metadata:
  tags: app-store, market-intelligence, competitor-analysis, revenue-validation, scoring, prd, rork, openclaw, telegram
---

# NicheHunter Ultra — Market Intelligence Mode

Designed for:
- OpenClaw running in a VPS (headless)
- Telegram interaction
- No interactive browser required

---

# TOOL REQUIREMENTS

At least ONE of the following must be available:

- web_search
- web_fetch
- curl (HTTP request capability)

If none are available → STOP execution.

---

# TOOL PRIORITY ORDER

1) web_search  
2) web_fetch  
3) curl (last fallback)

Always prefer higher-priority tools when available.

---

# TOOL ADAPTATION LOGIC

If web_search is available:
→ Use for discovery (charts, competitors, reviews, revenue signals).

If web_fetch is available:
→ Use for structured extraction.

If ONLY web_fetch is available:
→ Fetch official App Store category pages directly.
→ Extract app listings and derive competitors.

If ONLY curl is available:
→ Perform raw HTTP GET requests.
→ Parse HTML manually for:
   - App names
   - Rating counts
   - Pricing info
→ Confirm signals using multiple sources when possible.

Never fail solely due to missing web_search.

---

# EXECUTION DISCIPLINE

- Max 18 web_search calls
- Max 20 total URLs analyzed
- Max 8 competitors per niche
- Max 20 reviews per app (prioritize 1★ and 3★)
- No duplicate queries
- Proxy revenue must be labeled with confidence level
- No speculation presented as fact

---

# PIPELINE

1) Category Definition  
2) Market Demand Discovery  
3) Competitor Intelligence  
4) Gap Pattern Extraction  
5) Quantitative Scoring  
6) MARKET INTELLIGENCE REPORT  
7) PRD (after user selection)

Each step MUST output a structured checkpoint.

---

# CHECKPOINT FORMAT (STRICT STATE FORMAT)

Checkpoints are for STATE only.  
No conclusions. No scoring. No hype.

Must use this exact structure:

--- CHECKPOINT ---
Step: {number}
Category: {category}

Micro-niches identified:
• {niche 1}
• {niche 2}

Competitors analyzed ({count}/{max}):
• {App} — {ratings} — {core feature}
• {App} — {ratings} — {core feature}

Observed signals:
• {signal 1}
• {signal 2}

Gap hypotheses (not conclusions):
• {hypothesis 1}
• {hypothesis 2}

Confidence (intermediate): {Low | Medium | High}

Next Step: {next}
--- END CHECKPOINT ---

The checkpoint must NOT contain:
- Revenue estimates
- Final ranking
- Absolute claims ("NO EXISTE")
- Scoring values

---

# REVENUE ESTIMATION MODEL

If direct revenue found → use it.

If not:

Freemium:
Estimated installs ≈ ratings × 100

Paid:
Estimated installs ≈ ratings × 40

Revenue estimate:
installs × 3% × subscription_price

Confidence levels:
High (direct source)
Medium (strong proxy)
Low (weak signal)

Proxy must always be labeled.

---

# QUANTITATIVE SCORING MODEL

Score each opportunity 0–10:

Demand Strength (35%)
Gap Clarity (30%)
Monetization Viability (20%)
Build Simplicity (15%)

Weighted Score =
(demand × 0.35) +
(gap × 0.30) +
(monetization × 0.20) +
(build × 0.15)

Scores must be justified with evidence.

---

# STRICT FORMAT ENFORCEMENT

The assistant is STRICTLY FORBIDDEN from:

- Using ASCII tables
- Using column separators like "|"
- Using monospaced grid layouts
- Using star-only scoring (⭐⭐⭐)
- Formatting in horizontal table style

No ASCII tables are allowed under any circumstance.
Do not use "|" separators.
All output must be vertical structured blocks.

If a table or ASCII grid appears, the assistant must immediately rewrite the output in vertical structured format.

---

# OUTPUT ENFORCEMENT — TELEGRAM ULTRA FORMAT

Final report MUST use this structure:

════════════════════════════
📊 MARKET INTELLIGENCE REPORT
Category: {Category}
Research Confidence: {High | Medium | Low}
Competitors Analyzed: {Number}
════════════════════════════

🥇 OPPORTUNITY #1 — {Name}

🎯 Strategic Positioning  
{One concise positioning sentence}

━━━━━━━━━━━━━━━━━━━━━━
📈 Demand Analysis

• Top competitors analyzed: {names}  
• Rating range observed: {range}  
• Saturation level: {Low | Medium | High}  
• Demand summary: {1–2 lines}

━━━━━━━━━━━━━━━━━━━━━━
💰 Monetization Analysis

• Pricing benchmark: {range}  
• Revenue signals: {direct or proxy explanation}  
• Install estimate logic: {formula used}  
• Conversion assumption: {percentage}  
• Estimated revenue range: {range}  
• Confidence: {High | Medium | Low}

━━━━━━━━━━━━━━━━━━━━━━
🧩 Gap Intelligence

• Repeated complaint themes:
  - {theme 1}
  - {theme 2}

• Missing feature overlap:
  - {feature 1}
  - {feature 2}

• Structural competitor weakness:
  {brief explanation}

Primary Wedge:
{1–2 differentiators}

━━━━━━━━━━━━━━━━━━━━━━
⚙️ Build Assessment

Complexity: {Low | Medium | High}  
Reasoning: {brief explanation}

Risk Level: {Low | Medium | High}  
Primary Risk: {brief explanation}

━━━━━━━━━━━━━━━━━━━━━━
📊 Quantitative Scoring

Demand Strength: X/10  
Gap Clarity: X/10  
Monetization Viability: X/10  
Build Simplicity: X/10  

Weighted Score: X.X / 10  

Overall Attractiveness: {Strong | Moderate | Speculative}

════════════════════════════

🥈 OPPORTUNITY #2 — {Name}
(Condensed but same analytical structure)

════════════════════════════

🥉 OPPORTUNITY #3 — {Name}
(Condensed but same analytical structure)

════════════════════════════

🏁 STRATEGIC CONCLUSION

• Why #1 ranks highest  
• Where defensibility exists  
• Key leverage insight  

Data-based reasoning only.

After delivering this report, ask the user:
Choose #1 / #2 / #3 to generate the PRD.

---

# PRD REQUIREMENTS

After selection, generate:

1) Executive Summary  
2) Market Validation Summary  
3) Target Personas  
4) Core Differentiator (Wedge)  
5) MVP Feature Groups  
6) Screen Architecture (Expo Router structure)  
7) Monetization Strategy  
8) Tech Stack:
   - Expo SDK 52+
   - TypeScript
   - Expo Router
9) Design System:
   - Hex colors mandatory
10) KPIs  
11) Risks & Mitigations  

PRD must be:
- Concrete
- UI-specific
- Copy-paste ready for Rork
- No fluff
