# Mobile App Growth — Installs Are Not Users

An app funnel has a store in the middle of it and a permission wall at the start. Both are outside your product and both dominate the numbers. This file covers the install-to-value path, store conversion, the post-ATT attribution reality, and push as a retention instrument.

**Contents:** [The Real Funnel](#the-real-funnel) · [Store Conversion](#store-conversion) · [Permissions Are a Funnel Stage](#permissions-are-a-funnel-stage) · [Attribution After ATT](#attribution-after-att) · [Paid User Acquisition](#paid-user-acquisition) · [Retention on Mobile](#retention-on-mobile) · [Push Notifications](#push-notifications) · [Release Cadence and Ratings](#release-cadence-and-ratings) · [Traps](#traps)

**Before any UA or store work**, read `## Funnel` (install-to-activation rates by platform) and `## Channels` in `~/Clawic/data/growth/memory.md`. iOS and Android are two businesses with different CACs, retention, and monetisation; a blended app number is rarely actionable.

## The Real Funnel

```
impression → store page view → install → open → signup → permission → aha → D1 → D7 → D30
```

Two stages here exist nowhere else and are where most of the loss happens:

- **Store page view → install** is the store's conversion rate, and it is a page you barely control (`ecommerce.md` has the equivalent for a product page you do control).
- **Install → first open** loses a real share of users on both platforms, especially from ad clicks: the install completes, the user moves on, and the icon is never tapped. Measure it explicitly; UA reported "installs" that never opened are money spent on nothing.

Measure and report by platform and by source, always. Organic and paid installs behave differently enough that a blended D7 is a number with no owner.

## Store Conversion

The listing is a landing page with a fixed template and a review process.

| Element | Effect | Notes |
|---|---|---|
| Icon | High — the first and often only thing seen in search results | Test as a concept, not a colour |
| Title and subtitle | High — carries both ranking keywords and the promise | Keyword relevance and human legibility, in that order of constraint |
| First 2-3 screenshots | Highest controllable lever on the page | Most users never scroll; the first frames must state the value |
| Preview video | Mixed — helps some categories, hurts others by autoplaying badly | Test, do not assume |
| Ratings and review count | High and slow-moving; gates installs below a threshold | Prompt for review after a value moment, never on launch |
| Description | Low for humans, relevant for indexing | Front-load the first lines; the rest is rarely read |

Store keyword work (title, subtitle, keyword field, localisation) is a real channel with a real ceiling — the store's own search volume — and it compounds with ratings. Localising the listing (not just the app) into the languages of your top install markets is usually the cheapest volume available. Both stores run their own experimentation surface for listing assets; use it rather than inferring from install counts, which move with everything else.

## Permissions Are a Funnel Stage

- **Ask in context, after value.** The system prompt can be shown once; a denial is effectively permanent for most users, since re-granting requires a trip to settings.
- **Pre-prompt first**: an in-app screen explaining why, with the system prompt only for users who say yes. It converts the deniers into "not now" instead of "never".
- Order matters: push permission after the user has seen something worth being notified about; ATT after the user understands the product.
- Track grant rates per platform and per prompt placement as funnel stages, because they cap everything downstream — a 30% push grant rate caps every push-driven retention plan at 30%.

## Attribution After ATT

- Apple's App Tracking Transparency (2021) requires consent for cross-app tracking; most users decline, so **deterministic user-level attribution on iOS is gone**. SKAdNetwork returns delayed, aggregated, privacy-thresholded postbacks with a limited conversion-value payload.
- Consequences that are not optional: campaign structures must be coarser (SKAN has hard limits on how many campaigns can be measured per app), conversion values must be **encoded deliberately** — decide what the value bits mean and write it down, because you get few of them and changing the scheme resets your history — and results arrive on a delay measured in days.
- **Android** retains more signal but is moving the same direction; do not build a measurement plan that assumes today's identifiers exist next year.
- Practical stance: **incrementality and cohort analysis over per-user attribution** (`paid.md`). Geo hold-outs work on mobile and are underused. Media-mix reasoning at the channel level beats precise-looking numbers that are modelled anyway.

## Paid User Acquisition

- **Bid to predicted LTV by cohort, never to install cost.** Cost per install is the price of a lottery ticket; the payback is `LTV(D30 or later) − CAC` on the cohort.
- Early-signal modelling: predict D30/D180 revenue from D1-D7 behaviour, validate the model against matured cohorts quarterly, and state its error. A model never checked against maturity is a mechanism for spending money confidently.
- **Creative is the lever** on mobile UA as on any feed platform; test concepts, expect a small number of winners (`paid.md`).
- **Beware incentivised installs**: they deliver installs that never open and destroy your retention baselines. If a source's D1 is far below every other source's, suspect the source, not the app.
- Watch the **install → open → aha** chain per source; a source with cheap installs and a broken open rate is more expensive than the dashboard says.

## Retention on Mobile

- D1/D7/D30 are the standard reporting periods, but they are a convention: measure against the app's natural frequency like any other product (`retention.md`). A weekly-use app judged on D1 looks broken and is not.
- **Benchmarks vary by category by multiples**; your own first cohorts are the only baseline worth optimising against. Compare cohort to cohort, not to a published average.
- **Uninstall is a distinct event** from dormancy and is partially observable through store and push feedback. An uninstall spike concentrated after a release names the release.
- Onboarding on mobile pays more than anywhere else because the exit cost is one home-button press: cut steps to first value ruthlessly (`activation.md`).
- **App size and cold-start time** are conversion factors: large downloads lose installs on mobile data, and a slow first launch loses the users you just paid for.

## Push Notifications

The strongest retention instrument on mobile and the fastest way to be uninstalled.

- **Trigger on state change relevant to that user** — someone responded, the thing is ready, the threshold was crossed — never on a marketing calendar (`lifecycle.md`).
- **Frequency cap globally**, and treat opt-out rate and uninstall-after-push as the fatigue metrics.
- **Deep-link to the exact object**, never to the home screen. A notification that dumps the user on a feed wastes the only attention it will get.
- **Respect quiet hours in the user's timezone.** A 3am push costs a permission you cannot get back.
- Measure push on **downstream retention of the messaged cohort versus a hold-out**, not on open rate.

## Release Cadence and Ratings

- Review submission adds days of latency and can reject a build for reasons unrelated to your growth plan; anything with a date needs a buffer and, where possible, a server-side feature flag so the release and the launch are separate events.
- **Staged rollout** on Android and phased release on iOS limit blast radius; watch crash rate and D1 of the new-version cohort before completing the rollout.
- Rating prompts: after a value moment, capped by the platform's own limits, never after an error. In-app feedback for unhappy users before the store prompt is legitimate and standard; suppressing negative reviews by other means is not, and both stores police it.
- A crash-rate regression outranks every growth initiative in flight — it hits retention, ranking, and ratings simultaneously.

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Optimising cost per install | Buys installs that never open | Bid to cohort LTV; measure install → open → aha |
| Blended iOS + Android metrics | Two different businesses averaged into one meaningless number | Report per platform, always |
| Push permission requested at launch | Denied once, denied forever | Pre-prompt in context after value |
| Per-user ROAS on iOS | The data does not exist post-ATT | SKAN cohorts plus incrementality (`paid.md`) |
| Comparing D1 to a published benchmark | Category variance is multiples | Compare to your own cohorts over time |
| Marketing pushes to raise DAU | DAU up for a day, opt-outs and uninstalls up permanently | State-change triggers only |
| Ignoring app size and cold start | Loses paid installs before the app runs | Treat both as funnel stages |
| Store listing changed and shipped untracked | Install rate moves and nobody knows why | Use the store's own experiment surface; write the change and its date to `experiments/<year>.md` |

**After any UA change, store test, or retention read**, write it back in the same turn: install → open → activation rates per platform and per source into `## Funnel`, the UA channel row with cohort payback, currency and as-of date into `## Channels`, and D1/D7/D30 by cohort into `## Retention` — all in `~/Clawic/data/growth/memory.md` (`memory-template.md`). The SKAN conversion-value scheme is an artifact from the first version: `~/Clawic/data/growth/artifacts/skan-conversion-values.md` with its `## Boxes` line, because changing it resets history and the next person must know what the bits mean. Store-listing test results go to `experiments/<year>.md`.
