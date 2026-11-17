## Description:

AroFlo (aroflo.com). Use this skill for ANY AroFlo request — searching and reading data. Whenever a task involves AroFlo, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Operations teams use the skill to search and read clients, tasks, users, and public API health information in an AroFlo account connected through OOMOL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: If the oo CLI is missing, fallback setup may execute downloaded installer code without a separate approval step.

Mitigation: Review and approve the CLI installation separately; prefer a verified, fixed release and check whether setup installs additional agent skills.

Risk: Connecting AroFlo entrusts credentials and requested business data to OOMOL.

Mitigation: Connect only an account approved for use with OOMOL and limit requested business data to what the task needs.

## Reference(s):

- [AroFlo API documentation](https://docs.api.aroflo.com/)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [AroFlo](https://aroflo.com)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [Structured AroFlo response data with concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Content depends on the selected read action and the connected AroFlo account.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
