## Description: <br>
Automates Sovereign Local Vector Memory and Gemma-300M embeddings for OpenClaw, including local vector embedding setup, model configuration, and memory health monitoring without external API dependencies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[GreatApe42069](https://clawhub.ai/user/GreatApe42069) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External developers and OpenClaw users use this skill to configure local vector memory, local embedding model settings, and memory health checks for an agent environment. It is intended for users who explicitly want persistent local memory built from broad home or workspace content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad home or workspace indexing can capture sensitive local content into persistent agent memory. <br>
Mitigation: Before setup, narrow indexed paths to specific project folders, review exclusions, avoid symlinking sensitive directories, and know how to delete the vector database. <br>
Risk: The skill changes OpenClaw memory defaults and may retain indexed data after source files are removed. <br>
Mitigation: Review configuration changes before running, keep a rollback path for memory settings, and revert OpenClaw memory configuration when the persistent memory behavior is no longer wanted. <br>
Risk: Initial setup downloads packages and a local embedding model before memory indexing can run. <br>
Mitigation: Confirm the dependency and model sources are acceptable for the environment before approving setup commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/GreatApe42069/neverforget) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup guidance, local memory health checks, and OpenClaw memory configuration changes.] <br>

## Skill Version(s): <br>
1.0.4 (source: SKILL.md frontmatter, package.json, _meta.json, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
