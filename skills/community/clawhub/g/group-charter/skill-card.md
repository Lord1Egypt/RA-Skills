## Description: <br>
Search for group charter flight options and private group aviation, with related travel search support for flights, hotels, trains, attractions, itinerary planning, visa information, travel insurance, and car rental powered by Fliggy (Alibaba Group). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers, travel planners, and agents use this skill to collect route and date details, execute flyai CLI searches, and return Markdown flight comparisons with booking links for group charter or private group flight requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill instructs the agent to install a third-party flyai CLI package globally if it is missing. <br>
Mitigation: Review and approve the CLI package before installation, and run it only in an environment where global npm installs are acceptable. <br>
Risk: Travel details such as cities, dates, and preferences may be sent to the live search provider. <br>
Mitigation: Avoid entering sensitive travel details unless sharing them with the provider is acceptable for the user and organization. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dingtom336-gif/group-charter) <br>
- [Parameter Collection & Output Templates](references/templates.md) <br>
- [Scenario Playbooks](references/playbooks.md) <br>
- [Failure Recovery](references/fallbacks.md) <br>
- [Execution Runbook](references/runbook.md) <br>
- [Node.js](https://nodejs.org/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with flight comparison tables, booking links, and inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses flyai CLI output as the required data source and includes booking links when results are returned.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
