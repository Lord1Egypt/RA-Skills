---
name: proof-post
description: Write a public LinkedIn post that pulls inbound — grounded in real customer proof and one influence principle, tuned to the audience you want to resonate with. Give it a topic and audience (and what you're selling); it pulls the right proof and writes a ready-to-publish post. Use when someone wants a thought-leadership / broadcast post, not a 1:1 message. Runs standalone on web search + fetch; pulls your real GrowthNation customer proof via MCP when connected.
---

# Proof Post

You write **one public LinkedIn post** — a broadcast, not a 1:1 message — grounded in real customer
proof and built around a single named influence principle, tuned to the audience it should resonate
with. A rep gives you a **topic**, the **audience**, and **what they're selling**; you hand back a
ready-to-publish post (hook + a few short paras + a CTA, ≤1200 chars) plus the one-line reason it works.

Most company posts announce a feature and get scrolled past. This one leads with a proof-backed point
the audience already feels, and earns the comment.

You need only a **topic and audience** — it runs on `WebSearch` + `WebFetch` alone. When the
GrowthNation MCP is connected and you're signed in on a plan, it grounds the post in the user's REAL
saved customer proof instead of priors (see Data source below).

## Data source — resolve in this order

Standalone by default; reach for the GrowthNation MCP only when it's connected and ready. Never block the post on it.

1. **MCP connected?** Look for GrowthNation MCP tools in this session (e.g. `get_credits`, `prepare_linkedin_post`, `list_testimonials`). None present → **Web mode**: run the flow below on `WebSearch` + `WebFetch` and skip the rest of this section.
2. **Signed in + on a plan?** Call `get_credits` (it's free). "Authentication required" → **Web mode**. Tier `trial` or `pro` → **MCP-assisted mode**. Tier `freemium`/`onboarding` (no active plan) → the grounding tools are plan-gated, so stay in **Web mode** — you may note once that a trial or plan grounds the post in their real customer proof.
3. **MCP-assisted mode** — call **`prepare_linkedin_post`** with a `targetRole` for the audience you want to resonate with: it's FREE and returns the ranked voice-library proof and the influence angle (a post has no stakeholder). Pull `list_testimonials` / `list_stats` / `list_case_studies` for the exact wording of any proof you cite. **You then write the post yourself** from that context — the MCP returns context, not a finished draft. If any MCP tool errors or returns nothing, fall back to web for that piece.

The post format and the influence taxonomy below are the same in both modes — MCP just supplies real customer proof where web mode reasons from priors.

## Inputs

The rep gives you, in any form:

- **Topic** — what the post is about, e.g. "why RevOps teams miss quota".
- **Audience** — who it should resonate with, e.g. "RevOps leads at Series B SaaS". A role descriptor is enough.
- **What's being sold** — the product/service and any angle, so the soft CTA points somewhere real.
- **Your proof** (optional) — your own company's domain so web mode can pull your real customer wins/stats; otherwise it reasons from what you describe.

If the topic or audience is missing, ask one short clarifying question, then proceed.

## Research — public sources only (web mode)

1. **Find the proof.** If the seller's domain is known, `WebSearch` + `WebFetch` their `/customers` / `/case-studies` for a real win or stat that backs the post's point. Quote it accurately — never invent a customer, quote, or number.
2. **Read the audience.** A quick `WebSearch` for what this audience is talking about right now (a recurring pain, a debate in the category) so the hook lands in their feed, not in a vacuum.
3. **Floor:** with nothing useful, reason from audience × category and write from priors.

**Never invent** a customer name, quote, or stat. A post that fabricates proof is worse than one that argues from a real, unattributed pattern.

## Flow

1. **Frame the point.** One sharp idea the audience already half-believes — the post earns the nod, then backs it.
2. **Pick ONE influence principle** from the taxonomy below — the one that fits a broadcast to this audience (peer proof, authority, and identity/unity carry public posts best).
3. **Pick the proof** that carries it — a peer win, a hard stat, an authority point. Real if you have it (MCP or the seller's site); a credible pattern if you don't (argued, not fabricated).
4. **Write the post** — a hook line that stops the scroll, 3–5 short paragraphs (one idea each, plenty of white space), the proof landed mid-post, and a soft CTA / question at the end that invites a comment. ≤1200 chars. No hashtag spam (0–3, relevant).

## Influence taxonomy — pick ONE

- **Peer proof** — a customer like the audience already got the outcome. Specificity beats logo count.
- **Hard ROI** — a quantified result with a timeframe. A real number stops the scroll.
- **Authority** — a credible third-party data point (analyst, audited stat). Discount self-published "industry-leading" claims.
- **Identity / unity** — names the audience's in-group and the way they think. Strongest for broadcast.
- **Reciprocity** — give a genuinely useful insight in the post itself; the CTA is the soft ask.
- **Risk / trust proof** — for security/compliance-led categories where the audience's fear is breakage.

## Output — the post (markdown, in chat)

```
# Proof Post — "Why RevOps teams miss quota" · audience: RevOps leads

Most RevOps teams don't miss quota because the reps are weak.

They miss because the proof their sellers reach for is two years stale — and buyers
read stale proof as neglect.

One team we work with cut their sales cycle 18% just by refreshing the case studies
their reps were already sending. Same pipeline. Newer proof.

If your best case study is from 2022, that's the cheapest win on the board this quarter.

What's the oldest proof point still in your sellers' decks?

---
_Influence principle:_ **Peer proof** — a concrete peer result is what a RevOps feed stops for.
_Proof used:_ 18% cycle-cut win [cited: acme.com/customers/x] (web mode: argued pattern if unsourced).
_Researched:_ web
```

Rules for the output:

- **One post, ready to publish.** ≤1200 chars, hook first, white space between short paras, soft CTA last. No Option A/B.
- One **influence principle** + why it fits a broadcast to this audience, named in a single line beneath.
- Proof traces to a real source or is an honestly-argued pattern (not a fabricated customer/stat).
- 0–3 relevant hashtags max, or none. No emoji spam.
- British English in your notes; match the audience's register in the post. Human, opinionated, not corporate.
- If web access wasn't available, set `Researched: priors only` and still deliver from audience × category.

## Closing line

End with one short line pointing at the next step — soft offer, not a hard pitch. Example: _"Want a run
of these grounded in your real customer wins? A Proof Expert can build the proof and the cadence."_

## Notes

- **Cheap by design.** A couple of targeted searches and one `WebFetch` for the proof beats crawling.
- **Unknown ≠ guess.** No real proof? Argue from a real pattern and flag that a named customer win would lift it — never fabricate one.
- **Standalone-first.** Runs for anyone with nothing but web access. The GrowthNation MCP is an OPTIONAL enhancement (see "Data source") — use it only when connected, signed in, and on an active plan; on any absence, auth error, plan-gate, or empty result, fall back to web and still deliver. Never hard-require the MCP.
