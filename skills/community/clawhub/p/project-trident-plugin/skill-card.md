## Description: <br>
Permanent memory for OpenClaw agents. Lossless capture, intelligent routing, semantic recall, and disaster recovery in five tiers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shivaclaw](https://clawhub.ai/user/shivaclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this plugin to give agents persistent memory across sessions, including searchable conversation history, curated long-term memory, semantic recall, and recovery-oriented backups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The plugin can persist broad conversation history as long-term agent memory. <br>
Mitigation: Avoid storing secrets or sensitive content, review retention and purge procedures before enabling it, and restrict use in sensitive workspaces until the memory location and lifecycle are understood. <br>
Risk: Background routing can process memory on a schedule. <br>
Mitigation: Review the Layer 0.5 schedule and disable scheduled routing unless ongoing background processing is required. <br>
Risk: Semantic recall and Git backup can use external services or remote endpoints. <br>
Mitigation: Disable semantic recall, cloud endpoints, and Git backup unless needed; prefer local services for private workspaces and verify any configured remote destination. <br>
Risk: The artifact describes automatic setup for Qdrant and FalkorDB binaries. <br>
Mitigation: Verify downloaded binaries and source locations before first activation, especially in production or sensitive environments. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/shivaclaw/project-trident-plugin) <br>
- [Project homepage](https://github.com/ShivaClaw/trident-plugin) <br>
- [Repository](https://github.com/ShivaClaw/trident-plugin) <br>
- [Issue tracker](https://github.com/ShivaClaw/trident-plugin/issues) <br>
- [README](artifact/README.md) <br>
- [Installation guide](artifact/INSTALL.md) <br>
- [Configuration schema](artifact/config.schema.json) <br>
- [Plugin manifest](artifact/plugin-manifest.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Text and Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent-facing memory tool results may include search matches, expanded summaries, appended memory confirmations, and recalled context.] <br>

## Skill Version(s): <br>
2.0.0 (source: release evidence, SKILL.md frontmatter, plugin-manifest.json; package.json and openclaw.plugin.json still report 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
