## Description:

Review LyraShield release-assurance evidence through an OAuth-first MCP connection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ecryptoguru](https://clawhub.ai/user/ecryptoguru)

### License/Terms of Use:

MIT No Attribution

## Use Case:

Security reviewers, release owners, and developers use this skill to inspect LyraShield release-assurance evidence, summarize current issues, and explain pending approvals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Write-capable OAuth access could mutate LyraShield resources if scopes are broader than needed or write arguments are approved without review.

Mitigation: Keep OAuth scopes limited and review exact write arguments before approving any mutation.

Risk: Release-assurance summaries could be mistaken for a complete security guarantee.

Mitigation: Treat the skill as review assistance and keep final release and security decisions with the responsible reviewer.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/ecryptoguru/skills/lyrashield)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text review summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires LYRASHIELD_API_KEY; write actions require OAuth write scope and exact-argument approval.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
