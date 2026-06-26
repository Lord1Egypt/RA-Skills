---
name: investment-risk-scanner
description: >
  Investment risk scanner using Buffett + Porter's Five Forces framework. Triggers when users ask
  "analyze XXX's risk", "is this project legit", "can I buy this stock", "Buffett framework check",
  "is this business model sustainable", "Ponzi", "subsidy dependent", "loss making", "valuation".
  
  5-layer Buffett framework + Porter's Five Forces as complementary check.
  Built-in cases: Qutoutiao, StepN, WeWork, Quibi, Tesla, NVDA, PLTR, COIN, AMC, RIVN, BYD, Geely.
  Key addition: Supply Chain Finance risks (迪链-type tools), Hidden liabilities, OCF quality analysis.
---

# 🎯 Investment Risk Scanner — Buffett + Porter Framework

## Core Question

**"What happens if the subsidies stop?"** + **"Where does the OCF actually come from?"**

- Users still stay without incentive? → Probably OK ✅
- OCF comes from real business, not supplier/customer financing? → Clean ✅
- Users leave immediately? → Ponzi-lite 🚨

---

## ⚠️ CRITICAL: OCF Source Quality Analysis

**New mandatory check — Never look at OCF in isolation!**

### OCF Quality Matrix

| OCF Source | Quality | Example |
|------------|---------|---------|
| Real product/service sales | ✅ Clean | Apple iPhone sales |
| From supplier financing (欠供应商钱) | ⚠️ Dirty | 迪链模式 ⚠️ |
| From customer advance payments | ⚠️ Dirty | 预售模式 |
| From regulatory subsidies | ⚠️ Conditional | EV补贴 |
| From working capital manipulation | 🚨 Dangerous | 延付供应商+提前收客户 |

**The 迪链 Lesson (BYD case)**:
```
BYD OCF = ¥593亿 → Looks great!
BUT: ¥4000亿+ 迪链规模 = OCF partially from supplier financing
Real business OCF ≈ ¥593亿 - 供应商资金占用 ≈ ？
```

---

## Part 1: Five-Layer Buffett Framework

### Layer 1: Business Model

| Check | Pass ✅ | Danger 🚨 |
|-------|---------|-----------|
| Subsidy test | Users stay without incentive | 🚨 No (Qutoutiao/StepN) |
| Moat describable? | Clear description | 🚨 Vague |
| Competitor replication time | >3 years | 🚨 Cloneable anytime |
| DCF/Owner Earnings | Positive or estimable | ⚠️ Unclear |

### Layer 2: Unit Economics

| Check | Formula | Danger Signal |
|-------|---------|--------------|
| User value | Ad revenue > incentive cost? | Qutoutiao style 🚨 |
| Token value | Real cash flow support? | StepN style 🚨 |
| Lending model | Rate > cost + defaults? | P2P style 🚨 |
| Gross margin | >15% (industrial) | Below = weak ⚠️ |
| Revenue vs FCF quality | Is growth funded by real economics? | ⚠️ |

### Layer 3: Management

| Check | Pass ✅ | Danger 🚨 |
|-------|---------|-----------|
| Skin in Game | Major personal stake | 🚨 Barely holds shares |
| Track record | Delivers on promises | 🚨 Misses commitments |
| Narrative | Talks about moat | 🚨 Only talks about growth |
| Incentives | Aligned with shareholders | 🚨 Misaligned |
| Supplier relations | Treats suppliers fairly | 🚨 Exploits suppliers |

**Quantitative**: Founder/stakeholder ownership >20% = strong signal ✅

### Layer 4: Valuation & Margin of Safety

| Check | Pass ✅ | Danger 🚨 |
|-------|---------|-----------|
| DCF estimable? | Reasonable assumptions | 🚨 Pure speculation |
| Margin of safety? | >30% | 🚨 Zero margin |
| Sustainable growth? | <3% | �️ 5%+ unrealistic |
| Growth quality? | Organic | 🚨 Fundraising-dependent |

**Quantitative Thresholds**:

| Metric | Safe ✅ | Warning ⚠️ | Danger 🚨 |
|--------|---------|------------|--------|
| Forward P/E | <20x | 20-40x | >40x |
| PEG Ratio | <1.0 | 1.0-2.0 | >2.0 |
| P/S | <2x | 2-5x | >5x |
| P/B | <3x | 3-8x | >8x |
| FCF | Positive | Breakeven | Persistent negative |
| ROE | >15% | 8-15% | <8% |
| Net Margin | >10% | 3-10% | <3% |
| Debt/Equity | <30% | 30-60% | >60% |

