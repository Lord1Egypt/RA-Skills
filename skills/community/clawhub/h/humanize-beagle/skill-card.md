## Description:

Rewrite AI-generated developer text to sound human by fixing inflated language, filler, tautological docs, and robotic tone after review-ai-writing identifies issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical writers use this skill to clean up AI-generated repository text after a review-ai-writing scan. It can preview or apply categorized fixes to documentation, comments, messages, and other developer-facing prose while preserving meaning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically edit files based on .beagle/ai-writing-review.json, whose paths and contents may not be fully trustworthy.

Mitigation: Run it only in a clean, backed-up repository; prefer --dry-run first; trust the review file source; and validate that target paths stay inside the git worktree before applying fixes.

Risk: Validation may execute an unpinned npm package through npx -y for JavaScript or TypeScript files.

Mitigation: Use a pinned or locally installed JavaScript parser for validation, or review and approve any network-based package execution before running the skill.

Risk: Repository-wide cleanup can expose sensitive files or credentials to automated reads or edits.

Mitigation: Run the skill in a repository copy with sensitive files removed or access-limited, and review the resulting diff before keeping changes.

## Reference(s):

- [Humanize Beagle skill page](https://clawhub.ai/anderskev/skills/humanize-beagle)
- [Developer Voice Guidelines](references/developer-voice.md)
- [Fix Strategies by Category](references/fix-strategies.md)
- [Vocabulary Swap Reference](references/vocabulary-swaps.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown summaries, file edits, prompts, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports dry-run previews, category filtering, interactive review for higher-risk fixes, and per-file validation before cleanup.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
