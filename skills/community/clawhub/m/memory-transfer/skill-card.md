## Description: <br>
Transfer memory files from one OpenClaw agent workspace to another for migration, context sharing, or backups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codeblackhole1024](https://clawhub.ai/user/codeblackhole1024) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to list and transfer MEMORY.md and daily memory Markdown files between agent workspaces. It is intended for migration, context sharing, and backup workflows where copied memory is reviewed before use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release evidence says the skill overstates privacy features and may copy raw persistent memory that contains sensitive user information. <br>
Mitigation: Treat privacy filtering claims as unsupported; run a dry run first, inspect source memory, and manually redact sensitive content before transfer. <br>
Risk: The release evidence says real transfers can overwrite persistent target-agent memory. <br>
Mitigation: Make an independent backup of target memory before running a real transfer and review any generated .backup files after execution. <br>
Risk: The release evidence flags broad filesystem targeting through agent workspace paths. <br>
Mitigation: Use only trusted agent IDs and confirm source and target workspace paths before copying files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/codeblackhole1024/memory-transfer) <br>
- [Publisher profile](https://clawhub.ai/user/codeblackhole1024) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown instructions with bash command examples; CLI output is plain text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [When executed, the bundled script may copy or back up Markdown memory files in OpenClaw workspaces.] <br>

## Skill Version(s): <br>
2.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
