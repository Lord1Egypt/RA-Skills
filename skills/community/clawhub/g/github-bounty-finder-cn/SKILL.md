# GitHub Bounty Finder Skill

🎯 **Find high-value GitHub and Algora bounties with automated competition analysis**

## Description

GitHub Bounty Finder is a powerful scanning tool that helps developers discover lucrative bounty opportunities on GitHub and Algora. It automatically analyzes competition levels, scores opportunities, and provides actionable recommendations.

## Features

- 🔍 **Multi-Platform Scanning**: Scan both GitHub Issues and Algora bounties
- 📊 **Competition Analysis**: Analyze PR counts, comments, and engagement
- 🎯 **Smart Filtering**: Auto-filter low-competition, high-value opportunities
- 💰 **Opportunity Scoring**: 0-100 scoring algorithm based on value, competition, and freshness
- 🤖 **Automated Recommendations**: Get actionable insights for each bounty
- 📈 **Pricing Intelligence**: Market-based pricing recommendations

## Installation

```bash
# Install via clawhub
clawhub install github-bounty-finder

# Or install manually
cd skills/github-bounty-finder
npm install
```

## Configuration

Create a `.env` file in the skill directory:

```env
GITHUB_TOKEN=your_github_personal_access_token
ALGORA_API_KEY=your_algora_api_key
```

### Getting API Keys

1. **GitHub Token**: 
   - Go to GitHub Settings → Developer settings → Personal access tokens
   - Create a token with `public_repo` scope

2. **Algora API Key**:
   - Visit https://algora.io/settings/api
   - Generate a new API key

## Usage

### Basic Scan

```bash
github-bounty-finder scan
```

### Advanced Options

```bash
# Custom search query
github-bounty-finder scan --query "bug bounty"

# Set minimum bounty amount
github-bounty-finder scan --min-bounty 500

# Limit competition (max comments)
github-bounty-finder scan --max-competition 3

# GitHub only
github-bounty-finder scan --github-only

# Save results to file
github-bounty-finder scan --output results.json
```

### Demo Mode

```bash
github-bounty-finder demo
```

### Check Configuration

```bash
github-bounty-finder config
```

## Output Format

The scanner returns structured data:

```json
{
  "bounties": [
    {
      "id": 123,
      "title": "Fix memory leak",
      "url": "https://github.com/...",
      "bountyAmount": 1500,
      "comments": 0,
      "score": 95,
      "competitionLevel": "None",
      "recommendedAction": "🔥 HIGH PRIORITY - Apply immediately"
    }
  ],
  "totalFound": 25,
  "highPriority": 5,
  "goodOpportunities": 12,
  "pricingRecommendation": {
    "recommendedPrice": 149,
    "currency": "USD",
    "billingCycle": "monthly"
  }
}
```

## Opportunity Scoring Algorithm

Scores are calculated based on:

- **Bounty Value (0-30 points)**: Higher bounties score better
  - $1000+: +30 points
  - $500+: +20 points
  - $200+: +10 points

- **Competition Level (0-40 points)**: Less competition is better
  - 0 comments: +40 points
  - 1-2 comments: +30 points
  - 3-5 comments: +20 points
  - 6-10 comments: +10 points

- **Freshness (0-20 points)**: Newer is better
  - ≤3 days: +20 points
  - ≤7 days: +15 points
  - ≤14 days: +10 points
  - ≤30 days: +5 points

## Pricing Strategy

**Recommended Price: $149/month**

Justification:
- Average bounty value: $500-2000
- Time saved: 10-20 hours/week on manual searching
- ROI: One successful bounty covers 3-6 months subscription
- Target market: Professional developers, bounty hunters, OSS contributors

**Expected Revenue: $3,000-8,000/month**
- Conservative: 20 subscribers × $149 = $2,980/month
- Target: 50 subscribers × $149 = $7,450/month
- Optimistic: 100 subscribers × $149 = $14,900/month

## Integration Examples

### Node.js

```javascript
const BountyScanner = require('github-bounty-finder');

const scanner = new BountyScanner({
  minBounty: 200,
  maxCompetition: 5
});

const results = await scanner.scan({
  github: true,
  algora: true,
  limit: 100
});

console.log(`Found ${results.highPriority} high-priority bounties!`);
```

### CLI Automation

```bash
# Daily scan with cron
0 9 * * * github-bounty-finder scan --min-bounty 500 --output /path/to/results.json
```

## Troubleshooting

### API Rate Limits

If you hit GitHub API rate limits:
- Use authenticated requests (set GITHUB_TOKEN)
- Reduce scan frequency
- Increase delay between requests

### No Results Found

- Lower your `--min-bounty` threshold
- Increase `--max-competition` limit
- Try different search queries

## License

MIT

## Support

For issues and feature requests, visit the GitHub repository.

---

**Made with 🐉 by OpenClaw Skills**
