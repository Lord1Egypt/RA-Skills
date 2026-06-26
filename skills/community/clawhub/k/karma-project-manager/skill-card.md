## Description: <br>
Manage projects, grants, milestones, updates, payouts, and invoices on the Karma protocol through the Karma API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maheshmurthy](https://clawhub.ai/user/maheshmurthy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to create and update Karma projects, manage grants and milestones, report impact, add team members, and retrieve payout or invoice information. The skill is intended for account-backed Karma API workflows where the user confirms the exact action and parameters before requests are sent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send account-backed Karma API requests for project, grant, payout, and invoice tasks. <br>
Mitigation: Use a least-privileged Karma API key where possible and confirm the exact project, grant, network, action, and parameters before any request is sent. <br>
Risk: The skill depends on a Karma API key for authenticated operations. <br>
Mitigation: Keep the API key out of chat and use the separate setup-agent flow to configure or rotate credentials. <br>
Risk: Some payout and invoice data may be permissioned or reduced on public endpoints. <br>
Mitigation: Check permissions when an authenticated request returns 403 and clearly distinguish public endpoint results from full account-authorized results. <br>


## Reference(s): <br>
- [Karma API Documentation](https://gapapi.karmahq.xyz/v2/docs/static/index.html) <br>
- [ClawHub Skill Page](https://clawhub.ai/maheshmurthy/karma-project-manager) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, configuration guidance] <br>
**Output Format:** [Markdown with inline shell commands and structured API request guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Karma API key for authenticated actions; some public lookup endpoints return reduced data.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
