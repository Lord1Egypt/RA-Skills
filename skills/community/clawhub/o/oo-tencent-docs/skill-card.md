## Description:

Tencent Docs (docs.qq.com). Use this skill for ANY Tencent Docs request — reading, creating, and updating data. Whenever a task involves Tencent Docs, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People managing Tencent Docs use this skill to find and read documents, spreadsheets, and folders, or to create and update documents and forms through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may run downloaded CLI software without a separate approval step, and the external installer behavior is unverified.

Mitigation: Review setup before enabling the skill, install a reviewed and integrity-verified CLI version yourself, and check its agent-skill installation settings.

Risk: Document requests use the permissions of the connected Tencent Docs account.

Mitigation: Check the connected account's access and confirm the intended document and effect before creating or changing content.

## Reference(s):

- [Tencent Docs](https://docs.qq.com)
- [Tencent Docs API documentation](https://docs.qq.com/open/document/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Text responses and Tencent Docs documents or spreadsheets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include retrieved document content or requested document changes.]

## Skill Version(s):

1.0.4 (source: artifact/SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
