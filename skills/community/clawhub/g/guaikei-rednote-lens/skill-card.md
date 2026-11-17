## Description:

红笔记数据透镜 helps agents retrieve structured public Xiaohongshu/RedNote data for keyword search, note details, comments, and creator post monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

Content creators, marketers, analysts, and operations teams use this skill to collect public Xiaohongshu/RedNote content data for topic research, competitor monitoring, KOL screening, trend tracking, and comment analysis. It is not intended for publishing, account interaction, private content, or hidden content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the Guaikei API token, Xiaohongshu links, keywords, and requested limits to Guaikei.

Mitigation: Use the skill only when that data sharing is acceptable, keep the token scoped to this service, and rotate the token if exposure is suspected.

Risk: Retrieved content and URLs may be saved automatically under logs/ in the workspace.

Mitigation: Run the skill in a private workspace and delete saved result files when they are no longer needed.

Risk: The skill is intended for public Xiaohongshu/RedNote data and may be misused if applied to private, hidden, or unauthorized data collection tasks.

Mitigation: Confirm the task is limited to public data and decline requests for private, hidden, login-only, publishing, or interaction workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-rednote-lens)
- [Publisher profile](https://clawhub.ai/user/engheng-art)
- [Guaikei API token and support](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; command results are structured JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14.0+ and GUAIKEI_API_TOKEN; commands may save retrieved content and URLs under logs/.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact source metadata reports 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
