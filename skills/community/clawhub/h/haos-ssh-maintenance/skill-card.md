## Description: <br>
Use when Home Assistant OS needs SSH-based maintenance that cannot be completed cleanly through the Home Assistant API alone. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nextaltair](https://clawhub.ai/user/nextaltair) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and operators use this skill to guide Home Assistant OS maintenance when API-first inspection is insufficient and SSH access is needed for direct file access, YAML edits, custom component inspection, HAOS shell troubleshooting, or interactive ha CLI work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: SSH access can read or modify Home Assistant configuration and internal storage. <br>
Mitigation: Verify TOOLS.md points to the intended Home Assistant host, start read-only, review proposed YAML or .storage edits before they happen, and keep backups. <br>
Risk: Automation or registry edits can affect locks, alarms, access control, or physical devices. <br>
Mitigation: Require explicit review before behavior changes that affect safety-sensitive entities, make the smallest targeted change, and report rollback paths. <br>
Risk: Home Assistant ha CLI commands may behave differently in one-shot SSH and interactive SSH sessions. <br>
Mitigation: Use interactive PTY-backed SSH for ha CLI log access or commands that fail in one-shot mode, then verify reload or restart needs after the change. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nextaltair/haos-ssh-maintenance) <br>
- [Publisher profile](https://clawhub.ai/user/nextaltair) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports inspected paths, findings, changes, and whether reload or restart is needed.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
