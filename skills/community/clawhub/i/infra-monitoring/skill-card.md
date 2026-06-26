## Description: <br>
Infra Monitoring helps small teams, solo operators, and self-hosters assess server health, uptime, resource usage, SSL certificate expiry, and incidents through plain-language status reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gitcanadabrett](https://clawhub.ai/user/gitcanadabrett) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, DevOps engineers, solo SaaS operators, and self-hosters use this skill to interpret server metrics, endpoint checks, SSL certificate status, and incident signals. It is intended for practical infrastructure health reporting and prioritized operational guidance, not full observability platform replacement. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may be asked to check domains, IPs, logs, or infrastructure details that the user is not authorized to test. <br>
Mitigation: Only assess user-provided systems and endpoints that the user is authorized to monitor, and ask for scope clarification when ownership or authorization is unclear. <br>
Risk: Infrastructure logs, command output, or endpoint responses may include secrets, private keys, API tokens, or sensitive user data. <br>
Mitigation: Instruct users to redact secrets and sensitive data before sharing inputs, and exclude sensitive response data from reports and incident logs. <br>
Risk: On-demand health checks can be mistaken for continuous monitoring, real-time detection, or automated remediation. <br>
Mitigation: State when findings are based on supplied snapshots or explicit checks, and provide remediation guidance or commands for user review instead of taking direct action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gitcanadabrett/infra-monitoring) <br>
- [Publisher profile](https://clawhub.ai/user/gitcanadabrett) <br>
- [Infrastructure & Uptime Monitoring Skill README](artifact/README.md) <br>
- [Infrastructure & Uptime Monitoring Skill Spec](artifact/infra-monitoring-spec.md) <br>
- [Alert Severity Classification System](artifact/references/alert-severity.md) <br>
- [Infrastructure Metrics Thresholds Reference](artifact/references/metrics-thresholds.md) <br>
- [Monitoring Checklists](artifact/references/monitoring-checklists.md) <br>
- [Test Prompts](artifact/references/test-prompts.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance, Configuration] <br>
**Output Format:** [Markdown status reports with tables, prioritized findings, and inline shell commands when useful] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Separates observed metrics from diagnostic inferences and prioritizes items that need attention.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence, README status) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
