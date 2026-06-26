# Data Sources & Methodology Reference

## Recommended Data Sources

### Tier 1 — Primary Intelligence Sources
- **Reuters / AP** — Wire services, minimal editorial bias
- **Al Jazeera** — Strong MENA coverage
- **BBC World** — Broad international perspective
- **TASS / Xinhua** — State perspectives (read critically)

### Tier 2 — Analysis & Think Tanks
- **CSIS** (csis.org) — US foreign policy analysis
- **IISS** (iiss.org) — Military and strategic balance
- **CFR** (cfr.org) — Council on Foreign Relations
- **Brookings** (brookings.edu) — Policy analysis
- **RAND** (rand.org) — Defense and security research
- **ICG** (crisisgroup.org) — Conflict early warning

### Tier 3 — OSINT & Monitoring
- **World Monitor** (worldmonitor.app) — Real-time geopolitical dashboard
  - 435+ curated RSS feeds across 15 categories
  - CII (Country Instability Index) heatmap
  - AI-synthesized intelligence briefs
  - Live conflict/protest mapping
- **ACLED** (acleddata.com) — Armed conflict tracking
- **GDELT** (gdeltproject.org) — Event database
- **Liveuamap** — Conflict mapping

### Tier 4 — Prediction Markets
- **Polymarket** (polymarket.com) — Crypto prediction markets
  - API: `https://gamma-api.polymarket.com`
  - No authentication required
  - Endpoints: `/events`, `/markets`, `/public-search`
- **Metaculus** — Community prediction
- **Manifold Markets** — User-created markets

## Prediction Methodology

### Bayesian Reasoning Framework
1. **Base rate**: What is the historical frequency of this type of event?
2. **Update on evidence**: How does current intelligence shift the probability?
3. **Consider alternatives**: What other outcomes are possible?
4. **Calibration check**: Are probabilities consistent with evidence strength?

### Common Cognitive Biases to Avoid
- **Anchoring**: Don't over-weight the first data point
- **Availability**: Recent dramatic events aren't necessarily more likely
- **Confirmation**: Actively seek disconfirming evidence
- **Overconfidence**: Use wide probability ranges for genuine uncertainty

## World Monitor Integration

When World Monitor is available as a data source:

### Useful Endpoints (from worldmonitor.app)
- Conflict tracking layer — active conflicts and hotspots
- Sanctions data — current sanctions regimes
- Country Instability Index (CII) — composite risk score per country
- AI Deduction engine — LLM-powered geopolitical analysis

### RSS Feed Categories Relevant to Geopolitical Predicting
| Category | Sources |
|---|---|
| Geopolitics | Reuters World, AP, Al Jazeera, BBC |
| Military | Jane's, Defense News, War on the Rocks |
| Conflicts | ACLED, ICG, Liveuamap |
| Diplomacy | UN News, State Department, EU External Action |
| Sanctions | OFAC, EU Sanctions Map |
| Energy | IEA, OPEC, S&P Global Platts |
