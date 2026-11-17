## Description:

Generate slides, audio overviews, and documents from sources using Google NotebookLM via browser automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aoaibiz](https://clawhub.ai/user/aoaibiz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to automate Google NotebookLM content generation from text, URLs, and files, including slides, audio overviews, reports, quizzes, mind maps, and shareable notebook links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can operate a NotebookLM tab in a logged-in Chrome session.

Mitigation: Enable the browser relay only for the specific tab you intend to automate and keep unrelated sensitive content out of browser snapshots and screenshots.

Risk: The setup workflow can expose the local gateway token in terminal output.

Mitigation: Do not paste or share terminal output containing gateway tokens, and rotate the gateway token if it may have been exposed.

## Reference(s):

- [Chrome Relay Setup Guide](references/chrome-relay-setup.md)
- [Google NotebookLM](https://notebooklm.google.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash code blocks and generated NotebookLM links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an active OpenClaw Browser Relay connection to a logged-in Chrome session.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
