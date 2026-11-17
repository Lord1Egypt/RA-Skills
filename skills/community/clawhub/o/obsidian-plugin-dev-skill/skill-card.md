## Description:

Comprehensive skill for Obsidian plugin development with TypeScript, covering lifecycle, CodeMirror 6 editor extensions, UI frameworks, Vault APIs, settings, security, testing, CI/CD, and community submission.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yungho](https://clawhub.ai/user/yungho)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to create, debug, test, package, and prepare Obsidian community plugins written in TypeScript.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated plugin guidance could lead to reversible Base64 storage for API keys or other secrets.

Mitigation: Require Obsidian SecretStorage or another real secure storage mechanism, and review any generated credential-handling code before use.

Risk: Generated commands or workflows may modify vault files, delete files, copy builds into a live plugin folder, send network requests, or push release tags.

Mitigation: Review generated code and shell commands before execution, especially file operations, network requests, release automation, and live-vault deployment steps.

Risk: Unpinned one-off developer tool execution can change behavior over time.

Mitigation: Pin tool versions or install developer tools locally before running linting, build, or release commands.

## Reference(s):

- [Skill overview](SKILL.md)
- [README](README.md)
- [Lifecycle & Core API](reference/lifecycle.md)
- [CodeMirror 6 Editor Extensions](reference/editor-extensions.md)
- [React / Svelte / Vue Integration](reference/frameworks.md)
- [Vault & File Operations](reference/vault-operations.md)
- [Settings & Data Migration](reference/settings-migration.md)
- [Security & SecretStorage](reference/security.md)
- [Accessibility](reference/accessibility.md)
- [CSS Styling](reference/css-accessibility.md)
- [Dev Workflow & CLI](reference/dev-workflow.md)
- [Testing](reference/testing.md)
- [ESLint Rules](reference/eslint-rules.md)
- [CI/CD & Release](reference/cicd-release.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with TypeScript, JavaScript, JSON, CSS, YAML, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are advisory agent responses that should be reviewed before applying to plugin source code, release workflows, or vault files.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
