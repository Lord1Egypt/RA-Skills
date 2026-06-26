# Pinterest Trends Dashboard — Brief + PRD + Architecture

**Created:** 2026-03-08 22:14 PT  
**Status:** Ready for Review  
**Author:** Max (Autonomous Build)

---

## Executive Summary

A real-time visualization tool showing trending ClickBank niches, recommended product categories, and estimated affiliate payout potential. Purpose: help users identify high-opportunity niches for Pinterest-based affiliate marketing.

**Goal:** Convert research into a decision-making dashboard. Target user: affiliates deciding what niche to enter.

---

## Product Brief

### What We're Building
An interactive dashboard that aggregates ClickBank niche data, trending search terms on Pinterest, and affiliate payout data—then surfaces the top opportunities ranked by revenue potential and competition level.

### Why
Users need to make niche decisions quickly. Raw data exists (ClickBank published their 2025/2026 niche rankings). We package it visually with:
- Trending search volume estimates
- Average payout ranges by niche
- Competition heat map
- Recommended sub-niches
- Affiliate link generator shortcut

### Who
Beginners to intermediate affiliates exploring their first niche or pivoting.

### Key Differentiator
Most tools show "top niches" as a static list. We show *dynamic trends* + *payout potential* + *real search volume* on Pinterest specifically.

---

## Product Requirements Document (PRD)

### Core Features (MVP)

#### 1. Niche Rankings Dashboard
- **Display:** Top 10 ClickBank niches ranked by 2025 revenue data
- **Data shown per niche:**
  - Niche name (e.g., "Dietary Supplements")
  - Est. annual revenue (from ClickBank 2025 data)
  - Avg. affiliate payout ($120–$200+)
  - Competition score (1–10, based on gravity/search volume)
  - Growth trend (↑ ↓ → year-over-year)

#### 2. Sub-Niche Drilldown
- Click any niche → expand to show top 3–5 sub-niches
- Example: Dietary Supplements → "Fat Burning," "Muscle Growth," "Blood Sugar," etc.
- Show top product examples for each sub-niche

#### 3. Pinterest Search Trends
- Estimate monthly search volume for niche keywords on Pinterest
- Show 5 trending search terms related to selected niche
- Indicate seasonal demand (if applicable)

#### 4. Opportunity Scoring
- Simple algorithm: (Avg Payout × Search Volume) / (Competition Level)
- Higher score = better opportunity
- Highlight "hidden gems" (lower competition, decent payout)

#### 5. Action Buttons
- "View Products on ClickBank" → external link to niche category
- "Research on Pinterest" → prefilled Pinterest search
- "Create Board" → guide to Pinterest board strategy (future)

### Design

**Layout:**
- Header: "Pinterest Affiliate Trends Dashboard"
- Left sidebar: Niche selector (clickable list)
- Center: Main chart (horizontal bar chart or cards showing rankings)
- Right sidebar: Detailed view for selected niche
- Footer: Data sources + last update timestamp

**Visual Style:**
- Clean, minimal (Tailwind CSS)
- Color coding: Green (hot opportunity), Yellow (moderate), Red (high competition)
- Interactive: Hover for details, click to expand

**Responsive:**
- Works on desktop, tablet (portfolio use case)

---

## Architecture

### Tech Stack
- **Frontend:** Next.js (React) + Tailwind CSS
- **Data:** Static JSON (embedded) + optional API route for future real-time updates
- **Deployment:** Vercel (zero-config, integrates with Next.js)

### File Structure
```
pinterest-trends-dashboard/
├── app/
│   ├── page.tsx          # Main dashboard component
│   ├── layout.tsx        # Root layout
│   └── api/
│       └── niche-data.ts # JSON endpoint (optional for future)
├── components/
│   ├── NicheChart.tsx    # Main ranking chart
│   ├── SubNicheDetails.tsx # Drilldown view
│   ├── SearchTrends.tsx  # Pinterest search trends
│   └── OpportunityScore.tsx # Scoring display
├── data/
│   └── niches-2025.json  # ClickBank niche data + Pinterest estimates
├── styles/
│   └── globals.css       # Tailwind config
└── public/
    └── favicon.ico
```

### Data Structure (niches-2025.json)

```json
{
  "niches": [
    {
      "id": "dietary-supplements",
      "name": "Dietary Supplements",
      "rank": 1,
      "annualRevenue": 450000000,
      "avgPayout": 150,
      "competitionScore": 9,
      "trendYoY": "stable",
      "pinterestSearchVolume": 250000,
      "subNiches": [
        {
          "name": "Fat Burning",
          "topProducts": ["Mitolyn", "Leanbiome"],
          "avgPayout": 160
        },
        {
          "name": "Muscle Growth",
          "topProducts": ["Alpha Tonic"],
          "avgPayout": 140
        }
      ]
    },
    // ... 9 more niches
  ],
  "lastUpdated": "2026-03-08"
}
```

### Component Breakdown

**NicheChart.tsx**
- Displays ranked list of niches
- Bar chart or card grid showing ranking + key metrics
- Click handler to select niche → triggers drilldown

**SubNicheDetails.tsx**
- Shows sub-niches for selected parent niche
- Displays top products + avg payouts
- "View on ClickBank" button per sub-niche

**SearchTrends.tsx**
- Pinterest search volume estimate for niche keywords
- Trending terms (e.g., "weight loss supplements," "best fat burner")
- Seasonal spikes (if applicable)

**OpportunityScore.tsx**
- Calculate and display score formula
- Identify "hidden gems" (high score, low competition)
- Rank niches by score

### Pages

**`page.tsx` (Main Dashboard)**
```
Header
├── Title + description
├── Last updated (data source)
└── Quick stats (total niches, avg payout, etc.)

Main Layout
├── Left Sidebar (Niche Selector)
├── Center (NicheChart)
├── Right Sidebar (SubNicheDetails + SearchTrends)
└── Bottom (Action Buttons)
```

---

## Implementation Notes

### Data Sources
- ClickBank niche rankings: 2025 official blog post (fetched & cached)
- Pinterest search volume: Estimated from Pinterest Trends API (or manual estimates)
- Payout data: ClickBank published averages by niche

### Future Enhancements (Post-MVP)
1. Real-time Pinterest search API integration
2. ClickBank API for live payout/gravity data
3. User accounts → save favorite niches
4. Email alerts for trending shifts
5. Affiliate link prefilling

### Deployment
- Build: `npm run build` (Next.js static export)
- Deploy: Push to GitHub → Vercel auto-deploys on `main`
- Cost: Free tier (Vercel)

---

## Success Metrics
1. **Usability:** User can identify a niche + view top products in <2 minutes
2. **Accuracy:** Data matches ClickBank official niches (confidence: high)
3. **Engagement:** Click-through to ClickBank affiliate links (future analytics)

---

## Timeline
- **Design mockup:** 2 hours (this doc + Figma sketch)
- **Build (MVP):** 3–4 hours (Next.js + data embedding)
- **Deploy:** 30 minutes (Vercel)
- **Review:** Marlon feedback + iteration

**Ready to build?** Waiting for approval to start coding.
