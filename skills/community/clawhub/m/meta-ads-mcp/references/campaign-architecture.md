# Account, Architecture & Naming

## 1. Account & Business Setup

### Which Ad Account & Business Manager to Use

- **Always operate through Meta Business Manager** (`business.facebook.com`), never through personal ad accounts. Business accounts have better access controls, billing protection, and asset management.
- Identify the correct **Ad Account ID** (`act_XXXXXXXXXX`) before executing any action. Use `ads_get_ad_accounts` to list accessible accounts.
- Identify the correct **Business ID** using `ads_get_pages_for_business` if page-level targeting is needed.
- Each website/brand should have its own dedicated ad account when possible. Mixing unrelated brands muddles reporting and increases account-risk blast radius.
- Keep the **billing method verified** before launch. Unverified billing can pause campaigns automatically.

### MCP Account Verification Checklist

Run before the first campaign:

1. `ads_get_ad_accounts` — confirm correct account IDs are accessible.
2. `ads_get_pages_for_business` — confirm the correct Facebook Page is linked.
3. `ads_catalog_get_catalogs` — check whether a product catalog exists for dynamic ads.
4. `ads_get_dataset_details` — verify Pixel/dataset is installed and receiving events.
5. `ads_get_dataset_quality` — check Event Match Quality score; target `7+/10`.

---

## 2. Campaign Architecture — Three-Tier Hierarchy

```text
Campaign  (Objective + Budget Strategy)
  └── Ad Set  (Audience + Placement + Schedule + Budget)
        └── Ad  (Creative + Copy + CTA + Destination URL)
```

### Campaign Level

- Sets the **objective** — the single most important decision. Meta optimizes delivery for this goal.
- Sets **budget strategy**: CBO (Campaign Budget Optimization) or ABO (Ad Set Budget Optimization).
- Prefer one campaign per **product / funnel stage / business goal**.

| Business Goal | Campaign Objective |
|---|---|
| Drive website visits | Traffic |
| Get form submissions / leads | Leads |
| Sell a product | Sales |
| Grow brand recognition | Awareness |
| Promote content or page engagement | Engagement |
| Promote an app | App Promotion |

> **2026 update:** Detailed interest targeting was deprecated January 2026. Use **Advantage+ Audience** or **broad targeting with strong creative** as the primary strategy. Interest-based audiences created before October 2025 no longer deliver reliably.

### Ad Set Level

- Contains **audience**, **placement**, **schedule**, and **budget** if using ABO.
- Recommended range: **3–5 ad sets per campaign** — enough to test, not enough to fragment budget.
- Each ad set should target a **distinct, non-overlapping audience segment**.
- Minimum audience size: **50,000+ users** for efficient delivery.
- Budget must support roughly **50 optimization events per week** to exit the Learning Phase.

### Ad Level

- Contains **creative**, **headline**, **body copy**, **CTA button**, and **destination URL**.
- Recommended range: **3–5 ads per ad set** — enough for testing without starving delivery.
- Name ads consistently for reporting clarity.

---

## 3. Naming Conventions — Mandatory

Use consistent naming across all three levels.

### Campaign / Ad Set Format

```text
[Site] | [Objective] | [Funnel Stage] | [Audience/Test Variable] | [Date YYYY-MM]
```

Examples:

```text
BrandA | Traffic | Cold | Broad-Advantage+ | 2026-05
BrandB | Leads | Warm | Video-Viewers-LAL | 2026-05
BrandC | Sales | Retargeting | Site-Visitors-30d | 2026-05
```

### Ad Format

```text
[Site] | [Format] | [Angle/Hook] | [Variation Letter]
```

Examples:

```text
BrandA | Video | Founder-Story | A
BrandB | Image | Testimonial | B
BrandC | Carousel | Product-Benefits | C
```
