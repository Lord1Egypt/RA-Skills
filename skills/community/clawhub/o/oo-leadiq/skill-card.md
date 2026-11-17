## Description:

LeadIQ (leadiq.com). Use this skill for ANY LeadIQ request — searching and reading data. Whenever a task involves LeadIQ, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Sales, recruiting, and business development teams can use the skill to search LeadIQ for people and companies, retrieve person details, and check account and credit information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute unverified downloaded code and may make changes to other agents' skills without clear user control.

Mitigation: Review and approve CLI installation separately, prefer a verified release, and consider the documented OO_SKILLS_SYNC_DISABLED control.

Risk: Using the integration entrusts LeadIQ access and query data to OOMOL.

Mitigation: Use the integration only for LeadIQ access and queries that are approved for sharing with OOMOL.

## Reference(s):

- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [LeadIQ homepage](https://leadiq.com)
- [LeadIQ Public API Guide](https://leadiqhelp.zendesk.com/hc/en-us/articles/29375289152795-LeadIQ-Public-API-Guide)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [LeadIQ search, enrichment, and account data returned as JSON and summarized in text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fields vary by action and are determined by the connector schema.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
