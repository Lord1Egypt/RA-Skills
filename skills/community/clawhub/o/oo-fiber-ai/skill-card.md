## Description:

Fiber AI (fiber.ai). Use this skill for ANY Fiber AI request — searching and reading data. Whenever a task involves Fiber AI, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other Fiber AI users use this skill to retrieve organization credit and rate-limit information and to look up enum or reference values through their connected Fiber AI account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute downloaded CLI software that was not verified by the security review.

Mitigation: Review and verify the CLI installation separately before running it.

Risk: Automatic synchronization can introduce persistent agent skills without clear user approval.

Mitigation: Review the proposed skill changes and use OO_SKILLS_SYNC_DISABLED to opt out of synchronization when appropriate.

## Reference(s):

- [Fiber AI](https://fiber.ai)
- [Fiber AI API documentation](https://api.fiber.ai/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [Structured connector results and concise usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the connected Fiber AI account and selected read action.]

## Skill Version(s):

1.0.5 (source: release metadata, frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
