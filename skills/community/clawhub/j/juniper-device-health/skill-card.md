## Description: <br>
Juniper JunOS device health check and triage procedure for troubleshooting MX, SRX, EX, QFX, and PTX platforms across Routing Engine health, Packet Forwarding Engine state, chassis alarms, system resources, environment, dual-RE failover, alarm triage, PFE statistics, and commit-correlated diagnostics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vahagn-madatyan](https://clawhub.ai/user/vahagn-madatyan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Network engineers and incident responders use this skill to run a structured JunOS health assessment, identify RE/PFE, alarm, storage, interface, routing, and environmental issues, and produce prioritized findings with recommended actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence says the skill is labeled read-only while recommending actions that can change or delete data on network devices. <br>
Mitigation: Require explicit operator approval before request, cleanup, rescue-save, rollback, file-removal, or power-cycle actions, especially during incidents where logs and core dumps may be needed. <br>
Risk: Credentialed access to production network devices can expose sensitive operational state or enable impactful actions. <br>
Mitigation: Use least-privilege SSH or console credentials and scope execution to approved devices and maintenance procedures. <br>
Risk: JunOS health data from a backup Routing Engine can lead to incorrect assessment of the active forwarding path. <br>
Mitigation: Verify RE mastership first and switch to the master Routing Engine before collecting health data. <br>


## Reference(s): <br>
- [Juniper JunOS CLI Reference](references/cli-reference.md) <br>
- [Juniper JunOS Threshold Tables](references/threshold-tables.md) <br>
- [ClawHub release page](https://clawhub.ai/vahagn-madatyan/juniper-device-health) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with inline JunOS CLI commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces prioritized severity findings and recommended actions; does not collect telemetry by itself.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
