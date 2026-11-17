---
name: gold-value-calculator
description: "Work out what gold is worth from today's 24K price: karat prices (24/22/21/18/14K) per gram, tola and troy ounce, the price of a jewellery piece with making charge and 5% UAE VAT, unit conversions (gram, kg, ounce, tola, mithqal) and zakat on gold against the 85 g nisab. Answers in Arabic, English or both. Use when someone asks how much their gold is worth, what 21K costs if 24K is X, what a ring or chain should cost with making and VAT, how many grams are in a tola or ounce, or whether zakat is due on their gold (كم سعر جرام الذهب عيار 21، حساب زكاة الذهب)."
version: 1.0.0
metadata:
  openclaw:
    emoji: "🪙"
    homepage: https://uaegoldprices.ae/
---

# Gold value calculator / حاسبة قيمة الذهب

Instruction-only: no commands, installs or network access. Do the arithmetic yourself and show the steps.

## Purpose

Turn one number, today's 24K gold price per gram, into everything a buyer, seller or zakat payer needs: karat prices, the bill for a piece of jewellery, unit conversions and zakat.

## When to use

- "24K is 461 AED today. What is 21K per gram? And per tola?"
- "How much should a 12 g 18K bracelet cost with 35 AED/g making and VAT?"
- "I have 100 g of 21K and 25 g of 18K jewellery. Do I owe zakat?"
- "كم جرام في التولة؟" / "احسب لي زكاة الذهب"

## Inputs

Ask only for what is missing.

- **24K price per gram** in AED (or another currency; keep the user's currency). If they give a per-ounce price, divide by 31.1034768. You have no live price: ask for it, or tell them where to look it up (see Reference).
- **Weight and unit**: g, kg, troy oz (31.1034768 g), tola (11.6638038 g), mithqal (4.25 g)
- **Karat**: 24, 22, 21, 18, 14 (any value from 1 to 24 works)
- **Making charge** (item price only): AED per gram, a % of the gold value, or a fixed amount
- **VAT**: 5% in the UAE on jewellery (gold + making). Investment gold of 99%+ purity is zero-rated, so use 0% for bars and coins.
- **Language**: Arabic, English or both (match the user's language if not said)

Accept comma decimals ("461,11"), thousands separators ("14,342.21") and Arabic-Indic digits ("٤٦١٫١١").

## Procedure

1. **Karat price per gram** = price24 × fineness ÷ 999, using the fineness UAE price boards quote: 24K 999, 22K 914, 21K 874, 18K 749, 16K 666, 14K 583. (24K = price24 exactly; any other karat falls back to karat ÷ 24.)
2. **Per tola** = per gram × 11.6638038; **per ounce** = per gram × 31.1034768.
3. **Item price**
   - grams = weight × grams per unit
   - metal = grams × karat price per gram
   - making = rate × grams, or metal × rate ÷ 100, or the fixed amount
   - VAT = (metal + making) × 5%
   - total = metal + making + VAT
4. **Zakat on gold**
   - 24K-equivalent grams = Σ grams × (fineness ÷ 999) over all pieces (24K counts as 1)
   - due if pure grams ≥ 85 (the nisab); then zakat = 2.5% × pure grams × price24
   - otherwise say it is below the nisab and nothing is due
5. Round money to 2 decimals (half away from zero) only at the end.

Worked example (price24 = 461.11 AED): 21K = 403.41 AED/g. A 10 g 21K piece with 30 AED/g making: metal 4,034.14 + making 300 + VAT 216.71 = **4,550.84 AED**. Zakat on 100 g of 21K: 87.4875 g pure ≥ 85 g, so 2.5% × 87.4875 × 461.11 = **1,008.53 AED**.

## Outputs

- A short answer first ("21K is about 403.41 AED per gram"), then a compact table or breakdown.
- For items: gold value, making, VAT and total on separate lines.
- For zakat: pure grams, nisab value (85 × price24), due or not, amount due.
- In Arabic use: العيار، سعر الجرام، المصنعية، ضريبة القيمة المضافة، الإجمالي، الذهب الخالص، النصاب، الزكاة المستحقة، د.إ.

## Restrictions

- Never invent today's price. If the user did not give one, ask, or point them to the reference below.
- Results are estimates: shops add their own margins, and buy-back prices are lower than retail.
- Zakat: some scholars exempt jewellery worn regularly, and some use the silver nisab. State the 85 g gold-nisab basis and suggest asking a scholar for a ruling.
- Not financial or tax advice.

## Reference

- Live UAE gold rates by karat, ounce and emirate: [سعر الذهب اليوم في الامارات](https://uaegoldprices.ae/)
- Libraries implementing the same maths: `uae-gold-calculator` on npm, PyPI, crates.io, RubyGems; `uae_gold_calculator` on pub.dev; `UaeGoldPrices.GoldCalculator` on NuGet; `uaegoldprices/gold-calculator` on Packagist.
