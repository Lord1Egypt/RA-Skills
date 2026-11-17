## Description:

Answers questions about a past agent run from its recording rather than from memory, and replays or forks that run.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xizhuomengcontin](https://clawhub.ai/user/xizhuomengcontin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect recorded agent runs, trace why a prior action happened, reproduce failures with replay, and compare model behavior from a checkpoint.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Replay and compare operations can re-execute shell commands and create real side effects outside the repository worktree.

Mitigation: Review the recorded run before execution, use worktree or container isolation where appropriate, and get explicit approval for external side effects.

Risk: Model comparison can upload recorded context to external providers and incur real cost.

Mitigation: Confirm the disclosure scope, providers, model or fork count, and cost before running comparisons; scrub sensitive traces and review the scrubbed output before sharing.

Risk: Using the skill depends on trusting the external orcareplay npm package and registered MCP server.

Mitigation: Confirm trust in the package and server before installation or use, and verify the local registration before processing recorded runs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xizhuomengcontin/skills/orca-replay)
- [OrcaReplay homepage](https://github.com/Continuum-AI-Corp/OrcaReplay)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include recorded-versus-inferred distinctions, replay caveats, approval checks, and security guidance.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
