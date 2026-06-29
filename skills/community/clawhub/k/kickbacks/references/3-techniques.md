# Techniques — Advertising on Kickbacks

> Source: kickbacks.ai product documentation and ad submission form

## How to Advertise

Kickbacks' ad marketplace is live and open. Any advertiser can bid.

### Ad Submission Form Fields

| Field | Required | Rules |
|---|---|---|
| Email | ✅ | Required for account linking and notifications |
| Ad line | ✅ | 3–60 characters. The text shown in the spinner. |
| Destination URL | ✅ | https:// — where clicks go |
| Brand name | Optional | Shown on the public leaderboard |
| Brand icon | Optional | PNG/JPG/WebP ≤ 64 KB |
| Show on leaderboard | Optional (checkbox) | Public visibility toggle |
| Bid per block | ✅ | Minimum $1.00. Sets queue priority. |
| Number of blocks | ✅ | 1+ blocks. 1 block = 1,000 views. |

### Bidding Strategy

```
Bid queue (simplified):
#1: $5.00/block — Campaign A — gets all impressions first
#2: $3.00/block — Campaign B — gets impressions when A isn't serving
#3: $1.00/block — Campaign C — gets what's left
```

**Key rules:**
- Highest bid serves first. You outbid the top to take #1, or queue up behind.
- A higher bid doesn't add more views — it moves your ad up in priority.
- More blocks = more total views. Each block is 1,000 impressions.
- Clicks are billed at 50× the impression rate automatically.

### Example Bid

```
Ad line: "Ramp · save time and money"
URL: https://ramp.com
Bid: $5.00/block
Blocks: 5
Total: $25.00 for 5,000 impressions
```

### Campaign Management

- **Impressions feed** — The bid market page shows real-time impression counts across the fleet.
- **Status** — Each campaign shows live status (active, queued, completed).
- **24h history** — You can view the last 24 hours of ad activity.
- **All-time stats** — Lifetime impression and click data available.

> **Case: Campaign Lifecycle** (Product): An advertiser submits a $5.00 bid for 3 blocks. The bid enters the queue. If no higher bids exist, the ad goes live within seconds. Over the next few hours, 3,000 impressions are delivered. When the blocks are exhausted, the campaign ends and the advertiser can renew.

## Market Data Available

The bid market page shows:
- **Bid per 1,000 impressions** — Current market rate
- **Live impressions/min** — How fast ads are being served across the fleet
- **Active campaigns** — How many campaigns are currently live
- **Campaign history** — Past campaigns, bids, and impression counts
- **Leaderboard** — Top brands by total impressions
