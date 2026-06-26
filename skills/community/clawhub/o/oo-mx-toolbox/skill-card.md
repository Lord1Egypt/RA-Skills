## Description: <br>
MxToolbox enables agents to run DNS, mail, HTTP, ping, blacklist, monitor, and usage checks through an OOMOL-connected MxToolbox account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to query MxToolbox diagnostics and account monitor data from an agent workflow without handling raw MxToolbox credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires connected account credentials through OOMOL and can fail or expose account context if used outside the intended ClawHub/OOMOL setup. <br>
Mitigation: Use it only in the intended ClawHub/OOMOL context, rely on server-side credentials, and follow the setup flow only after an authentication or connection error. <br>
Risk: Incorrect connector payloads can produce failed or misleading MxToolbox lookups. <br>
Mitigation: Fetch the live connector schema before each action and build payloads that match the authoritative schema. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-mx-toolbox) <br>
- [Publisher profile](https://clawhub.ai/user/oomol) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector responses are returned as JSON data with execution metadata.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
