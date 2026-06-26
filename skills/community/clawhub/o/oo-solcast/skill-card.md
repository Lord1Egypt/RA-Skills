## Description: <br>
Solcast helps agents inspect connector schemas and retrieve Solcast irradiance and weather forecast, historic, and live estimated actuals data through an OOMOL-connected account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and operations teams use this skill to query Solcast solar irradiance and weather data by location through OOMOL's Solcast connector without handling raw API tokens. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an OOMOL-connected Solcast account and may fail or expose workflow friction if the oo CLI is not installed, the user is not signed in, or the Solcast connection is missing or expired. <br>
Mitigation: Install only when comfortable using OOMOL's oo CLI with a connected Solcast account, and follow the skill's first-time setup guidance only after an auth or connection error occurs. <br>
Risk: The setup path includes remote installer commands for the oo CLI. <br>
Mitigation: Review the oo CLI installer before running the remote install command, as recommended by the server security guidance. <br>


## Reference(s): <br>
- [Solcast homepage](https://solcast.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector calls return JSON data and execution metadata when run with the oo CLI.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
