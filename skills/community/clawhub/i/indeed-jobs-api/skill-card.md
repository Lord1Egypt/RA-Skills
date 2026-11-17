## Description:

Search Indeed job postings, pull one posting in full with its original ATS link, and read employer profiles and employee reviews.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, recruiters, and labor-market analysts use this skill to search Indeed listings, retrieve full posting details, and inspect employer profiles and employee reviews through structured API responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API requests use paid credits, including empty results and some errors.

Mitigation: Set spending expectations before loops, cap pagination, and validate filters before making calls.

Risk: Using optional SDK packages increases the local execution footprint.

Mitigation: Prefer direct HTTPS calls when possible, or install SDKs in an isolated environment without administrator privileges.

Risk: The skill requires a Scavio API key.

Mitigation: Expose only SCAVIO_API_KEY needed for this service and keep it out of source control.

## Reference(s):

- [Scavio Indeed Search Documentation](https://scavio.dev/docs/indeed-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=indeed-jobs-api)
- [ClawHub Skill Page](https://clawhub.ai/scavio-ai/skills/indeed-jobs-api)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration, API calls]

**Output Format:** [Markdown guidance with JSON API examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [API responses are structured JSON and require SCAVIO_API_KEY; Indeed endpoint calls consume paid credits.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
