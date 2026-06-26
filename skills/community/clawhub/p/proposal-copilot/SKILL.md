---
name: proposal-copilot
description: Generate Upwork/freelance bid materials from a job description, including English proposal draft, bid-worthiness score, pricing suggestion (fixed/hourly), milestone split, and D+1/D+3/D+7 follow-up messages. Use when user asks to write proposals, decide whether to bid, estimate rates, or prepare follow-up outreach.
---

# Proposal Copilot (MVP)

Read the user input and produce structured output for freelance bidding.

## Commands

- `proposal 帮助`: Show command usage
- `proposal 生成 <JD文本>`: Generate full proposal package (score + proposal + pricing + followups)
- `proposal 生成 <concise|professional|sales> <JD文本>`: Generate proposal in selected style (paid)
- `proposal 生成 预览 <concise|professional|sales> <JD文本>`: Free preview (first lines)
- `proposal 评分 <JD文本>`: Only return bid-worthiness score + reasons
- `proposal 报价 <JD文本> <fixed|hourly> [min] [max]`: Return pricing suggestion (paid)
- `proposal 跟进 <客户名> <岗位简述>`: Return D+1/D+3/D+7 follow-up copies (paid)

## Output Rules

Always return concise, copy-paste ready text.

For `proposal 生成`, return JSON with keys:
- `score` (0-100)
- `decision` (`BID|MAYBE|SKIP`)
- `summary` (one-line 投标建议结论)
- `reasons` (array)
- `proposal_en`
- `pricing`
- `milestones`
- `followups`

## Pricing Rules (MVP)

- If JD is clear + budget reasonable + skill match high: higher recommendation.
- If scope is vague: conservative pricing and add clarification questions.
- For hourly mode, return `recommended_rate`, `alt_rate_low`, `alt_rate_high`.
- For fixed mode, return 3 milestone split.

## Score Rubric (100)

- Budget match: 30
- Requirement clarity: 20
- Skill fit: 25
- Client quality signals: 15
- Delivery feasibility: 10

Decision threshold:
- `>=70`: BID
- `50-69`: MAYBE
- `<50`: SKIP

## Billing

This skill must charge `0.001 USDT` per paid generation call via SkillPay billing API.
If insufficient balance, return payment link.

## Notes

MVP focuses on speed and practical output. Do not over-explain.
