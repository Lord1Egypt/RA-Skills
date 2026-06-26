## Description: <br>
Prospector finds B2B leads matching an ideal customer profile by searching companies with Exa, enriching contacts with Apollo, exporting CSVs, and optionally syncing records to Attio CRM. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[slempiam](https://clawhub.ai/user/slempiam) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Sales, growth, and business development users use this skill to collect ICP criteria, generate lead and contact lists, and export or sync prospects for outreach workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys for Exa, Apollo, and Attio may be stored locally or supplied through environment variables. <br>
Mitigation: Use revocable least-privilege keys, keep local config permissions restricted, and rotate stored keys when the skill is no longer in use. <br>
Risk: ICP criteria and lead or contact data may be processed by Exa, Apollo, and Attio. <br>
Mitigation: Share only appropriate prospecting data with these services and protect or delete exported CSV files when no longer needed. <br>
Risk: Optional Attio sync can create or update CRM company and contact records. <br>
Mitigation: Review generated leads before syncing and confirm the target Attio workspace and permissions are appropriate. <br>


## Reference(s): <br>
- [Prospector on ClawHub](https://clawhub.ai/slempiam/prospector) <br>
- [Exa](https://exa.ai) <br>
- [Apollo](https://apollo.io) <br>
- [Attio](https://attio.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, CSV files, CRM records] <br>
**Output Format:** [Markdown guidance with shell commands and CSV output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Exports lead data to a local CSV and can optionally create or update Attio CRM records.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
