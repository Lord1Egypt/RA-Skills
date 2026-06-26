## Description: <br>
OpenAlex (openalex.org). Use this skill for ANY OpenAlex request - searching and reading data. Whenever a task involves OpenAlex, use this skill instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to search and read OpenAlex data through OOMOL's OpenAlex connector and the oo CLI, including autocomplete, entity lookup, work lookup, and list or group queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires OOMOL-mediated OpenAlex access and may use connected credentials or scopes. <br>
Mitigation: Connect only the OpenAlex credentials and scopes intended for this skill, and review OOMOL access before use. <br>
Risk: Fallback setup includes remote installer commands for the oo CLI. <br>
Mitigation: Review OOMOL's official install instructions or installer contents before running remote installer commands. <br>
Risk: Connector schemas may change over time, which can make stale payloads fail or behave unexpectedly. <br>
Mitigation: Fetch the live action schema with `oo connector schema` before constructing each action payload. <br>


## Reference(s): <br>
- [OpenAlex homepage](https://openalex.org/) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before action execution and returns connector responses as JSON.] <br>

## Skill Version(s): <br>
1.0.1 (source: evidence release version and SKILL.md metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
