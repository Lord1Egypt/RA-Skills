## Description: <br>
Automates freelance workflows including job search, proposal drafting, delivery tracking, client messaging, and invoice generation for platforms such as Upwork, Fiverr, Freelancer, and PeoplePerHour. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Neckr0ik](https://clawhub.ai/user/Neckr0ik) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External freelancers and operators can use this skill to search for candidate work, draft proposals, manage local job records, and generate invoice text. Outputs should be reviewed before use with clients or freelance platforms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill claims real freelance-platform automation while the code generates mock-looking job listings. <br>
Mitigation: Treat job results as demo or unverified data and confirm opportunities directly on the relevant platform before acting. <br>
Risk: Generated proposals, messages, and invoices may contain incorrect, misleading, or inappropriate client-facing content. <br>
Mitigation: Manually review and edit every proposal, message, and invoice before sending it to a client or platform. <br>
Risk: Business records are stored locally under ~/.freelance-automator. <br>
Mitigation: Avoid storing sensitive client data unless the local environment is secured and records are managed according to the user's retention needs. <br>
Risk: Platform integrations, permission boundaries, approval gates, and storage documentation are not clearly established. <br>
Mitigation: Do not provide platform credentials or rely on claimed platform coverage unless the publisher adds real integrations and clear operational controls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Neckr0ik/neckr0ik-freelance-automator) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/Neckr0ik) <br>
- [Upwork](https://www.upwork.com) <br>
- [Fiverr](https://www.fiverr.com) <br>
- [Freelancer](https://www.freelancer.com) <br>
- [PeoplePerHour](https://www.peopleperhour.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text, with optional JSON invoice output and local JSON records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local job, proposal, client, and invoice records under ~/.freelance-automator.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, SKILL.md frontmatter, claw.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
