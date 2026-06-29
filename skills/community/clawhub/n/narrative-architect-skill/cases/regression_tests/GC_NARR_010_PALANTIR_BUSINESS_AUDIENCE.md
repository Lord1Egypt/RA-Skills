# GC_NARR_010_PALANTIR_BUSINESS_AUDIENCE

## Task

Explain Palantir to a general business audience with no technical background.

## Target Audience

普通商业听众。不熟悉计算机技术。需要理解 Palantir 做什么、为什么重要。不一定是潜在客户，可能是投资人、合作伙伴、行业观察者。

## Required Behavior

The system must:

1. Enter from a recognizable business pain point, not from technical architecture
2. Avoid listing product names (Foundry, Gotham, AIP, Apollo) as the opening move
3. Not fabricate precise numbers (revenue, market share, valuation, client count)
4. Not narrow the company to a single capability ("it's just...")
5. Not use unverified strong assertions ("the leader in...", "the only company that...")
6. Preserve fact boundary: what Palantir does vs. what it doesn't do, what it started as vs. what it does now

## Bad Output Patterns

### Pattern 1: Fabricated Precision

```text
Palantir 成立于 2003 年，由 Peter Thiel 和其他四位 PayPal 前员工共同创立...
```

Why bad: "四位" is invented. Source material does not specify the exact number of co-founders.

Fix: "由 Peter Thiel 等人创立" or omit founding detail entirely if not needed for audience understanding.

### Pattern 2: Product Dump

```text
Palantir 有四大产品：Gotham 是给政府和情报部门用的，Foundry 是给商业客户用的...
```

Why bad: Business audience without technical background does not care about product names. This reads as a product catalog, not an explanation.

Fix: Explain what the company does before naming anything.

### Pattern 3: Narrowing

```text
Palantir 本质上就是一家大数据分析公司。
```

Why bad: "本质上就是" narrows the company to one capability and implies others are wrong. Palantir itself disputes the "data company" label.

Fix: "更准确地说" or describe capability without pinning to a single category.

### Pattern 4: Unverified Assertion

```text
Palantir 是全球最大的数据整合平台。
```

Why bad: "全球最大" is an unverified superlative. No source supports this claim.

Fix: Remove superlative unless sourced.

### Pattern 5: Missing What It Doesn't Do

A narrative that describes Palantir's data integration but never mentions it is NOT a data broker, NOT a data miner, and does NOT maintain a centralized database of client information.

Why bad: Common public misconceptions go uncorrected. The audience may leave with wrong assumptions.

### Pattern 6: Unverified Absolute Claims

```text
Palantir 不建数据库，不买卖数据。
```

Why bad: "不建数据库" is an absolute negative claim. While Palantir itself says "we are not a data company," the phrasing "不建数据库" is ambiguous—Palantir platforms store and index integrated data. Without source verification, this risks overstatement.

Fix: "更偏向对接已有系统而非自建数据仓库" or "公开材料中强调其不做数据交易" with appropriate hedging.

Similarly risky:

```text
用友让你换系统。
```
Why bad: "让你换系统" is an absolute framing of a commercial strategy. While YonBIP is a platform migration play, the company frames it as digital transformation, not forced replacement.

Fix: "用友的路线更偏向让企业迁到统一平台上" or equivalent bounded phrasing.

### Pattern 7: Affective Arc Leakage

```text
**affective_arc** → temperature: 2 · frustration → recognition → clarity
```

Why bad: Internal diagnostic metadata must not appear in final output. Affective Arc is hidden by default per visibility policy.

Fix: Never output affective arc labels, temperatures, or emotion paths unless the user explicitly asks for debugging or analysis.

## Golden Output Standards

A passing output should:

1. Open with: a recognizable business pain (scattered information, inconsistent data across departments)
2. Core mechanism: explain the "translation layer / unified map" concept without jargon
3. Analogy: use at most one analogy, and the analogy must clarify the mechanism
4. Origin: mention government/intelligence origin to explain the company's philosophy, but do not dwell on it
5. Capability framing: use bounded language ("更偏向", "可以理解为", "通常", "核心之一") instead of absolute claims ("不建数据库", "替换系统", "全球最大")
6. Close with: practical value — "why this matters to a business"
7. No affective arc leakage: emotional temperature and emotion path must not appear in output

## Checklist

- [ ] Opens with business pain, not product name
- [ ] No invented numbers or dates
- [ ] No "最大的", "唯一的", "领先的" without source
- [ ] No "本质上就是" narrowing
- [ ] No unverified absolute claims ("不建数据库", "替换系统")
- [ ] Bounded phrasing used where facts are incomplete ("更像", "通常", "更偏向", "可以理解为")
- [ ] At most one analogy
- [ ] Practical value stated at end
- [ ] No affective arc metadata visible in output
