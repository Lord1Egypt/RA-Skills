## Description:

This skill helps agents retrieve public XiaoHongShu note search results, note details, comments, and creator posts for trend research, competitor analysis, KOL screening, and comment insights.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users and teams use this skill to collect public XiaoHongShu content data through Guaikei API commands, then analyze topics, competitors, creators, and comments. It is intended for public-content research workflows and does not support login, posting, liking, or private-content access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, target profiles, comments, XiaoHongShu URLs, and retrieved results may be sensitive.

Mitigation: Review inputs before use, treat generated logs as sensitive, and delete or protect logs after the task is complete.

Risk: The skill requires a Guaikei API token and sends requests to the third-party Guaikei service.

Mitigation: Use a dedicated low-privilege token, avoid printing or sharing the token, and rotate it if exposure is suspected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-xhs-comments)
- [Publisher profile](https://clawhub.ai/user/engheng-art)
- [Guaikei API token and support site](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [JSON command output with optional Markdown summaries and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN and may write retrieved results to local logs.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata reports 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
