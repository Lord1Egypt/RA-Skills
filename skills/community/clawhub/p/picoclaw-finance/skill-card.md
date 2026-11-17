## Description:

Web scraping skill for LinkedIn job postings using public API endpoints. Extract job data without authentication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nicolassantos23](https://clawhub.ai/user/nicolassantos23)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, recruiters, and job-search automation workflows use this skill to collect public LinkedIn job listings and optional job details with filters for location, remote status, experience, job type, posting date, salary, company, and industry.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CSV exports can carry spreadsheet formula-injection or unsafe-opening risk.

Mitigation: Prefer JSON where possible, or sanitize CSV values before opening exported files in spreadsheet applications.

Risk: Scraping LinkedIn may create terms-of-service and rate-limit concerns.

Mitigation: Review LinkedIn terms, use conservative request limits, and follow the skill's throttling guidance.

Risk: User-directed exports can write data to unintended paths.

Mitigation: Choose explicit output paths and review destination paths before saving results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nicolassantos23/skills/picoclaw-finance)
- [Project homepage](https://github.com/nicolasteofilo/opencode-skills)
- [Project support issues](https://github.com/nicolasteofilo/opencode-skills/issues)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell examples; job results can be returned as Python dictionaries or exported as JSON or CSV.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses user-selected search filters and user-directed output paths; CSV output should be sanitized before opening in spreadsheet applications.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
