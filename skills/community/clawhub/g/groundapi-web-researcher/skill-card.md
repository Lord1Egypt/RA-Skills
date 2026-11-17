## Description:

Deep web research assistant that searches, scrapes, checks trending topics, retrieves daily briefings, and synthesizes multiple sources into structured reports using GroundAPI MCP tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qingkongzhiqian](https://clawhub.ai/user/qingkongzhiqian)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and other external users use this skill to run GroundAPI-powered web research, compare topics, monitor trends, and produce cited research summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research topics, selected URLs, and trend queries are sent to GroundAPI.

Mitigation: Use the skill only for information that is appropriate to share with GroundAPI and avoid sending sensitive or confidential topics.

Risk: The skill requires a GroundAPI key.

Mitigation: Keep the GroundAPI key private, scoped to the minimum needed access, and rotate it if exposure is suspected.

Risk: Broad trigger wording may invoke the skill for ordinary search or summary requests.

Mitigation: Review whether GroundAPI-assisted research is appropriate before using the skill for routine or sensitive requests.

## Reference(s):

- [GroundAPI homepage](https://groundapi.net)
- [GroundAPI MCP endpoint](https://mcp.groundapi.net/mcp)
- [ClawHub skill page](https://clawhub.ai/qingkongzhiqian/skills/groundapi-web-researcher)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown research reports with source links, summaries, findings, conclusions, and comparison tables when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output language follows the user request; source attribution is expected for synthesized claims.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
