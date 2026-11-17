## Description:

Fetch and analyze OpenRank and other statistical metrics for an open source repository or developer using OpenDigger data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunny0826](https://clawhub.ai/user/sunny0826)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and open source program teams use this skill to inspect repository or developer health, influence, activity, and contributor metrics from OpenDigger data. It supports latest summaries, trend descriptions, and period-specific metric tables for GitHub or Gitee targets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may make network requests to OpenDigger's public OSS data host for repository or developer names the user provides.

Mitigation: Use it for public OSS identifiers and avoid submitting private or sensitive repository or developer names.

Risk: A requested metric or period may be missing from the OpenDigger data files.

Mitigation: Report missing values explicitly as '-' or 'N/A' and keep the requested period visible in the response.

## Reference(s):

- [ClawHub OpenRank skill page](https://clawhub.ai/sunny0826/skills/openrank)
- [OpenDigger OSS data example](https://oss.open-digger.cn/github/X-lab2017/open-digger/openrank.json)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown summaries and tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responds in the user's language and may mark unavailable metric values as '-' or 'N/A'.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
