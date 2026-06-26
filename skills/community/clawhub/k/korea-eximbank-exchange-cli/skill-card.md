## Description: <br>
Korea Eximbank OpenAPI exchange-rate lookup CLI for AP01, AP02, and AP12 tables with date and currency filters and JSON or CSV output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chloepark85](https://clawhub.ai/user/chloepark85) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and finance operations users use this skill to configure and run a CLI that fetches Korea Eximbank exchange-rate data for a selected date, table, output format, and optional currency filter. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Korea Eximbank API key. <br>
Mitigation: Use a dedicated API key stored in KOREAEXIM_API_KEY and avoid sharing it in prompts, logs, or screenshots. <br>
Risk: The submitted artifact contains only the skill definition, so package implementation details are not available in the evidence. <br>
Mitigation: Confirm the intended repository and inspect the actual package files before installing or deploying the CLI. <br>
Risk: Exchange-rate responses may be empty on non-business days or constrained by API limits. <br>
Mitigation: Handle empty API responses and review the API msg field when requests fail. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chloepark85/korea-eximbank-exchange-cli) <br>
- [Publisher profile](https://clawhub.ai/user/chloepark85) <br>
- [Korea Eximbank exchangeJSON API](https://www.koreaexim.go.kr/site/program/financial/exchangeJSON) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON, CSV] <br>
**Output Format:** [Markdown with inline shell commands and CLI output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires KOREAEXIM_API_KEY in the environment.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
