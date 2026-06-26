# Profit Calculator — Output Template

Use this template to structure the per-unit profit waterfall analysis. Fill in each section with data gathered during the workflow steps.

---

## 1. SKU & COGS Summary

| SKU ID | Product Name | Factory Cost | Freight/Unit | Duty/Unit | Packaging | Prep/Other | **Landed Cost** |
|--------|-------------|-------------|-------------|-----------|-----------|------------|----------------|
| | | $ | $ | $ | $ | $ | **$** |
| | | $ | $ | $ | $ | $ | **$** |
| | | $ | $ | $ | $ | $ | **$** |

**COGS notes:**
- Date of most recent PO: ___
- Freight method: ocean / air / mixed
- Duty rate source: HTS code ___ at ____%
- Next expected cost change: ___

---

## 2. Channel Fee Schedule

### Channel: _______________

| Fee Type | Rate / Amount | Per-Unit Cost at Current ASP |
|----------|--------------|------------------------------|
| Commission / Referral | % | $ |
| Fulfillment fee | flat / tiered | $ |
| Payment processing | % + flat | $ |
| Storage (monthly) | $/unit/month | $ |
| Subscription (amortized) | $/month ÷ units | $ |
| Other: ___ | | $ |
| **Total channel fees** | | **$** |

*(Duplicate this table for each channel)*

---

## 3. Shipping & Fulfillment Costs

| Channel | Pick & Pack | Outbound Shipping | Materials | Multi-Item Adjustment | **Total per Unit** |
|---------|-----------|-------------------|-----------|----------------------|-------------------|
| DTC | $ | $ | $ | ÷ ___ units/order | **$** |
| Amazon FBA | Included in FBA fee | — | — | — | **$0.00** |
| TikTok Shop | $ | $ | $ | | **$** |
| Walmart | $ | $ | $ | | **$** |

**Shipping notes:**
- 3PL provider: ___
- Average shipping zone: ___
- Average package weight: ___ lbs
- Free shipping threshold: $___

---

## 4. Ad Spend Allocation

| Channel | Monthly Ad Spend | Monthly Revenue | Ad Cost % | Attribution Model | Per-Unit Ad Cost |
|---------|-----------------|----------------|-----------|-------------------|-----------------|
| DTC (Meta) | $ | $ | % | ___-day click | $ |
| DTC (Google) | $ | $ | % | | $ |
| Amazon (SP + SB) | $ | $ | % | | $ |
| TikTok Shop | $ | $ | % | | $ |
| **Total** | **$** | **$** | **%** | | |

**Allocation method used:** Blended MER / Channel-specific ROAS / SKU-level ROAS

**Blended MER (for reference):** Total ad spend $____ ÷ Total revenue $____ = ____%

---

## 5. Return Cost Model

| Channel | Return Rate | Reverse Logistics | Product Loss | Restocking Labor | Orig. Shipping Lost | **Cost per Return** | **Cost per Unit Sold** |
|---------|------------|-------------------|-------------|-----------------|--------------------|--------------------|----------------------|
| DTC | % | $ | $ | $ | $ | **$** | **$** |
| Amazon | % | $ | $ | $ | $ | **$** | **$** |
| TikTok | % | $ | $ | $ | $ | **$** | **$** |

**Product disposition rates:**
- Full price resellable: ___%
- Liquidation / discount: ___%
- Write-off / unsellable: ___%

**Product loss calculation:** (Liquidation % × discount amount) + (Write-off % × full COGS) = $____ average product loss per return

---

## 6. Overhead Allocation

| Overhead Category | Monthly Cost |
|-------------------|-------------|
| Warehouse / office rent | $ |
| Team salaries (non-variable) | $ |
| Software subscriptions | $ |
| Insurance | $ |
| Professional services | $ |
| Equipment / depreciation | $ |
| **Total monthly overhead** | **$** |

**Allocation method:** Revenue-weighted / Unit-weighted / Activity-based

| Channel | Revenue Share | Overhead Allocated | Units Sold | **Overhead per Unit** |
|---------|-------------|-------------------|-----------|----------------------|
| DTC | % | $ | | **$** |
| Amazon | % | $ | | **$** |
| TikTok | % | $ | | **$** |

---

## 7. Profit Waterfall — Per SKU Per Channel

### SKU: _______________ | ASP varies by channel

| Waterfall Line | DTC | Amazon | TikTok | Walmart |
|---------------|-----|--------|--------|---------|
| Retail price | $ | $ | $ | $ |
| − Platform fees | −$ | −$ | −$ | −$ |
| = Net after fees | $ | $ | $ | $ |
| − COGS (landed) | −$ | −$ | −$ | −$ |
| = Gross profit | $ | $ | $ | $ |
| − Shipping/fulfillment | −$ | −$ | −$ | −$ |
| = After fulfillment | $ | $ | $ | $ |
| − Ad spend allocation | −$ | −$ | −$ | −$ |
| = Contribution pre-returns | $ | $ | $ | $ |
| − Return costs | −$ | −$ | −$ | −$ |
| = Contribution post-returns | $ | $ | $ | $ |
| − Overhead allocation | −$ | −$ | −$ | −$ |
| = **Net contribution** | **$** | **$** | **$** | **$** |
| **Net margin** | **%** | **%** | **%** | **%** |

*(Duplicate this table for each SKU)*

---

## 8. Decision Summary

### SKU Rankings by Net Contribution Margin

| Rank | SKU | Best Channel | Margin | Worst Channel | Margin | Action |
|------|-----|-------------|--------|--------------|--------|--------|
| 1 | | | % | | % | Scale |
| 2 | | | % | | % | Maintain |
| ... | | | % | | % | |
| Last | | | % | | % | Kill / Reprice |

### Action Items

| SKU | Channel | Current Margin | Issue | Recommended Action | Expected Impact |
|-----|---------|---------------|-------|-------------------|----------------|
| | | % | | | +$___ /unit |
| | | % | | | +$___ /unit |

### Sensitivity Analysis Summary

| Scenario | Impact on Blended Margin |
|----------|------------------------|
| Price +$2 all channels | +___% |
| Price −$2 all channels | −___% |
| COGS +10% | −___% |
| Return rate −5 points | +___% |
| Ad spend −20% | +___% |

### Refresh Schedule

| Data Point | Refresh Frequency | Owner | Next Due |
|-----------|-------------------|-------|----------|
| COGS / landed cost | Per PO or quarterly | | |
| Platform fees | Quarterly or on fee change | | |
| Shipping rates | Quarterly or on contract renewal | | |
| Ad spend / ROAS | Monthly | | |
| Return rates | Monthly | | |
| Overhead | Quarterly | | |
