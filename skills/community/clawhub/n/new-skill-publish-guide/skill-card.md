## Description:

Guides skill maintainers through creating a ClawHub skill package, publishing it, archiving release notes in IMA, and notifying the main agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawhub-master](https://clawhub.ai/user/clawhub-master)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this guide to prepare new ClawHub skill releases, avoid publishing local secrets, run the ClawHub CLI release flow, archive release information in IMA, and send a completion notice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact exposes apparent live IMA credentials.

Mitigation: Treat the credentials as compromised, rotate them, and replace all credential examples with placeholders or environment-variable references before reuse.

Risk: Broad publishing commands such as sync --all could release unintended skills or files from a shared skills directory.

Mitigation: Review dry-run output first and run publishing commands only from a directory containing the intended release artifacts.

Risk: Local absolute paths and machine-specific setup details can confuse downstream users or disclose local environment structure.

Mitigation: Replace local paths with placeholders and document that users must configure their own runtime package and credentials after installation.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/clawhub-master/skills/new-skill-publish-guide)
- [Artifact README](artifact/README.md)
- [Artifact skill instructions](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Procedural release checklist with security-sensitive credential handling guidance.]

## Skill Version(s):

1.2.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
