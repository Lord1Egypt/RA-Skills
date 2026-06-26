## Description: <br>
Memory Layer provides guidance for organizing local agent memory into Index, Topic, and Transcript layers, with migration steps, configuration examples, and optional autoDream cleanup guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[whyischen](https://clawhub.ai/user/whyischen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to design and maintain a local memory structure that keeps always-loaded index content small, stores reusable knowledge in topic files, and keeps raw transcripts searchable without loading them into context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Transcript files are local plaintext logs and may expose sensitive information if users store secrets, credentials, health records, government IDs, or other private data. <br>
Mitigation: Keep sensitive data out of memory files, review transcript contents before retention or sharing, and apply local access controls and backups appropriate for the workspace. <br>
Risk: The optional autoDream cron example references placeholder automation that may modify or archive memory files if a user wires it to a real executable. <br>
Mitigation: Treat the example command as pseudocode unless you control the executable, run manual dry runs first, and make backups before migration, rollback, or automated archive steps. <br>


## Reference(s): <br>
- [Architecture Design](references/architecture.md) <br>
- [Index Layer Specification](references/index-spec.md) <br>
- [Topic Layer Specification](references/topic-spec.md) <br>
- [Transcript Layer Specification](references/transcript-spec.md) <br>
- [Configuration Reference](references/config.md) <br>
- [autoDream Guidance](references/autodream.md) <br>
- [Migration Guide](guides/MIGRATION.md) <br>
- [Examples](guides/EXAMPLES.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only skill; it does not include executable implementation code.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
