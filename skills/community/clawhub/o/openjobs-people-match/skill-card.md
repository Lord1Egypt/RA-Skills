## Description:

Evaluate candidate-job fit using OpenJobs AI. Grade a single CV against a job description or bulk-grade multiple candidates and rank them by match score.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openjobsai](https://clawhub.ai/user/openjobsai)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiters, hiring teams, and sourcing agents use this skill to evaluate how closely one or more candidates match a specific job description. It returns OpenJobs AI fit scores and concise ranked match explanations for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Candidate CVs, LinkedIn URLs, and job descriptions may contain personal or sensitive hiring data sent to OpenJobs AI.

Mitigation: Confirm data-sharing approval before use and send only candidate and job information that policy permits.

Risk: The Mira API key may be exposed if pasted into chat, printed, or stored in logs.

Mitigation: Configure MIRA_KEY through a protected secret mechanism, avoid printing it, and rotate the key if exposure is possible.

Risk: AI-generated fit scores may be mistaken for absolute candidate quality assessments.

Mitigation: Use scores only as job-description fit signals and keep human review in hiring decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/openjobsai/skills/openjobs-people-match)
- [OpenJobs AI](https://www.openjobs-ai.com/?utm_source=people_match_skill)
- [OpenJobs AI Platform](https://platform.openjobs-ai.com/)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Markdown, Guidance]

**Output Format:** [Markdown with inline shell commands and compact ranked grading results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses MIRA_KEY for OpenJobs AI API access; bulk grading accepts 1-20 LinkedIn URLs and returns ranked scores with brief explanations.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
