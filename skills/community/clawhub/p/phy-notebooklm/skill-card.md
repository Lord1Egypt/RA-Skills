## Description:

This skill queries Google NotebookLM notebooks from Claude Code to produce source-grounded, citation-backed answers using Gemini, with browser automation, library management, and persistent authentication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Claude Code users use this skill to authenticate to NotebookLM, manage notebook entries, ask questions against uploaded sources, upload selected local files, and synthesize NotebookLM answers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores Google NotebookLM browser session data locally.

Mitigation: Use it only where local session storage is acceptable, and clear authentication or run the documented cleanup command when finished.

Risk: The skill can upload selected local files or directories to Google NotebookLM.

Mitigation: Confirm exact files or directories before upload and use dry-run mode before performing uploads.

Risk: Security evidence reports inconsistent privacy and persistence guidance.

Mitigation: Review the skill's documented storage behavior and deployment expectations before enabling it for users.

## Reference(s):

- [Canlah AI](https://canlah.ai)
- [Phy Notebooklm on ClawHub](https://clawhub.ai/phy041/skills/phy-notebooklm)
- [phy041 ClawHub Profile](https://clawhub.ai/user/phy041)
- [Google NotebookLM](https://notebooklm.google.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with inline shell commands and NotebookLM answer synthesis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require browser authentication, persistent local session data, and user confirmation before file uploads.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
