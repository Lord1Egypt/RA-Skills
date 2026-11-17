## Description:

Shared .md interchange library for OpenClaw skills - atomic writes, deterministic serialization, YAML frontmatter, advisory locking, and schema validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[frank-bot07](https://clawhub.ai/user/frank-bot07)

### License/Terms of Use:

MIT

## Use Case:

Developers and skill authors use this library to read, write, validate, lock, index, and reconcile Markdown interchange files shared between OpenClaw skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public file APIs accept raw paths and may affect files outside the intended workspace.

Mitigation: Use only trusted callers, constrain interchange paths to a dedicated workspace, and avoid passing user-supplied paths directly.

Risk: The library is a foundational file-writing dependency for other OpenClaw skills.

Mitigation: Review and test integrations before deployment, especially write, locking, indexing, and validation workflows.

Risk: Dependencies were flagged for update by the server security guidance.

Mitigation: Update flagged dependencies and rerun security and regression checks before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/frank-bot07/skills/openclaw-interchange)
- [Publisher profile](https://clawhub.ai/user/frank-bot07)

## Skill Output:

**Output Type(s):** [Code, Files, Markdown, Configuration]

**Output Format:** [JavaScript library APIs that produce and consume Markdown files with YAML frontmatter]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include deterministic Markdown serialization, content hashes, generation IDs, indexes, and validation results.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
