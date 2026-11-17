## Description:

Talenox (talenox.com). Use this skill for ANY Talenox request — searching and reading data. Whenever a task involves Talenox, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

HR teams and administrators use the skill to retrieve employee, branch, company settings, and working time records from a connected Talenox account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup executes unverified remote code without a clear user approval step.

Mitigation: Review and approve CLI installation separately; prefer a verified, fixed release and review automatic skill synchronization settings.

Risk: Connecting Talenox allows OOMOL to handle credentials and sensitive employee data.

Mitigation: Review the connection and authorize access only for the intended Talenox account and data.

## Reference(s):

- [Talenox](https://www.talenox.com/)
- [Talenox API documentation](https://talenox.github.io/api-doc/index.html)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Talenox on ClawHub](https://clawhub.ai/oomol/skills/oo-talenox)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [Structured Talenox API response data with concise usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Retrieves records and settings from the connected Talenox account.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
