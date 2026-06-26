## Description: <br>
Helps agents search pet-friendly flights with the flyai CLI and format real-time flight options with booking links and pet travel reminders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bufferstreamer](https://clawhub.ai/user/bufferstreamer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers and travel-support agents use this skill to find pet-friendly flight options, prioritize direct or shorter trips, and present bookable results with reminders to confirm airline pet policies before purchase. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may direct an agent to install a global npm package for flyai CLI access. <br>
Mitigation: Install only if the flyai package is trusted in the deployment environment, and avoid sudo installation unless explicitly approved. <br>
Risk: The skill can retain travel searches and command history in a local .flyai-execution-log.json file. <br>
Mitigation: Disable, review, or remove the execution log when local retention of travel queries is not acceptable. <br>
Risk: Real-time flight results do not guarantee airline pet cabin, cargo, carrier, or fee eligibility. <br>
Mitigation: Confirm airline pet policies directly before booking and prefer direct flights when available. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/bufferstreamer/pet-flights) <br>
- [Parameter and output templates](references/templates.md) <br>
- [Scenario playbooks](references/playbooks.md) <br>
- [Fallback procedures](references/fallbacks.md) <br>
- [Execution log runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with booking links and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results are expected to come from flyai CLI output and include booking links when flight options are shown.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
