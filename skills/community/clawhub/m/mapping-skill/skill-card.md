## Description:

AI/ML talent discovery and outreach workflow for finding researchers from papers, labs, GitHub networks, and web pages, extracting structured profiles, deduplicating candidates, generating personalized recruiting emails, and supporting Feishu table workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[16miku](https://clawhub.ai/user/16miku)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, recruiters, and recruiting operations teams use this skill to discover AI/ML candidates from conferences, labs, GitHub networks, and supplied URLs, then structure contact data and generate personalized outreach. It can also support CSV export and Feishu table workflows for batch import, email generation, and record updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill collects personal contact data during recruiting and scraping workflows.

Mitigation: Run it only in a supervised, sandboxed environment, collect the minimum necessary data, and avoid public redistribution of personal contact details.

Risk: The skill includes Chinese-identity inference for candidate classification.

Mitigation: Do not use inferred identity as a recruiting selection or outreach-targeting criterion; limit use to user-reviewed context where legally and ethically appropriate.

Risk: The skill can write candidate and email data to Feishu with broad permissions.

Mitigation: Use least-privilege Feishu credentials, require dry runs before writes, and review table fields and record updates before batch operations.

Risk: Scraping workflows may interact with protected, rate-limited, or internal network resources.

Mitigation: Block local and internal network targets, respect site access rules, rate-limit requests, and prefer official APIs such as OpenReview when available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/16miku/skills/mapping-skill)
- [README](README.md)
- [Profile schema](references/profile-schema.md)
- [Search templates](references/search-templates.md)
- [Conference paper scraping](references/conference-paper-scraping.md)
- [Python scraping guide](references/python-scraping-guide.md)
- [Anti-scraping solutions](references/anti-scraping-solutions.md)
- [Candidate classifier](references/candidate-classifier.md)
- [Deduplication rules](references/deduplication-rules.md)
- [Field mappings](references/field-mappings.md)
- [Email templates](references/email-templates.md)
- [Talk tracks](references/talk-tracks.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, structured tables, CSV-oriented data, code snippets, shell commands, and Feishu workflow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce candidate profiles, contact fields, scraping plans, reusable Python command guidance, personalized outreach drafts, import/update summaries, and failure statistics.]

## Skill Version(s):

2.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
