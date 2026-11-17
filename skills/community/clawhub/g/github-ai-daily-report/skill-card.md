## Description:

Daily AI digest skill that fetches trending GitHub AI/LLM/agent projects and Hacker News discussions, formats a structured report with value analysis, sends it to a user via Feishu, and prepends it to a Feishu document.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ssyvonne](https://clawhub.ai/user/ssyvonne)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate a daily AI trend digest, deliver it through Feishu, and maintain a newest-first Feishu document archive with optional backlog entries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated report content can be written to unintended Feishu users or documents if destination identifiers are configured incorrectly.

Mitigation: Verify the Feishu open_id and document tokens before use, and enable the optional backlog token only when project-tracking entries should be written outside the daily archive.

Risk: Daily trend reports depend on public search results and may include outdated, low-signal, or misleading project descriptions.

Mitigation: Review the generated report before acting on recommendations or adding projects to a backlog.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ssyvonne/skills/github-ai-daily-report)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report with concise completion summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Report content is delivered to a configured Feishu user and prepended to a configured Feishu document when the required tokens are available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
