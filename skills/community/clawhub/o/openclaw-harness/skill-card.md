## Description:

Cross-session context manager for AI agents with checkpoint/snapshot, Build-Verify-Fix closure, and entropy management (GC).

This skill is ready for commercial/non-commercial use.

## Publisher:

[lanzhou3](https://clawhub.ai/user/lanzhou3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to initialize a local harness, create and restore checkpoints, run verification rules, track cross-session progress, and clean up stale workspace state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary says the skill advertises broad workspace-management abilities while shipping incomplete or unsafe tooling that can affect local state.

Mitigation: Review the skill carefully before installing and run cleanup-related commands in dry-run mode before allowing changes to important workspaces.

Risk: The security guidance identifies unresolved numeric config validation, symlink handling, path validation, restore warning, and memory-file scoping issues.

Mitigation: Treat .harness/config.json and packaged skill directories as trusted input only, and defer production use of the GC agent and examples until those issues are fixed.

## Reference(s):

- [OpenClaw Harness ClawHub Page](https://clawhub.ai/lanzhou3/skills/openclaw-harness)
- [Architecture](references/architecture.md)
- [Requirements](references/requirement.md)
- [Technical Knowledge Package](references/knowledge-package.md)
- [Maintenance Guide](references/maintenance.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local file and workspace state changes through harness commands.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
