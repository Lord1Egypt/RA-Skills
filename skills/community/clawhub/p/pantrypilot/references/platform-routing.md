# Platform Routing

Use this reference when deciding which replenishment bucket belongs on which platform type.

## Core Principle

Do not route by advertised price alone.

Route by:
- urgency
- perishability
- basket size
- packaging depth
- SKU specificity
- execution friction

## Meituan And Similar Instant-Retail Paths

Best for:
- tonight gap items
- missing dinner ingredients
- breakfast rescue items
- emergency household consumables
- small fresh top-ups
- convenience wins where execution speed matters more than absolute lowest price

Typical strengths:
- fast same-day fulfillment
- low decision latency
- strong for small urgent baskets

Typical weaknesses:
- higher unit price on bulky stock-up items
- packaging and delivery fees can erase small discounts
- bad default path for deep shelf-stable replenishment

Bias toward Meituan when:
- the item is needed before the next meal or morning routine
- the user wants one clean order with minimal planning
- paying a little more prevents a real continuity failure

## Meituan Maicai / Duoduo Maicai / Dingdong / Hema / Similar Grocery Channels

Best for:
- planned fresh baskets
- weekly vegetable and protein replenishment
- mixed produce + staples orders
- situations where freshness and basket-level value matter more than speed alone

Typical strengths:
- more natural whole-basket replenishment than instant takeout paths
- better for weekly fresh planning
- better fit for produce and recurring ingredients

Typical weaknesses:
- city and warehouse variance
- thresholds and delivery windows matter
- not every channel wins on every basket

Bias toward these channels when:
- the user is doing a true fresh restock
- there is enough basket depth to justify the threshold naturally
- the order does not need to land in the next hour

## PDD And Similar Stock-Up Commerce Paths

Best for:
- shelf-stable staples
- paper goods
- cleaning supplies
- drinks
- pantry stock-ups
- large packs where time flexibility exists

Typical strengths:
- deep-pack and family-pack pricing
- good for lowering refill frequency
- often strongest on routine household consumables when the user can wait

Typical weaknesses:
- slower fulfillment
- more friction if the item is actually needed now
- oversized packs may look optimal but be wrong for a small household

Bias toward PDD when:
- the item is low urgency
- the item is durable or shelf-stable
- the user wants to stock up rather than rescue tonight

## Taobao / Tmall And Similar Long-Tail Marketplace Paths

Best for:
- specific branded one-offs
- hard-to-find pantry or home items
- replacement tools or accessories
- niche condiments or specialty household goods

Typical strengths:
- SKU breadth
- long-tail coverage
- easier to find exact-match items

Typical weaknesses:
- not a great default path for emergency fresh replenishment
- not ideal for mixed urgent household baskets
- may add cognitive overhead if merged into a time-sensitive restock

Bias toward Taobao when:
- the exact item matters more than speed
- the item is irregular, branded, or niche
- the household is filling a known gap rather than doing this week's core fresh restock

## Split-Platform Logic

Recommend split routing only when the split solves a real household problem:
- Meituan for tonight's gap plus PDD for non-urgent stock-up
- grocery channel for fresh basket plus Taobao for one niche item
- local fast path for perishables plus slow commerce path for bulky goods

Reject split routing when:
- the savings are tiny
- the user must manage too many delivery windows
- the split is mathematically neat but operationally annoying

## Routing Shortcuts

Use these shortcuts when the user wants a fast answer:
- `今晚缺口`: Meituan / instant retail first
- `这周鲜食`: grocery channel first
- `耐放囤货`: PDD first
- `指定单品补齐`: Taobao or Tmall first

## Anti-Fake-Savings Reminders

Before routing, pressure-test the plan:
- Is this split saving real money after fees?
- Is the threshold natural or being forced?
- Is the deep pack actually appropriate for this household?
- Is a niche item delaying an otherwise simple restock?
