## Description:

Perstate gives agents a Git-native remote knowledge graph for persistent state, with commands to save, recall, branch, inspect, visualize, and prune memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fanzhidongyzby](https://clawhub.ai/user/fanzhidongyzby)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use Perstate to give an agent persistent, Git-backed memory for conversation-derived entities and relations. It supports recall, branch isolation, memory statistics, graph visualization, and cleanup for long-lived agent state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill maintains long-lived memory in ~/.perstate and may push conversation-derived knowledge to a Git remote.

Mitigation: Use a private repository or local path, avoid saving secrets or sensitive personal data, and review planned commits before allowing writes.

Risk: The security evidence flags broad authority to save knowledge with weak scoping.

Mitigation: Confirm the target repository, branch, and session binding before save operations, and use separate branches for different agents or contexts.

Risk: The graph viewer may expose unsafe content from shared or untrusted graph data and uses externally hosted JavaScript dependencies.

Mitigation: Avoid using /perstate view on shared or untrusted graph content until the viewer sanitizes HTML and pins or vendors its JavaScript dependencies.

## Reference(s):

- [Perstate ClawHub skill page](https://clawhub.ai/fanzhidongyzby/skills/perstate)
- [README](artifact/README.md)
- [Skill instructions](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated Markdown, YAML, Git state, and optional HTML graph output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Operates through local shell scripts, a local ~/.perstate configuration and cache, and an optional user-provided Git remote or local repository.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
