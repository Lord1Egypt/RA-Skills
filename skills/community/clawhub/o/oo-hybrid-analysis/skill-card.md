## Description:

Search and read Hybrid Analysis data through the connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Security analysts use the skill to search file hashes and retrieve Hybrid Analysis report summaries, overviews, and processing states.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup directs the agent to run an unverified remote installer, and the service connection runs through OOMOL.

Mitigation: Install a verified CLI release yourself, require approval before any downloaded installer runs, and confirm whether the CLI will install or update skills in other agent applications.

## Reference(s):

- [Hybrid Analysis](https://www.hybrid-analysis.com/)
- [Hybrid Analysis API documentation](https://www.hybrid-analysis.com/docs/api/v2)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Analysis, API Calls, Shell commands, JSON]

**Output Format:** [Text summaries, JSON payloads, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Queries depend on the connected Hybrid Analysis account and available report data.]

## Skill Version(s):

1.0.4 (source: frontmatter, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
