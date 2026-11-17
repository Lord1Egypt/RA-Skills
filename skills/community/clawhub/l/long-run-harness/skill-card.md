## Description:

Builds a Planner-Generator-Evaluator multi-agent harness or long-running orchestrator for automated app generation, evaluation, iteration, and workspace-safe artifact handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[is-xins-xiaobai](https://clawhub.ai/user/is-xins-xiaobai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create a configurable local harness that coordinates planner, generator, and evaluator agents across iterative app-building sprints. It is suited for teams that need structured handoffs, evaluation evidence, workspace boundaries, and configurable Claude, Codex, or DeepSeek-backed agent roles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide autonomous local coding agents with broad file, shell, environment, and git authority.

Mitigation: Use a disposable clone or container, keep production credentials out of the environment, and apply strict workspace and path boundaries before running generated harnesses.

Risk: Existing-codebase use can modify application files or repository history if write scope and commits are not constrained.

Mitigation: Define write allowlists and protected paths, keep generated artifacts under harness-state and harness-logs, and disable or path-scope git commits.

Risk: Optional DeepSeek-backed deepcode execution depends on a trusted local executable path and configured credentials.

Mitigation: Disable deepcode unless the executable path is trusted, pin dependencies, and scope DEEPSEEK_API_KEY exposure to the harness run.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/is-xins-xiaobai/skills/long-run-harness)
- [Skill definition](artifact/SKILL.md)
- [Agent patterns](artifact/instructions/agent-patterns.md)
- [Configuration guidance](artifact/instructions/config.md)
- [Workspace hygiene](artifact/instructions/workspace-hygiene.md)
- [Git safety](artifact/instructions/git-safety.md)
- [Evaluator evidence handling](artifact/instructions/evaluator-evidence.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python, YAML, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces scaffolded harness files, prompts, state models, evaluation rubrics, logs, and configuration guidance.]

## Skill Version(s):

1.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
