---
name: meetmatch_sales_coach
description: "AI sales coach that sends personalized morning briefings, tracks rep patterns over time, and uses MeetMatch's ML predictions to make your agent smarter about sales outcomes."
metadata:
  openclaw:
    requires:
      env:
        - MEETMATCH_API_KEY
        - MEETMATCH_ORG_ID
      config:
        - briefing_hour
        - delivery_method
    os: []
---

# MeetMatch Sales Coach

Your OpenClaw agent knows how to write emails and search the web. This skill teaches it how to actually sell.

MeetMatch Sales Coach connects your agent to real sales outcome data: which reps close which types of deals, who's at risk of a no-show, what coaching patterns emerge across hundreds of calls. Your agent doesn't just read a CRM. It taps into a prediction engine trained on your team's historical close data, then turns that into personalized coaching for every rep, every morning.

The result: your OpenClaw agent becomes the most prepared person on your sales team.

## What your agent gets access to

**Meeting schedules with risk scores.** Not just "you have a 2pm call." Your agent sees that the 2pm has a 73% no-show probability and the prospect came from a paid ad campaign with historically low attendance. It can warn the rep, suggest a confirmation sequence, or flag the meeting for overbooking.

**ML-powered routing context.** MeetMatch doesn't use round-robin. It uses machine learning trained on historical close data to match each prospect with the rep most likely to convert them. Your agent can surface why a specific meeting was routed to a specific rep ("You close 3x more deals in healthcare than the team average"), giving the rep genuine confidence before the call.

**Persistent rep memory.** After every call, MeetMatch generates coaching analysis. This skill accumulates those observations into a memory that follows each rep across weeks and months. If a rep keeps losing deals during the pricing conversation, your agent notices and brings it up before their next call where pricing matters.

**Performance data.** Close rates, no-show rates, streak data, trend lines. Not vanity metrics. The numbers your agent needs to write a morning briefing that actually means something.

## Morning Briefing

Every morning at a configurable hour, this skill generates a personalized briefing for each rep. The briefing includes:

- Today's meetings with prospect context and risk flags
- One focused coaching nudge based on the rep's long-term patterns
- Prep tips specific to each meeting (not generic advice, actual observations from prior calls with similar prospects)
- A performance snapshot showing close rate trend and team comparison

Briefings are sent via email by default. Your agent can also generate on-demand briefings when a rep asks.

## Memory that gets smarter

The coaching memory isn't static. After every call:

1. MeetMatch runs transcript analysis and generates a coaching scorecard
2. This skill compares the new data against the rep's existing memory
3. Patterns get reinforced, outdated observations get retired, milestones get recorded
4. The next briefing incorporates everything

A rep who used to struggle with objection handling but improved over the last month? The memory tracks that progression. The briefing stops nagging about it and shifts focus to the next area.

## Setup

1. Sign up at [meetmatch.ai](https://www.meetmatch.ai) and enable the Pro plan (morning briefings included)
2. Go to Settings > Integrations and generate an OpenClaw API key
3. Configure this skill:

```yaml
# ~/.openclaw/skills/meetmatch-sales-coach/config.yaml
meetmatch_api_key: "mm_live_..."
meetmatch_org_id: "your-org-uuid"
briefing_hour: 7          # Local time (uses each rep's timezone)
delivery_method: "email"   # email (default)
```

## Commands

Your agent responds to natural language:

- "How's Marcus doing this week?" — pulls memory and recent stats for a specific rep
- "What should I focus on in my next call?" — surfaces coaching nudges from accumulated memory
- "Show me my morning briefing" — generates a briefing on demand
- "What patterns have you noticed about my calls?" — lists active memory entries
- "Brief me on my 2pm" — pulls prospect context and risk assessment for a specific meeting

## API Endpoints

All requests need `Authorization: Bearer {MEETMATCH_API_KEY}` and `org_id` as a query param.

| Endpoint | What it returns |
|---|---|
| `GET /api/openclaw/briefing?member_id={id}` | Full morning briefing data (schedule + memory + stats) |
| `GET /api/openclaw/memory?member_id={id}` | Rep's accumulated AI memory entries |
| `GET /api/openclaw/stats?member_id={id}&days=30` | Performance stats with daily breakdown |
| `GET /api/openclaw/schedule?member_id={id}&date=YYYY-MM-DD` | Day's meetings with prospect details and risk scores |

## Why this matters for your agent

Most AI agents in sales are glorified search tools. They can pull CRM data and summarize emails. This skill gives your agent access to something different: prediction data from ML models trained on actual sales outcomes.

When your agent tells a rep "this meeting was routed to you because your close rate on enterprise healthcare deals is 3x the team average," that's not a compliment. That's a data point from a gradient-boosted model trained on your org's history. When it flags a meeting as high no-show risk, that's a prediction from a model that's seen thousands of similar booking patterns.

The more calls your team takes through MeetMatch, the better the predictions get, and the smarter your agent becomes.

## Pricing

MeetMatch morning briefings and the OpenClaw API are included in the Pro plan ($50/seat/mo). The skill itself is free to install.

## Links

- [MeetMatch](https://www.meetmatch.ai)
- [OpenClaw Integration Guide](https://www.meetmatch.ai/integrations/openclaw)
- [Interactive Demo](https://www.meetmatch.ai/demo/clawcon)
- [Support](mailto:support@meetmatch.ai)
