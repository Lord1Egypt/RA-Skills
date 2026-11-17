## Description:

Collects public Xiaohongshu note, comment, and creator-post data through Guaikei APIs for trend analysis, competitor monitoring, KOL screening, and report preparation without account login or content publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, content teams, marketers, and analysts use this skill to search Xiaohongshu keywords, retrieve note details and comments, and monitor public creator posts for downstream analysis and reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Xiaohongshu query inputs, URLs, and the Guaikei API token are sent to www.guaikei.com.

Mitigation: Use the skill only when that third-party data processing is acceptable, scope token access where possible, and rotate GUAIKEI_API_TOKEN if exposure is suspected.

Risk: Collected profile, comment, and URL-token data may be saved locally in plaintext logs.

Mitigation: Treat generated logs as sensitive, avoid syncing or committing the logs directory, and delete or protect stored outputs after use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-xhs-collector)
- [Guaikei API and token service](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance]

**Output Format:** [Markdown guidance with CLI commands and structured JSON results from invoked scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN; task results may be written to local logs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
