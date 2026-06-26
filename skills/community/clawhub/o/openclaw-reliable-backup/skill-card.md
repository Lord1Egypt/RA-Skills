## Description: <br>
Provides guided OpenClaw backup, snapshot, retention, email delivery, and recovery workflows for agents managing OpenClaw state. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LiliWang76](https://clawhub.ai/user/LiliWang76) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and operators use this skill to set up local backup directories, create scheduled or pre-change snapshots, manage retention, and follow recovery guidance for OpenClaw configuration and workspace state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Backups may include OpenClaw credentials, identity files, workspace data, and other private state. <br>
Mitigation: Use local encrypted storage with strict permissions, review the backup scope before execution, and keep archives out of shared locations. <br>
Risk: Email delivery can transmit sensitive backup archives without built-in encryption safeguards. <br>
Mitigation: Skip email delivery unless archives are encrypted before sending and the mail-skill configuration has been reviewed. <br>
Risk: Cleanup, restore, and gateway-control commands can delete backups or change running OpenClaw state. <br>
Mitigation: Require explicit user approval before deletion, restore, or gateway-control commands and verify checksums before recovery. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/LiliWang76/openclaw-reliable-backup) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and confirmation prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose filesystem, archive, restore, cleanup, and email-delivery commands for user approval.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
