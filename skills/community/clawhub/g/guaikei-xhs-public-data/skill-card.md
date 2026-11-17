## Description:

Provides structured Xiaohongshu public-data lookup for popular post discovery, competitor monitoring, KOL screening, and comment insight workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, content operators, marketers, and analysts use this skill to retrieve structured Xiaohongshu public post, profile, and comment data for content planning, competitive review, KOL screening, and reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The GUAIKEI_API_TOKEN may be exposed in shared shells, logs, or process output.

Mitigation: Use a scoped token, avoid echoing the token in logged environments, and rotate the token if it may have been exposed.

Risk: Xiaohongshu keywords, note URLs, profile URLs, and returned results are sent through a third-party API workflow.

Mitigation: Use only public data, avoid sensitive internal queries, and confirm the third-party service terms and retention posture before production use.

Risk: A paid or broadly privileged Guaikei token could incur quota or account impact if misused.

Mitigation: Limit token permissions where possible, monitor usage, and run the skill only in trusted environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-xhs-public-data)
- [Guaikei service site](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and structured JSON results from the invoked Node.js scripts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and GUAIKEI_API_TOKEN; commands may save result logs under the skill's logs directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
