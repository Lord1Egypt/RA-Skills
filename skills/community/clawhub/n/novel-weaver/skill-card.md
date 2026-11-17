## Description:

Novel Weaver guides agents through structured fiction writing, from setting and outline planning through staged drafting, continuity checks, style checks, logic checks, fidelity reports, and ending verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ldxs001](https://clawhub.ai/user/ldxs001)

### License/Terms of Use:

MIT

## Use Case:

Writers, editors, and agent operators use this skill to plan, draft, and review long-form fiction through a gated workflow with character, timeline, continuity, style, logic, semantic, and ending checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional model installation may run unpinned package installs and Hugging Face model loading with trust_remote_code through third-party mirrors.

Mitigation: Run optional model setup only in an isolated environment after reviewing package and model sources; pin package versions when possible.

Risk: Filesystem and network permissions are under-disclosed relative to optional setup and local project writes.

Mitigation: Restrict execution to the intended project directory and grant network access only for explicit model installation.

Risk: Broad auto-activation on ordinary writing requests could route unrelated writing tasks into this workflow.

Mitigation: Enable the skill only for novel or long-form story-writing sessions, or require an explicit user trigger before activation.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/ldxs001/skills/novel-weaver)
- [Execution standards](references/execution_standards.md)
- [Workflow hooks](references/hooks.md)
- [Examples](references/examples.md)
- [FAQ](references/faq.md)
- [Permissions](references/permissions.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline JSON examples, shell commands, and generated manuscript text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates local novel project state, chapter files, and review reports through bundled scripts when invoked by an agent.]

## Skill Version(s):

1.35.4 (source: server release metadata, SKILL.md frontmatter, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
