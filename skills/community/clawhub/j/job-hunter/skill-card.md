## Description:

Assists with finding, evaluating, and applying to jobs using multi-source searches, fit scoring, application support, interview preparation, salary research, and status tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sharbelayy](https://clawhub.ai/user/sharbelayy)

### License/Terms of Use:


## Use Case:

Job seekers and agents supporting them use this skill to find openings, evaluate fit against a candidate profile, prepare tailored application materials, research compensation, practice interviews, and track application status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled search script has an unsafe command-execution vulnerability.

Mitigation: Do not run artifact/scripts/search_jobs.sh until its Python interpolation issues are fixed; use manually reviewed search queries instead.

Risk: The skill can store personal job-search profile data such as location preferences, salary expectations, dealbreakers, and excluded companies.

Mitigation: Use it only in a workspace where saving job-search profile data is acceptable, and avoid putting highly sensitive personal information in profile.json.

Risk: When Brave search is enabled, search terms and location details may be sent to Brave via the configured API key.

Mitigation: Review search terms before enabling BRAVE_API_KEY and avoid including confidential personal details in queries.

## Reference(s):

- [Cover Letter & Application Guide](references/cover-letter-guide.md)
- [Interview Preparation Guide](references/interview-prep.md)
- [Candidate Profile Template](references/profile-template.json)
- [Job Search Strategies](references/search-strategies.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance, JSON data, workspace files, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update candidate profiles, job result lists, fit analyses, cover letters, interview notes, salary research notes, and application trackers in the workspace.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
