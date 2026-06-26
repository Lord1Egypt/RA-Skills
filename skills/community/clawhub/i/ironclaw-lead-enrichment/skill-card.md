## Description: <br>
Enrich contact and lead records with LinkedIn profiles, email addresses, company data, and education info. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aspenas](https://clawhub.ai/user/aspenas) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Sales, operations, and CRM users use this skill to fill missing lead data, find likely contact details, enrich company information, and summarize enrichment progress for individual or bulk records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can collect inferred personal contact data and enrich lead lists at scale. <br>
Mitigation: Use it only on lead lists the user is authorized to enrich, and confirm that LinkedIn, website, and search-based collection complies with applicable policies and source terms. <br>
Risk: The skill can bulk-update CRM records with inferred or conflicting data. <br>
Mitigation: Require a dry-run preview before database writes, avoid overwriting existing values unless requested, and keep backups or an audit log for rollback. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries with SQL examples, enrichment steps, confidence labels, and progress reporting.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose DuckDB updates and inferred contact fields; existing data should not be overwritten unless explicitly requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
