## Description:

Gstack OpenClaw provides a documentation-only set of OpenClaw role prompts that helps developers and product teams run structured software planning, development, review, release, and retrospective workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smseow001](https://clawhub.ai/user/smseow001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and product teams use this skill to switch between specialized software delivery roles for product planning, architecture, design review, code review, testing, deployment readiness, incident investigation, security analysis, performance checks, and retrospectives.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stale manual installation guidance may lead users to run an unpinned remote install script from outside the reviewed release.

Mitigation: Install through ClawHub by default; inspect and pin the exact remote commit before running any external install script.

Risk: Deployment, rollback, GitHub, browser-login, webhook, and telemetry examples can affect production systems or expose sensitive data if followed without safeguards.

Mitigation: Use test accounts and staging environments by default, keep tokens and session data out of logs, and require explicit approval before merge, deploy, rollback, or notification actions.

## Reference(s):

- [Gstack OpenClaw ClawHub listing](https://clawhub.ai/smseow001/skills/gstack-openclaw-sms)
- [Workflow guide](artifact/docs/workflow.md)
- [Security policy](artifact/SECURITY.md)
- [OpenClaw documentation](https://docs.openclaw.ai)
- [Garry Tan gstack reference](https://github.com/garrytan/gstack)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with structured reports, checklists, code blocks, shell commands, and configuration examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompt-oriented guidance; release evidence describes the skill as documentation-only, while security evidence calls for review of production-impacting workflows.]

## Skill Version(s):

2.5.10 (source: ClawHub release metadata and artifact _meta.json, released 2026-04-14)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
