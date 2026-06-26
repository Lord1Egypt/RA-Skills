## Description: <br>
Log Collector is a permanent log collection agent that collects logs and history from cluster nodes over SSH/VPN every 3 hours and stores them in logs.db with 30-day retention. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kikikari](https://clawhub.ai/user/kikikari) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure and run recurring collection of system, OpenClaw, VPN, and connection logs across multi-node clusters for troubleshooting and retention-managed audit history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Continuous cluster-wide log collection can capture sensitive logs from every configured node. <br>
Mitigation: Restrict the nodes database to approved systems, add redaction or exclusions for secrets, and protect logs.db. <br>
Risk: SSH collection relies on credentials and the artifact disables SSH host key verification. <br>
Mitigation: Use dedicated least-privilege SSH credentials and remove StrictHostKeyChecking=no before enabling collection. <br>
Risk: A cron deployment can keep collecting logs every 3 hours after installation. <br>
Mitigation: Document how to disable the cron job and review the schedule before production use. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown with inline code blocks and a Python script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes recurring log collection behavior, SQLite storage in logs.db, and 30-day retention when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
