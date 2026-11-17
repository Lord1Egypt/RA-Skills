## Description:

Manage ad campaigns across Meta, Google, TikTok, LinkedIn, Reddit, Apple, Bing, ChatGPT, and Snapchat Ads via the hosted LazyAds MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[camerondwills](https://clawhub.ai/user/camerondwills)

### License/Terms of Use:

MIT-0

## Use Case:

External advertisers, marketers, and operators use this skill to let an agent review, create, sync, and adjust campaigns across connected advertising accounts through LazyAds. It supports bridge workflows for manual campaign management and paid-plan workflows for Lazy Ads AI campaign building, creative generation, optimization, and competitor intelligence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent authority to create, launch, pause, resume, and modify live ad campaigns, including budgets, bids, targeting, automation, and creative spend.

Mitigation: Require explicit user confirmation before any mutating or spend-related action, and review proposed campaign, budget, targeting, and launch changes before execution.

Risk: The LazyAds API key grants access to connected advertising accounts through the hosted MCP server.

Mitigation: Store the key only in a private secret location, keep it scoped and revocable, rotate it if exposed, and avoid sending it in prompts or logs.

Risk: Full MCP AI tools can consume monthly AI credits for campaign builds, creative generation, optimization, or competitor intelligence.

Mitigation: Confirm plan level and credit impact before invoking Full MCP AI tools such as build_ai_campaign or generate_creative.

## Reference(s):

- [Server-resolved GitHub repository](https://github.com/camerondwills/lazyads-mcp)
- [ClawHub skill page](https://clawhub.ai/camerondwills/skills/lazyads-mcp)
- [LazyAds MCP tool catalog](https://lazyads.ai/mcp#tools)
- [LazyAds Hermes setup](https://lazyads.ai/hermes)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, guidance]

**Output Format:** [Markdown guidance with MCP tool calls and YAML configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May perform live LazyAds MCP actions when an API key and connected ad accounts are available.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
