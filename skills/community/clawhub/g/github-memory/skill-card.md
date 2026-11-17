## Description:

Gives AI agents a way to store, recall, and search GitHub issue and pull request context using BlueColumn persistent memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bluecolumnconsulting-lgtm](https://clawhub.ai/user/bluecolumnconsulting-lgtm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to recall and persist GitHub issue, pull request, and repository workflow context across interactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: GitHub issue, pull request, repository, or interaction summaries may be stored in a third-party persistent service.

Mitigation: Use only when organizational policy permits sending GitHub workflow data to BlueColumn, and require agent confirmation before storing new memories.

Risk: Stored memory could include secrets, private details, source code, or credentials if agents summarize sensitive work without review.

Mitigation: Configure agents to redact secrets and private details, avoid source code and credentials, and confirm how stored memories can be reviewed and deleted.

## Reference(s):

- [BlueColumn API documentation](https://bluecolumn.ai/docs)
- [ClawHub github-memory skill page](https://clawhub.ai/bluecolumnconsulting-lgtm/skills/github-memory)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with curl command examples and API request patterns]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a BlueColumn API key and can send GitHub workflow data to a third-party persistent memory service.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
