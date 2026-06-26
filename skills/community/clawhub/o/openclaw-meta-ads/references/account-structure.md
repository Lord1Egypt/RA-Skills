# Account Structure

## Core hierarchy

Meta Ads usually works like this:

1. Ad Account
2. Campaign
3. Ad Set
4. Ad
5. Creative

## What each layer usually controls

### Ad Account
- overall billing and access context
- top-level reporting
- account-wide lists of campaigns, ad sets, ads, creatives, and forms

### Campaign
- objective
- top-level budget in some setups
- broad directional strategy

### Ad Set
- audience
- placements
- optimization goal
- schedule
- budget in many setups

### Ad
- final delivery object
- creative attachment
- copy and call to action

### Creative
- image, video, text, headline, destination, CTA

### Insights
- performance metrics at account, campaign, ad set, or ad level
- common fields: spend, impressions, clicks, ctr, cpc, cpm, reach, frequency, actions, cost_per_action_type

### Lead Forms and Leads
- instant forms can generate leads directly in Meta
- lead data is often sensitive and may also sync downstream into systems like HubSpot

## Common confusion points

- campaign objective does not tell the whole optimization story
- ad set choices often drive audience and delivery more than campaign labels do
- good CTR does not guarantee good lead quality
- lead count does not guarantee pipeline value
- attribution and reporting windows can distort apparent winners and losers
