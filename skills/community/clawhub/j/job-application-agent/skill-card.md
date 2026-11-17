## Description:

Finds and evaluates job opportunities, prepares applications for candidate review, submits authorized applications, and tracks outcomes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vaibhavarora14](https://clawhub.ai/user/vaibhavarora14)

### License/Terms of Use:

MIT-0

## Use Case:

Candidates use this agent to search and assess job listings, prepare applications, submit them with the candidate's approval or standing authorization, and track application outcomes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill shares contact details by default.

Mitigation: Before onboarding, use `telemetry disable` to stop analytics and contact uploads, and separately use `sources sharing disable` to stop community contributions. These controls do not delete previously transmitted data.

Risk: On Macs, private profile data may be exposed to local monitoring tools.

Mitigation: Seek a fix that keeps profile contents out of process arguments on macOS. Limit information sent to optional LLM services and leave CAPTCHA vendors off for private application links.

Risk: Application submissions and public pull requests can disclose candidate information or make external changes.

Mitigation: Keep individual application review enabled and authorize public pull requests separately.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/vaibhavarora14/skills/job-application-agent)
- [Application runbook](references/RUNS.md)
- [Application accounting](references/ACCOUNTING.md)
- [Autonomy and authorization](references/AUTONOMY.md)
- [Data sharing and analytics](references/ANALYTICS.md)
- [Browser uploads](references/BROWSER_UPLOADS.md)
- [Cloud state](references/CLOUD_STATE.md)
- [Application guidance](references/APPLICATION_GUIDANCE.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Shell commands, Configuration, JSON]

**Output Format:** [Candidate-facing role assessments, application drafts, setup guidance, and tracking summaries; structured CLI outputs may be JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Content varies by workflow and is based on the candidate's supplied profile and job information.]

## Skill Version(s):

3.8.6 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
