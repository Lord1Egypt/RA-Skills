## Description: <br>
Packing List helps agents generate customized travel packing lists based on destination, season, trip type, and activities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel assistants use this skill to collect trip details and return concise Markdown packing guidance for destinations, seasons, trip types, and activities. The artifact also directs agents to use FlyAI/Fliggy-backed command output for booking-linked travel results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can trigger global installation and execution of a travel CLI. <br>
Mitigation: Require explicit user approval before running npm install commands or FlyAI CLI commands. <br>
Risk: The workflow may retain raw travel queries in a local execution log. <br>
Mitigation: Disable or delete `.flyai-execution-log.json` when local query history should not be retained. <br>
Risk: Travel searches and booking links may involve sensitive itinerary or booking information. <br>
Mitigation: Avoid entering passport, payment, booking-reference, or highly sensitive itinerary details. <br>


## Reference(s): <br>
- [Packing List ClawHub Release](https://clawhub.ai/xiejinsong/packing-list) <br>
- [Skill Definition](artifact/SKILL.md) <br>
- [Templates](artifact/references/templates.md) <br>
- [Playbooks](artifact/references/playbooks.md) <br>
- [Fallbacks](artifact/references/fallbacks.md) <br>
- [Runbook](artifact/references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and booking links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Follows the user's language and expects booking-linked results when FlyAI data is available.] <br>

## Skill Version(s): <br>
3.2.1 (source: server release metadata; artifact frontmatter says 3.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
