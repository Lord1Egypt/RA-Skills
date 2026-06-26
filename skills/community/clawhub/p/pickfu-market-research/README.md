# PickFu Market Research

PickFu delivers real human feedback in minutes — not simulated responses. This skill gives your AI agent the ability to run end-to-end consumer research studies: from research brief to survey design to published poll to structured analysis report, all without leaving your agent session.

## Quick start

Invoke directly:

```
/pickfu-market-research
```

Or describe your research need — the agent will invoke the skill automatically:

- "Which of these two logos do pet owners prefer?"
- "Test these three product names with US women aged 25-34"
- "Get feedback on this landing page design from Amazon Prime members"
- "Run a pricing study comparing $9.99, $14.99, and $19.99 tiers"

> **Note**: Publishing a survey charges your PickFu account balance. The agent will show you the survey design and ask for confirmation before anything is charged. See [pickfu.com/pricing](https://www.pickfu.com/pricing) for rates.

## What is PickFu?

[PickFu](https://www.pickfu.com) is a consumer research platform with ~15 million respondents. Ask targeted audiences to compare options, rate concepts, give written feedback, and more — without recruiting participants or managing panels.

## What does this skill do?

1. **Research brief** — Captures your research objective, target audience, and hypotheses
2. **Survey design** — Proposes question types, options, targeting, and sample size
3. **Create & publish** — Creates the survey and publishes (with your confirmation)
4. **Wait for results** — Monitors until all responses are collected
5. **Analyze & report** — Delivers a structured report with executive summary, per-question breakdown, verbatim quotes, demographic analysis, and next steps

## Use cases

- **A/B testing** — logos, packaging, product images, app icons, thumbnails
- **Product naming** — test product names, brand names, taglines, slogans
- **Book publishing** — book titles, cover designs, back cover copy, series branding
- **Marketing creatives** — ad copy, social media posts, email subject lines, banner ads, video thumbnails
- **UX/UI design** — landing pages, onboarding flows, navigation layouts, feature mockups, wireframes
- **Concept validation** — new product ideas, feature concepts, business models
- **Pricing research** — price sensitivity, price point testing, tier comparisons, willingness to pay
- **Amazon seller optimization** — listing images, titles, bullet points, A+ content with Prime member feedback
- **Brand perception** — competitive comparisons, brand trust, visual identity, tone of voice
- **Content testing** — headlines, blog titles, video concepts, podcast names, course descriptions

## Supported question types

| Type | Description |
|------|-------------|
| Head-to-head | A/B comparison — respondents pick a favorite and explain |
| Ranked | Rank 3-8 options in preference order |
| Open-ended | Free-form written feedback on a concept |
| Single select | Pick one from multiple options with explanation |
| Multi select | Select multiple answers from options |
| Emoji rating | Emoji sentiment + explanation |
| Star rating | 1-5 stars with written feedback |
| Click test | Heatmap of where users click on an image |
| Five second test | First impressions after brief timed exposure |
| Screen recording | Records user interaction with content |

## Supported countries

US (United States), CA (Canada), AU (Australia), DE (Germany), GB (United Kingdom), JP (Japan), MX (Mexico), ES (Spain), FR (France), IT (Italy), KR (South Korea), BR (Brazil), ZA (South Africa), PL (Poland)

## Setup

The skill works with two interfaces (auto-detected):

### Option A: PickFu MCP Server (recommended)

If you have the [PickFu MCP server](https://www.pickfu.com) configured in your OpenClaw instance, the skill will use it automatically. No additional setup needed.

### Option B: PickFu CLI

Visit [agents.pickfu.com](https://agents.pickfu.com) for install options, or use npx (zero-install, requires Node.js 20+):

```bash
npx --yes @pickfu/cli@latest auth login
```

For headless environments, use `npx --yes @pickfu/cli@latest auth login --headless`.

You can also authenticate with an API key:

```bash
export PICKFU_API_KEY=your_api_key
```

Get an API key at [app.pickfu.com/settings/api-keys](https://app.pickfu.com/settings/api-keys).

## Example output

```markdown
## Research Report

### Executive Summary
Logo A was the clear winner, preferred by 68% of respondents (34/50).
Respondents cited its "clean, modern feel" and "better color palette" as key factors.
Recommend proceeding with Logo A for the brand launch.

### Q1: Which logo do you prefer for a pet food brand? (head_to_head)
**Winner**: Option A (68% vs 32%)
**AI Summary**: Logo A resonated strongly across demographics...

**Notable Quotes**:
> "Logo A feels premium and trustworthy — I'd pick this off the shelf." — Female, 30
> "B looks too busy. A is cleaner and more memorable." — Male, 28

### Demographic Breakdown
| Segment | Logo A | Logo B |
|---------|--------|--------|
| Male    | 64%    | 36%    |
| Female  | 72%    | 28%    |

### Next Steps
- Proceed with Logo A for brand launch
- Consider a follow-up test with different color variations
```

## Templates

Pre-built survey templates in `examples/` — each file is a valid survey payload, directly usable with `npx --yes @pickfu/cli@latest survey create --from-file`:

- `ab-logo-test.json` — A/B logo comparison with demographic reporting
- `product-name-test.json` — Rank multiple product name candidates
- `concept-validation.json` — Five-second test + star rating + purchase intent
- `amazon-listing-comparison.json` — Compare Amazon listings by ASIN (Prime members)
- `pricing-study.json` — Price sensitivity with multiple price points

## Links

- [PickFu website](https://www.pickfu.com)
- [PickFu CLI & Agents](https://agents.pickfu.com)
- [PickFu Docs](https://www.pickfu.com/docs)
- [PickFu Help](https://www.pickfu.com/help)
- [API Keys](https://app.pickfu.com/settings/api-keys)
- [Pricing](https://www.pickfu.com/pricing)
