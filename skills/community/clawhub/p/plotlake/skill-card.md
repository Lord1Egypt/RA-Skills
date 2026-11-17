## Description:

Subscribes to WeChat public accounts and other sources through the Plotlake Open Channel API, then retrieves raw article content for an agent to assemble daily digests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eggyrooch-blip](https://clawhub.ai/user/eggyrooch-blip)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create Plotlake channels, subscribe curated or custom feed sources, fetch raw articles, and have an agent summarize them into daily digests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Feed choices, channel names, and submitted feed or website URLs are sent to Plotlake.

Mitigation: Use the skill only when sharing those values with Plotlake is acceptable, and avoid private intranet, authenticated, staging, or tokenized URLs.

Risk: Example commands can create, subscribe, add, or delete remote channel sources.

Mitigation: Review mutating curl commands before execution and confirm the target channel, source, and bundle identifiers.

## Reference(s):

- [Plotlake ClawHub Skill Page](https://clawhub.ai/eggyrooch-blip/skills/plotlake)
- [Project homepage](https://github.com/eggyrooch-blip/wewerss)
- [Plotlake Open Channel API](https://api.plotlake.com)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with bash and curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses curl and jq; no credential environment variables are documented.]

## Skill Version(s):

1.3.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
