# Support insights → PDP FAQ playbook

Load when `pdp-faq-from-support` needs extra depth. Use by section.

---

## 1. Rolling 30-day window (operational)

| Step | Action |
|------|--------|
| Export | Tickets/chats closed or tagged in last 30 days; include product handle or SKU if available |
| De-identify | Remove names, emails, addresses; keep product and objection text |
| Tag | Pre-purchase vs post-purchase; only **pre-purchase** themes feed PDP unless user wants hybrid |
| Dedupe | Merge "Will this fit size 9?" and "Sizing for wide feet" under one **fit** theme when appropriate |
| Count | Use tag volume, keyword frequency, or agent "macro" usage as a proxy if raw counts exist |

If exports are messy, prioritize **themes that appear in both** chat and email—higher confidence.

---

## 2. What counts as "conversion-blocking"

Strong candidates:

- Compatibility (device, skin type, vehicle model, software version)
- Authenticity, warranty, certification
- Sizing, materials, allergens, safety for kids/pets
- Shipping timeline to decision-relevant dates (events, holidays)
- Subscription / refill / cancellation anxiety
- Comparison ("vs Competitor X") — answer with **facts you can defend**, not trash talk

Weak candidates for PDP (often better elsewhere):

- Pure order edits, tracking, refund status
- Wholesale or B2B terms unless PDP serves both audiences

---

## 3. Clustering tips (lightweight "automation")

1. **Phrase bucket** — group by intent: fit, compatibility, safety, shipping, returns, authenticity, usage.
2. **Lift rule** — if a theme appears ≥ N times in 30d (N set by user) or is cited by CS as "top 3 annoyance," include it.
3. **Edge cases** — one-off weird questions → knowledge base, not hero FAQ.
4. **Conflicts** — if agents contradict each other, flag for **single source of truth** before publishing PDP.

---

## 4. PDP placement map (examples)

| Doubt type | Typical PDP home |
|------------|------------------|
| One-line reassurance | Bullet under product title or price |
| Step-by-step usage | Collapsible FAQ + link to guide |
| Spec-heavy | Specs table footnote or tooltip |
| Trust / proof | Icon row + short FAQ + link to certificate PDF |
| Comparison | Comparison table or "Why us" strip—not hidden in FAQ only if it drives choice |

Keep **the highest-volume doubt** visible without an extra click when possible.

---

## 5. Copy pattern: doubt → selling point

**Pattern:** Acknowledge the concern → state the fact or policy → give a **positive outcome** → optional proof link.

- Avoid arguing with the customer tone ("Actually you're wrong").
- Avoid unqualified superlatives ("best," "only") unless documented.
- Prefer **specifics** (materials, test standard, region-specific shipping SLA) over vague comfort.

---

## 6. Claims and compliance guardrails

- Align on-page text with **packaging, IFU, and regulatory** language where regulated.
- If the user has no proof, write **conditional** copy ("Designed for…" vs "Guaranteed to cure…") and flag for approval.
- Record **version + date** of PDP change for audit trails when the user operates in sensitive categories.

---

## 7. Measurement (practical proxies)

| Signal | Interpretation |
|--------|----------------|
| FAQ accordion opens (analytics) | Interest in former doubt themes |
| CS macro send rate down | Possible deflection |
| Same-theme ticket volume | Lagging indicator after publish |
| PDP scroll depth to FAQ | Placement effectiveness |

Suggest a **before window** matching the **after window** (same seasonality) when comparing CVR.
