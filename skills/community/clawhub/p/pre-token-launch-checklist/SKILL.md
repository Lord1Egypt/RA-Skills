---
name: pre-token-launch-checklist
description: Screen a pre-token DeFi protocol before farming or entering it. Runs the pre-entry checklist from the Token Launch Radar method — is it genuinely pre-token, does its category have live-token peers to price against, and are its size, momentum, age and reach real — and returns a pass / caution / fail verdict per check. Use when asked "is this pre-token protocol legit?", "should I farm this?", "check this protocol before I put time or money in", or before adding any no-token protocol to a watchlist.
license: MIT-0
metadata:
  version: 1.0.0
---

# Pre-Token Launch Checklist — free sample of Token Launch Radar

Before the Token Launch Radar ranks anything, it screens. A protocol that fails the
screen is never ranked, however big it looks. This skill is that screen, written out as
a checklist an agent can run by hand on one protocol at a time, using public data
(a DefiLlama protocol page and the protocol's own docs are enough).

Run the checks in order. Check 1 is a gate: a fail there ends the review.

## Check 1 — Is it genuinely pre-token? (the exclusion rule)

The single most common fake "upcoming launch" is a product whose token already trades
in another form. Set aside, without scoring:

- **Wrapped, staked or bridged products of a token that already trades.** A wrapper or
  bridge of a live token is not a launch; its "protocol" inherits a price that already
  exists.
- **Products whose category gives them away** — liquid-staking, wrapped-asset and
  bridge categories are the usual shapes of this.
- **Anything where a token contract for the protocol (or its parent) already trades
  on any chain**, under any ticker.

Verdict: if a tradable form of the token exists → **fail, stop here.** It may still be
a fine product, but it is not a pre-token opportunity and must not be ranked as one.

## Check 2 — Does its category have live peers?

The radar prices a pre-token protocol from the live-token protocols *in its own
category* — a lending protocol is judged against lending multiples, a bridge against
bridge multiples. So ask: are there established, live-token protocols in the same
category to compare against?

- Several live peers with real market caps → the category has a yardstick: **pass**.
- Peers exist but are tiny or illiquid → the yardstick is shaky: **caution**.
- No live-token protocol in the category at all → there is no market evidence for what
  this category is worth: **caution at best**, and treat any valuation claim about the
  protocol as unanchored.

## Check 3 — Size: is the TVL real and sustained?

- TVL that has existed for months at a similar level reads as real usage: **pass**.
- TVL that arrived in one spike — especially alongside a points or farming campaign
  announcement — is mercenary until it survives the campaign: **caution**.
- TVL you cannot corroborate outside the protocol's own site: **fail** for screening
  purposes; unverifiable size is not size.

## Check 4 — Momentum: read 7-day growth both ways

Growth is a signal, not a trophy.

- Steady positive 7-day growth on top of sustained TVL: **pass**.
- Flat or mildly negative growth in a protocol that passes the other checks:
  **caution**, not a rejection — quiet protocols launch too.
- Extreme one-week growth (a doubling or more) is a flag to investigate, not a
  strength: ask what incentive started this week and what happens when it ends.
  Unexplained → **caution**; explained by a just-announced mercenary incentive →
  weigh it under Check 3's rule, not here.

## Check 5 — Launch pressure: how long with no token?

- Running a year or more with real TVL and no token: launch pressure is real —
  the protocol has something to launch and a history to judge: **pass**.
- A few months old: normal; judge on the other checks: **caution** only if it is
  also failing elsewhere.
- Days or weeks old with big claims: nothing has been proven yet, and "no token
  *yet*" is doing all the work in the pitch: **caution**; a fail if Check 3 also
  fails.

## Check 6 — Reach: how many chains?

- Live on several chains with TVL actually spread across them: **pass** — breadth is
  evidence of real integration work.
- Deployed on many chains but with TVL on only one: count the one: **caution**.
- Single chain is not a fail — plenty of genuine protocols start there. It simply
  adds nothing.

## Combining the verdicts

- **Any fail on Check 1** → not a pre-token opportunity. Stop.
- **A fail anywhere else** → do not enter on the strength of the remaining passes;
  write down what would have to change.
- **Mostly passes, some cautions** → a legitimate watchlist entry. Record the
  cautions next to it; they are the things to re-check.
- **All passes** → it survives the screen. That is all it means: the protocol is a
  genuine, peer-comparable, pre-token protocol. It says nothing about whether it
  will launch, airdrop, or reward anyone.

## Limits — say these out loud when presenting a verdict

- This screen does not audit contracts, teams or tokenomics, and it is not a
  rug detector. It removes fake launches and unpriceable claims; it cannot certify
  safety.
- A protocol can pass every check and still never launch a token or reward farmers.
- Any value comparison is peer-relative — what similar live protocols are worth —
  never a prediction or a price target.

## The full version

This checklist is one screen, run by hand, on one protocol. The full **Token Launch
Radar** runs the complete method over an entire DefiLlama snapshot at once: it
applies this exclusion rule to every protocol, prices each pre-token protocol from
the live median of its own category *as read from that snapshot*, scores size,
momentum, launch pressure and reach with one deterministic function — no protocol
special-cased — and writes the ranked board, a web dashboard, and a farm plan for
every row. Same snapshot in, same board out, byte for byte.

- Paid skill catalogue (Token Launch Radar and more):
  https://github.com/Townsvilledh/agent-skills
- The author's cross-chain swap-pair dataset, sold over x402:
  https://fluid-quote.kanugideontownsville.workers.dev
