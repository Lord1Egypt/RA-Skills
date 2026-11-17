## Description:

Perryts helps agents work with the Perry TypeScript-to-native compiler, including compile and run commands, cross-compilation targets, perry.toml configuration, native UI, system APIs, threading, widgets, internationalization, plugins, and updater guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhenyangze](https://clawhub.ai/user/zhenyangze)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to get concise guidance for building Perry projects, compiling TypeScript to native executables, targeting supported platforms, configuring projects, and using Perry runtime APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill documents a UI testing HTTP interface that can inspect and control apps without stating access controls or production safeguards.

Mitigation: Treat the Geisterhand UI testing server as test-only unless the Perry project proves it is authenticated, loopback-only, and excluded from production builds.

Risk: Generated guidance may involve sensitive capabilities such as microphone capture, clipboard access, keychain storage, child_process, plugins, FFI, or automatic updates.

Mitigation: Review code using these capabilities for explicit user consent, least-privilege scoping, trusted inputs, signature or hash checks where applicable, and platform policy compliance.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/zhenyangze/PerryTS-Skill)
- [ClawHub skill page](https://clawhub.ai/zhenyangze/skills/perryts-skill)
- [CLI & Configuration](references/cli-reference.md)
- [Standard Library](references/stdlib.md)
- [Multi-Threading](references/threading.md)
- [Native UI](references/ui.md)
- [Platforms](references/platforms.md)
- [Internationalization](references/i18n.md)
- [System APIs](references/system.md)
- [Widgets](references/widgets.md)
- [Plugins & Auto-Update](references/plugins.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline TypeScript, TOML, JSON, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only output; generated guidance may reference platform SDKs, signing keys, native APIs, plugins, FFI, and auto-update workflows.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
