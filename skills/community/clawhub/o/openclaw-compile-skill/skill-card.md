## Description:

Compile turns raw markdown notes from an inbox into structured knowledge-transfer documents, then archives the original material with reversible links and checkpointed audit state.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arroncn993-sys](https://clawhub.ai/user/arroncn993-sys)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw operators use this skill to convert raw markdown inbox notes into curated transit documents while preserving source archive links and checkpointed audit state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad local file-mutation authority can move, archive, delete, or rewrite files inside configured vault paths.

Mitigation: Install only in a trusted local vault with backups or version control, and review COMPILE_* directories before use.

Risk: Untrusted note content or model-generated text could influence file paths or checkpoint audit commands.

Mitigation: Do not allow untrusted content to choose file paths or --audit-cmd values; review paths and commands before execution.

Risk: A failed audit can leave a partially compiled or archived note.

Mitigation: Follow the blocked checkpoint behavior and rerun compile_check.sh until it passes before treating a run as complete.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/arroncn993-sys/skills/openclaw-compile-skill)
- [Compile workflow](references/workflow.md)
- [Compile template](references/compile-template.md)
- [Frontmatter specification](references/frontmatter-spec.md)
- [Self-check checklist](references/self-check-checklist.md)
- [Title rules](references/title-rules.md)
- [Error playbook](references/error-playbook.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command invocations and generated or modified local markdown files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May move, archive, and update source markdown and asset files inside configured vault directories.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata; SKILL.md frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
