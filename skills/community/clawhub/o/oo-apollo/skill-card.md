## Description:

Apollo. Use this skill for ANY Apollo request — searching and reading data. Whenever a task involves Apollo, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using Apollo can search for people and organizations, enrich person or organization records, and check API usage through their OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI setup may execute downloaded code and make persistent changes to other agents’ skills.

Mitigation: Review and approve CLI installation separately; consider setting OO_SKILLS_SYNC_DISABLED=1 before using it.

Risk: Apollo requests through the connected account may consume credits.

Mitigation: Check the connected account and OOMOL credit status before running actions.

## Reference(s):

- [Apollo API documentation](https://docs.apollo.io/reference/authentication)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)
- [Connect Apollo in OOMOL](https://console.oomol.com/connections/apollo)
- [OOMOL billing and token recharge](https://console.oomol.com/billing/token-recharge)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [Structured JSON responses with text summaries or guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Apollo actions may return account and prospecting data; API calls may consume credits.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