### Layer 5: Structural Risk

| Check | Red Flag 🚩 |
|-------|-------------|
| Liquidity | Runway <12 months |
| Regulation | Depends on regulatory arbitrage |
| Technology | Single-tech dependency |
| Competition | Rapidly disrupting industry |
| Geopolitics | Major market concentration |
| **Supply Chain Finance** | **Relies on supplier financing (迪链-type)** 🚨 |

---

## Part 2: Porter's Five Forces (Complementary Framework)

### Why add Porter's Five Forces?

**Buffett's blind spot**: He focuses on "Is this a good business?" but misses "How does industry structure determine profitability?"

**The 迪链 lesson**: BYD looked great by Buffett metrics (OCF ¥593B, PE 19.7x) but Porter's Five Forces would immediately ask:
> "Why can BYD extract ¥4000B+ from suppliers?" → Supplier power is weak → Unstable moat

### The Five Forces

```
                    New Entrants
                        ↓
            ┌───────────────────────────┐
            │    Industry Competition   │
            │   (Price War = High)     │
            └───────────────────────────┘
            ↑                           ↑
  Suppliers ←                           → Buyers
(Weak = Good)                       (Competitive = Bad)
```

### Force 1: Bargaining Power of Suppliers

| Supplier Power | Implication | Example |
|----------------|-------------|---------|
| Weak (fragmented) | Company can extract value | BYD vs small suppliers ✅ |
| Strong (concentrated) | Suppliers capture value | Rare earth miners 🚨 |
| **Danger Pattern** | Company survives by squeezing suppliers | 迪链模式 ⚠️ |

**Critical Check**: *If a company's "moat" is based on supplier exploitation, how sustainable is it?*

### Force 2: Bargaining Power of Buyers

| Buyer Power | Implication | Example |
|-------------|-------------|---------|
| Weak (fragmented) | Company sets prices | Apple App Store ✅ |
| Strong (concentrated) | Buyers extract value | Car dealers vs OEMs ⚠️ |
| **In EV market** | Price war = buyer power HIGH | Bad for all EV makers ⚠️ |

### Force 3: Competitive Rivalry

| Competition Level | Signal | Example |
|-----------------|--------|---------|
| Low | Moat is real | Apple's ecosystem ✅ |
| High (price war) | Commodity trap | China EV market 🚨 |
| **Price War = Maturity Stage** | Buffett: "bad industry" | EV 2024-2026 ⚠️ |

### Force 4: Threat of New Entrants

| Barrier to Entry | Pass | Fail |
|-----------------|------|------|
| Capital requirements | High barrier ✅ | Low barrier 🚨 |
| Network effects | Strong barrier ✅ | No barrier 🚨 |
| Regulatory barriers | Protects incumbent ✅ | Open competition 🚨 |

### Force 5: Threat of Substitutes

| Substitute Risk | Example |
|-----------------|---------|
| Low | iPhone → App Store ecosystem ✅ |
| High | Fuel car → EV ⚠️ |
| Very High | Physical retail → E-commerce 🚨 |

---

## Part 3: Supply Chain Finance Risk (迪链-Type)

### 🚨 New Mandatory Check

**Ask this for every company:**

| Check | Question | Danger Signal |
|-------|----------|--------------|
| Supply chain financing | Does company use supplier financing tools? | 迪链/商票模式 ⚠️ |
| Scale | How large is supply chain finance? | >20% of OCF 🚨 |
| Supplier dependency | Are suppliers highly dependent on this company? | Yes = systemic risk ⚠️ |
| What-if scenario | What if sales drop 30%? Can suppliers survive? | Supplier collapse = company risk ⚠️ |

### The 迪链 Pattern (Case Study)

```
Company Profile:
- OCF: ¥593B positive ✅
- Apparent debt: ¥277B (5% of liabilities) ✅
- Reality: ¥4000B+ 迪链 (supply chain financing) ⚠️
- Real net debt: ¥3230B (vs reported ¥277B) 🚨

Key Insight:
OCF ¥593B ≠ "Great business"
OCF ¥593B = "Real business ¥593B" + "Supplier financing ¥???B"

Danger: If monthly sales drop below threshold (BYD: ~150k/month),
suppliers face cash crunch → systemic redemption crisis
```

### Red Flags for Supply Chain Finance

| Flag | What It Means |
|------|--------------|
| Company brags about "zero-interest supplier financing" | They're extracting from suppliers ⚠️ |
| Supplier Average Payment Period > 180 days | Likely using supply chain finance ⚠️ |
| Reported debt low but company dominates suppliers | Hidden leverage ⚠️ |
| Industry has "dominant player" + weak suppliers | Systemic risk if dominant player stumbles ⚠️ |

