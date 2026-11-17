## Description:

Multi Team Coding provides an AI-driven coding workflow for parallel agent teams, one-person-company automation, Playwright testing, and PR management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[longfer](https://clawhub.ai/user/longfer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, independent maintainers, and startup teams use this skill to coordinate multiple coding agents across git worktrees, generate and run Playwright tests, and manage pull requests from GitHub issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unattended agents can read GitHub issues, edit repository files, commit, push, open pull requests, and merge changes.

Mitigation: Use a test repository or fork first, restrict GitHub tokens, and require human review before any push or merge.

Risk: Cleanup and rollback commands can remove worktrees or reset repository state.

Mitigation: Review and remove or rewrite destructive cleanup commands before running the scripts on valuable work.

Risk: Playwright authentication state files can contain reusable session data.

Mitigation: Ignore Playwright auth state files and avoid committing saved authentication artifacts.

Risk: Automation dependencies and agent behavior may vary across environments.

Mitigation: Pin dependencies, run in isolated workspaces, and inspect generated diffs and test results before integrating changes.

## Reference(s):

- [Multi Team Coding ClawHub release](https://clawhub.ai/longfer/skills/multi-team-coding)
- [OpenClaw documentation](https://docs.openclaw.ai)
- [OpenClaw GitHub repository](https://github.com/openclaw/openclaw)
- [Quick reference](README.md)
- [One-person-company guide](ONE-PERSON-COMPANY.md)
- [Playwright automation guide](PLAYWRIGHT-AUTOMATION.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with bash, TypeScript, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes example automation scripts for Claude Code, Codex, OpenCode, GitHub CLI, OpenClaw, and Playwright.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
