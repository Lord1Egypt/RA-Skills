## Description:

Molt Life Kernel helps agents implement persistent memory, crash recovery, append-only audit trails, heartbeat monitoring, coherence checks, and witness-gated approval for critical actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jongartmann](https://clawhub.ai/user/jongartmann)

### License/Terms of Use:

MIT + Attribution Required

## Use Case:

Developers and agent operators use this skill to add continuity patterns to OpenClaw agents, including memory persistence, crash recovery, audit logging, health checks, and human approval gates for high-risk actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent logs and snapshots may retain sensitive user or session content across restarts.

Mitigation: Enable the skill only where persistent memory is explicitly desired, document retention expectations for users, and apply storage access controls and review procedures before deployment.

Risk: The Soul persona and AGENTS.md guidance can create long-lived behavior changes beyond a single task.

Mitigation: Adopt persona or persistent instruction files only after operator approval, and keep them separate from ordinary short-lived task context.

Risk: The example witness callback auto-approves some actions and is not sufficient for destructive or high-impact operations.

Mitigation: Replace the example with explicit human approval for destructive, privacy-sensitive, financial, or high-impact actions.

Risk: The skill depends on an external npm package for implementation behavior.

Mitigation: Pin the dependency version, audit the package before use, and review updates before deploying them to persistent agent environments.

## Reference(s):

- [Molt Life Kernel Skill](artifact/SKILL.md)
- [Molt Life Kernel README](artifact/README.md)
- [The Five Tenets of Crustafarianism](artifact/five-tenets.md)
- [EU AI Act Compliance via molt-life-kernel](artifact/eu-ai-act.md)
- [Molt Life Kernel Project](https://github.com/X-Loop3Labs/molt-life-kernel)
- [molt.church](https://molt.church)
- [X-Loop Labs](https://x-loop3.com)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with JavaScript examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend persistent logs, snapshots, heartbeat jobs, and witness-gated approval flows.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
