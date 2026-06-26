## Description: <br>
Configure firewalls on servers and cloud providers with security best practices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gonzachee](https://clawhub.ai/user/gonzachee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agents use this skill to reason about firewall rules for servers and cloud providers, including SSH access, default-deny inbound policy, provider firewalls, Docker exposure, IPv6 coverage, and common misconfigurations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Incorrect firewall guidance or unreviewed rule changes can block SSH or remote administration access, especially on remote servers. <br>
Mitigation: Require explicit user confirmation before applying firewall changes, allow remote access first, test from a second session, and confirm provider-console recovery access. <br>
Risk: The registry listing and package metadata do not fully match, which can reduce confidence that the displayed release and packaged artifact describe the same state. <br>
Mitigation: Confirm the publisher and release metadata before installation, and treat the skill as guidance rather than executable authority. <br>
Risk: Docker, IPv6, or provider-level firewall behavior can differ from host firewall assumptions and leave services unexpectedly exposed. <br>
Mitigation: Review provider, host, Docker, and IPv6 rules together; verify exposure from outside the network before relying on the configuration. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown firewall guidance and configuration considerations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only; does not include executable code, automation, hidden telemetry, persistence, or credential requirements.] <br>

## Skill Version(s): <br>
1.0.1 (source: target metadata and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
