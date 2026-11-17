## Description:

Manage Git hooks with easy installation, configuration, and sharing, supporting lint, test, commit message, and branch name validations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaiyuelv](https://clawhub.ai/user/kaiyuelv)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to install, configure, share, and validate Git hooks for repository quality gates such as linting, tests, branch naming, commit message format, and local CI checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hook import or install paths can write or delete files outside the Git hooks directory.

Mitigation: Use only on repositories you trust, avoid importing hook configuration from untrusted sources, and prefer a fixed version that rejects non-standard hook names and enforces path containment before writing or deleting files.

Risk: Installing or uninstalling hooks can overwrite or remove existing repository hooks.

Mitigation: Back up existing .git/hooks files and review proposed hook changes before running install, import, or uninstall commands.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kaiyuelv/skills/git-hooks-manager)
- [README](artifact/README.md)
- [Skill Definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, Python code examples, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or modify Git hook scripts and exported JSON hook configuration files when its commands are executed.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
