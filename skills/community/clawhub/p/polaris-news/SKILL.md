# polaris-news

Verified news intelligence for AI agents. Get real-time briefs from The Polaris Report — 160+ sources, 18 verticals, bias scored, confidence rated.

## Install

```
openclaw install polaris-news
```

## Commands

### `/news [category] [limit]`

Get the latest verified news briefs. Optionally filter by category and set result count.

```
/news              # Latest briefs across all categories
/news crypto 5     # Latest 5 crypto briefs
/news ai_ml 3      # Latest 3 AI/ML briefs
```

**Categories:** tech, policy, markets, global, science, health, startups, ai_ml, cybersecurity, climate, defense, realestate, biotech, crypto, politics, energy, space, sports

### `/brief [topic]`

Generate an on-demand intelligence brief about any topic. Returns a full brief with analysis, counter-argument, confidence score, and bias rating.

```
/brief impact of AI on healthcare
/brief bitcoin ETF inflows
/brief semiconductor export controls
```

### `/search [query]`

Search across all verified briefs. Returns the top 5 most relevant results.

```
/search federal reserve rate decision
/search nvidia earnings
/search climate policy EU
```

### `/trending`

See what's trending right now based on reader engagement.

```
/trending
```

## Pricing

| Tier | API Calls | Brief Generation | Price |
|------|-----------|------------------|-------|
| Free | 100/day | 3/day | $0 |
| Consumer | 100/day | 3/day | $9/mo |
| Usage (Pay-as-you-go) | 1,000 free/day, then $0.001/call | $0.10/brief | $0/mo + metered |
| Starter | 3,000/day | 20/mo included | $19/mo |
| Agent Pro | 10,000/day | Unlimited ($0.10 each) | $49/mo |

Free tier requires no API key. Upgrade at [thepolarisreport.com/pricing](https://thepolarisreport.com/pricing).

## Configuration

Set `POLARIS_API_URL` to point at a custom backend. Defaults to the production API.

## Privacy

This skill sends your queries to The Polaris Report API (thepolarisreport.com). Queries are used only to fetch news results and are not stored or shared. See our privacy policy: https://thepolarisreport.com/privacy

## Links

- [The Polaris Report](https://thepolarisreport.com)
- [API Documentation](https://thepolarisreport.com/docs)
- [Agent Integration Guide](https://thepolarisreport.com/agents)
