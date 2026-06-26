## Description: <br>
Rewrite AI-generated developer text to sound human by fixing inflated language, filler, tautological docs, and robotic tone after review-ai-writing identifies issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill after review-ai-writing to turn AI-styled developer documentation, comments, commit text, and error messages into direct prose while preserving meaning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify repository files when applying safe or approved rewrites. <br>
Mitigation: Use --dry-run first, rely on the clean-worktree or stash gate, and review diffs before keeping changes. <br>
Risk: The skill depends on .beagle/ai-writing-review.json; stale or malformed review data can target the wrong text. <br>
Mitigation: Require the JSON shape and git_head checks, rerun review when stale, and stop on validation failure. <br>


## Reference(s): <br>
- [Developer Voice Guidelines](artifact/references/developer-voice.md) <br>
- [Fix Strategies by Category](artifact/references/fix-strategies.md) <br>
- [Vocabulary Swap Reference](artifact/references/vocabulary-swaps.md) <br>
- [ClawHub skill page](https://clawhub.ai/anderskev/humanize-beagle) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown summaries with inline shell commands and rewritten text or code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May modify repository files after review validation; dry-run mode previews changes without editing files.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
