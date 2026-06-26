## Description: <br>
Search for military leave flights with armed forces travel options, plus related travel booking tasks such as hotels, trains, attraction tickets, itinerary planning, visa information, travel insurance, and car rental through flyai. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers and agents use this skill to collect route, date, budget, and preference details, run flyai travel-search commands, and return booking-focused Markdown results for military leave and related travel needs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill instructs agents to install an unpinned global npm CLI when flyai is missing. <br>
Mitigation: Review and approve the install first; prefer a pinned @fly-ai/flyai-cli version in an isolated environment. <br>
Risk: Route, date, and travel preferences may be sent to the travel provider used by the CLI. <br>
Mitigation: Use the skill only when sharing those travel details with the provider is acceptable. <br>
Risk: The skill can activate too broadly for travel-related requests. <br>
Mitigation: Limit use to explicit military leave, armed forces travel, or related booking requests and review commands before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiejinsong/military-leave) <br>
- [Parameter Collection & Output Templates](references/templates.md) <br>
- [Scenario Playbooks](references/playbooks.md) <br>
- [Failure Recovery](references/fallbacks.md) <br>
- [Execution Runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown travel search summaries with booking links and inline shell commands when command execution is needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results should be based on flyai CLI output, include detailUrl booking links, and avoid raw JSON.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
