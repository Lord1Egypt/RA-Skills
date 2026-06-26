# Promo inventory and ad sync playbook

Load when `promo-stock` needs depth. Use by section.

---

## 1. Signals to monitor

| Signal | Source examples |
|--------|------------------|
| Sellable quantity | WMS, Shopify inventory, ERP |
| Reserved / committed | Unshipped orders in promo window |
| Sell-through velocity | Units/hour or vs same hour prior week |
| Ad spend & schedules | Meta, Google, TikTok dashboards |
| Lead time | Supplier quoted days + buffer |

**Near real-time** = whatever the merchant actually has (hourly export, webhook, manual refresh)—state the lag.

---

## 2. Choosing X (threshold)

Common patterns:

- **% of allocation**: X = 20% of **quantity earmarked** for the event SKU.  
- **Days of cover (DoC)**: X = fewer than **N days** at **current burn** (state burn calculation).  
- **Absolute units**: X = below **floor** for hero SKU (e.g. 500 units).

Always separate **display inventory** from **physical** if overselling is the risk.

---

## 3. Ad actions when stock is thin

| Severity | Typical play |
|----------|----------------|
| Approaching X | Tighten audience, lower budget cap, pause broad prospecting |
| Below X | Pause SKU-specific shopping/placement; keep brand if needed |
| Stockout imminent | Pause all SKU-specific ads; landing → pre-order or waitlist |

Document **who approves** emergency pauses if the user has agency rules.

---

## 4. Pre-order copy principles

- **Ship-by or restock window** — range, not fake exact date unless fixed.  
- **Charge timing** — at order vs at ship (high level; finance owns detail).  
- **Cancellation** — link to policy.  
- **Locale** — EU/US pre-order disclosure expectations differ; suggest **legal review** when unsure.

---

## 5. Supplier email checklist

- SKU, variant, qty, date needed  
- PO #, prior ETA, consequence of miss (e.g. promo exposure without stock)  
- Ask for **written confirmation** and **tracking** when shipped  
- CC internal roles (ops, buying) as appropriate

---

## 6. T‑24h rapid pass

1. Freeze **pricing** and **inventory** sync settings if they change often.  
2. Confirm **hero SKUs** list matches **ad product feeds**.  
3. Pre-load **pre-order** PDP + **CS macros**.  
4. **Supplier** ping for in-transit lines.  
5. **Rollback plan**: if sell-through is **slow**, which ads scale back up.
