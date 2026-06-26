## Description: <br>
Self-hosted infrastructure monitoring for HTTP and HTTPS endpoints, TCP services, Docker containers, system resources, SSL certificate expiry, DNS checks, and alerting channels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mariusfit](https://clawhub.ai/user/mariusfit) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and infrastructure operators use this skill to configure and run local health checks for self-hosted services, containers, hosts, certificates, and network dependencies. It helps surface uptime and resource issues through status views and configured chat alerts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: HTTPS checks are reported to disable certificate verification. <br>
Mitigation: Review or patch HTTPS monitoring so certificate validation is enabled by default, and allow disabled verification only for explicitly approved self-signed internal endpoints. <br>
Risk: Alerts can disclose infrastructure names, targets, or status details to third-party chat services. <br>
Mitigation: Disable third-party alert channels unless needed, and avoid sensitive hostnames, secrets, customer names, or internal identifiers in monitor names and URLs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mariusfit/infra-watchdog) <br>
- [Publisher profile](https://clawhub.ai/user/mariusfit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text with command examples and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local monitor configuration, SQLite state, status output, and alert messages when installed and run.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
