## Description: <br>
Comprehensive skill for Obsidian plugin development with TypeScript, including plugin lifecycle, CodeMirror 6 editor extensions, framework integration, Vault API patterns, settings migrations, security, accessibility, testing, CI/CD, and community submission guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yungho](https://clawhub.ai/user/yungho) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI coding agents use this skill to create, debug, test, release, and prepare Obsidian community plugins written in TypeScript. It provides patterns and checklists for lifecycle management, editor extensions, settings, accessibility, security, and submission review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Plugin authors could copy API-key examples or store long-lived credentials in synced or plaintext settings. <br>
Mitigation: Use Obsidian SecretStorage where available, avoid persisting long-lived keys in plaintext settings, and redact tokens from logs and errors. <br>
Risk: Plugins generated from the guidance may call external HTTPS endpoints without clearly explaining user data transfer. <br>
Mitigation: Validate HTTPS endpoints and disclose any external data transfer to users before release. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yungho/obsidian-plugin-dev-skill) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Lifecycle and core API](artifact/reference/lifecycle.md) <br>
- [CodeMirror 6 editor extensions](artifact/reference/editor-extensions.md) <br>
- [Framework integration](artifact/reference/frameworks.md) <br>
- [Vault operations](artifact/reference/vault-operations.md) <br>
- [Settings migration](artifact/reference/settings-migration.md) <br>
- [Security and SecretStorage](artifact/reference/security.md) <br>
- [Accessibility](artifact/reference/accessibility.md) <br>
- [Testing](artifact/reference/testing.md) <br>
- [CI/CD and release](artifact/reference/cicd-release.md) <br>
- [Obsidian ESLint plugin](https://github.com/obsidianmd/eslint-plugin) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with TypeScript, JSON, CSS, YAML, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Topic-specific reference files are loaded as needed for plugin lifecycle, security, accessibility, testing, and release workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
