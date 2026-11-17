# Referrals — Programs That Produce Users, Not Fraud

A referral program converts existing affection into new users. It cannot create the affection. Every failed program in this domain shares one cause: it was built before anyone loved the product, and the incentive then bought people who would never have come.

**Contents:** [Preconditions](#preconditions) · [Word of Mouth vs Referral vs Affiliate](#word-of-mouth-vs-referral-vs-affiliate) · [The Five Design Decisions](#the-five-design-decisions) · [Incentive Sizing](#incentive-sizing) · [Placement and Timing](#placement-and-timing) · [Attribution Mechanics](#attribution-mechanics) · [Fraud Controls](#fraud-controls) · [Measuring It](#measuring-it) · [Traps](#traps)

**Before designing a program**, read `## Retention` and `## Channels` in `~/Clawic/data/growth/memory.md`, and `artifacts/referral-program.md` if `## Boxes` lists it. The retention curve decides whether this is a growth lever or a fraud budget.

## Preconditions

Three, all required. A program launched without them will produce a number that looks good for six weeks and a cohort that never activates.

1. **The retention curve flattens** for the segment you will ask (`retention.md`). People do not recommend something they are about to abandon.
2. **A moment of realised value exists** and you can detect it as an event — that moment is where the ask goes.
3. **The referred user can experience value quickly**, ideally through the thing that was shared. If your onboarding takes a week, referral traffic dies in it (`activation.md`).

If precondition 1 fails, the honest answer is that this is a product conversation, not a referral one.

## Word of Mouth vs Referral vs Affiliate

| Mechanism | Motivation | Best for | Fails as |
|---|---|---|---|
| Organic word of mouth | Social capital; the product makes the sharer look good | Anything with visible output | Something you can schedule — you can only make it easier |
| Product-embedded sharing | Using the product creates the invitation (shared doc, public link, split bill) | Collaborative and multiplayer products | An "invite friends" page nobody visits (`loops.md`) |
| Incentivised referral | Reward for both sides | Products with clear per-user value and a measurable conversion | A substitute for advocacy |
| Affiliate / creator | Commercial commission to a third party | Transactional purchases with clear attribution | A referral program with a bigger fraud surface (`acquisition.md`) |

Product-embedded sharing outperforms an incentivised program in almost every collaborative product, because the invitation is the work rather than an extra task. Exhaust it first.

## The Five Design Decisions

| Decision | Options | Default and why |
|---|---|---|
| Who gets rewarded | Referrer only · referee only · both | **Both.** Double-sided gives the referrer something to give rather than something to extract, which is what makes the ask socially safe |
| Reward type | Product currency (credit, storage, seats, months) · cash · charity · status | **Product currency.** Costs marginal, retains the user, and selects for people who want the product; cash selects for people who want cash |
| Trigger to reward | On signup · on activation · on payment | **On activation or payment.** Rewarding signups is a fraud subsidy with a public rate card |
| Where the ask lives | Post-value in-product moment · email · account page | **In-product at the value moment**, with email as a reminder to people who already engaged with the ask |
| Limits | Uncapped · capped per user · tiered | **Capped per user per period** at launch; raise it once fraud patterns are understood |

## Incentive Sizing

```
max_reward_value = target_CAC × margin_of_safety     (0.3-0.5 for a first program)
total_cost_per_referral = referrer_reward + referee_reward + fraud_allowance
```

Worked: target CAC 120 USD, safety 0.4 → ~48 USD total across both sides, e.g. 24 USD credit each. Compare against the paid CAC for the same customer quality; if the referral cost approaches paid CAC, the program is a worse channel with more moving parts.

- **Value the reward at its cost to you, not its face value.** A month of a 30 USD plan at 85% gross margin costs ~4.50 USD; that asymmetry is why product currency wins.
- **Referee-side reward doubles as a first-purchase incentive** and lifts the referred conversion rate — usually the larger effect of the two.
- **Beware discount-trained cohorts**: referred users acquired with a discount convert at the discounted price and often expect it at renewal. Track the referred cohort's retention and ARPA separately from organic, as its own row in `## Retention`.

## Placement and Timing

- Ask **immediately after realised value**, not after signup and not on a schedule: the project finished, the report generated, the order delivered, the problem solved.
- Make the share **one action** with a pre-filled message the user can edit. Every extra field halves participation.
- Offer the channel they actually use — a copyable link beats an email-address form; email-address forms feel like handing over an address book.
- The **landing experience is the program**: the referred user must land on the thing that was shared, with the reward and the sender's name visible, and be able to try before creating an account where the product allows it.
- Remind participants **once**, tied to a state change ("your friend signed up, one more step to your credit"), never on a drip (`lifecycle.md`).

## Attribution Mechanics

- Generate a unique `referrer_id` per user and pass it through link, cookie, and — critically — through signup, so the join survives the session (`instrumentation.md`).
- Support **manual code entry** as the fallback: links break, are copied without parameters, and are pasted into apps that strip them.
- Set an **attribution window** and write it down (30 days is a common default); after it expires, the signup is organic. Without a window, referrals accumulate forever and every cohort number becomes wrong.
- Handle the collision rule explicitly: if a user arrives via both a referral link and a paid click, decide which wins **before** launch and apply it consistently, or the two channels will each claim the customer and your total CAC will not reconcile.

## Fraud Controls

Every incentive is an attack surface, and the rate card is public.

| Control | Catches |
|---|---|
| Reward on activation or payment, never signup | Self-referral farms and bulk fake accounts |
| Per-user and per-period caps | Industrialised abuse from a single actor |
| Duplicate detection on payment instrument, device fingerprint, and IP cluster | Same person, many accounts |
| Disposable-email domain blocklist | The cheapest possible fake account |
| Holding period before payout (e.g. after refund window) | Refund-and-keep-the-reward |
| Manual review above a threshold of referrals per user | The top of the distribution, which is where nearly all abuse lives |
| Watching the referred cohort's activation rate | The single best signal — fraud has near-zero activation |

The last one is the alarm to build first: a referral cohort activating far below organic is fraud or a broken landing experience, and both are urgent.

## Measuring It

- **Participation rate** = users who shared ÷ eligible users. Below a few percent, the ask placement is wrong, not the incentive.
- **Referred conversion rate** = referred signups ÷ shares delivered.
- **Referral CAC** = (total rewards paid + fraud losses) ÷ referred customers who activated. The parentheses are the point: fraud losses divide too, and a program that skips them reports the reward cost as its CAC.
- **Cohort quality**: activation, retention and ARPA of referred users versus organic, tracked separately and permanently. Referred users often retain better — that is the argument for the program's budget, and it needs the data to make it.
- **Cannibalisation check**: how many rewarded referrals would have arrived anyway. A hold-out (program hidden from a slice of users) answers it; without it the program's reported CAC is a floor, not a fact (`experiments.md`).

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Program before product love | Buys signups from people with nothing to say | Precondition 1: the curve flattens first |
| Rewarding on signup | Publishes a fraud rate card | Reward on activation or payment |
| One-sided referrer reward | The ask reads as "help me get paid" | Double-sided |
| Cash rewards in a product business | Selects for reward-seekers, costs full value | Product currency |
| Buried on an account page | Nobody visits it | In-product at the value moment |
| No attribution window | Referrals accrue forever; every cohort number rots | Fixed window, written down |
| Uncapped at launch | Industrial abuse before you have patterns | Cap first, raise later |
| Judging on referred signups | Fraud and low-intent traffic look like success | Judge on activated referred users and their retention |

**After launching or changing a program**, write it back in the same turn: the channel row (referral CAC, participation rate, referred cohort activation, as-of date) into `## Channels` in `~/Clawic/data/growth/memory.md`, and the full design — the five decisions, the incentive math, the attribution window, the fraud controls, what was rejected — into `~/Clawic/data/growth/artifacts/referral-program.md`, born as its own file with its `## Boxes` line in the same turn (`memory-template.md`). Fraud patterns observed go to `## Pain Points` with dates; the hold-out result goes to `experiments/<year>.md`.
