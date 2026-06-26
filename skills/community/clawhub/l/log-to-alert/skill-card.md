## Description: <br>
Log To Alert helps agents turn recurring server, application, or system log errors and warnings into structured alert-rule drafts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangjipeng977](https://clawhub.ai/user/wangjipeng977) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, site reliability engineers, and operations teams use this skill to convert user-provided logs into alert-rule drafts for monitoring systems such as Prometheus, Grafana, or PagerDuty. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Logs may contain API keys, tokens, cookies, session IDs, customer data, internal hostnames, or other sensitive operational details. <br>
Mitigation: Redact sensitive values before pasting logs or providing file paths. <br>
Risk: Generated alert-rule drafts may be too broad, duplicated, or noisy if log patterns are not reviewed. <br>
Mitigation: Review each draft rule for unique names, specific regex patterns, appropriate severity, and thresholds above one occurrence before deploying it. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wangjipeng977/log-to-alert) <br>
- [Reference Index](references/index.md) <br>
- [Metadata Source](https://github.com/MiniMax-AI/skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown with YAML, JSON, or regex alert-rule snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Drafts rules only; does not deploy, persist data, or contact external systems.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter reports 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
