## Description:

Lattice (lattice.com). Use this skill for ANY Lattice request — searching and reading data. Whenever a task involves Lattice, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Teams using Lattice can ask an agent to look up users, departments, goals, and tags through their connected Lattice account. The skill retrieves records to support workplace tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup fallback runs downloaded CLI installation code without verification or a separate approval step.

Mitigation: Review and approve the CLI installation separately, prefer a fixed release with verified integrity, and grant only the Lattice permissions needed for the task.

## Reference(s):

- [Lattice](https://lattice.com)
- [Lattice API authentication documentation](https://developers.lattice.com/docs/authentication-1)
- [oo CLI source repository](https://github.com/oomol-lab/oo-cli)
- [Lattice skill release on ClawHub](https://clawhub.ai/oomol/skills/oo-lattice)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Natural-language responses with structured Lattice data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the connected account's Lattice access and the requested read action.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
