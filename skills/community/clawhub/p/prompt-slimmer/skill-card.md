## Description:

Audits OpenClaw workspace Markdown files for redundant, low-frequency, and duplicated content, then produces a slim-down plan with metrics and approved archive moves.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaoyaner0201](https://clawhub.ai/user/xiaoyaner0201)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to reduce recurring OpenClaw system prompt overhead by auditing workspace files, finding ghost Markdown files, deduplicating repeated content, and planning archive moves that preserve retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompt-slimming recommendations can move or rewrite identity, safety, or root-level Markdown content that affects future agent behavior.

Mitigation: Review the proposed slim-down plan before execution, approve only intended moves or edits, and verify archived content remains searchable.

## Reference(s):

- [Prompt Slimmer ClawHub Page](https://clawhub.ai/xiaoyaner0201/skills/prompt-slimmer)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands, audit tables, and before/after metrics]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose workspace Markdown edits and archive moves that require user approval before execution.]

## Skill Version(s):

1.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
