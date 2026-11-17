## Description:

AI marketing agent and AI ad generator for your agent. Research winning ads, generate on-brand image and video ads, publish, schedule and run ad campaigns. No markup on models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hermoso-dev](https://clawhub.ai/user/hermoso-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing teams and agents use Hermoso to research competitor ads, create branded image and video ads, publish or schedule content on connected channels, and build or review ad campaigns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connected accounts and the agent key can enable publishing or campaign actions.

Mitigation: Connect only intended accounts and protect the agent key.

Risk: Renders consume credits, and live campaigns can spend ad budget.

Mitigation: Quote render costs and set spending and publishing limits; keep campaigns paused unless the user explicitly asks to activate them.

Risk: The local stdio setup runs an npm package, and this review does not cover the external service implementation.

Mitigation: Prefer the HTTP connection or pin a reviewed package version.

## Reference(s):

- [Hermoso MCP](https://hermoso.ai/mcp/)
- [Hermoso ClawHub release](https://clawhub.ai/hermoso-dev/skills/hermoso)

## Skill Output:

**Output Type(s):** [Guidance, API calls, Images and videos, Social posts and campaign data]

**Output Format:** [Text, image and video files, and social platform content or campaign records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated media may take several minutes; quote render credits before rendering. Campaigns are created paused, and activation requires explicit confirmation.]

## Skill Version(s):

1.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
