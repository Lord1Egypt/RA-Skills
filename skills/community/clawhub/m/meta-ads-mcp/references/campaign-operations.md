# Campaign Creation, KPIs & Documentation

## 11. CAMPAIGN MANAGEMENT: CREATING VIA MCP

### Creating a Campaign (Step-by-Step with MCP Tools)

**Step 1**: Gather account info
```
ads_get_ad_accounts → get act_XXXXXXXXXX
ads_get_pages_for_business → get page ID
ads_get_dataset_details → get pixel ID
```

**Step 2**: Create campaign (PAUSED)
```
ads_create_campaign
  - objective: TRAFFIC / OUTCOME_LEADS / OUTCOME_SALES
  - status: PAUSED
  - name: [naming convention]
  - special_ad_categories: [] (or CREDIT/HOUSING/EMPLOYMENT/ISSUES if applicable)
```

**Step 3**: Create ad set (PAUSED)
```
ads_create_ad_set
  - campaign_id: from step 2
  - targeting: audience definition
  - budget: daily_budget (in cents)
  - optimization_goal: LINK_CLICKS / LEAD_GENERATION / CONVERSIONS
  - status: PAUSED
```

**Step 4**: Create ad (PAUSED)
```
ads_create_ad
  - adset_id: from step 3
  - creative: image/video + copy + headline + CTA
  - status: PAUSED
```

**Step 5**: Full review before activation
- Check all levels in Ads Manager UI
- Verify pixel is attached to ad set
- Verify destination URL is correct and loads
- Verify creative and copy look correct in preview

**Step 6**: Activate (set top-level campaign to ACTIVE only after review)

---

## 12. PERFORMANCE TRACKING & KPIs

### Core KPIs by Campaign Objective

| Objective | Primary KPI | Secondary KPIs |
|---|---|---|
| Traffic | CTR (Link), CPC | Reach, Frequency, Landing Page Views |
| Leads | CPL (Cost per Lead) | Lead volume, Lead quality, Form completion rate |
| Sales | ROAS, CPA | Add-to-cart rate, Checkout initiation, Purchase volume |
| Awareness | CPM, Reach | Frequency, Video views, Brand lift |

### Reporting Cadence
- **Daily** (launch week): Check spend, CTR, any disapprovals
- **Weekly**: Full performance review — CTR, CPM, CPL/CPA, ROAS, frequency
- **Monthly**: Strategic review — winners vs. losers, budget reallocation, new creative planning

### When to Intervene
| Signal | Action |
|---|---|
| CTR < 0.5% on cold campaigns | Test new hook / creative |
| CPM rising week-over-week | Audience fatigued — refresh creative or expand audience |
| Frequency > 5 | Expand audience or pause ad set |
| Ad in "Learning Limited" status | Consolidate ad sets or increase budget |
| Spend depleting with zero conversions | Pause immediately, review pixel and landing page |
| ROAS < break-even | Pause ad set, investigate (creative? audience? landing page?) |

### Using MCP for Reporting
```
ads_get_ad_entities — pull campaign/ad set/ad performance
ads_insights_performance_trend — analyze trends over time
ads_insights_anomaly_signal — detect unusual patterns
ads_insights_auction_ranking_benchmarks — see how ads perform vs. benchmarks
ads_get_opportunity_score — get Meta's recommendations
```

---

## 13. EXTERNAL CAMPAIGN DOCUMENTATION

### Per-Campaign Document (create in Google Drive for each site)

Store in the site's designated Drive folder. Document should include:

**Campaign Brief**
- Campaign name (per naming convention)
- Objective and KPI targets
- Budget (daily, total)
- Start date / end date / ongoing
- Ad Account ID
- Pixel ID

**Audience Definition**
- Cold audience description
- Retargeting audiences and window
- Exclusions applied

**Creative Log**
| Ad Name | Format | Angle | Status | CTR | CPM | Notes |
|---|---|---|---|---|---|---|
| Seraphim-Video-Story-A | Video 4:5 | Origin Story | Active | 1.8% | $8.20 | Top performer |
| Seraphim-Image-Product-B | Image 1:1 | Product Shot | Paused | 0.4% | $12.00 | Low CTR |

**Results Tracker**
- Weekly snapshot of: Spend, Impressions, CTR, CPM, Leads/Sales, CPA/CPL, ROAS
- Notes on what changed each week

**Decisions Log**
- Date / decision / reason
- e.g. "2026-05-10: Paused ad set 2 — frequency reached 7, CTR dropped to 0.3%"

**Creative Archive**
- Link to Google Drive folder with all assets
- Retired creatives marked "Archive" — never deleted

---
