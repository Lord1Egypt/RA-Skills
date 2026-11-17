## Description:

Add new language translations to customer service response templates and sync the update across Feishu Wiki, GitHub, and local files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, documentation maintainers, and customer support operations teams use this skill to add multilingual response-template translations, sync the updated content to Feishu Wiki, create a GitHub tracking issue, and commit the local template change.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Feishu sync script can send credentials and selected file contents to a configurable external API URL.

Mitigation: Use only in trusted workspaces, keep Feishu credentials least-privilege, and confirm FEISHU_BASE_URL is unset or points to the official Feishu API before running sync commands.

Risk: The workflow can publish or track customer-service template changes in external systems.

Mitigation: Confirm the exact template file, Feishu Wiki node, and GitHub repository before running sync or issue-creation commands.

## Reference(s):

- [Language Style Guide](references/language-style-guide.md)
- [ClawHub Skill Page](https://clawhub.ai/terrycarter1985/skills/multilingual-template-sync)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and file-change instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local Markdown templates, Feishu Wiki documents, GitHub issues, and Git commits when the user executes the described workflow.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
