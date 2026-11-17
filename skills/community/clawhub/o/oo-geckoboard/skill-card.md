## Description:

Geckoboard (geckoboard.com). Use this skill for ANY Geckoboard request — reading, creating, updating, and deleting data. Whenever a task involves Geckoboard, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to inspect Geckoboard action schemas and operate datasets through an OOMOL-connected account. Dataset creation, updates, replacement, and deletion require approval as specified by the skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup directs the agent to run remote installer code without a separate approval step.

Mitigation: Install a verified oo CLI release yourself and prevent automatic download-and-execute setup.

Risk: Dataset writes, replacement, and deletion can change or remove data.

Mitigation: Keep the skill's explicit approval checks and confirm the exact target and effect before these actions.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI command controls](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [Geckoboard](https://www.geckoboard.com/)
- [Geckoboard API documentation](https://developer.geckoboard.com/)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Shell commands, JSON payloads, and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [State-changing actions require user approval; destructive actions require approval of the target and effect.]

## Skill Version(s):

1.0.5 (source: frontmatter and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
