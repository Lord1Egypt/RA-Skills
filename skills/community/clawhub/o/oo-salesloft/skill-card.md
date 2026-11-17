## Description:

Connects to Salesloft through the oo CLI to search and read Salesloft data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Salesloft users and developers use this skill to retrieve account, person, cadence, and current-user data through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback setup runs downloaded installer code, while the installers and server-side implementation were not verified.

Mitigation: Review the CLI and installer before installation, and check the CLI's automatic agent-skill synchronization settings.

Risk: Connecting Salesloft entrusts OOMOL with access to business records.

Mitigation: Review the connection settings and account access before connecting Salesloft.

## Reference(s):

- [Salesloft](https://www.salesloft.com/)
- [Salesloft API request and response documentation](https://developers.salesloft.com/docs/platform/api-basics/request-response-format/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API data, JSON]

**Output Format:** [JSON responses containing Salesloft data and execution metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses include data and a meta.executionId value.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
