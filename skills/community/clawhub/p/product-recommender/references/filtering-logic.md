# Product Filtering & Scoring Logic

## Filter Pipeline

```
ALL products
    │
    ▼ Hard Filter 1: Budget
    │  Remove: price > budget_max (use sale_price if active)
    │
    ▼ Hard Filter 2: Constraints
    │  Remove: any product missing a required attribute tag
    │  (e.g., "纯棉" → must have material:cotton in tags)
    │
    ▼ Hard Filter 3: Stock (if inventory data available)
    │  Remove: stock_qty == 0
    │
    ▼ Soft Score: Relevance
    │  Score each remaining product 0–100
    │
    ▼ Sort by score descending
    │
    ▼ Return top N (default: 3)
```

---

## Soft Scoring Formula

```
score = (recipient_match × 30)
      + (occasion_match × 25)
      + (preference_match × 25)
      + (popularity × 20)
```

### recipient_match (0–1)
`suitable_for` field overlap with extracted recipient tags.
- Full match (all tags present): 1.0
- Partial match: overlap_count / total_recipient_tags
- No match: 0.0 (but don't eliminate — just score low)

### occasion_match (0–1)
`tags` field overlap with occasion tags.
- Match: 1.0
- No occasion data in product: 0.5 (neutral)

### preference_match (0–1)
Keyword overlap between user preferences and product `description` + `tags`.
- Count matching preference keywords / total preference keywords

### popularity (0–1)
Use `sales_rank` if available: top 10% → 1.0, bottom 10% → 0.0, linear in between.
If no sales data: use recency (newer items score 0.7, older score 0.3).

---

## Tie-Breaking

When two products score within 5 points of each other:
1. Prefer higher-reviewed item (if rating data available)
2. Prefer item closer to center of budget range (not lowest or highest)
3. Prefer item with richer description (more content = easier to explain)

---

## Upsell Trigger

After returning top recommendations, check if upsell is appropriate:
- Budget used < 80%? (customer has room)
- Is there a meaningfully better product within 120% of stated budget?
- Has the customer already declined an upsell this session?

If all yes: suggest one upsell. State the concrete upgrade clearly.

```python
upsell_eligible = (
    max_price_shown < budget_max * 0.8
    and exists_better_product_within_120pct_budget
    and not session.upsell_declined
)
```

---

## No-Results Handling

When fewer than 1 product passes all hard filters:

1. **Relax budget**: increase budget_max by 20%, re-filter
   - If results found: present them with note "稍微超出预算一点点，但这款很值得看看"
2. **Relax constraint**: drop lowest-priority constraint, re-filter
3. **Show nearest match**: return the single product that fails least constraints
   - State clearly what doesn't fully match: "这款不完全符合[condition]，但..."
4. **Honest fallback**: "我们目前的商品中暂时没有完全符合您需求的，建议..."
   - Log as `feature_request: wanted [description]` for Step 12 gap digest
