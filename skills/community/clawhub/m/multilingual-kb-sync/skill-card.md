## Description:

Adds new language translations to customer service response templates and syncs updates across local files, Feishu Wiki, and GitHub issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Customer support, localization, and documentation teams use this skill to add reviewed language blocks to knowledge-base templates, publish them to Feishu Wiki, and document the update in GitHub.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scripts can publish local files to Feishu Wiki or GitHub without strong scoping or confirmation.

Mitigation: Review inputs before execution, restrict use to intended kb-templates files and approved repositories or wiki spaces, and preview content before publishing.

Risk: The workflow requires Feishu and GitHub credentials.

Mitigation: Use least-privileged credentials and avoid running the workflow in shared or logged environments until credential handling is improved.

## Reference(s):

- [Feishu Wiki API Reference](references/feishu-wiki-api.md)
- [GitHub Issue Template for KB Template Updates](references/github-issue-template.md)
- [Feishu Wiki create node API](https://open.feishu.cn/document/server-docs/docs/wiki-v2/space-node/create)
- [Feishu Docx create block API](https://open.feishu.cn/document/server-docs/docs/docs/docx-v1/document-block/create)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated GitHub issue text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May publish provided markdown content to Feishu Wiki and create GitHub issues when run with credentials.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
