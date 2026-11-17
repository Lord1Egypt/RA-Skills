## Description:

Analyzes carrier logistics index data from Excel or CSV files to report a carrier's score, industry average, ranking, trend, contributing sub-metric, and operational recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[a-vb](https://clawhub.ai/user/a-vb)

### License/Terms of Use:

MIT-0

## Use Case:

Operations teams and carrier analysts use this skill to query carrier logistics index scores for a specified date, compare them with the industry average, inspect recent score trends, and identify the largest contributing sub-metric.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Plaintext HTTP portal links may expose sensitive carrier or operational data in transit.

Mitigation: Prefer verified HTTPS access where available, confirm the destination before downloading anomaly details, and avoid sending sensitive operational data over plaintext HTTP.

Risk: Local spreadsheet inputs may contain sensitive carrier or operational data.

Mitigation: Install and run the skill only when the agent is intended to read the specific spreadsheet supplied by the user.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/a-vb/skills/indexquery)
- [Jingwe/JDL index direction portal](http://jingwe.jdl.com/#/indexCenter/indexDirection)
- [Jingwe/JDL shipper overview portal](http://jingwe.jdl.com/#/indexCenter/shipperOverview)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown narrative with carrier metrics, trend summary, impact metric, recommendations, and anomaly-detail notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads user-provided .xlsx or .csv carrier index data and may reference Jingwe/JDL portal pages for metric composition and anomaly details.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
