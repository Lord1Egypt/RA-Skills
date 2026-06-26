## Description: <br>
Build OpenClaw plugins from scratch, including the manifest, entry point, tool registration, channel plugins, provider plugins, config schema, setup wizards, runtime helpers, and publishing steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pathanaawej0-dot](https://clawhub.ai/user/pathanaawej0-dot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to create, extend, debug, test, and publish native OpenClaw plugins, including tools, channels, providers, manifests, runtime helpers, and configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated plugin code or manifests may create powerful OpenClaw extensions, including tools, channels, providers, hooks, routes, or services. <br>
Mitigation: Review generated files before enabling them, keep side-effect tools optional or explicitly allowed, and scan plugins before deployment. <br>
Risk: Example provider and channel configurations may involve API keys, OAuth tokens, or bot tokens. <br>
Mitigation: Store real credentials outside source-controlled files and mark secret configuration fields as sensitive. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pathanaawej0-dot/openclaw-plugin-creator-agent-skill) <br>
- [Homepage](https://github.com/pathanaawej0-dot/openclaw-plugin-creation-skill) <br>
- [Manifest reference](references/manifest.md) <br>
- [SDK subpaths reference](references/sdk-subpaths.md) <br>
- [Channel plugin reference](references/channel-plugin.md) <br>
- [Provider plugin reference](references/provider-plugin.md) <br>
- [Runtime reference](references/runtime.md) <br>
- [Testing reference](references/testing.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code, shell commands, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces implementation guidance and scaffoldable examples for user-reviewed OpenClaw plugin files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
