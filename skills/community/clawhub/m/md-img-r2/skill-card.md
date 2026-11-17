## Description:

Markdown Images to R2 helps agents inspect local Markdown image references, create dry-run publishing plans, and, after explicit confirmation, upload or rewrite those references for Cloudflare R2 or S3-compatible public URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangchao228](https://clawhub.ai/user/yangchao228)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, publishing operators, and content creators use this skill to prepare Markdown files with local images for public distribution. It supports plan-first review, confirmed R2 or S3-compatible uploads, and reviewed URL-map rewrites before downstream publishing approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private images, sensitive local paths, or credentials could be exposed if the skill is used on unreviewed content or with overly broad storage credentials.

Mitigation: Review the generated plan first, avoid private images, use least-privilege R2 credentials, and confirm that reports do not contain access-key or secret-key values.

Risk: Markdown could be rewritten with incorrect or unacceptable public URLs.

Mitigation: Use plan mode before applying changes, require explicit upload or write confirmation, inspect the backup and replacement report, and verify resulting public URLs separately when required.

Risk: Images outside the intended project root could be uploaded if outside-root access is allowed without review.

Mitigation: Keep outside-root access disabled by default and use --allow-outside-root only after checking the referenced paths.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yangchao228/skills/md-img-r2)
- [Publisher Profile](https://clawhub.ai/user/yangchao228)
- [Project Homepage](https://github.com/yangchao228/my_open_skills/tree/main/skills/publishing/md-img-r2)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands plus JSON image-publish plan and replacement reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Plan mode leaves Markdown unchanged; apply mode creates a backup and rewrites only confirmed local-image references.]

## Skill Version(s):

1.0.4 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
