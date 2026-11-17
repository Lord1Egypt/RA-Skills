## Description:

Connect to Qdrant Cloud to list collections, inspect and search points, create collections, and insert or replace points.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data engineers use this skill to manage Qdrant Cloud collections and points, search vector data, and follow approval checks for changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI installation and automatic agent-skill synchronization involve software and skill changes that have not been verified.

Mitigation: Review installation separately, use a fixed release with verified integrity, and check or disable automatic skill synchronization before use.

Risk: Qdrant credentials and state-changing actions can expose or alter account data.

Mitigation: Use narrowly scoped credentials and retain approval checks, confirming the target and exact payload before writes or overwrites.

## Reference(s):

- [Qdrant Cloud](https://qdrant.tech/cloud/)
- [Qdrant API documentation](https://api.qdrant.tech/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, JSON, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action inputs follow the live connector schema; state-changing actions require approval.]

## Skill Version(s):

1.0.5 (source: server-resolved release, frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
