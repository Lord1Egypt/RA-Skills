## Description: <br>
Hire a private car with driver for customized day tours, with support for related travel booking tasks such as flights, hotels, trains, attraction tickets, itinerary planning, visa information, travel insurance, and car rental through Fliggy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers and travel-support agents use this skill to search for private-car-with-driver day tours and related travel products using live flyai CLI results. It helps format real-time travel options into concise, bookable Markdown responses with required booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can save raw user travel requests in a local .flyai-execution-log.json file, which may retain sensitive trip details without clear consent or retention controls. <br>
Mitigation: Avoid entering passport numbers, booking references, phone numbers, or other sensitive details; review and delete .flyai-execution-log.json when saved query history is not needed. <br>
Risk: The skill depends on the flyai CLI and an external travel service, so results can fail, time out, or be unavailable. <br>
Mitigation: Run the documented environment check, retry or simplify failed queries, and report failures honestly instead of answering from model memory. <br>


## Reference(s): <br>
- [Private Car skill page](https://clawhub.ai/xiejinsong/private-car) <br>
- [Parameter and output templates](references/templates.md) <br>
- [Private car playbooks](references/playbooks.md) <br>
- [Failure fallbacks](references/fallbacks.md) <br>
- [Execution log runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with comparison tables, booking links, and inline shell commands when setup or retry steps are needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires live flyai CLI execution for travel data; raw JSON should not be shown to users.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
