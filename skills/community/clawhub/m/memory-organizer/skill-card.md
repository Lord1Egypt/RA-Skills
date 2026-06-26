## Description: <br>
Organize, compress, and curate OpenClaw memory without polluting permanent memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codeblackhole1024](https://clawhub.ai/user/codeblackhole1024) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to keep permanent memory concise while preserving dated memory history. It supports scanning, compressing, deduplicating, and selectively promoting durable facts from workspace memory files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can alter workspace memory files during compression, merge, discard, and cleanup operations. <br>
Mitigation: Run it only in trusted OpenClaw workspaces and review the target file or command before applying changes; documented compression and discard paths create backups. <br>
Risk: Incorrect promotion choices can move transient daily notes into permanent memory and increase startup context noise. <br>
Mitigation: Follow the documented two-layer memory rule and promote only stable preferences, durable configuration, workspace rules, and active cross-session todos. <br>


## Reference(s): <br>
- [Memory Organizer README](artifact/README.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/codeblackhole1024/memory-organizer) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text, shell commands, files] <br>
**Output Format:** [Markdown guidance and command-line text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update OpenClaw MEMORY.md and memory/*.md files; compression and discard operations create recoverable backup files when used as documented.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release evidence and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
