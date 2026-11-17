## Description:

Use this skill for RenderForm requests such as searching and reading data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and RenderForm users can use the skill to search and read templates, usage, and generated results through their connected RenderForm account. They can also request image or PDF renders and website screenshots.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create potentially billable renders or website screenshots even though its summary frames RenderForm work as searching and reading data.

Mitigation: Require confirmation of each render or screenshot request, its payload, and possible credit costs before execution.

Risk: The CLI installation and hosted connector implementation are not verified, and the CLI documentation describes startup synchronization that can change installed agent skills.

Mitigation: Review and verify the CLI installation separately; check the CLI controls documentation and use OO_SKILLS_SYNC_DISABLED to disable startup synchronization when appropriate.

## Reference(s):

- [RenderForm](https://renderform.io)
- [RenderForm API documentation](https://renderform.io/docs/api/get-started)
- [oo CLI command documentation](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown instructions with inline Bash commands and JSON request and response data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action-dependent RenderForm data, request identifiers, and file URLs for rendered images, PDFs, or screenshots.]

## Skill Version(s):

1.0.5 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
