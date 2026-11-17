## Description:

AI News Digest helps agents generate daily or weekly AI and technology news briefings with structured summaries, topical grouping, optional formats, and email-ready output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunshine-del-ux](https://clawhub.ai/user/sunshine-del-ux)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to produce AI and technology news digests for personal briefings, newsletters, or organization-specific update workflows. The bundled shell behavior currently emits a template digest unless live news, OpenAI, and email integrations are configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional OpenAI and SMTP credentials can be exposed if they are placed in shared shell history, committed files, or broad-scope accounts.

Mitigation: Use scoped or app-specific credentials, keep secrets out of checked-in files and shared command history, and rotate credentials if exposed.

Risk: Automated email delivery can send incomplete or template-only digests if enabled before live news sources and SMTP behavior are reviewed.

Mitigation: Review any cron job before enabling it, test delivery manually, and confirm configured sources produce the expected digest content.

Risk: Generated news summaries may be inaccurate, stale, or incomplete when source feeds, APIs, or summarization settings are not configured or reviewed.

Mitigation: Use trusted news sources, validate important claims before redistribution, and review generated summaries before commercial publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sunshine-del-ux/skills/new-ai-news-digest)
- [ClawHub publisher profile](https://clawhub.ai/user/sunshine-del-ux)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-like text with optional HTML or plain text output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference optional OpenAI API and SMTP environment configuration for smarter summaries and email delivery.]

## Skill Version(s):

1.0.0 (source: release metadata and _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
