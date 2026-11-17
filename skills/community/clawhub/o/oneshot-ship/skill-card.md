## Description:

Oneshot Ship helps agents run the oneshot CLI to plan, implement, review, and open pull requests for code changes over SSH or locally.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adwilkinson](https://clawhub.ai/user/adwilkinson)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to delegate code-shipping tasks to the oneshot CLI, including planning, implementation, review, branch creation, PR creation or update, and optional Linear ticket updates. It is suited for repositories where automated local or SSH-based coding workflows are acceptable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote SSH runs can forward credential-bearing configuration to the target host.

Mitigation: Use remote mode only with trusted hosts; prefer local or dry-run mode first, and avoid remote SSH configuration unless the host can be trusted with provider and Linear credentials.

Risk: The CLI can automate branch creation, commits, pushes, PR updates, and Linear comments.

Mitigation: Use it only in repositories where these mutations are acceptable, and review generated pull requests before merging.

Risk: The release installs a powerful mutable CLI globally.

Mitigation: Pin and verify the package version before installation where possible, and run package and environment health checks before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/adwilkinson/skills/oneshot-ship)
- [Project repository metadata](https://github.com/ADWilkinson/oneshot-cli)
- [Bun documentation](https://bun.sh)
- [Codex CLI](https://github.com/openai/codex)
- [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code)
- [GitHub CLI](https://cli.github.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, configuration examples, and workflow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or coordinate code changes, commits, pull request metadata, JSONL run events, status summaries, and Linear comments through the oneshot CLI.]

## Skill Version(s):

0.2.13 (source: ClawHub release metadata; artifact metadata version: 1.2.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
