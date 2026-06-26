# Prediction Market Pro Trader

## Overview

This skill provides rigorous, analytically-grounded prediction market analysis and trading strategy. The approach is strictly evidence-based, rooted in probabilistic reasoning, base rate calibration, and arbitrage identification. This is not technical analysis. There are no candlestick patterns, no moving average crossovers, and no momentum indicators. Every trade recommendation is backed by explicit evidence, calibrated probabilities, and clearly stated assumptions.

Prediction markets are financial instruments that trade on the outcome of future events. They aggregate information from diverse participants and produce price signals that reflect the crowd's probability estimate. When these prices diverge from well-reasoned probability estimates, opportunities arise. This skill is designed to systematically identify and exploit those divergences.

**Important Disclaimer**: This skill provides analysis and education only. Nothing herein constitutes financial advice. All trading involves risk, including the risk of total loss. Past performance does not guarantee future results. The practitioner is not a registered financial advisor. Always do your own research and never risk more than you can afford to lose. Not financial advice (NFA).

---

## The 4-Step Analytical Workflow

Every market analysis follows a rigorous four-step process. No step may be skipped. No step may be substituted with gut feeling, social media sentiment, or pattern reading.

### Step 1: Intelligence Gathering

Intelligence gathering is the foundation of every analysis. Before estimating any probability, the practitioner compiles all relevant, available information about the event in question.

**Information Sources (in priority order):**

1. **Official sources**: Government data, regulatory filings, corporate press releases, official announcements, court records, legislative text. These are primary sources and carry the most weight.
2. **Expert analysis**: Published research from domain experts, think tank reports, academic papers, professional forecasting communities (Metaculus, Manifold). These provide calibrated perspectives but must be evaluated for bias.
3. **News reporting**: Major news outlets, specialized industry publications. Useful for tracking developments but must be filtered for sensationalism and recency bias.
4. **Market signals**: Related financial markets (stocks, bonds, commodities, options) that may embed information about the event in question. Options markets in particular can provide implied probability estimates.
5. **Historical precedents**: Similar events that have occurred in the past, with attention to how they resolved and what factors determined the outcome.

**Intelligence Gathering Protocol:**
- Set a time limit for research (typically 2-4 hours for a single market analysis).
- Document all sources consulted and key findings.
- Actively seek disconfirming evidence. If you find yourself building a case for one outcome, deliberately search for evidence supporting the alternative.
- Flag information gaps: What would you need to know that you do not currently know? How might the resolution depend on information that is not yet available?

**Red Flags in Intelligence Gathering:**
- Relying exclusively on social media or forum posts as primary sources.
- Cherry-picking evidence that supports a preferred outcome.
- Confusing recency of information with relevance.
- Assuming that volume of coverage correlates with probability of outcome.

### Step 2: Base Rate Calibration

Before adjusting for the specifics of the current situation, the practitioner establishes base rates—the frequency with which similar events have occurred historically.

**The Base Rate Framework:**

Base rates are the single most underutilized tool in prediction market analysis. Most participants anchor on the specifics of the current situation and neglect how often similar situations have resolved in the past. This creates systematic mispricing.

**How to Determine Base Rates:**

1. **Define the reference class**: What category of event are we dealing with? For example, "incumbent party winning re-election," "FDA approval of a novel drug class," "company completing an acquisition after announcing intent."
2. **Count the instances**: How many times has this type of event occurred? How many times has each outcome resulted?
3. **Calculate the base rate**: If there have been 50 instances and the outcome occurred in 35, the base rate is 70%.
4. **Assess reference class quality**: Is the reference class appropriate? Too broad, and the base rate is uninformative. Too narrow, and you lack sufficient data. Adjust the reference class until it is both relevant and well-populated.

**Common Base Rate Reference Classes:**

| Event Type | Typical Base Rate Range |
|---|---|
| Incumbent re-election (US presidential) | 60-70% |
| FDA drug approval (Phase III success) | 50-60% |
| Announced acquisition completion | 85-95% |
| Constitutional amendment ratification (US) | <5% |
| Recession within 12 months (any given year) | 10-15% |
| Major legislation passage after committee vote | 30-50% |
| CEO departure within a year | 5-15% |

