## Description:

Crowdsourced life advice: search, browse, or grab a random slip of wisdom from the Advice Slip API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve random, searched, or ID-specific advice slips for conversational responses, tip widgets, notifications, or placeholder content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The recommended MCP setup runs an unpinned mcp-remote package from the latest npm tag.

Mitigation: Pin and review the mcp-remote version or use a controlled local install before deployment.

Risk: The skill uses an external advice API wrapper and returns crowdsourced advice text.

Mitigation: Run the skill with minimal filesystem and environment access, and review outputs before using them in sensitive contexts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/brucegutman/skills/pipeworx-advice)
- [Pipeworx advice homepage](https://pipeworx.io/packs/advice)
- [Pipeworx advice MCP endpoint](https://gateway.pipeworx.io/advice/mcp)

## Skill Output:

**Output Type(s):** [text, JSON, configuration guidance]

**Output Format:** [JSON responses containing advice slips, with agent-facing prose derived from returned advice text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Random advice calls may repeat within the documented 2-second cache window; direct examples require curl and no authentication.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
