## Description: <br>
Detect text originality and AI-generated content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlark](https://clawhub.ai/user/openlark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Writers, editors, educators, and developers use this skill to run local heuristic checks on submitted text and receive reference-only originality, AI-likelihood, paragraph analysis, and rewriting guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Heuristic originality and AI-generation scores can be inaccurate or produce false positives. <br>
Mitigation: Treat reports as reference signals and do not use them as the sole basis for academic, legal, employment, or disciplinary decisions. <br>
Risk: Quoted text, common technical terminology, and short passages may be flagged even when reuse is legitimate. <br>
Mitigation: Review flagged passages manually, check citations and context, and prefer longer inputs that meet the artifact's recommended minimum length. <br>
Risk: File-based checks can process sensitive drafts from local paths selected by the user. <br>
Mitigation: Run the skill only on intended files and review file paths before execution. <br>


## Reference(s): <br>
- [Detection Guide](artifact/references/detection-guide.md) <br>
- [Report Template](artifact/references/report-template.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/openlark/plagiarism-checker) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Plain text terminal report with markdown-compatible recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports include word and character counts, originality score, AI-generation probability, paragraph analysis, risk level, and recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
