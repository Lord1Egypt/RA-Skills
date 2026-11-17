## Description:

Detects AI-writing patterns in Chinese MBA thesis text and provides reports, rewrite plans, and guidance for making revisions more natural and academically grounded.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stephenlzc](https://clawhub.ai/user/stephenlzc)

### License/Terms of Use:

MIT-0

## Use Case:

Students, editors, and academic writing assistants use this skill to evaluate Chinese MBA thesis drafts for AI-like wording, weak evidence, formatting issues, and repetitive structure. It supports transparent revision planning, citation-quality checks, and academically appropriate polishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is designed to reduce AI and plagiarism detection signals in MBA thesis text, which can support misrepresentation of academic work.

Mitigation: Use it only for transparent editing, formatting, and citation-quality checks on work the user is allowed to revise; do not use it to present AI-generated or copied work as original.

Risk: Optional auto-apply behavior may overwrite non-.txt files because of a reported edge case.

Mitigation: Avoid --apply on non-.txt files until the overwrite issue is fixed, and keep backups before applying automated edits.

Risk: Optional unpinned pip installation can introduce dependency supply-chain or environment drift risk.

Mitigation: Install optional dependencies only in an isolated environment and pin or review packages before use.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/stephenlzc/skills/humanize-mba-text-skill)
- [AI writing patterns](references/ai-writing-patterns.md)
- [MBA rewrite checklist](references/mba_rewrite_checklist.toml)
- [Chapter rewrite rules](references/chapter_rewrite_rules.toml)
- [Format standards](references/format-standards.md)
- [Strategy optimization](references/strategy_optimization.toml)
- [thesis-optimizer technical reference](https://github.com/Haimbeau1o/thesis-optimizer)
- [humanizer-academic-zh supplementary reference](https://github.com/cangtianhuang/humanizer-academic-zh)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown and JSON reports, rewrite plans, comparison summaries, and targeted editing guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include file-level reports, sentence-level risk annotations, and optional in-place spacing fixes.]

## Skill Version(s):

1.5.0 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
