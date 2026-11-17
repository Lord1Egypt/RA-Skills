## Description:

Monitor GitCode PRs for one or more repos, auto-run AI review via OpenClaw Gateway, post PR comments, and send notifications (DingTalk + WeCom).

This skill is ready for commercial/non-commercial use.

## Publisher:

[mingyang1996](https://clawhub.ai/user/mingyang1996)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to monitor GitCode repositories for new pull requests, run automated review through OpenClaw, publish Markdown review comments, and notify DingTalk or WeCom channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically uses GitCode credentials.

Mitigation: Use a dedicated least-privilege GitCode token, store the token file securely, and avoid running the scripts with elevated privileges.

Risk: The skill can automatically post PR comments and send reports to DingTalk or WeCom.

Mitigation: Review notification targets and generated reports before enabling automatic posting or attachments in production workflows.

Risk: A general OpenClaw agent reviews PR content that may include untrusted changes.

Mitigation: Prefer an isolated review agent or session for each PR and review generated findings before relying on them.

## Reference(s):

- [Configuration](artifact/references/CONFIG.md)
- [ClawHub skill page](https://clawhub.ai/mingyang1996/skills/openclaw-gitcode-pr-monitor)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown review reports, PR comment text, chat notification messages, shell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses GitCode API credentials, stores PR state and review reports in the OpenClaw workspace, and can post comments and send external chat notifications.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
