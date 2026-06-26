## Description: <br>
Find overnight and late-night departure flights, with support for flight booking, hotel reservation, train tickets, attraction tickets, itinerary planning, visa information, travel insurance, car rental, and related travel tasks powered by Fliggy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel agents use this skill to search for late-night or overnight travel options, compare cheaper night departures, and format real-time booking results from the flyai CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may prompt installation of the flyai npm package and make broad local environment changes. <br>
Mitigation: Require explicit user approval before installation, avoid sudo or automatic global installs unless approved, and review the package source and permissions before use. <br>
Risk: Travel searches and command history may expose raw itinerary or personal travel details. <br>
Mitigation: Avoid entering sensitive personal data unless necessary, limit local logging, and clear generated logs or shell history when appropriate. <br>
Risk: The skill depends on the external flyai/Fliggy service for real-time travel data and booking links. <br>
Mitigation: Use it only when the user trusts the service, and present failures or missing results honestly rather than substituting unsourced travel information. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiejinsong/overnight-flights) <br>
- [Output templates](references/templates.md) <br>
- [Scenario playbooks](references/playbooks.md) <br>
- [Fallback guidance](references/fallbacks.md) <br>
- [Execution runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with booking links and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Travel results must come from flyai CLI output and include booking links when results are shown.] <br>

## Skill Version(s): <br>
3.2.1 (source: server release metadata; artifact frontmatter states 3.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
