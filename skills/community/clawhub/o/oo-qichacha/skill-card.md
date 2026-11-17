## Description:

Qichacha (openapi.qcc.com). Use this skill for ANY Qichacha request — searching and reading data. Whenever a task involves Qichacha, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use the skill to retrieve Qichacha company shareholder and subscribed contribution details, and historical outbound investment and exit information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback setup runs a downloaded CLI installer without verification or a clear approval step.

Mitigation: Review and approve CLI installation separately, and prefer a pinned, verified installer.

Risk: Using the connector requires connected-account access and may incur service charges.

Mitigation: Review the connected account access and possible charges before using the connector.

## Reference(s):

- [Qichacha OpenAPI](https://openapi.qcc.com/)
- [Qichacha API documentation](https://openapi.qcc.com/dataApi)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON]

**Output Format:** [JSON connector payloads and responses, with inline Bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Connector responses may include execution metadata.]

## Skill Version(s):

1.0.4 (source: server-resolved release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
