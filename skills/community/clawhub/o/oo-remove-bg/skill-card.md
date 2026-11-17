## Description:

remove.bg (remove.bg). Use this skill for ANY remove.bg request — reading, creating, updating, and deleting data. Whenever a task involves remove.bg, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other oo CLI users can manage a connected remove.bg account by checking credits, removing image backgrounds, and optionally submitting source images to the improvement program.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup runs an unverified remote installer, and the installer payload remains unverified.

Mitigation: Review and install the oo CLI separately before using this skill.

Risk: The CLI can make broader changes to agent skills through automatic synchronization.

Mitigation: Decide whether to allow automatic skill synchronization before enabling it.

Risk: Images are processed through OOMOL/remove.bg and connector storage; improvement submissions contribute the source image for model improvement.

Mitigation: Approve improvement submissions only when you intend to contribute the source image.

## Reference(s):

- [oo CLI documentation and source](https://github.com/oomol-lab/oo-cli)
- [remove.bg](https://www.remove.bg)
- [remove.bg API documentation](https://www.remove.bg/api)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON payload examples; generated image or ZIP results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Background removal returns a generated image or ZIP result; account queries return credit and free-call information.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
