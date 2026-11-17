## Description:

Safely write large files or files with CJK or special characters using an incremental Edit strategy instead of direct Write.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thinkdonk](https://clawhub.ai/user/thinkdonk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to write or update large files, files with CJK characters, and multi-function source files while reducing write truncation and encoding failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill changes how an agent mutates files and may leave placeholders, anchors, or partial edits in important generated files.

Mitigation: Review important generated files after use and confirm placeholders, temporary markers, and file boundaries were cleaned up correctly.

Risk: Incremental edit workflows can still produce incorrect or incomplete output if anchors are stale or match unintended text.

Mitigation: Read the target file before editing, use unique anchors, and spot-check the first and last sections of generated files.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/ThinkDonk/llm-safe-write)
- [ClawHub skill page](https://clawhub.ai/thinkdonk/skills/llm-safe-write)
- [Publisher profile](https://clawhub.ai/user/thinkdonk)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration, Markdown]

**Output Format:** [Markdown guidance with inline code and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide the agent to create ASCII skeletons, placeholders, temporary anchors, and incremental edits; review important generated files after use.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
