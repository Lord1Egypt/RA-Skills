## Description:

Audits dependency supply chains for bad versions, lockfile drift, and artifact integrity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to audit Python project dependencies against known-bad versions, inspect lockfile and artifact integrity, and guide response to suspected supply-chain compromises.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A full environment snapshot written to a plaintext temporary file could expose credentials.

Mitigation: Avoid dumping the full environment; capture only necessary values, redact secrets, restrict file permissions, and limit retention.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/athola/skills/nm-leyline-supply-chain-advisory)
- [Metadata homepage](https://github.com/athola/claude-night-market/tree/master/plugins/leyline)

## Skill Output:

**Output Type(s):** [Analysis, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands and Python code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.10.4 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
