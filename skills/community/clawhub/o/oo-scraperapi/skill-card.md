## Description:

ScraperAPI (scraperapi.com). Use this skill for ANY ScraperAPI request — reading, creating, and updating data. Whenever a task involves ScraperAPI, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to check ScraperAPI account usage, fetch public URLs, and submit POST or PUT requests through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup executes unverified installation scripts and may add agent skills through automatic synchronization.

Mitigation: Review and approve a fixed CLI release before setup, check its skill synchronization settings, and connect only the intended account.

Risk: Requests pass through OOMOL and ScraperAPI and may incur charges.

Mitigation: Review the target URL and action, and check account usage and billing before making requests.

## Reference(s):

- [ScraperAPI API documentation](https://docs.scraperapi.com/synchronous-apis/using-the-api-endpoint)
- [ScraperAPI](https://www.scraperapi.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Text, JSON, Shell commands]

**Output Format:** [JSON responses and oo CLI command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results vary by action; requests may incur charges.]

## Skill Version(s):

1.0.4 (source: SKILL.md frontmatter and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
