## Description:

Goal Loop supervises complex multi-step work by keeping a goal ledger, validating deliverables, repairing failures, blocking premature completion, maintaining project checkpoints when appropriate, and resuming from the latest verified state.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bz-ai](https://clawhub.ai/user/bz-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and agent users apply this skill when complex work needs explicit requirements tracking, validation evidence, repair loops, checkpointing, and disciplined final delivery. It is intended for non-trivial software, document, data, research, file-processing, multi-agent, or long-running tasks where omissions or early stopping would be costly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may create or maintain a local PROJECT-CHECKPOINT.md during larger tasks, which can affect repositories with strict tracking, privacy, or workflow rules.

Mitigation: Review the checkpoint file before sharing or committing it, or use an existing project tracker when repository policy requires a specific state record.

Risk: A structured completion and validation loop may add process overhead if applied to simple one-shot requests.

Mitigation: Use it for complex or costly multi-step work and keep simple lookups, translations, or tiny edits lightweight.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bz-ai/skills/goal-loop)
- [README.md](artifact/README.md)
- [PROJECT-CHECKPOINT.md template](artifact/templates/PROJECT-CHECKPOINT.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Files]

**Output Format:** [Markdown guidance and optional local checkpoint file updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May maintain PROJECT-CHECKPOINT.md for larger multi-phase tasks; does not include hidden code, network access, credential handling, or destructive instructions according to the provided security evidence.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter lists 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
