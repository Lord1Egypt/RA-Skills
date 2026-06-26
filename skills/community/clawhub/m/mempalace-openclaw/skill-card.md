## Description: <br>
MemPalace archives AI conversations into local long-term storage and supports semantic search over saved memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deveuper](https://clawhub.ai/user/deveuper) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to archive, search, and restore important conversation memories across OpenClaw-compatible workflows. It is intended for local memory retention where users want searchable context without relying on a cloud memory service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist broad conversation and project data into durable local memory. <br>
Mitigation: Install only when durable searchable memory is intended, verify storage paths before use, and avoid mining directories that contain secrets or private files. <br>
Risk: Initial setup can modify the active Python environment by installing dependencies. <br>
Mitigation: Use an isolated virtual environment and review package installation commands before first execution. <br>
Risk: Hooks or scheduled saving can automatically capture session content. <br>
Mitigation: Disable or avoid hooks and cron-style automation unless automatic saving is explicitly desired. <br>
Risk: The artifact may perform Wikipedia lookups despite local-only messaging. <br>
Mitigation: Block or remove Wikipedia lookup behavior when fully offline operation is required. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/deveuper/mempalace-openclaw) <br>
- [Bundled skill instructions](artifact/SKILL.md) <br>
- [Bundled README](artifact/README.md) <br>
- [Bundled MemPalace package README](artifact/mempalace/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline commands and local file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces and searches local conversation archives and vector index files when executed in a configured environment.] <br>

## Skill Version(s): <br>
1.6.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
