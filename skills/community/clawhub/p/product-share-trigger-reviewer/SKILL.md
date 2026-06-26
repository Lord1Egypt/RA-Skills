---
name: product-share-trigger-reviewer
description: Strictly review any new skill, browser extension, app, community, course, template, or micro-product before building or launching it. Use when the user wants a traffic-source, trust, shareability, free-MVP, go/no-go, or ecosystem-fit review of a product idea or shipped draft.
---

# Product Share Trigger Reviewer

Use this skill before building, packaging, submitting, launching, or monetizing
any new skill, extension, app, community, course, template, or bundle. Be
skeptical. Treat the product as a hypothesis, not as something to defend.

For repos that include a product-share review, run it before product-fit,
design, CWS, public-page, or submission checks. In this repo the deterministic
check is:

```bash
python3 scripts/check_product_share_gate.py
```

For a single candidate:

```bash
python3 scripts/check_product_share_gate.py --product <slug>
```

## Inputs

Collect or infer:

- product type: skill, extension, app, community, course, template, or bundle,
- target user and painful moment,
- first traffic source and exact first-client path,
- why the user would trust this creator or product,
- product action that creates a visible win,
- moment when the user would want to share it,
- giveaway or free MVP plan for the first 30 to 45 days,
- traction target and stop criteria for days 30 to 60,
- related tools, skills, channels, or communities in the ecosystem,
- privacy, platform, legal, health, financial, and trademark boundaries.

If any core input is missing, state the missing assumption and review the idea
against the harshest reasonable interpretation.

## Workflow

1. State the product in one sentence:
   - audience,
   - job-to-be-done,
   - first useful artifact,
   - distribution surface.
2. Apply the hard-stop checks:
   - no exact first traffic source means `do not build yet`,
   - no trust reason means `do not ask for attention yet`,
   - no share moment means `do not depend on organic growth`,
   - no free test plan means `do not monetize yet`,
   - no stop criteria means `do not start yet`.
   If the user asks to proceed anyway, keep working only on research, rewrite,
   or review artifacts; do not submit, publish, or call the product ready.
3. Score each review dimension from 0 to 2:
   - `0`: absent or wishful,
   - `1`: plausible but vague,
   - `2`: concrete, observable, and testable within 30 days.
4. Define the share trigger with this exact structure:
   - user feels: the emotion or relief after the win,
   - user has: the artifact they can show,
   - user shares with: the specific recipient or channel,
   - user says: the shareable sentence,
   - user gains: why sharing helps the user, not the creator.
5. Red-team the idea:
   - traffic fantasy,
   - trust gap,
   - virality gap,
   - freebie-seeker risk,
   - too-many-features risk,
   - copycat or commodity risk,
   - claims or compliance risk.
6. Prescribe one of four decisions:
   - `Kill`: no credible traffic source or no painful job,
   - `Park`: useful but timing, trust, or channel is weak,
   - `Rework`: keep the audience, change the promise or share mechanic,
   - `Ship Free`: launch a narrow free MVP for 30 to 45 days.
7. If `Ship Free`, define:
   - first 10 users,
   - first 100 touches,
   - free giveaway,
   - onboarding prompt,
   - share prompt embedded in the user win,
   - day-7, day-30, and day-60 metrics,
   - shutdown threshold.
   The free MVP window must be 30 to 45 days unless the user provides measured
   existing demand.
8. Check ecosystem fit:
   - what existing asset sends traffic to it,
   - what it sends traffic to next,
   - what reusable template, skill, or proof artifact it creates,
   - what should be reinvested if it works.

## Output

Return:

- blunt verdict: `Kill`, `Park`, `Rework`, or `Ship Free`,
- one-sentence reason,
- readiness score table,
- exact traffic-source plan,
- exact trust reason,
- share-trigger definition,
- free MVP and giveaway plan,
- 30 to 60 day traction and shutdown thresholds,
- ecosystem role,
- copy fixes for the product name, promise, CTA, and share prompt,
- top 3 risks and the smallest next experiment.

When editing a repo, also update the local review artifact if one exists:

- `docs/product-share-gate-*.json` for product decisions,
- `scripts/check_product_share_gate.py` for deterministic validation,
- `package.json` scripts such as `check:product-share:*`,
- inventory or release checks so the product-share check runs before shipping.

Use concrete numbers when possible. Prefer small proof targets over revenue
claims. If the product cannot earn organic sharing, say so directly.

## Examples

Good public-safe inputs:

- "Review this new browser extension idea before I build it."
- "Check whether this Skool community has a real first traffic source and share
  moment."
- "Review this skill pack: who would share it, when, and why?"
- "Should I give this free for 45 days, kill it, or build the paid version?"

Avoid inputs that require private member lists, hidden community posts, DMs,
paid lessons, customer exports, credentials, private exports, payment data, or
unconsented testimonials. Replace them with public page copy, aggregate counts,
creator-owned notes, explicit opt-in feedback, or synthetic examples.

## Guardrails

- Do not scrape private communities, member lists, DMs, paid lessons, hidden
  pages, or account-only product data.
- Do not request, store, transform, or paste credentials, API keys, session
  cookies, payment data, private exports, account recovery data, or raw user
  identifiers.
- Do not promise revenue, profit, income, growth, conversion, virality, ranking,
  health, financial, legal, or education outcomes.
- Do not approve a product because the builder likes it; approve only when the
  traffic source, trust reason, share moment, and measurement loop are concrete.
- Do not recommend paid traffic as the first answer unless the user already has
  a proven funnel and budget.
- Do not recommend monetizing the first rough MVP. Use free distribution for 30
  to 45 days unless there is already explicit demand.
- Do not let ecosystem logic hide a weak product. Each product must still have a
  painful job, first user path, and share trigger.
