## Description: <br>
Use when managing a Halo blog instance via CLI, including authentication, posts, pages, themes, plugins, attachments, backups, comments, moments, notifications, or public site search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alex-shen1121](https://clawhub.ai/user/alex-shen1121) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and site operators use this skill to administer Halo blog instances from an agent-assisted CLI workflow, including publishing content, managing profiles, moderating comments, operating themes and plugins, handling attachments and backups, and searching public site content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can administer a Halo site using OAuth or other sensitive credentials. <br>
Mitigation: Use least-privilege, revocable tokens and avoid sharing real credentials in terminals, logs, or transcripts. <br>
Risk: Publishing, force-importing, deleting, installing, uninstalling, and bulk-upgrading can significantly change live site content or behavior. <br>
Mitigation: Require explicit user approval before high-impact operations and confirm the active Halo profile before changes. <br>
Risk: Markdown-to-HTML publishing may introduce unintended formatting or content changes. <br>
Mitigation: Review Markdown and rendered HTML before publishing or importing content. <br>


## Reference(s): <br>
- [Halo website](https://www.halo.run) <br>
- [ClawHub release page](https://clawhub.ai/alex-shen1121/halo-blog) <br>
- [Publisher profile](https://clawhub.ai/user/alex-shen1121) <br>
- [Authentication and profile management](references/auth.md) <br>
- [Content management](references/content.md) <br>
- [Publishing rules](references/publishing.md) <br>
- [Operations](references/operations.md) <br>
- [Moderation](references/moderation.md) <br>
- [Search](references/search.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, configuration examples, and script snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or run Halo CLI operations that publish, modify, delete, install, uninstall, back up, or search site resources.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