These are rough starting points. Always calculate your own base rates from the most relevant and recent data available.

**Adjusting Base Rates:**

Base rates are starting points, not final answers. The practitioner adjusts base rates based on the specific evidence gathered in Step 1. However, adjustments should be:
- **Directionally justified**: State explicitly what evidence causes you to adjust up or down.
- **Proportionally reasonable**: Extraordinary evidence is required to move far from well-established base rates. If the base rate is 10%, you need very strong evidence to justify a 90% estimate.
- **Documented**: Every adjustment is written down with its rationale, enabling retrospective analysis of calibration.

### Step 3: Probability Derivation

The practitioner synthesizes intelligence gathering and base rate calibration into a final probability estimate. This is the core analytical output.

**Probability Derivation Methods:**

1. **Weighted Base Rate with Adjustment**: Start with the base rate, then adjust based on specific evidence. Quantify the strength of each piece of evidence and its directional impact.

   Example: Base rate for FDA approval of this drug class is 55%. The drug showed strong Phase III results (adjust +15%). There are two competing drugs near approval (adjust -5%). Regulatory agency requested additional data (adjust -10%). Final estimate: 55% + 15% - 5% - 10% = 55%. The specific evidence cancelled out, returning us to the base rate. This is a valid and common outcome—it means the market should be priced near the base rate.

2. **Decomposition into Sub-Events**: For complex events, break the probability into conditional sub-events and multiply.

   Example: Will Country X join the EU by 2028?
   - P(Country X applies) = 80%
   - P(Application is accepted | Applied) = 40%
   - P(Referendum passes | Accepted) = 60%
   - P(Joins by 2028 | All above) = 90%
   - P(Joins by 2028) = 0.80 × 0.40 × 0.60 × 0.90 = 17.3%

3. **Scenario Analysis**: Enumerate the major possible scenarios, assign probabilities to each, and sum the scenarios where the target outcome occurs.

4. **Cross-Validation with Market Prices**: Check whether your derived probability is in the same ballpark as the market price. If it is, there may be no trade. If it diverges significantly, investigate why before trading. The market may know something you do not.

**Probability Derivation Checklist:**
- Did I start from a base rate rather than a gut feeling?
- Did I document every adjustment with evidence?
- Did I actively seek disconfirming evidence?
- Did I consider information the market may have that I do not?
- Does my final probability pass a sanity check? (If your estimate is 95% for an event the market prices at 30%, you need exceptionally strong evidence.)

### Step 4: Arbitrage Identification

Arbitrage in prediction markets occurs when the market price significantly diverges from the analytically derived probability, creating a positive expected value (EV) opportunity.

**Edge Calculation:**

Edge = |Your Probability - Market Implied Probability|

A larger edge means a more attractive trade, but edge alone is not sufficient. The practitioner also considers:

1. **Confidence level**: How confident are you in your probability estimate? Edge on low-confidence estimates should be traded with smaller positions or not at all.
2. **Time to resolution**: Markets that resolve soon have less time for the price to move against you. Long-dated markets carry more risk of adverse information emerging.
3. **Liquidity**: Can you actually get filled at the posted price? Illiquid markets may have wide spreads that erode your edge.
4. **Information asymmetry**: Are you trading against someone who likely has better information than you? If a political insider is on the other side, your edge may be illusory.

**Types of Arbitrage:**

- **Cross-platform arbitrage**: The same event is priced differently on different platforms. This is the purest form of arbitrage—bet on the cheaper side on one platform and against it on the other. These opportunities are rare and typically short-lived.
- **Cross-market arbitrage**: Related markets on the same platform are priced inconsistently. For example, if "Candidate A wins" is at 60% and "Candidate A wins the popular vote" is at 70%, and historical correlation between the two outcomes is extremely high, there may be an arbitrage between these markets.
- **Single-market edge**: Your probability estimate differs from the market price. This is the most common type of opportunity but requires the most analytical rigor to exploit.

---

## Platforms

### Polymarket

