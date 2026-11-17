## Description:

Hybrid orchestration skill where OpenClaw stays the control plane and ACP Claude Code is the default execution backend for coding work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jkobject](https://clawhub.ai/user/jkobject)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to keep OpenClaw as a lightweight planning, routing, and checkpoint control plane while ACP Claude Code and ACP Codex workers handle longer implementation, review, and fix work through file-based handoffs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad unattended worker permissions can let spawned coding workers act outside the intended task scope.

Mitigation: Run workers in a tightly isolated account or sandbox, restrict them to the intended repository or worktree and artifact directories, and replace blanket approve-all behavior with task-scoped permissions where possible.

Risk: Service-level API-key exposure can turn a local configuration mistake into credential leakage or unintended account use.

Mitigation: Protect API keys as secrets, expose them only to the service that needs them, rotate them if exposed, and avoid copying them into handoff files, run state, or logs.

Risk: Persistent sessions and run-state files can leave stale workers, old state, or sensitive task context behind.

Mitigation: Define cleanup rules for persistent sessions and generated run-state files, and review shared artifacts before reuse or publication.

Risk: Some bundled workflows are structurally validated but not fully end-to-end validated.

Mitigation: Run smoke tests for each selected workflow and backend before relying on it for high-impact or long-running work.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jkobject/skills/orchestration-setups)
- [README](artifact/README.md)
- [Skill entrypoint](artifact/SKILL.md)
- [Reproducing the Setup](artifact/docs/reproduction.md)
- [Detailed Setup Matrix](artifact/docs/setup-matrix.md)
- [Test Results](artifact/docs/test-results.md)
- [Orchestration V1 runtime reference](artifact/docs/runtime/README.md)
- [Session Patterns](artifact/examples/session-patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON/YAML configuration snippets and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces orchestration recommendations, handoff templates, review criteria, workflow definitions, and worker launch patterns.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
