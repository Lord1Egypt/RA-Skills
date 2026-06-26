## Description: <br>
Aggregates and filters webhook alerts from multiple sources, correlates incidents by host, and escalates critical events via Telegram with rate limiting and buffering guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mbojer](https://clawhub.ai/user/mbojer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill as an architecture and runbook reference for designing an alert gateway that receives monitoring webhooks, stores raw alerts, correlates incidents, and escalates critical events. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact is an architecture and runbook, not a ready-to-run monitoring integration. <br>
Mitigation: Review and implement the gateway components deliberately before relying on it for production alert handling. <br>
Risk: Future implementations may close incidents, change rules, or suppress alerts in ways that affect operations. <br>
Mitigation: Require explicit confirmation or authorization before closing incidents, changing rules, or enabling suppression behavior. <br>
Risk: The planned gateway depends on sensitive database, webhook, and Telegram credentials. <br>
Mitigation: Restrict credential access, protect local cache and buffer files, and review retention for raw alert data before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mbojer/noise-maker) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with architecture notes, schemas, configuration examples, and implementation steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Planning document; not runnable code.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
