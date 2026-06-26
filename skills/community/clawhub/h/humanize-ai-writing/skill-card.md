## Description: <br>
Rewrite AI-generated developer text to sound human - fix inflated language, filler, tautological docs, and robotic tone. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical writers use this skill after review-ai-writing to preview or apply edits that remove AI-writing patterns from developer documentation, comments, commit text, and related repository prose. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can rewrite files in the current repository, especially when run with --all. <br>
Mitigation: Run with --dry-run first and use a clean branch or committed worktree before applying changes. <br>
Risk: Automated prose changes can remove useful specificity or alter meaning. <br>
Mitigation: Review proposed changes, especially items classified as needing review, before accepting them. <br>
Risk: The workflow may create a git stash, revert files that fail validation, and delete the review JSON after a successful run. <br>
Mitigation: Check git status and preserve any needed review output before cleanup. <br>


## Reference(s): <br>
- [Developer Voice Guidelines](references/developer-voice.md) <br>
- [Fix Strategies by Category](references/fix-strategies.md) <br>
- [Vocabulary Swap Reference](references/vocabulary-swaps.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown summaries with inline shell commands and repository file edits] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports dry-run previews, category-filtered runs, and full-codebase runs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
