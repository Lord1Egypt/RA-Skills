## Description:

Semantic diff for system prompts and agent instructions that compares prompt versions and reports behavior-level changes, contradictions, guardrail removals, permission expansions, instruction density changes, and a commit-ready changelog.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, prompt authors, and agent maintainers use this skill to compare two versions of system prompts, skill files, or agent instructions and understand behavior-level changes before committing them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompt files provided for comparison may contain secrets or sensitive instructions, and those contents may appear in the diff report.

Mitigation: Use the skill only on prompt files you explicitly choose to provide, and avoid comparing prompts that contain secrets unless the resulting report can safely include them.

## Reference(s):

- [Phy Prompt Diff on ClawHub](https://clawhub.ai/phy041/skills/phy-prompt-diff)
- [Canlah AI](https://canlah.ai)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown prompt diff report with tables and a changelog snippet]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local prompt comparison; no external API is required.]

## Skill Version(s):

1.0.3 (source: server release metadata, target metadata, and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
