## Description: <br>
Calendarific (calendarific.com). Use this skill for any Calendarific request, including searching and reading holiday, country, and language data through the OOMOL connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query Calendarific holiday data, supported countries, and supported languages through an OOMOL-connected Calendarific account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on the OOMOL oo CLI and includes remote installer commands for first-time setup. <br>
Mitigation: Review the official OOMOL CLI install guide or installer source before running setup commands, and run them only when the CLI is missing. <br>
Risk: Calendarific access requires sensitive credentials through an OOMOL-connected account. <br>
Mitigation: Use the expected OOMOL connection flow and avoid sharing raw Calendarific API keys directly with the agent or command payloads. <br>
Risk: Connector schemas can change over time, which can make hard-coded payloads incorrect. <br>
Mitigation: Fetch the live action schema with `oo connector schema` before constructing each connector payload. <br>


## Reference(s): <br>
- [Calendarific homepage](https://calendarific.com/) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [Calendarific skill page](https://clawhub.ai/oomol/oo-calendarific) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return Calendarific connector responses as JSON through the oo CLI.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
