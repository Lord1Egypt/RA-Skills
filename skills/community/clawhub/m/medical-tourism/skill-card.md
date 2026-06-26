## Description: <br>
Book flights for medical tourism, health checkups, and overseas treatment using the flyai CLI, with support for related travel booking tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bufferstreamer](https://clawhub.ai/user/bufferstreamer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to search medical tourism flights and related travel options through real-time flyai CLI results. It helps agents collect route parameters, run approved CLI searches, and return Markdown booking options with links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill instructs an agent to install and run an external flyai CLI. <br>
Mitigation: Require explicit user approval before installation, verify the package source and version, and review the skill before deployment. <br>
Risk: Booking links lead to third-party travel services. <br>
Mitigation: Treat returned booking links as external service links and have users review destination, price, and provider details before booking. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/bufferstreamer/medical-tourism) <br>
- [Parameter Collection and Output Templates](references/templates.md) <br>
- [Scenario Playbooks](references/playbooks.md) <br>
- [Failure Recovery](references/fallbacks.md) <br>
- [Execution Runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with booking links and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Flight result tables must be based on flyai CLI output and include detailUrl booking links.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
