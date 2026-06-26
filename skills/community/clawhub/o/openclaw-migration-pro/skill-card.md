## Description: <br>
Openclaw Migration Pro helps users analyze, package, transfer, and restore OpenClaw skills, memory, configuration, and cron jobs across environments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yankj](https://clawhub.ai/user/yankj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to migrate or back up an OpenClaw environment while preserving local skills, memory, configuration, and scheduled jobs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can package and transmit sensitive OpenClaw skills, memory, configuration, and cron job data. <br>
Mitigation: Inspect archive contents before transfer, disable automatic sending unless explicitly intended, and encrypt backups before moving them through cloud storage or shared channels. <br>
Risk: Restoring a backup can overwrite or reintroduce configuration and cron jobs in the target environment. <br>
Mitigation: Restore only into a backed-up or fresh environment, review restored configuration and scheduled jobs, and restart services only after confirming the contents. <br>
Risk: The release has a suspicious security verdict because its migration behavior has weak warnings and controls. <br>
Mitigation: Install only when the migration behavior is acceptable for the environment and review the skill and generated backup before deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/yankj/openclaw-migration-pro) <br>
- [README](README.md) <br>
- [Migration Guide](MIGRATION-GUIDE.md) <br>
- [Capability Report](CAPABILITY-REPORT.md) <br>
- [Compression Comparison](COMPRESSION-COMPARISON.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated manifest or backup files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate archives, manifests, and restored OpenClaw files when the recommended commands are executed.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
