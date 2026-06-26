## Description: <br>
Simulates NIH study section peer review for grant proposals, generating structured critiques, 1-9 criterion scores, weakness analysis, revision recommendations, and NIH-style summary statements. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AIPOCH-AI](https://clawhub.ai/user/AIPOCH-AI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Grant writers, researchers, and proposal teams use this skill to run a local mock NIH-style review before submission. It helps identify proposal weaknesses, calibrate scores, and prioritize revisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Confidential grant drafts may be processed through local input files and written to local output files. <br>
Mitigation: Use deliberate input and output paths, keep sensitive drafts in controlled workspaces, and remove generated review files when they are no longer needed. <br>
Risk: Generated critiques and scores are simulated and may be misleading if treated as authoritative NIH review outcomes. <br>
Mitigation: Review generated critiques before relying on them and use the output as preparation for human expert review, not as a replacement. <br>
Risk: PDF and DOCX extraction behavior is not implemented in the artifact script. <br>
Mitigation: Prefer TXT or Markdown inputs unless PDF or DOCX extraction has been verified separately. <br>


## Reference(s): <br>
- [NIH Scoring Rubric Reference](artifact/references/nih_scoring_rubric.md) <br>
- [Review Criteria Explained](artifact/references/review_criteria_explained.md) <br>
- [Common Weaknesses Catalog](artifact/references/common_weaknesses_catalog.md) <br>
- [Score Calibration Guide](artifact/references/score_calibration_guide.md) <br>
- [Summary Statement Templates](artifact/references/summary_statement_templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, guidance] <br>
**Output Format:** [Markdown-style summary statements and revision recommendations, or JSON score summaries when scores-only mode is used] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are written to stdout or to a user-selected local output path.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
