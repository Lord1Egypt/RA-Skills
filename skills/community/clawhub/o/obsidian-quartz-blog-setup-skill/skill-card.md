## Description:

Guides an AI coding agent through setting up a Quartz v4 static blog from an Obsidian vault and deploying it to GitHub Pages with GitHub Actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[orbisz](https://clawhub.ai/user/orbisz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical writers, and Obsidian users use this skill to create an initial Quartz blog project, sync Markdown notes into it, configure GitHub Pages deployment, and publish the site. It is intended for first-time setup rather than incremental blog updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish broad content from an Obsidian vault, including private notes, credentials, client data, personal information, or sensitive attachments.

Mitigation: Use a dedicated public-notes vault or allowlist, inspect the exact files to be copied, confirm repository visibility, and require final manual approval before git add, commit, or push.

Risk: The artifact includes a self-evolution section that can propose modifying the skill after execution.

Mitigation: Review or remove the self-evolution behavior before installation, and require human review for any proposed changes to the skill source.

Risk: The workflow runs cloned Quartz and npm commands as part of local setup.

Mitigation: Pin Quartz and npm execution to reviewed versions where possible and review commands before execution.

## Reference(s):

- [Quartz v4 Documentation](https://quartz.jzhao.xyz/)
- [Obsidian](https://obsidian.md)
- [GitHub Pages](https://pages.github.com/)
- [Companion update skill](https://github.com/orbisz/obsidian-wiki-blog-push)
- [ClawHub skill page](https://clawhub.ai/orbisz/skills/obsidian-quartz-blog-setup-skill)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Code, Files, Guidance]

**Output Format:** [Markdown with inline shell, PowerShell, TypeScript, and YAML code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup steps for local project changes, Quartz configuration, Git remote configuration, and a GitHub Actions deployment workflow.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
