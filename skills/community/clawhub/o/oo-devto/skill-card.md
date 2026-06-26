## Description: <br>
Dev.to (dev.to). Use this skill for ANY Dev.to request - reading, creating, and updating data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content operators use this skill to read Dev.to content and manage authenticated Dev.to articles through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an authenticated OOMOL-connected Dev.to account and can use credentials indirectly. <br>
Mitigation: Use it only with accounts intended for Dev.to operations, and reconnect or refresh credentials only when the connector reports an authentication or connection error. <br>
Risk: Write actions can create or update Dev.to articles. <br>
Mitigation: Confirm the exact payload and expected publishing effect with the user before running write actions. <br>
Risk: Connector input schemas may change over time. <br>
Mitigation: Inspect the live connector schema before constructing each action payload. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/oomol/oo-devto) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [Dev.to Homepage](https://dev.to) <br>
- [OOMOL CLI Install Guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return Dev.to connector responses as JSON when actions are run with the oo CLI.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
