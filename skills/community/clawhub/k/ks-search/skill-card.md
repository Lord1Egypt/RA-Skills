## Description:

Searches public Kuaishou videos by keyword and returns video details, engagement metrics, creator information, timestamps, links, and CSV exports for research and monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mystery77777777](https://clawhub.ai/user/mystery77777777)

### License/Terms of Use:

MIT-0

## Use Case:

External users can search public Kuaishou videos for a keyword to support content research, competitor monitoring, creator screening, and category reviews. The skill returns video details and engagement counts, and can export results as CSV.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports suspicious charge approval handling and capabilities beyond the declared Kuaishou search purpose.

Mitigation: Review the keyword, requested count, estimated charge, and settlement terms with the user, and wait for explicit confirmation before submitting a search.

Risk: The default service URL uses HTTP, which can expose the account token in transit.

Mitigation: Use a trusted HTTPS service endpoint with certificate verification enabled before providing account credentials.

Risk: The security scan inspected only part of the release and reports degraded tool-misuse analysis.

Mitigation: Review the skill's behavior and service interactions before providing credentials or running collection tasks; treat unreported behavior as unassessed.

## Reference(s):

- [ClawHub listing](https://clawhub.ai/mystery77777777/skills/ks-search)

## Skill Output:

**Output Type(s):** [JSON, CSV files, Shell commands]

**Output Format:** [JSON search results and CSV exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One keyword per search; requests can ask for 1–500 videos, with actual results depending on availability.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
