## Description: <br>
IPGeolocation.io (ipgeolocation.io). Use this skill for ANY IPGeolocation.io request - searching and reading data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to run IPGeolocation.io lookup, astronomy, and timezone actions through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive IPGeolocation.io credentials through the OOMOL connection. <br>
Mitigation: Use it only with a trusted OOMOL account and connected IPGeolocation.io API key, and avoid exposing raw credentials in prompts or files. <br>
Risk: First-time setup can install or authenticate the OOMOL oo CLI. <br>
Mitigation: Run installer or login commands only when setup errors require them and only after trusting the OOMOL CLI source. <br>
Risk: Live connector schemas can change over time. <br>
Mitigation: Inspect the action schema with the oo CLI before building each payload. <br>


## Reference(s): <br>
- [IPGeolocation.io homepage](https://ipgeolocation.io/) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, API Calls, JSON, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the OOMOL oo CLI connector and returns action responses as JSON with data and meta.executionId fields.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
