## Description:

Provides fast, read-only codebase search and exploration using grep for content, glob for filenames, and tree for directory structure with filtering and limits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yanxingang](https://clawhub.ai/user/yanxingang)

### License/Terms of Use:


## Use Case:

Developers and coding agents use this skill to search source code, find files, and inspect project structure with consistent read-only command output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency installation guidance includes unverified system-wide binary installs.

Mitigation: Prefer trusted package-manager channels for rg, fd, and tree; only use fallback downloads after independently verifying artifacts and approving the install scope.

Risk: The skill can expose contents from directories the agent is allowed to inspect.

Mitigation: Use it only on intended project directories and avoid pointing it at locations containing unrelated sensitive files.

## Reference(s):

- [OpenClaw Code Search skill page](https://clawhub.ai/yanxingang/skills/openclaw-code-search)
- [Yanxingang publisher profile](https://clawhub.ai/user/yanxingang)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Structured text with Markdown command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only grep, glob, tree, and dependency-check outputs include delimiters, limits, and error messages.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
