## Description: <br>
Heleni Maintenance helps an agent back up a workspace to GitHub, update OpenClaw and installed skills, and clean stale OpenClaw session data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[netanel-abergel](https://clawhub.ai/user/netanel-abergel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to run workspace backups, OpenClaw and skill updates, and session-store cleanup on demand or on a schedule. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run unattended backups that upload broad workspace contents to GitHub. <br>
Mitigation: Use a private repository, review staged files before pushes, and exclude secrets and private notes from backup scope. <br>
Risk: The skill looks for GitHub credentials and may use tokens with access to repositories. <br>
Mitigation: Store credentials in a secret manager, use least-privilege tokens, avoid printing token values, and rotate credentials if exposed. <br>
Risk: The skill can update OpenClaw, update installed skills, clean session state, and restart the gateway. <br>
Mitigation: Require explicit confirmation for updates, session cleanup, and restarts; keep cron jobs visible and easy to disable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/netanel-abergel/heleni-maintenance) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance, Text] <br>
**Output Format:** [Markdown with shell commands and status reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May schedule recurring maintenance, push workspace changes, update installed tools, and clean session data.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
