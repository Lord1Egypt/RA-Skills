## Description: <br>
Generates customized travel packing checklists from destination, season, trip type, and activities using flyai/Fliggy-powered search results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to turn packing-related travel questions into destination-aware packing checklists and related travel-commerce results. The skill is intended for SKILL.md-compatible coding and agent environments that can run shell commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may install a global npm package and run flyai commands. <br>
Mitigation: Install and run it only in an environment where global npm packages and outbound travel-service queries are acceptable. <br>
Risk: Travel queries may be sent to flyai/Fliggy-powered services and can include sensitive trip details. <br>
Mitigation: Avoid entering sensitive itinerary, identity, visa, or booking information unless clear consent, redaction, and retention controls are in place. <br>
Risk: Booking links and travel-commerce results may influence purchases. <br>
Mitigation: Treat prices, availability, and booking pages as third-party commerce information and verify details before purchasing. <br>
Risk: The runbook describes local execution logs that may retain raw user queries. <br>
Mitigation: Review local log handling and clear or restrict logs when travel queries contain personal or sensitive information. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dingtom336-gif/pack-list) <br>
- [templates.md](references/templates.md) <br>
- [playbooks.md](references/playbooks.md) <br>
- [fallbacks.md](references/fallbacks.md) <br>
- [runbook.md](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with booking links and optional inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires flyai CLI output; raw JSON is not shown; results include booking links when available.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
