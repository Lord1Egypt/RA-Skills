## Description: <br>
Search and compare flights across multiple airlines for best deals, with support for related travel tasks such as booking, hotels, trains, attraction tickets, itinerary planning, visa information, travel insurance, and car rental powered by Fliggy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to collect route details, run the FlyAI CLI, compare carrier options by recommendation, price, duration, or direct-flight preference, and return bookable flight results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill instructs agents to install an unpinned global npm CLI when FlyAI is unavailable. <br>
Mitigation: Require explicit user approval before global npm installation, prefer a pinned or sandboxed install, and verify the CLI from a trusted source before use. <br>
Risk: Route, date, and travel-search details may be sent to the FlyAI provider during CLI execution. <br>
Mitigation: Tell users before sending travel-search details to the provider and avoid submitting sensitive personal information unless the user approves. <br>
Risk: Booking links can lead users into purchase flows outside the agent environment. <br>
Mitigation: Require explicit user confirmation before opening or acting on booking links, and present links as options rather than completing purchases automatically. <br>


## Reference(s): <br>
- [Parameter Collection & Output Templates](references/templates.md) <br>
- [Scenario Playbooks](references/playbooks.md) <br>
- [Failure Recovery](references/fallbacks.md) <br>
- [Execution Runbook](references/runbook.md) <br>
- [Node.js](https://nodejs.org/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with comparison tables, booking links, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Flight results should be based on FlyAI CLI output, include branded booking links when available, and avoid raw JSON.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
