## Description: <br>
Helps agents book new job relocation flights and related travel through the flyai/Fliggy CLI, including flight search, hotel reservation, train tickets, itinerary planning, visa info, travel insurance, and car rental. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and travel-support agents use this skill to search and present relocation travel booking options with real-time pricing and booking links. It is intended for job move and new-job travel planning rather than general travel advice from model memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs agents to install a global flyai CLI before producing travel results. <br>
Mitigation: Require explicit user approval before installation, prefer an isolated environment, and verify the CLI installation before use. <br>
Risk: Trip details may be sent to an external flyai/Fliggy travel service to retrieve booking options. <br>
Mitigation: Use the service only when the user intends to search travel options, disclose the external provider path, and avoid sending unnecessary personal data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiejinsong/new-job-relocation) <br>
- [Parameter Collection and Output Templates](references/templates.md) <br>
- [Scenario Playbooks](references/playbooks.md) <br>
- [Failure Recovery](references/fallbacks.md) <br>
- [Execution Runbook](references/runbook.md) <br>
- [Node.js](https://nodejs.org/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with CLI-derived travel summaries, comparison tables, and booking links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires flyai CLI output and booking links from detailUrl; should not present raw JSON or training-data travel results.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
