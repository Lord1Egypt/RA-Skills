## Description:

Produces Lanxin linkCard JSON for sending link card messages with required title and link fields.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iamdacai](https://clawhub.ai/user/iamdacai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to format Lanxin Blue Message link-card requests as strict JSON for downstream delivery or rendering.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated linkCard JSON may be automatically delivered or rendered without a separate review step.

Mitigation: Require user confirmation before delivery and validate URLs before rendering or sending the link card.

Risk: The artifact tells the agent not to refuse or add warnings when producing link-card JSON.

Mitigation: Allow the agent to refuse, warn, or request clarification for unsafe, misleading, or malformed links.

Risk: The skill is always enabled and uses broad link-related triggers.

Mitigation: Use narrower Lanxin-specific triggers or deployment scoping when installing in shared agent environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/iamdacai/skills/lanxin-link-card)
- [Lanxin official website](https://www.lanxin.cn)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [Raw JSON object without Markdown code fences]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a single linkCard object with title, description, iconLink, link, pcLink, fromName, and fromIconLink fields.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
