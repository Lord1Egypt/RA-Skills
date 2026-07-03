---
load: on demand — when classifying or auditing a feature
parent: ../SKILL.md
---

# Kano Classification — Full Reference

## The 2-question pair (run for every feature)

| Question | What it reveals |
|---|---|
| **Functional:** "How would the user feel if this feature IS present?" | Whether presence creates satisfaction or is invisible |
| **Dysfunctional:** "How would the user feel if this feature is MISSING?" | Whether absence creates dissatisfaction or is unnoticeable |

Both must be answered. Most miscategorizations happen because the analyst skipped the
dysfunctional question and anchored on "users say they want it" (which is what they say, not what
satisfies them).

## Full category table

| Category | Functional (present) | Dysfunctional (missing) | User reaction | Engineering stance |
|---|---|---|---|---|
| **Must-be** | "Expected, I assume it just works" | "Angry. Unacceptable. Bug." | Take for granted, furious when absent | Zero-bug. Test obsessively. Cost-of-quality investment. |
| **Performance (Linear)** | "Better is better" | "Worse is worse" | Satisfaction scales monotonically with execution | Invest to budget. Benchmark against competitors. |
| **Attractive (Delight)** | "Wow, didn't expect that" | "Don't care, never noticed" | Surprise + delight when present, neutral when absent | Build ONE as MDP. Don't over-invest — the delight is in the surprise, not the depth. |
| **Indifferent** | "Don't care" | "Don't care" | No measurable effect either way | **KILL.** Pure waste. Maintenance burden without value. |
| **Reverse** | "Annoying, why is this here?" | "Good, finally" | Active dissatisfaction when present | **KILL or make opt-in.** This is a feature that pushes users away. |
| **Questionable** | Unclear | Unclear | Cannot classify without more data | Defer classification. Run the cheapest research. Do NOT build on a guess. |

## Edge cases the analyst will hit

### "Users said they want it"
Stated preference ≠ revealed preference. Kano asks what creates satisfaction, not what people
say in interviews. If users want it but their behavior shows they do not use it after release,
it is likely Indifferent or Attractive that was never delivered as a surprise. Re-classify based
on observed behavior, not the interview quote.

### "Competitors have it"
Not enough. Competitors may have it because they never pruned. The competitive question is:
**"Does its absence cause users to switch away?"** If yes, Must-be or Performance. If no,
Irrelevant for your roadmap.

### "The CEO wants it"
Political, not analytical. Classify it honestly, then make the case in the output. If it is
Indifferent, say so. If it is Reverse, say so louder. Refusing to call a Reverse feature
"Reverse" because of politics is exactly how Experience Rot starts.

### "It is cheap to build"
Cost does not enter the Kano category. A cheap Indifferent feature is still Indifferent. Cheap
features still need care, still take design surface, still create support surface.

### "It was easy to add, so we added it"
This is the canonical Experience Rot origin. Past ease is not present justification. Every
feature in the backlog must justify itself fresh, as if it were a new proposal.

### "It is just a setting"
Settings that 95% of users never touch are Indifferent at scale. A toggle that is a power-user
feature is fine. A toggle that pretends to be a feature is waste.

## Confidence rating

For every classification, mark confidence:

- **High** — backed by user research, support ticket data, or analytics showing behavior change
- **Medium** — backed by segment knowledge, competitor analysis, or strong inference
- **Low** — guess. Needs research before commitment. Mark as Questionable and run the cheapest
  validation (5 user calls, or a 1-week fake-door test).

If more than 30% of classifications are Low confidence, the analysis is not ready. Either gather
data or pick fewer features.

## Time evolution (often forgotten)

Kano categories shift over the product lifecycle:

- **Attractive → Performance** — once a feature is "expected" (e.g., dark mode in 2020 was
  Attractive, in 2024 is Must-be for many segments)
- **Performance → Must-be** — once competitors standardize (e.g., page load time)
- **Must-be is permanent** — once Must-be, always Must-be. You do not get to retire the brakes.

Re-run Kano annually at minimum. A feature that was Attractive at launch and is now Must-be is
a zero-bug obligation, not a delight lever.

## Market-access conditions vs. user-facing features

Not everything on the v1 roadmap is a user-facing feature. Some items are
**market-access conditions** — sales, security, or legal prerequisites that
block the ability to sell, deploy, or operate the product, but don't directly
satisfy a user need.

Examples:

- **Certifications / attestations** — SOC2 Type II, ISO 27001, HIPAA, GDPR,
  PCI-DSS, FedRAMP. The *certification* is the real work; any visible UI
  (badge, trust center page) is a 1-day ticket once the cert is in hand.
- **Data residency** — EU data stays in EU. The infrastructure is the
  work; a region selector in settings is the UI.
- **Audit log export** — required for enterprise sales. The export
  infrastructure is engineering; the "export to CSV" button is the UI.
- **SSO / SAML** — required for enterprise sales. The auth protocol
  integration is the work; the "Sign in with SSO" button is the UI.

**Why this distinction matters for Kano:**

The Kano classification is a tool for *user satisfaction*. A SOC2 badge
doesn't satisfy a user — it satisfies a procurement officer. Putting
"SOC2 badge" through the Kano pair produces nonsense:

- Functional: "How does the user feel if the SOC2 badge is in the UI?" → "I
  don't care, I never look at the trust page."
- Dysfunctional: "How does the user feel if the SOC2 badge is missing?" →
  "Same as above."

The pair produces "Indifferent" for a thing that is *actually* a hard launch
gate. The mistake that follows: PM puts SOC2 badge in the kills list to
"save eng weeks," misses the fact that the enterprise sales motion is now
blocked, and the launch fails for an entirely different reason.

**How to handle it:**

1. **Run Kano only on user-facing features.** Items that are clearly
   market-access conditions go in a separate **Prerequisites** section of
   the output, with their own owner (compliance lead, security lead, GRC
   consultant) and their own dates.
2. **The UI element of a prerequisite can be Kano-classified** if it's
   visible and meaningful to the user. The SOC2 *badge* is a Performance
   feature (visible trust signal). The SOC2 *certification* is not a
   feature at all.
3. **Cross-check at the end**: any item in the Kano table whose only
   justification is "sales needs it" or "compliance requires it" is
   probably miscategorized. Move it to Prerequisites.
4. **Do not let prerequisites consume user-facing eng capacity.** The
   compliance lead owns the cert. The eng lead owns the user-facing
   features. Don't merge them onto one roadmap.

The exception: if a compliance requirement *is* itself a user-facing
feature (e.g., a customer-managed encryption key UI, a granular permission
system), then it is fair game for Kano. The test is "would a user
independently want this, or does it only matter because someone in
procurement asked?"

**Worked example:**

| Item | Type | Classification | Owner | Eng weeks |
|---|---|---|---|---|
| SOC2 Type II certification | Prerequisite | N/A (gate) | Compliance lead | 0 (parallel track) |
| SOC2 Type II badge in UI | User-facing | Performance (trust signal) | Eng | XS |
| "Export audit log" feature | User-facing | Performance / Must-be for enterprise segment | Eng | M |
| AI clause extraction | User-facing | Attractive (MDP) | Eng | M-L |

The compliance lead's 12-week cert track and the eng team's 6-week product
track run in parallel. They share dates at the launch gate. They do not
share eng capacity.
