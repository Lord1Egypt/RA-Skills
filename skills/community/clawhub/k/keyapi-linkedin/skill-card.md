## Description:

Analyze LinkedIn users and companies through the KeyAPI REST API using live official docs for professional profiles, contact information, work history, education, skills, posts, company profiles, employees, jobs, job counts, and job details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xyzzero](https://clawhub.ai/user/xyzzero)

### License/Terms of Use:

MIT-0

## Use Case:

External users, business researchers, recruiters, and developers use this skill to route LinkedIn research questions to documented KeyAPI workflows, run authorized live API requests, and return concise analysis or structured reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The authentication setup can store a KeyAPI bearer token in plaintext shell profile files.

Mitigation: Prefer a session-scoped KEYAPI_TOKEN or a separate secret manager, avoid the --token command form, and never print, restate, screenshot, commit, or log the token.

Risk: LinkedIn contact and profile workflows can collect personal or business contact data without strong privacy guardrails.

Mitigation: Use these workflows only for authorized, necessary, and compliant business purposes, and confirm scope before broad reporting or enrichment.

Risk: Live KeyAPI requests may consume credits, and repeated identical helper-script requests call the API again.

Mitigation: Limit pagination and report scope to the approved task, preview results when practical, and save full responses only when complete data is needed.

## Reference(s):

- [KeyAPI LinkedIn documentation](https://docs.keyapi.ai/en/linkedin/)
- [KeyAPI docs index](https://docs.keyapi.ai/llms.txt)
- [KeyAPI bearer authentication](https://docs.keyapi.ai/overview/authentication#bearer-authentication)
- [Global rules](references/global-rules.md)
- [Scenario cards](references/scenarios.md)
- [Routing policy](references/routing-policy.md)
- [LinkedIn user module rules](references/linkedin-user-rules.md)
- [LinkedIn company module rules](references/linkedin-company-rules.md)
- [LinkedIn jobs module rules](references/linkedin-jobs-rules.md)
- [Setup and auth](references/setup-and-auth.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with inline shell commands and optional JSON output from KeyAPI helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Live KeyAPI calls require KEYAPI_TOKEN and should stay within the user's approved LinkedIn lookup or report scope.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
