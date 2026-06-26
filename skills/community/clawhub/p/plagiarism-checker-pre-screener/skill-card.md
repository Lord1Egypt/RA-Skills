## Description: <br>
Pre-screens supplied text for local similarity patterns, originality scoring, flagged segments, and paraphrasing suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Writers, reviewers, and developers use this skill to run a local pre-screen for repeated or highly similar passages in supplied text before manual review and revision. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is a local similarity pre-screener and does not check external plagiarism databases or internet sources. <br>
Mitigation: Use it as a triage aid and require manual review or external plagiarism checks before making publication, academic, or compliance decisions. <br>
Risk: An existing report file may be overwritten when an output path is supplied. <br>
Mitigation: Choose a deliberate output filename and review the destination before running with an output path. <br>
Risk: Document support is limited to text-readable files; docx support is not proven by the release security evidence. <br>
Mitigation: Convert documents to supported text or Markdown before analysis and verify that input extraction succeeded. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/aipoch-ai/plagiarism-checker-pre-screener) <br>
- [Algorithm Technical Documentation](references/algorithm.md) <br>
- [Paraphrasing Guide](references/paraphrasing_guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Guidance] <br>
**Output Format:** [JSON or plain-text report with originality score, flagged segments, and optional paraphrasing suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write a report file when an output path is provided; otherwise prints to stdout.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
