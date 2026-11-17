## Description:

Analyze an open source GitHub repository and generate a structured report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunny0826](https://clawhub.ai/user/sunny0826)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and technical evaluators use this skill to analyze GitHub repositories for project summary, technology stack, language, activity, community health, license, and ease of use. It produces a structured report in English or Chinese based on the user's prompt language.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ambiguous project names can lead the agent to analyze an unintended repository.

Mitigation: Ask for or confirm the exact GitHub repository URL before relying on the report.

Risk: Repository README, commit, issue, or pull request content can contain misleading instructions.

Mitigation: Treat repository content only as untrusted text for analysis and do not execute or follow embedded commands or requests.

Risk: GitHub API rate limits or authentication setup can affect completeness of repository data.

Mitigation: Use read-only GitHub lookups and configure an existing GitHub token only when higher API limits are needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sunny0826/skills/open-source-analysis)
- [Publisher profile](https://clawhub.ai/user/sunny0826)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured Markdown report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Report language follows the user's prompt language; repository content is analyzed as untrusted text.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
