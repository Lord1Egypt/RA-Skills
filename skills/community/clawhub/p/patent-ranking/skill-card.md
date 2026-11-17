## Description:

Builds a patent leaderboard for a selected technology, region, or organization type, ranking valid invention patents, recent filings, and growth with the counting rules stated.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ip930](https://clawhub.ai/user/ip930)

### License/Terms of Use:

MIT-0

## Use Case:

Patent analysts, business teams, and researchers can compare organizations by valid invention grants, recent filing volume, and filing growth for a chosen technology or geography. The skill exports the results with counting rules and a statistics date for reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to PatentMax and may disclose confidential invention details.

Mitigation: Use non-confidential search terms and review query content before sending it to the service.

Risk: API-key handling, authenticated destinations, redirects, or saved-key storage may expose account credentials.

Mitigation: Do not paste keys into chat; use a limited-credit key through the environment, restrict authenticated destinations and redirects, and secure saved-key storage.

Risk: Patent searches and statistics can spend account credit.

Mitigation: Explain the estimated cost and obtain the user's agreement before running paid queries.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/ip930/skills/patent-ranking)
- [PatentMax patent search](https://app.ip930.com/)
- [PatentMax API platform](https://api.ip930.com)

## Skill Output:

**Output Type(s):** [Files, Text]

**Output Format:** [UTF-8 CSV with BOM plus a concise conversational summary.]

**Output Parameters:** [A ranked table with organization, valid invention count, recent and prior-period application counts, growth, and notes; includes scope, counting basis, statistics date, and data source.]

**Other Properties Related to Output:** [Counts are taken from PatentMax query results; the skill documents normalization choices and notes that applicant names are not group-normalized. Statistics return up to 20 entries.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
