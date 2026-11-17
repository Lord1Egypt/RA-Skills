## Description:

Performs advanced Google searches with Playwright for OpenClaw technical resources, summarizes the top results, and prepares the summary for Telegram delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sonpham1909](https://clawhub.ai/user/sonpham1909)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical users can use this skill to search for OpenClaw-related documentation, repositories, and usage guides, then receive concise Markdown summaries through a Telegram workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow executes a local Python script with user-provided search keywords.

Mitigation: Audit and control the referenced bot.py file, restrict who can modify it, and pass arguments without shell interpretation.

Risk: The workflow depends on browser automation, dependency installation, and Telegram credentials.

Mitigation: Pin and install dependencies safely, run Playwright setup intentionally, and configure Telegram destinations and credentials through a secure mechanism.

Risk: Automated Google searching and Telegram delivery can violate service rules or expose unintended recipients if configured incorrectly.

Mitigation: Confirm compliance with applicable terms and local requirements, and explicitly verify the Telegram channel or user ID before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sonpham1909/skills/google-research-pro)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summary with structured search-result content and Telegram delivery status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local Python search script, Playwright browser setup, and Telegram destination and credential configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
