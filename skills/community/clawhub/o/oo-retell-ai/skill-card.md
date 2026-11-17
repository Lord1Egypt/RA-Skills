## Description:

Searches and reads Retell AI calls, phone numbers, voice agents, and voices through a connected OOMOL account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External developers use this skill to search and read Retell AI workspace data, including calls, phone numbers, voice agents, and voices, through their connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup directs execution of downloaded installers whose behavior has not been verified.

Mitigation: Require approval before running an installer; use a reviewed, version-pinned oo CLI and check its automatic skill synchronization settings.

Risk: Connecting Retell AI gives OOMOL access to account data.

Mitigation: Review the connection and its access scopes before connecting the account.

## Reference(s):

- [Retell AI API documentation](https://docs.retellai.com/)
- [Retell AI](https://www.retellai.com/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON data with concise explanatory text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only Retell AI lookup results; exact fields depend on the selected action.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
