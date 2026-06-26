# Influencer Partnership Scout

## Overview

Influencer Partnership Scout helps SMB e-commerce brands shortlist likely creator fits, choose partnership modes, and draft outreach logic. This MVP is descriptive only, with no real creator API access.

## Trigger

Use this skill when the user wants to:
- find likely creator archetypes for a campaign
- compare influencer fit for awareness, UGC, affiliate, or conversion goals
- decide between gifting, affiliate, paid post, or ambassador strategy
- generate an outreach shortlist and contact brief

### Example prompts
- "Help me shortlist creators for my skincare brand"
- "Should we use micro influencers or larger creators?"
- "Give me outreach strategy for a pet accessory launch"
- "Rank influencer fit for UGC + conversion"

## Workflow

1. Capture brand brief and campaign goal.
2. Infer creator fit, audience fit, and content compatibility.
3. Recommend partnership mode and shortlist tiers.
4. Generate outreach and risk notes in markdown.

## Inputs
- brand name or category
- market / region
- product price range
- campaign goal: awareness / UGC / affiliate / conversion
- preferred platform and follower range
- optional candidate handles or niche keywords

## Outputs
- influencer shortlist framework
- partnership fit analysis
- recommended partnership mode
- contact brief and outreach angle

## Safety
- No live social platform data
- No guarantee of creator pricing, reply rate, or conversion
- Final brand-safety review should be done by a human

## Acceptance Criteria
- Must return markdown
- Must include shortlist tiers
- Must include fit analysis and risk notes
- Must include outreach recommendation and contact brief
