## Description: <br>
Lets agents query Insentek / E-Ecology IoT device data with natural language, including live readings, historical data, trend analysis, device comparison, and exports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xddcode](https://clawhub.ai/user/xddcode) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate against Insentek IoT accounts from supported agent platforms, resolving devices, querying sensor readings, generating summaries or reports, and exporting data files without exposing API credentials in chat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stored Insentek API credentials can be sent to a configured API base URL. <br>
Mitigation: Use only the default Insentek endpoint or a trusted test/self-hosted endpoint; do not set INSENTEK_API_BASE or --api-base to an untrusted host. <br>
Risk: Sensitive appid and secret values may be exposed if handled through chat or command-line flags. <br>
Mitigation: Use the interactive login flow, avoid sharing credentials in conversation, and rotate credentials if they may have been exposed. <br>
Risk: Exports and generated reports can write files to user-specified paths. <br>
Mitigation: Review output paths before allowing CSV, Excel, JSON, or HTML writes. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/xddcode/insentek-openapi) <br>
- [README](README.md) <br>
- [Getting Started](docs/getting-started.md) <br>
- [Interaction Guide](docs/interaction.md) <br>
- [Analysis Guide](docs/analysis.md) <br>
- [Insentek OpenAPI Reference](reference/api-doc.md) <br>
- [Insentek OpenAPI endpoint](https://openapi.ecois.info) <br>
- [E-Ecology cloud portal](https://cloud.ecois.info) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, files, guidance] <br>
**Output Format:** [Markdown guidance with bash commands, JSON API responses, and CSV, Excel, JSON, or HTML file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local encrypted credential setup, dry-run previews, row limits, and output-path checks for generated exports and reports.] <br>

## Skill Version(s): <br>
1.2.4 (source: SKILL.md frontmatter, skill.json, CHANGELOG, and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
