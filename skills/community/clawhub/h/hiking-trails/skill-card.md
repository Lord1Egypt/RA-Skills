## Description: <br>
Find hiking trails from easy walks to challenging mountain treks, including difficulty levels, elevation, duration, packing guidance, and FlyAI/Fliggy-backed booking results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel agents use this skill to find hiking trails, mountain treks, and easy walks from live FlyAI/Fliggy travel search results. It collects location parameters, runs flyai CLI commands, and formats bookable trail or attraction results in the user's language. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install and run a global flyai CLI before producing travel results. <br>
Mitigation: Install and review @fly-ai/flyai-cli yourself before using the skill, and run only the expected flyai commands for travel search. <br>
Risk: The skill may persist raw travel queries in .flyai-execution-log.json when filesystem writes are available. <br>
Mitigation: Avoid entering sensitive itinerary or identity details, and delete or disable .flyai-execution-log.json if local query history should not be retained. <br>
Risk: Travel recommendations can be stale or misleading if generated without live FlyAI results. <br>
Mitigation: Require responses to come from flyai CLI output and include Book links from detailUrl for listed results. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xiejinsong/hiking-trails) <br>
- [Publisher Profile](https://clawhub.ai/user/xiejinsong) <br>
- [Parent FlyAI Skill](https://github.com/alibaba-flyai/flyai-skill/tree/main/skills/flyai) <br>
- [templates.md](references/templates.md) <br>
- [playbooks.md](references/playbooks.md) <br>
- [fallbacks.md](references/fallbacks.md) <br>
- [runbook.md](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with comparison tables, booking links, concise guidance, and inline shell commands when setup or retry steps are needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should be based on flyai CLI results, include Book links from detailUrl when results are shown, and avoid raw JSON.] <br>

## Skill Version(s): <br>
3.2.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
