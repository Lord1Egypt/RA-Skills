## Description:

Rewrite AI-generated developer text to sound human \u2014 fix inflated language, filler, tautological docs, and robotic tone.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and documentation maintainers use this skill after review-ai-writing to apply safe writing cleanups and review riskier edits across developer docs, commit text, code comments, and repository prose.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically edit repository files using paths and findings from .beagle/ai-writing-review.json.

Mitigation: Run with --dry-run first, inspect .beagle/ai-writing-review.json before applying fixes, and use it only with trusted review output.

Risk: Validator commands may create local code-execution risk when run in untrusted repositories or with unpinned tooling.

Mitigation: Avoid untrusted repositories and replace unpinned npx/Python validation patterns with path-safe, pinned, worktree-contained validators before broad use.

Risk: Automatic cleanup can change repository prose or code comments in ways that need human judgment.

Mitigation: Review proposed changes, use interactive confirmation for riskier fixes, and keep a recoverable working tree state before applying edits.

## Reference(s):

- [Developer Voice Guidelines](references/developer-voice.md)
- [Fix Strategies by Category](references/fix-strategies.md)
- [Vocabulary Swap Reference](references/vocabulary-swaps.md)
- [ClawHub release page](https://clawhub.ai/anderskev/skills/humanize-ai-writing)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown summaries, inline shell commands, and repository file edits]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports dry-run previews, category filtering, and interactive confirmation for riskier fixes.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
