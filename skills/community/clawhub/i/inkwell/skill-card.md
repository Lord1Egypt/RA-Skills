## Description:

Inkwell bootstraps a three-layer OpenClaw memory system with PARA Markdown structure, QMD search guidance, daily consolidation, transcript verification, and sign-off workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davidkim01](https://clawhub.ai/user/davidkim01)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to initialize a local agent memory workspace, organize knowledge with PARA Markdown files, configure searchable memory, and add optional daily consolidation and sign-off routines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent transcript and session indexing can retain sensitive conversations or credentials.

Mitigation: Keep transcript storage opt-in and local, preserve gitignore protections, avoid storing secrets in memory files, and apply a retention limit.

Risk: Scheduled consolidation can write incorrect or sensitive session details into long-term memory.

Mitigation: Configure consolidation to produce reviewable updates, use private delivery channels, and review memory changes before relying on them.

Risk: Third-party installation commands for QMD can introduce supply-chain risk.

Mitigation: Review the skill before installation and replace broad install commands with pinned, verified installation methods where possible.

## Reference(s):

- [QMD Setup Guide](references/qmd-setup.md)
- [Daily Consolidation](references/consolidation.md)
- [Transcript Verification System](references/transcripts.md)
- [Sign-Off Routine](references/sign-off.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or proposes local Markdown memory files and optional scheduled consolidation and transcript workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
