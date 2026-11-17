## Description:

Monitor server health, uptime, resource utilization, SSL certificate expiry, and incident detection for small teams and self-hosters. Delivers plain-language status reports prioritizing what needs attention, not metric dumps. Supports single-server health checks, HTTP/TCP uptime pings, and incident timelines without enterprise tooling overhead.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gitcanadabrett](https://clawhub.ai/user/gitcanadabrett)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, small operations teams, self-hosters, and solo SaaS operators use this skill to assess server health, endpoint uptime, SSL certificate status, incident signals, and capacity concerns without enterprise monitoring overhead.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make user-directed endpoint checks that may target private, internal, or unauthorized systems.

Mitigation: Use agent runtime network controls, require public or authorized targets, and reject localhost, private, link-local, and metadata address ranges before broad use.

Risk: Endpoint checks could follow redirects or inspect response data in ways that expose sensitive systems or content.

Mitigation: Validate redirects, limit allowed ports and response data, and avoid forwarding credentials or sensitive response bodies.

Risk: Monitoring output may include credentials, PII, or sensitive server response details if raw inputs contain them.

Mitigation: Exclude credentials and PII from reports, reference secret managers or environment variables instead of writing secrets, and summarize sensitive responses rather than reproducing them.

Risk: Operational diagnosis and remediation guidance can be wrong or harmful if treated as an automated fix.

Mitigation: Keep remediation as reviewed guidance, separate observed facts from interpretations, and require user approval before any action that changes infrastructure.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gitcanadabrett/skills/infra-monitoring)
- [Infrastructure Metrics Thresholds](references/metrics-thresholds.md)
- [Alert Severity Classification System](references/alert-severity.md)
- [Monitoring Checklists](references/monitoring-checklists.md)
- [Test Prompts](references/test-prompts.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown status report with tables and inline shell commands when useful]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include severity labels, endpoint status, SSL expiry, incident timelines, observed facts, interpretations, and prioritized next steps.]

## Skill Version(s):

0.1.0 (source: release evidence and README)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
