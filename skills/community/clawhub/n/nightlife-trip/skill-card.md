## Description: <br>
Book flights for nightlife trips featuring night markets and entertainment districts, with support for related travel planning tasks such as hotels, train tickets, attractions, visas, insurance, and car rental. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travel agents and end users use this skill to search live flight options for nightlife-focused trips, compare routes by recommendation, price, duration, or directness, and return booking links in the user's language. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill instructs agents to install @fly-ai/flyai-cli globally when flyai is missing. <br>
Mitigation: Require explicit user approval before persistent global installation, verify the package source, and prefer an isolated or user-local install. <br>
Risk: Live travel searches send route, date, and preference details to the flyai service. <br>
Mitigation: Use the skill only when the user accepts that disclosure and avoid sending sensitive personal details that are not needed for the search. <br>
Risk: Security evidence flags overbroad and inconsistent command guidance. <br>
Mitigation: Use only documented CLI parameters, ask for clarification when required values are missing, and do not fabricate travel results if the CLI fails. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/xiejinsong/nightlife-trip) <br>
- [Parameter collection and output templates](references/templates.md) <br>
- [Scenario playbooks](references/playbooks.md) <br>
- [Failure recovery](references/fallbacks.md) <br>
- [Execution runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with comparison tables, booking links, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live flyai CLI output and requires booking links from detailUrl for included flight results.] <br>

## Skill Version(s): <br>
3.2.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
