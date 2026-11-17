## Description:

Shorten.REST (shorten.rest). Use this skill for any Shorten.REST request, including reading, creating, updating, and deleting data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to manage Shorten.REST aliases and retrieve alias or click data through their connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute downloaded CLI code, and the installed CLI may synchronize changes into other agents’ skill directories.

Mitigation: Review and install a fixed CLI release; set OO_SKILLS_SYNC_DISABLED=1 to prevent startup synchronization, and inspect any resulting changes.

Risk: Shorten.REST requests are handled through OOMOL and may be processed by that service.

Mitigation: Confirm OOMOL may process the requests before connecting the service.

Risk: Creating, updating, and deleting aliases change user data.

Mitigation: Keep the skill’s approval requirements for write and destructive actions; confirm the exact payload and target before execution.

## Reference(s):

- [Shorten.REST API documentation](https://docs.shorten.rest/)
- [Shorten.REST](https://shorten.rest)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Shorten.REST on ClawHub](https://clawhub.ai/oomol/skills/oo-shorten-rest)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action responses depend on the selected Shorten.REST operation.]

## Skill Version(s):

1.0.5 (source: server-resolved release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