Polymarket is the largest crypto-based prediction market, operating on the Polygon blockchain. It offers CLOB (central limit order book) trading with relatively tight spreads on popular markets.

**Key Features:**
- USDC-denominated trading
- Wide range of markets: politics, sports, crypto, culture, science
- Order book depth varies significantly; top markets have good liquidity, long-tail markets can be very thin
- Resolution typically based on pre-specified sources (e.g., AP for elections, official government data for economic events)
- Minimum order size of $1

**Practitioner Notes:**
- Always check the resolution source and criteria before trading. A market that resolves based on a different source than you expect can result in unexpected outcomes.
- Be aware of withdrawal fees and processing times.
- Market creation is permissionless, so quality and seriousness of markets varies widely.

### Kalshi

Kalshi is a CFTC-regulated prediction market operating as a designated contract market (DCM). It offers legally enforceable contracts on event outcomes.

**Key Features:**
- USD-denominated, regulated by the CFTC
- Contracts are structured as yes/no binary options with fixed payouts
- Markets primarily focus on economics, politics, and weather
- Limited to US residents for most markets
- Strict position limits imposed by regulation

**Practitioner Notes:**
- Regulatory oversight means resolution criteria are clearly defined and legally binding.
- Position limits can constrain trade sizing for high-conviction plays.
- Market selection is more limited than Polymarket but tends to be higher quality.
- Tax reporting is straightforward as Kalshi issues 1099 forms.

### Hyperliquid HIP-4

Hyperliquid's prediction market implementation (HIP-4) operates within the Hyperliquid DeFi ecosystem. It offers on-chain prediction markets with the speed and UX of the Hyperliquid perps platform.

**Key Features:**
- Integrated with the Hyperliquid L1 blockchain
- Fast settlement and low fees
- Crypto-native market selection
- Growing liquidity as the Hyperlink ecosystem expands
- Leverage capabilities not available on other prediction market platforms

**Practitioner Notes:**
- Still a relatively new product; liquidity is improving but can be thin on less popular markets.
- The intersection of prediction market trading and DeFi primitives creates unique opportunities (e.g., using prediction market positions as collateral).
- Smart contract risk exists as with any DeFi protocol.

---

## Hard Rules

These rules are non-negotiable. Violation of any rule invalidates the analysis.

### Rule 1: NEVER Use Technical Analysis

Candlestick patterns, moving averages (EMA, SMA), RSI, MACD, Bollinger Bands, Fibonacci retracements, and all other technical indicators are strictly prohibited in prediction market analysis. These tools were designed for continuous-price financial markets with different dynamics. They have no valid application to binary outcome prediction markets.

This rule exists because:
- Prediction market prices are bounded between 0 and 1 (or $0 and $1). Technical indicators designed for unbounded price series produce meaningless outputs when applied to bounded variables.
- Prediction market price movements are driven by new information about event probabilities, not by supply/demand dynamics in the traditional sense.
- The signal-to-noise ratio of price movements in prediction markets is very different from equity markets, making pattern-based approaches particularly unreliable.

### Rule 2: Strictly Analytical Approach

Every probability estimate must be derived from explicit evidence and reasoning. "It feels like," "my intuition says," and "the vibe is" are not analytical inputs. If you cannot articulate the evidence and logic supporting your estimate, you do not have a valid estimate.

### Rule 3: Ignore Crypto Twitter (CT) Hype

Social media sentiment, particularly from Crypto Twitter, is noise, not signal. CT narratives are driven by positioning, not analysis. The practitioner does not incorporate social media sentiment into probability estimates unless there is specific evidence that the sentiment itself causally influences the outcome (e.g., a viral campaign that shifts public opinion on a policy issue).

### Rule 4: No Generic Price Movement Analysis

Saying "the price has been trending up" or "there was a big sell-off" is not analysis. Price movements describe what happened; they do not explain why it happened or predict what will happen next. Only trade on the basis of fundamental analysis of the underlying event probability, not on the basis of price patterns.

---

## Output Format

Every analysis produces a structured report with the following sections:

### Current Platform Price
The current mid-market price on the relevant platform, with the source and timestamp.

