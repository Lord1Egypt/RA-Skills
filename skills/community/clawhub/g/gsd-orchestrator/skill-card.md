## Description:

Orchestrates GSD projects through the `gsd headless` command so agents can create milestones from specs, execute development workflows, monitor progress, handle blockers, and track costs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[glittercowboy](https://clawhub.ai/user/glittercowboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to plan and run GSD software-development milestones, inspect project state, process structured results, and manage blocker or budget decisions from command output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Headless GSD subprocesses can make broad project changes.

Mitigation: Run the skill in a restricted project workspace and review resulting file changes before merging or deployment.

Risk: Answer injection can place secrets into child-process environments.

Mitigation: Avoid broad environment credentials, keep answer files out of version control, and restrict their file permissions.

Risk: Automatic prompt responses can approve actions without precise human intent.

Mitigation: Use explicit answers or supervised mode for workflows that require policy, budget, or security decisions.

Risk: A moving global install could change behavior unexpectedly.

Mitigation: Prefer a pinned or local `gsd-pi` installation before running commercial workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/glittercowboy/skills/gsd-orchestrator)
- [Command Reference](references/commands.md)
- [Headless JSON Result Reference](references/json-result.md)
- [Answer Injection Reference](references/answer-injection.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe command output in plain text, structured JSON, or JSONL event streams depending on the selected GSD output mode.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
