## Description:

Automates NotebookLM notebook creation from YouTube videos by researching featured people, adding the video and research as sources, and generating an Audio Overview.

This skill is ready for commercial/non-commercial use.

## Publisher:

[x-rayluan](https://clawhub.ai/user/x-rayluan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn YouTube interviews, talks, and documentaries into NotebookLM notebooks with background research and an Audio Overview.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent controls Chrome while the user is logged into Google and NotebookLM.

Mitigation: Use a dedicated browser profile or account and review each browser action before allowing it to proceed.

Risk: The workflow sends YouTube URLs, research text, and generated notebook content to third-party services.

Mitigation: Avoid confidential, regulated, private, or copyrighted material unless the user has permission and accepts the data sharing.

Risk: NotebookLM has multiple similar text inputs, so automation can target the wrong field.

Mitigation: Follow the artifact's screenshot-first workflow and verify the modal, selector, and button state before each action.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/x-rayluan/skills/notebooklm-youtube-skill)
- [NotebookLM UI Quick Reference](references/notebooklm_ui_guide.md)
- [NotebookLM](https://notebooklm.google.com/)
- [Claude Skill Documentation](https://support.claude.com/en/articles/12512180-using-skills-in-claude)

## Skill Output:

**Output Type(s):** [Guidance, Text, Markdown, Code]

**Output Format:** [Markdown guidance with inline JavaScript snippets and browser automation steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates account-linked NotebookLM notebooks and Audio Overviews through Chrome using the user's logged-in session.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
