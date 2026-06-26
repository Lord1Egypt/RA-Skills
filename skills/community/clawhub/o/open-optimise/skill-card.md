## Description: <br>
Cost Optimizer helps OpenClaw users reduce API costs through model routing, session management, output efficiency, free-model setup, and monitoring scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rajdeep09-dev](https://clawhub.ai/user/rajdeep09-dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to audit agent API spending, route work to lower-cost models, apply budget presets, and monitor ongoing cost trends. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Some helper scripts unsafely execute local configuration files as code. <br>
Mitigation: Review before installing, run scripts only against trusted configuration files, and replace dynamic config execution with safe JSON or JSON5 parsing. <br>
Risk: Reporting and automation features may expose sensitive configuration or usage data if enabled without review. <br>
Mitigation: Treat instances.json and API keys as secrets, avoid plaintext HTTP provider or instance URLs, and review webhook and cron templates before enabling them. <br>


## Reference(s): <br>
- [Model Tier Reference Card](references/model-tiers.md) <br>
- [Configuration Templates](references/setup-config.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes optional script-generated reports, dashboards, backups, and preset configuration files.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
