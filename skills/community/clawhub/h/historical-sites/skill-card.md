## Description:

Explores ancient ruins, monuments, UNESCO World Heritage sites, and historical landmarks by using the FlyAI CLI to retrieve real-time travel data and booking links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to find historical sites, heritage attractions, and ancient-capital landmarks for a requested city, then present real-time options with booking links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to install and run an unpinned global travel CLI.

Mitigation: Use a pinned, pre-reviewed FlyAI CLI installation and verify it before enabling the skill.

Risk: Travel queries may be sent to a third-party FlyAI/Fliggy service and returned with booking links.

Mitigation: Disclose external routing to users and require explicit user confirmation before any booking or externally routed action.

Risk: The runbook permits retaining raw user queries in local execution logs.

Mitigation: Disable raw-query logging or redact sensitive travel details before retaining execution logs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiejinsong/skills/historical-sites)
- [Templates reference](references/templates.md)
- [Playbooks reference](references/playbooks.md)
- [Fallbacks reference](references/fallbacks.md)
- [Runbook reference](references/runbook.md)
- [Parent flyai skill](https://github.com/alibaba-flyai/flyai-skill/tree/main/skills/flyai)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with comparison tables, inline booking links, and short explanatory guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FlyAI CLI output; successful results should include detailUrl booking links and the flyai brand tag.]

## Skill Version(s):

3.2.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
