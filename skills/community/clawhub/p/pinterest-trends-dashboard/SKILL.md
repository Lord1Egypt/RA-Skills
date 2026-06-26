---
name: pinterest-trends-dashboard
description: >
  Real-time visualization dashboard showing trending ClickBank niches, Pinterest search
  volume estimates, and affiliate payout potential. Helps users identify high-opportunity
  affiliate niches for Pinterest-based marketing. Part of Max's ClickBank + Pinterest
  automation suite for passive income generation.
---

# Pinterest Trends Dashboard

An interactive dashboard visualizing ClickBank niche profitability, trending search terms on Pinterest, and opportunity scoring. Purpose: help affiliates make data-driven niche decisions for Pinterest-based affiliate marketing.

## Status

**MVP Specification Complete** — Ready for Phase 1 build. See `BRIEF_PRD_ARCH.md` for full specification.

## Core Features (MVP)

### 1. Niche Rankings Dashboard
- Top 10 ClickBank niches ranked by 2025 revenue data
- Metrics per niche:
  - Est. annual revenue
  - Avg. affiliate payout
  - Competition score (1–10)
  - Year-over-year trend (↑ ↓ →)

### 2. Sub-Niche Drilldown
- Click any niche → expand to top 3–5 sub-niches
- Example: "Dietary Supplements" → "Fat Burning," "Muscle Growth," "Blood Sugar"
- Show top product examples + avg payouts per sub-niche

### 3. Pinterest Search Trends
- Monthly search volume estimates for niche keywords
- 5 trending search terms per niche
- Seasonal demand indicators

### 4. Opportunity Scoring Algorithm
```
Score = (Avg Payout × Search Volume) / (Competition Level)
```
- Higher score = better opportunity
- Highlights "hidden gems" (low competition, good payout)

### 5. Action Buttons
- **View Products on ClickBank** — Direct link to niche products
- **Research on Pinterest** — Pre-filled Pinterest search
- **Create Board** — Board strategy guide (future feature)

## Tech Stack

- **Frontend:** Next.js (React 19) + Tailwind CSS
- **Data:** Static JSON (niches-2025.json) + optional API routes
- **Deployment:** Vercel (free tier)
- **Build Time:** 3–4 hours (MVP)

## Data Structure

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
        }
      ]
    }
  ],
  "lastUpdated": "2026-03-08"
}
```

## Component Architecture

```
App Layout
├── Header (Title + Last Updated)
├── Left Sidebar
│   └── NicheSelector
├── Center
│   └── NicheChart (Rankings + Metrics)
├── Right Sidebar
│   ├── SubNicheDetails
│   └── SearchTrends
└── Footer (Data Sources)
```

### Key Components

| Component | Purpose |
|-----------|---------|
| `NicheChart` | Bar/card ranking of niches, click to select |
| `SubNicheDetails` | Shows sub-niches + top products for selection |
| `SearchTrends` | Pinterest search volume + trending terms |
| `OpportunityScore` | Score calculation + "hidden gems" highlight |

## Integration with Affiliate Automation Suite

### 1. ClickBank Scraper → Dashboard
```
clickbank-scraper (daily job)
    ↓
latest.json (product data)
    ↓
pinterest-trends-dashboard (niche opportunity view)
    ↓
[User selects niche]
    ↓
Auto-generate Pinterest pins (n8n workflow)
```

### 2. User Workflow
1. Open dashboard
2. View top niches + scores
3. Click "Research on Pinterest" → see trending keywords
4. Click "View Products" → ClickBank affiliate links
5. (Future) Auto-generate pins based on selection

### 3. n8n Workflow Integration
```javascript
// n8n "Read From Dashboard API" node
const selectedNiche = {{ $json.selectedNiche }};
const topProducts = {{ $json.products }};

// Generate Pinterest pins automatically
return {
  niche: selectedNiche,
  productCount: topProducts.length,
  action: "generate_pins"
};
```

## Development Roadmap

### MVP (Phase 1) — 4 hours
- [x] Specification complete
- [ ] Next.js project scaffold
- [ ] Data file (niches-2025.json)
- [ ] NicheChart component
- [ ] SubNicheDetails component
- [ ] Styling (Tailwind)
- [ ] Deploy to Vercel

### Phase 2 — Pinterest API Integration
- [ ] Real-time Pinterest search volume API
- [ ] Trending term discovery
- [ ] Seasonal demand tracking

### Phase 3 — ClickBank API Integration
- [ ] Live gravity scores
- [ ] Real-time payout data
- [ ] Product-level filtering

### Phase 4 — User Features
- [ ] User accounts (saved niches)
- [ ] Email alerts (trending shifts)
- [ ] Export niche analysis as PDF

### Phase 5 — Content Generation
- [ ] Auto-generate Pinterest pin templates
- [ ] Blog post outlines per niche
- [ ] Email swipe copy

## Deployment

### Build
```bash
npm run build
npm run start  # local testing
```

### Deploy to Vercel
```bash
git push origin main
# Vercel auto-deploys on push
```

### Data Updates
Update `data/niches-2025.json` monthly with latest ClickBank + Pinterest trends:
```bash
node scripts/update-niche-data.js  # future: automated script
```

## Data Sources

- **ClickBank Niches:** Official ClickBank 2025 niche rankings (blog post)
- **Affiliate Payouts:** ClickBank published averages by category
- **Pinterest Search Volume:** Pinterest Trends API (or manual estimates)
- **Competition Data:** Derived from gravity scores + search volume

## Success Metrics

1. **Usability:** Identify niche + view products in <2 minutes
2. **Accuracy:** Data matches ClickBank official rankings (high confidence)
3. **Engagement:** Track click-through rates to ClickBank affiliate links
4. **Time to Value:** Dashboard fully functional within 4 hours of starting build

## Integration with OpenClaw

Use as a sub-agent view or scheduled report generator:

```bash
# Run dashboard builder as cron job
openclaw cron add pinterest-dashboard-updater \
  --schedule "0 9 * * 0" \
  --command "cd max-co/products/pinterest-trends-dashboard && npm run build"

# Or spawn as interactive session
claude-code "Build and deploy Pinterest Trends Dashboard"
```

## File Structure

```
pinterest-trends-dashboard/
├── BRIEF_PRD_ARCH.md        # Full specification (this doc)
├── SKILL.md                  # This skill definition
├── app/
│   ├── page.tsx             # Main dashboard
│   ├── layout.tsx           # Root layout
│   └── api/
│       └── niche-data.ts    # Data endpoint (optional)
├── components/
│   ├── NicheChart.tsx       # Rankings chart
│   ├── SubNicheDetails.tsx  # Drilldown view
│   ├── SearchTrends.tsx     # Pinterest trends
│   └── OpportunityScore.tsx # Opportunity ranking
├── data/
│   └── niches-2025.json     # Static niche data
├── styles/
│   └── globals.css          # Tailwind config
├── package.json
└── next.config.js
```

## Author

Max @ max-co.digital — Autonomous affiliate marketing automation for passive income.

## License

Proprietary — Part of Digital Helper Agency / max-co product suite.

## Questions?

See `BRIEF_PRD_ARCH.md` for implementation details or integration examples.
