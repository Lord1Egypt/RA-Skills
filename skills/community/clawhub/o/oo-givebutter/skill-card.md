## Description:

Givebutter (givebutter.com). Use this skill for ANY Givebutter request — searching and reading data. Whenever a task involves Givebutter, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can retrieve Givebutter campaigns, chapters, contacts, funds, recurring plans, and transactions through an OOMOL-connected account. The agent uses the returned records to answer search and read requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute unverified remote code without a clear approval step.

Mitigation: Review and approve CLI installation separately using a verified, fixed release; consider disabling automatic skill synchronization.

Risk: Connecting Givebutter entrusts OOMOL with access to contact and transaction data.

Mitigation: Connect only an account whose data access is appropriate for this use, and review the permissions granted to the connection.

## Reference(s):

- [Givebutter API authentication documentation](https://docs.givebutter.com/api-reference/authentication)
- [Givebutter](https://givebutter.com)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [JSON records interpreted and summarized in text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only Givebutter records from get and list actions.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
