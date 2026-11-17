# Lifecycle Messaging — Email, Push, and In-Product, Triggered by State

A lifecycle program is a state machine, not a calendar. Every message answers "the user is in state X and has not done Y" — messages that exist because it is Tuesday are the reason people unsubscribe.

**Contents:** [The State Map](#the-state-map) · [The Programs Worth Building, In Order](#the-programs-worth-building-in-order) · [Trigger Design](#trigger-design) · [Channel Choice](#channel-choice) · [Frequency and Fatigue](#frequency-and-fatigue) · [Deliverability](#deliverability) · [Consent and Compliance](#consent-and-compliance) · [Measuring a Program](#measuring-a-program) · [Traps](#traps)

**Before adding any message**, read `artifacts/lifecycle-map.md` if `## Boxes` in `~/Clawic/data/growth/memory.md` lists it, plus `## Metric Definitions` for the natural frequency the cadence is set against. Programs accumulate: without the map, the new welcome email lands on top of two others nobody remembers shipping.

## The State Map

Draw the states before the messages. Each user is in exactly one, and each state has at most one active program.

| State | Definition | Goal | Primary message |
|---|---|---|---|
| New, not activated | Signed up, no aha action, inside the activation window | Reach first value | Behaviour-triggered nudge to the exact next step (`activation.md`) |
| Activated, not habitual | Aha reached, usage below natural frequency | Form the habit | Return trigger tied to state change, not to a schedule |
| Habitual | Using at or above natural frequency | Deepen, expand, refer | Feature depth, invite prompt (`loops.md`), expansion (`monetization.md`) |
| At risk | Usage falling versus their own baseline | Interrupt the slide | Ask what changed; surface unfinished value |
| Dormant | No value action for ~3× the median gap (`retention.md`) | Resurrect on a real change | "What is new since you left", scoped to their use case |
| Churned, voluntary | Cancelled with a reason | Learn; win back on the fixed reason | Reason-specific, only when the reason is genuinely resolved |
| Churned, involuntary | Payment failed | Recover the payment | Dunning sequence (`monetization.md`) |
| Never activated, long dead | Signed up, never reached value, months old | Suppress | Nothing — these people damage deliverability |

The map is one page. If it takes more, states have been invented to justify messages.

## The Programs Worth Building, In Order

Build in this order; each earns the right to the next.

1. **Transactional and system messages.** Receipts, password resets, payment failures, invites. Highest open rates in any program and the least designed. Payment-failure recovery is usually the highest-ROI message in the entire product.
2. **Activation sequence.** Triggered by *absence* of the next step, stopped instantly when the step happens. Three messages maximum before you accept the answer.
3. **Dunning.** Retry schedule plus pre-expiry card notices. Pure recovered revenue with no acquisition cost (`monetization.md`).
4. **Return / habit triggers.** Fired by state change in the product — someone commented, the report is ready, the threshold was crossed. Something happened, not "we miss you".
5. **Expansion and upgrade.** Triggered by hitting a limit or by usage that implies the next tier, never by tenure.
6. **Resurrection.** Batched, infrequent, and only when there is a real change to announce.
7. **Newsletter / broadcast.** Last, because it is the only one that is not triggered and the one most likely to burn the list.

## Trigger Design

- **Trigger on absence with a deadline**: "signed up ≥24h ago AND no project created" — not "24h after signup", which fires at people who already succeeded.
- **Exit conditions are part of the trigger.** Every sequence names what stops it; the message that arrives after the user did the thing is the one that destroys trust in every future message.
- **Suppression is global**: one place that decides whether a user may receive anything right now (recently messaged, in dunning, in an active support conversation, unsubscribed from this category).
- **Delay to the natural moment.** A nudge sent at 3am local time is a notification the user dismisses in bulk. Send in the recipient's timezone, inside their observed active window.
- **One primary message per state**, one owner. Competing teams messaging the same state is how a user gets four emails in a morning.

## Channel Choice

| Channel | Strength | Cost of misuse | Use for |
|---|---|---|---|
| In-product | Highest relevance; the user is already there | Interrupts the task | Anything actionable while they are using the product |
| Email | Reaches everyone, carries detail, archivable | Deliverability damage is slow and hard to reverse | Activation, dunning, expansion, resurrection |
| Push (mobile) | Immediate; strongest return driver on mobile | Permission is revoked once and never returns; uninstall risk | Time-sensitive, personally relevant state changes (`mobile.md`) |
| SMS / WhatsApp | Near-certain read | Expensive, intrusive, heavily regulated | Transactional confirmations, delivery, appointments |
| Browser push | Cheap reach | Low relevance, easily disabled | Rarely worth the trust it spends |

Rule of preference: **in-product first, email for anything that must survive the session, push only for what would matter if it woke them up.**

## Frequency and Fatigue

- Set a **global frequency cap** per user per channel per week, enforced by the suppression layer, and hold marketing and product messages to the same budget.
- Watch **unsubscribe rate per send** and **push opt-out rate** as the fatigue signals; a rising unsubscribe rate at flat volume means the content stopped being relevant before the volume became the problem.
- Watch **the silent metric**: opens and clicks fall long before anyone unsubscribes. A list with high open rates and low send volume is worth more than the reverse.
- Prune. Contacts with no engagement over several send cycles should be suppressed, not re-activated harder; sending to dead addresses is what moves the whole domain into spam.

## Deliverability

Deliverability is earned infrastructure plus behaviour; there is no copy trick that survives bad reputation.

- **Authenticate**: SPF, DKIM, and DMARC aligned on the sending domain. Major mailbox providers now enforce authentication and one-click unsubscribe for bulk senders — unauthenticated bulk mail is filtered, not delivered.
- **Separate subdomains** for transactional and marketing mail, so a bad campaign cannot take down password resets.
- **Warm up** a new sending domain gradually; volume spikes from a cold domain read as a compromised account.
- **Engagement is the ranking signal.** Sending to unengaged addresses lowers placement for everyone else on the domain — pruning improves the inbox rate of the mail you care about.
- Complaint rate is the hard ceiling: providers publish thresholds in the region of a fraction of a percent, and crossing it costs weeks of recovery. One bad broadcast to a purchased list can end a domain's reputation permanently. Never buy a list.

## Consent and Compliance

Under `privacy_regime` = gdpr or both: marketing email needs demonstrable consent obtained at collection, separate from the terms checkbox, and it must be as easy to withdraw as to give. Double opt-in is not a legal requirement in itself — it is the cheapest proof that consent existed, and it improves list quality. Transactional messages sit on a different legal basis and must not carry marketing content, or they lose that status.

Under CCPA/CPRA the operative rights are notice and opt-out of sale/sharing, which affects retargeting audiences built from your list more than it affects your own email. The consent record — source, timestamp, and what was agreed to — belongs with the contact in the user's own systems, never in `~/Clawic/data/`.

## Measuring a Program

- Judge programs on the **downstream state transition**, not on opens: activation sequence → activation rate of the messaged cohort versus a hold-out; dunning → recovered revenue; resurrection → users who return *and* retain one period later.
- **Keep a permanent hold-out** of ~5-10% who receive nothing from a given program. It is the only way to know whether the sequence caused the behaviour, and it costs almost nothing (`experiments.md`).
- Open rate stopped being a clean metric once mail privacy features began pre-fetching images; treat it as directional, and measure clicks and downstream actions.
- Attribute conservatively: a user who was going to come back anyway also clicks the email.

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Drip by calendar day | Fires at people who already did the thing | Trigger on absence, exit on completion |
| No exit condition | Congratulating a user for a step they finished yesterday | Exit condition written with the trigger |
| "We miss you" with no news | Nothing changed for the user, so nothing changes | Resurrect on a real change (`retention.md`) |
| Discount as the default re-engagement | Trains waiting; damages LTV in the cohort you are measuring | Value reminder first; discount is a last resort with a deadline (`monetization.md`) |
| Marketing mail on the transactional domain | One campaign takes down password resets | Separate subdomains |
| Buying or scraping a list | Complaint rate spikes; domain reputation is very hard to recover | Never; grow the list with consent |
| Push for marketing | Permission revoked permanently, uninstall risk | Push for state changes that matter to that user |
| Judging on open rate | Inflated by privacy pre-fetching; says nothing about value | Downstream transition versus hold-out |

**After shipping or changing any program**, write it back in the same turn: the state, trigger, exit condition, channel and owner into `~/Clawic/data/growth/artifacts/lifecycle-map.md`, born as its own file with the first state and never a section of `memory.md` — it is read whole, and only when messaging comes up — with its `## Boxes` line in the same turn (`memory-template.md`). Program results with their hold-out comparison go to `experiments/<year>.md`; a deliverability incident and its recovery goes to `## Pain Points` with the date, because the next domain decision depends on it. Never store an ESP API key or a list export — pointer only (`env:ESP_API_KEY`), and aggregates instead of rows.
