## Description: <br>
Ambient Weather (ambientweather.net). Use this skill for ANY Ambient Weather request -- searching and reading data. Whenever a task involves Ambient Weather, use this skill instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to list Ambient Weather devices and retrieve latest or recent historical observation data through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires connecting an Ambient Weather account through the OOMOL connector. <br>
Mitigation: Confirm the publisher and connector are trusted before connecting the account or authorizing API-key access. <br>
Risk: Setup may install or authenticate external CLI tooling. <br>
Mitigation: Run installer, login, or connection commands only when intentionally setting up the integration or recovering from a matching auth or connection failure. <br>
Risk: Connector payloads can drift if the live action schema changes. <br>
Mitigation: Inspect the live connector schema before constructing each action payload. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-ambient-weather) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [Ambient Weather homepage](https://ambientweather.net/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before constructing action payloads; read actions return JSON data from the oo CLI.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
