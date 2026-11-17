## Description:

Automates local vector memory with Gemma-300M embeddings, model configuration, and memory health monitoring without external API dependencies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[greatape42069](https://clawhub.ai/user/greatape42069)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to configure a local vector-memory stack, set local embedding model options, and add health checks for memory indexing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can build a persistent local memory index over broad parts of the user's home environment.

Mitigation: Narrow the filesystem scope to specific project folders before setup and review exclusions for secrets and private data.

Risk: Setup may make persistent changes by installing dependencies, restarting the gateway, changing configuration, and appending HEARTBEAT.md content.

Mitigation: Review each setup step before approval and keep a rollback plan for dependency, configuration, gateway, and HEARTBEAT.md changes.

Risk: Symlink-based or overly broad indexing can pull unintended files into memory.

Mitigation: Avoid symlink-based indexing unless deliberate and verify indexed paths after the first run.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/greatape42069/skills/neverforget)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup guidance for local indexing, model configuration, exclusion rules, and memory health checks.]

## Skill Version(s):

1.0.4 (source: SKILL.md frontmatter, package.json, _meta.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
