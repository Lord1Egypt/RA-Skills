## Description: <br>
Automates healthcare patient support workflows with AI-assisted query responses, appointment scheduling, reminders, and EMR/CRM integration guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ncreighton](https://clawhub.ai/user/ncreighton) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Healthcare operations teams, clinic administrators, and developers use this skill to plan or configure chatbot workflows for patient questions, appointment handling, reminders, billing FAQs, and staff escalation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for access to sensitive healthcare systems and patient communication channels. <br>
Mitigation: Use test credentials first, restrict EMR read and write scopes, and require HIPAA/BAA review for each provider integration. <br>
Risk: Automated messages, billing answers, appointment changes, or EMR writes could affect patient care or operations if used without review. <br>
Mitigation: Keep human approval on outbound patient messages, billing responses, appointment changes, and EMR writes until the workflow is validated. <br>
Risk: Conversation logging can expose protected health information if consent and retention controls are incomplete. <br>
Mitigation: Require explicit patient consent before storing or transmitting PHI and apply organization-approved audit, retention, and access controls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ncreighton/healthcare-chatbot-pro) <br>
- [Publisher profile](https://clawhub.ai/user/ncreighton) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with prompts, configuration snippets, shell commands, and example chatbot outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node, python3, OpenAI, Twilio, EMR, and CRM credentials when adapting the workflows for real systems.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
