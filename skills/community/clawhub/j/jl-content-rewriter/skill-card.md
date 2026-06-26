## Description: <br>
Rewrites Chinese articles into polished Markdown while preserving core meaning, reducing textual similarity, and improving readability. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pyzxs](https://clawhub.ai/user/pyzxs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External writers, editors, and content operators can use this skill to adapt source articles they own or are authorized to transform into cleaner, publication-ready Markdown. It is intended for rewriting, polishing, similarity review, and platform-fit guidance, not for disguising copied material. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is explicitly designed to lower plagiarism and AI-detection signals for publishing platforms. <br>
Mitigation: Use it only on content the user owns or is authorized to adapt, preserve attribution where required, and review the rewritten result before publication. <br>
Risk: Similarity and platform-risk scoring can create misplaced confidence that rewritten material is original or compliant. <br>
Mitigation: Treat similarity reports as editorial guidance only and perform independent copyright, platform-policy, and factual review. <br>
Risk: File-based workflows can write rewritten content to an unexpected local path when output environment variables are misconfigured. <br>
Mitigation: Review the configured output directory, suffix, and path-retention settings before running the skill on local files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pyzxs/jl-content-rewriter) <br>
- [AI humanizer guidance](references/ai-humanizer.md) <br>
- [Evaluation dimensions](references/evaluation-dimensions.md) <br>
- [Principled review](references/principled-review.md) <br>
- [Risk assessment](references/risk-assessment.md) <br>
- [User command flow](references/user-command.md) <br>
- [Word replacement guidance](references/word-replace.md) <br>
- [Writing polish guidance](references/writing-polish.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, guidance, configuration] <br>
**Output Format:** [Markdown article files with optional similarity reports and concise completion guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses configurable output directory, filename suffix, and path-retention environment variables when handling local files.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
