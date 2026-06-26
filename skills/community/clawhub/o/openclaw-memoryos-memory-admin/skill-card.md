## Description: <br>
Inspect, back up, search, export, and update OpenClaw long-term memory stored with MemoryOS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaocaijic](https://clawhub.ai/user/xiaocaijic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect, back up, search, export, and intentionally update OpenClaw-style long-term memory stored in MemoryOS files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read, export, back up, and change persistent long-term memory files. <br>
Mitigation: Verify the MemoryOS data root, user ID, assistant ID, backup directory, and export path before running commands, and create a backup before mutating memory. <br>
Risk: Adding or replacing memory with unreviewed text can persist incorrect or unwanted user or assistant context. <br>
Mitigation: Review proposed memory text before adding it, search for near-duplicates first, and use profile replacement only when a curated replacement is intended. <br>


## Reference(s): <br>
- [MemoryOS Long-Term Memory Layout](references/memoryos-layout.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/xiaocaijic/openclaw-memoryos-memory-admin) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples; bundled script commands can emit JSON summaries and Markdown exports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Operates on local MemoryOS JSON storage files and may create backups or export files when invoked.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
