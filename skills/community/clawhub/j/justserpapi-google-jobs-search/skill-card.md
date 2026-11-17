## Description:

Call GET /api/v1/google/jobs/search for Google SERP Jobs Search through Just Serp API with query.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justserpapi](https://clawhub.ai/user/justserpapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to query Just Serp API for Google Jobs results, including job titles, companies, and locations. It supports job board aggregation, hiring trend analysis, and recruitment monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented command passes the Just Serp API key as a command-line argument, which can expose the secret through process listings or logs.

Mitigation: Prefer a protected secret channel or a runner version that reads JUST_SERP_API_KEY directly from the environment, and avoid pasting key values into chat messages, screenshots, or logs.

Risk: Job-search queries and filters are sent to Just Serp API.

Mitigation: Install and use the skill only when sending those search terms to Just Serp API is acceptable for the intended workflow.

## Reference(s):

- [Just Serp API](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_jobs_search&utm_content=project_link)
- [Just Serp API Docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_jobs_search&utm_content=project_link)
- [ClawHub Skill Page](https://clawhub.ai/justserpapi/skills/justserpapi-google-jobs-search)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown summary with optional JSON response payloads and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JUST_SERP_API_KEY and Node.js; calls the jobsSearch operation on /api/v1/google/jobs/search.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
