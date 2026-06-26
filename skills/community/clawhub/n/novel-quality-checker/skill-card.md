## Description: <br>
Checks Chinese novel chapter quality across 33 dimensions, including length, Chinese text purity, AI-marker phrases, templated endings, repetition, outline fit, and cross-chapter continuity, while reporting results in a five-layer audit. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shine8592](https://clawhub.ai/user/shine8592) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Writers, editors, and publishing teams use this skill to audit single chapters or batches of Chinese novel chapters for quality, formatting, style, and continuity issues. It is for review and reporting, not for generating or rewriting story content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Batch checks can read every matching chapter file in a selected directory, which may include private drafts the user did not intend to review. <br>
Mitigation: Invoke the skill with explicit file paths or a carefully scoped directory, and avoid directories that contain unrelated private drafts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shine8592/novel-quality-checker) <br>
- [Publisher profile](https://clawhub.ai/user/shine8592) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown and terminal-style quality audit reports with pass/fail indicators and metric values.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports quick checks, full 33-dimension checks, directory batch checks, and optional previous-chapter continuity checks.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
