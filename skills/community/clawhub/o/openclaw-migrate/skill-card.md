## Description: <br>
Migrate OpenClaw configurations, skills, memory, tokens, environment variables, and cron jobs to a new host over SSH. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chris6970barbarian-hue](https://clawhub.ai/user/chris6970barbarian-hue) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to move an OpenClaw installation from one host to another, including local configuration, skills, memory, selected credentials, environment variables, and scheduled jobs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The migration copies sensitive OpenClaw data, memory, tokens, environment variables, and cron jobs to another host. <br>
Mitigation: Run it only between trusted hosts, review which credentials and scheduled jobs should move, and limit copied secrets before migration. <br>
Risk: The security scan reports broad control over SSH migration and unsafe shell command construction. <br>
Mitigation: Use only trusted host, user, and key values, inspect the generated migration behavior before execution, and avoid untrusted input in connection settings. <br>
Risk: Remote shell profiles and crontab entries may be changed during migration. <br>
Mitigation: Review the target host after migration and clean up shell profile or crontab entries that should not persist. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/chris6970barbarian-hue/openclaw-migrate) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Text] <br>
**Output Format:** [Markdown and terminal-oriented command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Interactive setup, SSH connectivity checks, migration status text, and error messages.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
