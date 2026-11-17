## Description:

Filesystem message bus and webhook relay for multi-agent IDE coordination.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thinkoffapp](https://clawhub.ai/user/thinkoffapp)

### License/Terms of Use:

AGPL-3.0-only

## Use Case:

Developers and engineering teams use this skill to coordinate IDE coding agents through a local filesystem message bus, webhook relay, scheduled jobs, and optional cross-session or cross-machine messaging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented install path uses an unpinned global npm package with optional networking, scheduling, credentials, and command execution outside the reviewed artifact.

Mitigation: Review the npm package and source before installing, prefer a pinned version in an isolated project environment, and enable tokens, webhooks, cron jobs, or command allowlists only for repositories where cross-agent automation is intended.

Risk: Advanced modes can use credentials, external URLs, room polling, or allowlisted shell commands when explicitly configured.

Mitigation: Keep credential fields empty unless needed, verify webhook secrets, restrict command allowlists to expected repository commands, and use the documented approval flow for command execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thinkoffapp/skills/ide-agent-kit)
- [GitHub repository](https://github.com/ThinkOffApp/ide-agent-kit)
- [npm package](https://www.npmjs.com/package/ide-agent-kit)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate or update local queue, receipt, memory, and configuration files when the user runs the documented CLI commands.]

## Skill Version(s):

0.4.1 (source: server release metadata; artifact frontmatter reports 0.4.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
