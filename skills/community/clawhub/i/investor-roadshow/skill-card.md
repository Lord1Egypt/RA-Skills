## Description: <br>
Book flights for investor roadshows and IPO fundraising travel, with supporting workflows for related travel services through the flyai CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to search investor-roadshow and fundraising travel options, format flight results, and provide booking links from live flyai CLI output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may install an unpinned global flyai CLI package. <br>
Mitigation: Preinstall a reviewed, pinned flyai CLI version before enabling the skill, and avoid allowing automatic global installs in restricted environments. <br>
Risk: Investor-roadshow routes and itinerary details may be sent to an external travel provider. <br>
Mitigation: Use only with provider-approved data, and avoid confidential itinerary details unless the travel provider is acceptable for that data. <br>
Risk: Broad travel requests may trigger the skill outside the intended investor-roadshow workflow. <br>
Mitigation: Confirm user intent and required route parameters before running searches or presenting booking options. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dingtom336-gif/investor-roadshow) <br>
- [Parameter collection and output templates](references/templates.md) <br>
- [Scenario playbooks](references/playbooks.md) <br>
- [Failure recovery](references/fallbacks.md) <br>
- [Execution runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, markdown, guidance] <br>
**Output Format:** [Markdown with booking links and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires live flyai CLI results; booking results must include detailUrl links.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
