## Description:

Intelligent webhook dispatcher with GitHub API fallback. Automatically handles git push failures by routing to GitHub Contents API. Supports retry logic, delivery receipts, and multi-endpoint fan-out.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nima54851](https://clawhub.ai/user/nima54851)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to recover from git push failures by dispatching files through the GitHub Contents API, with retry handling, delivery receipts, and optional fan-out to multiple repositories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent toward authenticated writes to GitHub repositories through a fallback upload path.

Mitigation: Use narrowly scoped tokens, restrict allowed repositories and file paths, and require explicit confirmation before fallback uploads.

Risk: The skill may contact external dispatcher or alert endpoints during fallback workflows.

Mitigation: Review and approve dispatcher and alert endpoints before use, and avoid hardcoding secrets in configuration.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON, YAML, and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe authenticated GitHub repository writes, retry behavior, delivery receipts, and webhook configuration.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
