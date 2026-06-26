## Description: <br>
Book graduation trip flights, post-grad travel, and class trip booking with student fare deals, with support for flight booking, hotels, train tickets, attraction tickets, itinerary planning, visa information, travel insurance, car rental, and related Fliggy-powered travel services. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and SKILL.md-compatible agents use this skill to collect graduation travel parameters, run the flyai CLI for real-time travel results, and return booking-linked comparison tables and travel guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can require a global flyai CLI installation. <br>
Mitigation: Review and trust the @fly-ai/flyai-cli package and the Fliggy/flyai provider before installation; prefer a controlled environment for execution. <br>
Risk: Local execution logs can retain raw travel queries. <br>
Mitigation: Avoid entering passport, payment, or highly sensitive identity details unless required, and review or delete .flyai-execution-log.json when local query retention is not desired. <br>


## Reference(s): <br>
- [Skill release page](https://clawhub.ai/dingtom336-gif/graduation) <br>
- [Templates - graduation](references/templates.md) <br>
- [Playbooks - graduation](references/playbooks.md) <br>
- [Fallbacks - Flight Category (Graduation)](references/fallbacks.md) <br>
- [Runbook - Execution Log Schema (Universal)](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown responses with booking links, comparison tables, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires travel results from flyai CLI output; each booking option must include a detailUrl-based Book link.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
