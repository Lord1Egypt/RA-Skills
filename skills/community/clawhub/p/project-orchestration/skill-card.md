## Description: <br>
Complete project orchestration: model routing, coding workflow, scripts, session logging, decision tracking, price checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[genortg](https://clawhub.ai/user/genortg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to coordinate AI-assisted project work, including model inventory, routing choices, project onboarding, session logging, architecture decision records, price checks, and dashboard-based status review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent project and session logs can capture sensitive project details, model choices, or user notes. <br>
Mitigation: Set a dedicated ORCHESTRATOR_DATA_DIR and avoid logging secrets, tokens, credentials, or full connection strings. <br>
Risk: Project discovery and onboarding may inspect or write files in local project directories. <br>
Mitigation: Approve discovery and onboarding one path at a time, and review generated .planning files before relying on them. <br>
Risk: Provider discovery, model checks, and price checks can make outbound network requests and may be scheduled repeatedly if cron is enabled. <br>
Mitigation: Run network checks only for approved providers and enable cron only when recurring checks are expected. <br>
Risk: The dashboard is unauthenticated and the bundled server binds to all network interfaces. <br>
Mitigation: Run the dashboard only on trusted networks, protect it with local firewall rules, or change the server to bind to localhost before use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/genortg/project-orchestration) <br>
- [Package Homepage](https://clawhub.com/packages/project-orchestration) <br>
- [README](README.md) <br>
- [Model Routing Table Template](ROUTING.md) <br>
- [OpenRouter Models API](https://openrouter.ai/api/v1/models) <br>
- [OpenRouter Pricing](https://openrouter.ai/pricing) <br>
- [OpenCode Pricing](https://opencode.ai/pricing) <br>
- [Cursor Pricing](https://cursor.com/pricing) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, generated project files, JSON configuration, and dashboard status data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write persistent orchestration data, project planning files, session logs, decision records, model inventories, and price-check logs under the configured data directory or selected project paths.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
