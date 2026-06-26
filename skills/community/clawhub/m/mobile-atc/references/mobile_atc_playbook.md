# Mobile ATC visibility playbook

Load when `mobile-atc` needs depth. Use by section.

---

## 1. When mobile CVR << desktop

Confirm **same attribution**, **same date range**, and **mobile definition** (exclude tablet if user cares). A **≥50% relative gap** (e.g. mobile 1%, desktop 2%+) warrants **above-fold ATC** as a top hypothesis—not the only one (speed, payment mix, and traffic quality still matter).

---

## 2. Above-fold score rubric (example weights)

Adjust weights in the answer if the user’s primary CTA is **Subscribe** not **ATC**.

| Criterion | Example weight |
|-----------|----------------|
| ATC fully visible without scroll on primary breakpoints | 30 |
| Tap target size & spacing (no crowding) | 20 |
| Visual hierarchy (price + CTA beats decorative chrome) | 15 |
| Sticky ATC or persistent path to cart | 15 |
| Competing CTAs diluted primary action | 10 |
| Load / CLS risk to CTA position | 10 |

**100** = excellent on stated viewports; document **what would add points**.

---

## 3. Scroll simulation (no tool)

Narrate **fold 1 → fold 2 → fold 3**: trust badges, variant pickers, long descriptions. Flag **walls of text** where users **think** they are still "reading the product" while **never reaching** ATC again.

---

## 4. Density heuristics

- **> ~300 words** above ATC without breaks → likely **cognitive overload**.  
- **Accordions** for shipping/returns/specs → good; **all expanded by default** on mobile → bad.  
- **Duplicate ATC** (top + bottom) → often good if **both** are real buttons, not fake anchors.

---

## 5. Layout patterns

| Pattern | Pros | Cons |
|---------|------|------|
| Sticky bottom ATC | Always in thumb zone | Hides content; needs safe-area padding |
| Inline ATC under price | Clear hierarchy | Scrolls away |
| Sticky mini-bar + expand | Balance | More dev work |

---

## 6. Platform notes (high level)

- **iOS Safari** bottom bar changes **visible viewport**—retest **after** scroll stop.  
- **Shopify themes**: watch **announcement bar + sticky header** stacking.  
- **Video hero**: ensure **mute + height** does not push ATC to fold 2+.
