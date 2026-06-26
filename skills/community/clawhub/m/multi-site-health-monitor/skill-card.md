## Description: <br>
Monitor dozens of websites with configurable health checks, auto-restart alerts, and intelligent alert routing. Use when the user needs uptime tracking, performance monitoring, or automated incident response across multiple domains. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ncreighton](https://clawhub.ai/user/ncreighton) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use this skill to plan multi-site uptime checks, performance monitoring, certificate checks, WordPress health checks, alert routing, and incident response workflows across production services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill describes automated production restarts, rollbacks, SSH commands, and scaling actions that can change live infrastructure. <br>
Mitigation: Start in alert-only mode and require explicit human approval before SSH, restart, scaling, rollback, or other infrastructure-changing actions. <br>
Risk: The skill relies on operational credentials for alerting and monitoring services. <br>
Mitigation: Use least-privilege tokens, rotate credentials, store secrets outside prompts and logs, and avoid logging full response bodies or secret-bearing headers. <br>
Risk: The skill can route incidents, metrics, and logs to broad third-party destinations. <br>
Mitigation: Restrict allowed destinations, review what data is sent to each integration, and limit outbound reporting to approved channels. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ncreighton/multi-site-health-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with YAML configuration examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and jq; uses Slack, PagerDuty, and Datadog credentials when those integrations are enabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
