## Description:

Use this skill to read, create, and update Coda data through the connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users working with Coda use the skill to inspect docs, pages, tables, columns, and rows, and to create pages or insert and update rows through the connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructions can trigger unverified remote code execution without a separate approval step; installer payloads were unavailable for inspection.

Mitigation: Review the CLI installation first, install a verified version-specific release separately, and approve any additional local changes.

Risk: Connecting Coda entrusts OOMOL with the integration credentials and requested data.

Mitigation: Review the account connection and requested data access before connecting Coda.

Risk: Creating pages and inserting or updating rows change Coda data.

Mitigation: Keep the skill's confirmation requirement for Coda writes and confirm the intended change before execution.

## Reference(s):

- [Coda](https://coda.io)
- [Coda API documentation](https://coda.io/developers/apis/v1)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands depend on the selected Coda action and its current input schema.]

## Skill Version(s):

1.0.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
