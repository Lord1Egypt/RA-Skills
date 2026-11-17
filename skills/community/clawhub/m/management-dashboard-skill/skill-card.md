## Description:

Generates a manager-facing daily HTML dashboard from AI summaries of meeting or field recordings, including team assets, field efficiency, compliance monitoring, RM rankings, lead conversion, and management advice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[legionspace-hackathon](https://clawhub.ai/user/legionspace-hackathon)

### License/Terms of Use:

MIT-0

## Use Case:

Managers and operations teams use this skill to turn recording-derived AI summaries into a daily management dashboard. The report supports review of team activity, compliance signals, individual RM performance, lead quality, and follow-up priorities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive recording-derived business data and sends summaries into LLM analysis and generated HTML reports.

Mitigation: Deploy only in a controlled environment and document retention and protection for recording summaries, LLM prompts, and generated reports.

Risk: The artifact defaults the recording API base URL to HTTP and a private network address.

Mitigation: Force HTTPS for the recording API and restrict allowed API hosts and paths before deployment.

Risk: Dashboard HTML is assembled from analysis fields and report content.

Mitigation: Escape or template all report output before writing HTML reports.

Risk: Generated reports load Chart.js from a public CDN.

Mitigation: Bundle Chart.js or use integrity-pinned assets from an approved source.

Risk: Pagination can continue until the recording service reports completion.

Mitigation: Bound pagination and request time windows to limit runtime and data volume.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/legionspace-hackathon/skills/management-dashboard-skill)
- [artifact/README.md](artifact/README.md)
- [artifact/SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated HTML report file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces responsive HTML dashboard reports saved under the skill's reports directory; empty recording data still produces a zero-metric HTML report.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