---

## Part 4: Hidden Liabilities Checklist

### 🚨 New Section — Always Check These

| Hidden Liability | How to Detect | Risk Level |
|----------------|---------------|-----------|
| Supply chain financing (迪链) | Notes payable + accounts payable days | 🚨 High |
| Operating lease obligations | Off-balance sheet leases | ⚠️ Medium |
| Product warranties/recalls | Accumulated warranty reserves | ⚠️ Medium |
| Environmental remediation | EPA-type obligations | ⚠️ Medium |
| Pension underfunding | Pension assets vs liabilities | ⚠️ Medium |
| Related party guarantees | Guarantees on affiliate debt | 🚨 High |
| Sales-type leasing (dealer inventory) | Auto manufacturers special | 🚨 High |

**Formula for Real Net Debt**:
```
Real Net Debt = Reported Net Debt
              + Supply Chain Finance (迪链-type)
              + Operating Lease PV
              + Pension Underfunding
              + Related Party Guarantees
              - Excess Cash above operational needs
```

---

## Part 5: Industry Lifecycle Check

### Which Stage Is This Industry In?

| Stage | Characteristics | Investment Implication |
|-------|----------------|----------------------|
| **Introduction** | High growth, unproven model | High risk, high reward |
| **Growth** | Revenue growing 20%+, competition emerging | Buy if moat forming |
| **Mature** | Growth <10%, price war begins | ⚠️ Buffett: "bad industry" |
| **Decline** | Revenue shrinking, overcapacity | 🚨 Avoid |

**The Price War Signal**:
```
Mature/Decline Indicators:
- Industry-wide price cuts
- "Winner takes all" narrative
- Capacity expansion despite declining margins
- Weak players not exiting
→ Buffett 1977: "In bad industries, even brilliant management fails"
```

---

## Updated Case Library

| Project | Type | Conclusion |
|---------|------|-----------|
| Qutoutiao | Ponzi-lite | 🚨 Avoid — no moat, DCF always negative |
| StepN | Ponzi-lite | 🚨 Avoid — token has no cash flow, Ponzi structure |
| WeWork | Turnaround trap | 🚨 Avoid — no moat, management failure |
| Quibi | Concept failure | 🚨 Avoid — no user stickiness, unit economics collapsed |
| AMC | Meme-stock Ponzi | 🚨 Avoid — dilution machine, bankruptcy risk |
| RIVN | EV price war victim | 🚨 Avoid — burning cash, no clear path to profit |
| COIN | Crypto policy bet | 🚨 High Risk — regulatory uncertainty is existential |
| TSLA | Dream stock | 🚨 High Risk — PE 341, Elon Musk concentration risk |
| PLTR | Government dependency | ⚠️ Watch — AIP promising but PE 500+ is rich |
| NVDA | AI infrastructure moat | ⚠️ Watch — real moat but fully priced in |
| **BYD** | EV with hidden supply chain risk | 🚨 Watch — PE 19.7x cheap BUT ¥4000B+ 迪链 ⚠️⚠️ |
| **Geely** | Cheap EV, strong founder | ⚠️ Watch — PE 11x extremely cheap, FCF positive |

### BYD Analysis (Updated with 迪链 Finding)

**Updated structural risk**: 🔴 **Extremely High** (was "High")

| Risk | Level | Note |
|------|-------|------|
| 迪链 Supply Chain Finance | 🚨 ¥4000B+ hidden | Real net debt ¥3230B vs reported ¥277B |
| Price War | 🚨 Extreme | China EV = mature stage, price war |
| Geopolitical | 🚨 High | US 100% tariff, EU tariffs |
| OCF Quality | ⚠️ Mixed | Real ¥593B + supplier financing |
| Moat Sustainability | ⚠️ Uncertain | Moat based partly on supplier extraction |

**New Conclusion**: ⚠️ **Watch — But with much higher risk than surface metrics show**

---

## Output Format Template (Updated)

