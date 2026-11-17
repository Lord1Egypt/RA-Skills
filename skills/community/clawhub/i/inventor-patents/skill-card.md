## Description:

Finds an inventor’s patents, distinguishes people with the same name by organization, marks inventor order, and exports a review-ready list.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ip930](https://clawhub.ai/user/ip930)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, professionals, and applicants use this skill to identify an inventor’s patent records, separate namesakes by organization, and prepare lists for title reviews, grant applications, or résumés.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Patent search details are sent to PatentMax, and requests can consume account credit.

Mitigation: Set a spending limit and confirm the intended search scope before running paid requests.

Risk: The security assessment flags API-key handling and cache file paths for improvement.

Mitigation: Do not send paid API keys through chat; before using one, require HTTPS and redirect safeguards, protected opt-in credential storage, and validated cache paths.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/ip930/skills/inventor-patents)
- [PatentMax search workflow](artifact/references/search-workflow.md)
- [PatentMax query pitfalls](artifact/references/pitfalls.md)
- [PatentMax API platform](https://api.ip930.com/features/api-platform)

## Skill Output:

**Output Type(s):** [Text, CSV]

**Output Format:** [Brief text summary and UTF-8-with-BOM CSV file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The patent list is sorted by application date and includes publication number, title, type, applicant, application date, legal status, inventor order, and notes.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
