## Description:

Perforce / Helix Core (p4) power-user CLI for inspecting and managing changelists, shelves, clients, annotations, syncs, and depots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[m9rco](https://clawhub.ai/user/m9rco)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to operate Perforce / Helix Core workspaces through the p4u CLI, including changelist inspection, shelving workflows, annotation, sync, client cleanup, and untracked-file discovery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Nightly remote binaries are mutable and would execute with access to local workspaces and Perforce sessions.

Mitigation: Prefer a pinned, signed, versioned p4u release or build from auditable source before installing.

Risk: Installing CLI binaries into a system-wide PATH can expand the impact of a compromised or incorrect binary.

Mitigation: Review the install path and avoid installing nightly binaries into system-wide PATH.

Risk: Delete, revert, client deletion, and force operations can remove or alter Perforce workspace state.

Mitigation: Keep explicit confirmation before destructive operations and show the exact command before execution.

## Reference(s):

- [p4u ClawHub skill page](https://clawhub.ai/m9rco/skills/p4u)
- [p4u repository](https://github.com/m9rco/p4u-skill)
- [p4u releases](https://github.com/m9rco/p4u-skill/releases)
- [Helix Core command-line client downloads](https://www.perforce.com/downloads/helix-command-line-client-p4)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON-producing CLI invocations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill directs agents to use --non-interactive for p4u commands, request confirmation for destructive operations, and use --json when output needs programmatic parsing.]

## Skill Version(s):

0.0.0-nightly.e055304 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
