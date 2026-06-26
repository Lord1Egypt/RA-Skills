## Description: <br>
Query and export device/site data via the iammeter API (based on https://www.iammeter.com/swaggerui/swagger.json). Triggers: list sites/devices, get real-time or historical energy data, export CSV, run power or offline analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[IAMMETER](https://clawhub.ai/user/IAMMETER) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and energy-monitoring operators use this skill to query IAMMETER sites and devices, retrieve real-time or historical energy data, export CSV history, and run power or offline analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an IAMMETER token that grants access to user energy-monitoring data. <br>
Mitigation: Use a dedicated token, store it only in IAMMETER_TOKEN or the OpenClaw skill configuration, and keep it out of public files. <br>
Risk: CSV export can overwrite the output path supplied by the user. <br>
Mitigation: Choose CSV output paths deliberately and review paths before running export commands. <br>
Risk: The skill depends on short JavaScript files and npm packages for API access. <br>
Mitigation: Review the JavaScript files and dependencies before deployment when higher assurance is required. <br>


## Reference(s): <br>
- [IAMMETER API Reference](references/api.md) <br>
- [IAMMETER Swagger Specification](https://www.iammeter.com/swaggerui/swagger.json) <br>
- [IAMMETER Cloud API Documentation](https://www.iammeter.com/docs/system-api) <br>
- [IAMMETER Device Communication Protocols](https://www.iammeter.com/newsshow/blog-fw-features) <br>
- [ClawHub Skill Page](https://clawhub.ai/IAMMETER/iammeter-openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, code] <br>
**Output Format:** [Markdown guidance with shell commands and optional JSON or CSV command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an IAMMETER token supplied by IAMMETER_TOKEN or the OpenClaw skill configuration.] <br>

## Skill Version(s): <br>
0.2.0 (source: evidence.json release.version and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
