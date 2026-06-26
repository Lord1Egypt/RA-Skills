## Description: <br>
Search for flights suitable for loyalty program miles redemption, with support for related travel searches and booking workflows powered by Fliggy (Alibaba Group). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bufferstreamer](https://clawhub.ai/user/bufferstreamer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers and travel-support agents use this skill to search loyalty, miles, award, and frequent-flyer flight options through the flyai CLI and return booking-ready Markdown results with links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks agents to globally install and run a third-party travel CLI, which may send flight or trip details to that service. <br>
Mitigation: Review and install the CLI manually where possible, prefer a pinned version if available, and confirm each external search before execution. <br>
Risk: Booking links and travel results depend on external CLI output and should not be replaced with model knowledge. <br>
Mitigation: Require each listed result to include a booking link from CLI output and rerun or stop when the CLI fails or returns invalid data. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/bufferstreamer/loyalty-flight) <br>
- [Parameter Collection & Output Templates](references/templates.md) <br>
- [Scenario Playbooks](references/playbooks.md) <br>
- [Failure Recovery](references/fallbacks.md) <br>
- [Execution Runbook](references/runbook.md) <br>
- [Node.js](https://nodejs.org/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with comparison tables, booking links, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results should come from flyai CLI output, include booking links, follow the user's language, and avoid raw JSON.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
