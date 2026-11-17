## Description:

Guides agents in installing and using SkillHub plugin UI registration so plugins can add custom Control dashboard views and navigation tabs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and SkillHub operators use this skill to understand plugin UI registration patterns, navigation grouping, icon selection, and troubleshooting for Control dashboard extensions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for broad write, shell command, API, and credential-related authority without clear operational boundaries.

Mitigation: Use it only in a disposable or controlled SkillHub environment, and allow shell or write actions only after reviewing separate trusted installation instructions and the exact files to be changed.

Risk: Credential handling guidance could lead users to provide API keys even though the security evidence recommends withholding them.

Mitigation: Do not provide API keys or other secrets unless the installation source is independently trusted and the required credential scope is understood.

Risk: Manual installation behavior may modify SkillHub UI or plugin files in ways that are not fully bounded by the artifact.

Mitigation: Inspect installation steps before execution, run from version-controlled or backed-up files, and verify sidebar registrations for duplicate IDs, valid groups, and supported icons.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/plugin-arch-2)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with TypeScript and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Review before execution because the security evidence flags broad write, shell, API, and credential-related authority.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
