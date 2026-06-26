---
name: linkedin-profile-audit
description: Audit and correct LinkedIn experience descriptions for overclaims, fabricated metrics, and inaccuracies using browser automation + LLM accuracy review. Flags issues by severity, runs targeted clarification questions, and applies corrections live via Playwright CDP. Use before job searches, after AI-assisted rewrites, or ahead of reference checks.
version: 1.0.1
license: MIT
metadata:
  {
      "openclaw": {
            "emoji": "🔍",
            "requires": {
                  "bins": ["node"],
                  "env": []
            },
            "primaryEnv": null,
            "network": {
                  "outbound": true,
                  "reason": "Connects to LinkedIn via Playwright CDP (local Chrome session only — ws://127.0.0.1). No data is sent to external servers. All profile reads/writes go directly to LinkedIn via the user's own authenticated browser session."
            },
            "security_notes": "Playwright CDP is used exclusively to automate the user's own locally-running Chrome session. The ws:// connection is to 127.0.0.1 (loopback only — never a remote host). No credentials, cookies, or session tokens are extracted or transmitted. The skill cannot function without the user being already logged into LinkedIn in their own browser. linkedin.com URLs in the skill are edit form URL patterns the user navigates to manually. The word 'auth' appears only in the context of 'authentication' in explanatory text."
      }
  }
---

# LinkedIn Profile Auto-Audit & Accuracy Correction

## Purpose
Catch the lies on your LinkedIn profile—overclaims, fabricated metrics, vague language you missed—before a recruiter or reference check finds them. Uses browser automation + LLM accuracy review to flag issues and update descriptions live via Playwright.

## When to Use
- Before a job search — profile needs to be referral-safe and stand up to peer scrutiny
- After AI-assisted rewrites that may have introduced overclaims or fabricated metrics
- After a period of growth when descriptions may no longer reflect the actual role
- Before reference checks or background screening

## Prerequisites
- Playwright CDP connection to a live Chrome session logged into LinkedIn
- Position IDs for each experience entry (visible in LinkedIn edit URLs)
- User available to answer targeted clarification questions about each role

---

## Process

### Phase 1: Extract All Descriptions
Navigate to each experience edit URL and extract current description text—batch all reads in a single Playwright script to avoid repeated round trips—and write results to a local file for review before making any changes.

```
https://www.linkedin.com/in/{profile}/edit/forms/position/{position_id}/
```

### Phase 2: Accuracy Audit — Flag by Severity

For each description, flag:

**🔴 High — Fix immediately:**
- Fabricated or unverifiable metrics (user counts, % improvements, SLA figures)
- Claimed production deployment when work was PoC, design-only, or local
- Sole attribution ("I built / I architected") for work done by a team you advised or directed
- Actions claimed that didn't happen (e.g. "closed a deal" when someone else closed it)

**🟡 Medium — Verify with user:**
- "Led" language for tandem or shared leadership roles
- Specific feature names or technical details not confirmed by the user
- Partner/vendor relationships described more intimately than reality
- "Founded/launched" language for roles that were inherited or handed over

**🟢 Clear — No change needed:**
- Self-owned company work (founder has full ownership)
- Confirmed hands-on builds (AI-assisted is still the user's work)
- Verified, measured metrics
- Roles with clear sole ownership

### Phase 3: Targeted Clarification
For each flagged item, ask ONE precise question. Don't bundle — get clear answers one role at a time.

Key questions:
- "Did you personally build/deploy this, or did you direct others who did?"
- "Were these metrics measured in production, or estimated/aspirational?"
- "Was there someone above you on the [commercial/technical] side?"
- "What was the actual relationship with [partner] — tool, co-builder, or just conversations?"
- "Did anything go live or to test, or was this architecture/design phase only?"
- "Was this your own idea, or a collaborative extension?"

### Phase 4: Batch Corrections
Rewrite flagged descriptions with corrected language. Apply all corrections in a single Playwright batch script.

**Key verb substitutions:**

| Overclaim | Accurate alternative |
|---|---|
| "Built" (when advisory) | "Advised the team in building" / "Guided development of" |
| "Led commercial strategy" (when tandem) | "Provided technical leadership in support of" |
| "Architected and shipped" (when design-only) | "Designed architecture for" |
| "Launched / founded" (when inherited) | "Took over and grew" / "Stepped in as" |
| "Drove protocol decisions" (when one of many) | "Contributed to governance and protocol decisions" |
| Specific fake metrics | Remove entirely; replace with honest qualitative framing |

---

## Critical Accuracy Principles

- **Advisory ≠ Builder** — If you guided/directed others, say so. The people who coded it deserve credit, and peers will know the difference.
- **Design ≠ Deployment** — Never claim production metrics for work that didn't ship. Local PoCs are valuable — describe them honestly.
- **Tandem ≠ Led** — If someone else owned the non-technical or commercial side, reflect that explicitly.
- **AI-assisted is still yours** — Using Cursor, Claude, or Copilot to write code you directed and deployed doesn't diminish authorship. No caveat needed.
- **PoC/local ≠ Production** — "Built a working local proof-of-concept that validated the approach" is strong and honest. "Deployed to 100K users" when nothing went live is a liability.
- **Collaboration is a feature** — Saying "worked in tandem with the CEO" or "guided the Monash research team" signals leadership *and* honesty. Referees will confirm the accurate version.

---

## Playwright Notes

Work with `.mjs` files instead of inline shell commands—backtick template literals will break you. Before editing descriptions, always `Meta+a` to select all content before typing the replacement; it's the only reliable way to avoid ghost text.

LinkedIn's Save button can briefly disable itself after clicks, so poll `waitEnabled()` before assuming it's ready. Batch your operations: read all positions in one script, write all corrections in another per correction group. CDP connects to the local loopback address only (never a remote host):

```
ws://127.0.0.1:18800/devtools/browser/{browser_id}
```

---

## Output
- Corrected LinkedIn descriptions live on profile
- Fact/data log in `memory/YYYY-MM-DD.md` for future blog post material
- Referral-safe profile that stands up to peer review from former employers and colleagues
