## Description: <br>
Lets an agent query Insentek IoT device data with natural language, including real-time readings, historical data, trend analysis, cross-device comparison, and data export. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xddcode](https://clawhub.ai/user/xddcode) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and operators with Insentek-connected IoT devices use this skill to retrieve device status, inspect historical trends, compare devices, detect anomalies, and export reports without handling raw API calls directly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Insentek appid and secret credentials. <br>
Mitigation: Configure credentials only with `npx @insentek/openapi-skill login`; do not paste appid or secret into an agent chat. <br>
Risk: Changing the API base URL can route device-data requests to an unintended endpoint. <br>
Mitigation: Leave `INSENTEK_API_BASE` unset unless the endpoint is controlled and trusted. <br>
Risk: Exports and generated reports can write device data to local files. <br>
Mitigation: Choose output paths deliberately and use dry-run or summarized previews before creating large exports. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xddcode/insentek-api-skill) <br>
- [Getting Started](docs/getting-started.md) <br>
- [Interaction Guide](docs/interaction.md) <br>
- [Analysis Guide](docs/analysis.md) <br>
- [Platform Setup Guide](docs/platform-setup.md) <br>
- [Insentek OpenAPI Reference](reference/api-doc.md) <br>
- [Script Usage](scripts/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Code, Files] <br>
**Output Format:** [Markdown summaries and tables, JSON command output, shell commands, CSV/Excel/JSON exports, and HTML report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Chat output is summarized rather than full raw sensor dumps; file exports and reports may contain device data and should use intentional output paths.] <br>

## Skill Version(s): <br>
1.2.2 (source: server release evidence, SKILL.md frontmatter, skill.json, package.json, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
