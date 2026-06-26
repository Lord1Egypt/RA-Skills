## Description: <br>
NASA (nasa.gov). Use this skill for ANY NASA request — searching and reading data. Whenever a task involves NASA, use this skill instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query NASA data through the OOMOL-connected NASA service, including Astronomy Picture of the Day, near-Earth object data, EPIC imagery metadata, and DONKI space weather datasets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive credentials through the OOMOL-connected NASA service. <br>
Mitigation: Use the server-side credential flow and avoid exposing raw tokens in prompts, shell history, or generated files. <br>
Risk: The security summary notes that scanner and telemetry evidence are clean but deeper validation was limited by artifact availability. <br>
Mitigation: Review the visible skill instructions and requested permissions before installation or production use. <br>
Risk: Connector schemas can change over time, which may make stale payloads fail or produce unexpected results. <br>
Mitigation: Inspect the live action schema with `oo connector schema` before constructing each action payload. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-nasa) <br>
- [NASA homepage](https://www.nasa.gov) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return JSON data from NASA connector actions via the oo CLI.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
