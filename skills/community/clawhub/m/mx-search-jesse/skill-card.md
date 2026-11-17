## Description:

Mx Search helps agents retrieve timely Eastmoney financial information, including news, announcements, research reports, policy items, trading rules, event context, and impact analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jessecq1995](https://clawhub.ai/user/jessecq1995)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query Eastmoney's financial search API for current market-related information and save both readable text and raw JSON results for follow-up analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial search queries are sent to Eastmoney's external API using the configured MX_APIKEY.

Mitigation: Avoid submitting confidential internal research, account data, or other sensitive financial information in search queries.

Risk: Search results are saved locally as text and JSON files and may contain sensitive query context or retrieved financial information.

Mitigation: Review and periodically remove local mx_search output files when results should not be retained.

## Reference(s):

- [Mx Search ClawHub page](https://clawhub.ai/jessecq1995/skills/mx-search-jesse)
- [Eastmoney financial search API endpoint](https://mkapi2.dfcfs.com/finskillshub/api/claw/news-search)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Plain text, JSON, and terminal output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Saves extracted text and raw JSON search results to local files when run as a command-line helper.]

## Skill Version(s):

1.0.5 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
