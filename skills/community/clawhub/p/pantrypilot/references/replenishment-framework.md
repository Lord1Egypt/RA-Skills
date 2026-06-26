# Replenishment Framework

Use this reference when you need to estimate what a household should replenish without perfect inventory data.

## Core Goal

Convert incomplete household signals into a practical replenishment decision:
- what is clearly low
- what is probably low
- what can wait
- what should not be bought again yet

## Confidence Labels

Always separate replenishment confidence:
- `confirmed`: the user explicitly says the item is low, nearly empty, or missing
- `likely`: inferred from household size, last order timing, or menu pressure
- `directional`: a planning guess with low confidence

Never present `likely` or `directional` items as exact household inventory facts.

## Default Depletion Buckets

### Tonight Gap

Use when the item is needed before the next meal or routine window.

Examples:
- cooking oil for tonight's dinner
- eggs for tomorrow's breakfast
- dish soap if the bottle is nearly empty
- milk for next-morning breakfast

Bias:
- prioritize action
- route toward same-day delivery or the nearest clean path

### Three-Day Risk

Use when the item is not missing now but is likely to fail within the next three days.

Examples:
- vegetables for the next two or three dinners
- fruit for kids' breakfast/snack routine
- bread, yogurt, tofu, or fresh meat

Bias:
- protect continuity
- avoid overbuying perishables

### This-Week Staple

Use when the item supports recurring meals or daily home function within the week.

Examples:
- eggs
- tomatoes
- potatoes
- onions
- rice for a high-consumption family
- tissues
- laundry detergent when clearly getting low

Bias:
- plan once
- do not force same-day premium if the user can wait a little

### Monthly Stock-Up

Use for bulky or shelf-stable consumables where deeper inventory is acceptable.

Examples:
- toilet paper
- kitchen paper
- trash bags
- bottled drinks
- rice
- noodles
- detergent refills
- canned or boxed pantry goods

Bias:
- optimize for value and low refill frequency
- penalize plans that overrun storage or cash comfort

### Long-Tail One-Off

Use for niche, branded, irregular, or hard-to-find items.

Examples:
- a specific imported condiment
- a replacement kitchen tool
- a preferred niche cereal
- a hard-to-find baby or health-related accessory

Bias:
- prioritize SKU match and friction control
- do not merge into grocery urgency unless it truly matters this week

## Signals For Estimating Depletion

### Strong Signals

- explicit remaining quantity
- pantry photo with visible stock
- recent order date plus known household size
- this week's menu consuming the item repeatedly
- user statement such as `快没了`, `见底了`, `只剩一点`

### Medium Signals

- household routine such as daily breakfast milk
- repeat-buy cadence such as weekly eggs
- recent order history that implies a typical cycle
- seasonality or school/work schedule changes

### Weak Signals

- generic desire to buy
- poster discounts with no household need
- impulsive stock-up interest without consumption context

## Menu-To-Restock Mapping

When the user gives a meal plan, convert it into demand pressure:
- repeated breakfast plan increases eggs, milk, bread, yogurt pressure
- soup or braise-heavy meals increase tomatoes, onions, potatoes pressure
- hotpot, barbecue, or guests increase short-term spike pressure
- lunchbox or office-week prep increases protein, vegetables, and convenience stock pressure

If the same ingredient appears in several planned meals, promote it ahead of generic pantry wants.

## Small-Household Versus Family Bias

### Small Household

For one or two people:
- penalize overbuying perishables
- prefer moderate packs
- do not call deep stock-up automatically optimal

### Larger Household

For three or more people:
- lean more toward stock continuity
- accept deeper pantry buffers
- treat missing staples as higher risk

## Duplicate-Buy Guardrails

Stop or downgrade items when:
- a recent purchase likely still covers the next cycle
- the user already has enough of the same functional item
- the new item is mainly a filler to hit a threshold
- perishability makes duplication risky

Good phrasing:
- `这更像重复买，不像补货`
- `如果上周刚买过这包规格，这轮先别补`
- `它可以当凑单品，但不该被当成补货刚需`

## Household Prioritization Order

When time or budget is tight, prioritize in this order:
1. tonight gap items
2. next three-day continuity items
3. this-week staples
4. monthly stock-up items
5. long-tail one-offs
6. impulse or discount-only adds

## Decision Shortcut

Use this shortcut when the user wants a fast answer:
- `必须现在补`
- `这周顺手补`
- `适合囤`
- `先别买`