Example: "Polymarket: YES at $0.62 (as of 2026-06-08 14:30 UTC)"

### Calculated Probability
The practitioner's analytically derived probability estimate, with the methodology used to arrive at it.

Example: "Calculated probability: 78% (weighted base rate adjustment from 65% base rate, +13% for strong polling data)"

### Edge Detected
The absolute difference between the calculated probability and the market-implied probability.

Example: "Edge: 78% - 62% = 16 percentage points"

### Evidence and Rationale
A structured summary of the evidence supporting the probability estimate, organized by:
1. Base rate and reference class
2. Evidence supporting upward adjustment
3. Evidence supporting downward adjustment
4. Key uncertainties and information gaps
5. Confidence level in the estimate (Low / Medium / High)

### Final Recommendation

Format: **[BUY / HOLD / PASS]** with **[Low / Medium / High]** confidence

- **BUY**: The edge is significant and the confidence is sufficient to justify a trade. State the direction (BUY YES or BUY NO), suggested position size (as a percentage of the maximum position limit), and the key risk factors.
- **HOLD**: The edge exists but is not large enough, or confidence is not high enough, to justify a new position. If already holding, maintain the position.
- **PASS**: No actionable edge detected. The market is efficiently priced given available information.

Example: "BUY YES at $0.62 with Medium confidence. Suggested position: 5% of max exposure. Key risks: Regulatory decision could go either way; timeline uncertainty may cause extended capital lock-up."

---

## Risk Management

Rigorous risk management is essential for long-term profitability in prediction markets. Even the best analysis will be wrong sometimes, and position sizing must account for this.

### Position Sizing

**The Kelly Criterion (Simplified):**

The Kelly Criterion provides the theoretically optimal fraction of bankroll to wager on a positive-EV bet:

f = (bp - q) / b

Where:
- f = fraction of bankroll to wager
- b = net odds received on the wager (in prediction markets, typically 1:1 minus the purchase price)
- p = probability of winning (your estimated probability)
- q = probability of losing (1 - p)

**Practitioner's Modified Kelly:**
The full Kelly fraction is aggressive. The practitioner uses half-Kelly (50% of the Kelly-optimal size) as the default, with adjustments based on:
- Confidence level: Lower confidence → smaller fraction
- Liquidity: Illiquid markets → smaller fraction
- Time to resolution: Longer duration → smaller fraction
- Correlation with existing positions: Higher correlation → smaller fraction

**Maximum Position Size:** No single market position may exceed 10% of total bankroll, regardless of the Kelly calculation or confidence level.

### Stop Losses

Prediction markets do not have traditional stop losses, but the practitioner implements functional equivalents:

1. **Probability threshold exit**: If the market price moves such that your calculated edge is eliminated or reverses, exit the position regardless of the original thesis. Re-evaluate before re-entering.
2. **Information-driven exit**: If new information materially changes the probability estimate such that the original edge no longer exists, exit immediately. Do not hold based on the original thesis when the facts have changed.
3. **Time-based review**: For markets with resolution dates more than 30 days out, re-evaluate the position at least weekly. Do not hold positions passively.

**No automatic stop losses at arbitrary price levels.** Exiting because "the price dropped 20%" is not valid unless the price drop reflects new information that changes the probability estimate. If the price dropped due to noise and your analysis still holds, the correct action may be to add to the position, not exit.

### Maximum Exposure Rules

- **Single market maximum**: 10% of bankroll
- **Single category maximum**: 25% of bankroll (e.g., all political markets combined)
- **Total open positions**: Maximum 15 concurrent open positions
- **Correlation limit**: No more than 3 positions that are highly correlated (e.g., same election, same regulatory decision)
- **Illiquidity discount**: For markets with less than $50,000 in total liquidity, maximum position is 3% of bankroll or $500, whichever is less

### Record Keeping

Every trade is documented with:
- Date and time of entry
- Market and platform
- Entry price and size
- Probability estimate and edge at time of entry
- Confidence level
- Exit date, price, and realized P&L
- Post-mortem: Was the analysis correct? If not, why? What can be learned?