```
## 🎯 [Name] Risk Assessment

### 📋 Inspection Results
| Dimension | Result | Note |
|-----------|--------|------|
| Business Model | ✅/⚠️/🚨 | [One sentence] |
| Unit Economics | ✅/⚠️/🚨 | [One sentence] |
| Management | ✅/⚠️/🚨 | [One sentence] |
| Valuation | ✅/⚠️/🚨 | [One sentence] |
| Structural Risk | Low/Med/High/🔴 Extreme | [Key risks] |

### 🔍 OCF Quality Analysis [NEW]
| OCF Component | Amount | Quality |
|---------------|--------|---------|
| Real business OCF | ¥XXX | ✅ Clean |
| Supplier financing | ¥XXX | ⚠️ Dirty |
| Customer advances | ¥XXX | ⚠️ Conditional |
| **Total Reported OCF** | ¥XXX | [Mix assessment] |

### ⚠️ Porter's Five Forces Summary
| Force | Level | Implication |
|-------|-------|-------------|
| Supplier Power | Strong/Weak | [Note] |
| Buyer Power | Strong/Weak | [Note] |
| Competitive Rivalry | High/Med/Low | [Note] |
| New Entrant Threat | High/Med/Low | [Note] |
| Substitute Threat | High/Med/Low | [Note] |

### ⚠️ Key Risks
1. [Most serious risk — include hidden liabilities if found]
2. [Secondary risk]
3. [Other observations]

### ✅ Potential Upsides
1. [If any]
2. [If any]

### 📊 Quantitative Scorecard
| Metric | Value | Signal |
|--------|-------|--------|
| Forward P/E | xxx | ✅/⚠️/🚨 |
| PEG | xxx | ✅/⚠️/🚨 |
| ROE | xxx | ✅/⚠️/🚨 |
| FCF | xxx | ✅/⚠️/🚨 |
| Real Net Debt | xxx (vs reported yyy) | ⚠️ Hidden risk |
| Debt/Equity | xxx | ✅/⚠️/🚨 |

### 📌 Framework Quotes
> "[Relevant Buffett quote]"
> "[Relevant Porter insight]"

---
**Overall**: □ Investable  □ Watch  □ Avoid
```

---

## Cross-Stock Comparison Template (Updated)

```
| Metric | [Stock A] | [Stock B] | Winner |
|--------|-----------|-----------|--------|
| Market Cap | $X | $Y | [A/B] |
| Forward P/E | Xx | Yx | ✅ Cheaper |
| **Real Net Debt** | ¥X (rep ¥Y) | ¥X (rep ¥Y) | ⚠️ Hidden risk |
| **OCF Quality** | Clean/Mixed/Dirty | Clean/Mixed/Dirty | ✅ Cleaner |
| ROE | X% | Y% | ✅ Higher |
| Net Margin | X% | Y% | ✅ Higher |
| FCF | $X | $Y | ✅ Better |
| Debt/Equity | X% | Y% | ✅ Lower risk |
| Supplier Power Dependency | High/Med/Low | High/Med/Low | ⚠️ Risk |
| Founder Ownership | X% | Y% | ✅ Stronger |
| Moat Depth | Strong/Med/Weak | ... | ... |
| Price War Resilience | Strong/Med/Weak | ... | ... |
| Industry Lifecycle | Intro/Growth/Mature/Decline | ... | ... |

Overall: □ [A]  □ [B]  □ Tie
```

---

## Quantitative Decision Matrix

When scoring, use 1-5 stars:

| Score | Meaning | Action |
|-------|---------|--------|
| ⭐⭐⭐⭐⭐ (5) | Exceptional — rare opportunity | Strong buy |
| ⭐⭐⭐⭐ (4) | Good — meets all criteria | Buy on dips |
| ⭐⭐⭐ (3) | Average — mixed signals | Watch only |
| ⭐⭐ (2) | Below average — multiple concerns | Avoid or sell |
| ⭐ (1) | Poor — fails most tests | Avoid |

**Final Score = Average of 5 layers**
**Penalty**: If hidden liabilities >50% of reported → automatic downgrade 1 star

---

## Key Lessons from Recent Cases

### The 迪链 Lesson (BYD)
```
What we missed: OCF ¥593B looked great, but didn't ask "HOW?"
Buffett asks: "Is this a good business?"
Porter asks: "Why can this company extract ¥4000B from suppliers?"
Answer: Because suppliers are weak → Not a sustainable moat
New rule: Always ask "Where does the OCF actually come from?"
```

### The Correct Process
```
1. Buffett Layer 1-5: Check business quality
2. OCF Quality Check: Is OCF from real business or financing?
3. Porter Five Forces: Why does industry structure allow this?
4. Hidden Liabilities: What's NOT on the balance sheet?
5. Industry Lifecycle: Is this a price war (mature) industry?
```

---

## Related Resources

- Buffett Moat Framework: [[护城河 (Moat) - 投资概念]]
- Buffett Valuation: [[内在价值 (Intrinsic Value)]]
- Safety Margin: [[安全边际 (Margin of Safety)]]
- Complete checklist: Feishu Wiki (投资风险快筛表)
