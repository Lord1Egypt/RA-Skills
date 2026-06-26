# Experiment Design Guide

Practical statistics for pricing tests, written for a seller who is not a statistician but wants to avoid fooling themselves. The rules here are deliberately simple; when stakes are high, have an analyst run the exact numbers.

## 1. Choose the primary metric first — and prefer profit per visitor

Decide the single number that defines the winner *before* you launch. For pricing, the right default is almost always **profit per visitor**:

> profit per visitor = (price − COGS − payment fee − fulfillment fee) × conversion rate

Why not raw conversion rate? Because lowering price or deepening a discount almost always lifts CR — that's not a discovery, it's mechanics. Optimizing CR systematically pushes you toward the cheapest offer, which is rarely the most profitable. Profit per visitor captures both how often people buy **and** how much you keep per buyer, on the same denominator (a visitor), so variants with different prices are directly comparable.

Use **revenue per visitor** only when margins are identical across variants (e.g., a layout test at one fixed price). Use raw CR only as a guardrail or for a free signup with no price.

## 2. Minimum detectable effect (MDE)

The MDE is the smallest improvement you'd care enough about to act on. Set it from business value, not convenience. A smaller MDE detects subtler differences but needs far more traffic — required sample size scales roughly with 1/MDE², so halving the effect you want to detect roughly **quadruples** the visitors you need. Be honest: if a 0.1-point CR change isn't worth a price change, don't power the test to find it.

## 3. A sample-size rule of thumb

For a two-variant test on a conversion rate, with 80% power and 95% confidence (p < 0.05, two-sided), a workable approximation for visitors **per variant** is:

> n ≈ 16 × p × (1 − p) / (MDE_absolute)²

where `p` is the baseline conversion rate (as a decimal) and `MDE_absolute` is the absolute change you want to detect (as a decimal).

**Worked example.** Baseline CR p = 0.04 (4%). You want to detect a drop to 3.5%, so MDE_absolute = 0.005.

- p × (1 − p) = 0.04 × 0.96 = 0.0384
- 16 × 0.0384 = 0.6144
- MDE² = 0.005² = 0.000025
- n ≈ 0.6144 / 0.000025 ≈ **24,576 visitors per variant**

So ~24.6k per arm, ~49k total. At 2,500 visitors/day split 50/50, that's about **20 days** — round up to ~3–4 weeks to cover full business cycles. (The constant 16 is the common rule-of-thumb value; some teams use ~21 to be more conservative. Use a proper calculator for final planning.)

If the required N is unreachable in a sensible window: target a larger MDE, move the test to a higher-traffic surface, pool similar SKUs, or accept a higher (pre-registered) p-threshold for a low-risk, reversible change.

## 4. Test duration and business cycles

Sample size tells you *how many* visitors; duration must also cover *which* visitors. Buying behavior swings by day of week, payday, and promo calendar. **Run at least one, ideally two, full weekly cycles**, and avoid windows distorted by a sitewide sale, a holiday, or a stockout — unless that period is exactly what you're testing. Set the end date in advance. If you hit your sample size mid-week, finish the week so both arms see a balanced mix of days.

## 5. The dangers of peeking and p-hacking

A fixed-horizon test assumes you look **once**, at the end. If you watch results daily and stop the moment you see p < 0.05, your true false-positive rate balloons — repeatedly testing the same data turns random fluctuations into "wins," and the real error rate can exceed 25–30% instead of 5%.

Defenses:
- **Pre-register** the sample size / end date and stick to it.
- If you need to monitor, pre-register a **single interim look** or use a proper **sequential test** (e.g., alpha-spending / always-valid methods) that's designed to be peeked at.
- Don't **metric-shop** or **segment-shop** after the fact (HARKing). Slicing until something is significant guarantees false positives. Pre-declare the primary metric and key segments; treat anything found post-hoc as a hypothesis for a fresh test, not a result.

## 6. Significance vs practical significance

**Statistical significance** answers "is this difference probably real, or noise?" **Practical significance** answers "is it big enough to be worth shipping?" They're independent. With enough traffic, a trivial 0.05% lift can be statistically significant yet not worth the engineering effort or risk. With little traffic, a large, real effect can fail to reach significance. Decide your minimum *worth-shipping* effect in advance, and report both the p-value (or interval) and the absolute lift.

## 7. Confidence intervals beat bare p-values

A p-value says "different or not"; a **confidence interval** says "by how much, with what uncertainty." Report the estimated difference in the primary metric with a 95% CI (e.g., "+$0.04 profit/visitor, 95% CI [+$0.01, +$0.07]"). If the interval excludes zero, the effect is significant at that level; the **width** tells you how precise the estimate is. Wide intervals that include zero mean "we can't tell yet" — that's an honest, common, and acceptable outcome. Don't report it as a win.

## 8. Randomization-unit cleanliness

The unit you randomize on must be **stable and sticky**: a logged-in customer ID, or a persistent cookie that survives sessions and (ideally) devices. If you randomize per pageview or per session, a visitor can see different prices on different visits — which erodes trust, creates legal/optics risk, and corrupts your data (their behavior mixes arms).

Also verify:
- **Balanced arms.** Splits should be roughly even on traffic source, device, and new-vs-returning. A skew there can masquerade as a price effect.
- **No leakage.** Don't pipe an email blast or all returning customers into one arm.
- **Consistent price across the funnel.** The assigned price must match on PDP, cart, and checkout. A mismatch causes abandonment and noise.
- **Exclusions.** Filter internal/staff traffic and obvious bots before analysis.

Get the metric and the randomization right and most pricing tests become straightforward to read. Get them wrong and no amount of statistics will save the conclusion.
