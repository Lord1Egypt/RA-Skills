## Description:

Use an OOMOL-connected account to inspect HoneyHive action schemas and read, create, update, or delete datasets and datapoint associations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data teams use this skill to inspect HoneyHive action schemas and manage datasets and their datapoints through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute downloaded CLI installer code whose contents have not been verified.

Mitigation: Review and separately approve installation, verify the CLI version, and inspect its effects on installed agent skills.

Risk: OOMOL mediates HoneyHive access and receives action payloads; credential-handling details remain unverified.

Mitigation: Avoid including sensitive data in payloads unless OOMOL's handling is approved for that data.

Risk: Dataset write and deletion actions can change or remove data.

Mitigation: Confirm the exact payload and effect before writes, and get explicit approval before destructive actions.

## Reference(s):

- [HoneyHive API documentation](https://docs.honeyhive.ai/)
- [HoneyHive homepage](https://www.honeyhive.ai/)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [Shell commands with JSON payloads and JSON action responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Write and destructive actions require user approval; the action schema is checked before payload construction.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
