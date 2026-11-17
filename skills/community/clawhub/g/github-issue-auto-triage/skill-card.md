## Description:

Automatically triages GitHub issues with AI-assisted labeling, duplicate detection, owner assignment guidance, and FAQ replies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sxliuyu](https://clawhub.ai/user/sxliuyu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and maintainers use this skill to review newly opened GitHub issues, suggest classifications, identify likely duplicates, and apply configured triage actions. It is intended for repository issue-management workflows where automated labels, comments, and reports are useful after credential and data-sharing review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change GitHub issues by adding labels and comments when dry-run is disabled.

Mitigation: Start with dry-run, review the proposed labels and comments, and run with the narrowest GitHub token permissions available for the target repository.

Risk: Issue titles and bodies may be sent to DashScope for LLM classification.

Mitigation: Confirm that project policy allows this data sharing before enabling DashScope credentials; note that dry-run still contacts the LLM provider when configured.

Risk: Unattended scheduled execution could repeatedly apply unwanted triage actions.

Mitigation: Avoid cron or systemd deployment until repository owners have reviewed token scopes, labels, comments, and operating mode.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sxliuyu/skills/github-issue-auto-triage)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON configuration examples; runtime execution can write JSON triage reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GitHub repository settings and credentials; optional DashScope credentials enable LLM-assisted classification.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter; artifact changelog and ClawHub config contain conflicting 2.0.0 signals)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
