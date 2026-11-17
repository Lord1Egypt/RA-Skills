## Description:

Production resilience patterns for Paperclip AI agent orchestration, including spawn fallback, model rotation, run recovery, blocker routing, and task injection for OpenClaw deployments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[levineam](https://clawhub.ai/user/levineam)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to make Paperclip agents running under OpenClaw more resilient to provider rate limits, gateway restarts, failed heartbeat runs, and blocked sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send credentials and task contents to Paperclip API destinations controlled by configuration.

Mitigation: Use only trusted Paperclip endpoints, prefer HTTPS with a known host, avoid secrets in task text, and constrain credentials before scheduling recovery jobs.

Risk: Task injection can add default workflow-changing instructions to spawned agents.

Mitigation: Disable or customize task-injection defaults unless the PR and blocker-routing workflow is intended for the deployment.

Risk: Run recovery may operate with broad Paperclip credentials if scheduled without careful scoping.

Mitigation: Do not schedule run recovery until endpoint handling and credential scope are reviewed and constrained.

## Reference(s):

- [Paperclip Resilience on ClawHub](https://clawhub.ai/levineam/skills/paperclip-resilience)
- [Architecture documentation](docs/architecture.md)
- [Paperclip](https://github.com/paperclipai/paperclip)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [Paperclip issue #276: Auto-requeue agent on failure](https://github.com/paperclipai/paperclip/issues/276)
- [Paperclip issue #1845: No crash-recovery wakeup after restart](https://github.com/paperclipai/paperclip/issues/1845)
- [Paperclip issue #1861: Agent death on 429 with no model fallback](https://github.com/paperclipai/paperclip/issues/1861)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples, JavaScript module usage, and JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke OpenClaw and Paperclip workflows when operators run the provided Node.js scripts.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
