## Description:

Search, discover, and retrieve professional candidate profiles using OpenJobs AI. Supports structured search, profile lookup, candidate comparison, talent analytics, and contact info unlock.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openjobsai](https://clawhub.ai/user/openjobsai)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiters and talent sourcing teams use this skill to search OpenJobs AI candidate data, retrieve profiles, compare candidates, analyze talent pools, and unlock contact information for authorized recruiting workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Mira API key and setup instructions could expose the secret if copied into chat or printed in logs.

Mitigation: Use a secure secret store or preconfigured MIRA_KEY environment variable; do not paste the key into chat or print it with echo.

Risk: Candidate email unlock can reveal personal contact information.

Mitigation: Unlock or display candidate email addresses only for legitimate authorized recruiting purposes with appropriate privacy controls.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/openjobsai/skills/openjobs-people-search)
- [OpenJobs AI](https://www.openjobs-ai.com)
- [OpenJobs AI platform](https://platform.openjobs-ai.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Guidance]

**Output Format:** [Markdown summaries with inline shell commands and API response interpretation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses OpenJobs AI API results and should avoid raw JSON dumps for candidate presentation.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
