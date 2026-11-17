## Description:

NavClaw helps agents plan driving routes with Amap by comparing many routing strategies, generating congestion-avoidance candidates, and returning mobile navigation links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ai4mse](https://clawhub.ai/user/ai4mse)

### License/Terms of Use:

MIT-0

## Use Case:

Drivers and agent users use NavClaw to request route planning between an origin and destination, compare Amap route candidates, and receive recommended routes with iOS and Android navigation links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Amap receives route queries that may include sensitive origin and destination details.

Mitigation: Tell users before route lookup, send only the needed trip details, and avoid using the skill for sensitive locations unless the user accepts Amap processing.

Risk: The skill asks agents to reuse stored API keys and chat credentials.

Mitigation: Do not search general memory for secrets; store keys in a proper secret manager or environment variables and write only explicit user-provided values into local configuration.

Risk: Configured Mattermost posting can share detailed route summaries and logs to a channel without a strong per-run consent boundary.

Mitigation: Prefer local-only execution with --no-send, require user confirmation before enabling posting, and verify the Mattermost URL is HTTPS and trusted.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ai4mse/skills/navclaw)
- [Amap Open Platform](https://lbs.amap.com/)
- [Amap Geocode API](https://restapi.amap.com/v3/geocode/geo)
- [Amap Driving Route API](https://restapi.amap.com/v5/direction/driving)
- [Technical Documentation](docs/technical_EN.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and plain-text route summaries with navigation links, optional logs, and setup commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call Amap APIs and, when configured, post route summaries and logs to Mattermost.]

## Skill Version(s):

1.0.3 (source: evidence release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
