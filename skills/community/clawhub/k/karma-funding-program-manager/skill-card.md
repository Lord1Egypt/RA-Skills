## Description: <br>
Create and manage Karma funding programs, including program setup, intake forms, applications, reviewers, milestones, payouts, grant agreements, comments, and AI evaluation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maheshmurthy](https://clawhub.ai/user/maheshmurthy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Program administrators and grant operators use this skill to run funding program workflows on Karma, from program creation and application intake through reviewer management, approvals, payouts, agreements, and reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent durable API access to high-impact Karma funding administration workflows. <br>
Mitigation: Use a dedicated, least-privileged Karma API key and review the key's permissions before use. <br>
Risk: Administrative actions can approve or reject applications, change reviewers, toggle agreements, run AI evaluations, and create payouts. <br>
Mitigation: Manually confirm every high-impact command and its target identifiers before it runs. <br>
Risk: Persisting a Karma API key in shell startup files or credential files can increase credential exposure. <br>
Mitigation: Avoid long-lived shell startup storage unless necessary, prefer scoped credential storage, and rotate the key if exposure is suspected. <br>


## Reference(s): <br>
- [Karma API Docs](https://gapapi.karmahq.xyz/v2/docs/static/index.html) <br>
- [ClawHub Skill Page](https://clawhub.ai/maheshmurthy/karma-funding-program-manager) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with curl command examples and JSON request bodies.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Karma API keys and program, application, community, grant, wallet, and payout identifiers supplied by the user or environment.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
