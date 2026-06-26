## Description: <br>
Finds hotels that welcome pets, including pet policies, nearby parks, pet-friendly room options, and related travel services powered by Fliggy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers and travel-support agents use this skill to search for pet-friendly lodging, collect required trip parameters, run flyai hotel-search commands, and return bookable hotel options with current details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs installation and use of a global npm CLI dependency. <br>
Mitigation: Vet @fly-ai/flyai-cli before installation and prefer a managed or isolated environment for execution. <br>
Risk: Booking-link travel results can influence purchases or reservations. <br>
Mitigation: Require user review and confirmation before any purchase, booking, or external checkout step. <br>
Risk: The runbook describes local logging of raw travel queries when file writes are available. <br>
Mitigation: Disable, remove, or sanitize execution logging unless local retention of travel queries is intended. <br>


## Reference(s): <br>
- [ClawHub Pet Hotel release page](https://clawhub.ai/xiejinsong/pet-hotel) <br>
- [Parameter and output templates](artifact/references/templates.md) <br>
- [Pet-hotel playbooks](artifact/references/playbooks.md) <br>
- [Hotel fallback guidance](artifact/references/fallbacks.md) <br>
- [Execution log schema](artifact/references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with booking links, comparison tables, and inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires flyai CLI output for travel results and should include booking links when results are shown.] <br>

## Skill Version(s): <br>
3.2.1 (source: server release metadata; artifact frontmatter is 3.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
