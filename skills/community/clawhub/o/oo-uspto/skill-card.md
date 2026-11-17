## Description:

Use this skill to search and read USPTO trademark records through a connected OOMOL account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents can retrieve USPTO trademark case status, latest recorded update dates, and associated document metadata. The skill uses the user's connected OOMOL account to run read-only USPTO actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup directs the agent to run downloaded CLI software that has not been independently verified.

Mitigation: Review and approve CLI installation separately, preferably using a pinned release with verified integrity.

Risk: USPTO requests pass through OOMOL, require a connected API key, and may incur charges.

Mitigation: Review the OOMOL connection and billing terms before connecting the API key.

## Reference(s):

- [USPTO skill release](https://clawhub.ai/oomol/skills/oo-uspto)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [USPTO](https://www.uspto.gov/)
- [Trademark Enterprise API User Guide](https://www.uspto.gov/sites/default/files/documents/tm-enterprise-api-user-guide-v2.pdf)

## Skill Output:

**Output Type(s):** [JSON, XML, Guidance]

**Output Format:** [USPTO record data in JSON or XML, with concise guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only trademark records; case status is returned as XML.]

## Skill Version(s):

1.0.5 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
