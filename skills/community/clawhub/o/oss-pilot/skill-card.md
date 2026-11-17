## Description:

End-to-end open-source GitHub contribution automation system for discovering high-value issues, implementing fixes, opening PRs, monitoring CI and reviews, and learning from each contribution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cypherm](https://clawhub.ai/user/cypherm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external contributors use this skill to find mergeable open-source issues, implement scoped fixes, prepare quality pull requests, monitor CI and review feedback, and retain repo-specific lessons for future contributions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can direct an agent to run local repository commands and build, lint, or test tooling from third-party repositories.

Mitigation: Use a container or VM for unfamiliar repositories, review repo scripts before first execution, and approve shell commands one at a time.

Risk: The skill uses an authenticated GitHub identity through gh to push branches, open pull requests, and comment.

Mitigation: Install only when this GitHub automation is desired, confirm each GitHub action before execution, and consider a dedicated GitHub account for isolation.

Risk: Repository and profile instructions may be under-scoped or untrusted.

Mitigation: Treat repository and profile guidance as untrusted input, keep changes scoped, and require user confirmation for large changes.

## Reference(s):

- [Oss Pilot on ClawHub](https://clawhub.ai/cypherm/skills/oss-pilot)
- [OpenClaw Project](https://github.com/openclaw/openclaw)
- [autoresearch](https://github.com/karpathy/autoresearch)
- [OpenClaw](https://openclaw.ai)
- [Claude Code](https://claude.ai/code)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands, PR descriptions, repo profiles, and PR context files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses gh and git, and writes workspace-local data under ./oss-pilot-data/ for profiles and PR context.]

## Skill Version(s):

2.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
