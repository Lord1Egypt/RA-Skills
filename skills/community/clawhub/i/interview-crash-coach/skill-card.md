## Description:

Prepares company- and role-specific interview briefs, practice questions, truthful answer frameworks, and optional mock-interview feedback without requiring a resume.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bowen-aijishu](https://clawhub.ai/user/bowen-aijishu)

### License/Terms of Use:

MIT-0

## Use Case:

Job candidates use this skill to research a prospective employer and role, build a focused preparation pack, and optionally practice interview answers one question at a time. It requires JishuDB for the preparation records and separate consent to retain personal answers or feedback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled setup can install JishuDB Desktop and change client configuration.

Mitigation: Review the installation plan and configuration changes, and authorize setup only on a trusted machine.

Risk: Interview-preparation records persist in JishuDB, and personal practice could be retained beyond the conversation.

Mitigation: Approve the destination and general records deliberately; separately approve any retention of personal answers or feedback.

Risk: The Windows helper invokes PowerShell to create a launch shortcut despite documentation saying PowerShell is not used.

Mitigation: Review the Windows setup path and shortcut creation before authorizing execution.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/bowen-aijishu/skills/interview-crash-coach)
- [Project homepage (listed in skill metadata)](https://github.com/x-aijishu/jishudb-skills/tree/main/skills/interview-crash-coach)
- [Bundled JishuDB setup quickstart](references/jishudb-setup/references/setup-quickstart.md)

## Skill Output:

**Output Type(s):** [Markdown, Text guidance]

**Output Format:** [Markdown preparation files and conversational practice feedback]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Cites public sources; saves personal answers or feedback only with separate approval.]

## Skill Version(s):

0.1.19 (source: ClawHub release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
