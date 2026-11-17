## Description:

Turn agent explanations into local animated flow diagrams, described in YAML and played back one hop at a time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[naorsabag](https://clawhub.ai/user/naorsabag)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical teams use OpenHop to turn explanations, code walkthroughs, service architectures, product workflows, pipelines, state machines, and user journeys into local animated flow diagrams.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to run unpinned npm-based OpenHop commands.

Mitigation: Prefer a pinned or preinstalled OpenHop CLI before allowing the agent to run OpenHop commands.

Risk: The skill broadly redirects explanation and diagram requests into local command execution.

Mitigation: Use the skill only when the user explicitly wants an OpenHop-generated local flow diagram, and review the generated YAML and command plan before execution.

Risk: The skill may start local services or change local OpenHop state through init, serve, demo, push, patch, list, or remove commands.

Mitigation: Approve service startup and configuration or flow-state changes before allowing those commands.

## Reference(s):

- [OpenHop project homepage](https://github.com/naorsabag/openhop)
- [ClawHub OpenHop listing](https://clawhub.ai/naorsabag/skills/openhop)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with YAML examples and shell command snippets; command output is JSON containing a local flow URL.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local OpenHop flow specifications and returns a per-flow localhost URL when the agent runs OpenHop commands.]

## Skill Version(s):

1.0.1 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
