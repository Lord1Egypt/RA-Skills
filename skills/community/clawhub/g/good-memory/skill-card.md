## Description:

Good Memory restores recent OpenClaw session history after a reset or session rotation so an agent can continue with prior conversation context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[acilgit](https://clawhub.ai/user/acilgit)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers of OpenClaw use this skill to restore recent conversation context after a session reset or rotation. It is intended for OpenClaw environments where automatic session-start recovery is acceptable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic recovery can replay prior chat content into later sessions.

Mitigation: Enable automatic recovery only with informed user or administrator approval, and limit restored history to the minimum context needed.

Risk: The advertised one-line installer and persistence changes can modify local agent startup behavior.

Mitigation: Install only from a pinned, locally reviewed archive with a verified hash, review AGENTS.md changes before use, and keep a clear uninstall or rollback path.

Risk: Trackers and logs may expose session paths or recovered conversation context.

Mitigation: Restrict permissions on tracker and log files, and review storage locations before deployment.

## Reference(s):

- [Good Memory on ClawHub](https://clawhub.ai/acilgit/skills/good-memory)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text recovery context with Markdown documentation and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Restores recent prior-session records when recovery is enabled; exact restored history depends on local OpenClaw session files and configuration.]

## Skill Version(s):

2.0.1 (source: SKILL.md frontmatter, release evidence, CHANGELOG released 2026-03-28)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
