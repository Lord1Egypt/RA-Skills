## Description:

This skill helps agents collect public Xiaohongshu content evidence for topic research, high-performing notes, comments, competitor style, and creator activity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

External users, content teams, marketing analysts, and agents use this skill to retrieve Xiaohongshu public-content data for creator research, trend monitoring, competitor analysis, KOL review, and comment analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends a private API token and Xiaohongshu keywords, profile URLs, or note URLs to a third-party service.

Mitigation: Install only if Guaikei is trusted for those inputs, avoid sensitive business targets unless that transfer is approved, and rotate the token if logs or traces may have been shared.

Risk: Command runs may automatically save full result data locally under logs/.

Mitigation: Protect the workspace, restrict access to generated logs, and delete logs after use when results include sensitive research targets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-xhs-kol-check)
- [Publisher profile](https://clawhub.ai/user/engheng-art)
- [Guaikei API token and support](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON command output with optional Markdown summaries and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN; command runs may save full results under logs/.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata reports 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
