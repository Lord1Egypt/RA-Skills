## Description:

Analyze access, JSONL application and GZIP logs for errors, HTTP status, popular routes and time patterns. Use for Log Diagnostics Toolbox.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hznetnewpower](https://clawhub.ai/user/hznetnewpower)

### License/Terms of Use:

MIT No Attribution

## Use Case:

Developers and site reliability engineers use it to inspect selected access and application logs, find error patterns and route or time trends, and produce local reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reports may retain sensitive routes or error messages, and reports plus local state files persist after analysis.

Mitigation: Select only logs intended for analysis, review reports before sharing, and remove reports and local state when no longer needed.

## Reference(s):

- [Action contract](references/input.md)
- [MochiLab](https://mochilab.bz)

## Skill Output:

**Output Type(s):** [Text, JSON, CSV, HTML]

**Output Format:** [Text analysis with JSON, CSV, or HTML report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports are saved locally; source log files are preserved.]

## Skill Version(s):

1.0.1 (source: frontmatter metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
