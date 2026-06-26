## Description: <br>
Lead Gen Pipeline helps web design agencies find local businesses with missing or weak websites, create demo HTML sites, deploy them, send personalized pitch emails, and track leads in leads.md. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[michelle447](https://clawhub.ai/user/michelle447) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Web design agencies and sales operators use this skill to identify local website leads, build demo pages, deploy previews, prepare cold outreach, and maintain lead status tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can handle real lead and contact data for business outreach. <br>
Mitigation: Confirm recipients, data handling, and outreach compliance obligations before collecting, storing, or emailing leads. <br>
Risk: Automated pitch sending and follow-ups can create unwanted or non-compliant outreach if used without review. <br>
Mitigation: Keep manual review enabled unless the operator accepts automated sending, and respect the documented daily email limit. <br>
Risk: SMTP or Gmail credentials could be exposed if pasted into chat or committed to configuration files. <br>
Mitigation: Store credentials in environment variables or a secrets manager and avoid placing passwords in prompts, lead files, or repo files. <br>
Risk: Generated demo sites and pitch text may contain inaccurate claims about a business. <br>
Mitigation: Review business details, demo content, and email copy before deployment or sending. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/michelle447/mjw-lead-gen-pipeline) <br>
- [Demo Site HTML Template](references/demo-site-template.md) <br>
- [leads.md Schema](references/leads-schema.md) <br>
- [Cold Pitch Email Template](references/pitch-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with generated HTML/CSS snippets, lead tables, email drafts, deployment commands, and configuration guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update leads.md and demo site files when executed by an agent with filesystem access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
