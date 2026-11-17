## Description:

Truvera (truvera.io). Use this skill for ANY Truvera request — reading, creating, updating, and deleting data. Whenever a task involves Truvera, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use the skill to read and manage DIDs, credential schemas, profiles, and jobs in a connected Truvera account. State-changing actions require confirmation of the exact payload and effect.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup fallback runs unverified internet code without a separate approval step.

Mitigation: Review the CLI installation source and install the CLI separately before use; do not run the fallback installer automatically.

Risk: Write and deletion actions can change or remove Truvera account data.

Mitigation: Connect only the intended Truvera account and retain confirmation of the exact payload and effect before state-changing actions.

## Reference(s):

- [Truvera API documentation](https://docs.truvera.io/truvera-api/getting-started)
- [Truvera](https://truvera.io)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON API responses and shell commands with Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions cover Truvera DIDs, credential schemas, profiles, and jobs.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
