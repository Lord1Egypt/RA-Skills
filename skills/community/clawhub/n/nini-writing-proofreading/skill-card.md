## Description:

Use when user wants to review, polish, or proofread articles. Triggers include「帮我改文章」「检查一下」「润色」「帮我改改」「校对一下」「看看文章」.

This skill is ready for commercial/non-commercial use.

## Publisher:

[niracler](https://clawhub.ai/user/niracler)

### License/Terms of Use:


## Use Case:

Writers and editors use this skill to review Chinese Markdown articles through a structured six-step proofreading workflow covering organization, reader context, language clarity, source verification, personal style, and Markdown formatting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional Markdown autofix command may change article formatting in ways the writer did not intend.

Mitigation: Run the lint check first, review any proposed or generated diff, and accept fixes only after user confirmation.

Risk: The external setup command can retrieve code outside this release artifact.

Mitigation: Inspect the external package or use a pinned, lockfile-managed version before running setup commands.

Risk: Proofreading suggestions and source-verification guidance can still introduce incorrect wording or weak citations.

Mitigation: Discuss each source-backed change with the user, prefer authoritative sources, and keep detailed claims in footnotes.

## Reference(s):

- [Writing Proofreading on ClawHub](https://clawhub.ai/niracler/skills/nini-writing-proofreading)
- [中文写作规范](references/chinese-style.md)
- [结构诊断与读者 Context 检查](references/structure-review.md)
- [信源查证与脚注规范](references/source-verification.md)
- [个人风格指南](references/personal-style.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown prose with checklists, editing suggestions, source notes, and optional shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The workflow asks the agent to review one or two Markdown sections at a time and wait for user confirmation before making changes.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
