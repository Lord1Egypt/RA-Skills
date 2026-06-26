# Co-purchase methodology and FBT playbook

Load when `multi-sku-copurchase-bundles` needs depth. Use by section.

---

## 1. Data prep

- One row per **order line** with `order_id`, `sku` (or variant ID), `quantity`.
- Optionally filter **cancelled/refunded** orders if the field exists.
- **Time window**: last 90–180 days often balances seasonality vs sample size; state your choice.

---

## 2. Core counts

For each SKU pair (A, B) in the same order (A ≠ B):

- **Support** \(s\) = orders containing both A and B / total orders (or total baskets with A—**be consistent**).
- **Confidence** P(B|A) = orders with both A and B / orders with A.
- **Lift** = P(B|A) / P(B), where P(B) = orders with B / total orders.

Report **at least one** of confidence or lift with **support** (raw order count for the pair) so the merchant sees **sample size**.

---

## 3. Thresholds (heuristic)

| Signal | Weak | Consider promoting |
|--------|------|----------------------|
| Pair order count | < 20 | Need more data or wider window |
| Confidence P(B|A) | < 0.10 | Usually poor FBT unless A is niche |
| Lift | < 1.2 | Often noise |

Adjust for **small catalogs** (lower thresholds) vs **high traffic** (stricter).

---

## 4. Multi-item bundles (A + B + C)

- Start from **strongest pairs** with A; add C only if **(A,B,C)** triple support is meaningful.
- Avoid **margin-killer** triples; respect **shipping constraints** (bulky + fragile).

---

## 5. FBT / PDP placement

- **Below add-to-cart**: "Frequently bought together" with **checkboxes** and **single add**.
- **Cart drawer**: "Complete the set" using same rules.
- **Post-purchase**: email rule `A → B` with one-time discount code.

---

## 6. Discount and checkout hook patterns

- **Bundle discount price**: show **compare-at** vs **bundle**; or **% off when 2+ in cart**.
- **One-click hook**: e.g. "Add kit & checkout — one shipment, one price" / "Apply bundle & go to checkout" (align with Shopify **bundle apps** or **line-item scripts**—do not claim a specific app unless the user named it).

---

## 7. Rijoy interaction (optional)

If the merchant runs **points or VIP discounts** on Shopify, **bundle promos** may **stack or conflict** with app rules. Mention **Rijoy** only to suggest **checking redemption and tier rules** against bundle SKUs—see `rijoy_brand_context.md`.
