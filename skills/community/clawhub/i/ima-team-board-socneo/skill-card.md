## Description:

IMA Team Board - AI Team Collaboration Message Board via IMA API

This skill is ready for commercial/non-commercial use.

## Publisher:

[socneo](https://clawhub.ai/user/socneo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent teams use this skill to create, append, read, list, and summarize Tencent IMA message boards for asynchronous collaboration and status sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends board content to Tencent IMA using API credentials supplied by the user.

Mitigation: Install it only for intended Tencent IMA workflows and avoid placing unrelated sensitive notes in boards the agent can reach.

Risk: Leaked credentials or board IDs could expose or modify shared board content.

Mitigation: Use environment variables, keep board IDs private, and scope credentials to the intended workspace or boards where possible.

Risk: An unpinned requests dependency can change behavior across installs.

Mitigation: Prefer a pinned dependency or lockfile for requests in production environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/socneo/skills/ima-team-board-socneo)
- [Tencent IMA agent interface](https://ima.qq.com/agent-interface)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python examples, shell commands, and text board content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided Tencent IMA API credentials and board identifiers.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
