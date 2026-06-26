# Spending Categories Reference

Default categories used by `categorize.py` and how to customize them.

## Default Categories

| Category | Description |
|---|---|
| **Housing** | Rent, mortgage, HOA, storage, renters/home insurance |
| **Food & Dining** | Groceries, restaurants, coffee, food delivery |
| **Transportation** | Gas, rideshare, parking, tolls, flights, car maintenance |
| **Utilities** | Electric, gas, water, internet, phone/cell service |
| **Entertainment** | Movies, concerts, tickets, gaming, clubs, sports |
| **Shopping** | Amazon, retail, clothing, home goods, electronics |
| **Health** | Pharmacy, doctor, dental, gym, prescriptions |
| **Subscriptions** | Streaming, software, SaaS, memberships |
| **Income** | Direct deposit, payroll, Venmo/Zelle received, tax refunds |
| **Other** | Anything that doesn't match (review these manually) |

---

## How Categorization Works

`categorize.py` uses regex keyword matching against the transaction description:

1. **Income check first** — all credits (money coming in) default to Income unless clearly something else
2. **Keyword rules** — checked in priority order (Housing → Utilities → Subscriptions → Food → Transport → Health → Entertainment → Shopping)
3. **Bank category fallback** — if no keyword match, uses the bank's original category if present
4. **Other** — anything that falls through all rules

Each transaction gets a `confidence` field:
- `high` — keyword match found
- `medium` — using bank's category or unmatched credit
- `low` — fell through to "Other"

The LLM should review all `low` and `medium` confidence transactions before generating the report.

---

## Customizing Categories

### Add Keywords to an Existing Category

Edit the `CATEGORY_RULES` list in `categorize.py`. Each entry is a tuple of `(category_name, [regex_patterns])`.

Example — adding a local grocery chain to Food & Dining:
```python
("Food & Dining", [
    ...existing patterns...
    r"\bpublix\b",           # already included
    r"\bwinn-dixie\b",       # add this
    r"\bpiggly wiggly\b",    # add this
]),
```

### Add a New Category

Add a new tuple to `CATEGORY_RULES` before the `"Other"` fallback. Place it in priority order — more specific categories should appear before broader ones.

Example — adding a "Pets" category:
```python
("Pets", [
    r"\bpet supply\b",
    r"\bpetsmart\b",
    r"\bpetco\b",
    r"\bvet\b",
    r"\bveterinary\b",
    r"\banimal hospital\b",
    r"\bdog groomer\b",
]),
```

Then add it to `sample-budget.json`:
```json
{
  "monthly_budgets": {
    "Pets": 100
  }
}
```

### Rename a Category

Change the category name in both:
1. `CATEGORY_RULES` in `categorize.py`
2. `monthly_budgets` keys in your budget JSON

The report uses whatever category names appear in the categorized data — no hardcoded list in `report.py`.

### Override Individual Transactions

After running `categorize.py`, manually edit the output JSON before passing it to `report.py`. Change the `category` field on specific transactions:

```json
{
  "date": "2024-01-15",
  "description": "AMAZON.COM*AB1234",
  "amount": 29.99,
  "type": "debit",
  "category": "Subscriptions",  // changed from Shopping
  "confidence": "high"
}
```

---

## Category Patterns — Quick Reference

### Subscriptions vs. Shopping
Amazon purchases default to **Shopping**. Prime membership and Amazon subscription charges should be manually recategorized to **Subscriptions** if needed (or add `amazon.*prime` to the Subscriptions rules).

### Transportation vs. Utilities
Cell phone and internet bills go to **Utilities**. Rideshare (Uber, Lyft) and gas stations go to **Transportation**. Uber Eats goes to **Food & Dining** (matched before the Uber transportation pattern).

### Food & Dining vs. Shopping
Grocery stores (Whole Foods, Kroger, etc.) go to **Food & Dining**. General retail like Walmart and Target go to **Shopping** even if you buy groceries there.

### Credits and Refunds
- Refunds from Amazon, restaurants, etc. → categorize.py assigns them to **Income** since they're credits
- If you want refunds in the original category instead, manually recategorize after running categorize.py
- True income (payroll, etc.) stays in **Income**

---

## Adding to Budget Config

Add any category to the `monthly_budgets` object in your budget JSON. Categories without a budget entry still appear in the report — they just show without a budget comparison column.

```json
{
  "monthly_budgets": {
    "Housing": 1800,
    "Food & Dining": 600,
    "Transportation": 200,
    "Utilities": 150,
    "Entertainment": 100,
    "Shopping": 200,
    "Health": 100,
    "Subscriptions": 75,
    "Other": 50
  }
}
```

Income is excluded from budget tracking (it's money coming in, not spending).
