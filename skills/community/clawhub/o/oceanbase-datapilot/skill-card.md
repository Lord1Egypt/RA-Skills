## Description: <br>
DataPilot helps agents connect data sources, answer natural-language data questions, validate SQL, generate charts, export reports, and manage DataAgent knowledge bases through the DataPilot OpenAPI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HSunboy](https://clawhub.ai/user/HSunboy) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and data analysts use this skill to create DataAgent instances for business datasets, ask natural-language data questions, validate SQL, generate charts and reports, and maintain agent knowledge entries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The CLI can persist raw DataPilot credentials in a local log file. <br>
Mitigation: Remove or patch raw-key logging before using live credentials, delete old dataagent_cli.log files, and rotate any DATAPILOT_API_KEY already used with this version. <br>
Risk: Data source credentials and inline datasource JSON may expose sensitive database access details. <br>
Mitigation: Prefer least-privilege read-only datasource credentials and avoid inline datasource JSON containing secrets. <br>
Risk: The skill can create, update, and delete DataAgent resources and knowledge entries. <br>
Mitigation: Manually confirm create, update, and delete actions before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/HSunboy/oceanbase-datapilot) <br>
- [Publisher profile](https://clawhub.ai/user/HSunboy) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Markdown, JSON, Files, Guidance] <br>
**Output Format:** [Markdown and JSON command results, with DataPilot API requests and downloadable report links when available] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js plus DATAPILOT_API_URL and DATAPILOT_API_KEY configuration.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
