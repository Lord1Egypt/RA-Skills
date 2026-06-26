## Description: <br>
Manage Elastic Kibana for observability and security operations, including data views, alerting rules, detection engine rules, Fleet agent policies, cases, and Elastic Security workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, site reliability engineers, and security operations teams use this skill to inspect and manage Kibana observability and security resources through ClawLink-authenticated tool calls. It supports discovery-first workflows for data views, alerting, cases, detection alerts, Fleet policies, Elastic Package Manager data, and selected administrative delete operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access a connected Kibana instance through ClawLink and uses sensitive credentials for authenticated requests. <br>
Mitigation: Install only when the user accepts connecting ClawLink to the target Kibana instance and verify the active integration before making tool calls. <br>
Risk: Delete operations, Fleet configuration changes, connector changes, and detection-rule updates can affect monitoring, security operations, or deployed agents. <br>
Mitigation: Use discovery and preview steps first, then require explicit user confirmation for write or destructive actions before execution. <br>


## Reference(s): <br>
- [Kibana Documentation](https://www.elastic.co/guide/en/kibana/current/index.html) <br>
- [Elastic Fleet Documentation](https://www.elastic.co/guide/en/fleet/current/fleet-overview.html) <br>
- [Elastic Security Solution](https://www.elastic.co/security) <br>
- [ClawLink OpenClaw Documentation](https://docs.claw-link.dev/openclaw) <br>
- [ClawLink Verification](https://claw-link.dev/verify) <br>
- [ClawHub Skill Page](https://clawhub.ai/hith3sh/kibana-observability) <br>
- [Publisher Profile](https://clawhub.ai/user/hith3sh) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown with inline shell commands and tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a connected Kibana instance through ClawLink; write and destructive actions should be previewed and confirmed before execution.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
