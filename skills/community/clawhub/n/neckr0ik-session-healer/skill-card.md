## Description: <br>
Automatically detects and repairs locked OpenClaw session files by reporting stale locks, clearing them, and recovering failed sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Neckr0ik](https://clawhub.ai/user/Neckr0ik) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to diagnose OpenClaw session lock timeouts, identify stale lock files, and repair or recover affected sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can alter OpenClaw session files and remove lock files, which may disrupt running agents or corrupt session state. <br>
Mitigation: Inspect sessions first with check or dry-run behavior, keep backups, and avoid force-clearing locks while OpenClaw agents are running. <br>
Risk: Unlocking or recovering the wrong session can affect active or recoverable session data. <br>
Mitigation: Manually verify that a session is inactive before unlocking or recovering it, and rely on backups before modifying session files. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Neckr0ik/neckr0ik-session-healer) <br>
- [Skill documentation](SKILL.md) <br>
- [Main healer script](scripts/healer.py) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and command output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May modify OpenClaw lock and session files when heal, unlock, or recover commands are executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, claw.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
