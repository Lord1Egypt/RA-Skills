## Description: <br>
Book last minute flights, same-day tickets and urgent departures with emergency travel options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[palexu](https://clawhub.ai/user/palexu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers and travel-support agents use this skill to find urgent same-day or near-term flights through the flyai CLI, then present real-time options with booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks agents to install or use a global flyai CLI package. <br>
Mitigation: Review the package before installation and require explicit approval for global or sudo-level changes. <br>
Risk: Travel searches may involve sensitive personal or emergency travel details that could be sent to a provider or retained in a local log. <br>
Mitigation: Avoid entering sensitive personal details unless the user understands and accepts provider transmission and possible local logging. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/palexu/last-minute) <br>
- [Fallbacks](references/fallbacks.md) <br>
- [Playbooks](references/playbooks.md) <br>
- [Runbook](references/runbook.md) <br>
- [Templates](references/templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with flight result tables, booking links, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires live flyai CLI results; every listed flight should include a Book link from detailUrl.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
