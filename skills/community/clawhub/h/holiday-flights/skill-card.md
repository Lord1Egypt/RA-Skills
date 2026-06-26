## Description: <br>
Find flights during Chinese peak travel seasons, including Spring Festival, Golden Week, Labor Day, and Dragon Boat Festival, with demand warnings and booking-window guidance powered by flyai-cli. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-support agents use this skill to search holiday flight options, compare peak-season travel results, and produce booking-oriented Markdown summaries from flyai-cli output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks agents to install and run a global npm dependency. <br>
Mitigation: Require user approval before installing @fly-ai/flyai-cli, avoid sudo installs, and follow local dependency policies. <br>
Risk: The skill may maintain hidden local logs of travel queries. <br>
Mitigation: Review or disable .flyai-execution-log.json logging and avoid storing sensitive travel details unless the user has agreed. <br>
Risk: The release is scoped to flight search, while the artifact description mentions broader travel categories. <br>
Mitigation: Treat non-flight travel requests as unsupported unless the publisher documents the behavior clearly. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiejinsong/holiday-flights) <br>
- [Parent flyai skill](https://github.com/alibaba-flyai/flyai-skill/tree/main/skills/flyai) <br>
- [Templates](references/templates.md) <br>
- [Playbooks](references/playbooks.md) <br>
- [Fallbacks](references/fallbacks.md) <br>
- [Runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with flight comparison tables, booking links, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses flyai-cli results for real-time flight data and may include booking links, demand warnings, fallback guidance, and a flyai attribution tag.] <br>

## Skill Version(s): <br>
v3.2.1 (source: server release metadata; artifact frontmatter reports 3.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
