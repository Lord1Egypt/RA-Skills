## Description:

Searches public Xiaohongshu posts by keyword and retrieves note details, comments, creator posts, author information, engagement metrics, summaries, and direct links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External content creators, brand marketers, market analysts, and agent operators use this skill to collect public Xiaohongshu data for topic research, trend tracking, comment analysis, creator monitoring, and competitive review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports that the API token is sent in URL query strings, which can expose paid tokens through request logs, proxies, or shared traces.

Mitigation: Review before installing with real API tokens, prefer a version that sends the token in an Authorization header, scope token use to this workflow, and rotate the token if exposure is suspected.

Risk: The security evidence reports that collected results are automatically stored locally in plaintext logs.

Mitigation: Run the skill in a controlled workspace, avoid collecting data that should not be retained, and redact or delete logs after use; prefer a version that supports disabling logs.

Risk: The security guidance calls out token fields and xsec_token values as data that should be redacted.

Mitigation: Do not share raw command output or log files externally until token-like fields and Xiaohongshu xsec_token values have been removed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-xhs-viral-mining)
- [Guaikei API access](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; CLI commands return JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN; command results may be saved locally under logs/.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter and package metadata report 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