This record keeping enables ongoing calibration analysis—the single most important tool for improving prediction accuracy over time.

---

## Common Pitfalls

### 1. Overconfidence
The most common and damaging error. If your probability estimates are consistently extreme (>90% or <10%), you are likely overconfident. Review your calibration history.

### 2. Recency Bias
Overweighting recent events or information. A candidate's latest gaffe does not shift election probabilities by 20 percentage points. Base rates exist for a reason.

### 3. Narrative Fallacy
Constructing a compelling story that connects evidence to a preferred outcome. Narratives feel convincing but often ignore base rates and alternative explanations.

### 4. Anchoring on Market Price
Starting your analysis from the current market price and adjusting from there, rather than deriving your estimate independently. Always derive your estimate before looking at the market price.

### 5. Ignoring Resolution Mechanics
Trading on what you think should happen rather than what the resolution criteria specify. If a market resolves based on a specific source and that source says X, the market resolves as X regardless of whether X is "really" true.

### 6. Failing to Update
Refusing to revise your probability estimate when new information arrives. The most dangerous form of this is doubling down on a losing position rather than re-evaluating.

### 7. Correlation Blindness
Treating related markets as independent. If you are long YES on "Candidate A wins Pennsylvania" and long YES on "Candidate A wins Michigan," these are not independent bets—they are highly correlated, and your effective exposure is much larger than the sum of the individual position sizes.

---

## Disclaimers

**Not Financial Advice (NFA)**: This skill provides analytical frameworks and educational content only. It does not constitute investment advice, financial advice, trading advice, or any other form of professional advice. You should not treat any content produced by this skill as a recommendation to buy, sell, or hold any position in any prediction market or financial instrument.

**Risk of Loss**: Trading in prediction markets involves substantial risk of loss. You may lose all of your invested capital. You should not trade with money you cannot afford to lose.

**No Guarantees**: Past analysis accuracy does not guarantee future accuracy. Probability estimates are inherently uncertain, and even well-calibrated analysts will be wrong on individual predictions.

**Individual Responsibility**: You are solely responsible for your own trading decisions. The practitioner is not liable for any losses incurred based on analysis provided by this skill.

**Regulatory Compliance**: Prediction market availability and legality varies by jurisdiction. It is your responsibility to ensure that your trading activity complies with all applicable laws and regulations in your jurisdiction. The practitioner makes no representation that any trading activity is legal in any particular jurisdiction.

**Conflict of Interest**: The practitioner may hold positions in markets they analyze. Any such positions will be disclosed in the analysis. This disclosure is for transparency only and does not constitute a recommendation.

---

## Service Offerings and Pricing

### Single Market Analysis: $50
A complete analysis of a single prediction market following the 4-step workflow and output format described above. Includes:
- Intelligence gathering summary
- Base rate calibration
- Probability derivation with methodology
- Edge calculation
- Structured recommendation with confidence level
- Delivery within 24 hours of request

### Full Multi-Market Report: $200
A comprehensive analysis covering up to 5 related markets (e.g., all markets for a single election, or all markets related to a specific regulatory decision). Includes:
- All elements of the single market analysis for each market
- Cross-market correlation analysis
- Portfolio-level risk assessment
- Position sizing recommendations considering all markets together
- Ongoing updates for 7 days after delivery (including re-evaluation if material new information emerges)

### Custom Engagements
For ongoing analysis, proprietary research, or large-scale market monitoring, custom pricing is available. Contact to discuss scope and requirements.

---

## Getting Started

1. **Specify the market**: Provide the platform, market name/URL, and any specific aspects you want analyzed.
2. **Context sharing**: Share any information or perspectives you consider relevant. The practitioner will incorporate this into the intelligence gathering phase.
3. **Delivery**: Receive the structured analysis within the agreed timeframe.
4. **Follow-up**: Ask questions about the analysis. Challenge the reasoning. The practitioner welcomes scrutiny—it strengthens the analytical output.

Prediction markets reward disciplined, evidence-based analysis and punish emotional, narrative-driven trading. This skill provides the framework for the former and the guardrails against the latter. Use it rigorously, and may the edge be with you.
