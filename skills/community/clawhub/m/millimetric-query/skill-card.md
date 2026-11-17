## Description:

Query Millimetric analytics - top sources, aggregate stats, raw events, and the Facebook social-vs-paid split.

This skill is ready for commercial/non-commercial use.

## Publisher:

[soybelli](https://clawhub.ai/user/soybelli)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and analytics users use this skill to generate read-only curl and jq workflows for querying Millimetric traffic sources, aggregate metrics, and raw event data from the command line.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Raw event and per-user analytics queries can expose sensitive behavioral data.

Mitigation: Use the skill only with authorization for the Millimetric workspace, prefer aggregate reports when possible, and avoid sharing outputs that include user identifiers or activity timelines.

Risk: A read key grants access to Millimetric analytics data for the associated workspace.

Mitigation: Keep MILLIMETRIC_RK in the local environment, do not paste it into shared outputs, and rotate it if exposure is suspected.

## Reference(s):

- [Millimetric API](https://api.millimetric.ai)
- [ClawHub Skill Page](https://clawhub.ai/soybelli/skills/millimetric-query)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces read-only analytics query recipes that require MILLIMETRIC_RK, curl, and jq.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
