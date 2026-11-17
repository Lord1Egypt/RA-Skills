## Description:

Use this skill to query your Google NotebookLM notebooks directly from Claude Code for source-grounded, citation-backed answers from Gemini.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guccidgi](https://clawhub.ai/user/guccidgi)

### License/Terms of Use:


## Use Case:

Developers and local Claude Code users use this skill to ask questions against their Google NotebookLM notebooks, manage notebook links, and synthesize document-grounded answers into their coding or research workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores Google browser session data and NotebookLM library metadata locally.

Mitigation: Use a dedicated Google account when possible, keep the skill directory private, and avoid storing it in synced or shared folders.

Risk: The skill automates a local browser session with a Google account.

Mitigation: Install only if local browser automation is acceptable, authenticate manually in a visible browser, and verify NotebookLM URLs before use.

Risk: Cleanup and remove commands can delete local authentication, browser state, or notebook library data.

Mitigation: Review cleanup previews, back up important notebook metadata, and use preserve-library options when retaining notebook records matters.

Risk: The skill gives the agent broad browser and command behavior.

Mitigation: Review commands before execution and use the skill in a local Claude Code environment where its browser and file behavior are expected.

## Reference(s):

- [NotebookLM Skill Page](https://clawhub.ai/guccidgi/skills/notebooklm-skill)
- [Authentication Architecture](AUTHENTICATION.md)
- [NotebookLM Skill API Reference](references/api_reference.md)
- [NotebookLM Skill Troubleshooting Guide](references/troubleshooting.md)
- [NotebookLM Skill Usage Patterns](references/usage_patterns.md)
- [Google NotebookLM](https://notebooklm.google/)
- [Playwright Session Cookie Persistence Issue](https://github.com/microsoft/playwright/issues/36139)
- [Playwright Persistent Context Storage State Issue](https://github.com/microsoft/playwright/issues/14949)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include NotebookLM-sourced answers, citations, follow-up questions, local setup commands, and notebook management guidance.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
