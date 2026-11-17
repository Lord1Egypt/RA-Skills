## Description:

小红书精选 helps agents retrieve public Xiaohongshu notes, note details, comments, and creator post lists as structured data for trend research, competitor analysis, KOL screening, and content planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, content teams, marketers, and analysts use this skill to search Xiaohongshu public content, inspect note details and comments, and monitor public creator posts. The retrieved structured data supports content research, market trend analysis, competitor monitoring, and KOL evaluation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries, Xiaohongshu links, returned public content, and GUAIKEI_API_TOKEN are sent to the third-party guaikei.com service.

Mitigation: Use only when that data sharing is acceptable, scope inputs to public content, and rotate the API token if logs, traces, or diagnostics may have exposed it.

Risk: Command results are saved under logs/ and may contain sensitive research records or API-derived public content.

Mitigation: Treat generated logs as sensitive working files, avoid committing or sharing them, and delete them when no longer needed.

Risk: The skill is limited to public Xiaohongshu data and does not support private, hidden, login-only, publishing, liking, commenting, or following actions.

Mitigation: Use the skill only for public-data lookup workflows and request a valid keyword, note URL, or creator profile URL before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-xhs-pick)
- [Guaikei service site](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance]

**Output Format:** [Markdown guidance with inline shell commands; command execution returns structured JSON and may save JSON logs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14.0+ and GUAIKEI_API_TOKEN; outputs include status, request metadata, execution metadata, and results or error details.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata reports 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
