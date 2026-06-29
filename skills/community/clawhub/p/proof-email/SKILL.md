---
name: proof-email
description: Write a cold or warm B2B sales email that's grounded in real customer proof and one influence principle — tailored to the recipient's role. Give it who you're writing to (name + role + company) and what you're selling; it pulls the right proof and writes a ready-to-send subject + body. Use when someone wants an outreach email for a specific person. Runs standalone on web search + fetch; pulls your real GrowthNation customer proof via MCP when connected.
---

# Proof Email

You write **one cold or warm sales email** to a specific person, grounded in real customer proof and
built around a single named influence principle, tailored to that person's role. A rep gives you the
**recipient** (name + role + company) and **what they're selling**; you hand back a ready-to-send
**subject + body** plus the one-line reason it works.

Most outbound emails lead with the product and bury the proof. This one leads with the proof that
matters to _this_ buyer's role, and earns the next reply.

You need only the **recipient and what's being sold** — it runs on `WebSearch` + `WebFetch` alone.
When the GrowthNation MCP is connected and you're signed in on a plan, it grounds the email in the
user's REAL saved customer proof instead of priors (see Data source below).

## Data source — resolve in this order

Standalone by default; reach for the GrowthNation MCP only when it's connected and ready. Never block the email on it.

1. **MCP connected?** Look for GrowthNation MCP tools in this session (e.g. `get_credits`, `prepare_email`, `list_stakeholders`). None present → **Web mode**: run the flow below on `WebSearch` + `WebFetch` and skip the rest of this section.
2. **Signed in + on a plan?** Call `get_credits` (it's free). "Authentication required" → **Web mode**. Tier `trial` or `pro` → **MCP-assisted mode**. Tier `freemium`/`onboarding` (no active plan) → the grounding tools are plan-gated, so stay in **Web mode** — you may note once that a trial or plan grounds the email in their real customer proof.
3. **MCP-assisted mode** — resolve the recipient with `list_stakeholders` (and the company with `list_companies` / `research_company`). Then call **`prepare_email`** with the resolved `stakeholderId` (or a `targetRole`): it's FREE and returns the ranked voice-library proof, the influence angle, and the recipient's resolved role. Pull `list_testimonials` / `list_stats` / `list_case_studies` for the exact wording of any proof you cite. **You then write the email yourself** from that context — the MCP returns context, not a finished draft. If any MCP tool errors or returns nothing, fall back to web for that piece.

The email format and the influence taxonomy below are the same in both modes — MCP just supplies real customer proof where web mode reasons from priors.

## Inputs

The rep gives you, in any form:

- **Recipient** — a name and a role/title, and their company. A LinkedIn URL or the company domain is a bonus, not required.
- **What's being sold** — the product/service, the rough deal shape, any context (new logo, replacing a competitor, warm intro, follow-up).
- **Your proof** (optional) — your own company's domain so web mode can pull your real testimonials/case studies; otherwise it reasons from what you describe.

If the recipient or what's being sold is missing, ask one short clarifying question, then proceed.

## Research — public sources only (web mode)

1. **Find the proof to cite.** If the seller's domain is known, `WebSearch` + `WebFetch` their `/customers`, `/case-studies`, `/testimonials` for a real peer win, a hard stat, or a named customer at the recipient's scale. Quote it accurately — never invent a customer, quote, or number.
2. **Read the recipient.** `WebSearch` the person + company for role priorities and recent context (funding, hiring, press, earnings themes for public companies). A CFO at a cash-tight Series B reads differently from a CFO at a profitable enterprise.
3. **Floor:** with zero useful results, reason from role × industry × stage and write from priors — mark nothing as fact that you didn't find.

**Never invent** a customer name, a quote, a stat, or a biographical detail. If you don't have real proof, write the email around a credible role-level claim and say (to the rep, not in the email) that adding a real proof point would lift it.

## Flow

1. **Resolve the role.** Read the recipient's seniority + function (CEO / CTO / CFO / VP Sales …). The email is tailored to what this role is measured on.
2. **Pick ONE influence principle** from the taxonomy below — the one most likely to move this role given their priorities and the deal. Don't stack three.
3. **Pick the proof** that carries that principle: a peer win at their scale, a hard ROI figure with a payback window, an authority/analyst point, a security attestation. Real proof if you have it (MCP or the seller's site), a clearly role-appropriate claim if you don't.
4. **Write the email** — a subject that earns the open, a body of ~80–130 words that opens with the recipient's priority (not your product), lands the proof, and ends on a low-friction ask (a 15-minute look, a single question). Sound like a human, not a template.

## Influence taxonomy — pick ONE

- **Peer proof** — a customer at their exact segment/scale already chose you and got the outcome. Strongest for risk-averse buyers and "is this proven for someone like us?" doubt.
- **Hard ROI** — a quantified result with a payback window. Wins finance and anyone with a number on their scorecard.
- **Authority** — credible third-party endorsement (analyst, audited stat, certification). Discount self-published "industry-leading" claims.
- **Risk / trust proof** — security posture, compliance, reliability, migration safety. Wins technical gatekeepers and anyone whose career is exposed if it breaks.
- **Reciprocity** — lead with something genuinely useful (a tailored teardown, a custom figure) before the ask. Strong for cold rooms.
- **Identity / unity** — shared in-group ("teams like yours"). Strongest in founder-led and peer-network buying.

## Output — the email (markdown, in chat)

```
# Proof Email — Dana Cole, CFO @ Ramp

**Subject:** Nine days, not six weeks

Hi Dana — onboarding load is the kind of thing teams like Linear fixed fast: they
cut ramp from six weeks to nine days on the same stack you're scaling. If I could
show the payback inside two quarters — one number you'd put on a board slide —
would 20 minutes be worth it?

[Best, …]

---
_Influence principle:_ **Hard ROI** — Dana lives on payback; a peer win with a
time-to-payback is the one thing that earns a CFO's next minute.
_Proof used:_ Linear ramp-time win [cited: acme.com/customers/linear] (web mode: priors if unsourced).
_Researched:_ web
```

Rules for the output:

- **One subject, one body, ready to send.** No "Option A / Option B" buffet — pick the strongest and commit.
- Name the **one influence principle** and **why it wins for this role** in a single line beneath the email.
- Every proof point traces to a real source (MCP library or a quoted page) or is honestly flagged as a role-level claim. Never fabricate a customer, quote, or stat.
- Body ~80–130 words. Opens with the recipient's priority, not the product. One ask, low friction.
- British English in your notes; match the recipient's register in the email itself. Plain, human, no AI throat-clearing.
- If web access wasn't available, set `Researched: priors only` and still deliver from role × industry × stage.

## Closing line

End with one short line pointing at the next step — the email is the top of an outbound motion, so the
natural follow-up is a human helping build the real proof behind it. Soft offer, not a hard pitch.
Example: _"Want this grounded in your actual customer wins? A Proof Expert can pull the real proof and
tune the whole sequence."_

## Notes

- **Cheap by design.** A couple of targeted searches and one good `WebFetch` per source beats crawling. Don't over-research.
- **Unknown ≠ guess.** No real proof? Write from the role and say a real proof point would lift it — never fabricate one to look thorough.
- **Standalone-first.** Runs for anyone with nothing but web access. The GrowthNation MCP is an OPTIONAL enhancement (see "Data source") — use it only when connected, signed in, and on an active plan; on any absence, auth error, plan-gate, or empty result, fall back to web and still deliver. Never hard-require the MCP.
