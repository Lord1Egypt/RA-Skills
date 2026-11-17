## Description:

Use when managing a Halo blog instance via CLI, including authentication, posts, pages, themes, plugins, attachments, backups, comments, moments, notifications, or public site search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alex-shen1121](https://clawhub.ai/user/alex-shen1121)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, content operators, and blog maintainers use this skill to operate Halo blog instances from an agent, including profile authentication, content publishing, theme and plugin operations, attachments and backups, comment moderation, notifications, and public search.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publishing untrusted Markdown can expose the user to unexpected local code execution through the Markdown-to-HTML helper workflow.

Mitigation: Use trusted Markdown sources, pin npm dependencies, and avoid the publishing helper for untrusted Markdown.

Risk: Forced imports, deletes, uninstalls, bulk upgrades, and plugin changes can alter live blog content or configuration.

Mitigation: Verify the active Halo profile before using `--force` or `--all --yes`, review commands before execution, and keep backups before content or plugin changes.

Risk: Tokens or passwords passed through shared command lines can expose credentials.

Mitigation: Avoid sharing commands that contain real tokens or passwords, and use Halo profile and keyring storage for credentials.

## Reference(s):

- [Halo Official Site](https://www.halo.run)
- [Authentication and Profile Management](artifact/references/auth.md)
- [Content Management](artifact/references/content.md)
- [Moderation and Notifications](artifact/references/moderation.md)
- [Operations](artifact/references/operations.md)
- [Publishing Format Rules](artifact/references/publishing.md)
- [Public Search](artifact/references/search.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Halo CLI commands, JSON-oriented workflows, Markdown publishing guidance, and local script usage guidance.]

## Skill Version(s):

1.0.5 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
