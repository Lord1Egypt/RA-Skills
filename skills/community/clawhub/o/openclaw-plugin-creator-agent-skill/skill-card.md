## Description:

Build OpenClaw plugins from scratch, including manifests, entry points, tool registration, channel and provider plugins, config schemas, setup wizards, runtime helpers, and publishing steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pathanaawej0-dot](https://clawhub.ai/user/pathanaawej0-dot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to scaffold, extend, debug, test, and publish native OpenClaw plugins that add tools, messaging channels, model providers, runtime hooks, and configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated or installed OpenClaw plugins run as trusted Gateway code and may handle credentials, write configuration, register routes or tools, and call external providers.

Mitigation: Review generated plugin code and configuration before running it, avoid placing real API keys or bot tokens in shared config files, and use allow, deny, and sensitive-field controls for privileged behavior.

Risk: Following install commands without verifying package identity can introduce untrusted CLI or plugin code.

Mitigation: Verify the official ClawHub CLI package identity before installation, prefer pinned versions, and review dependencies before executing generated commands.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/pathanaawej0-dot/skills/openclaw-plugin-creator-agent-skill)
- [Project Homepage](https://github.com/pathanaawej0-dot/openclaw-plugin-creation-skill)
- [Plugin Manifest Reference](references/manifest.md)
- [SDK Subpath Import Reference](references/sdk-subpaths.md)
- [Channel Plugin Guide](references/channel-plugin.md)
- [Provider Plugin Guide](references/provider-plugin.md)
- [Plugin Runtime Reference](references/runtime.md)
- [Plugin Testing Reference](references/testing.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code, JSON/YAML configuration, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated plugin files or commands for local execution when the user asks the agent to implement a plugin.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release; changelog released 2026-04-29)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
