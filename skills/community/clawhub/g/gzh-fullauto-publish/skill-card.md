## Description:

Helps WeChat Official Account creators draft and format articles, generate covers, save drafts through a local authenticated session, and verify the saved result.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lingyu9495-source](https://clawhub.ai/user/lingyu9495-source)

### License/Terms of Use:

MIT-0

## Use Case:

WeChat Official Account creators use this skill to prepare a formatted article and cover images, save them to their own account's drafts, and check the draft before publishing it manually.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated browser sessions and account-accessing requests can affect the user's WeChat account.

Mitigation: Review the skill before use and run it with a dedicated account and browser profile where possible.

Risk: Session tokens could be exposed through shared profiles, logs, or screenshots.

Mitigation: Keep the browser profile outside Git, cloud, and shared folders; do not share logs or screenshots containing tokens.

Risk: Draft changes or deletion commands could remove content, and generated articles may need editorial review.

Mitigation: Review deletion commands before running them and manually inspect the saved draft before public posting.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/lingyu9495-source/skills/gzh-fullauto-publish)
- [Quick start](artifact/README-快速开始.md)
- [Writing and compliance guidelines](artifact/references/02-写作与合规红线.md)
- [Login and draft workflow](artifact/references/05-登录与入稿通道.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, HTML, Shell commands, Guidance]

**Output Format:** [Article copy and formatted HTML, cover-image instructions, summaries, and local draft/verification commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local scripts can generate cover images and save a draft to the user's WeChat Official Account; public posting remains manual.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
