## Description: <br>
A legal intake agent for law firms that is designed to collect potential-client details, flag conflicts and timing concerns, and avoid unauthorized legal advice during initial triage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[igorganapolsky](https://clawhub.ai/user/igorganapolsky) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Law firm intake teams can use this skill to structure first-contact conversations with potential new clients, collect contact and case facts, and prepare conflict, statute-of-limitations, scheduling, and CRM handoff information for attorney review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive potential-client data and CRM credentials without enough privacy, consent, retention, or compliance detail. <br>
Mitigation: Require lawyer or compliance-owner review before installation, use mock data first, provide explicit privacy notice and consent before collection or CRM transfer, and define retention, redaction, access-control, and audit requirements. <br>
Risk: Prompt rules alone do not prove HIPAA compliance or prevent unauthorized practice of law. <br>
Mitigation: Treat the skill as intake support only, require attorney review for legal conclusions, keep jurisdiction-specific disclaimers current, and prevent the agent from giving advice or outcome guarantees. <br>
Risk: Automated CRM writes could expose or persist incorrect, sensitive, or unauthorized intake data. <br>
Mitigation: Restrict CRM credentials to least privilege and require human confirmation before any write or transfer to Clio, MyCase, Litify, or similar systems. <br>


## Reference(s): <br>
- [Setup Guide](artifact/setup-guide.md) <br>
- [ThumbGate Prevention Rules](artifact/thumbgate-rules.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/igorganapolsky/legal-intake-pilot) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with setup steps, intake flow instructions, and rule descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce intake summaries, disclaimer language, CRM handoff guidance, and safety-rule checks that require human legal and compliance review.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
