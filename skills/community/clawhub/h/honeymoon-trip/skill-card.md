## Description: <br>
Plan a dreamy honeymoon with luxury hotels, romantic activities, couples' spa, sunset dinners, and booking-linked travel options powered by Fliggy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to plan honeymoon travel by collecting trip parameters, running FlyAI travel lookups, and returning booking-linked flight, hotel, and activity recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install or require a global third-party travel CLI before producing results. <br>
Mitigation: Install only after reviewing and trusting the FlyAI npm CLI, and have the user approve any global installation step. <br>
Risk: Travel requests may include personal or payment-adjacent trip details and can be sent to third-party travel lookups. <br>
Mitigation: Ask only for the trip details needed to complete the lookup and avoid collecting unnecessary personal or payment information. <br>
Risk: The skill may keep raw trip requests in a local .flyai-execution-log.json file. <br>
Mitigation: Tell users who do not want local trip logs to delete or disable .flyai-execution-log.json after use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiejinsong/honeymoon-trip) <br>
- [Parameter and output templates](references/templates.md) <br>
- [Scenario playbooks](references/playbooks.md) <br>
- [Fallback guidance](references/fallbacks.md) <br>
- [Execution log runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with booking links, comparison tables, and inline shell commands for CLI setup or retries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FlyAI CLI output for travel data and should include booking links for each recommended result.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
