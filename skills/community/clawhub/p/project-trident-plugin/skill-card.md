## Description:

Permanent memory for OpenClaw agents. Lossless capture, intelligent routing, semantic recall, and disaster recovery in five tiers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shivaclaw](https://clawhub.ai/user/shivaclaw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this plugin to give agents persistent memory tools for searching, expanding, updating, and recalling conversation context across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release makes broad persistence and installation claims that do not match the shipped code.

Mitigation: Review the actual plugin behavior and test memory capture, recall, and recovery workflows before relying on it for production continuity.

Risk: Setup guidance includes unsafe installation patterns and unsigned binary download commands.

Mitigation: Do not run sudo curl pipelines or downloaded binaries until sources, checksums, and signatures are independently verified.

Risk: Persistent capture, cloud embeddings, cron routing, and Git backup can expose or retain sensitive conversation memory.

Mitigation: Enable these features only after confirming storage locations, access controls, retention expectations, and third-party service exposure.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shivaclaw/skills/project-trident-plugin)
- [Repository](https://github.com/ShivaClaw/trident-plugin)
- [Issue tracker](https://github.com/ShivaClaw/trident-plugin/issues)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown documentation with inline shell commands and JSON configuration examples; plugin tools return text responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Memory tools accept search, expansion, update, and recall parameters for agent context workflows.]

## Skill Version(s):

2.0.0 (source: server release metadata, SKILL.md frontmatter, plugin-manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
