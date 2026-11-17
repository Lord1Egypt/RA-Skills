## Description:

Scaffold, sanitize, or share an OpenClaw multi-agent memory system with a reusable workspace, memory-lancedb-pro configuration, role prompts, task-board conventions, and startup scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sora-mury](https://clawhub.ai/user/sora-mury)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to scaffold an isolated OpenClaw memory workspace, sanitize an existing setup for sharing, and generate role prompts, task-board conventions, memory configuration, and launcher guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables automatic invocation while working with a persistent OpenClaw memory workspace.

Mitigation: Prefer explicit invocation, use an isolated target directory, and review generated workspace files before use.

Risk: The skill references installing local npm dependencies without pinned versions in the reviewed artifact.

Mitigation: Pin and verify package versions before installing dependencies.

Risk: The referenced bootstrap workflow is not included for review in the artifact.

Mitigation: Do not run the bootstrap workflow until the actual script and dependency commands have been inspected.

## Reference(s):

- [OpenClaw Memory Kit on ClawHub](https://clawhub.ai/sora-mury/skills/openclaw-memory-kit)
- [OpenClaw Memory Kit Architecture](references/architecture.md)
- [Generated Files](references/generated-files.md)
- [Sanitization Rules](references/sanitization.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with PowerShell commands, generated file descriptions, and configuration instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or guide creation of OpenClaw workspace files, launch scripts, memory directories, and placeholder environment files.]

## Skill Version(s):

0.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
