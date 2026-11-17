## Description:

Spawns OpenCode as an ACP subagent for game builds, web apps, multi-file coding projects, and complex refactoring tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jadegaul](https://clawhub.ai/user/jadegaul)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to delegate game development, web app creation, multi-file project scaffolding, and complex refactoring to an OpenCode ACP subagent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can delegate coding tasks to OpenCode with read/write file access, shell commands, and git operations.

Mitigation: Use it only in trusted project directories and review spawned-agent actions before accepting changes to important repositories or sensitive files.

Risk: Broad trigger language may activate the launcher for coding tasks beyond the user's intended scope.

Mitigation: Use explicit prompts, narrow the working directory, and avoid delegating ambiguous requests.

## Reference(s):

- [OpenCode Game Builder on ClawHub](https://clawhub.ai/jadegaul/skills/opencode-games)

## Skill Output:

**Output Type(s):** [code, shell commands, configuration, guidance]

**Output Format:** [Text, Markdown guidance, shell command examples, and generated or modified project files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify files and run shell or git operations when coding work is delegated to OpenCode.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
