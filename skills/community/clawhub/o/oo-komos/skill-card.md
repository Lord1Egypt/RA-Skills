## Description:

Komos (komos.ai). Use this skill for ANY Komos request — reading, creating, updating, and deleting data. Whenever a task involves Komos, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use Komos through their connected OOMOL account to inspect saved tasks and task runs, review execution logs, queue task runs, and request cancellation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Initial setup may run an unverified remote CLI installer.

Mitigation: Review and approve CLI installation separately, and connect only the intended Komos account.

## Reference(s):

- [Komos API documentation](https://docs.komos.ai/api-reference/introduction)
- [Komos homepage](https://komos.ai/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-komos)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [CLI commands with JSON payloads and JSON connector responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results vary by Komos action and may include task data, run status, execution logs, or action confirmation details.]

## Skill Version(s):

1.0.1 (source: frontmatter, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
