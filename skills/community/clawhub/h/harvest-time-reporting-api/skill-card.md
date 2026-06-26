## Description: <br>
Integrates with the Harvest API to help agents manage time entries, projects, tasks, clients, users, invoices, expenses, reports, and related account records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zachgodsell93](https://clawhub.ai/user/zachgodsell93) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operations teams use this skill to guide agents working with Harvest time tracking and business records through documented API requests, authentication headers, pagination, rate limits, and reporting endpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A powerful Harvest token can allow an agent to create, update, or delete real business data. <br>
Mitigation: Use the least-privileged Harvest token available and test with limited or non-production access before using production accounts. <br>
Risk: Invoice, payment, user, role, company-setting, and deletion actions can have financial or administrative impact. <br>
Mitigation: Require explicit human review before any create, update, delete, invoice, payment, role, user, or company-setting action. <br>
Risk: The skill includes examples that use account identifiers and bearer-token authentication. <br>
Mitigation: Keep Harvest tokens and account IDs in environment variables or a secret manager, and do not paste credentials into prompts, logs, or shared output. <br>


## Reference(s): <br>
- [Harvest API v2 base URL](https://api.harvestapp.com/v2) <br>
- [Harvest developer access token page](https://id.getharvest.com/developers) <br>
- [ClawHub skill page](https://clawhub.ai/zachgodsell93/harvest-time-reporting-api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with cURL examples and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Harvest account credentials supplied by the user environment.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
