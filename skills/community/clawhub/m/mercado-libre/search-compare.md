# Search and Compare - Mercado Libre

Use this file when user wants to find, shortlist, or compare products.

## Search Workflow

1. Define target outcome: best value, lowest risk, fastest delivery, or premium quality.
2. Set constraints: budget, category, must-have features, and delivery deadline.
3. Build shortlist: 3 to 5 options from distinct sellers when possible.
4. Normalize total cost before ranking.
5. Recommend one winner and one backup.

## Comparison Matrix

Build this matrix for final options:

| Factor | Option A | Option B | Option C | Weight |
|--------|----------|----------|----------|--------|
| Total price with shipping | | | | High |
| Delivery window reliability | | | | High |
| Seller reputation and volume | | | | High |
| Return and claim friction | | | | Medium |
| Feature fit for user need | | | | Critical |

Do not publish a recommendation without weights.

## Auto Shortlist Rules

- Exclude listings with inconsistent title, image, and attribute signals.
- Exclude options with unclear delivery promises when deadline matters.
- Flag suspiciously low prices as risk, not instant wins.
- Prefer options with stronger evidence of post-sale reliability.

## Output Template

```text
Decision type:
Constraints:
Compared options:
Winner:
Backup:
Why winner:
Main risk:
Review trigger:
```
