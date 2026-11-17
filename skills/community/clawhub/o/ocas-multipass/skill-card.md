## Description:

Accomplishes tasks that need tools the agent does not have by planning approaches, filling capability gaps with sandboxed tools, executing in an isolated session, and returning a task result plus replay script.

This skill is ready for commercial/non-commercial use.

## Publisher:

[indigokarasu](https://clawhub.ai/user/indigokarasu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use Multipass when a task requires tools, APIs, disposable identity, or isolated execution that the current agent does not already have. It is intended for capability-gap resolution, sandboxed execution, session replay, and failure reporting rather than permanent skill installation or general web research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can autonomously search for and call external tools or services.

Mitigation: Run it only in an isolated session and review the final manifest, replay script, and external services used before relying on the result.

Risk: The skill can create disposable signups and persist some credentials or run records outside a single response.

Mitigation: Require explicit approval for identity or credential use, keep credentials session-scoped where possible, and delete stored tokens or run records when the task is complete.

Risk: The skill includes self-update behavior from an upstream Git source.

Mitigation: Review or disable the self-update script before deployment and pin a reviewed release for managed environments.

Risk: Downloaded skills or discovered tools may be untrusted.

Mitigation: Treat discovered skills as untrusted evidence until scanned and reviewed; do not execute downloaded instructions directly without validation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/indigokarasu/skills/ocas-multipass)
- [Workflow](references/workflow.md)
- [Orchestration](references/orchestration.md)
- [Search Surfaces](references/surfaces.md)
- [Resilience](references/resilience.md)
- [Scoring Rubric](references/scoring.md)
- [Loop Prevention Rules](references/loop-prevention.md)
- [Journal](references/journal.md)
- [Storage Layout](references/storage-layout.md)
- [Self-Update](references/self-update.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown task results with replay instructions, manifests, logs, checkpoints, and JSON journals]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are written within the session directory and may include partial or failed-run reports when a task cannot be fully completed.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter and changelog list 4.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
