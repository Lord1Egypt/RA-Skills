## Description: <br>
Automated backup of agent state to trusted peers with encryption and versioning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to generate backup, restore, and rotation commands for Pilot agent configuration and state files using trusted peer storage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Backup commands can transmit sensitive agent state to a backup peer. <br>
Mitigation: Install and use only when the backup peer is understood and controlled; do not assume archive encryption unless pilotctl documentation or an added encryption step proves it. <br>
Risk: Restore commands can unpack received archives into persistent Pilot state. <br>
Mitigation: Verify the sender and inspect archive contents in a temporary directory before copying approved files into $HOME/.pilot. <br>
Risk: Backup rotation can delete local backup archives. <br>
Mitigation: Replace direct cleanup with a reviewed flow that previews exactly which backup files will be removed before deletion. <br>


## Reference(s): <br>
- [Pilot Protocol homepage](https://pilotprotocol.network) <br>
- [Pilot Backup ClawHub release](https://clawhub.ai/teoslayer/pilot-backup) <br>
- [Publisher profile](https://clawhub.ai/user/teoslayer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands assume pilotctl, jq, tar, and gzip are available and that a Pilot daemon is running.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact metadata version 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
