## Description:

通过官方 @halo-dev/api-client 发布 Halo 博客文章，支持将 Markdown 自动转换为 HTML 富文本，并可查看和删除文章。

This skill is ready for commercial/non-commercial use.

## Publisher:

[binsonhao](https://clawhub.ai/user/binsonhao)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and Halo blog operators use this skill to publish Markdown-authored posts through the Halo API, list recent posts, and delete posts by keyword.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Halo bearer token and post content can be sent to the hardcoded default site if HALO_URL is not explicitly set.

Mitigation: Set HALO_URL explicitly for every run, use a least-privileged Halo token, and revoke any token used without a confirmed HALO_URL.

Risk: Delete behavior can remove the first post matching a keyword with weak safeguards.

Mitigation: Avoid deletion unless the target post has been verified, and keep backups or recovery procedures available before running delete commands.

Risk: The lockfile resolves dependencies from an HTTP mirror, which may weaken dependency integrity expectations.

Mitigation: Regenerate the lockfile from an HTTPS registry and update dependencies before production installation.

## Reference(s):

- [ClawHub skill page: halo-manager](https://clawhub.ai/binsonhao/skills/halo-manager)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and CLI-oriented text with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses HALO_URL and HALO_TOKEN environment variables when executing the bundled CLI.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
