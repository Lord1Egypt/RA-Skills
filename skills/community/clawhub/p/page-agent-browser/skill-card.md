## Description:

通过 page-agent CLI（CDP）驱动浏览器；CLI 当前仅从 GitHub Release 的 .tgz 安装（npm 官方包尚未发布）。

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdyuyouth](https://clawhub.ai/user/sdyuyouth)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to connect to a local Chrome or Edge browser over CDP, inspect tab state, execute indexed browser actions, and maintain reusable site experience notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A global third-party CLI can control a local browser through CDP.

Mitigation: Install only after reviewing the release source and archive; prefer a temporary browser profile and avoid sensitive accounts.

Risk: Automating a normal logged-in browser profile can expose cookies, accounts, and private browsing state to unintended actions.

Mitigation: Use a dedicated browser profile for automation and close or isolate sessions that are not required for the task.

Risk: Browser automation can trigger payments, posting, deletion, uploads, or account changes.

Mitigation: Require explicit human confirmation before critical actions and keep upload, payment, posting, deletion, and account-change steps under review.

## Reference(s):

- [page-agent CLI releases](https://github.com/sdyuyouth/page-agent-cli/releases)
- [ClawHub skill page](https://clawhub.ai/sdyuyouth/skills/page-agent-browser)
- [CLI reference](artifact/CLI_REFERENCE.md)
- [Architecture](artifact/ARCHITECTURE.md)
- [Critical actions](artifact/CRITICAL_ACTIONS.md)
- [Experience schema](artifact/EXPERIENCE_SCHEMA.md)
- [Exploration protocol](artifact/EXPLORATION_PROTOCOL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON]

**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented CLI output expectations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require a locally installed page-agent CLI and a Chrome or Edge browser started with a CDP debugging port.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
