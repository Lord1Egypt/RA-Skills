## Description: <br>
mar-docs-cog helps agents create professional documents such as resumes, contracts, reports, proposals, invoices, and certificates through SkillBoss API Hub. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marjoriebroad](https://clawhub.ai/user/marjoriebroad) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and professionals use this skill to draft, format, and generate polished business, career, legal, finance, education, event, and marketing documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Document prompts and provided content are sent to a third-party API service. <br>
Mitigation: Avoid secrets, regulated personal data, confidential client material, or legally sensitive facts unless the provider terms are reviewed and the user is authorized to share the data. <br>
Risk: Contracts, privacy policies, financial documents, and compliance claims may be incomplete or unsuitable for direct use. <br>
Mitigation: Treat these outputs as drafts and obtain qualified human review before relying on them. <br>
Risk: The skill requires a sensitive API credential. <br>
Mitigation: Store SKILLBOSS_API_KEY in the agent environment and avoid placing it in prompts, generated documents, source files, or logs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/marjoriebroad/mar-docs-cog) <br>
- [SkillBoss API endpoint](https://api.heybossai.com/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with shell and Python examples; generated documents are requested as PDF by default.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY and sends document prompts and provided content to the SkillBoss/HeyBoss API service.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
