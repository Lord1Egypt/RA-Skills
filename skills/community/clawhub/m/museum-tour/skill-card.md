## Description: <br>
Find museums, art galleries, and exhibitions in any city, with ticket links and visiting tips powered by Fliggy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to search for museums, galleries, exhibitions, and related travel options, then receive concise Markdown results with booking links and visit guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks agents to install and run an unpinned global flyai CLI. <br>
Mitigation: Use manual approval for installation and pin or verify the package where possible before execution. <br>
Risk: Travel-search details may be sent to the flyai or Fliggy provider. <br>
Mitigation: Avoid entering sensitive personal or booking information unless the provider is trusted for the intended use. <br>
Risk: The artifact describes persisting raw user queries in a local .flyai-execution-log.json file. <br>
Mitigation: Manage, disable, or remove the local log file and avoid storing sensitive request details. <br>


## Reference(s): <br>
- [templates.md](references/templates.md) <br>
- [playbooks.md](references/playbooks.md) <br>
- [fallbacks.md](references/fallbacks.md) <br>
- [runbook.md](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with booking links and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires flyai CLI output for travel data and should not include raw JSON.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
