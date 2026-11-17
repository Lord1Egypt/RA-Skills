## Description:

Use when operating Halo themes, plugins, attachments, backups, or moments from the terminal, including install, upgrade, activate, upload, download, create, delete, and batch maintenance flows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ruibaby](https://clawhub.ai/user/ruibaby)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to operate Halo themes, plugins, attachments, backups, and moments from the terminal, including routine maintenance and mutating administration tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: URL-based installs or upgrades can fetch content from non-default hosts, and --yes can bypass CLI confirmation prompts.

Mitigation: Review source URLs before execution, prefer trusted hosts, and reserve --yes for controlled automation.

Risk: Commands using --force can mutate or delete Halo resources.

Mitigation: Use the intended --profile, inspect resources with list or get first, and require review before destructive batch maintenance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ruibaby/skills/halo-cli-operations)
- [Shared Halo CLI skill reference](../halo-cli-shared)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include JSON-output guidance for automation and profile selection guidance for target environments.]

## Skill Version(s):

0.1.1 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
