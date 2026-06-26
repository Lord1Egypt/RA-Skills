## Description: <br>
Helps agents search and format real-time island and beach flight options with booking links using flyai/Fliggy CLI results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers and travel-planning agents use this skill to collect island flight parameters, run flyai searches, and present real-time route options with booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can ask the agent to install a global npm CLI, with fallback guidance that may use sudo. <br>
Mitigation: Require explicit user confirmation before installation, avoid sudo where possible, and pin the CLI version before use. <br>
Risk: Travel search details may be sent to flyai/Fliggy-backed services when the CLI is used. <br>
Mitigation: Tell users before sending trip details to the service and avoid submitting sensitive travel information unless they approve. <br>
Risk: The skill describes local execution logs that can include raw travel queries. <br>
Mitigation: Disable logging where possible, or redact and remove .flyai-execution-log.json after use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dingtom336-gif/island-flight) <br>
- [Templates - island-flight](references/templates.md) <br>
- [Playbooks - island-flight](references/playbooks.md) <br>
- [Fallbacks - Flight Category (Island Flight)](references/fallbacks.md) <br>
- [Runbook - Execution Log Schema](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with booking links and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires live flyai CLI output and detailUrl booking links for each result.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
